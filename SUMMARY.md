# Release Readiness Summary

- Repos audited: **33**
- A-grade: 31
- B-grade: 2
- C-grade: 0
- D-grade: 0

## Per-Repo Scorecard

| Repo | Overall | Pass | Blockers |
|------|---------|-----:|---------:|
| `context-mode` | **B** | 6/8 | 0 |
| `hermes-agent-review` | **B** | 6/8 | 0 |
| `Agent_Memory_Final` | **A** | 8/8 | 0 |
| `Coding-Dev-Tools-revenueholdings.dev` | **A** | 7/8 | 1 |
| `Coding-Dev-Tools.github.io` | **A** | 7/8 | 1 |
| `Obsidian-Vault-Local` | **A** | 7/8 | 0 |
| `SaaS-Churn-Predictor` | **A** | 8/8 | 0 |
| `Snippet-Manager-Pro-main` | **A** | 7/8 | 1 |
| `agent-os` | **A** | 7/8 | 1 |
| `api-contract-guardian` | **A** | 7/8 | 0 |
| `apiauth` | **A** | 8/8 | 0 |
| `awesome-python-fork` | **A** | 8/8 | 0 |
| `configdrift` | **A** | 7/8 | 0 |
| `crossrepo-dep-manager` | **A** | 8/8 | 0 |
| `datamorph` | **A** | 7/8 | 0 |
| `deploydiff` | **A** | 7/8 | 0 |
| `devforge-cli` | **A** | 7/8 | 0 |
| `devforge-core` | **A** | 8/8 | 0 |
| `envault` | **A** | 8/8 | 0 |
| `hermes-workspace` | **A** | 7/8 | 1 |
| `homebrew-tap` | **A** | 7/8 | 1 |
| `infra-scripts` | **A** | 8/8 | 0 |
| `json2sql` | **A** | 7/8 | 0 |
| `keybridge` | **A** | 7/8 | 0 |
| `openclaw` | **A** | 7/8 | 1 |
| `profitmax-pro` | **A** | 8/8 | 0 |
| `pypi-index` | **A** | 7/8 | 0 |
| `revenue-dashboard` | **A** | 7/8 | 1 |
| `revenueholdings.dev` | **A** | 7/8 | 1 |
| `rtk-command-code` | **A** | 7/8 | 1 |
| `schemaforge` | **A** | 7/8 | 0 |
| `scoop-bucket` | **A** | 7/8 | 1 |
| `vscode-schemaforge` | **A** | 7/8 | 0 |

## Top Common Findings (across all repos)

| Finding ID | Repos affected |
|------------|---------------:|
| `DEP-FLOATING` | 70 |
| `DOC-NO-TEST-INSTR` | 9 |
| `DEAD-DEBUG-NOISE` | 9 |
| `DEP-NO-LOCKFILE` | 9 |
| `TEST-NO-TESTS` | 8 |
| `SEC-INJECTION-SINK` | 7 |
| `ERR-BARE-EXCEPT` | 5 |
| `SEC-HARDCODED-SECRET` | 3 |

## Per-Angle Grade Distribution

| Angle | A | B | C | D |
|-------|--:|--:|--:|--:|
| security | 26 | 0 | 4 | 3 |
| dependencies | 19 | 5 | 9 | 0 |
| tests | 25 | 0 | 0 | 8 |
| lint-types | 33 | 0 | 0 | 0 |
| dead-code | 24 | 9 | 0 | 0 |
| errors-logging | 19 | 12 | 2 | 0 |
| docs | 24 | 9 | 0 | 0 |
| release | 33 | 0 | 0 | 0 |

## Repos Sorted By Priority (worst first)

### `context-mode` — grade B (6/8 passing, 0 blocker(s))
- C-grade `security`: 9 possible injection sink(s) outside tests/blog/build-scripts
- C-grade `dependencies`: No lockfile present (package-lock/pnpm-lock/yarn.lock/poetry.lock/uv.lock/Pipfile.lock); dependencies.@clack/prompts = '^1.0.1' (floating); dependencies.@mixmark-io/domino = '^2.2.0' (floating)

### `hermes-agent-review` — grade B (6/8 passing, 0 blocker(s))
- C-grade `security`: 3 possible injection sink(s) outside tests/blog/build-scripts
- C-grade `errors-logging`: 1583 bare except/empty catch

### `Agent_Memory_Final` — grade A (8/8 passing, 0 blocker(s))

### `Coding-Dev-Tools-revenueholdings.dev` — grade A (7/8 passing, 1 blocker(s))
- **BLOCKER** `tests`: No tests directory and no real test script

### `Coding-Dev-Tools.github.io` — grade A (7/8 passing, 1 blocker(s))
- **BLOCKER** `tests`: No tests directory and no real test script

