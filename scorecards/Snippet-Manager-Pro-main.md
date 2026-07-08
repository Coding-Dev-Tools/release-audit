# Release Audit: `Snippet-Manager-Pro-main`

- Path: `C:\Users\jomie\workspace\Snippet-Manager-Pro-main`
- Audited: 2026-06-16T07:41:16.378445+00:00
- Overall grade: **A**
- Angles passing (A/B): 7 / 8
- Release blockers: 1

| Angle | Grade | Findings |
|-------|-------|----------|
| security | D | 2 |
| dependencies | B | 11 |
| tests | A | 0 |
| lint-types | A | 0 |
| dead-code | B | 1 |
| errors-logging | A | 0 |
| docs | A | 0 |
| release | A | 0 |

## security (grade D)
- **SEC-HARDCODED-SECRET** — 3 possible hardcoded secret(s) outside tests/blog/prose/example
  - Fix: Move to env vars / secret manager, rotate
- **SEC-INJECTION-SINK** — 6 possible injection sink(s) outside tests/blog/build-scripts
  - Fix: Audit each call site, prefer parameterized queries and structured subprocess.run([...])

## dependencies (grade B)
- **DEP-FLOATING** — devDependencies.@babel/core = '^7.23.0' (floating)
  - Fix: Pin @babel/core to an exact version for reproducible builds
- **DEP-FLOATING** — devDependencies.@babel/preset-env = '^7.23.0' (floating)
  - Fix: Pin @babel/preset-env to an exact version for reproducible builds
- **DEP-FLOATING** — devDependencies.@commitlint/cli = '^20.5.0' (floating)
  - Fix: Pin @commitlint/cli to an exact version for reproducible builds
- **DEP-FLOATING** — devDependencies.@commitlint/config-conventional = '^20.5.0' (floating)
  - Fix: Pin @commitlint/config-conventional to an exact version for reproducible builds
- **DEP-FLOATING** — devDependencies.babel-jest = '^29.7.0' (floating)
  - Fix: Pin babel-jest to an exact version for reproducible builds
- **DEP-FLOATING** — devDependencies.bestzip = '^2.2.1' (floating)
  - Fix: Pin bestzip to an exact version for reproducible builds
- **DEP-FLOATING** — devDependencies.esbuild = '^0.27.3' (floating)
  - Fix: Pin esbuild to an exact version for reproducible builds
- **DEP-FLOATING** — devDependencies.eslint = '^8.56.0' (floating)
  - Fix: Pin eslint to an exact version for reproducible builds
- **DEP-FLOATING** — devDependencies.jest = '^29.7.0' (floating)
  - Fix: Pin jest to an exact version for reproducible builds
- **DEP-FLOATING** — devDependencies.jest-environment-jsdom = '^29.7.0' (floating)
  - Fix: Pin jest-environment-jsdom to an exact version for reproducible builds
- **DEP-FLOATING** — devDependencies.lint-staged = '^16.4.0' (floating)
  - Fix: Pin lint-staged to an exact version for reproducible builds

## tests (grade A)
- (no findings)

## lint-types (grade A)
- (no findings)

## dead-code (grade B)
- **DEAD-DEBUG-NOISE** — 478 debug print/console.log statements
  - Fix: Remove debug prints; rely on a real logger

## errors-logging (grade A)
- (no findings)
- _note_: Python repo (6 .py files) with no logging import

## docs (grade A)
- (no findings)
- _note_: No CHANGELOG file (acceptable for early-stage projects)

## release (grade A)
- (no findings)
