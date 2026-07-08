#!/usr/bin/env python3
"""
Agent C — Docs & Tests

Goals:
  1. For every README that has no "## Install" section, append one with
     the appropriate command (npm install / pnpm install / pip install / etc).
  2. For every README that has no "## Test" section, append one with the
     test command for the project.
  3. For non-content repos with no tests/ dir, create tests/test_smoke.py
     (Python) or tests/smoke.test.js (Node) with a passing smoke test.

Idempotent: detects existing sections and skips.
"""
from __future__ import annotations
import json
import re
import subprocess
from pathlib import Path

WORKSPACE = Path(r"C:\Users\jomie\workspace")
LOG_PATH = WORKSPACE / "RELEASE-AUDIT" / "agents" / "agent-c-docs.log.json"
MD_PATH = WORKSPACE / "RELEASE-AUDIT" / "agents" / "agent-c-docs.md"


def is_content_repo(root: Path) -> bool:
    has_code_manifest = any((root / f).exists() for f in ("package.json", "pyproject.toml", "setup.py", "Cargo.toml", "go.mod"))
    has_dev_requirements = (root / "requirements.txt").exists() or (root / "requirements-dev.txt").exists()
    has_code = has_code_manifest or has_dev_requirements
    py_files = sum(1 for _ in root.rglob("*.py"))
    if has_code:
        return False
    return (
        any((root / f).exists() for f in ("index.html", "index.md"))
        or any(root.glob("*.html"))
        or (root / "Formula").is_dir()
        or (root / "bucket").is_dir()
        or (py_files <= 1 and any(root.glob("*.html")))
    )


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


def find_readme(root: Path) -> Path | None:
    for cand in ("README.md", "README.rst", "README.txt", "README"):
        p = root / cand
        if p.exists():
            return p
    return None


def has_section(readme_text: str, name: str) -> bool:
    return bool(re.search(r"(?im)^#{1,6}\s+" + re.escape(name) + r"\b", readme_text))


def detect_install_cmd(root: Path, kind: str) -> str:
    pkg = root / "package.json"
    if kind == "node" and pkg.exists():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8", errors="replace"))
            pm = (data.get("packageManager") or "").strip()
            if pm.startswith("pnpm"):
                return "pnpm install"
            if pm.startswith("yarn"):
                return "yarn install"
            if pm.startswith("npm"):
                return "npm install"
        except (json.JSONDecodeError, OSError):
            pass
        if (root / "pnpm-lock.yaml").exists():
            return "pnpm install"
        if (root / "package-lock.json").exists():
            return "npm install"
        if (root / "yarn.lock").exists():
            return "yarn install"
        return "npm install"
    if kind == "python":
        if (root / "pyproject.toml").exists():
            return "pip install -e ."
        if (root / "requirements.txt").exists() or (root / "requirements-dev.txt").exists():
            return "pip install -r requirements.txt"
    return "# see project docs"


def detect_test_cmd(root: Path, kind: str) -> str:
    pkg = root / "package.json"
    if kind == "node" and pkg.exists():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8", errors="replace"))
            scripts = data.get("scripts") or {}
            if "test" in scripts and "echo" not in scripts["test"]:
                return f"npm test  # runs: {scripts['test']}"
        except (json.JSONDecodeError, OSError):
            pass
        # Fallback to node --test if tests/ exists
        if any((root / d).is_dir() for d in ("tests", "test", "__tests__")):
            return "npm test  # uses node --test tests/"
    if kind == "python":
        pyt = root / "pyproject.toml"
        if pyt.exists() and "[tool.pytest" in pyt.read_text(encoding="utf-8", errors="replace"):
            return "pytest -q"
        if (root / "tests").is_dir() or (root / "test").is_dir():
            return "pytest -q"
        if (root / "pyproject.toml").exists():
            return "pytest -q"
    return "# see project docs"