### `Obsidian-Vault-Local` — grade A (7/8 passing, 0 blocker(s))
- C-grade `errors-logging`: 23 bare except/empty catch

### `SaaS-Churn-Predictor` — grade A (8/8 passing, 0 blocker(s))

### `Snippet-Manager-Pro-main` — grade A (7/8 passing, 1 blocker(s))
- **BLOCKER** `security`: 3 possible hardcoded secret(s) outside tests/blog/prose/example; 6 possible injection sink(s) outside tests/blog/build-scripts

### `agent-os` — grade A (7/8 passing, 1 blocker(s))
- **BLOCKER** `tests`: No tests directory and no real test script

### `api-contract-guardian` — grade A (7/8 passing, 0 blocker(s))
- C-grade `dependencies`: No lockfile present (package-lock/pnpm-lock/yarn.lock/poetry.lock/uv.lock/Pipfile.lock)

### `apiauth` — grade A (8/8 passing, 0 blocker(s))

### `awesome-python-fork` — grade A (8/8 passing, 0 blocker(s))

### `configdrift` — grade A (7/8 passing, 0 blocker(s))
- C-grade `dependencies`: No lockfile present (package-lock/pnpm-lock/yarn.lock/poetry.lock/uv.lock/Pipfile.lock)

### `crossrepo-dep-manager` — grade A (8/8 passing, 0 blocker(s))

### `datamorph` — grade A (7/8 passing, 0 blocker(s))
- C-grade `dependencies`: No lockfile present (package-lock/pnpm-lock/yarn.lock/poetry.lock/uv.lock/Pipfile.lock)

### `deploydiff` — grade A (7/8 passing, 0 blocker(s))
- C-grade `dependencies`: No lockfile present (package-lock/pnpm-lock/yarn.lock/poetry.lock/uv.lock/Pipfile.lock)

### `devforge-cli` — grade A (7/8 passing, 0 blocker(s))
- C-grade `dependencies`: No lockfile present (package-lock/pnpm-lock/yarn.lock/poetry.lock/uv.lock/Pipfile.lock)

### `devforge-core` — grade A (8/8 passing, 0 blocker(s))

### `envault` — grade A (8/8 passing, 0 blocker(s))

### `hermes-workspace` — grade A (7/8 passing, 1 blocker(s))
- **BLOCKER** `security`: 5 possible hardcoded secret(s) outside tests/blog/prose/example; 5 possible injection sink(s) outside tests/blog/build-scripts

### `homebrew-tap` — grade A (7/8 passing, 1 blocker(s))
- **BLOCKER** `tests`: No tests directory and no real test script

### `infra-scripts` — grade A (8/8 passing, 0 blocker(s))

### `json2sql` — grade A (7/8 passing, 0 blocker(s))
- C-grade `dependencies`: No lockfile present (package-lock/pnpm-lock/yarn.lock/poetry.lock/uv.lock/Pipfile.lock)

### `keybridge` — grade A (7/8 passing, 0 blocker(s))
- C-grade `dependencies`: No lockfile present (package-lock/pnpm-lock/yarn.lock/poetry.lock/uv.lock/Pipfile.lock)

### `openclaw` — grade A (7/8 passing, 1 blocker(s))
- **BLOCKER** `security`: 1 possible hardcoded secret(s) outside tests/blog/prose/example; 2 possible injection sink(s) outside tests/blog/build-scripts

### `profitmax-pro` — grade A (8/8 passing, 0 blocker(s))

### `pypi-index` — grade A (7/8 passing, 0 blocker(s))
- C-grade `security`: 1 possible injection sink(s) outside tests/blog/build-scripts

### `revenue-dashboard` — grade A (7/8 passing, 1 blocker(s))
- **BLOCKER** `tests`: No tests directory and no real test script

### `revenueholdings.dev` — grade A (7/8 passing, 1 blocker(s))
- **BLOCKER** `tests`: No tests directory and no real test script

### `rtk-command-code` — grade A (7/8 passing, 1 blocker(s))
- **BLOCKER** `tests`: No tests directory and no real test script

### `schemaforge` — grade A (7/8 passing, 0 blocker(s))
- C-grade `dependencies`: No lockfile present (package-lock/pnpm-lock/yarn.lock/poetry.lock/uv.lock/Pipfile.lock)

### `scoop-bucket` — grade A (7/8 passing, 1 blocker(s))
- **BLOCKER** `tests`: No tests directory and no real test script

### `vscode-schemaforge` — grade A (7/8 passing, 0 blocker(s))
- C-grade `security`: 1 possible injection sink(s) outside tests/blog/build-scripts
