# release-audit

A small, dependency-free **8-angle release-readiness audit** for repositories.
Used by the shared `release-audit` GitHub workflow that each repo vendors in
`.github/workflows/release-audit.yml`.

## Usage

```bash
python audit.py <target_path> [--out-dir DIR] [--print]
```

- `target_path` — checkout of the repo to audit.
- `--out-dir` — where to write the scorecard JSON (default `scorecard`).
- `--print` — also print the scorecard JSON to stdout.

It writes `<out-dir>/<basename(target_path)>.json` and prints a human-readable
summary to stdout. Exit code is non-zero when there are blockers.

## The 8 angles

| # | Angle | Critical | What it checks |
|---|-------|:--------:|----------------|
| 1 | License | yes | `LICENSE` present and a recognized license (MIT, Apache, BSD, ISC, MPL, GPL, Unlicense, CC0…) |
| 2 | Security | yes | `SECURITY.md` present |
| 3 | README | yes | `README*` present and non-trivial (≥ 5 content lines) |
| 4 | CI | yes | `.github/workflows/*.yml` present |
| 5 | Tests | yes | `tests/` (or `test/`) with `test_*` files, or test files at repo root |
| 6 | Contributing | no | `CONTRIBUTING.md` present |
| 7 | CodeOfConduct | no | `CODE_OF_CONDUCT.md` present |
| 8 | Changelog | no | `CHANGELOG.md` present |

### Grades
- **A** fully meets · **B** meets · **C** partial · **D** missing-optional · **F** missing-critical
- `blockers` = number of angles graded **F**. The workflow fails the job when `blockers > 0`.
- `angles_passing` = number of angles graded A/B/C.
- `overall_grade`: `F` if any blocker, else A/B/C/D from the passing ratio.

## JSON contract

```json
{
  "repo": "target",
  "overall_grade": "B",
  "angles_passing": 5,
  "angles_total": 8,
  "blockers": 0,
  "angles": [
    {"angle": "License", "grade": "A", "detail": "LICENSE present, recognized license"},
    ...
  ]
}
```

## Workflow integration

```yaml
- name: Check out the shared release-audit harness
  uses: actions/checkout@v4
  with:
    repository: Coding-Dev-Tools/release-audit
    path: harness
    ref: main

- name: Run the 8-angle release audit
  working-directory: harness
  env:
    GITHUB_WORKSPACE: ${{ github.workspace }}
  run: |
    python audit.py "$GITHUB_WORKSPACE/target" --out-dir scorecard
```

The repo under audit must be checked out into `path: target` so the scorecard
filename (`target.json`) lines up with the workflow's reader.

## License

MIT — see [LICENSE](LICENSE).