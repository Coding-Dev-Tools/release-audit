# 5-Agent Release Improvement Report

_Generated: 2026-06-16 (post-5-agent pass)_

## Headline

After the 5 improvement agents ran (4 from previous turn + Agent E for release-readiness CI):

- **31 / 33 repos are A-grade (7-8 / 8 angles passing)**
- **2 / 33 repos are B-grade (6 / 8)** — context-mode and hermes-agent-review
- **0 C-grade, 0 D-grade**
- **120 remaining findings** (down from 273 in the original sweep)

| Stage | A | B | C | D | Findings |
|-------|---|---|---|---|---------:|
| Original sweep | 9 | 14 | 10 | 0 | 273 |
| + first prep pass | 19 | 14 | 0 | 0 | 182 |
| + 4-agent improvements | 31 | 2 | 0 | 0 | 123 |
| + 5-agent (release-audit CI) | 31 | 2 | 0 | 0 | 120 |

## What Agent E did

**Files:** `agents/agent_e_release_ci.py`, `agents/agent-e-release-ci.md` / `.log.json`

Added a reusable GitHub Actions workflow to every non-content repo (27 workflows total) that:

1. Checks out the target repo on every PR
2. Checks out the shared `RELEASE-AUDIT/` harness from `Coding-Dev-Tools/release-audit`
3. Runs the 8-angle audit
4. Posts the result as a Markdown table in the workflow log
5. **Fails the workflow on any D-grade angle** (release blocker)

This means every PR going forward gets an automatic release-readiness check. The team can't regress to D-grade without CI catching it.

## Status of remaining B-grade repos (real review items, not noise)

### context-mode (6/8)
- **security C (29 injection sinks in start.mjs / hooks/*.mjs / insight/server.mjs)** — all `execSync` calls with hardcoded shell commands (npm install, npx tsc, codesign). Currently safe but should be reviewed and ideally converted to list-form.
- **dead-code B (637 debug print/console.log statements)** — high volume in the bundled CLI files.

### hermes-agent-review (6/8)
- **security C (3 injection sinks in tools/)** — `subprocess.run(command, shell=True)` and `subprocess.Popen(stop_cmd, shell=True)` in `transcription_tools.py:518` and `environments/docker.py:638`. Both use controlled values but flagged for review.
- **dead-code B (5,775 debug print/console.log statements)** — overwhelmingly in red-teaming skills, where debug logging is expected.
- **errors-logging C (1,583 bare except/empty catch)** — across the entire repo; refactor to specific exceptions would be a separate project.

## Final artifact list

```
C:\Users\home\workspace\RELEASE-AUDIT\
├── PROTOCOL.md                  # the 8-angle inspection protocol
├── audit.py                     # per-repo auditor (Windows-friendly, pure stdlib)
├── audit_all.py                 # driver: audits every git repo
├── prep.py                      # 1st-prep fix-applier (idempotent)
├── build_summary.py             # builds SUMMARY.md
├── diff_summary.py              # builds the headline report
├── scorecards/                  # 33 × {repo}.json + {repo}.md
├── SUMMARY.md                   # ranked priority list
├── PREP-LOG.md                  # 1st-prep log
├── RELEASE-READINESS-REPORT.md  # post-1st-prep report
├── 4-AGENT-REPORT.md            # post-4-agent report
├── 5-AGENT-REPORT.md            # this report
└── agents/
    ├── agent_a_deps.py          # Deps & lockfiles
    ├── agent_b_lint.py          # Lint & type scripts
    ├── agent_c_docs.py          # Docs & tests
    ├── agent_d_security.py      # Security hardening (SECURITY.md, real key fix)
    ├── agent_e_release_ci.py    # Release-audit CI workflow
    ├── agent-a-deps.md / .log.json
    ├── agent-b-lint.md / .log.json
    ├── agent-c-docs.md / .log.json
    ├── agent-d-security.md / .log.json
    ├── agent-e-release-ci.md / .log.json
    ├── list_findings.py         # utility: dump findings by type
    ├── triage_secrets.py        # utility: show each hardcoded secret with context
    └── triage_sinks.py          # utility: show each injection sink with context
```

## Per-repo evidence (file changes)

**32 repos** got SECURITY.md
**27 repos** got `.github/workflows/release-audit.yml`
**12 repos** got `eslint.config.mjs`
**9 repos** got `Makefile`
**9 repos** got `uv.lock`
**7 repos** got `package-lock.json` or `pnpm-lock.yaml`
**32 repos** got `## Install` and `## Test` sections appended to README
**25 repos** got `tests/test_smoke.py` or `tests/smoke.test.js`
**1 real code fix** — `infra-scripts/ensure-optimal.cjs` now reads API keys from env vars instead of inlining them
**1 additional code fix** — `hermes-agent-review/hermes_cli/tools_config.py` cua-driver install no longer uses `shell=True` and the `curl | sh` anti-pattern

## How to verify

```bash
cd C:\Users\home\workspace

# Re-run the 8-angle audit
python RELEASE-AUDIT\audit_all.py

# Build the summary
python RELEASE-AUDIT\build_summary.py

# Rebuild the report
python RELEASE-AUDIT\diff_summary.py

# Re-run the 5 improvement agents (all idempotent)
python RELEASE-AUDIT\agents\agent_a_deps.py
python RELEASE-AUDIT\agents\agent_b_lint.py
python RELEASE-AUDIT\agents\agent_c_docs.py
python RELEASE-AUDIT\agents\agent_d_security.py
python RELEASE-AUDIT\agents\agent_e_release_ci.py
```
