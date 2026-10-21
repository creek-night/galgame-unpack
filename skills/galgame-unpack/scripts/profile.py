"""Save verified provenance and script snapshots; find exact matching source/tool conditions."""
from pathlib import Path
import argparse,json,shutil,os
from adapter_io import sha256,save_json
from verify_run import check

def fingerprint(path,cache):
    path=Path(path).resolve(strict=True);before=path.stat()
    signature=(before.st_size,before.st_mtime_ns,before.st_ctime_ns)
    cached=cache.get(path)
    if cached is None or cached[0]!=signature:
        digest=sha256(path);after=path.stat()
        if signature!=(after.st_size,after.st_mtime_ns,after.st_ctime_ns):
            raise ValueError("File changed while hashing")
        cache[path]=(signature,digest)
    return cache[path][1]

def local_snapshot(root,value):
    value=Path(value)
    if value.is_absolute():raise ValueError("Snapshot path must be relative")
    path=(root/value).resolve(strict=True)
    if not path.is_relative_to(root.resolve()):raise ValueError("Snapshot escapes profile")
    if not path.is_file():raise ValueError("Snapshot is not a file")
    return path

def match(profile,source,cache=None):
    cache={} if cache is None else cache
    try:
        return match_record(profile,source,cache)
    except (OSError,ValueError,KeyError,TypeError,AttributeError) as error:
        return {"profile":str(profile),"match":False,"reason":"Invalid or unavailable profile dependency", "detail":str(error)}

def match_record(profile,source,cache):
    p=json.loads(Path(profile).read_text("utf-8-sig"));source=Path(source).resolve(strict=True)
    if p.get("schema_version")!=2:return {"profile":str(profile),"match":False,"reason":"legacy profile; inspect manually"}
    rows=p.get("fingerprints",[])
    if not rows:return {"profile":str(profile),"match":False,"reason":"no source fingerprints"}
    paths=[]
    for row in rows:
        path=(source/row["path"]).resolve()
        if not path.is_relative_to(source) or not path.is_file() or path.stat().st_size!=row["bytes"]:
            return {"profile":str(profile),"match":False,"reason":"source path/size differs","file":row["path"]}
        paths.append((path,row))
    for path,row in paths:
        if fingerprint(path,cache)!=row["sha256"]:
            return {"profile":str(profile),"match":False,"reason":"source hash differs","file":row["path"]}
    for row in p.get("scripts",[]):
        path=local_snapshot(Path(profile).parent,row["path"])
        if fingerprint(path,cache)!=row["sha256"]:
            return {"profile":str(profile),"match":False,"reason":"script snapshot changed"}
    warnings=[]
    for row in p.get("recipe_snapshots",[]):
        path=local_snapshot(Path(profile).parent,row["from"])
        if not row.get("sha256"):
            warnings.append("Historic recipe has no pinned digest; inspect before reuse")
        elif fingerprint(path,cache)!=row["sha256"]:
            return {"profile":str(profile),"match":False,"reason":"recipe snapshot changed","file":row["from"]}
    for row in p.get("tools",[]):
        path=Path(row["path"])
        if not path.is_absolute() or not path.is_file() or fingerprint(path,cache)!=row["sha256"]:
            return {"profile":str(profile),"match":False,"reason":"required tool differs","file":str(path)}
    if not p.get("tools"):warnings.append("No tool fingerprints declared; source match does not establish tool compatibility")
    return {"profile":str(profile),"match":True,"scope":p["scope"],"status":p["status"],
            "limitations":p["limitations"],"warnings":warnings,
            "reuse":"Only the recorded selectors and tool conditions; new output still requires verification"}

def dependencies(manifest):
    rows=manifest.get("tools",[])
    if not isinstance(rows,list):raise ValueError("tools must be a list")
    seen=set()
    for row in rows:
        path=Path(row["path"])
        if not path.is_absolute():raise ValueError("Tool path must be absolute")
        path=path.resolve(strict=True)
        if path in seen:raise ValueError("Duplicate tool dependency")
        seen.add(path)
        if not row.get("sha256") or sha256(path)!=row["sha256"]:raise ValueError("Declared tool hash differs: "+str(path))
        if "bytes" in row and path.stat().st_size!=row["bytes"]:raise ValueError("Tool size differs")
    return rows

