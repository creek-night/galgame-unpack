"""Behavior tests for exact-input offline replay using generated PF8 data."""
from pathlib import Path
import copy,hashlib,importlib.util,io,json,os,shutil,struct,sys,tempfile,unittest
from PIL import Image

SCRIPTS=Path(os.environ.get("GALGAME_TEST_SCRIPTS",Path(__file__).resolve().parents[1]/"skills"/"galgame-unpack"/"scripts"))
sys.path.insert(0,str(SCRIPTS))
spec=importlib.util.spec_from_file_location("gal_profiles",SCRIPTS/"profile.py")
profiles=importlib.util.module_from_spec(spec);spec.loader.exec_module(profiles)
import profile_replay as replay
from adapter_io import sha256

class ReplayTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix="gal-replay-")
        self.root=Path(self.temp.name).resolve()
        self.assertTrue(self.root.is_relative_to(Path(tempfile.gettempdir()).resolve()))
        self.addCleanup(self.temp.cleanup)
        self.source=self.root/"source 游戏";self.source.mkdir()
        self.old=self.root/"old run";(self.old/"assets/cg").mkdir(parents=True)
        self.scripts=self.root/"scripts";self.scripts.mkdir()
        for name in ("pfs_extract.py","adapter_io.py"):
            shutil.copy2(SCRIPTS/name,self.scripts/name)
        payload=io.BytesIO();Image.new("RGBA",(2,3),(20,40,60,128)).save(payload,format="PNG")
        self.png=payload.getvalue();name=b"cg/sample.png";length=4+4+len(name)+12
        index=struct.pack("<II",1,len(name))+name+struct.pack("<III",0,7+length,len(self.png))
        key=hashlib.sha1(index).digest()
        archive=self.source/"input.pfs"
        archive.write_bytes(b"pf8"+struct.pack("<I",length)+index+bytes(b^key[i%20] for i,b in enumerate(self.png)))
        (self.old/"assets/cg/sample.png").write_bytes(self.png)
        self.request={"scope":"sample","requested_categories":["cg"],"extras":[],"compose":False}
        self.manifest=dict(self.request,schema_version=1,game="Generated fixture",source=str(self.source),status="passed",
            sources=[{"path":str(archive),"bytes":archive.stat().st_size,"sha256":sha256(archive)}],
            tools=[{"path":sys.executable,"sha256":sha256(sys.executable),"kind":"python-runtime"}],
            outputs=[{"path":"assets/cg/sample.png","sha256":hashlib.sha256(self.png).hexdigest(),"size":[2,3],
                "alpha_extrema":[128,128],"category":"cg","complete":True,"native_canvas_evidence":"Generated 2x3 PNG",
                "classification_evidence":"Declared generated fixture","visual_review":"Known generated pixels",
                "provenance":{"source":str(archive),"entry":"cg/sample.png"}}],unresolved=[])
        self.mpath=self.old/"manifest.json";self.write(self.mpath,self.manifest)
        self.plan={"schema_version":1,"mode":"offline","python_packages":["Pillow"],"steps":[
            {"argv":["{PYTHON}","-B","{PROFILE}/scripts/pfs_extract.py","extract","{SOURCE}/input.pfs",
                     "--entry","cg/sample.png","--image","--out","{RUN}/assets/cg/sample.png"],"timeout_seconds":10}]}
        self.planpath=self.root/"plan.json";self.write(self.planpath,self.plan)

    def write(self,path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding="utf-8")

    def save(self,plan=None,with_plan=True):
        if plan is not None:self.write(self.planpath,plan)
        out=self.root/"saved profile"
        result=profiles.save(self.mpath,out,self.scripts,replay_plan=self.planpath if with_plan else None)
        return Path(result["profile"])

    def run_replay(self,path,request=None,execute=True,source=None,out=None):
        return replay.replay_profile(path,source or self.source,out or self.root/"new run",
                                     self.request if request is None else request,execute,profiles.match)

    def test_preview_and_relocated_replay_do_not_need_old_outputs(self):
        path=self.save()
        preview=self.run_replay(path,execute=False)
        self.assertEqual(preview["status"],"ready")
        self.assertFalse((self.root/"new run").exists())
        # Both rename targets are explicitly inside this test's owned temporary root.
        moved=self.root/"moved source";self.source.rename(moved)
        old_hidden=self.root/"old evidence unavailable";self.old.rename(old_hidden)
        relocated=self.root/"relocated profile";path.parent.rename(relocated)
        result=self.run_replay(relocated/"profile.json",source=moved)
        self.assertEqual(result["status"],"passed")
        self.assertEqual((self.root/"new run/assets/cg/sample.png").read_bytes(),self.png)
        m=json.loads((self.root/"new run/manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(replay.request_options(m),self.request)
        self.assertTrue((self.root/"new run/logs/verification.json").is_file())
        self.assertEqual(sha256(moved/"input.pfs"),self.manifest["sources"][0]["sha256"])

    def test_preserves_request_on_save_without_replay(self):
        path=self.save(with_plan=False)
        d=json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(d["request"],self.request)
        self.assertTrue(profiles.match(path,self.source)["match"])
        with self.assertRaisesRegex(ValueError,"executable replay plan"):self.run_replay(path)
        self.assertFalse((self.root/"new run").exists())

    def test_rejects_each_request_change_before_creating_run(self):
        path=self.save()
        for field,value in [("scope","full"),("requested_categories",["cg","sprites"]),("extras",["bgm"]),("compose",True)]:
            with self.subTest(field=field):
                request=dict(self.request,**{field:value})
                with self.assertRaisesRegex(ValueError,"Request differs"):self.run_replay(path,request=request)
                self.assertFalse((self.root/"new run").exists())

    def test_changed_source_stops_before_execution(self):
        path=self.save()
        archive=self.source/"input.pfs";data=bytearray(archive.read_bytes());data[-1]^=1;archive.write_bytes(data)
        with self.assertRaisesRegex(ValueError,"Profile mismatch"):self.run_replay(path)
        self.assertFalse((self.root/"new run").exists())

    def test_changed_script_stops_before_execution(self):
        path=self.save();script=path.parent/"scripts/pfs_extract.py"
        script.write_bytes(script.read_bytes()+b"\n# changed\n")
        with self.assertRaisesRegex(ValueError,"Profile mismatch"):self.run_replay(path)
        self.assertFalse((self.root/"new run").exists())

    def test_changed_declared_tool_stops_before_execution(self):
        dependency=self.root/"dependency.dat";dependency.write_bytes(b"old")
        self.manifest["tools"].append({"path":str(dependency),"sha256":sha256(dependency),"kind":"dependency"})
        self.write(self.mpath,self.manifest);path=self.save();dependency.write_bytes(b"new")
        with self.assertRaisesRegex(ValueError,"Profile mismatch"):self.run_replay(path)
        self.assertFalse((self.root/"new run").exists())

    def test_runtime_drift_stops_before_execution(self):
        path=self.save();record=json.loads(path.read_text(encoding="utf-8"))
        record["replay"]["runtime"]["python_version"]=[0,0,0]
        record["replay_sha256"]=replay.digest(record["replay"]);self.write(path,record)
        with self.assertRaisesRegex(ValueError,"Python runtime"):self.run_replay(path)
        self.assertFalse((self.root/"new run").exists())

    def test_existing_directory_and_source_destination_are_refused(self):
        path=self.save();out=self.root/"new run";out.mkdir();(out/"keep.txt").write_text("keep",encoding="utf-8")
        with self.assertRaises(FileExistsError):self.run_replay(path)
        self.assertEqual((out/"keep.txt").read_text(encoding="utf-8"),"keep")
        with self.assertRaisesRegex(ValueError,"outside the game"):self.run_replay(path,out=self.source/"child")
        self.assertFalse((self.source/"child").exists())

    def test_plan_tampering_is_detected(self):
        path=self.save();record=json.loads(path.read_text(encoding="utf-8"))
        record["replay"]["plan"]["steps"][0]["argv"][-1]="{RUN}/elsewhere.png";self.write(path,record)
        self.assertFalse(profiles.match(path,self.source)["match"])
        with self.assertRaisesRegex(ValueError,"intact executable"):self.run_replay(path)

    def test_unsafe_or_unportable_plans_are_refused_at_save(self):
        variants=[]
        plan=copy.deepcopy(self.plan);plan["mode"]="runtime";variants.append(plan)
        plan=copy.deepcopy(self.plan);plan["steps"][0]["argv"]="echo invalid";variants.append(plan)
        plan=copy.deepcopy(self.plan);plan["steps"][0]["argv"][-1]="{RUN}/../outside.png";variants.append(plan)
        plan=copy.deepcopy(self.plan);plan["steps"][0]["argv"][2]="{PROFILE}/scripts/not-saved.py";variants.append(plan)
        plan=copy.deepcopy(self.plan);plan["steps"][0]["argv"][0]=sys.executable;variants.append(plan)
        for plan in variants:
            with self.subTest(plan=plan):
                with self.assertRaises(ValueError):self.save(plan)
                self.assertFalse((self.root/"saved profile").exists())

    def test_failed_step_stops_later_steps_and_records_blocked(self):
        (self.scripts/"fail.py").write_text("raise SystemExit(7)\n",encoding="utf-8")
        (self.scripts/"marker.py").write_text("import sys\nfrom pathlib import Path\nPath(sys.argv[1]).write_text('ran')\n",encoding="utf-8")
        self.plan["steps"]=[
            {"argv":["{PYTHON}","-B","{PROFILE}/scripts/fail.py"]},
            {"argv":["{PYTHON}","-B","{PROFILE}/scripts/marker.py","{RUN}/should-not-exist"]}]
        path=self.save(self.plan);result=self.run_replay(path)
        self.assertEqual(result["status"],"blocked")
        self.assertFalse((self.root/"new run/should-not-exist").exists())
        self.assertEqual(len(result["steps"]),1)
        m=json.loads((self.root/"new run/manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(m["status"],"blocked")
        self.assertEqual(m["outputs"],[])
        self.assertTrue((self.root/"new run/logs/replay-result.json").is_file())

    def test_wrong_fresh_bytes_cannot_leave_passed_manifest(self):
        (self.scripts/"wrong.py").write_text(
            "import sys\nfrom pathlib import Path\np=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'wrong')\n",encoding="utf-8")
        self.plan["steps"]=[{"argv":["{PYTHON}","-B","{PROFILE}/scripts/wrong.py","{RUN}/assets/cg/sample.png"]}]
        path=self.save(self.plan);result=self.run_replay(path)
        self.assertEqual(result["status"],"blocked")
        m=json.loads((self.root/"new run/manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(m["status"],"blocked")
        self.assertTrue((self.root/"new run/logs/rejected-manifest.json").is_file())

    def test_timeout_stops_and_records_failure(self):
        (self.scripts/"slow.py").write_text("import time\ntime.sleep(20)\n",encoding="utf-8")
        self.plan["steps"]=[{"argv":["{PYTHON}","-B","{PROFILE}/scripts/slow.py"],"timeout_seconds":1}]
        path=self.save(self.plan);result=self.run_replay(path)
        self.assertEqual(result["status"],"blocked")
        self.assertIn("timed out",result["error"])

if __name__=="__main__":unittest.main()
