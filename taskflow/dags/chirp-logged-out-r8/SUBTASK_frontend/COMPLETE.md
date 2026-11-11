# SUBTASK_frontend — Completion Record

**Task**: Frontend Logged-Out Components  
**Status**: COMPLETED  
**Branch**: `work/chirp-logged-out`  
**Branch HEAD**: `21dca55` (feat(chirp-frontend): implement sign-up form at /signup route (AC-4))

---

## Outputs Delivered

### Primary: Git commits on `work/chirp-logged-out`

The frontend implementation was already complete on the branch before this task executed.
Key frontend commits:

| Commit | Message |
|--------|---------|
| `21dca55` | feat(chirp-frontend): implement sign-up form at /signup route (AC-4) |
| `fed1fc8` | fix(chirp-frontend): align public API structs with backend wire format |
| `e02b1d8` | feat(frontend): public timeline, user profile, sign-in/sign-up routes |

### Secondary: `frontend_summary.md`

Written to `SUBTASK_frontend/frontend_summary.md`. Documents routes, components, states,
state machine, test coverage, CI results, SSR strategy, and deviations from the analysis.

---

## Acceptance Criteria — Verified

| AC | Criterion | Status |
|----|-----------|--------|
| AC-1 | Logged-out visitor can load public timeline and open user profile without auth | ✓ Routes `/` and `/@:handle` have no auth guard |
| AC-2 | Empty state shows "what Chirp is" statement + sign-up/sign-in route | ✓ `empty_view()` in `landing.rs`; tested in `empty_model_renders_welcome_statement_and_cta_links` |
| AC-3 | Timeline load failure shows clear, recoverable message | ✓ Error state with retry button; tested in `initial_error_renders_error_message_and_retry_button` |
| AC-4 | "Create an account" route visible from landing and from sign-in screen | ✓ `nav_bar()` global nav + `header_nav()` in landing + "Already have an account?" link in sign-up view |
| AC-5 | Loading, empty, error, end-of-list states each visually distinct | ✓ 4 CSS classes (`chirp-loading`, `chirp-landing-empty`, `chirp-landing-error`, `chirp-list`+end note); each tested |

---

## CI Results

| Job | Result |
|-----|--------|
| `cargo fmt --all --check` | ✓ pass |
| `cargo clippy --workspace --all-targets --locked -- -D warnings` | ✓ pass |
| `cargo test --workspace --locked` | ✓ pass (76 chirp-frontend unit tests, 0 failures) |
| `cargo build -p chirp-frontend --target wasm32-unknown-unknown --locked` | ✓ pass |
| `cargo build -p chirp-frontend --example chirp --target wasm32-unknown-unknown --locked` | ✓ pass |
| `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps --locked` | ✓ pass |
