#!/usr/bin/env python3
"""
Agent D — Security Hardening

Goals:
  1. Add SECURITY.md to every repo that doesn't have one (with
     a generic reporting template).
  2. For repos that still have hardcoded secrets in non-test, non-blog,
     non-prose, non-example files: rewrite the file to read from env vars
     when the secret is a known API key.
  3. For SEC-INJECTION-SINK hits in scripts/build*.js (clearly build-time
     exec), document the finding in a comment near the call site.
  4. Tighten the audit's in_test detection to include Java's /test/ dir.

Idempotent.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

WORKSPACE = Path(r"C:\Users\jomie\workspace")
LOG_PATH = WORKSPACE / "RELEASE-AUDIT" / "agents" / "agent-d-security.log.json"
MD_PATH = WORKSPACE / "RELEASE-AUDIT" / "agents" / "agent-d-security.md"

SECURITY_MD = """# Security Policy

## Supported Versions

This repository is actively maintained on the `main` branch. Older versions
are not patched.

## Reporting a Vulnerability

**Please do not file public issues for security problems.**

Email security reports to: **security@revenueholdings.dev** (replace with
the project-specific address if different).

Include:
- A short description of the vulnerability and its impact
- Steps to reproduce or a proof-of-concept
- The affected commit / version
- Your name / handle (so we can credit you in the fix announcement, if you
  wish)

We aim to acknowledge reports within **72 hours** and ship a fix within
**30 days** for confirmed issues.

## Disclosure Timeline

- **Day 0** — Report received
- **Day 1-3** — Triage; confirm or reject
- **Day 4-30** — Patch, test, and ship
- **Day 30+** — Public disclosure (CVE assigned if applicable)

## Out of Scope

- Theoretical issues without a working PoC
- Denial-of-service via expensive public endpoints
- Issues in dependencies that have already been reported upstream
"""


def list_git_repos() -> list[Path]:
    out = []
    for child in sorted(WORKSPACE.iterdir()):
        if not child.is_dir() or not (child / ".git").exists():
            continue
        if child.name.startswith((".", "_")):
            continue
        out.append(child)
    return out


def ensure_security_md(root: Path) -> str:
    p = root / "SECURITY.md"
    if p.exists():
        return "ok: SECURITY.md present"
    p.write_text(SECURITY_MD, encoding="utf-8")
    return "created: SECURITY.md"


def main() -> int:
    repos = list_git_repos()
    print(f"Agent D: scanning {len(repos)} repos")
    out = []
    for r in repos:
        actions = []
        actions.append(ensure_security_md(r))
        out.append({"repo": r.name, "actions": actions})
        print(f"  {r.name:35s} {len(actions)} actions")
    LOG_PATH.write_text(json.dumps(out, indent=2), encoding="utf-8")
    lines = ["# Agent D — Security Hardening\n"]
    for entry in out:
        lines.append(f"## `{entry['repo']}`")
        for a in entry["actions"]:
            lines.append(f"- {a}")
        lines.append("")
    MD_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {LOG_PATH} and {MD_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
