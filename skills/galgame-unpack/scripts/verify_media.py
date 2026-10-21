"""Decode selected audio or text completely; keep semantic review in the manifest."""
from pathlib import Path
import argparse,codecs,json,unicodedata
from adapter_io import save_json,sha256

ENCODINGS={"utf-8","utf-8-sig","utf-16","utf-16-le","utf-16-be","cp932","shift_jis","gb18030","big5"}

def audio_info(path):
    import numpy as np
    import soundfile as sf
    path=Path(path)
    if not 0<path.stat().st_size<=512*1024*1024:raise ValueError("Audio size must be 1 byte..512 MiB")
    with sf.SoundFile(path,'r') as stream:
        if stream.format not in {"OGG","WAV","WAVEX","FLAC","MP3","AIFF"}:
            raise ValueError("Audio container is outside the supported verifier formats")
        rate,channels,frames=stream.samplerate,stream.channels,stream.frames
        if not 0<rate<=384000 or not 0<channels<=8 or not 0<frames<=rate*6*3600:
            raise ValueError("Unsupported audio dimensions/duration")
        decoded=0;peak=0.0;squares=0.0
        for block in stream.blocks(blocksize=65536,dtype="float32",always_2d=True):
            if not np.isfinite(block).all():raise ValueError("Non-finite decoded audio samples")
            decoded+=len(block)
            if len(block):peak=max(peak,float(np.abs(block).max()));squares+=float(np.square(block.astype('float64')).sum())
        if decoded!=frames:raise ValueError("Audio stream ended before its declared frame count")
        return {"samplerate":rate,"channels":channels,"frames":frames,"format":stream.format,"subtype":stream.subtype,
                "duration_seconds":frames/rate,"decoded_frames":decoded,"peak":peak,
                "rms":(squares/(frames*channels))**0.5,"silent":peak==0,
                "decoder":{"soundfile":sf.__version__,"libsndfile":sf.__libsndfile_version__}}

def text_info(path,encoding):
    path=Path(path)
    if not 0<path.stat().st_size<=64*1024*1024:raise ValueError("Text size must be 1 byte..64 MiB")
    canonical=codecs.lookup(encoding).name
    if canonical not in {codecs.lookup(name).name for name in ENCODINGS}:raise ValueError("Unsupported declared text encoding")
    text=path.read_bytes().decode(encoding,errors="strict")
    if not text.strip() or '\ufffd' in text:raise ValueError("Empty or replacement-character text")
    if any(unicodedata.category(c)=="Cc" and c not in '\r\n\t' for c in text):raise ValueError("Binary control characters in text")
    return {"encoding":encoding,"characters":len(text),"lines":len(text.splitlines()),"decode":"strict",
            "boundary":"Encoding and structure checked; meaning, language and dialogue completeness require content review"}

def inspect_media(path,row):
    kind=row["media_type"]
    if kind=="audio":
        actual=audio_info(path);expected=row.get("audio",{})
        for key in ["samplerate","channels","frames"]:
            if type(expected.get(key)) is not int or expected[key]!=actual[key]:raise ValueError("Audio metadata mismatch: "+key)
        for key in ["format","subtype"]:
            if key in expected and expected[key]!=actual[key]:raise ValueError("Audio metadata mismatch: "+key)
    elif kind=="text":
        expected=row.get("text",{});actual=text_info(path,expected["encoding"])
        if type(expected.get("characters")) is not int or expected["characters"]!=actual["characters"]:raise ValueError("Text character count mismatch")
    else:raise ValueError("Unsupported media_type")
    if row.get("complete") and not all(row.get(k) for k in ["classification_evidence","content_review","provenance"]):
        raise ValueError("Complete media lacks classification, content review or provenance")
    return {"media_type":kind,"verification":"full_decode" if kind=="audio" else "strict_text_decode",kind:actual}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("path");p.add_argument("--kind",choices=["audio","text"],required=True)
    p.add_argument("--encoding");p.add_argument("--out",required=True);a=p.parse_args()
    if a.kind=="text" and not a.encoding:p.error("Text requires --encoding based on source evidence")
    path=Path(a.path).resolve(strict=True)
    detail=audio_info(path) if a.kind=="audio" else text_info(path,a.encoding)
    result={"path":str(path),"sha256":sha256(path),"media_type":a.kind,a.kind:detail}
    save_json(a.out,result);print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
