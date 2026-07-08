#!/usr/bin/env python3
"""
Agent A — Deps & Lockfiles

Goals:
  1. For every Python repo missing a lockfile, run `uv lock` (creates uv.lock).
  2. For every Node repo missing a lockfile, run `pnpm install --lockfile-only`
     (writes pnpm-lock.yaml without installing into node_modules).
  3. For DEP-FLOATING (^/~/*/latest) in package.json, run `pnpm install
     --lockfile-only --no-frozen-lockfile` to refresh; if the resolved version
     is already pinned by the lockfile, leave the range alone but document it.
  4. For each repo, log what was changed and verify the lockfile exists.

Safe-by-default: never modifies version strings inside package.json /
pyproject.toml (those are version bumps the user must approve). Only generates
lockfiles from the current manifest.
"""
from __future__ import annotations
import json
import shutil
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(r"C:\Users\jomie\workspace")
LOG_PATH = WORKSPACE / "RELEASE-AUDIT" / "agents" / "agent-a-deps.log.json"
MD_PATH = WORKSPACE / "RELEASE-AUDIT" / "agents" / "agent-a-deps.md"

LOCKFILE_CANDIDATES = (
    "package-lock.json", "pnpm-lock.yaml", "yarn.lock",
    "poetry.lock", "uv.lock", "Pipfile.lock",
)

EXCLUDE_PREFIXES = (".", "_")  # dot / scratch dirs
PKG_JSON = "package.json"
PYPROJECT = "pyproject.toml"


def has_uv() -> bool:
    return shutil.which("uv") is not None


def has_pnpm() -> bool:
    return shutil.which("pnpm") is not None


def has_npm() -> bool:
    return shutil.which("npm") is not None


def list_git_repos() -> list[Path]:
    out = []
    for child in sorted(WORKSPACE.iterdir()):
        if not child.is_dir() or not (child / ".git").exists():
            continue
        if child.name.startswith(EXCLUDE_PREFIXES):
            continue
        out.append(child)
    return out


def detect_kind(root: Path) -> str:
    if (root / PKG_JSON).exists():
        return "node"
    if (root / PYPROJECT).exists() or (root / "requirements.txt").exists() or (root / "requirements-dev.txt").exists():
        return "python"
    return "other"


def has_lockfile(root: Path) -> bool:
    return any((root / c).exists() for c in LOCKFILE_CANDIDATES)


def run(cmd: list[str], cwd: Path, timeout: int = 180) -> dict:
    try:
        cp = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return {"cmd": " ".join(cmd), "returncode": cp.returncode, "stdout_tail": cp.stdout[-500:], "stderr_tail": cp.stderr[-500:]}
    except subprocess.TimeoutExpired as e:
        return {"cmd": " ".join(cmd), "returncode": -1, "error": "timeout"}
    except FileNotFoundError as e:
        return {"cmd": " ".join(cmd), "returncode": -1, "error": str(e)}


def agent_a_node(root: Path) -> dict:
    """For a Node repo: run `pnpm install --lockfile-only` if no lockfile present."""
    before = [c for c in LOCKFILE_CANDIDATES if (root / c).exists()]
    result = {"kind": "node", "actions": []}
    if before:
        result["actions"].append({"step": "skip-lockfile-exists", "lockfiles": before})
        return result
    if not has_pnpm():
        result["actions"].append({"step": "skip-no-pnpm"})
        return result
    # Run pnpm install --lockfile-only with --ignore-scripts for speed/safety.
    # This creates pnpm-lock.yaml based on the current package.json.
    r = run(["pnpm", "install", "--lockfile-only", "--ignore-scripts"], cwd=root, timeout=240)
    result["actions"].append({"step": "pnpm-install-lockfile-only", **r})
    after = [c for c in LOCKFILE_CANDIDATES if (root / c).exists()]
    result["lockfiles_after"] = after
    return result


def agent_a_python(root: Path) -> dict:
    """For a Python repo: run `uv lock` if uv is available and no lockfile present."""
    before = [c for c in LOCKFILE_CANDIDATES if (root / c).exists()]
    result = {"kind": "python", "actions": []}
    if before:
        result["actions"].append({"step": "skip-lockfile-exists", "lockfiles": before})
        return result
    # Need pyproject.toml for uv lock
    if not (root / PYPROJECT).exists():
        result["actions"].append({"step": "skip-no-pyproject"})
        return result
    if not has_uv():
        result["actions"].append({"step": "skip-no-uv"})
        return result
    r = run(["uv", "lock"], cwd=root, timeout=180)
    result["actions"].append({"step": "uv-lock", **r})
    after = [c for c in LOCKFILE_CANDIDATES if (root / c).exists()]
    result["lockfiles_after"] = after
    return result


def main() -> int:
    repos = list_git_repos()
    print(f"Agent A: scanning {len(repos)} repos")
    out = []
    for r in repos:
        kind = detect_kind(r)
        if kind == "node":
            res = agent_a_node(r)
        elif kind == "python":
            res = agent_a_python(r)
        else:
            res = {"kind": "other", "actions": [{"step": "skip-other"}]}
        out.append({"repo": r.name, **res})
        status = res.get("lockfiles_after") or [a.get("lockfiles", [None])[0] for a in res["actions"] if a.get("step") == "skip-lockfile-exists"] or ["(unchanged)"]
        print(f"  {r.name:35s} {kind:6s} {status}")
    LOG_PATH.write_text(json.dumps(out, indent=2), encoding="utf-8")
    # Markdown summary
    lines = ["# Agent A — Deps & Lockfiles\n"]
    lines.append(f"_Generated for {len(repos)} repos_\n")
    for entry in out:
        lines.append(f"## `{entry['repo']}` ({entry['kind']})")
        for a in entry.get("actions", []):
            step = a.get("step", "?")
            if step == "pnpm-install-lockfile-only" or step == "uv-lock":
                lines.append(f"- **{step}** rc={a.get('returncode')} {a.get('stderr_tail','')[:80]}")
            else:
                lines.append(f"- {step}: {a}")
        if entry.get("lockfiles_after"):
            lines.append(f"- lockfiles now: {entry['lockfiles_after']}")
        lines.append("")
    MD_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {LOG_PATH} and {MD_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
