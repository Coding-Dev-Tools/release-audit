# Release Audit: `hermes-workspace`

- Path: `C:\Users\home\workspace\hermes-workspace`
- Audited: 2026-06-16T07:40:56.535088+00:00
- Overall grade: **A**
- Angles passing (A/B): 7 / 8
- Release blockers: 1

| Angle | Grade | Findings |
|-------|-------|----------|
| security | D | 2 |
| dependencies | B | 20 |
| tests | A | 0 |
| lint-types | A | 0 |
| dead-code | B | 1 |
| errors-logging | B | 0 |
| docs | A | 0 |
| release | A | 0 |

## security (grade D)
- **SEC-HARDCODED-SECRET** — 5 possible hardcoded secret(s) outside tests/blog/prose/example
  - Fix: Move to env vars / secret manager, rotate
- **SEC-INJECTION-SINK** — 5 possible injection sink(s) outside tests/blog/build-scripts
  - Fix: Audit each call site, prefer parameterized queries and structured subprocess.run([...])

## dependencies (grade B)
- **DEP-FLOATING** — dependencies.@base-ui/react = '^1.1.0' (floating)
  - Fix: Pin @base-ui/react to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.@hugeicons/core-free-icons = '^3.1.1' (floating)
  - Fix: Pin @hugeicons/core-free-icons to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.@hugeicons/react = '^1.1.4' (floating)
  - Fix: Pin @hugeicons/react to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.@lobehub/icons = '^5.0.1' (floating)
  - Fix: Pin @lobehub/icons to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.@lobehub/icons-static-png = '^1.83.0' (floating)
  - Fix: Pin @lobehub/icons-static-png to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.@monaco-editor/react = '^4.7.0' (floating)
  - Fix: Pin @monaco-editor/react to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.@react-three/drei = '^10.7.7' (floating)
  - Fix: Pin @react-three/drei to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.@react-three/fiber = '^9.6.1' (floating)
  - Fix: Pin @react-three/fiber to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.@react-three/postprocessing = '^3.0.4' (floating)
  - Fix: Pin @react-three/postprocessing to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.@react-three/rapier = '^2.2.0' (floating)
  - Fix: Pin @react-three/rapier to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.@tailwindcss/vite = '^4.1.18' (floating)
  - Fix: Pin @tailwindcss/vite to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.class-variance-authority = '^0.7.1' (floating)
  - Fix: Pin class-variance-authority to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.clsx = '^2.1.1' (floating)
  - Fix: Pin clsx to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.ecctrl = '^1.0.97' (floating)
  - Fix: Pin ecctrl to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.electron-updater = '^6.6.2' (floating)
  - Fix: Pin electron-updater to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.framer-motion = '^12.36.0' (floating)
  - Fix: Pin framer-motion to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.marked = '^17.0.1' (floating)
  - Fix: Pin marked to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.motion = '^12.29.2' (floating)
  - Fix: Pin motion to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.motion-dom = '^12.36.0' (floating)
  - Fix: Pin motion-dom to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.motion-utils = '^12.36.0' (floating)
  - Fix: Pin motion-utils to an exact version for reproducible builds

## tests (grade A)
- (no findings)

## lint-types (grade A)
- (no findings)

## dead-code (grade B)
- **DEAD-DEBUG-NOISE** — 41 debug print/console.log statements
  - Fix: Remove debug prints; rely on a real logger

## errors-logging (grade B)
- (no findings)
- _note_: Python repo (3 .py files) with no logging import

## docs (grade A)
- (no findings)

## release (grade A)
- (no findings)
