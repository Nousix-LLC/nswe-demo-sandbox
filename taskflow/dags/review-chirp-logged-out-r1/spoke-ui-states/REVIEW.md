# Review — AC-2/3/4 UI States, Error Messages, and CTAs

Pinned commit: `decb6196c2c1e6ed421d393a642f0c844cc333ba`

---

## Verdict

**FINDINGS**

One blocker is open: the "Log in →" CTA on the sign-up page routes to `/compose` instead of
`/signin` (see Additional Findings, F1). AC-2 and AC-3 are clean. The main AC-4 concerns —
`header_nav` presence and the sign-in-to-sign-up path — are clean. The blocker is in the
sign-up page's navigation back to sign-in.

---

## AC-2 — Empty state

**Verdict: PASS**

`empty_view()` at `crates/chirp-frontend/src/landing.rs:286–306` satisfies all three
sub-criteria.

The function renders an h2 heading "Welcome to Chirp" at line 290 and a plain-English
description at lines 293–296 — neither is a generic placeholder. A `div.chirp-landing-cta`
at line 299 contains two correctly-routed links: `link("/signup", "Create an account")` at
line 301 and `link("/signin", "Sign in")` at line 303. The test
`empty_model_renders_welcome_statement_and_cta_links` at lines 526–542 asserts both class
presence and text content including product identity and action labels; it would fail if the
view returned a blank or generic node — the test is behavioral, not an existence check.

---

## AC-3 — Error state recoverability

**Verdict: PASS** (one non-blocking test-coverage finding)

The implementation satisfies all three sub-criteria. One non-blocking finding: the existing
test does not assert the `role="alert"` attribute it covers.

**What passes:**

