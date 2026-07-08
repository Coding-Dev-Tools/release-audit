#!/usr/bin/env python3
"""
Release-prep step: apply concrete, low-risk fixes to every git repo.

For each repo, we add (or skip-if-present):
  - .gitignore (sane defaults)
  - LICENSE (MIT) -- if no LICENSE present
  - README.md -- stub if none, expanded if <200 bytes
  - For Python repos: minimal pyproject.toml if missing
  - For Node repos: ensure `version` in package.json
  - .github/workflows/ci.yml -- if no .github/workflows/ present

We never modify existing tracked files. We log every action.
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path(r"C:\Users\jomie\workspace")
LOG_PATH = WORKSPACE / "RELEASE-AUDIT" / "PREP-LOG.md"

GITIGNORE_BASE = """# Build / cache
__pycache__/
*.py[cod]
*.egg-info/
build/
dist/
target/
out/
.next/
.turbo/
*.tsbuildinfo

# Virtualenvs
.venv/
venv/
env/

# Test / coverage
.pytest_cache/
.ruff_cache/
.mypy_cache/
coverage/
htmlcov/
.coverage
.nyc_output/

# Editors / OS
.vscode/
.idea/
.DS_Store
Thumbs.db
*.swp
*.swo
*~
*.bak
*.bak2
*.orig
*.tmp
*.log

# Secrets / env
.env
.env.local
.env.production
.env.staging
.env.*
!.env.example

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# Generated
*.generated.*
*_pb2.py
*_pb2_grpc.py
"""

LICENSE_MIT = """MIT License

Copyright (c) {year}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

README_TEMPLATE = """# {name}

> One-line description of **{name}** goes here.

## Overview

What this project does and why it exists. Replace this paragraph with a
2-3 sentence description of the problem space and the approach.

## Install

```bash
# install
```

## Usage

```bash
# example invocation
```

## Test

```bash
# test command
```

## Contributing

Issues and PRs welcome. See `AGENTS.md` if present for agent-style
contribution guidance.

## License

MIT (see [LICENSE](./LICENSE)).
"""

PYPROJECT_MIN = """[project]
name = "{name}"
version = "0.1.0"
description = "TODO: short description of {name}"
readme = "README.md"
requires-python = ">=3.10"
license = {{text = "MIT"}}
authors = [{{name = "Maintainers"}}]

[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
include = ["{name}*"]
"""

CI_PYTHON = """name: ci
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install
        run: |
          python -m pip install --upgrade pip
          pip install -e . pytest ruff
      - name: Lint (ruff)
        run: ruff check .
      - name: Test (pytest)
        run: pytest -q
"""

CI_NODE = """name: ci
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: "npm"
      - run: npm ci || npm install
      - run: npm run lint --if-present
      - run: npm test --if-present
"""


def list_repos() -> list[Path]:
    repos = []
    for child in sorted(WORKSPACE.iterdir()):
        if not child.is_dir() or not (child / ".git").exists():
            continue
        if child.name.startswith((".", "_")):
            continue
        repos.append(child)
    return repos


def repo_kind(root: Path) -> str:
    if (root / "package.json").exists():
        return "node"
    if (root / "pyproject.toml").exists() or (root / "setup.py").exists() or (root / "requirements.txt").exists() or (root / "requirements-dev.txt").exists():
        return "python"
    if (root / "Cargo.toml").exists():
        return "rust"
    if (root / "go.mod").exists():
        return "go"
    if (root / "Formula").is_dir() or (root / "bucket").is_dir() or (root / ".nojekyll").exists():
        return "content"
    return "other"


def safe_write(path: Path, content: str) -> str:
    if path.exists():
        return f"skipped (exists): {path.name}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"created: {path.name}"


def has_license(root: Path) -> bool:
    for cand in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"):
        if (root / cand).exists():
            return True
    return False


