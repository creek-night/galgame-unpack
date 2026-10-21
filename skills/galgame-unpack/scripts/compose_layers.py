"""Compose explicitly evidenced RGBA layers at original pixel coordinates."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("recipe")
    p.add_argument("--out",required=True)
    a=p.parse_args()
    recipe=Path(a.recipe).resolve(strict=True)
    d=json.loads(recipe.read_text(encoding="utf-8-sig"))
    if not d.get("evidence"): raise ValueError("Recipe must explain combination and placement evidence")
    w,h=d["canvas"]
    if not (0<w<=32768 and 0<h<=32768 and w*h<=100_000_000): raise ValueError("Invalid canvas")
    canvas=Image.new("RGBA",(w,h))
    preserve=d.get("preserve_base_rgba",False)
    if type(preserve) is not bool: raise ValueError("preserve_base_rgba must be boolean")
    if not d.get("layers"): raise ValueError("Recipe has no layers")
    used=[]
    for index,layer in enumerate(d["layers"]):
        if layer.get("blend","normal")!="normal": raise ValueError("Only normal alpha-over is supported")
        f=(recipe.parent/layer["file"]).resolve(strict=True)
        im=Image.open(f).convert("RGBA")
        x,y=layer["position"]
        if not isinstance(x,int) or not isinstance(y,int): raise ValueError("Positions must be integral pixels")
        if x<0 or y<0 or x+im.width>w or y+im.height>h: raise ValueError("Layer would be clipped")
        if preserve and index==0:
            if [x,y]!=[0,0] or im.size!=(w,h): raise ValueError("Preserved base must fill the canvas at [0,0]")
            canvas=im.copy()
        else:
            canvas.alpha_composite(im,(x,y))
        used.append(dict(file=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),position=[x,y]))
    out=Path(a.out)
    if out.exists() or Path(str(out)+".json").exists(): raise FileExistsError("Output or sidecar already exists")
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("xb") as f: canvas.save(f,format="PNG")
    with Path(str(out)+".json").open("x",encoding="utf-8") as f:
        json.dump(dict(algorithm="rgba-preserve-base-alpha-over-v1" if preserve else "rgba-alpha-over-v1",evidence=d["evidence"],layers=used,
                       output=str(out.resolve()),sha256=hashlib.sha256(out.read_bytes()).hexdigest()),f,ensure_ascii=False,indent=2)
    print(out)
if __name__=="__main__": main()
