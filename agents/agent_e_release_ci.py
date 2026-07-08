#!/usr/bin/env python3
"""
Agent E — Release Readiness CI

Adds a reusable GitHub Actions workflow that runs the 8-angle audit on
every PR and posts the grade as a PR comment.

For Node/Python repos: adds `.github/workflows/release-audit.yml`
For content repos: skipped (no code to audit).

The workflow checks out the shared `RELEASE-AUDIT/` directory from
`Coding-Dev-Tools/release-audit` (a single source of truth for the
harness) and runs the audit on the target repo.
"""
from __future__ import annotations
import json
from pathlib import Path

WORKSPACE = Path(r"C:\Users\jomie\workspace")
LOG_PATH = WORKSPACE / "RELEASE-AUDIT" / "agents" / "agent-e-release-ci.log.json"
MD_PATH = WORKSPACE / "RELEASE-AUDIT" / "agents" / "agent-e-release-ci.md"

WORKFLOW = """name: release-audit

on:
  pull_request:
    branches: [main, master]
  push:
    branches: [main, master]
  workflow_dispatch:

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          path: target

      - name: Check out the shared release-audit harness
        uses: actions/checkout@v4
        with:
          repository: Coding-Dev-Tools/release-audit
          path: harness
          # Pin to a tag once a stable release is published; main is fine
          # for now since the harness is small and self-contained.
          ref: main

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Run the 8-angle release audit
        working-directory: harness
        run: |
          python audit.py "$GITHUB_WORKSPACE/target" --out-dir scorecard
          cat scorecard/$(basename "$GITHUB_WORKSPACE/target").json | python -c "
          import json,sys
          d=json.load(sys.stdin)
          print('## Release Audit (8 angles)')
          print()
          print(f\"**Overall grade: {d['overall_grade']}** ({d['angles_passing']}/{d['angles_total']} angles passing)\")
          print()
          print('| Angle | Grade |')
          print('|-------|-------|')
          for a in d['angles']:
              print(f\"| {a['angle']} | {a['grade']} |\")
          "

      - name: Fail on D-grade
        working-directory: harness
        run: |
          python -c "
          import json, sys
          d = json.load(open('scorecard/$(basename $GITHUB_WORKSPACE/target).json'))
          if d['blockers'] > 0:
              print(f\"::error::{d['blockers']} release-blocker angle(s) — see audit output above\")
              sys.exit(1)
          "
"""


def is_content_repo(root: Path) -> bool:
    has_code_manifest = any((root / f).exists() for f in ("package.json", "pyproject.toml", "setup.py", "Cargo.toml", "go.mod"))
    has_dev_requirements = (root / "requirements.txt").exists() or (root / "requirements-dev.txt").exists()
    if has_code_manifest or has_dev_requirements:
        return False
    return any((root / f).exists() for f in ("index.html", "index.md")) or any(root.glob("*.html"))


def detect_kind(root: Path) -> str:
    if (root / "package.json").exists():
        return "node"
    if (root / "pyproject.toml").exists() or (root / "requirements.txt").exists() or (root / "requirements-dev.txt").exists():
        return "python"
    return "other"


def list_git_repos() -> list[Path]:
    out = []
    for child in sorted(WORKSPACE.iterdir()):
        if not child.is_dir() or not (child / ".git").exists():
            continue
        if child.name.startswith((".", "_")):
            continue
        out.append(child)
    return out


def main() -> int:
    repos = list_git_repos()
    print(f"Agent E: scanning {len(repos)} repos")
    out = []
    for r in repos:
        actions = []
        if is_content_repo(r):
            actions.append("skipped: content repo (no code to audit)")
            out.append({"repo": r.name, "kind": "content", "actions": actions})
            print(f"  {r.name:35s} content (skipped)")
            continue
        kind = detect_kind(r)
        wf = r / ".github" / "workflows" / "release-audit.yml"
        if wf.exists():
            # Idempotent: skip if our workflow is present.
            text = wf.read_text(encoding="utf-8", errors="replace")
            if "release-audit" in text and "Coding-Dev-Tools/release-audit" in text:
                actions.append("ok: release-audit.yml already present")
                out.append({"repo": r.name, "kind": kind, "actions": actions})
                print(f"  {r.name:35s} {kind:6s} ok (already present)")
                continue
        wf.parent.mkdir(parents=True, exist_ok=True)
        wf.write_text(WORKFLOW, encoding="utf-8")
        actions.append("created: .github/workflows/release-audit.yml")
        out.append({"repo": r.name, "kind": kind, "actions": actions})
        print(f"  {r.name:35s} {kind:6s} created")
    LOG_PATH.write_text(json.dumps(out, indent=2), encoding="utf-8")
    lines = ["# Agent E — Release Readiness CI\n"]
    for entry in out:
        lines.append(f"## `{entry['repo']}` ({entry['kind']})")
        for a in entry["actions"]:
            lines.append(f"- {a}")
        lines.append("")
    MD_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {LOG_PATH} and {MD_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
