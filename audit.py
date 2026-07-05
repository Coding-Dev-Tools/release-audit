#!/usr/bin/env python3
"""8-angle release-readiness audit for a repository.

Usage:
    python audit.py <target_path> [--out-dir DIR]

It scans ``<target_path>`` (the checkout of the repo under audit) and writes a
single JSON scorecard to ``<out-dir>/<basename(target_path)>.json``.

JSON contract (consumed by the release-audit GitHub workflows):

    {
        "repo": "target",                  # basename of target_path
        "overall_grade": "B",              # A | B | C | D | F
        "angles_passing": 5,               # count of angles graded A/B/C
        "angles_total": 8,
        "blockers": 0,                      # count of angles graded F
        "angles": [
            {"angle": "License", "grade": "A", "detail": "..."},
            ...
        ]
    }

The 8 angles and their criticality:

    Critical (missing → blocker, grade F):
        1. License        — LICENSE file present and a recognized license
        2. Security       — SECURITY.md present
        3. README         — README present and non-trivial
        4. CI             — .github/workflows/*.yml present
        5. Tests          — tests/ dir or test files present and non-empty

    Optional (missing → grade D, never a blocker):
        6. Contributing   — CONTRIBUTING.md present
        7. CodeOfConduct   — CODE_OF_CONDUCT.md present
        8. Changelog      — CHANGELOG.md present

Grades per angle: A (fully meets), B (meets), C (partial), D (missing-optional),
F (missing-critical). ``blockers`` is the count of F grades; the workflow fails
the job when ``blockers > 0``.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# Angles marked critical: a missing critical file is a release blocker (F).
CRITICAL_ANGLES = {"License", "Security", "README", "CI", "Tests"}

# Recognized license identifiers (case-insensitive substring match on LICENSE).
KNOWN_LICENSES = [
    "mit license",
    "apache license",
    "apache-2.0",
    "bsd 2-clause",
    "bsd 3-clause",
    "bsd zero clause",
    "isc license",
    "mozilla public license",
    "gnu general public license",
    "gnu lesser general public license",
    "the unlicense",
    "creative commons zero",
    "cc0",
]

# README is considered non-trivial when it has at least this many non-blank
# lines of real content (not just a title).
README_MIN_CONTENT_LINES = 5


def _grade_missing(angle: str) -> str:
    """Grade for a missing file: F if critical, else D."""
    return "F" if angle in CRITICAL_ANGLES else "D"


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def _audit_license(root: Path) -> dict[str, Any]:
    for name in ("LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE", "COPYING"):
        p = root / name
        if p.is_file():
            text = _read_text(p) or ""
            low = text.lower()
            if any(tok in low for tok in KNOWN_LICENSES):
                return {"angle": "License", "grade": "A",
                        "detail": f"{name} present, recognized license"}
            return {"angle": "License", "grade": "B",
                    "detail": f"{name} present but license type not recognized"}
    return {"angle": "License", "grade": "F",
            "detail": "no LICENSE file found"}


def _audit_security(root: Path) -> dict[str, Any]:
    for name in ("SECURITY.md", "SECURITY", "docs/SECURITY.md"):
        if (root / name).is_file():
            return {"angle": "Security", "grade": "A",
                    "detail": f"{name} present"}
    return {"angle": "Security", "grade": "F",
            "detail": "no SECURITY.md found"}


def _audit_readme(root: Path) -> dict[str, Any]:
    for name in ("README.md", "README.rst", "README.txt", "README", "readme.md"):
        p = root / name
        if p.is_file():
            text = _read_text(p) or ""
            content_lines = [ln for ln in text.splitlines()
                             if ln.strip() and not ln.strip().startswith("#")]
            if len(content_lines) >= README_MIN_CONTENT_LINES:
                return {"angle": "README", "grade": "A",
                        "detail": f"{name} present with substantive content"}
            return {"angle": "README", "grade": "C",
                    "detail": f"{name} present but thin ({len(content_lines)} content lines)"}
    return {"angle": "README", "grade": "F",
            "detail": "no README found"}


def _audit_ci(root: Path) -> dict[str, Any]:
    wf = root / ".github" / "workflows"
    if wf.is_dir():
        ymls = [p for p in wf.iterdir() if p.suffix in (".yml", ".yaml") and p.is_file()]
        if ymls:
            return {"angle": "CI", "grade": "A",
                    "detail": f"{len(ymls)} workflow(s): {', '.join(sorted(p.name for p in ymls))}"}
        return {"angle": "CI", "grade": "C",
                "detail": ".github/workflows present but no .yml workflows"}
    return {"angle": "CI", "grade": "F",
            "detail": "no .github/workflows directory found"}


def _audit_tests(root: Path) -> dict[str, Any]:
    test_dirs = [d for d in ("tests", "test", "tests") if (root / d).is_dir()]
    if test_dirs:
        d = root / test_dirs[0]
        test_files = [p for p in d.rglob("*")
                      if p.is_file() and p.name.lower().startswith("test_")
                      and p.suffix in (".py", ".js", ".ts", ".rs", ".go")]
        if test_files:
            return {"angle": "Tests", "grade": "A",
                    "detail": f"{len(test_files)} test file(s) under {test_dirs[0]}/"}
        return {"angle": "Tests", "grade": "C",
                "detail": f"{test_dirs[0]}/ present but no test_* files found"}
    # Fallback: any test files at the repo root.
    root_tests = [p for p in root.iterdir()
                  if p.is_file() and p.name.lower().startswith("test_")
                  and p.suffix in (".py", ".js", ".ts", ".rs", ".go")]
    if root_tests:
        return {"angle": "Tests", "grade": "B",
                "detail": f"{len(root_tests)} test file(s) at repo root"}
    return {"angle": "Tests", "grade": "F",
            "detail": "no tests directory or test files found"}


def _audit_optional(root: Path, angle: str, filename: str) -> dict[str, Any]:
    candidates = [filename, f"docs/{filename}", f".github/{filename}"]
    for c in candidates:
        if (root / c).is_file():
            return {"angle": angle, "grade": "A", "detail": f"{c} present"}
    return {"angle": angle, "grade": "D", "detail": f"no {filename} found"}


def _overall_grade(angles: list[dict[str, Any]], blockers: int) -> str:
    if blockers > 0:
        return "F"
    passing = sum(1 for a in angles if a["grade"] in ("A", "B", "C"))
    total = len(angles)
    ratio = passing / total if total else 0.0
    if ratio >= 7 / 8:
        return "A"
    if ratio >= 5 / 8:
        return "B"
    if ratio >= 3 / 8:
        return "C"
    if ratio >= 1 / 8:
        return "D"
    return "F"


def audit(target: Path) -> dict[str, Any]:
    if not target.is_dir():
        raise SystemExit(f"audit: target is not a directory: {target}")

    angles = [
        _audit_license(target),
        _audit_security(target),
        _audit_readme(target),
        _audit_ci(target),
        _audit_tests(target),
        _audit_optional(target, "Contributing", "CONTRIBUTING.md"),
        _audit_optional(target, "CodeOfConduct", "CODE_OF_CONDUCT.md"),
        _audit_optional(target, "Changelog", "CHANGELOG.md"),
    ]

    blockers = sum(1 for a in angles if a["grade"] == "F")
    passing = sum(1 for a in angles if a["grade"] in ("A", "B", "C"))

    return {
        "repo": target.resolve().name,
        "overall_grade": _overall_grade(angles, blockers),
        "angles_passing": passing,
        "angles_total": len(angles),
        "blockers": blockers,
        "angles": angles,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="8-angle release-readiness audit.")
    parser.add_argument("target", type=Path, help="path to the repo checkout to audit")
    parser.add_argument("--out-dir", type=Path, default=Path("scorecard"),
                        help="directory to write the scorecard JSON (default: scorecard)")
    parser.add_argument("--print", action="store_true",
                        help="also print the scorecard JSON to stdout")
    args = parser.parse_args(argv)

    result = audit(args.target)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    out_path = args.out_dir / f"{result['repo']}.json"
    out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    # Human-readable summary to stdout (shows up in the Actions log).
    print(f"Release audit: {result['repo']}")
    print(f"  Overall grade: {result['overall_grade']} "
          f"({result['angles_passing']}/{result['angles_total']} angles passing, "
          f"{result['blockers']} blocker(s))")
    for a in result["angles"]:
        print(f"  - {a['angle']:<14} {a['grade']}  {a['detail']}")
    print(f"  Scorecard written to {out_path}")

    if args.print:
        print(json.dumps(result, indent=2))

    # Exit non-zero on blockers so the workflow's "Fail on blockers" step
    # can rely on either this exit code or the JSON count.
    return 1 if result["blockers"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())