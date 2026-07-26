#!/usr/bin/env python3
"""Build a summary report from per-repo scorecards."""
from __future__ import annotations
import json
from collections import Counter, defaultdict
from pathlib import Path

OUT_DIR = Path(r"C:\Users\home\workspace\RELEASE-AUDIT\scorecards")
SUMMARY_PATH = Path(r"C:\Users\home\workspace\RELEASE-AUDIT\SUMMARY.json")
SUMMARY_MD = Path(r"C:\Users\home\workspace\RELEASE-AUDIT\SUMMARY.md")

data = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
repos = data["repos"]

# Aggregate findings by id
finding_counter = Counter()
finding_by_repo = defaultdict(list)
per_angle_grade = defaultdict(list)
for r in repos:
    for a in r["angles"]:
        per_angle_grade[a["angle"]].append((r["repo"], a["grade"]))
        for f in a.get("findings", []):
            finding_counter[f["id"]] += 1
            finding_by_repo[r["repo"]].append(f)

# Sort repos by overall grade (D first = needs most help)
def grade_key(g):
    return {"A": 0, "B": 1, "C": 2, "D": 3}[g]

repos_sorted = sorted(repos, key=lambda r: (-grade_key(r["overall_grade"]), r["repo"]))

# Build markdown
lines = []
lines.append("# Release Readiness Summary")
lines.append("")
lines.append(f"- Repos audited: **{len(repos)}**")
lines.append(f"- A-grade: {sum(1 for r in repos if r['overall_grade']=='A')}")
lines.append(f"- B-grade: {sum(1 for r in repos if r['overall_grade']=='B')}")
lines.append(f"- C-grade: {sum(1 for r in repos if r['overall_grade']=='C')}")
lines.append(f"- D-grade: {sum(1 for r in repos if r['overall_grade']=='D')}")
lines.append("")
lines.append("## Per-Repo Scorecard")
lines.append("")
lines.append("| Repo | Overall | Pass | Blockers |")
lines.append("|------|---------|-----:|---------:|")
for r in repos_sorted:
    lines.append(f"| `{r['repo']}` | **{r['overall_grade']}** | {r['angles_passing']}/8 | {r['blockers']} |")
lines.append("")
lines.append("## Top Common Findings (across all repos)")
lines.append("")
lines.append("| Finding ID | Repos affected |")
lines.append("|------------|---------------:|")
for fid, n in finding_counter.most_common(30):
    lines.append(f"| `{fid}` | {n} |")
lines.append("")
lines.append("## Per-Angle Grade Distribution")
lines.append("")
lines.append("| Angle | A | B | C | D |")
lines.append("|-------|--:|--:|--:|--:|")
for ang in ("security","dependencies","tests","lint-types","dead-code","errors-logging","docs","release"):
    counts = Counter(g for _, g in per_angle_grade[ang])
    lines.append(f"| {ang} | {counts.get('A',0)} | {counts.get('B',0)} | {counts.get('C',0)} | {counts.get('D',0)} |")
lines.append("")
lines.append("## Repos Sorted By Priority (worst first)")
lines.append("")
for r in repos_sorted:
    lines.append(f"### `{r['repo']}` — grade {r['overall_grade']} ({r['angles_passing']}/8 passing, {r['blockers']} blocker(s))")
    blocker_angles = [a for a in r["angles"] if a["grade"] == "D"]
    if blocker_angles:
        for a in blocker_angles:
            lines.append(f"- **BLOCKER** `{a['angle']}`: " + "; ".join(f["msg"] for f in a["findings"]))
    c_angles = [a for a in r["angles"] if a["grade"] == "C"]
    if c_angles:
        for a in c_angles:
            lines.append(f"- C-grade `{a['angle']}`: " + "; ".join(f["msg"] for f in a["findings"][:3]))
    lines.append("")

SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {SUMMARY_MD}")
print(f"Total findings: {sum(finding_counter.values())}")
print(f"Top 5 finding types:")
for fid, n in finding_counter.most_common(5):
    print(f"  {fid}: {n}")
