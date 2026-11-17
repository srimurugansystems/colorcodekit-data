"""Consistency check for the dataset. Standard library only.  python3 scripts/verify.py"""
import csv
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
rows = list(csv.DictReader((root / "data" / "css-named-colors.csv").open(encoding="utf-8")))
meta = json.loads((root / "data" / "css-named-colors.json").read_text(encoding="utf-8"))
errs = []
if len(rows) != meta["count"] or len(meta["colors"]) != meta["count"]:
    errs.append(f"row count: csv {len(rows)}, json {len(meta['colors'])}, declared {meta['count']}")
names = [r["name"] for r in rows]
if len(set(names)) != len(names):
    errs.append("duplicate names")
for r, j in zip(rows, meta["colors"]):
    h = r["hex"]
    if not (len(h) == 7 and h[0] == "#" and h == h.upper()):
        errs.append(f"{r['name']}: hex format {h}")
        continue
    rgb = (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16))
    if rgb != (int(r["r"]), int(r["g"]), int(r["b"])):
        errs.append(f"{r['name']}: hex {h} does not match r,g,b")
    if r["best_text"] not in ("#FFFFFF", "#000000"):
        errs.append(f"{r['name']}: best_text {r['best_text']}")
    if r["name"] != j["name"] or h != j["hex"]:
        errs.append(f"{r['name']}: csv and json disagree")
    if r["nearest_other"] not in names:
        errs.append(f"{r['name']}: nearest_other {r['nearest_other']} is not a name in the file")
    if r["nearest_other"] == r["name"]:
        errs.append(f"{r['name']}: nearest_other is itself")
print(f"{len(rows)} rows checked, {len(errs)} problems")
for e in errs[:20]:
    print(" ", e)
sys.exit(1 if errs else 0)
