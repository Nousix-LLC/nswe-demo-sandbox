# SUBTASK_frontend-ui — Completion Record

## Status: completed

## Task
Implement the logged-out visitor frontend in `crates/chirp-frontend` on branch
`work/chirp-logged-out`, satisfying AC-1 through AC-5.

## Outputs Produced

| Output | Location |
|--------|----------|
| `frontend-impl.md` | `SUBTASK_frontend-ui/frontend-impl.md` |
| Code commits | `work/chirp-logged-out` branch |

## AC Coverage

| AC | Verdict |
|----|---------|
| AC-1 — unauthenticated public timeline + user profile | Met |
| AC-2 — empty state with "what Chirp is" + sign-up/sign-in CTA | Met |
| AC-3 — recoverable timeline error state | Met |
| AC-4 — "Create an account" visible on landing and sign-in screen | Met |
| AC-5 — four visually distinct states (loading/empty/error/end-of-list) | Met |

## Quality Gates

| Gate | Result |
|------|--------|
| `cargo build -p chirp-frontend --target wasm32-unknown-unknown` | Pass |
| `cargo clippy -p chirp-frontend -- -D warnings` | Pass (0 warnings) |
| `cargo fmt -p chirp-frontend --check` | Pass |
| `cargo test -p chirp-frontend` | Pass (76/76) |

## Key Commits on Branch

- `e02b1d8` — feat(frontend): public timeline, user profile, sign-in/sign-up routes
- `fed1fc8` — fix(chirp-frontend): align public API structs with backend wire format
- `21dca55` — feat(chirp-frontend): implement sign-up form at /signup route (AC-4)
- `617f253` — fix(chirp-frontend): correct empty-state CTA links in timeline view
