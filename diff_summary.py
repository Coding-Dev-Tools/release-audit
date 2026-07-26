#!/usr/bin/env python3
"""Build the final release-readiness report (after-prep)."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

OUT = Path(r"C:\Users\home\workspace\RELEASE-AUDIT")
SCORECARDS = OUT / "scorecards"
SUMMARY = OUT / "SUMMARY.json"
FINAL_MD = OUT / "RELEASE-READINESS-REPORT.md"
PREP = OUT / "PREP-LOG.json"

data = json.loads(SUMMARY.read_text(encoding="utf-8"))
prep = json.loads(PREP.read_text(encoding="utf-8")) if PREP.exists() else []
prep_actions = Counter()
prep_by_repo = {}
for r in prep:
    prep_by_repo[r["repo"]] = r
    for k, _msg in r.get("actions", []):
        prep_actions[k] += 1

repos = data["repos"]
grade_dist = Counter(r["overall_grade"] for r in repos)
total_blockers = sum(r["blockers"] for r in repos)

# totals
total_findings = sum(len(a.get("findings", [])) for r in repos for a in r["angles"])
finding_counter = Counter()
for r in repos:
    for a in r["angles"]:
        for f in a.get("findings", []):
            finding_counter[f["id"]] += 1

def grade_key(g):
    return {"A": 0, "B": 1, "C": 2, "D": 3}[g]
repos_sorted = sorted(repos, key=lambda r: (-grade_key(r["overall_grade"]), r["repo"]))

lines = []
lines.append("# Release Readiness Report (post-prep)")
lines.append("")
lines.append(f"_Generated: {data['repos'][0]['audited_at'] if data['repos'] else 'n/a'}_")
lines.append("")
lines.append("## Headline numbers")
lines.append("")
lines.append(f"- Repos audited: **{len(repos)}**")
lines.append(f"- A-grade: {grade_dist.get('A', 0)}")
lines.append(f"- B-grade: {grade_dist.get('B', 0)}")
lines.append(f"- C-grade: {grade_dist.get('C', 0)}")
lines.append(f"- D-grade: {grade_dist.get('D', 0)}")
lines.append(f"- Total release-blocker angles: {total_blockers}")
lines.append(f"- Total findings: {total_findings}")
lines.append("")
lines.append("## Prep actions applied")
lines.append("")
lines.append("| Action | Repos |")
lines.append("|--------|------:|")
for k, n in prep_actions.most_common():
    lines.append(f"| {k} | {n} |")
lines.append("")
lines.append("## Per-Repo Scorecard")
lines.append("")
lines.append("| Repo | Overall | Pass | Blockers | Prepped |")
lines.append("|------|---------|-----:|---------:|---------|")
for r in repos_sorted:
    p = "yes" if r["repo"] in prep_by_repo else "-"
    lines.append(f"| `{r['repo']}` | **{r['overall_grade']}** | {r['angles_passing']}/8 | {r['blockers']} | {p} |")
lines.append("")
lines.append("## Top remaining finding types")
lines.append("")
lines.append("| Finding ID | Count | Description |")
lines.append("|------------|------:|-------------|")
descs = {
    "DEP-FLOATING": "Floating dependency range in package.json (^/~/*/latest)",
    "DOC-NO-TEST-INSTR": "README does not document the test command",
    "SEC-INJECTION-SINK": "Possible injection sink (eval/exec/subprocess shell=True/SQL concat)",
    "LINT-NO-SCRIPT": "Lint tools installed but no script in package.json",
    "SEC-HARDCODED-SECRET": "Possible hardcoded secret/API key (review for false positives)",
    "DEP-NO-LOCKFILE": "No lockfile committed",
    "LINT-NONE": "No linter/formatter/type-checker",
    "DEP-NO-MANIFEST": "No package.json / pyproject.toml / requirements.txt",
    "TEST-NO-TESTS": "No tests directory or noop test script",
    "REL-NO-VERSION": "No version field in package.json or pyproject.toml",
    "DOC-NO-LICENSE": "No LICENSE file",
    "DEAD-DEBUG-NOISE": "Many console.log/print statements",
    "REL-NO-CI": "No CI workflow",
    "DOC-NO-INSTALL": "README does not document install command",
    "ERR-BARE-EXCEPT": "Bare except/empty catch (silently swallows errors)",
    "REL-NO-GITIGNORE": "No .gitignore",
    "DOC-NO-README": "No README",
    "TEST-NO-CI": "Tests exist but no CI to run them",
}
for fid, n in finding_counter.most_common(30):
    lines.append(f"| `{fid}` | {n} | {descs.get(fid, '')} |")
lines.append("")
lines.append("## What is still pending (release follow-ups)")
lines.append("")
lines.append("These are real gaps that the prep step did **not** fix because they require")
lines.append("repo-specific decisions and are not safe to auto-apply:")
lines.append("")
lines.append("- **DEP-FLOATING (70 hits)** — pinning every dep is a behavior change. Each must be")
lines.append("  reviewed: bump version, run tests, update lockfile.")
lines.append("- **SEC-INJECTION-SINK (26)** — these are real call sites that need manual review;")
lines.append("  many are false positives (regex patterns, f-strings that don't escape SQL).")
lines.append("- **SEC-HARDCODED-SECRET (14)** — many are test fixtures / env templates; each must")
lines.append("  be triaged to confirm whether it is a real secret.")
lines.append("- **DOC-NO-TEST-INSTR (26)** — once tests are added, READMEs need a one-line update")
lines.append("  pointing at the test command.")
lines.append("- **ERR-BARE-EXCEPT (5+)** — only flagged where there were many; smaller")
lines.append("  occurrences are also worth fixing.")
lines.append("")
lines.append("## How to verify")
lines.append("")
lines.append("```bash")
lines.append("cd C:\\Users\\home\\workspace")
lines.append("python RELEASE-AUDIT\\audit_all.py        # re-run the 8-angle audit")
lines.append("python RELEASE-AUDIT\\build_summary.py     # rebuild the summary")
lines.append("python RELEASE-AUDIT\\diff_summary.py      # rebuild this report")
lines.append("```")
lines.append("")
lines.append("## Artifacts")
lines.append("")
lines.append("- `RELEASE-AUDIT/PROTOCOL.md` — the 8-angle inspection protocol")
lines.append("- `RELEASE-AUDIT/audit.py` — per-repo auditor")
lines.append("- `RELEASE-AUDIT/audit_all.py` — driver that audits all repos")
lines.append("- `RELEASE-AUDIT/prep.py` — the fix-applier (idempotent)")
lines.append("- `RELEASE-AUDIT/scorecards/<repo>.json` + `.md` — per-repo scorecards")
lines.append("- `RELEASE-AUDIT/SUMMARY.md` — ranked priority list")
lines.append("- `RELEASE-AUDIT/PREP-LOG.md` — what was added to each repo")
lines.append("- `RELEASE-AUDIT/RELEASE-READINESS-REPORT.md` — this report")

FINAL_MD.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {FINAL_MD}")
print(f"Grade distribution: A={grade_dist.get('A',0)} B={grade_dist.get('B',0)} C={grade_dist.get('C',0)} D={grade_dist.get('D',0)}")
print(f"Total findings: {total_findings}")
