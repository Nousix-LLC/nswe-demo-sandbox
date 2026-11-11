# COMPLETE — SUBTASK_check-ac3

## Task

Adjudicate AC-3 (error-state recoverability and `role="alert"`) for
`crates/chirp-frontend/src/landing.rs` at pinned commit
`decb6196c2c1e6ed421d393a642f0c844cc333ba`.

## Work Done

- Fetched `landing.rs` and `error.rs` from `Nousix-LLC/nswe-demo` at the pinned commit.
- Located the initial-error branch in `view_tree` (lines 243–251).
- Traced `AppError::user_message()` in `error.rs` across all three enum arms; confirmed no
  `{:?}` debug repr on any path.
- Verified `button("Retry", on_retry)` at line 249 is wired to `reload()`.
- Verified `.attr("role", "alert")` at line 380 in `error_banner`.
- Read `initial_error_renders_error_message_and_retry_button` (lines 584–598); confirmed the test
  does not assert `role="alert"`.

## Outputs

- `concern_ac3.md` — finding schema per `../contracts/_MANIFEST.yaml`

## Summary

**Status**: `has_findings`

All three implementation criteria pass. One non-blocking finding: the existing test
`initial_error_renders_error_message_and_retry_button` does not assert that `role="alert"` is
present on the error banner element, creating a regression gap for the ARIA attribute.
Resolution: add an attribute assertion using `find_class(&tree, "chirp-error")` and check
`banner.attrs` contains `("role", "alert")`.
