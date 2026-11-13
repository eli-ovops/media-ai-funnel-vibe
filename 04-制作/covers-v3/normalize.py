"""Copy generation sources; use ffmpeg for proportional size normalization and QC previews."""
import hashlib
import json
import shutil
import struct
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FFMPEG = "/Users/USER/.local/bin/ffmpeg"

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def dimensions(path):
    with path.open("rb") as stream:
        header = stream.read(24)
    assert header[:8] == b"\x89PNG\r\n\x1a\n"
    return list(struct.unpack(">II", header[16:24]))

def run(args):
    subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error", "-nostdin", *args], check=True)

manifest = []
for item in json.loads((ROOT / "sources.json").read_text()):
    source = Path(item["source"])
    local = ROOT / "generated" / (item["ratio"] + "-source.png")
    shutil.copy2(source, local)
    w, h = item["width"], item["height"]
    target = ROOT / f"cover-{item['ratio']}-{w}x{h}-v3.png"
    run(["-i", str(local), "-vf",
         f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=white,setsar=1",
         "-frames:v", "1", str(target)])
    thumbnail = ROOT / "qc" / f"{item['ratio']}-320.png"
    run(["-i", str(target), "-vf", "scale=320:-1", "-frames:v", "1", str(thumbnail)])
    assert dimensions(target) == [w, h]
    manifest.append({
        **item, "generated_copy": str(local), "source_dimensions": dimensions(source),
        "source_sha256": digest(source), "file": str(target),
        "dimensions": dimensions(target), "bytes": target.stat().st_size,
        "sha256": digest(target), "thumbnail": str(thumbnail),
        "processing": "ffmpeg proportional scale and white padding; no cropping or content redraw",
    })
thumbs = [entry["thumbnail"] for entry in manifest]
args = []
for path in thumbs:
    args.extend(["-i", path])
filters = [f"[{i}:v]pad=320:570:0:(oh-ih)/2:color=white[t{i}]" for i in range(4)]
filters.append("[t0][t1][t2][t3]hstack=inputs=4[out]")
run([*args, "-filter_complex", ";".join(filters), "-map", "[out]", "-frames:v", "1",
     str(ROOT / "qc" / "contact-sheet.png")])
(ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(manifest, ensure_ascii=False, indent=2))
