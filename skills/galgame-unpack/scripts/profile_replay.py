"""Re-run a reviewed offline plan against exact inputs in a fresh directory.

This is an orchestration helper, not a sandbox for untrusted scripts or tools.
"""
from pathlib import Path, PureWindowsPath
import copy, hashlib, importlib.metadata, json, os, re, shutil, subprocess, sys, time
from adapter_io import sha256, save_json
from verify_run import check, selected_categories

TOKEN=re.compile(r"\{(SOURCE|RUN|PROFILE|PYTHON|TOOL:[A-Za-z0-9_-]+|TOOL_DIR:[A-Za-z0-9_-]+)\}")
ANY_TOKEN=re.compile(r"\{[A-Z][A-Z0-9_:.-]*\}")

def request_options(manifest,required=True):
    keys=("scope","requested_categories","extras","compose")
    if any(key not in manifest for key in keys):
        if required:raise ValueError("Replay requires explicit scope, requested_categories, extras and compose")
        return None
    selected_categories(manifest)
    if manifest["scope"] not in ("sample","full") or type(manifest["compose"]) is not bool:
        raise ValueError("Explicit scope and boolean compose required")
    if any(len(manifest[k])!=len(set(manifest[k])) for k in ("requested_categories","extras")):
        raise ValueError("Duplicate requested categories")
    return {key:copy.deepcopy(manifest[key]) for key in keys}

def same_request(a,b):
    return a["scope"]==b["scope"] and a["compose"]==b["compose"] and all(
        set(a[key])==set(b[key]) for key in ("requested_categories","extras"))

def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()

def runtime(packages):
    if not isinstance(packages,list) or any(not isinstance(p,str) or not p for p in packages):
        raise ValueError("python_packages must be a list of distribution names")
    paths=[str(Path(p).resolve()) for p in os.environ.get("PYTHONPATH","").split(os.pathsep) if p]
    return {"python_sha256":sha256(sys.executable),"python_version":list(sys.version_info[:3]),
            "pythonpath":paths,"packages":{name:importlib.metadata.version(name) for name in packages}}

def tools_by_id(tools):
    result={}
    for row in tools:
        key=row.get("id")
        if key is None:continue
        if not isinstance(key,str) or not re.fullmatch(r"[A-Za-z0-9_-]+",key) or key in result:
            raise ValueError("Tool ids must be unique simple names")
        result[key]=row
    return result

def validate_plan(plan,scripts,tools):
    if not isinstance(plan,dict) or plan.get("schema_version")!=1 or plan.get("mode")!="offline":
        raise ValueError("Only schema 1 reviewed offline plans can be replayed; runtime authorization is not inherited")
    if set(plan)-{"schema_version","mode","steps","python_packages"}:
        raise ValueError("Unknown replay plan fields")
    rows=plan.get("steps")
    if not isinstance(rows,list) or not rows:raise ValueError("Replay needs explicit steps")
    declared=tools_by_id(tools)
    known_scripts=set(scripts)
    for step in rows:
        if not isinstance(step,dict) or set(step)-{"argv","timeout_seconds"}:raise ValueError("Invalid replay step")
        argv=step.get("argv")
        if not isinstance(argv,list) or not argv or any(not isinstance(v,str) or not v or "\0" in v for v in argv):
            raise ValueError("Each step requires an argv list, never a shell string")
        timeout=step.get("timeout_seconds",300)
        if type(timeout) is not int or not 1<=timeout<=3600:raise ValueError("Step timeout must be 1..3600 seconds")
        if argv[0]=="{PYTHON}":
            if len(argv)<3 or argv[1]!="-B" or not argv[2].startswith("{PROFILE}/scripts/"):
                raise ValueError("Python steps must use -B and a snapshotted script")
            rel=argv[2][len("{PROFILE}/"):]
            if rel not in known_scripts or not rel.endswith(".py"):raise ValueError("Python entrypoint is not snapshotted")
        else:
            token=TOKEN.fullmatch(argv[0])
            if not token or not token[1].startswith("TOOL:"):raise ValueError("Entrypoint must be PYTHON or a declared offline tool")
            tool=declared.get(token[1][5:])
            if not tool or tool.get("kind")!="offline-decoder":
                raise ValueError("Executable tool requires kind=offline-decoder")
            if Path(tool["path"]).suffix.lower() in (".bat",".cmd",".ps1"):
                raise ValueError("Shell scripts are not replay entrypoints")
        for value in argv:
            matches=list(ANY_TOKEN.finditer(value))
            if matches and (len(matches)!=1 or matches[0].start()!=0 or not TOKEN.fullmatch(matches[0].group())):
                raise ValueError("Use one known path token at the start of a separate argv element")
            if not matches and (Path(value).is_absolute() or PureWindowsPath(value).is_absolute()):
                raise ValueError("Absolute command paths must use SOURCE/RUN/PROFILE/TOOL tokens")
            if matches:
                token=TOKEN.match(value)[1]
                if token.startswith(("TOOL:","TOOL_DIR:")) and token.split(":",1)[1] not in declared:
                    raise ValueError("Undeclared tool binding")
    return plan

