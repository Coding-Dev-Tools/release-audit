"""Triage SEC-INJECTION-SINK hits for a single repo."""
import json
import sys
from pathlib import Path

if len(sys.argv) < 2:
    sys.exit("usage: triage_sinks.py <repo>")
repo = sys.argv[1]
WORKSPACE = Path(r"C:\Users\home\workspace")
OUT = WORKSPACE / "RELEASE-AUDIT" / "scorecards" / f"{repo}.json"
d = json.loads(OUT.read_text(encoding="utf-8"))
for a in d["angles"]:
    if a["angle"] != "security":
        continue
    for f in a.get("findings", []):
        if f["id"] != "SEC-INJECTION-SINK":
            continue
        for s in a.get("raw", {}).get("sinks", []):
            if s.get("in_test") or s.get("in_blog"):
                continue
            rel = s["file"]
            line = s["line"]
            kind = s["kind"]
            fp = WORKSPACE / repo / rel
            if not fp.exists():
                continue
            text = fp.read_text(encoding="utf-8", errors="replace")
            lines = text.splitlines()
            lo = max(0, line - 2)
            hi = min(len(lines), line + 2)
            snippet = "\n".join(f"  {i+1:4d}: {lines[i]}" for i in range(lo, hi))
            print(f"\n=== {repo} ===  {rel}:{line}  kind={kind}\n{snippet}")
