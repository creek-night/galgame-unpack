"""Create a non-overwriting extraction run under the user's output root."""
import argparse, datetime, json, os, re, uuid
from pathlib import Path
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root",default=os.environ.get("GALGAME_UNPACK_OUTPUT_ROOT") or str(Path.home()/"galgame-unpack-output"),help="Output root (or GALGAME_UNPACK_OUTPUT_ROOT; defaults to ~/galgame-unpack-output)")
    p.add_argument("--game",required=True)
    p.add_argument("--source",required=True)
    p.add_argument("--compose",choices=["yes","no"],required=True)
    p.add_argument("--categories",default="cg,sprites",help="Selected resource categories; defaults to cg,sprites")
    p.add_argument("--extras",default="",help="Comma-separated explicitly chosen extra categories")
    p.add_argument("--scope",choices=["sample","full"],required=True)
    a=p.parse_args()
    categories=[v.strip() for v in a.categories.split(",") if v.strip()]
    if not categories or len(categories)!=len(set(categories)):p.error("Choose nonempty, unique categories")
    source=Path(a.source).resolve(strict=True)
    root=Path(a.root).expanduser().resolve()
    if source.is_dir() and root.is_relative_to(source):
        p.error("Output root must be outside the read-only game directory")
    game=re.sub(r'[<>:"/\\|?*\x00-\x1f]',"_",a.game).strip(" .")
    if not game or game.upper() in {"CON","PRN","AUX","NUL",*[f"COM{i}" for i in range(10)],*[f"LPT{i}" for i in range(10)]}:
        p.error("Invalid game directory name")
    run_id=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+"-"+uuid.uuid4().hex[:8]
    run=root/game/run_id
    run.mkdir(parents=True,exist_ok=False)
    for d in ["assets/cg","assets/sprites","assets/layers","inferred","work","scripts","logs","previews"]:
        (run/d).mkdir(parents=True)
    record=dict(schema_version=1,game=a.game,source=str(source),output_root=str(root),run_id=run_id,
                scope=a.scope,compose=a.compose=="yes",requested_categories=categories,extras=[v.strip() for v in a.extras.split(",") if v.strip()],
                status="in_progress",sources=[],outputs=[],unresolved=[])
    (run/"manifest.json").write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding="utf-8")
    print(run)
if __name__=="__main__": main()
