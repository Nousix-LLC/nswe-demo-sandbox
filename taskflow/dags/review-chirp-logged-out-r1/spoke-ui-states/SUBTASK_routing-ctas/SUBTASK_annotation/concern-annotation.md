# Route annotation concern

## Concern: Route annotation anomaly — /sign-in "for AC-3" comment

## Checked

**File**: `crates/chirp-frontend/src/app.rs`  
**Pinned commit**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`

Three locations examined:

1. **Line 13** — module-level doc comment, route table entry:
   ```
   //! - `/sign-in`   -- [`sign_in_view`](crate::sign_in::sign_in_view) (alias for AC-3)
   ```
   This is the annotation under review. The parenthetical `(alias for AC-3)` attributes the
   hyphenated alias route to AC-3.

2. **Line 94** — `nav_bar()` function doc comment:
   ```
   /// `/signin` so logged-out visitors have visible entry points into each distinct flow (AC-4).
   ```
   Same file, same author, a few lines later: AC-4 is cited correctly for sign-in/sign-up
   navigation entry points. This shows the developer did reference AC numbers elsewhere, and
   used AC-4 for navigation concerns.

3. **Line 147** — actual route registration in `start()`:
   ```rust
   .route("/sign-in", move |_params| sign_in_view(&signin_hyphen_ctx))
   ```
   No inline comment here. The route resolves `/sign-in` (hyphenated) to `sign_in_view`,
   identical to the `/signin` (unhyphenated) primary registration on the line above. The
   behavior is mechanically correct.

**AC-3 description (from hub)**: Recoverable error messages on the timeline — error message
display, Retry button, `role="alert"` accessibility attribute. AC-3 concerns `landing.rs`
and the timeline view; it has no routing component and no documented connection to the
sign-in URL or its aliases.

**AC-4 description (from hub)**: Sign-in view → "Create an account" link → route resolution →
usable sign-up implementation at the destination. AC-4 concerns the navigability of the
sign-in-to-sign-up path; it involves the sign-in page and its outbound links.

## Verdict

fail

## Finding or Clean Item

**Location**: `crates/chirp-frontend/src/app.rs`, line 13, commit `decb6196`

**Principle**: Code comments must accurately attribute the acceptance criteria they satisfy.
A comment that cites the wrong AC number creates a false traceability link that misleads
reviewers, misleads the author on re-reads, and corrupts the record of which acceptance
criteria drove which implementation choices.

**Rationale**: AC-3 (recoverable error messages / Retry / `role="alert"`) has no documented
connection to sign-in URL routing. The comment `(alias for AC-3)` on the `/sign-in` alias
is therefore incorrect. The developer cited `(AC-4)` correctly at line 94 for the `nav_bar()`
entry points, which makes the wrong AC-3 reference at line 13 a likely copy-paste or
transposition error rather than a principled design decision. The most plausible intended
citation is AC-4 (which does motivate having a reachable sign-in URL), but the comment as
written does not support that reading.

**Behavioral bug assessment**: None. The route registration at line 147 is correct — `/sign-in`
aliases to `sign_in_view` exactly as the primary `/signin` route does. The annotation error
lives only in the module doc comment and does not affect routing behavior, link resolution,
or any other runtime property. No code path depends on the doc comment content.

**Severity**: non-blocking

**Resolution**: Correct the annotation at line 13. If AC-4 motivated the hyphenated alias
(so that any inbound `/sign-in` link resolves for logged-out visitors), change `(alias for AC-3)`
to `(alias; both spelling variants reach the sign-in view)` or `(alias for AC-4)` with a
brief rationale. If no specific AC motivated it and it is simply a URL tolerance alias,
remove the AC attribution and add a plain prose note, e.g. `(hyphen-spelling alias)`.
