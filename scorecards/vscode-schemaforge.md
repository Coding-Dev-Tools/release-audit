# Release Audit: `vscode-schemaforge`

- Path: `C:\Users\jomie\workspace\vscode-schemaforge`
- Audited: 2026-06-16T07:41:16.543136+00:00
- Overall grade: **A**
- Angles passing (A/B): 7 / 8
- Release blockers: 0

| Angle | Grade | Findings |
|-------|-------|----------|
| security | C | 1 |
| dependencies | B | 6 |
| tests | A | 0 |
| lint-types | A | 0 |
| dead-code | A | 0 |
| errors-logging | A | 0 |
| docs | A | 0 |
| release | A | 0 |

## security (grade C)
- **SEC-INJECTION-SINK** — 1 possible injection sink(s) outside tests/blog/build-scripts
  - Fix: Audit each call site, prefer parameterized queries and structured subprocess.run([...])

## dependencies (grade B)
- **DEP-FLOATING** — devDependencies.@vscode/test-cli = '^0.0.4' (floating)
  - Fix: Pin @vscode/test-cli to an exact version for reproducible builds
- **DEP-FLOATING** — devDependencies.@vscode/test-electron = '^2.3.8' (floating)
  - Fix: Pin @vscode/test-electron to an exact version for reproducible builds
- **DEP-FLOATING** — devDependencies.typescript = '^5.3.0' (floating)
  - Fix: Pin typescript to an exact version for reproducible builds
- **DEP-FLOATING** — devDependencies.eslint = '^8.50.0' (floating)
  - Fix: Pin eslint to an exact version for reproducible builds
- **DEP-FLOATING** — devDependencies.@typescript-eslint/eslint-plugin = '^6.0.0' (floating)
  - Fix: Pin @typescript-eslint/eslint-plugin to an exact version for reproducible builds
- **DEP-FLOATING** — devDependencies.@typescript-eslint/parser = '^6.0.0' (floating)
  - Fix: Pin @typescript-eslint/parser to an exact version for reproducible builds

## tests (grade A)
- (no findings)

## lint-types (grade A)
- (no findings)

## dead-code (grade A)
- (no findings)
- _note_: 3 debug print(s) - low noise

## errors-logging (grade A)
- (no findings)

## docs (grade A)
- (no findings)
- _note_: No CHANGELOG file (acceptable for early-stage projects)

## release (grade A)
- (no findings)
