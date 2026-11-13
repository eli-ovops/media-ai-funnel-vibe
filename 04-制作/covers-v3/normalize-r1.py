import hashlib
import json
import shutil
import struct
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parent
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def dims(p):
    return list(struct.unpack(">II", p.read_bytes()[16:24]))
def run(args):
    subprocess.run(["/Users/USER/.local/bin/ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", *args], check=True)
record = json.loads((root / "generation-r1.json").read_text())
source = Path(record["source"])
local = root / "generated/9x16-source-r1.png"
shutil.copy2(source, local)
target = root / "cover-9x16-1080x1920-v3-r1.png"
run(["-i", str(local), "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=white,setsar=1", "-frames:v", "1", str(target)])
thumb = root / "qc/9x16-320-r1.png"
run(["-i", str(target), "-vf", "scale=320:-1", "-frames:v", "1", str(thumb)])
items = json.loads((root / "manifest.json").read_text())
for item in items:
    if item["ratio"] == "9x16":
        item.update(source=str(source), generated_copy=str(local), source_dimensions=dims(source),
                    source_sha256=sha(source), file=str(target), dimensions=dims(target),
                    bytes=target.stat().st_size, sha256=sha(target), thumbnail=str(thumb), revision="v3-r1")
    else:
        assert sha(Path(item["file"])) == item["sha256"]
        item["revision"] = "v3 unchanged"
assert dims(target) == [1080, 1920]
args = []
for item in items:
    args.extend(["-i", item["thumbnail"]])
filters = [f"[{i}:v]pad=320:570:0:(oh-ih)/2:color=white[t{i}]" for i in range(4)]
filters.append("[t0][t1][t2][t3]hstack=inputs=4[out]")
run([*args, "-filter_complex", ";".join(filters), "-map", "[out]", "-frames:v", "1", str(root / "qc/contact-sheet-r1.png")])
(root / "manifest-r1.json").write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(items[1], ensure_ascii=False, indent=2))
