# Senior-Dev 8-Angle Release Inspection Protocol

A repo is "release-ready" when it passes all 8 angles. Each angle is run
by a focused sub-agent (in this turn, the harness emits findings for all
8 in one pass; in production these would be 8 parallel sub-agents).

## The 8 Angles

1. **Security & Secrets** - no hardcoded API keys, no committed `.env`,
   no `eval`/`exec` of remote input, dependencies free of known critical CVEs,
   no obvious injection sinks (SQL/command/template).
2. **Dependencies & Supply Chain** - lockfile present and committed,
   `package.json`/`pyproject.toml` pinned (not floating), no `latest`
   ranges for runtime deps, no abandoned/deprecated deps.
3. **Tests & Coverage** - test framework installed, >= 1 test runs green,
   coverage config present, CI workflow actually runs tests.
4. **Static Quality & Lint** - linter configured, type-checker configured
   (tsc / mypy / ruff), no `noqa`/`eslint-disable` abuse, formatter
   present (prettier/black/ruff-format).
5. **Dead Code & Complexity** - no `console.log`/`print` debug,
   no commented-out blocks, no TODO/FIXME older than 90 days,
   no `*.bak` / `*.tmp` / `_tmp_*` files tracked, file size sane
   (< 1000 LOC per file unless generated).
6. **Errors, Logging & Observability** - error boundaries exist for
   user-facing code, no bare `except:`/`catch{}` swallowers,
   structured logging used, no `print` used as the only logger.
7. **Documentation & Onboarding** - README present and not stub,
   LICENSE present (unless explicitly unlicensed), CHANGELOG or
   release notes, install + run + test instructions accurate.
8. **Release Engineering** - CI workflow present, version pin,
   Dockerfile or build script, no `// FIXME release` markers,
   `package.json` `version` / `pyproject` `version` present,
   no `dist/`/`build/` committed, `.gitignore` covers
   `node_modules`, `__pycache__`, `.env`, `dist`, `build`.

## Per-Repo Score

Each angle emits findings graded A/B/C/D where:
- **A**: angle fully satisfied
- **B**: minor issues, no blockers
- **C**: real gaps, fixable in <1 hour
- **D**: blocker for release

Overall release-readiness = number of A/B angles / 8.

## Per-Repo Findings Format

```
repo: <name>
angle: <one of 8>
grade: A|B|C|D
findings:
  - <id>: <file:line> <description>
recommendation: <concrete next step>
```

Findings are emitted as JSON, then rendered to a Markdown scorecard.
