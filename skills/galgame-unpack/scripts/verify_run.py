"""Validate a completed extraction manifest, PNG bytes and explicit alpha-over recipes."""
from pathlib import Path
import argparse,collections,json
from PIL import Image
from adapter_io import sha256,save_json

def contained(root,value):
    p=Path(value);p=(p if p.is_absolute() else root/p).resolve(strict=True)
    if not p.is_relative_to(root):raise ValueError("Output/recipe escapes run")
    return p

def unresolved_rows(values,legacy=False):
    if not isinstance(values,list):raise ValueError("unresolved must be a list")
    result=[]
    for value in values:
        if legacy and isinstance(value,str):result.append({"category":"unspecified","reason":value})
        elif isinstance(value,dict) and isinstance(value.get("reason"),str) and value["reason"].strip():
            if not legacy and (not isinstance(value.get("category"),str) or not value["category"].strip()):
                raise ValueError("Unresolved item requires a category")
            result.append(value)
        else:raise ValueError("Unresolved item requires a reason")
    return result

def selected_categories(manifest,legacy=False):
    if legacy:return manifest.get("requested_categories",["cg","sprites"])
    selected=manifest.get("requested_categories")
    extras=manifest.get("extras",[])
    for name,values in [("requested_categories",selected),("extras",extras)]:
        if not isinstance(values,list) or (name=="requested_categories" and not values):
            raise ValueError(name+" must be an explicit nonempty list" if name=="requested_categories" else name+" must be a list")
        if any(not isinstance(value,str) or not value.strip() or value!=value.strip() for value in values):
            raise ValueError(name+" must contain category names")
    return list(dict.fromkeys(selected+extras))

def verify_recipe(run,recipe_path,output,legacy=False):
    recipe_path=contained(run,recipe_path)
    recipe=json.loads(recipe_path.read_text("utf-8"))
    if legacy and recipe.get("coordinate_source") and recipe.get("draw_order"):
        # Earlier PBD recipes record the same geometry under explicit metadata keys.
        recipe={"canvas":recipe["canvas"],"evidence":recipe["coordinate_source"]+"; "+recipe["draw_order"],
                "layers":[{"file":layer["decoded_path"],
                           "position":[layer["source_metadata"]["left"],layer["source_metadata"]["top"]]}
                          for layer in recipe["layers"]]}
    if not recipe.get("evidence"):raise ValueError("Composition evidence missing")
    width,height=recipe["canvas"]
    if not 0<width*height<=100_000_000:raise ValueError("Invalid recipe canvas")
    canvas=Image.new("RGBA",(width,height))
    if not recipe.get("layers"):raise ValueError("Recipe has no layers")
    preserve=recipe.get("preserve_base_rgba",False)
    if type(preserve) is not bool:raise ValueError("preserve_base_rgba must be boolean")
    for index,layer in enumerate(recipe["layers"]):
        if layer.get("blend","normal")!="normal":raise ValueError("Only explicit normal alpha-over can be recomposed")
        path=contained(run,str(recipe_path.parent/layer["file"]))
        im=Image.open(path).convert("RGBA");x,y=layer["position"]
        if type(x) is not int or type(y) is not int or min(x,y)<0 or x+im.width>width or y+im.height>height:
            raise ValueError("Recipe clips/rescales its source layer")
        if preserve and index==0:
            if [x,y]!=[0,0] or im.size!=(width,height):raise ValueError("Preserved base must fill the canvas at [0,0]")
            canvas=im.copy()
        else:
            canvas.alpha_composite(im,(x,y))
    im=Image.open(output).convert("RGBA")
    if im.size!=canvas.size or im.tobytes()!=canvas.tobytes():raise ValueError("Composed pixels/canvas differ from recipe")
    return str(recipe_path)

