"""Small shared I/O helpers for explicit, read-only extraction adapters."""
from pathlib import Path
import hashlib,json

def sha256(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f,"sha256").hexdigest()

def output_path(path,source_roots=()):
    out=Path(path).resolve()
    for source in source_roots:
        source=Path(source).resolve()
        if out==source or out.is_relative_to(source):
            raise ValueError("Output must stay outside the source directory")
    if out.exists() or Path(str(out)+".json").exists():
        raise FileExistsError("Output or sidecar exists; choose a new path")
    return out

def save_json(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("x",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

def save_bytes(out,data,record):
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("xb") as f:f.write(data)
    record=dict(record,output=str(out),sha256=sha256(out),bytes=out.stat().st_size)
    save_json(str(out)+".json",record)
    return record

def save_png(out,image,record):
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    image.load()
    with out.open("xb") as f:image.save(f,format="PNG")
    record=dict(record,output=str(out),sha256=sha256(out),size=list(image.size),
                mode=image.mode,alpha_extrema=list(image.convert("RGBA").getchannel("A").getextrema()))
    save_json(str(out)+".json",record)
    return record
