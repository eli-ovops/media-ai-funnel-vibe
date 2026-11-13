"""Read-only pixel measurement; does not edit image content."""
import json
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parent.parent
cases = [
    ("3x4", "cover-3x4-1080x1440-v4.png", (20, 1060, 230, 450), (530, 1020, 450, 650)),
    ("9x16", "cover-9x16-1080x1920-v4.png", (10, 1060, 390, 630), (530, 1030, 630, 830)),
    ("4x3", "cover-4x3-1440x1080-v4.png", (60, 1380, 230, 430), (750, 1150, 430, 650)),
]
results = []
for ratio, filename, title_roi, hair_roi in cases:
    im = Image.open(root / filename).convert("RGB")
    def rows(roi, threshold):
        x0, x1, y0, y1 = roi
        return [y for y in range(y0, y1) if any(max(im.getpixel((x, y))) < threshold for x in range(x0, x1))]
    last = max(rows(title_roi, 180))
    first = min(rows(hair_roi, 200))
    results.append({"ratio": ratio, "title_roi": title_roi, "hair_roi": hair_roi,
                    "last_dark_text_y": last, "first_dark_hair_y": first, "gap_rows": first-last-1})
im = Image.open(root / "cover-16x9-1920x1080-v4.png").convert("RGB")
right = max(x for x in range(50,1200) if any(min(im.getpixel((x,y)))<150 for y in range(50,500)))
left = min(x for x in range(1200,1800) if any(max(im.getpixel((x,y)))<200 for y in range(40,320)))
results.append({"ratio":"16x9", "title_right_x":right, "hair_left_x":left, "horizontal_gap_columns":left-right-1})
data={"method":"RGB pixel thresholds + separate visual full-image/thumbnail review; excludes faint near-white antialiasing; not subpixel contour measurement", "results":results}
(root / "qc/spacing.json").write_text(json.dumps(data, indent=2)+"\n")
print(json.dumps(data, indent=2))