def bind_arg(value,source,run,profile,tools):
    match=TOKEN.match(value)
    if not match:return value
    key=match[1];tail=value[match.end():]
    if key=="PYTHON":
        if tail:raise ValueError("PYTHON cannot have a path suffix")
        return sys.executable
    if key.startswith(("TOOL:","TOOL_DIR:")):
        row=tools[key.split(":",1)[1]]
        base=Path(row["path"]).resolve(strict=True)
        if base.is_relative_to(source):raise ValueError("Tools must stay outside the game directory")
        if key.startswith("TOOL:"):
            if tail:raise ValueError("TOOL cannot have a path suffix")
            return str(base)
        base=base.parent
    else:base={"SOURCE":source,"RUN":run,"PROFILE":profile}[key]
    if tail and not tail.startswith(("/","\\")):raise ValueError("Path suffix must begin with a separator")
    result=(base/tail.lstrip("/\\")).resolve()
    if not result.is_relative_to(base):raise ValueError("Bound path escapes its root")
    return str(result)

def transform(value,fn):
    if isinstance(value,str):return fn(value)
    if isinstance(value,list):return [transform(v,fn) for v in value]
    if isinstance(value,dict):return {k:transform(v,fn) for k,v in value.items()}
    return value

def portable_manifest(manifest,source,run):
    roots=sorted([(source,"{SOURCE}"),(run,"{RUN}")],key=lambda pair:len(str(pair[0])),reverse=True)
    def convert(value):
        for path,token in roots:
            for spelling in (str(path),path.as_posix()):
                if value==spelling:return token
                if value.startswith(spelling+"\\") or value.startswith(spelling+"/"):
                    return token+"/"+value[len(spelling)+1:].replace("\\","/")
        return value
    template=transform(manifest,convert)
    for key in ("run_id","output_root","validation","replay_execution"):
        template.pop(key,None)
    return template

def build_replay(manifest_path,manifest,scripts_root,plan):
    source=Path(manifest["source"]).resolve(strict=True)
    root=manifest_path.parent
    if scripts_root is None:raise ValueError("Replay requires --scripts-root")
    scripts_root=Path(scripts_root).resolve(strict=True)
    names=["scripts/"+p.name for p in scripts_root.iterdir() if p.is_file() and p.suffix in (".py",".cs",".ps1")]
    validate_plan(plan,names,manifest.get("tools",[]))
    request_options(manifest)
    for tool in manifest.get("tools",[]):
        if Path(tool["path"]).resolve().is_relative_to(root):
            raise ValueError("Move tool dependencies out of the old run into a durable tools directory")
    bindings=tools_by_id(manifest.get("tools",[]))
    for step in plan["steps"]:
        for value in step["argv"]:
            bind_arg(value,source,root,scripts_root.parent,bindings)
    return {"plan":copy.deepcopy(plan),"manifest_template":portable_manifest(manifest,source,root),
            "runtime":runtime(plan.get("python_packages",[]))}

