"""Exact-name Light.vn mcdat reader, verified on the three local installations.
Algorithm: shiikwi/Light.VNRev commit d097884a5af32be37af5eaa058470d722271ba19.
"""
from pathlib import Path
import argparse,io,json
from adapter_io import output_path,save_json,save_bytes,save_png,sha256
KEY=b"d6c5fKI3GgBWpZF3Tz6ia3kF0"

def decode_index(data):
    b=bytearray(data)+b"\0";n=len(data)
    for i in range(n):
        b[i]^=KEY[i%len(KEY)];b[n-i]^=KEY[i%len(KEY)]
    return bytes(b[:n])

def decode(data):
    if len(data)<100:return decode_index(data) if data else data
    b=bytearray(data)
    for i in range(100):b[i]^=KEY[i%len(KEY)]
    for i in range(99):b[len(b)-99+i]^=KEY[::-1][i%len(KEY)]
    return bytes(b)

def unique_pairs(pairs):
    out={}
    for key,value in pairs:
        if key in out:raise ValueError("Duplicate index key")
        out[key]=value
    return out

def load_index(root):
    z=Path(root)/"Data/_/0.mcdat"
    if not 1<=z.stat().st_size<=16*1024*1024:raise ValueError("Index size outside supported range")
    names=json.loads(decode_index(z.read_bytes()).decode("utf-8-sig"),object_pairs_hook=unique_pairs)
    if not isinstance(names,dict) or any(not isinstance(k,str) or not isinstance(v,str) for k,v in names.items()):
        raise ValueError("Unsupported name mapping")
    return z,names

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode",choices=["index","raw","image"]);p.add_argument("root")
    p.add_argument("--entry");p.add_argument("--out",required=True)
    a=p.parse_args();root=Path(a.root).resolve(strict=True);out=output_path(a.out,[root])
    z,names=load_index(root)
    record={"index":str(z),"index_sha256":sha256(z),"decoder":"Light.VNRev-d097884a-bounded",
            "patch_policy":"Selected original mapping only; patch loading order unverified"}
    if a.mode=="index":
        save_json(out,dict(record,entries=names))
        print(json.dumps({"entries":len(names),"output":str(out)}));return
    if not a.entry:p.error("raw/image requires --entry")
    mapped=names[a.entry];source=(root/mapped).resolve(strict=True)
    if not source.is_relative_to(root) or not source.is_file():raise ValueError("Mapped source escapes game root")
    if source.stat().st_size>128*1024*1024:raise ValueError("Selected asset exceeds 128 MiB limit")
    data=decode(source.read_bytes())
    record.update(source=str(source),source_sha256=sha256(source),entry=a.entry,mapping=mapped)
    if a.mode=="raw":record=save_bytes(out,data,record)
    else:
        from PIL import Image
        with Image.open(io.BytesIO(data)) as im:
            im.load();record["source_format"]=im.format
            record=save_png(out,im,record)
    print(json.dumps(record,ensure_ascii=False))
if __name__=="__main__":main()
