# _BRIEF.md — chirp-logged-out-r27 (swe-coder)

## Goal

Remediate PR #263 (`work/chirp-logged-out`, head `decb6196c2c1e6ed421d393a642f0c844cc333ba`) against issue #35.
Two single-line blockers were found by the review and must be fixed. After fixing, all 5 ACs must pass and CI must remain green.

## Repository

`Nousix-LLC/nswe-demo`  
Branch: `work/chirp-logged-out`  
PR: #263

---

## Blockers to fix (verbatim — both are single-line regressions introduced by this PR)

### Blocker 1 — Authenticated home timeline routes through global unauthenticated feed

**File**: `crates/chirp-frontend/src/timeline.rs`, line 218  
**Current (wrong)**:
```rust
let result = ctx.client().pub_timeline(&query).await;   // ← was timeline()
```
**Fix**:
```rust
let result = ctx.client().timeline(&query).await;
```

`pub_timeline()` constructs an unauthenticated HTTP client (explicitly omits `self.token`) and routes to `/api/public/timeline`. Authenticated users navigating to `/timeline` now see the global public feed instead of their personalized following feed. The module doc at `timeline.rs:4` documents the correct call as `ctx.client().timeline(..)`. This line must revert exactly.

### Blocker 2 — "Log in →" CTA on sign-up page routes to compose view

**File**: `crates/chirp-frontend/src/compose.rs`, line 519  
**Current (wrong)**:
```rust
link("/compose", "Log in →")   // should be /signin
```
**Fix**:
```rust
link("/signin", "Log in →")
```

A user clicking "Log in →" from the sign-up page reaches `/compose` instead of `/signin`. The route table names `/signin` as the canonical sign-in destination.

---

## Prior context — what chirp-logged-out-r26 verified as good (do not regress)

`chirp-logged-out-r26` folded PASS on PR #263 (HEAD `decb6196`). The following was verified clean and must remain so:

- Three new public endpoints (`GET /api/chirps`, `GET /api/users/{username}/chirps`, `GET /api/public/timeline`) have no `AuthUser` extractor and are correctly unguarded.
- All previously auth-gated handlers (`create_chirp`, `timeline`, `follow`, `unfollow`, `like`, `unlike`) retain their `AuthUser` extractor unchanged.
- SQL in both new `postgres.rs` methods is correct: before-filter operator, null-cursor handling, ordering, soft-delete exclusion, two-query join safety, case-insensitive username lookup.
- `empty_view()` at `landing.rs:286–306` renders correctly with two CTAs (`/signup`, `/signin`).
- `error_banner` sets `role="alert"` on every call path; "Retry" wired to full re-fetch.
- `header_nav` is structurally guaranteed (hoist-before-branch).
- All four required states present in both `landing.rs` and `public_profile.rs` with distinct CSS classes and text.
- CI: 6/6 checks (fmt, clippy, test, wasm, doc, image) all PASS on `decb6196`.

---

## Acceptance criteria (all 5 must pass — from issue #35)

1. **AC-1**: A logged-out visitor can load the home/public timeline and open a user profile and read chirps without being forced to sign up or sign in first. (`REQ-PROD-013`, `BAR-011`)
2. **AC-2**: On arrival with no content, the visitor sees a clear statement of what chirp is plus an obvious way to sign up or sign in — never a blank page or an unexplained error. (`REQ-PROD-014`, `BAR-011`)
3. **AC-3**: If the timeline fails to load, a clear, recoverable message is shown instead of a broken screen. (`REQ-PROD-014`, `BAR-011`)
4. **AC-4**: A "create an account" route is visible on the landing and on the sign-in screen, and following it reaches sign-up. (`REQ-PROD-015`, `BAR-011`) — This includes: the sign-up page "Log in →" CTA must route to `/signin`, not `/compose` (Blocker 2).
5. **AC-5**: The logged-out landing/timeline exercises its loading, empty, error, and end-of-list states accurately and distinctly. (`REQ-UX-002/030/031/032`, `BAR-011`, one-state-model criterion)

---

## Constraints

- **No force-push.** Use `git push` (or `--force-with-lease` only if a rebase/squash requires it). PR #263 head must remain traceable.
- **CI must be green** after the fix commits: all 6 checks pass.
- Changes are limited to the two lines identified in Blockers 1 and 2 plus any tests that verify them. Do not alter the rest of the PR's logic.

---

## Declared output

1. Commits on `work/chirp-logged-out` that fix Blocker 1 and Blocker 2.
2. PR #263 updated with the new commits (or the existing PR head advanced on the same branch).
3. A root `SYNTHESIS.md` at the DAG workspace root, with:
   - Verdict: PASS or FAIL
   - Per-AC verdict table (AC-1 through AC-5), each with key evidence
   - CI status after the fix commits
   - New HEAD SHA on `work/chirp-logged-out`
