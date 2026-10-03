#!/usr/bin/env python3
"""Driver: audit every git repo in the user's workspace."""
from __future__ import annotations
import json
import os
import subprocess
import sys
import time
from pathlib import Path

WORKSPACE = Path.home() / "workspace"
AUDIT_SCRIPT = WORKSPACE / "RELEASE-AUDIT" / "audit.py"
OUT_DIR = WORKSPACE / "RELEASE-AUDIT" / "scorecards"
SUMMARY_PATH = WORKSPACE / "RELEASE-AUDIT" / "SUMMARY.json"
SUMMARY_MD = WORKSPACE / "RELEASE-AUDIT" / "SUMMARY.md"

SKIP_DIR_PREFIXES = (
    ".",  # dot-dirs
    "_",  # scratch
)


def list_repos() -> list[Path]:
    repos = []
    for child in sorted(WORKSPACE.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith(SKIP_DIR_PREFIXES):
            continue
        if (child / ".git").exists():
            repos.append(child)
    return repos


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    repos = list_repos()
    print(f"Found {len(repos)} repos")
    results = []
    started = time.time()
    for r in repos:
        t0 = time.time()
        try:
            cp = subprocess.run(
                [sys.executable, str(AUDIT_SCRIPT), str(r), "--out-dir", str(OUT_DIR)],
                capture_output=True, text=True, timeout=300,
            )
        except subprocess.TimeoutExpired:
            print(f"TIMEOUT {r.name}", flush=True)
            continue
        line = cp.stdout.strip().splitlines()[-1] if cp.stdout.strip() else f"no-output rc={cp.returncode}"
        print(f"  {r.name:35s} {line} ({time.time()-t0:.1f}s)", flush=True)
        if cp.returncode != 0:
            print(f"    stderr: {cp.stderr.strip()[:300]}", flush=True)
            continue
        scorecard = json.loads((OUT_DIR / f"{r.name}.json").read_text(encoding="utf-8"))
        results.append(scorecard)
    elapsed = time.time() - started
    print(f"Done {len(results)}/{len(repos)} repos in {elapsed:.1f}s")
    # write summary
    SUMMARY_PATH.write_text(json.dumps({"repos": results, "elapsed_s": elapsed}, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
