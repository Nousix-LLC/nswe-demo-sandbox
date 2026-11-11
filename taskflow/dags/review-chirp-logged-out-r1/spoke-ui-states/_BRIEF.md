# _BRIEF.md — Spoke: AC-2/3/4 UI States, Error Messages, and CTAs

## Objective

Review the user-visible UI behaviors introduced by PR #263 against AC-2, AC-3, and AC-4 of
issue #35, including the empty-state explanation, the recoverable error message, and the
sign-up / sign-in CTAs.

**AC-2**: On arrival with no content, the visitor sees a clear statement of what Chirp is plus
an obvious way to sign up/sign in — never a blank page or unexplained error.

**AC-3**: If the timeline fails to load, a clear, recoverable message is shown instead of a
broken screen.

**AC-4**: A "create an account" route is visible on the landing and on the sign-in screen, and
following it reaches sign-up.

## Inputs

- PR #263 diff: `Nousix-LLC/nswe-demo`, head `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Global context: `taskflow/dags/review-chirp-logged-out-r1/_GLOBAL.md`
- Primary code areas:
  - `crates/chirp-frontend/src/landing.rs` — `empty_view()`, `header_nav()`, `error_banner()`,
    `footer()`, and the `view_tree` dispatch logic
  - `crates/chirp-frontend/src/sign_in.rs` — sign-in stub, its "Create an account" link
  - `crates/chirp-frontend/src/sign_up.rs` — sign-up stub (note: may not be in the route table)
  - `crates/chirp-frontend/src/compose.rs` — `signup_view`, `render_signup`, the
    `link("/compose", "Log in →")` link in the sign-up form
  - `crates/chirp-frontend/src/app.rs` — route table: `/signup` → `signup_view` (compose.rs),
    `/signin` → `sign_in_view` (sign_in.rs), the `/sign-in` alias with its "for AC-3" comment

## Specific concerns this spoke must resolve

1. **AC-2 — Empty state content**: Does `empty_view()` in `landing.rs` explain what Chirp is
   and show a CTA? Does it qualify as "clear" rather than a blank or generic "No items" message?

2. **AC-3 — Error state recoverability**: Does the initial-error path in `view_tree` render a
   user-readable message (not a raw technical error) and a usable Retry action? Does the
   `role="alert"` attribute on the error banner satisfy the recoverable-message bar?

3. **AC-4 — CTA visibility and reachability**:
   - Is `header_nav()` present in EVERY rendered state of `landing_view`, including loading and
     error states?
   - Does the sign-in screen (`sign_in_view`) link to sign-up, and does following that link reach
     a usable sign-up page?
   - Two sign-up implementations exist: `sign_up.rs` exports `sign_up_view` (a placeholder stub
     with a disabled "Create account (coming soon)" button), and `compose.rs` exports
     `signup_view` (a functional form). The route table maps `/signup` → `signup_view`. Which
     implementation does a visitor actually reach, and is the reached implementation adequate for
     AC-4?

4. **CTA link correctness**: `compose.rs`'s `render_signup()` contains
   `link("/compose", "Log in →")`. Does this link to the right place for a logged-out visitor,
   or does it expose an internal compose path?

5. **Route annotation anomaly**: The `/sign-in` alias has a comment "for AC-3". AC-3 is about
   recoverable error messages; it has nothing to do with a route alias. Is this a copy-paste
   error or does it signal a misunderstanding?

## Declared output

A `REVIEW.md` at `taskflow/dags/review-chirp-logged-out-r1/spoke-ui-states/REVIEW.md`
containing:

- Verdict for this concern: PASS or FINDINGS
- For each finding: location (file + line at the pinned commit), what principle is at stake, why
  it matters in this system, severity (blocker / non-blocking), and what would satisfy it
- An account of what each sub-concern checked and found clean

## Success criteria

- Each of AC-2, AC-3, and AC-4 is explicitly adjudicated with evidence from the code
- The sign-up implementation ambiguity (stub vs. functional) is resolved
- Every CTA link's destination is verified correct and reachable
- The route annotation anomaly is noted as a finding or explained away

## Constraints

- Repository: `Nousix-LLC/nswe-demo` only
- Do not post to the PR; that is the synthesis child's responsibility
- Findings point at repository file paths and lines; do not name host paths, private IPs, or
  internal infrastructure details