def recipes(manifest,root):
    result=[];seen=set()
    for row in manifest["outputs"]:
        if not row.get("recipe"):continue
        value=Path(row["recipe"]);path=(value if value.is_absolute() else root/value).resolve(strict=True)
        if not path.is_relative_to(root):raise ValueError("Recipe escapes run")
        if path in seen:continue
        seen.add(path);recipe=json.loads(path.read_text("utf-8-sig"))
        for layer in recipe.get("layers",[]):
            for key in ["file","decoded_path"]:
                if key not in layer:continue
                value=Path(layer[key]);file=(value if value.is_absolute() else path.parent/value).resolve(strict=True)
                if not file.is_relative_to(root):raise ValueError("Recipe layer escapes run")
                layer[key]=Path(os.path.relpath(file,path.parent)).as_posix()
        relative=path.relative_to(root).as_posix()
        result.append(({"from":"recipes/"+relative,"to":relative,"original_sha256":sha256(path)},recipe))
    return result

def save(manifest,out,scripts_root=None,legacy=False,verify_sources=True):
    manifest=Path(manifest).resolve(strict=True)
    verified=check(manifest,legacy,verify_sources)
    m=json.loads(manifest.read_text("utf-8-sig"));source=Path(m["source"]).resolve(strict=True)
    if m["status"]=="blocked":raise ValueError("No successful capability to save")
    out=Path(out).resolve()
    if out.is_relative_to(source):raise ValueError("Profile must stay outside game")
    fingerprints=[]
    for item in m["sources"]:
        path=Path(item["path"]).resolve(strict=True)
        if not path.is_relative_to(source):raise ValueError("Source outside declared game root")
        if not item.get("sha256"):raise ValueError("Source fingerprint required")
        size=item.get("bytes",item.get("size",path.stat().st_size))
        fingerprints.append({"path":path.relative_to(source).as_posix(),"bytes":size,"sha256":item["sha256"]})
    if not fingerprints:raise ValueError("Source fingerprints required")
    tools=dependencies(m)
    recipe_data=recipes(m,manifest.parent)
    out.mkdir(parents=True,exist_ok=False)
    recipe_snapshots=[]
    for entry,recipe in recipe_data:
        dest=out/entry["from"];save_json(dest,recipe)
        recipe_snapshots.append(dict(entry,sha256=sha256(dest)))
    scripts=[]
    if scripts_root:
        scripts_root=Path(scripts_root)
        for path in sorted(scripts_root.iterdir()):
            if path.is_file() and path.suffix in [".py",".cs",".ps1"]:
                dest=out/"scripts"/path.name;dest.parent.mkdir(exist_ok=True);shutil.copy2(path,dest)
                scripts.append({"path":dest.relative_to(out).as_posix(),"sha256":sha256(dest)})
    record={"schema_version":2,"id":out.name,"game":m.get("game"),"engine":m.get("engine"),
            "scope":m["scope"],"status":m["status"],"source_hint":str(source),
            "fingerprints":fingerprints,"scripts":scripts,"tools":tools,"recipe_snapshots":recipe_snapshots,
            "selectors_and_provenance":m["outputs"],"verified_outputs":verified["outputs"],
            "limitations":verified["unresolved"]+m.get("limitations",[]),
            "evidence":[str(manifest),str(manifest.parent/"report.md")],
            "source_hashes_rechecked":verify_sources,
            "boundary":"Recorded sample only; unknown patch loading order and new combinations remain unverified"}
    save_json(out/"profile.json",record)
    save_json(out/"verification.json",verified)
    return {"profile":str(out/"profile.json"),"source_files":len(fingerprints),"scripts":len(scripts)}

def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest="mode",required=True)
    s=sub.add_parser("save");s.add_argument("manifest");s.add_argument("--out",required=True)
    s.add_argument("--scripts-root");s.add_argument("--legacy",action="store_true")
    m=sub.add_parser("match");m.add_argument("--profiles",required=True);m.add_argument("--source",required=True)
    a=p.parse_args()
    if a.mode=="save":result=save(a.manifest,a.out,a.scripts_root,a.legacy)
    else:
        root=Path(a.profiles);cache={}
        paths=[root] if root.is_file() else sorted(root.glob("*/profile.json"))
        result=[match(path,a.source,cache) for path in paths]
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
