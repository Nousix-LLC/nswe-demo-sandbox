# COMPLETE — spoke-error-safety

**Task**: Concern 8 — Error Message Safety (AppError / user_message())
**Status**: completed
**Output**: `error_safety_findings.md`

## Summary

Examined every `AppError` variant's `user_message()` return value at pinned commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`. Identified two non-blocking findings on the `AppError::Transport` path; the server-side `AppError::Api` path and the `AppError::Network` path are clean.

**Verdict**: FINDINGS (two non-blocking)

- Finding 1: `HttpError::Deserialize` propagates serde_json error message into the UI banner via `AppError::Transport`.
- Finding 2: `HttpError::Status` with non-JSON body includes the API endpoint URL in the UI banner.

## Files Read

- `crates/chirp-frontend/src/error.rs` — `AppError` enum, `user_message()`, `from_http()`
- `crates/ferric-http/src/error.rs` — `HttpError` enum and Display impls
- `crates/chirp-server/src/error.rs` — `ServerError`, `IntoResponse`, `into_api_error()`
- `crates/chirp-server/src/repository/postgres.rs` — ServerError instantiation sites
- `crates/chirp-frontend/src/landing.rs` — `user_message()` call sites and UI rendering
- `crates/chirp-frontend/src/api.rs` — `AppError::from_http` usage in API client methods
