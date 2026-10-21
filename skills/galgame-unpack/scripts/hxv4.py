"""Run the pinned static Hxv4 decoder on one archive/index or one selected entry."""
from pathlib import Path
import argparse,hashlib,json,os,re,subprocess,time,zlib
from adapter_io import output_path,save_json,sha256

DEFAULT_TOOL=os.environ.get("GALGAME_HXV4_TOOL_MANIFEST")

def linux(path):
    p=Path(path).resolve()
    if len(p.drive)!=2 or p.drive[1]!=":":raise ValueError("WSL input must be an absolute local drive path")
    return "/mnt/"+p.drive[0].lower()+p.as_posix()[2:]

def read_index(path,count=None):
    path=Path(path)
    if not 1<=path.stat().st_size<=128*1024*1024:raise ValueError("Invalid index size")
    lines=path.read_text("utf-8").splitlines()
    if not lines or lines[0]!="index\tname\tunpacked_size\tadler32\thx_info":raise ValueError("Invalid index header")
    rows=[]
    for expected,line in enumerate(lines[1:]):
        parts=line.split("\t",4)
        if len(parts)!=5 or int(parts[0])!=expected:raise ValueError("Incomplete/non-contiguous index")
        row={"index":expected,"name":parts[1],"size":int(parts[2]),"adler32":parts[3],"hx_info":parts[4]}
        if row["size"]<0 or not re.fullmatch("[0-9a-fA-F]{8}",row["adler32"]):raise ValueError("Invalid index record")
        rows.append(row)
    if not rows or (count is not None and len(rows)!=count):raise ValueError("Index count does not match completion marker")
    return rows

def checked_index(path):
    path=Path(path).resolve(strict=True);record=json.loads(Path(str(path)+".json").read_text("utf-8"))
    if record.get("kind")!="index" or record.get("status")!="verified":raise ValueError("Index has no completed verification")
    if sha256(path)!=record["sha256"]:raise ValueError("Index bytes changed")
    return read_index(path,record["entry_count"]),record

def lookup(path,name):
    rows,record=checked_index(path)
    digest=hashlib.blake2s((name+"xp3hnp").encode("utf-16le")).digest()
    matched=[]
    for row in rows:
        m=re.search(r"file_hash: \[([0-9, ]+)\]",row["hx_info"])
        if m and bytes(int(n.strip()) for n in m.group(1).split(","))==digest:matched.append(row)
    if len(matched)!=1:raise ValueError("Exact filename hash did not identify one entry")
    return matched[0]