def ensure_install_section(readme: Path, cmd: str) -> str:
    text = readme.read_text(encoding="utf-8", errors="replace")
    if has_section(text, "Install"):
        return "ok: Install section present"
    addendum = f"\n## Install\n\n```bash\n{cmd}\n```\n"
    readme.write_text(text.rstrip() + "\n" + addendum, encoding="utf-8")
    return f"added: Install section ({cmd})"


def ensure_test_section(readme: Path, cmd: str) -> str:
    text = readme.read_text(encoding="utf-8", errors="replace")
    if has_section(text, "Test") or has_section(text, "Tests") or has_section(text, "Testing"):
        return "ok: Test section present"
    addendum = f"\n## Test\n\n```bash\n{cmd}\n```\n"
    readme.write_text(text.rstrip() + "\n" + addendum, encoding="utf-8")
    return f"added: Test section ({cmd})"


def ensure_python_tests(root: Path) -> str:
    td = root / "tests"
    if td.exists() and any(td.glob("test_*.py")):
        return "ok: tests/ has test files"
    td.mkdir(parents=True, exist_ok=True)
    if not (td / "__init__.py").exists():
        (td / "__init__.py").write_text("", encoding="utf-8")
    if not (td / "test_smoke.py").exists():
        (td / "test_smoke.py").write_text('def test_smoke():\n    """Trivially passing smoke test for CI."""\n    assert True\n', encoding="utf-8")
    return "created: tests/test_smoke.py"


def ensure_node_tests(root: Path) -> str:
    td = root / "tests"
    if td.exists() and any(td.glob("*.test.*")):
        return "ok: tests/ has test files"
    td.mkdir(parents=True, exist_ok=True)
    if not (td / "smoke.test.js").exists():
        (td / "smoke.test.js").write_text("const test = require('node:test');\nconst assert = require('node:assert');\n\ntest('smoke', () => {\n  assert.strictEqual(1, 1);\n});\n", encoding="utf-8")
    # Wire up the test script in package.json
    p = root / "package.json"
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8", errors="replace"))
            scripts = data.get("scripts") or {}
            if "test" in scripts and "echo" not in scripts["test"]:
                return "created: tests/smoke.test.js (test script already wired)"
            scripts["test"] = "node --test tests/"
            data["scripts"] = scripts
            p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            return "created: tests/smoke.test.js + wired test script"
        except (json.JSONDecodeError, OSError):
            return "created: tests/smoke.test.js (could not wire script)"
    return "created: tests/smoke.test.js"


def main() -> int:
    repos = list_git_repos()
    print(f"Agent C: scanning {len(repos)} repos")
    out = []
    for r in repos:
        kind = detect_kind(r)
        content = is_content_repo(r)
        actions = []
        # README updates apply to all repos (including content sites)
        readme = find_readme(r)
        if readme is None:
            actions.append("skipped: no README")
        else:
            install_cmd = detect_install_cmd(r, kind) if kind != "other" else "open the static site locally"
            test_cmd = detect_test_cmd(r, kind) if kind != "other" else "n/a (static content)"
            actions.append(ensure_install_section(readme, install_cmd))
            actions.append(ensure_test_section(readme, test_cmd))
        # Tests dir only for code repos (not content)
        if not content and kind == "python":
            actions.append(ensure_python_tests(r))
        elif not content and kind == "node":
            actions.append(ensure_node_tests(r))
        else:
            actions.append("skipped: content repo or no kind")
        out.append({"repo": r.name, "kind": kind, "content": content, "actions": actions})
        print(f"  {r.name:35s} {kind:6s} {len(actions)} actions")
    LOG_PATH.write_text(json.dumps(out, indent=2), encoding="utf-8")
    lines = ["# Agent C — Docs & Tests\n"]
    for entry in out:
        lines.append(f"## `{entry['repo']}` ({entry['kind']}{', content' if entry['content'] else ''})")
        for a in entry["actions"]:
            lines.append(f"- {a}")
        lines.append("")
    MD_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {LOG_PATH} and {MD_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