- `AppError::user_message()` in `crates/chirp-frontend/src/error.rs` returns plain-English
  text on all three enum arms (`Api`, `Network`, `Transport`). No arm uses `{:?}` debug
  formatting. The `Transport` arm can include technical detail ("HTTP status 500 for
  /api/chirps"), which is readable; this is within AC-3 as stated.
- `button("Retry", on_retry)` at `landing.rs:249` renders a `<button type="button">` with a
  clear label wired to `reload(retry_ctx.clone())`, which calls `model.begin_initial()` and
  re-triggers `request_load`. The test asserts "Retry" is present.
- `error_banner` at `crates/chirp-frontend/src/landing.rs:377–383` sets
  `.attr("role", "alert")` on the `<p>` element at line 380 on every call path — the
  initial-error path (line 248) and the footer load-more-error path (line 359) share the
  same helper.

**Non-blocking finding — test does not assert `role="alert"`:**

- **Location**: `crates/chirp-frontend/src/landing.rs:584–598` at
  `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle**: Acceptance-criterion tests should fail if the criterion they cover is broken.
- **Rationale**: `initial_error_renders_error_message_and_retry_button` checks only
  `text_content` for the error message string and "Retry". Removing `.attr("role", "alert")`
  from `error_banner` would leave this test green while silently regressing the ARIA attribute
  that AC-3 specifically requires. `find_class` already walks attrs, so the gap is cheap to
  close.
- **Severity**: non-blocking
- **Resolution**: Add an assertion in `initial_error_renders_error_message_and_retry_button`
  (or a dedicated test) that locates the element with class `chirp-error` and verifies it
  carries `("role", "alert")` in its attrs:
  ```rust
  let banner = find_class(&tree, "chirp-error").expect("error banner present");
  assert!(
      banner.attrs.iter().any(|(k, v)| k == "role" && v == "alert"),
      "error banner must carry role=alert for screen-reader announcement"
  );
  ```

---

## AC-4 — Sign-up / sign-in CTAs

**Verdict: PASS on the core concerns.** One blocker (Additional Findings, F1) affects
navigation from the sign-up page back to sign-in.

**header_nav presence in every rendered state** — PASS

`header_nav()` is called at `crates/chirp-frontend/src/landing.rs:264` outside all branching
— "hoist before branch." The outer `section` is built unconditionally with
`.child(header_nav()).child(body)` at lines 262–266. The guarantee is structural: no branch can
accidentally omit it without modifying the outer wrapper. All four branch arms (loading,
initial-error, empty, populated) confirmed. `header_nav()` at lines 270–277 is itself
non-conditional — it always returns a `div.chirp-landing-nav` containing both nav links.
Test `every_state_includes_header_nav_links` at line 509 covers the structural guarantee.

**Sign-in-to-sign-up path** — PASS

`link("/signup", "Create an account")` at `crates/chirp-frontend/src/sign_in.rs:68` correctly
targets `/signup`. That route resolves at `crates/chirp-frontend/src/app.rs:148` to
`compose.rs::signup_view` — a functional form with live state management (`ComposeState::
signup_busy`) and an active `POST /users` submission path. The confusably-named
`sign_up.rs::sign_up_view` stub (disabled button, "coming soon" label, module doc
"intentionally non-functional") is not imported in `app.rs` and is not reachable from any
route.

**Sign-up-to-sign-in path** — see Additional Findings F1 (blocker)

The sign-up page contains `link("/compose", "Log in →")` at `compose.rs:519` that sends the
user to `/compose` instead of `/signin`. This is flagged below as a blocker.

---

## Additional findings

### F1 — Blocker: "Log in →" CTA routes to compose view instead of sign-in view

- **Location**: `crates/chirp-frontend/src/compose.rs:519` at
  `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle**: A CTA should route to the view whose purpose matches the stated user intent.
  The intent of "Log in →" on the sign-up page is to reach the sign-in flow, not the compose
  view.
- **Rationale**: A user on the sign-up page who clicks "Log in →" expects to reach `/signin`.
  The link sends them to `/compose` instead. While `compose_view` shows a login form when the
  session is absent, the destination is semantically wrong: the URL reads `/compose`, not
  `/signin`; any post-login redirect logic or UX behavior specific to `sign_in_view` is
  bypassed; and the route table names `/signin`/`/sign-in` as the canonical sign-in
  destinations, making the CTA's target contradict that design decision.
- **Severity**: blocker
- **Resolution**: Change `link("/compose", "Log in →")` to `link("/signin", "Log in →")` at
  `compose.rs:519`.

### F2 — Non-blocking: Route annotation cites wrong acceptance criterion

- **Location**: `crates/chirp-frontend/src/app.rs:13` at
  `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle**: Code comments must accurately attribute the acceptance criteria they satisfy.
  A comment citing the wrong AC number creates a false traceability link that misleads
  reviewers on re-reads.
- **Rationale**: The module doc comment reads `(alias for AC-3)` but AC-3 covers recoverable
  error messages, not routing. The same developer cited `(AC-4)` correctly at line 94 for
  `nav_bar()` entry points, suggesting the wrong AC-3 reference at line 13 is a likely
  copy-paste transposition. The route registration at line 147 is mechanically correct; the
  error is confined to the doc comment and has no runtime effect.
- **Severity**: non-blocking
- **Resolution**: Correct to `(alias for AC-4)` if the hyphenated alias was added to satisfy
  AC-4 sign-in navigation; or replace with `(hyphen-spelling alias)` if no specific AC
  motivated it.

---

## What was checked and found clean

**AC-2 — empty_view() content and CTA**: Examined `empty_view()` at
`crates/chirp-frontend/src/landing.rs:286–306`, the module-level doc comment at lines 1–6,
`view_tree` call site at lines 248–253 and 262–283, and test
`empty_model_renders_welcome_statement_and_cta_links` at lines 526–542. Product description
present (non-placeholder), CTA links present and correctly routed to `/signup` and `/signin`,
test is behavioral. All three sub-criteria pass.

**AC-3 implementation — error state recoverability**: Examined `view_tree` initial-error
branch at lines 243–251, `AppError::user_message()` across all three enum arms in `error.rs`,
`error_banner` at `landing.rs:377–383`, and test at lines 584–598. User-readable message on
all paths: confirmed. Retry action wired to a full re-fetch: confirmed. `role="alert"` present
in implementation: confirmed. Test coverage gap noted as non-blocking.

**AC-4 — header_nav structural guarantee**: Examined `view_tree` at lines 238–267 including
all four branch arms, and `header_nav()` definition at lines 270–277. The hoist-before-branch
pattern at line 264 makes the guarantee structural, not conditional. No branch can accidentally
omit it. Test `every_state_includes_header_nav_links` at line 509 covers the structural
guarantee correctly and is behavioral.

**AC-4 — sign-in-to-sign-up path**: Examined `sign_in.rs:68` (CTA link target),
`app.rs:148` (route registration), `compose.rs:627` (signup_view implementation), and
`sign_up.rs:23` (placeholder stub not in route table). The sign-in-to-sign-up navigation path
is correctly wired: a visitor clicking "Create an account" from the sign-in page reaches the
functional account-creation form.
