"""Decode all delivered PNGs and make alpha-aware previews; this is not a semantic completeness test."""
import argparse,hashlib,json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("run");p.add_argument("--tag",default="image-check")
    a=p.parse_args();run=Path(a.run).resolve(strict=True)
    if Path(a.tag).name!=a.tag or a.tag in (".",".."):p.error("Tag must be a file name")
    records=[];previews=[]
    for sub in ("assets","inferred"):
        for f in sorted((run/sub).rglob("*.png")):
            if not f.resolve().is_relative_to(run):raise ValueError("Output symlink escapes run")
            with Image.open(f) as im:im.verify()
            with Image.open(f) as im:
                im.load(); rgba=im.convert("RGBA"); alpha=rgba.getchannel("A")
                records.append(dict(path=f.relative_to(run).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),
                    size=list(im.size),mode=im.mode,alpha_extrema=alpha.getextrema(),
                    nonzero_alpha_bbox=alpha.getbbox(),bytes=f.stat().st_size))
                if "layers" not in f.relative_to(run).parts:
                    rgba.thumbnail((380,300))
                    bg=Image.new("RGBA",rgba.size,"#eeeeee");dr=ImageDraw.Draw(bg)
                    for y in range(0,bg.height,16):
                        for x in range(0,bg.width,16):
                            if (x//16+y//16)%2:dr.rectangle((x,y,x+15,y+15),fill="#d0d0d0")
                    bg.alpha_composite(rgba)
                    previews.append((f.relative_to(run).as_posix(),bg.convert("RGB")))
    if not records:raise ValueError("No delivered PNG files")
    summary=run/"logs"/(a.tag+".json");summary.parent.mkdir(exist_ok=True)
    with summary.open("x",encoding="utf-8") as f:
        json.dump(dict(check="PNG decode, dimensions, RGBA alpha and SHA256",images=records),f,ensure_ascii=False,indent=2)
    if previews:
        cols=3;cw,ch=400,350
        sheet=Image.new("RGB",(cw*cols,ch*math.ceil(len(previews)/cols)),"white")
        dr=ImageDraw.Draw(sheet)
        try:font=ImageFont.truetype("C:/Windows/Fonts/msyh.ttc",13)
        except OSError:font=ImageFont.load_default()
        for i,(label,im) in enumerate(previews):
            x=(i%cols)*cw;y=(i//cols)*ch
            sheet.paste(im,(x+(cw-im.width)//2,y+25))
            label=label.replace("assets/","").replace("inferred/","INFERRED/")
            dr.text((x+6,y+4),label[:50],font=font,fill="black")
        dest=run/"previews"/(a.tag+".jpg");dest.parent.mkdir(exist_ok=True)
        with dest.open("xb") as f:sheet.save(f,format="JPEG",quality=92)
    print(json.dumps(dict(run=str(run),decoded_pngs=len(records),previews=len(previews)),ensure_ascii=False))
if __name__=="__main__":main()