def validate_saved(record):
    replay=record.get("replay")
    if not isinstance(replay,dict) or record.get("replay_sha256")!=digest(replay):
        raise ValueError("No intact executable replay plan; legacy commands require review and a new save")
    validate_plan(replay["plan"],[row["path"] for row in record["scripts"]],record.get("tools",[]))
    if not same_request(request_options(record["request"]),request_options(replay["manifest_template"])):
        raise ValueError("Saved request differs from the manifest template")
    return replay

def within(root,value):
    value=Path(value)
    if value.is_absolute() or PureWindowsPath(str(value)).is_absolute():raise ValueError("Replay paths must be relative")
    result=(root/value).resolve()
    if not result.is_relative_to(root):raise ValueError("Replay path escapes run")
    return result

def replay_profile(profile_path,source,run,request,execute,matcher):
    profile_path=Path(profile_path).resolve(strict=True);profile=profile_path.parent
    source=Path(source).resolve(strict=True);run=Path(run).resolve()
    if not source.is_dir():raise ValueError("Replay source must be the game root directory")
    if run.exists():raise FileExistsError("Run already exists; choose a fresh directory")
    if run.is_relative_to(source) or run.is_relative_to(profile):
        raise ValueError("Run must stay outside the game and profile")
    record=json.loads(profile_path.read_text("utf-8-sig"))
    saved=validate_saved(record)
    current_request=request_options(request)
    if not same_request(current_request,record["request"]):
        raise ValueError("Request differs from the saved scope/categories/extras/composition; prepare a new plan")
    match=matcher(profile_path,source)
    if not match.get("match"):raise ValueError("Profile mismatch: "+json.dumps(match,ensure_ascii=False))
    plan=saved["plan"]
    if runtime(plan.get("python_packages",[]))!=saved["runtime"]:
        raise ValueError("Python runtime, PYTHONPATH or declared package versions differ; revalidate before saving a new plan")
    tools=tools_by_id(record.get("tools",[]))
    bind=lambda text:bind_arg(text,source,run,profile,tools)
    commands=[{"argv":[bind(v) for v in step["argv"]],"timeout_seconds":step.get("timeout_seconds",300)} for step in plan["steps"]]
    template=saved["manifest_template"]
    manifest=transform(template,lambda text:TOKEN.sub(lambda m:bind_arg(m[0],source,run,profile,tools),text))
    manifest["source"]=str(source)
    for row in manifest["outputs"]:
        raw=Path(row["path"])
        if raw.is_absolute():
            if not raw.is_relative_to(run):raise ValueError("Output outside fresh run")
            row["path"]=raw.relative_to(run).as_posix()
        within(run,row["path"])
        if row.get("recipe"):
            p=Path(row["recipe"])
            if p.is_absolute():row["recipe"]=p.relative_to(run).as_posix()
            within(run,row["recipe"])
    copies=[]
    for entry in record.get("recipe_snapshots",[]):
        src=within(profile,entry["from"]);dst=within(run,entry["to"])
        if src.suffix.lower()!=".json" or not entry.get("sha256") or sha256(src)!=entry["sha256"]:
            raise ValueError("Replay requires intact JSON recipe snapshots")
        if dst==run/"manifest.json" or dst.is_relative_to(run/"logs"):
            raise ValueError("Recipe destination conflicts with replay metadata")
        copies.append((src,dst))
    preview={"profile":str(profile_path),"source":str(source),"run":str(run),"request":current_request,
             "status":"ready","execute":bool(execute),"steps":commands,"limitations":record.get("limitations",[]),
             "boundary":"Reviewed offline tools only; no inherited game/runtime authorization. Exact recorded output bytes required."}
    if not execute:return preview
    run.mkdir(parents=True,exist_ok=False)
    for name in ("assets/cg","assets/sprites","assets/layers","inferred","work/temp","logs"):
        (run/name).mkdir(parents=True,exist_ok=True)
    save_json(run/"logs"/"replay-plan.json",preview)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",PYTHONIOENCODING="utf-8",
             TMP=str(run/"work/temp"),TEMP=str(run/"work/temp"),TMPDIR=str(run/"work/temp"))
    started=time.monotonic();steps=[]
    try:
        for src,dst in copies:
            dst.parent.mkdir(parents=True,exist_ok=True)
            with dst.open("xb") as output:output.write(src.read_bytes())
        for index,step in enumerate(commands,1):
            outcome={"step":index,"argv":step["argv"]};steps.append(outcome)
            with (run/"logs"/f"step-{index:03}-stdout.txt").open("xb") as stdout, (run/"logs"/f"step-{index:03}-stderr.txt").open("xb") as stderr:
                process=subprocess.run(step["argv"],cwd=run,env=env,stdout=stdout,stderr=stderr,timeout=step["timeout_seconds"],shell=False)
            outcome["returncode"]=process.returncode
            if process.returncode:raise ValueError(f"Step {index} failed with exit code {process.returncode}; see logs")
        if not matcher(profile_path,source).get("match"):raise ValueError("Inputs or dependencies changed during replay")
        declared={within(run,row["path"]) for row in manifest["outputs"]}
        for directory in ("assets","inferred"):
            extra=[p for p in (run/directory).rglob("*") if p.is_file() and p.suffix.lower()!=".json" and p.resolve() not in declared]
            if extra:raise ValueError("Undeclared output: "+str(extra[0]))
        for row in manifest["outputs"]:
            if row.get("complete"):
                row["visual_review"]="Fresh output bytes match the saved reviewed sample; no new visual or in-game rendering review. Prior evidence: "+str(row.get("visual_review",""))
        manifest["replay_execution"]={"profile":str(profile_path),"profile_sha256":sha256(profile_path),
                                      "output_comparison":"Exact SHA-256 against previously verified outputs"}
        save_json(run/"manifest.json",manifest)
        verified=check(run/"manifest.json",verify_sources=True)
        save_json(run/"logs"/"verification.json",verified)
        result={"status":manifest["status"],"run":str(run),"manifest":str(run/"manifest.json"),
                "png_count":verified["png_count"],"complete_counts":verified["complete_counts"],
                "steps":steps,"seconds":time.monotonic()-started}
        (run/"report.md").write_text(
            "# Verified offline replay\n\nFresh outputs were recreated from matched game sources and checked against the saved hashes and recipes.\n\n"
            "Request: "+json.dumps(current_request,ensure_ascii=False)+"\n\n"
            "Status: "+manifest["status"]+"\n\nNo new visual classification or in-game rendering comparison. Recorded limitations still apply:\n\n"+
            json.dumps(record.get("limitations",[]),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    except (OSError,ValueError,KeyError,subprocess.SubprocessError) as error:
        # Do not leave a success manifest when its post-run verification failed.
        failed=copy.deepcopy(manifest);failed.update(status="blocked",outputs=[],unresolved=[{"category":"execution","reason":str(error)}])
        if (run/"manifest.json").exists():
            (run/"manifest.json").replace(run/"logs"/"rejected-manifest.json")
        save_json(run/"manifest.json",failed)
        result={"status":"blocked","run":str(run),"error":str(error),"steps":steps,"seconds":time.monotonic()-started}
        (run/"report.md").write_text("# Replay incomplete\n\n"+str(error)+"\n\nPartial files and logs remain for diagnosis; choose a new directory to retry.\n",encoding="utf-8")
    save_json(run/"logs"/"replay-result.json",result)
    return result
