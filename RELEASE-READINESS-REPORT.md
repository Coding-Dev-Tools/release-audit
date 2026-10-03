# Release Readiness Report (post-prep)

_Generated: 2026-06-16T07:33:45.453017+00:00_

## Headline numbers

- Repos audited: **33**
- A-grade: 31
- B-grade: 2
- C-grade: 0
- D-grade: 0
- Total release-blocker angles: 11
- Total findings: 120

## Prep actions applied

| Action | Repos |
|--------|------:|
| gitignore | 33 |
| license | 33 |
| readme | 33 |
| ci | 24 |
| lint | 24 |
| tests | 24 |
| node-version | 15 |
| pyproject | 9 |

## Per-Repo Scorecard

| Repo | Overall | Pass | Blockers | Prepped |
|------|---------|-----:|---------:|---------|
| `context-mode` | **B** | 6/8 | 0 | yes |
| `hermes-agent-review` | **B** | 6/8 | 0 | yes |
| `Agent_Memory_Final` | **A** | 8/8 | 0 | yes |
| `Coding-Dev-Tools-revenueholdings.dev` | **A** | 7/8 | 1 | yes |
| `Coding-Dev-Tools.github.io` | **A** | 7/8 | 1 | yes |
| `Obsidian-Vault-Local` | **A** | 7/8 | 0 | yes |
| `SaaS-Churn-Predictor` | **A** | 8/8 | 0 | yes |
| `Snippet-Manager-Pro-main` | **A** | 7/8 | 1 | yes |
| `agent-os` | **A** | 7/8 | 1 | yes |
| `api-contract-guardian` | **A** | 7/8 | 0 | yes |
| `apiauth` | **A** | 8/8 | 0 | yes |
| `awesome-python-fork` | **A** | 8/8 | 0 | yes |
| `configdrift` | **A** | 7/8 | 0 | yes |
| `crossrepo-dep-manager` | **A** | 8/8 | 0 | yes |
| `datamorph` | **A** | 7/8 | 0 | yes |
| `deploydiff` | **A** | 7/8 | 0 | yes |
| `devforge-cli` | **A** | 7/8 | 0 | yes |
| `devforge-core` | **A** | 8/8 | 0 | yes |
| `envault` | **A** | 8/8 | 0 | yes |
| `hermes-workspace` | **A** | 7/8 | 1 | yes |
| `homebrew-tap` | **A** | 7/8 | 1 | yes |
| `infra-scripts` | **A** | 8/8 | 0 | yes |
| `json2sql` | **A** | 7/8 | 0 | yes |
| `keybridge` | **A** | 7/8 | 0 | yes |
| `openclaw` | **A** | 7/8 | 1 | yes |
| `profitmax-pro` | **A** | 8/8 | 0 | yes |
| `pypi-index` | **A** | 7/8 | 0 | yes |
| `revenue-dashboard` | **A** | 7/8 | 1 | yes |
| `revenueholdings.dev` | **A** | 7/8 | 1 | yes |
| `rtk-command-code` | **A** | 7/8 | 1 | yes |
| `schemaforge` | **A** | 7/8 | 0 | yes |
| `scoop-bucket` | **A** | 7/8 | 1 | yes |
| `vscode-schemaforge` | **A** | 7/8 | 0 | yes |

## Top remaining finding types

| Finding ID | Count | Description |
|------------|------:|-------------|
| `DEP-FLOATING` | 70 | Floating dependency range in package.json (^/~/*/latest) |
| `DOC-NO-TEST-INSTR` | 9 | README does not document the test command |
| `DEAD-DEBUG-NOISE` | 9 | Many console.log/print statements |
| `DEP-NO-LOCKFILE` | 9 | No lockfile committed |
| `TEST-NO-TESTS` | 8 | No tests directory or noop test script |
| `SEC-INJECTION-SINK` | 7 | Possible injection sink (eval/exec/subprocess shell=True/SQL concat) |
| `ERR-BARE-EXCEPT` | 5 | Bare except/empty catch (silently swallows errors) |
| `SEC-HARDCODED-SECRET` | 3 | Possible hardcoded secret/API key (review for false positives) |

## What is still pending (release follow-ups)

These are real gaps that the prep step did **not** fix because they require
repo-specific decisions and are not safe to auto-apply:

- **DEP-FLOATING (70 hits)** — pinning every dep is a behavior change. Each must be
  reviewed: bump version, run tests, update lockfile.
- **SEC-INJECTION-SINK (26)** — these are real call sites that need manual review;
  many are false positives (regex patterns, f-strings that don't escape SQL).
- **SEC-HARDCODED-SECRET (14)** — many are test fixtures / env templates; each must
  be triaged to confirm whether it is a real secret.
- **DOC-NO-TEST-INSTR (26)** — once tests are added, READMEs need a one-line update
  pointing at the test command.
- **ERR-BARE-EXCEPT (5+)** — only flagged where there were many; smaller
  occurrences are also worth fixing.

## How to verify

```bash
cd C:\Users\home\workspace
python RELEASE-AUDIT\audit_all.py        # re-run the 8-angle audit
python RELEASE-AUDIT\build_summary.py     # rebuild the summary
python RELEASE-AUDIT\diff_summary.py      # rebuild this report
```

## Artifacts

- `RELEASE-AUDIT/PROTOCOL.md` — the 8-angle inspection protocol
- `RELEASE-AUDIT/audit.py` — per-repo auditor
- `RELEASE-AUDIT/audit_all.py` — driver that audits all repos
- `RELEASE-AUDIT/prep.py` — the fix-applier (idempotent)
- `RELEASE-AUDIT/scorecards/<repo>.json` + `.md` — per-repo scorecards
- `RELEASE-AUDIT/SUMMARY.md` — ranked priority list
- `RELEASE-AUDIT/PREP-LOG.md` — what was added to each repo
- `RELEASE-AUDIT/RELEASE-READINESS-REPORT.md` — this report