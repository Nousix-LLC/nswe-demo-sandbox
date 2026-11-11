# Findings — landing-states review

## Concerns checked

- AC-2 (empty_view content and CTA): `empty_view()` at lines 286–306 is clean — the
  view delivers a readable product description, two correctly-routed sign-up/sign-in links
  in a dedicated CTA container, and no blank or generic empty-state content.
- AC-3 (error state recoverability and role="alert"): the error path is substantively correct;
  one non-blocking finding — the test `initial_error_renders_error_message_and_retry_button`
  does not assert the `role="alert"` attribute that the implementation correctly sets, so
  removing it would not break the test.
- AC-4 partial (header_nav in all states): `header_nav()` is structurally guaranteed in every
  rendered state via a "hoist before branch" pattern at line 264; all four branch arms
  (loading, initial-error, empty, populated) confirmed clean.

## Findings

### Finding 1 — AC-3: test does not assert `role="alert"`

**Location**: `crates/chirp-frontend/src/landing.rs:584–598` at
`decb6196c2c1e6ed421d393a642f0c844cc333ba`

**Principle**: Acceptance-criterion tests should fail if the criterion they cover is broken.

**Rationale**: `error_banner` correctly sets `.attr("role", "alert")` on the `<p>` element at
line 380 — the implementation satisfies AC-3. The test
`initial_error_renders_error_message_and_retry_button` checks only text content (the error
message string and "Retry") via `text_content(&tree)`. Removing the `role="alert"` attribute
would leave this test green while silently regressing the ARIA attribute that AC-3 specifically
requires. `find_class` already walks attrs, so the gap is cheap to close.

**Severity**: non-blocking

**Resolution**: Add an assertion in `initial_error_renders_error_message_and_retry_button` (or a
dedicated `error_banner_has_role_alert` test) that locates the element with class `chirp-error`
and verifies it carries `("role", "alert")` in its attrs:

```rust
let banner = find_class(&tree, "chirp-error").expect("error banner present");
assert!(
    banner.attrs.iter().any(|(k, v)| k == "role" && v == "alert"),
    "error banner must carry role=alert for screen-reader announcement"
);
```

## Clean items

### AC-2 — empty_view() content and CTA

**Concern**: AC-2 — does `empty_view()` explain what Chirp is and present an obvious
sign-up/sign-in CTA?

**Checked**: `empty_view()` at lines 286–306 of `crates/chirp-frontend/src/landing.rs` at
`decb6196c2c1e6ed421d393a642f0c844cc333ba`, against three sub-criteria: (1) human-readable
product description, (2) sign-up/sign-in CTA presence and routing, (3) no blank or generic
empty-state content. Corroborating evidence read: module-level doc comment at lines 1–6,
`view_tree` call site at lines 248–253 and 262–283, and the test
`empty_model_renders_welcome_statement_and_cta_links` at lines 526–542.

**Result**: All three sub-criteria clean.

Sub-criterion 1: `empty_view()` renders an h2 heading "Welcome to Chirp" at
`crates/chirp-frontend/src/landing.rs:290 at decb6196c2c1e6ed421d393a642f0c844cc333ba`
and a `p.chirp-landing-description` with a plain-English product sentence at lines 293–296.
Neither element is a generic placeholder.

Sub-criterion 2: A `div.chirp-landing-cta` at line 299 contains exactly two links:
`link("/signup", "Create an account")` at line 301 and `link("/signin", "Sign in")` at line 303.
Both have explicit, correct routes and readable labels. The function's doc comment at line 286
confirms the intent is deliberate. Visual prominence depends on CSS outside this scope; structural
prominence is present.

Sub-criterion 3: `empty_view()` produces a non-blank tree with three substantive child
elements. The test asserts both class presence (`chirp-landing-empty`) and text content including
both product identity ("Welcome"/"Chirp") and action labels ("Create an account"/"Sign in");
the test would fail if the view returned a blank or generic node — a behavioral check, not an
existence check.

---

### AC-3 — error-state recoverability and role="alert" (clean parts)

**Concern**: AC-3 — user-readable message (not raw Rust error/debug repr), usable retry
action, and `role="alert"` on the error element.

**Checked**: `view_tree` initial-error branch at lines 243–251; `AppError::user_message()` in
`crates/chirp-frontend/src/error.rs` across all three enum arms; `error_banner` at lines 377–383;
test `initial_error_renders_error_message_and_retry_button` at lines 584–598.

**Result**: Three sub-criteria clean; one non-blocking finding on test coverage noted above.

Sub-criterion 1 (user-readable message): `AppError::user_message()` returns plain-English text
on all three enum arms — `Api` returns `api.message.clone()`, `Network` returns
`format!("Network error: {message}")`, `Transport` returns
`format!("Something went wrong: {message}")`. No path uses `{:?}` formatting or a raw debug
repr. The `Transport` arm can include technical detail ("HTTP status 500 for /api/chirps"), which
is readable but slightly technical; this is within AC-3 as stated.

Sub-criterion 2 (retry action): `button("Retry", on_retry)` at line 249 renders a
`<button type="button">` with a clear label wired to `reload(retry_ctx.clone())`, which calls
`model.begin_initial()` and re-triggers `request_load(ctx, LoadKind::Initial)` — a full
re-fetch. The test asserts `content.contains("Retry")`, pinning the label.

Sub-criterion 3 (role="alert" present in implementation): `error_banner` at lines 377–383
sets `.attr("role", "alert")` on the `<p>` element at line 380 on every call path. The
attribute is present in both the initial-error path (line 248) and the footer load-more-error
path (line 359), which share the same helper.

---

### AC-4 partial — header_nav() in every rendered state

**Concern**: AC-4-partial — is `header_nav()` present in EVERY rendered state of
`landing_view`?

**Checked**: `view_tree` function at lines 238–267; each of the four branch arms (loading state,
initial-error state, empty state, populated state); `header_nav()` definition at lines 270–277;
test `every_state_includes_header_nav_links` at line 509.

**Result**: Clean. `header_nav()` is called at line 264 outside all branching. The pattern
used is "hoist before branch": `body` is computed by the if/else at lines 243–260, then the
outer `section` is built unconditionally with `.child(header_nav()).child(body)` at lines
262–266. The guarantee is structural — no branch can accidentally omit `header_nav()` without
modifying the outer wrapper. All four enumerated branch arms confirmed.

`header_nav()` at lines 270–277 is itself non-conditional: it always returns a
`div.chirp-landing-nav` containing both nav links. The test `every_state_includes_header_nav_links`
at line 509 exercises the structural guarantee; because the guarantee is at the wrapper level, one
state is sufficient to verify coverage. The test checks the right thing — class attribute
presence and nav link text — and is behavioral.
