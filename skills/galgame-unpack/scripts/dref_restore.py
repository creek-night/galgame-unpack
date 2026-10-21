"""Restore an evidenced two-entry DREF from one plain PSB package, preserving PNG layers."""
from pathlib import Path
import argparse,hashlib,io,json,re,struct,zlib
from PIL import Image
from psb_extract import PSB
from adapter_io import save_json,save_bytes,save_png,sha256

def references(path):
    path=Path(path)
    if not 0<path.stat().st_size<=65536:raise ValueError("DREF size outside supported range")
    data=path.read_bytes();encoding='utf-16' if data.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig'
    lines=[line.strip() for line in data.decode(encoding).splitlines() if line.strip()]
    if len(lines)!=2:raise ValueError("Only evidenced base+one-difference DREF is supported")
    result=[]
    for line in lines:
        m=re.fullmatch(r'psb://([^/\\:]+\.dpak)/([^/\\:]+\.png)',line)
        if not m or '..' in m.groups():raise ValueError("Unsupported DREF resource reference")
        result.append({'package':m.group(1),'entry':m.group(2)})
    if result[0]['package']!=result[1]['package']:raise ValueError("Cross-package DREF requires separate mapping")
    return result

def png_metadata(data):
    if data[:8]!=b'\x89PNG\r\n\x1a\n':raise ValueError("Resource is not PNG")
    position=8;meta={};ended=False
    while position<len(data):
        if position+12>len(data):raise ValueError("Truncated PNG chunk")
        size=struct.unpack_from('>I',data,position)[0];tag=data[position+4:position+8];end=position+12+size
        if end>len(data):raise ValueError("PNG chunk exceeds file")
        body=data[position+8:position+8+size];crc=struct.unpack_from('>I',data,position+8+size)[0]
        if zlib.crc32(tag+body)&0xffffffff!=crc:raise ValueError("PNG chunk CRC mismatch")
        if tag in [b'oFFs',b'vpAg']:
            key=tag.decode('ascii')
            if key in meta or size!=9:raise ValueError("Invalid/duplicate PNG coordinate chunk")
            x,y,unit=struct.unpack('>iiB' if tag==b'oFFs' else '>IIB',body)
            if unit!=0:raise ValueError("Only pixel-unit PNG placement is supported")
            meta[key]=[x,y]
        if tag==b'IEND':
            if size or end!=len(data):raise ValueError("Invalid PNG end/trailing data")
            ended=True;break
        position=end
    if not ended:raise ValueError("PNG has no IEND")
    with Image.open(io.BytesIO(data)) as im:
        im.load();image=im.convert('RGBA')
    return image,meta

def restore(dref,package,out):
    dref=Path(dref).resolve(strict=True);package=Path(package).resolve(strict=True);out=Path(out).resolve()
    if out.exists():raise FileExistsError("DREF output directory exists")
    if any(out.is_relative_to(p.parent) for p in [dref,package]):raise ValueError("Output must stay outside source directories")
    refs=references(dref)
    if refs[0]['package']!=package.name:raise ValueError("Package name does not match explicit DREF reference")
    psb=PSB(package);payload=[]
    for ref in refs:
        data,index=psb.resource(ref['entry']);im,meta=png_metadata(data);payload.append((data,index,im,meta))
    base=payload[0][2];difference=payload[1][2];metadata=payload[1][3]
    if 'oFFs' not in metadata or metadata.get('vpAg')!=list(base.size):raise ValueError("Missing or conflicting native canvas/offset metadata")
    x,y=metadata['oFFs']
    if min(x,y)<0 or x+difference.width>base.width or y+difference.height>base.height:raise ValueError("Difference clips the original canvas")
    if any(value and index not in [0,255] for index,value in enumerate(difference.getchannel('A').histogram())):
        raise ValueError("Fractional-alpha difference needs explicit engine blending evidence")
    canvas=base.copy();canvas.alpha_composite(difference,(x,y))
    independent=base.copy();independent.paste(difference,(x,y),difference.getchannel('A'))
    if independent.tobytes()!=canvas.tobytes():raise ValueError("Independent binary-mask composition mismatch")
    out.mkdir(parents=True,exist_ok=False);rows=[]
    for i,(ref,(data,index,im,meta)) in enumerate(zip(refs,payload)):
        dest=out/'layers'/f'{i:02d}.png'
        record=save_bytes(dest,data,{'source':str(package),'source_sha256':sha256(package),'entry':ref['entry'],'resource_index':index,'png_metadata':meta})
        rows.append(dict(record,file=dest.relative_to(out).as_posix(),position=[0,0] if i==0 else [x,y]))
    recipe={'canvas':list(base.size),'preserve_base_rgba':True,'evidence':'Explicit DREF order, exact PSB names, PNG oFFs/vpAg, binary alpha; independent mask replacement equals alpha-over.',
            'layers':[{'file':row['file'],'position':row['position']} for row in rows]}
    save_json(out/'recipe.json',recipe)
    output=save_png(out/'result.png',canvas,{'source':str(package),'source_sha256':sha256(package),'dref':str(dref),'dref_sha256':sha256(dref),'references':refs,'recipe':'recipe.json','layers':rows,'verification':'independent binary-mask and alpha-over pixels equal','boundary':'Metadata-supported static image; no in-game patch-order or camera-effects comparison'})
    return output

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('dref');p.add_argument('--package',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    result=restore(a.dref,a.package,a.out);print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
