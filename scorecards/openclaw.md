# Release Audit: `openclaw`

- Path: `C:\Users\home\workspace\openclaw`
- Audited: 2026-06-16T07:41:08.496430+00:00
- Overall grade: **A**
- Angles passing (A/B): 7 / 8
- Release blockers: 1

| Angle | Grade | Findings |
|-------|-------|----------|
| security | D | 2 |
| dependencies | A | 0 |
| tests | A | 0 |
| lint-types | A | 0 |
| dead-code | A | 0 |
| errors-logging | A | 0 |
| docs | A | 0 |
| release | A | 0 |

## security (grade D)
- **SEC-HARDCODED-SECRET** — 1 possible hardcoded secret(s) outside tests/blog/prose/example
  - Fix: Move to env vars / secret manager, rotate
- **SEC-INJECTION-SINK** — 2 possible injection sink(s) outside tests/blog/build-scripts
  - Fix: Audit each call site, prefer parameterized queries and structured subprocess.run([...])

## dependencies (grade A)
- (no findings)

## tests (grade A)
- (no findings)

## lint-types (grade A)
- (no findings)

## dead-code (grade A)
- (no findings)

## errors-logging (grade A)
- (no findings)

## docs (grade A)
- (no findings)

## release (grade A)
- (no findings)
