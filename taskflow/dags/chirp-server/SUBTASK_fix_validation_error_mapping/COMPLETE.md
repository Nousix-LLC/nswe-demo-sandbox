# COMPLETE — SUBTASK_fix_validation_error_mapping (F1 remediation)

**Status:** COMPLETED (Atomic)

## What was done

Fixed synthesis-gate finding **F1**: DTO-validation failures on the `chirp-server` HTTP surface now
conform to the frozen error contract. A request with well-formed JSON but an invalid DTO field value
returns **HTTP 400** with a `chirp_types::api::ApiError { code: VALIDATION_ERROR, details:
[FieldError…] }` body, instead of axum's former default **422** plain-text response.

Mechanism: a new `ValidatedJson<T>` request-body extractor (`src/api/json.rs`) delegates to
`axum::Json` and maps any `JsonRejection` — via a new `From<JsonRejection> for ServerError` into a
new `ServerError::InvalidBody` variant (→ `VALIDATION_ERROR`/400) — through the existing
`into_api_error()` / `IntoResponse` seam. The three JSON-body handlers (`create_user`, `login`,
`create_chirp`) use it in place of `Json<T>`. The F1 characterization test was flipped to assert the
contract and renamed `invalid_dto_field_is_rejected_as_400_validation_error`.

Full detail, the documented field-name limitation, and the file-by-file change list are in
`FIX_NOTES.md`.

## Outputs

- Corrective commit `714d50f` on `work/chirp-server` in the shared clone
  (`.../chirp-server/checkout`) — base `main` @ `25e90c0` untouched.
- `FIX_NOTES.md` (this workspace) — the handoff the re-verification gate reads.

## Success criteria — all met

- [x] Well-formed-JSON body + invalid DTO field value → 400 + `ApiError{code:VALIDATION_ERROR, details:[…]}` (non-empty).
- [x] `cargo build --workspace`, `cargo test`, `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings` all clean; no regression (chirp-server 24 lib + 20 integration tests pass, other crates unchanged).
- [x] Characterization test asserts the 400 contract, renamed; no test pins 422.
- [x] Committed to `work/chirp-server`; `main` untouched; no attribution trailers; no DTO re-declared.
- [x] `FIX_NOTES.md` written.

## For the dependent (`SUBTASK_reverify_gate`)

Re-run the authoritative gate commands against `work/chirp-server` HEAD `714d50f` and re-assert the
three F1 observable outcomes (see `FIX_NOTES.md` §"Observable outcomes"). F2 (rustdoc intra-doc-link
cleanup) was deliberately left untouched as a separate, non-gating concern.