def verify_payload(data,expected):
    """Verify original bytes or the pinned decoder's reversible Script type-1 output.

    The tool's source/src/process/script.rs swaps adjacent bits in UTF-16 words.
    Reconstruction is explicit evidence, never a generic allowance for mismatches.
    """
    def matches(raw):
        return len(raw)==expected["size"] and f"{zlib.adler32(raw)&0xffffffff:08x}"==expected["adler32"].lower()
    decoded={"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),"adler32":f"{zlib.adler32(data)&0xffffffff:08x}"}
    if matches(data):return {"verification":"original_payload","decoded_resource":decoded}
    if data.startswith(b"\xff\xfe") and len(data)%2==0 and len(data)+3==expected["size"]:
        swap=bytes(((value&0xaa)>>1)|((value&0x55)<<1) for value in range(256))
        reconstructed=b"\xfe\xfe\x01\xff\xfe"+data[2:].translate(swap)
        if matches(reconstructed):
            data[2:].decode("utf-16le",errors="strict")
            if b"\xff\xfe"+reconstructed[5:].translate(swap)!=data:raise ValueError("Text transform roundtrip failed")
            return {"verification":"reconstructed_type1_payload","transform":"kirikiri-script-type1-to-utf16le",
                    "decoded_resource":decoded,"archive_resource":{"bytes":len(reconstructed),
                    "adler32":expected["adler32"].lower(),"sha256":hashlib.sha256(reconstructed).hexdigest(),
                    "reconstructed":True},"boundary":"Only the pinned decoder's reversible type-1 script normalization; not raw bytes emitted by the decoder"}
    raise ValueError("Decoded resource size/Adler32 mismatch; no verified reversible transform")

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode",choices=["index","extract","find"])
    p.add_argument("--exe");p.add_argument("--archive");p.add_argument("--out")
    p.add_argument("--tool",default=DEFAULT_TOOL,help="Compatible bounded decoder manifest (or GALGAME_HXV4_TOOL_MANIFEST)");p.add_argument("--distro",default="Ubuntu")
    p.add_argument("--index-file");p.add_argument("--entry-index",type=int);p.add_argument("--name")
    p.add_argument("--timeout",type=int,default=600)
    a=p.parse_args()
    if a.mode=="find":
        if not a.index_file or not a.name:p.error("find requires --index-file and --name")
        print(json.dumps(lookup(a.index_file,a.name),ensure_ascii=False));return
    if not a.tool:p.error("--tool or GALGAME_HXV4_TOOL_MANIFEST is required; the external bounded decoder is not bundled")
    if not a.exe or not a.archive or not a.out:p.error("--exe, --archive and --out are required")
    if not 1<=a.timeout<=3600:p.error("Timeout must be 1..3600 seconds")
    exe=Path(a.exe).resolve(strict=True);archive=Path(a.archive).resolve(strict=True)
    out=output_path(a.out,[exe.parent,archive.parent]);temporary=Path(str(out)+".partial")
    log=Path(str(out)+".attempt.json")
    if temporary.exists() or log.exists():raise FileExistsError("Attempt/partial path exists; use a new output")
    toolfile=Path(a.tool).resolve(strict=True);tool=json.loads(toolfile.read_text("utf-8"))
    binary=(toolfile.parent/tool["binary"]).resolve(strict=True)
    if not binary.is_relative_to(toolfile.parent) or sha256(binary)!=tool["binary_sha256"]:
        raise ValueError("Pinned decoder hash/path mismatch")
    inputs={"exe_sha256":sha256(exe),"archive_sha256":sha256(archive),"binary_sha256":tool["binary_sha256"]}
    expected=None
    if a.mode=="extract":
        if not a.index_file or a.entry_index is None:p.error("extract requires verified --index-file and --entry-index")
        rows,index_record=checked_index(a.index_file)
        if any(index_record.get(k)!=v for k,v in inputs.items()):raise ValueError("Index belongs to different source/tool bytes")
        if not 0<=a.entry_index<len(rows):raise ValueError("Entry index out of range")
        expected=rows[a.entry_index]
        if expected["size"]>512*1024*1024:raise ValueError("Selected resource exceeds 512 MiB bound")
    out.parent.mkdir(parents=True,exist_ok=True)
    command=["wsl.exe","-d",a.distro,"--exec","timeout","--kill-after=5",str(a.timeout),
             linux(binary),linux(exe),linux(archive),linux(temporary),
             "--index" if a.mode=="index" else "#"+str(a.entry_index)]
    record=dict(inputs,argv=command,status="failed",kind=a.mode,source=str(archive),exe_as_data=str(exe),tool_manifest=str(toolfile))
    start=time.monotonic()
    try:
        completed=subprocess.run(command,capture_output=True,timeout=a.timeout+20)
        record.update(exit_code=completed.returncode,stdout=completed.stdout.decode("utf-8",errors="replace"),
                      stderr=completed.stderr.decode("utf-8",errors="replace"))
        if completed.returncode:raise RuntimeError("Static decoder failed; see attempt log")
        if a.mode=="index":
            markers=re.findall(r"^indexed (\d+) entries ->",record["stdout"],re.M)
            if len(markers)!=1:raise ValueError("Missing index completion marker")
            rows=read_index(temporary,int(markers[0]))
            record["entry_count"]=len(rows)
        else:
            raw=temporary.read_bytes()
            record.update(verify_payload(raw,expected))
            record["entry"]=expected
        temporary.rename(out)
        record.update(status="verified",output=str(out),sha256=sha256(out))
        save_json(str(out)+".json",record)
    except Exception as e:
        record["error"]=str(e);raise
    finally:
        record["elapsed_seconds"]=round(time.monotonic()-start,3);save_json(log,record)
    print(json.dumps({k:v for k,v in record.items() if k not in ["stdout","stderr","argv"]},ensure_ascii=False))
if __name__=="__main__":main()
