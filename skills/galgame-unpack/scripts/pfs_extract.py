"""Bounded pf8 index and exact-entry reader; preserve the original index for SHA1 XOR."""
from pathlib import Path
import argparse,hashlib,json,struct,io
from adapter_io import output_path,save_json,save_bytes

def read_index(source):
    source=Path(source)
    total=source.stat().st_size
    with source.open("rb") as f:
        head=f.read(7)
        if len(head)!=7 or head[:3]!=b"pf8":raise ValueError("Expected pf8 signature")
        length=struct.unpack_from("<I",head,3)[0]
        if not 4<=length<=min(256*1024*1024,total-7):raise ValueError("Invalid index length")
        raw=f.read(length)
    if len(raw)!=length:raise ValueError("Truncated index")
    count=struct.unpack_from("<I",raw)[0]
    if count>(length-4)//17:raise ValueError("Impossible entry count")
    pos=4;entries=[]
    for _ in range(count):
        if pos+4>length:raise ValueError("Truncated name length")
        n=struct.unpack_from("<I",raw,pos)[0];pos+=4
        if not 0<n<=4096 or pos+n+12>length:raise ValueError("Truncated or invalid index record")
        name=raw[pos:pos+n];pos+=n
        flag,offset,size=struct.unpack_from("<III",raw,pos);pos+=12
        entries.append({"name":name.decode("utf-8",errors="replace"),"_name":name,
                        "flag":flag,"offset":offset,"size":size,
                        "valid_bounds":offset>=7+length and size>0 and offset+size<=total})
    return raw,entries

def extract(source,name,max_bytes=128*1024*1024):
    raw,entries=read_index(source)
    matches=[e for e in entries if e["_name"]==name.encode("utf-8")]
    if len(matches)!=1:raise ValueError("Exact name must match one index entry")
    entry=matches[0]
    if not entry["valid_bounds"] or entry["size"]>max_bytes:
        raise ValueError("Selected entry has invalid bounds or exceeds the explicit size limit")
    with Path(source).open("rb") as f:
        f.seek(entry["offset"]);data=f.read(entry["size"])
    if len(data)!=entry["size"]:raise ValueError("Truncated payload")
    key=hashlib.sha1(raw).digest()
    data=bytes(b^key[i%len(key)] for i,b in enumerate(data))
    record={k:v for k,v in entry.items() if k!="_name"}
    record.update(source=str(Path(source).resolve()),source_bytes=Path(source).stat().st_size,
                  index_sha256=hashlib.sha256(raw).hexdigest(),xor_key_sha1=key.hex(),
                  index_entries=len(entries),invalid_bounds=sum(not e["valid_bounds"] for e in entries),
                  decoder="pf8-original-index-sha1-xor")
    return data,record

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode",choices=["index","extract"]);p.add_argument("source")
    p.add_argument("--entry");p.add_argument("--out",required=True)
    p.add_argument("--max-entry-mib",type=int,default=128)
    p.add_argument("--image",action="store_true",help="Require a decodable image; preserve its original bytes and comments")
    a=p.parse_args();source=Path(a.source).resolve(strict=True)
    out=output_path(a.out,[source.parent])
    if not 1<=a.max_entry_mib<=1024:p.error("Size limit must be 1..1024 MiB")
    if a.mode=="index":
        raw,entries=read_index(source)
        record={"source":str(source),"index_sha256":hashlib.sha256(raw).hexdigest(),
                "index_sha1":hashlib.sha1(raw).hexdigest(),"entry_count":len(entries),
                "invalid_bounds":sum(not e["valid_bounds"] for e in entries),
                "entries":[{k:v for k,v in e.items() if k!="_name"} for e in entries]}
        save_json(out,record)
        print(json.dumps({k:v for k,v in record.items() if k!="entries"},ensure_ascii=False));return
    if not a.entry:p.error("extract requires --entry")
    data,record=extract(source,a.entry,a.max_entry_mib*1024*1024)
    if a.image:
        from PIL import Image
        with Image.open(io.BytesIO(data)) as im:
            im.load();record.update(size=list(im.size),mode=im.mode,source_format=im.format)
    print(json.dumps(save_bytes(out,data,record),ensure_ascii=False))
if __name__=="__main__":main()