def check(manifest,legacy=False,verify_sources=False):
    manifest=Path(manifest).resolve(strict=True);run=manifest.parent
    m=json.loads(manifest.read_text("utf-8-sig"))
    if m.get("scope") not in ["sample","full"]:raise ValueError("Explicit scope required")
    if m.get("status") not in ["passed","partial","blocked"]:raise ValueError("Final status required")
    unresolved=unresolved_rows(m.get("unresolved",[]),legacy)
    requested=selected_categories(m,legacy)
    if not isinstance(m.get("sources"),list):raise ValueError("sources must be a list")
    source_checks=[]
    if verify_sources:
        for source in m["sources"]:
            path=Path(source["path"]).resolve(strict=True)
            if not source.get("sha256") or sha256(path)!=source["sha256"]:raise ValueError("Source hash mismatch: "+str(path))
            source_checks.append(str(path))
    outputs=[];unverified=[];seen=set();counts=collections.Counter();png_count=0;media_counts=collections.Counter()
    for row in m["outputs"]:
        if not legacy and any(k not in row for k in ["path","sha256","category","complete"]):
            raise ValueError("Output requires canonical path/sha256/category/complete")
        raw=row.get("path") or row.get("file") or row.get("output")
        f=contained(run,raw)
        if f in seen:raise ValueError("Duplicate manifest output")
        seen.add(f)
        if sha256(f)!=row["sha256"]:raise ValueError("Output hash mismatch: "+str(f))
        category={"layer":"layers","sprite":"sprites"}.get(row.get("category"),row.get("category"))
        complete=row.get("complete")
        if not legacy:
            if not isinstance(category,str) or not category.strip():raise ValueError("Output category required")
            if type(complete) is not bool:raise ValueError("complete must be boolean")
        if f.suffix.lower()!=".png" and row.get("media_type") in ["audio","text"]:
            from verify_media import inspect_media
            detail=inspect_media(f,row)
            if complete:
                if "inferred" in f.relative_to(run).parts or category in ["layers","inferred"]:
                    raise ValueError("Inferred/component cannot be complete")
                counts[category]+=1
            if row.get("recipe"):raise ValueError("Image composition recipe cannot validate audio/text")
            media_counts[row["media_type"]]+=1
            outputs.append(dict(detail,path=f.relative_to(run).as_posix(),sha256=row["sha256"],category=category,complete=complete))
            continue
        if f.suffix.lower()!=".png":
            if not legacy and complete:raise ValueError("Output has no selected decoder validation; complete must be false: "+str(f))
            unverified.append({"path":f.relative_to(run).as_posix(),"sha256":row["sha256"],
                               "category":category,"complete":False,"verification":"hash_only",
                               "reason":"No selected decoder establishes usability of this file type",
                               "declared_complete":complete})
            continue
        if not legacy and "size" not in row:raise ValueError("PNG output requires size")
        if row.get("media_type") not in [None,"image"]:raise ValueError("PNG cannot declare an audio/text media type")
        with Image.open(f) as im:
            if im.format!="PNG":raise ValueError("PNG extension does not match actual image format")
            im.load();size=list(im.size);alpha=list(im.convert("RGBA").getchannel("A").getextrema())
        expected=row.get("size") or row.get("dimensions") or [row.get("width"),row.get("height")]
        if size!=list(expected):raise ValueError("Image dimensions differ from manifest")
        if "alpha_extrema" in row and alpha!=list(row["alpha_extrema"]):raise ValueError("Image alpha differs from manifest")
        if complete:
            if "inferred" in f.relative_to(run).parts or category in ["layers","inferred"]:raise ValueError("Inferred/component cannot be complete")
            if not legacy and not all(row.get(k) for k in ["native_canvas_evidence","classification_evidence","visual_review","provenance"]):
                raise ValueError("Complete output lacks evidence")
            counts[category]+=1
        recipe=None;recipe_limitation=None
        if row.get("recipe"):
            metadata_path=contained(run,row["recipe"])
            metadata=json.loads(metadata_path.read_text("utf-8"))
            if legacy and not complete and category=="inferred" and metadata.get("status")=="partial-inferred-rendering":
                recipe_limitation="Diagnostic prefab metadata only; custom shader/stencil rendering not verified"
                limitation={"category":"inferred","reason":recipe_limitation,"recipe":str(metadata_path)}
                if limitation not in unresolved:unresolved.append(limitation)
            else:
                recipe=verify_recipe(run,row["recipe"],f,legacy)
        png_count+=1
        outputs.append({"path":f.relative_to(run).as_posix(),"sha256":row["sha256"],
                        "size":size,"alpha_extrema":alpha,"category":category,"complete":complete,
                        "recipe_verified":recipe,"recipe_limitation":recipe_limitation})
    if not outputs and m["status"]!="blocked":raise ValueError("No verified outputs")
    if not legacy and m["status"]=="passed":
        for category in requested:
            if not counts[category]:raise ValueError("Passed without requested complete category: "+category)
        for issue in unresolved:
            category={"layer":"layers","sprite":"sprites"}.get(issue["category"],issue["category"])
            if category in requested or (category=="coverage" and m["scope"]=="full"):
                raise ValueError("Passed with unresolved requested capability: "+category)
    return {"manifest":str(manifest),"scope":m["scope"],"status":m["status"],"legacy":legacy,
            "png_count":png_count,"media_counts":dict(media_counts),"complete_counts":dict(counts),"outputs":outputs,
            "requested_categories":requested,"unverified_outputs":unverified,
            "source_hashes_verified":source_checks,"unresolved":unresolved,
            "boundary":"PNG/recipes, selected full audio decode and strict text decode checked; other files hash-only. Counts do not establish coverage, semantic correctness or patch order"}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("manifest")
    p.add_argument("--legacy",action="store_true",help="Read earlier field aliases; incomplete semantics remain unspecified")
    p.add_argument("--sources",action="store_true");p.add_argument("--out",required=True);a=p.parse_args()
    result=check(a.manifest,a.legacy,a.sources);save_json(a.out,result)
    print(json.dumps({k:v for k,v in result.items() if k not in ["outputs","unresolved","source_hashes_verified","unverified_outputs"]},ensure_ascii=False))
if __name__=="__main__":main()