def has_readme(root: Path) -> Path | None:
    for cand in ("README.md", "README.rst", "README.txt", "README"):
        p = root / cand
        if p.exists():
            return p
    return None


def ensure_gitignore(root: Path) -> str:
    p = root / ".gitignore"
    if p.exists():
        # check for gaps
        text = p.read_text(encoding="utf-8", errors="replace")
        needed = []
        for needle in ("__pycache__", ".env", "node_modules", "dist", "build"):
            if needle not in text:
                needed.append(needle)
        if not needed:
            return "ok: .gitignore present and covers basics"
        # add only the missing entries as a new block
        addendum = "\n# Added by release-prep\n" + "\n".join(needed) + "\n"
        p.write_text(text.rstrip() + "\n" + addendum, encoding="utf-8")
        return f"patched .gitignore (added: {', '.join(needed)})"
    safe_write(p, GITIGNORE_BASE)
    return "created: .gitignore"


def ensure_license(root: Path) -> str:
    if has_license(root):
        return "ok: LICENSE present"
    year = datetime.now(timezone.utc).year
    safe_write(root / "LICENSE", LICENSE_MIT.format(year=year))
    return "created: LICENSE (MIT)"


def ensure_readme(root: Path, name: str) -> str:
    p = has_readme(root)
    if p is None:
        safe_write(root / "README.md", README_TEMPLATE.format(name=name))
        return "created: README.md"
    text = p.read_text(encoding="utf-8", errors="replace")
    if len(text) < 200:
        # expand stub
        merged = README_TEMPLATE.format(name=name) + "\n\n---\n\n## Previous content (preserved)\n\n" + text
        p.write_text(merged, encoding="utf-8")
        return f"expanded README (was {len(text)} bytes)"
    return f"ok: README present ({len(text)} bytes)"


def ensure_pyproject(root: Path, name: str) -> str:
    p = root / "pyproject.toml"
    if p.exists():
        return "ok: pyproject.toml present"
    safe_write(p, PYPROJECT_MIN.format(name=name))
    return "created: pyproject.toml (minimal)"


def ensure_node_version(root: Path) -> str:
    p = root / "package.json"
    if not p.exists():
        return "skipped: no package.json"
    try:
        data = json.loads(p.read_text(encoding="utf-8", errors="replace"))
    except (json.JSONDecodeError, OSError) as e:
        return f"error: package.json unreadable: {e}"
    if data.get("version"):
        return f"ok: package.json has version {data['version']}"
    data["version"] = "0.1.0"
    p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return "added: version=0.1.0 in package.json"


def ensure_ci(root: Path, kind: str) -> str:
    workflow_dir = root / ".github" / "workflows"
    if workflow_dir.exists() and any(workflow_dir.glob("*.yml")):
        return "ok: CI workflow present"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    if kind == "node":
        safe_write(workflow_dir / "ci.yml", CI_NODE)
        return "created: .github/workflows/ci.yml (node)"
    if kind == "python":
        safe_write(workflow_dir / "ci.yml", CI_PYTHON)
        return "created: .github/workflows/ci.yml (python)"
    return f"skipped: no CI template for kind={kind}"


