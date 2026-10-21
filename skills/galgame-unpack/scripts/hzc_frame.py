"""Decode one explicitly selected BGRA frame from an HZC1/NVSG resource."""
from pathlib import Path
import argparse,json,struct,zlib
from PIL import Image
from adapter_io import output_path,save_png,sha256

def read_frame(source,frame):
    data=Path(source).read_bytes()
    if len(data)<40 or data[:4]!=b"hzc1" or data[12:16]!=b"NVSG":raise ValueError("Expected HZC1/NVSG")
    unpacked,header=struct.unpack_from("<II",data,4)
    kind,w,h,x,y=struct.unpack_from("<HHHhh",data,18)
    if kind!=2 or not w or not h:raise ValueError("Only verified BGRA kind 2 is supported")
    size=w*h*4
    if not 0<unpacked<=512*1024*1024 or unpacked%size:raise ValueError("Invalid decoded size")
    count=unpacked//size
    if not 0<=frame<count:raise ValueError("Frame outside stored frame count")
    if not 28<=header<len(data)-12:raise ValueError("Invalid NVSG header length")
    dec=zlib.decompressobj();raw=dec.decompress(data[12+header:],unpacked+1)
    if len(raw)!=unpacked or not dec.eof or dec.unconsumed_tail or dec.unused_data:
        raise ValueError("Truncated or oversized compressed payload")
    return Image.frombytes("RGBA",(w,h),raw[frame*size:(frame+1)*size],"raw","BGRA"),[x,y],count

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("source")
    p.add_argument("--frame",type=int,required=True);p.add_argument("--out",required=True);a=p.parse_args()
    source=Path(a.source).resolve(strict=True);out=output_path(a.out,[source.parent])
    im,offset,count=read_frame(source,a.frame)
    record={"source":str(source),"source_sha256":sha256(source),"frame":a.frame,
            "frame_count":count,"offset":offset,"decoder":"hzc1-nvsg-bgra-zlib",
            "offset_meaning":"Native metadata; distinguish relative face offset from scene placement"}
    print(json.dumps(save_png(out,im,record),ensure_ascii=False))
if __name__=="__main__":main()
