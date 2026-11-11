# Review DAG Brief: review-chirp-logged-out-r2

**Repository**: Nousix-LLC/nswe-demo  
**PR**: #263 (`work/chirp-logged-out`)  
**Branch HEAD**: `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`  
**Issue**: #35 — "Logged-out reading and a useful landing with accurate states"  
**Review kind**: Re-review after remediation  
**Code DAG synthesis**: `taskflow/dags/chirp-logged-out-r27/SYNTHESIS.md` (PASS — both blockers fixed, CI 6/6 green)  
**Previous review**: `taskflow/dags/review-chirp-logged-out-r1/SYNTHESIS.md` (REQUEST-CHANGES)

---

## Context

PR #263 adds logged-out public timeline reading and user profile pages to the chirp frontend, plus the
server-side public endpoints they depend on. This is issue #35 ("Logged-out reading and a useful landing
with accurate states").

The first review (review-chirp-logged-out-r1, HEAD `decb6196`) returned REQUEST-CHANGES with two blockers
and eight non-blockers. The remediation DAG (chirp-logged-out-r27) produced a new commit on top of
`decb6196`, advancing the PR HEAD to `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`. CI is fully green (6/6:
fmt, clippy, test, wasm, doc, image — run 42249419769). PR is OPEN and MERGEABLE.

This re-review is held to the new HEAD `7f4b684`, not `decb6196`. The remediation commit claims to fix
exactly the two blockers — no other changes. The five acceptance criteria must still hold on this HEAD.

---

## Issue #35 — Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-1 | A logged-out visitor can load the home/public timeline and open a user profile and read chirps **without being forced to sign up or sign in first**. No auth wall on `/` or `/@:handle`. |
| AC-2 | On arrival with no content, the visitor sees a **clear statement of what Chirp is plus an obvious way to sign up or sign in** — never a blank page or unexplained error. |
| AC-3 | If the timeline fails to load, a **clear, recoverable error message** is shown — not a broken or blank screen. A retry path exists. |
| AC-4 | A "create an account" route is **visible on the landing and on the sign-in screen**; following it reaches sign-up. The sign-up page "Log in →" CTA must route to `/signin`. |
| AC-5 | The logged-out landing/timeline renders its loading, empty, error, and end-of-list states **accurately and distinctly** — each state has a unique combination of content and style; no two states collapse together. |

---

## Previous review: blockers that must now be fixed

**Blocker 1 (B1)** — `crates/chirp-frontend/src/timeline.rs:218`  
Previous HEAD `decb6196` had: `ctx.client().pub_timeline(&query)` — this routes authenticated users through
the global unauthenticated feed instead of their personalized `/api/timeline` feed.  
**Expected fix**: reverted to `ctx.client().timeline(&query)`.

**Blocker 2 (B2)** — `crates/chirp-frontend/src/compose.rs:519`  
Previous HEAD `decb6196` had: `link("/compose", "Log in →")` — the sign-up page "Log in →" CTA routed to
the compose view instead of the sign-in page.  
**Expected fix**: changed to `link("/signin", "Log in →")`.

The remediation DAG's SYNTHESIS.md at `taskflow/dags/chirp-logged-out-r27/SYNTHESIS.md` describes what was
changed. The re-review must verify those changes are correct and complete, and that no other changes were
introduced.

---

## Review concerns

The diff under review is a remediation commit on top of `decb6196`. Address these concerns fresh for this
diff; do not reuse review-r1's concern list wholesale.

### 1. Correctness of the two blocker fixes

Inspect `timeline.rs:218` and `compose.rs:519` on the new HEAD `7f4b684`:

- **B1**: Is `ctx.client().timeline(&query)` present? Does `timeline()` construct an authenticated client
  (includes `self.token`) and route to `/api/timeline`, not `/api/public/timeline`? Does the fix restore the
  behavior documented in the module-level doc at `timeline.rs:4`? Is there any remaining `pub_timeline` call
  in `timeline.rs` that could still route authenticated traffic through the public feed?
- **B2**: Is `link("/signin", "Log in →")` present at `compose.rs:519`? Does `/signin` resolve to the
  sign-in view in the router? Is the fix consistent with the route table?

