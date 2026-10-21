"""Bounded Unity object inventory and exact-object PNG export; never executes game code."""
import argparse, collections, hashlib, json, re
from pathlib import Path
import UnityPy

def write_json(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("x", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def key(obj):
    return (obj.assets_file.name, obj.path_id)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=["inventory", "export"])
    p.add_argument("source")
    p.add_argument("--out", required=True)
    p.add_argument("--path-id", type=int)
    p.add_argument("--serialized")
    p.add_argument("--restore-dicing", action="store_true")
    args = p.parse_args()
    source = Path(args.source).resolve(strict=True)
    if not source.is_file():
        p.error("Supply a specific asset or bundle file, not a whole game folder")
    env = UnityPy.load(str(source))
    paths = collections.defaultdict(list)
    for name, ptr in env.container.items():
        try:
            obj = ptr.deref() if hasattr(ptr, "deref") else ptr
            paths[key(obj)].append(name)
        except Exception:
            continue
    objects = env.objects
    if args.command == "inventory":
        rows = []
        for obj in objects:
            if obj.type.name not in ("Texture2D", "Sprite", "MonoBehaviour", "TextAsset", "AssetBundle"):
                continue
            try:
                name = obj.peek_name()
            except Exception as e:
                name = ""
            row = dict(serialized=obj.assets_file.name, path_id=obj.path_id,
                       type=obj.type.name, name=name, container=paths[key(obj)])
            if obj.type.name in ("Sprite", "Texture2D"):
                data = obj.parse_as_object()
                if obj.type.name == "Sprite":
                    r=data.m_Rect
                    row["rect"]=[r.x,r.y,r.width,r.height]
                    row["pivot"]=[data.m_Pivot.x,data.m_Pivot.y]
                    row["pixels_to_units"]=data.m_PixelsToUnits
                else:
                    row["size"]=[data.m_Width,data.m_Height]
            rows.append(row)
        write_json(args.out, dict(source=str(source), unitypy=UnityPy.__version__,
             counts=dict(collections.Counter(o.type.name for o in objects)), objects=rows))
        print(json.dumps(dict(source=str(source), counts=dict(collections.Counter(o.type.name for o in objects))),ensure_ascii=False))
        return
    if args.path_id is None: p.error("export requires --path-id")
    matches = [o for o in objects if o.path_id == args.path_id and
               (args.serialized is None or o.assets_file.name == args.serialized)]
    if len(matches) != 1:
        raise ValueError("Expected one object; disambiguate with --serialized")
    obj=matches[0]
    if obj.type.name not in ("Sprite", "Texture2D"):
        raise ValueError("PNG export accepts only Sprite or Texture2D")
    if args.restore_dicing and obj.type.name != "Sprite":
        raise ValueError("--restore-dicing requires a Sprite object")
    out=Path(args.out)
    if out.exists() or Path(str(out)+".json").exists():
        raise FileExistsError("Output or sidecar already exists")
    data=obj.parse_as_object()
    reconstruction=None
    if args.restore_dicing:
        from sprite_mesh import restore
        im,reconstruction=restore(data)
    else:
        im=data.image
    out=Path(args.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("xb") as f: im.save(f,format="PNG")
    record=dict(source=str(source), serialized=obj.assets_file.name, path_id=obj.path_id,
                name=data.m_Name, type=obj.type.name, container=paths[key(obj)],
                output=str(out.resolve()), size=list(im.size), mode=im.mode,
                sha256=hashlib.sha256(out.read_bytes()).hexdigest(),unitypy=UnityPy.__version__)
    if reconstruction: record["reconstruction"]=reconstruction
    write_json(str(out)+".json",record)
    print(json.dumps({k:v for k,v in record.items() if k!="reconstruction"},ensure_ascii=False))

if __name__=="__main__": main()
