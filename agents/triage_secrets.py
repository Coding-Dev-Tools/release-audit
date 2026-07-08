"""Triage the 7 remaining SEC-HARDCODED-SECRET hits by showing each one with context."""
import json
from pathlib import Path

OUT = Path(r"C:\Users\jomie\workspace\RELEASE-AUDIT\scorecards")
WORKSPACE = Path(r"C:\Users\jomie\workspace")

for p in sorted(OUT.glob("*.json")):
    d = json.loads(p.read_text(encoding="utf-8"))
    for a in d["angles"]:
        if a["angle"] != "security":
            continue
        for f in a.get("findings", []):
            if f["id"] != "SEC-HARDCODED-SECRET":
                continue
            for s in a.get("raw", {}).get("secrets", []):
                if s.get("in_test") or s.get("in_blog") or s.get("in_prose") or s.get("in_example"):
                    continue
                rel = s["file"]
                line = s["line"]
                fp = WORKSPACE / d["repo"] / rel
                if not fp.exists():
                    print(f"\n=== {d['repo']} ===  MISSING: {rel}:{line}  kind={s.get('kind')}")
                    continue
                text = fp.read_text(encoding="utf-8", errors="replace")
                lines = text.splitlines()
                lo = max(0, line - 2)
                hi = min(len(lines), line + 2)
                snippet = "\n".join(f"  {i+1:4d}: {lines[i]}" for i in range(lo, hi))
                print(f"\n=== {d['repo']} ===  {rel}:{line}  kind={s.get('kind')}\n{snippet}")