For each fix: is it correct (the right behavior), is it complete (nothing else needs to change), and is it
minimal (no unintended side effects)?

### 2. All 5 ACs still hold on the new HEAD

AC-1 through AC-5 were evaluated on `decb6196` (four passed, two failed). The two targeted fixes are
single-line changes that should be orthogonal to the passing ACs. Confirm:

- AC-1: Public endpoints remain unguarded; the B1 fix is in `timeline.rs` which serves the *authenticated*
  timeline component (`/timeline`), not the public landing or public profile routes.
- AC-2: `empty_view()` in `landing.rs` is unchanged; still renders product identity and CTAs.
- AC-3: `error_banner` and retry logic in `landing.rs` unchanged.
- AC-4: The B2 fix is exactly what satisfies AC-4's sign-up "Log in →" requirement. Confirm the fix is
  present and consistent with the rest of `compose.rs`. Confirm the sign-in-to-sign-up path (`sign_in.rs`)
  is unchanged and still correct.
- AC-5: State branches in `landing.rs` and `public_profile.rs` are unchanged; still accurate and distinct.

### 3. Code quality

Are the two changes minimal and clean? Do they follow the codebase's code style and naming conventions? No
extraneous whitespace, comment, or refactoring introduced? No unintended refactoring of surrounding logic?

### 4. Test coverage

Are the two fixes adequately tested?
- For B1: Is there a test that explicitly confirms `timeline_view` calls `timeline()` (authenticated) rather
  than `pub_timeline()`? The previous review (review-r1) noted the fix would need a frontend test or
  manual verification; check whether one was added.
- For B2: Is there a test verifying `compose.rs:519` renders a "Log in →" link pointing to `/signin`? Check
  the existing test suite for `compose.rs` or the sign-up view.

If new tests were added, do they cover the fixed behavior and would they catch a regression?

### 5. Security

No new attack surface from either single-line change. Confirm:
- B1 fix: `timeline()` uses an authenticated client — no unintended credential handling introduced.
- B2 fix: a link destination change — no input, no processing, no surface.
- No host paths, internal network addresses (tailnet `100.x` or LAN IPs), internal server URLs, host runtime
  or taskflow directory paths committed in the diff.
- No new dependency or unsafe block introduced.

### 6. Regression check

Does the new commit introduce any change *other than* the two targeted single-line fixes? If the diff
contains any additional modifications (new files, removed lines, changed logic beyond `timeline.rs:218` and
`compose.rs:519`), those additional changes must be evaluated against the full review bar.

---

## Declared output

1. **Posted review** on PR #263 — the full verdict and per-concern findings. Because the PR author and the
   reviewer share the same account, a formal GitHub approval may not be possible; post the verdict and findings
   as a PR comment covering each concern and naming any new non-blocking findings. Every reviewed PR shows its
   review.

2. **Root `SYNTHESIS.md`** at `taskflow/dags/review-chirp-logged-out-r2/SYNTHESIS.md` with:
   - Verdict: **APPROVE** or **REQUEST-CHANGES**
   - Verdict on each blocker fix (B1, B2)
   - Verdict on each of the 5 ACs
   - Per-concern findings (what was checked and what was found, clean or not)
   - Any new non-blocking findings with severity and ID

3. **New non-blocking findings** (if any): filed as GitHub issues in Nousix-LLC/nswe-demo, linked to PR #263
   and issue #35. De-duplicate against existing open non-blockers (#264–#271 from review-r1). Write findings
   for the repository's readers: point at files and lines in the repository. Do not name host paths, tailnet
   addresses, or review DAG internal paths in the posted review, issues, or PR comments.

---

## Notes

- The diff to review is `decb6196..7f4b684` on `work/chirp-logged-out`. Inspect it with `gh pr diff 263 -R Nousix-LLC/nswe-demo` or `git diff decb6196 7f4b684`.
- Existing non-blockers #264–#271 (from review-r1) are already filed and do not need re-filing. If this review
  finds the same underlying gap at the same location, note it as already tracked rather than filing a duplicate.
- headless: true; landing_authority: delegated — the overseer will land the PR on APPROVE; this review is the
  approval gate.
