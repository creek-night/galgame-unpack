"""Read a Naninovel layered prefab's default state and produce an explicitly approximate preview.
Supports local pointers, identity rotation/scale, and uniform pixels-per-unit.
Material shader/stencil reproduction is intentionally unresolved; output must be under inferred/.
"""
import argparse,json,math
from pathlib import Path
import UnityPy
from PIL import Image

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("source");p.add_argument("--out",required=True)
    a=p.parse_args(); out=Path(a.out).resolve()
    if "inferred" not in out.parts: p.error("Approximate output must be under inferred/")
    out.mkdir(parents=True,exist_ok=False)
    env=UnityPy.load(a.source)
    objects={o.path_id:o for o in env.objects}
    parsed={o.path_id:o.parse_as_dict() for o in env.objects if o.type.name in
            ("GameObject","Transform","SpriteRenderer","MonoBehaviour","Material")}
    def local(ptr):
        if ptr["m_FileID"]: raise ValueError("External object pointer requires dependency resolution")
        return ptr["m_PathID"]
    go={i:d for i,d in parsed.items() if objects[i].type.name=="GameObject"}
    tr={i:d for i,d in parsed.items() if objects[i].type.name=="Transform"}
    gt={local(d["m_GameObject"]):i for i,d in tr.items()}
    actors=[d for i,d in parsed.items() if "compositionMap" in d]
    if len(actors)!=1: raise ValueError("Expected one layered actor")
    actor=actors[0]; root=local(actor["m_GameObject"]); rt=gt[root]
    def chain(t):
        result=[]
        while t!=rt:
            if t in result: raise ValueError("Cyclic hierarchy")
            result.append(t); t=local(tr[t]["m_Father"])
        return result+[rt]
    renderer_transforms=[gt[local(d["m_GameObject"])] for i,d in parsed.items() if objects[i].type.name=="SpriteRenderer"]
    chains=[chain(t) for t in renderer_transforms]
    common=next(t for t in chains[0] if all(t in c for c in chains))
    common_path="/".join(go[local(tr[t]["m_GameObject"])]["m_Name"] for t in reversed(chain(common)[:-1]))
    def location(t,seen=()):
        if t in seen: raise ValueError("Cyclic transform")
        if t==common: return common_path,0.,0.,True
        d=tr[t]; rotation=d["m_LocalRotation"]; scale=d["m_LocalScale"]
        if any(abs(rotation[v])>1e-5 for v in "xyz") or abs(abs(rotation["w"])-1)>1e-5:
            raise ValueError("Rotated layer requires another compositor")
        if any(abs(scale[v]-1)>1e-5 for v in "xyz"):
            raise ValueError("Scaled layer requires another compositor")
        prefix,x,y,active=location(local(d["m_Father"]),seen+(t,))
        g=go[local(d["m_GameObject"])]
        return (prefix+"/"+g["m_Name"]).lstrip("/"),x+d["m_LocalPosition"]["x"],y+d["m_LocalPosition"]["y"],active and g["m_IsActive"]
    layers=[]
    for i,d in parsed.items():
        if objects[i].type.name!="SpriteRenderer": continue
        g=local(d["m_GameObject"]); name,x,y,active=location(gt[g])
        layers.append(dict(renderer=i,path=name,x=x,y=y,enabled=bool(d["m_Enabled"]) and active,data=d))
    aliases={v["Key"]:v["Composition"] for v in actor["compositionMap"]}
    expanded=[]
    def apply(text,stack=()):
        for term in text.split(","):
            term=term.strip()
            if term in aliases:
                if term in stack: raise ValueError("Cyclic appearance alias")
                apply(aliases[term],stack+(term,));continue
            expanded.append(term)
            if ">" in term:
                group,child=term.split(">",1); chosen=group+"/"+child
                affected=[l for l in layers if l["path"].startswith(group+"/")]
                if not affected or not any(l["path"]==chosen or l["path"].startswith(chosen+"/") for l in affected):
                    raise ValueError("Unresolved appearance branch: "+term)
                for l in affected: l["enabled"]=l["path"]==chosen or l["path"].startswith(chosen+"/")
            elif term.endswith("-"):
                group=term[:-1]
                affected=[l for l in layers if l["path"]==group or l["path"].startswith(group+"/")]
                if not affected: raise ValueError("Unresolved disabled group: "+term)
                for l in affected:l["enabled"]=False
            else: raise ValueError("Unsupported composition command: "+term)
    apply(actor["defaultAppearance"])
    chosen=sorted((l for l in layers if l["enabled"]),key=lambda l:l["data"]["m_SortingOrder"])
    ppu=None; records=[]; images=[]
    (out/"layers").mkdir()
    for n,l in enumerate(chosen):
        d=l["data"]; s=objects[local(d["m_Sprite"])].parse_as_object()
        if ppu is None: ppu=s.m_PixelsToUnits
        if s.m_PixelsToUnits!=ppu: raise ValueError("Mixed resolution")
        if d["m_FlipX"] or d["m_FlipY"]:raise ValueError("Flipped layer not supported here")
        if d["m_SortingLayerID"]:
            raise ValueError("Custom sorting layer or tint not supported")
        im=s.image.convert("RGBA")
        if im.size!=(round(s.m_Rect.width),round(s.m_Rect.height)):
            raise ValueError("Restore full Sprite canvas before composition")
        left=l["x"]*ppu-s.m_Pivot.x*im.width
        top=l["y"]*ppu+(1-s.m_Pivot.y)*im.height
        name=f"{n:02d}-{s.m_Name}.png"
        im.save(out/"layers"/name)
        mats=[parsed[local(m)] for m in d["m_Materials"]]
        records.append(dict(file="layers/"+name,path=l["path"],sprite_id=local(d["m_Sprite"]),
            left=left,top=top,size=list(im.size),sorting_order=d["m_SortingOrder"],
            tint=d["m_Color"],materials=[dict(name=m["m_Name"],properties=m["m_SavedProperties"]) for m in mats]))
        tint=[d["m_Color"][c] for c in "rgba"]
        im=Image.merge("RGBA",tuple(ch.point(lambda v,factor=factor: round(v*factor)) for ch,factor in zip(im.split(),tint)))
        images.append(im)
    if not images:raise ValueError("No visible layers")
    xmin=math.floor(min(r["left"] for r in records)+0.002)
    xmax=math.ceil(max(r["left"]+r["size"][0] for r in records)-0.002)
    ymin=math.floor(min(r["top"]-r["size"][1] for r in records)+0.002)
    ymax=math.ceil(max(r["top"] for r in records)-0.002)
    canvas=Image.new("RGBA",(xmax-xmin,ymax-ymin))
    for r,im in zip(records,images):
        r["position"]=[round(r["left"]-xmin),round(ymax-r["top"])]
        canvas.alpha_composite(im,tuple(r["position"]))
    canvas.save(out/"default-alpha-only.png")
    record=dict(source=str(Path(a.source).resolve()),actor=go[root]["m_Name"],
        default_appearance=actor["defaultAppearance"],expanded_commands=expanded,
        status="partial-inferred-rendering",
        evidence="Combination, transforms, pivots and layer order read from prefab metadata",
        unresolved=["Custom material multiply/overlay/softlight and stencil behavior not reproduced; preview uses normal alpha-over"],
        bounds=[xmin,ymin,xmax,ymax],coordinate_frame=common_path,common_transform=tr[common],layers=records)
    (out/"recipe.json").write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(dict(output=str(out),layers=len(records),status=record["status"]),ensure_ascii=False))
if __name__=="__main__":main()
