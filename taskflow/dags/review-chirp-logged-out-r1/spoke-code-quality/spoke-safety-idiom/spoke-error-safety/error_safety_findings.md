# Error Safety Findings — Concern 8

PR #263, `Nousix-LLC/nswe-demo`, pinned commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`.

---

## Verdict

FINDINGS

---

## Findings

### Finding 1: Client-side JSON deserialization failure propagates serde_json error into the UI banner

- **Location**: `crates/ferric-http/src/error.rs`, line 111; `crates/chirp-frontend/src/error.rs`, line 60 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle at stake**: User-facing errors must not expose internal implementation details — stack traces, schema structure, or any detail beyond what the user needs to act.
- **Why it matters**: When a 2xx server response fails client-side JSON deserialization (for example, during a rolling deployment where the server and client types are mismatched), `AppError::from_http` reaches the catch-all arm at line 60 (`other => AppError::Transport(other.to_string())`). For `HttpError::Deserialize`, `to_string()` calls the Display impl at `ferric-http/src/error.rs` line 111, producing `"failed to deserialize response body: {serde_error}"`. The serde_json error message then flows through `user_message()` as `"Something went wrong: failed to deserialize response body: missing field \`chirps\` at line 1 column 2"` and is rendered verbatim in the error banner (`landing.rs` line 248, 359). The exposed text names expected JSON fields from the response type — `chirps`, `hasMore`, etc. — which are the wire schema's field names. While these are camelCase (not raw Rust field names), they reveal the expected response structure to anyone who encounters the error. This path is reachable in production during deployments.
- **Severity**: non-blocking
- **Satisfying condition**: `AppError::from_http` should handle `HttpError::Deserialize` explicitly before the catch-all arm, producing a fixed message such as `"failed to process server response"` and suppressing the serde_json detail from `user_message()`. The serde error should be retained for logging, not surfaced to the banner.

---

### Finding 2: HTTP status error with non-JSON body includes the API endpoint URL in the UI banner

- **Location**: `crates/chirp-frontend/src/error.rs`, lines 53–57 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle at stake**: User-facing error messages should not embed implementation details the user cannot act on.
- **Why it matters**: When the server returns a non-2xx response with a body that does not decode as `ApiError` JSON (for example, a proxy-level 502 returning HTML), `AppError::from_http` constructs `format!("HTTP status {status} {status_text} for {url}")` and stores it in `AppError::Transport`. This message, including the full API endpoint URL, reaches the error banner via `user_message()`: `"Something went wrong: HTTP status 502 Bad Gateway for /api/timeline"`. The URL is the client-constructed path, not an internal server filesystem path, but it still embeds API endpoint structure in a user-visible string. The endpoint paths are visible in browser DevTools, so the exposure is low; still, the URL adds no information the user can act on and a generic form suffices.
- **Severity**: non-blocking
- **Satisfying condition**: The Status-with-non-JSON-body branch should emit a message that includes the status code but omits the URL — for example `"HTTP status {status}"` or `"HTTP status {status} {status_text}"`. The full URL and body should be logged for diagnostics rather than surfaced in `user_message()`.

---

## Clean Account

- **Concern 8 — `AppError::Api` path (server-authored messages)**: Checked `IntoResponse` for `ServerError` in `crates/chirp-server/src/error.rs`. `Internal` and `Unavailable` are sanitized at the wire boundary: the SQLx/database error is logged under `tracing::error!` and the wire `ApiError.message` is hardcoded to `"an internal server error occurred"`. All SQLx errors in `crates/chirp-server/src/repository/postgres.rs` are wrapped in `ServerError::Internal`, none in user-visible variants. The human-authored strings for `NotFound`, `Conflict`, `Unauthorized`, and `Forbidden` describe domain facts (e.g., `"user 'alice'"`, `"invalid or expired session token"`) without including database error text, SQL, stack traces, or internal paths. The `InvalidBody` variant stores `axum::extract::rejection::JsonRejection::body_text()`, which for a JSON deserialization failure names camelCase field names from the public request schema rather than internal Rust type names; found no internal-implementation detail in this path. Found Finding 1 and Finding 2 on the `AppError::Transport` path; the `AppError::Api` path itself is clean.

- **Concern 8 — `AppError::Network` path**: Checked `HttpError::Network` in `crates/ferric-http/src/error.rs`. Network errors originate in the browser Fetch API (messages such as `"Failed to fetch"`), not from server internals. `user_message()` for this variant produces `"Network error: {message}"`. No server-side implementation detail is exposed. Found clean.

- **Concern 8 — `AppError::Transport` path**: Checked `AppError::from_http` in `crates/chirp-frontend/src/error.rs` and the full `HttpError` Display impls in `crates/ferric-http/src/error.rs`. The `HttpError::Status` branch with a non-JSON body includes the API endpoint URL in the banner string (Finding 2). The catch-all arm passes `HttpError::Deserialize`'s `to_string()` — a serde_json error — directly into `user_message()` (Finding 1). The `Builder` and `Body` variants produce client-side error descriptions (`"failed to build request: …"`, `"failed to read response body: …"`) with no server-internal content; found clean.

- **Concern 8 — UI rendering path**: Checked `user_message()` call sites in `crates/chirp-frontend/src/landing.rs` (lines 248, 359). The return value of `user_message()` is passed as a string argument to `error_banner()` and rendered in the DOM. No escaping or further filtering occurs between `user_message()` and the visible banner text, confirming that whatever `user_message()` returns reaches the user verbatim.
