## Concern: AC-3 — error-state recoverability and role="alert"

**Status**: has_findings

## Checked

Reviewed `crates/chirp-frontend/src/landing.rs` and `crates/chirp-frontend/src/error.rs` at
pinned commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`.

**Initial-error branch located**: `view_tree` at lines 243–251. The branch fires when
`!model.loaded && model.error == Some(err)` — that is, when the first load has not yet completed
and an error was set. This is the full-screen initial-error state, distinct from the inline
load-more-error state rendered by `footer` (line 353–362) which is out of scope.

**Criteria applied**:
1. User-readable message — traced `err.user_message()` (line 248) through `AppError::user_message()`
   in `error.rs`; inspected all three enum arms for format.
2. Retry action — read the second `.child(...)` call (line 249) and traced `on_retry` to `reload()`.
3. `role="alert"` — read `error_banner` (lines 377–383) for the ARIA attribute.
4. Tests — read `initial_error_renders_error_message_and_retry_button` (lines 584–598) to check
   whether the test suite pins each criterion.

---

## Findings

### Finding 1 — Test does not assert `role="alert"`

**Location**: `crates/chirp-frontend/src/landing.rs:584–598` at `decb6196c2c1e6ed421d393a642f0c844cc333ba`

**Principle**: Acceptance-criterion tests should fail if the criterion they cover is broken.

**Rationale**: The implementation correctly sets `role="alert"` on `error_banner`'s `<p>` element
(line 380). However, the test `initial_error_renders_error_message_and_retry_button` uses
`text_content(&tree)` to assert only that the error message string and the word "Retry" are
present. It does not use `find_class(&tree, "chirp-error")` (or equivalent) to check that the
element carries `role="alert"`. Removing `.attr("role", "alert")` from `error_banner` would leave
this test passing while silently regressing the ARIA attribute that AC-3 specifically requires.
Given that `find_class` already walks attrs and could trivially extend to check `role`, the gap
is worth closing.

**Severity**: non-blocking

**Resolution**: Add an assertion to `initial_error_renders_error_message_and_retry_button` (or a
dedicated `error_banner_has_role_alert` test) that locates the element with class `chirp-error` and
verifies it carries `("role", "alert")` in its attrs:

```rust
let banner = find_class(&tree, "chirp-error").expect("error banner present");
assert!(
    banner.attrs.iter().any(|(k, v)| k == "role" && v == "alert"),
    "error banner must carry role=alert for screen-reader announcement"
);
```

---

## Clean Notes

### Sub-criterion 1 — User-readable message: CLEAN

**What was examined**: `error_banner(&err.user_message())` at line 248. Traced
`AppError::user_message()` in `error.rs` across all three enum arms:

- `AppError::Api(api)` → `api.message.clone()`: the server's typed human-readable message.
- `AppError::Network(message)` → `format!("Network error: {message}")`: plain-English prefix with
  the network error description.
- `AppError::Transport(message)` → `format!("Something went wrong: {message}")`: plain-English
  prefix; the embedded `{message}` can include "HTTP status 500 for /api/chirps" in the
  non-decodable-body path, which is technically worded but is not a Rust `{:?}` debug repr or an
  `Error { ... }` struct dump.

No path uses `{:?}` formatting, `format!("{:?}", err)`, or `.to_string()` on the raw error for
display. The `.user_message()` method was deliberately designed for user-facing output, distinct
from `Debug`/`Display` impls on the error type itself. AC-3's criterion ("not a Rust debug repr
or struct dump") is satisfied on every code path.

**Note** (not a finding): The `Transport` arm exposes technical detail ("HTTP status 500 for
/api/chirps") in the wrapped message. This is readable and not a debug repr, but a stricter UX
bar might prefer a more generic message for HTTP errors. That is outside the scope of AC-3 as
stated.

### Sub-criterion 2 — Retry action: CLEAN

**What was examined**: Line 249: `button("Retry", on_retry)`. The `button` helper (lines 385–391)
renders a `<button type="button">` with the given label wired to the click handler. The `on_retry`
closure captures the `AppContext` and calls `reload(retry_ctx.clone())` (line 231); `reload` calls
`model.begin_initial()` and re-triggers `request_load(ctx, LoadKind::Initial)`. The button
is clearly labeled "Retry", unambiguously identifies the available action, and is wired to a full
re-fetch of the initial timeline. The test `initial_error_renders_error_message_and_retry_button`
(line 594–596) also asserts `content.contains("Retry")`, pinning the label.

### Sub-criterion 3 — `role="alert"` present: CLEAN

**What was examined**: `error_banner` at lines 377–383:

```rust
fn error_banner(message: &str) -> VNode {
    VElement::new("p")
        .attr("class", "chirp-error")
        .attr("role", "alert")
        .child(text(message.to_string()))
        .into()
}
```

`.attr("role", "alert")` is explicitly set at line 380 on the `<p>` element that carries the
error message. This is a live-region role; screen readers will announce the content when it is
inserted into the DOM without requiring focus. The attribute is present on every call path that
renders an error message (both the initial-error path at line 248 and the footer load-more-error
path at line 359 share the same `error_banner` helper).
