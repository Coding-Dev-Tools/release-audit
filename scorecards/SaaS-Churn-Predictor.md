# Release Audit: `SaaS-Churn-Predictor`

- Path: `C:\Users\jomie\workspace\SaaS-Churn-Predictor`
- Audited: 2026-06-16T07:41:10.474515+00:00
- Overall grade: **A**
- Angles passing (A/B): 8 / 8
- Release blockers: 0

| Angle | Grade | Findings |
|-------|-------|----------|
| security | A | 0 |
| dependencies | B | 20 |
| tests | A | 0 |
| lint-types | A | 0 |
| dead-code | B | 1 |
| errors-logging | B | 1 |
| docs | A | 0 |
| release | A | 0 |

## security (grade A)
- (no findings)

## dependencies (grade B)
- **DEP-FLOATING** — dependencies.@ai-sdk/openai-compatible = '^2.0.47' (floating)
  - Fix: Pin @ai-sdk/openai-compatible to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.@ai-sdk/react = '^3.0.186' (floating)
  - Fix: Pin @ai-sdk/react to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.@radix-ui/react-slider = '^1.3.6' (floating)
  - Fix: Pin @radix-ui/react-slider to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.@radix-ui/react-tabs = '^1.1.13' (floating)
  - Fix: Pin @radix-ui/react-tabs to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.@reduxjs/toolkit = '^2.12.0' (floating)
  - Fix: Pin @reduxjs/toolkit to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.@supabase/supabase-js = '^2.105.4' (floating)
  - Fix: Pin @supabase/supabase-js to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.@tailwindcss/postcss = '^4.3.0' (floating)
  - Fix: Pin @tailwindcss/postcss to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.@upstash/ratelimit = '^2.0.8' (floating)
  - Fix: Pin @upstash/ratelimit to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.@upstash/redis = '^1.38.0' (floating)
  - Fix: Pin @upstash/redis to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.ai = '^6.0.180' (floating)
  - Fix: Pin ai to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.clsx = '^2.1.1' (floating)
  - Fix: Pin clsx to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.date-fns = '^4.2.0' (floating)
  - Fix: Pin date-fns to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.framer-motion = '^12.40.0' (floating)
  - Fix: Pin framer-motion to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.lucide-react = '^1.16.0' (floating)
  - Fix: Pin lucide-react to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.next = '^15.5.18' (floating)
  - Fix: Pin next to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.react = '^19.2.6' (floating)
  - Fix: Pin react to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.react-dom = '^19.2.6' (floating)
  - Fix: Pin react-dom to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.recharts = '^3.8.1' (floating)
  - Fix: Pin recharts to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.resend = '^3.2.0' (floating)
  - Fix: Pin resend to an exact version for reproducible builds
- **DEP-FLOATING** — dependencies.sonner = '^2.0.7' (floating)
  - Fix: Pin sonner to an exact version for reproducible builds

## tests (grade A)
- (no findings)
- _note_: pyproject.toml references pytest

## lint-types (grade A)
- (no findings)

## dead-code (grade B)
- **DEAD-DEBUG-NOISE** — 178 debug print/console.log statements
  - Fix: Remove debug prints; rely on a real logger

## errors-logging (grade B)
- **ERR-BARE-EXCEPT** — 4 bare except/empty catch
  - Fix: Catch specific exceptions; log or re-raise

## docs (grade A)
- (no findings)

## release (grade A)
- (no findings)
