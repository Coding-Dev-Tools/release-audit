"""List all per-repo findings of given types."""
import json
import sys
from pathlib import Path
from collections import defaultdict

OUT = Path(r"C:\Users\home\workspace\RELEASE-AUDIT\scorecards")
filter_ids = set(sys.argv[1:]) if len(sys.argv) > 1 else None

per_repo = defaultdict(list)
for p in sorted(OUT.glob("*.json")):
    d = json.loads(p.read_text(encoding="utf-8"))
    for a in d["angles"]:
        for f in a.get("findings", []):
            if filter_ids and f["id"] not in filter_ids:
                continue
            per_repo[d["repo"]].append((a["angle"], f["id"], f.get("msg", "")))

for repo, items in sorted(per_repo.items()):
    print(f"\n## {repo}")
    for ang, fid, msg in items:
        print(f"  - {ang} / {fid}: {msg[:120]}")
