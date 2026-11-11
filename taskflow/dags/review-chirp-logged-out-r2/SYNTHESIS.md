# SYNTHESIS — review-chirp-logged-out-r2

**Repository**: Nousix-LLC/nswe-demo  
**PR**: #263 (`work/chirp-logged-out`)  
**Head reviewed**: `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`  
**Issue**: #35  
**Verdict**: **APPROVE**

Both blockers from the r1 review are fixed and confirmed at HEAD. All five acceptance criteria pass. The remediation is one commit, two files, one line changed each. No regression. No new blockers.

---

## Verdict

gate: PASS  
round: 1 (re-review of r1 REQUEST-CHANGES)

---

## Checks

| Check | Result | Mechanical evidence |
|-------|--------|---------------------|
| Fix verdicts (B1, B2) | PASS | Direct file reads at `7f4b684`: `timeline.rs:218` = `timeline()`, `compose.rs:519` = `/signin` |
| AC verdicts (AC-1 through AC-5) | PASS | All five criteria satisfied; see per-AC table below |
| Regression | PASS | Diff `decb6196..7f4b684`: exactly two single-line changes, one commit, no collateral |
| New blocking findings | PASS | No new blockers; two test-coverage gaps (TC-B1, TC-B2) are non-blocking |

---

## B1 verdict: PASS

**File**: `crates/chirp-frontend/src/timeline.rs:218`  
**Head**: `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`

The r1 blocker was `ctx.client().pub_timeline(&query)` routing authenticated users to the global unauthenticated feed. At HEAD, line 218 reads:

```rust
let result = ctx.client().timeline(&query).await;
```

Confirmed by direct file read. `timeline()` uses `self.token` and routes to `GET /api/timeline` (the personalized authenticated feed). `pub_timeline()` is not called anywhere in `timeline.rs` at this HEAD. The module-level doc at `timeline.rs:4` documents `ctx.client().timeline(..)` as the correct call; the fix is consistent with its own specification.

---

## B2 verdict: PASS

**File**: `crates/chirp-frontend/src/compose.rs:519`  
**Head**: `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`

The r1 blocker was `link("/compose", "Log in →")` routing sign-up-page visitors to the compose view. At HEAD, line 519 reads:

```rust
.child(link("/signin", "Log in →")),
```

Confirmed by both direct file read and the PR diff (the corrected line appears as an addition). The `/signin` route resolves to `sign_in_view` in `app.rs`.

---

## Per-AC verdict table

| AC | Concern | Verdict | Key evidence |
|----|---------|---------|--------------|
| AC-1 | Public access without forced auth | PASS | `timeline.rs:218` calls `ctx.client().timeline()` (authenticated feed); `public_chirps`, `user_chirps`, `public_timeline` carry no `AuthUser` extractor and are mounted without an auth layer; frontend routes `/` and `/@:handle` are unguarded bare closures |
| AC-2 | Empty state | PASS | `empty_view()` renders "Welcome to Chirp" heading + `/signup` and `/signin` CTAs when `model.loaded && model.chirps.is_empty()`; `empty_model_renders_welcome_statement_and_cta_links` asserts heading and both links |
| AC-3 | Error state recoverability | PASS | `error_banner()` sets `role="alert"` on every call path; Retry triggers `reload(ctx)` → `model.begin_initial()` + full re-fetch; `initial_error_renders_error_message_and_retry_button` asserts message and Retry present |
| AC-4 | Sign-up / sign-in CTAs | PASS | `compose.rs:519` → `link("/signin", "Log in →")` confirmed; `/signin` resolves to `sign_in_view`; `header_nav()` renders both "Create account" (→ `/signup`) and "Sign in" (→ `/signin`) unconditionally on every landing-page render |
| AC-5 | State branches accurate and distinct | PASS | `landing.rs`: 4 named states (`Loading`, `Error`, `Empty`, `Loaded`), each with distinct render path and unit test; `public_profile.rs`: 6 named states via `LoadPhase` enum, each covered by a named unit test |

---

## Regression verdict: PASS

The remediation diff `decb6196..7f4b684` is exactly one commit, two files (`timeline.rs`, `compose.rs`), one addition and one deletion each. No new files, no dependency changes, no reformatting of neighboring code. The commit message ("fix(chirp-frontend): revert auth timeline to personalized feed, fix signup Log-in link") is accurate and correctly scoped.

---

## New non-blocking findings

| ID | Location | Severity | Description |
|----|----------|----------|-------------|
| TC-B1 | `crates/chirp-frontend/src/timeline.rs` | Non-blocking | No automated test verifies that `timeline_view` calls `ctx.client().timeline()` rather than `pub_timeline()`. The r1 B1 finding required "a frontend test or manual verification"; manual verification is complete and confirms the fix, but the automated regression guard is absent. A regression reverting line 218 would not be caught by the existing suite. |
| TC-B2 | `crates/chirp-frontend/src/compose.rs:519` | Non-blocking | No test verifies that `render_signup` renders "Log in →" pointing to `/signin`. A regression reverting to `"/compose"` would not be caught. |

Findings from r1 (issues #264–#271) remain open and are not re-filed here.

---

## Coverage assertion

- **B1 and B2 fix verdicts**: both present and PASS ✓
- **AC-1 through AC-5 verdicts**: all five present and PASS ✓
- **Regression verdict**: present and PASS ✓
- **New blocking findings**: none ✓
- **Contract identity assertions from `contracts/_MANIFEST.yaml`**:
  - `findings-fixes.md` carries explicit verdict for B1: PASS ✓
  - `findings-fixes.md` carries explicit verdict for B2: PASS ✓
  - `findings-acs.md` carries explicit verdict for each of AC-1 through AC-5: all PASS ✓
  - B1=PASS, B2=PASS, all 5 ACs=PASS, regression=PASS, no new blockers → verdict = APPROVE ✓

---

## What was clean

**B1 fix**: `ctx.client().timeline(&query)` confirmed at the exact line cited in r1. The module doc documents `timeline()` as correct; the fix aligns with its own specification. No other call to `pub_timeline` exists in `timeline.rs`.

**B2 fix**: `link("/signin", "Log in →")` confirmed at `compose.rs:519`, inside `render_signup`. The `/signin` route resolves correctly in the route table. The PR diff also shows the corrected line as an addition.

**Diff scope**: One commit, two files, one line changed each. No collateral changes found in the remediation diff.

**Code quality**: Both changes follow codebase naming and style conventions. No whitespace or formatting drift in surrounding code.

**Security**: B1 restores the authenticated feed with no new credential handling or token-exposure surface. B2 is a routing-string change in a rendered hyperlink with no input processing.

**AC-1 public access**: All three newly added backend handlers (`public_chirps`, `user_chirps`, `public_timeline`) carry no `AuthUser` extractor and are mounted without an auth layer. Auth-gated handlers retain their extractors unchanged. Frontend home and profile routes are unguarded, as r1 confirmed.

**AC-2 through AC-5**: The r1 PASS verdicts carry forward for all code not in the remediation diff. For the modified code (`compose.rs`) and previously-verified new code (`landing.rs`, `app.rs`), the verify-acs spoke confirmed correctness at HEAD through direct file inspection and PR diff analysis. State-branch coverage, error recoverability, and CTA routing all remain correct.