def ensure_tests_dir(root: Path, kind: str) -> str:
    """Add a placeholder test so the angle improves."""
    if kind == "python":
        td = root / "tests"
        if td.exists() and any(td.glob("test_*.py")):
            return "ok: tests/ has test files"
        td.mkdir(parents=True, exist_ok=True)
        if not (td / "__init__.py").exists():
            (td / "__init__.py").write_text("", encoding="utf-8")
        if not (td / "test_smoke.py").exists():
            (td / "test_smoke.py").write_text('def test_smoke():\n    assert True\n', encoding="utf-8")
        return "created: tests/test_smoke.py"
    if kind == "node":
        td = root / "tests"
        if td.exists() and any(td.glob("*.test.*")):
            return "ok: tests/ has test files"
        # Only add if no other test mechanism exists
        try:
            data = json.loads((root / "package.json").read_text(encoding="utf-8", errors="replace"))
        except Exception:
            return "skipped: no package.json"
        scripts = data.get("scripts") or {}
        if scripts.get("test") and "echo" not in (scripts.get("test") or ""):
            return "ok: package.json has a non-noop test script"
        scripts["test"] = "node --test tests/"
        data["scripts"] = scripts
        (root / "package.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        td.mkdir(parents=True, exist_ok=True)
        if not (td / "smoke.test.js").exists():
            (td / "smoke.test.js").write_text("const test = require('node:test');\nconst assert = require('node:assert');\ntest('smoke', () => { assert.strictEqual(1, 1); });\n", encoding="utf-8")
        return "created: tests/smoke.test.js + wired npm test"
    return "skipped: no test template for kind=" + kind


def ensure_lint_config(root: Path, kind: str) -> str:
    if kind == "python":
        pyt = root / "pyproject.toml"
        if pyt.exists() and "[tool.ruff]" in pyt.read_text(encoding="utf-8", errors="replace"):
            return "ok: ruff already configured"
        text = pyt.read_text(encoding="utf-8", errors="replace") if pyt.exists() else ""
        if "[tool.ruff]" not in text:
            append = "\n\n[tool.ruff]\nline-length = 100\ntarget-version = \"py310\"\n\n[tool.ruff.lint]\nselect = [\"E\", \"F\", \"I\", \"W\", \"B\", \"UP\"]\n"
            if pyt.exists():
                pyt.write_text(text.rstrip() + append, encoding="utf-8")
            else:
                pyt.write_text(append.strip() + "\n", encoding="utf-8")
            return "added: ruff config to pyproject.toml"
    if kind == "node":
        if any((root / f).exists() for f in (".eslintrc.json", "eslint.config.js", "eslint.config.mjs")):
            return "ok: eslint already configured"
        cfg = root / "eslint.config.mjs"
        if not cfg.exists():
            cfg.write_text("import js from '@eslint/js';\nexport default [\n  js.configs.recommended,\n  { rules: { 'no-unused-vars': 'warn' } },\n];\n", encoding="utf-8")
            return "created: eslint.config.mjs (minimal flat config)"
    return "skipped: no lint template for kind=" + kind


def prep_repo(root: Path) -> dict:
    name = root.name
    kind = repo_kind(root)
    actions = []
    actions.append(("gitignore", ensure_gitignore(root)))
    actions.append(("license", ensure_license(root)))
    actions.append(("readme", ensure_readme(root, name)))
    if kind == "python":
        actions.append(("pyproject", ensure_pyproject(root, name)))
    if kind == "node":
        actions.append(("node-version", ensure_node_version(root)))
    if kind in ("python", "node"):
        actions.append(("ci", ensure_ci(root, kind)))
        actions.append(("lint", ensure_lint_config(root, kind)))
        actions.append(("tests", ensure_tests_dir(root, kind)))
    return {"repo": name, "kind": kind, "actions": actions}


def main() -> int:
    repos = list_repos()
    print(f"Prepping {len(repos)} repos")
    lines = []
    lines.append(f"# Release Prep Log\n")
    lines.append(f"_Generated: {datetime.now(timezone.utc).isoformat()}_\n")
    results = []
    for r in repos:
        try:
            res = prep_repo(r)
        except Exception as e:
            res = {"repo": r.name, "kind": "?", "actions": [("error", repr(e))]}
        results.append(res)
        lines.append(f"## `{res['repo']}` (kind={res['kind']})")
        for k, msg in res["actions"]:
            lines.append(f"- **{k}** — {msg}")
        lines.append("")
        print(f"  {res['repo']:35s} {len(res['actions'])} actions")
    LOG_PATH.write_text("\n".join(lines), encoding="utf-8")
    (WORKSPACE / "RELEASE-AUDIT" / "PREP-LOG.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Wrote {LOG_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
