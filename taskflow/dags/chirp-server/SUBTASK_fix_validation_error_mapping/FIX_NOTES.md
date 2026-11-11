# FIX_NOTES.md — F1 remediation: DTO-validation failures now surface as the contract's 400 `ApiError`

Remediation fix-task for synthesis-gate finding **F1**. Operated on the shared clone, adding one
corrective commit on top of the three implementation spokes. Scope was strictly F1 — the
validation→400 error path — with no other behavior touched.

## Clone / branch / commit pointers

| What | Value |
|------|-------|
| Clone path | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/checkout` |
| Branch | `work/chirp-server` (base `main` @ `25e90c0`, untouched) |
| Predecessor HEAD (tests+docs spoke) | `ea08e73` |
| This fix's commit | `714d50f` — `fix(chirp-server): surface DTO-validation failures as 400 ApiError (F1)` |
| Backing store | `InMemoryRepository` — no database, no network bind |

## The violation (recap)

`POST /api/users` with `{"username":"has space", …}` (well-formed JSON, invalid `Username` value)
returned **422 Unprocessable Entity** with a plain-text body
(`Failed to deserialize the JSON body into the target type: …`). The `chirp-types` value objects
validate on deserialization via `#[serde(try_from = "String")]`, so the `try_from` failure became
axum's default `JsonRejection::JsonDataError` → 422 at the plain `axum::Json<T>` extractor boundary,
never routing through `ServerError::Validation` / `IntoResponse`. The contract
(`contracts/_MANIFEST.yaml` `error_mapping` row 1 + `_GLOBAL.md` "typed errors → HTTP status +
`ApiError`") requires **400 `VALIDATION_ERROR`** with an `ApiError` carrying `details`.

## What changed (approach)

A custom JSON body extractor funnels every body-decoding/validation rejection through the one error
seam (the idiomatic axum approach the brief flagged). Specifically:

| File | Change |
|------|--------|
| `src/api/json.rs` **(new)** | `pub struct ValidatedJson<T>(pub T)` implementing `FromRequest` by delegating to `axum::Json::<T>::from_request` and mapping the `JsonRejection` via `?`. Thin wrapper; behaves like `Json<T>` on success. |
| `src/error.rs` | New `ServerError::InvalidBody(String)` variant (→ `ErrorCode::ValidationError`, so 400 via the existing `code()`-keyed `IntoResponse`); `into_api_error()` arm lifts it into an `ApiError{code: VALIDATION_ERROR, details: [FieldError]}`; new `impl From<JsonRejection> for ServerError` preserving `rejection.body_text()` as the message. Existing variants and the domain `Validation(ValidationError)` path are unchanged. |
| `src/api/handlers.rs` | The three JSON-request-body handlers (`create_user`, `login`, `create_chirp`) extract with `ValidatedJson<T>` in place of `Json<T>`; response `Json<T>` is unchanged. Direct handler-level unit-test call sites updated to the new signature. Doc comments on the error path corrected. |
| `src/api/mod.rs`, `src/lib.rs` | Register `pub mod json;` and re-export `ValidatedJson` at the api module and crate root (symmetry with `AuthUser`). |
| `src/api/auth.rs` | `ignore`d doc example updated to `ValidatedJson` for accuracy. |
| `tests/api.rs` | The F1 characterization test flipped to assert the contract and **renamed** `invalid_dto_field_is_rejected_as_422_not_contract_400` → `invalid_dto_field_is_rejected_as_400_validation_error` (asserts 400 + `ApiError.code == VALIDATION_ERROR` + non-empty `details`). No test pins 422 any longer. |

Why `ServerError::InvalidBody` rather than forcing the rejection into the existing
`ServerError::Validation(ValidationError)`: the domain `ValidationError` requires a `&'static str`
field, which cannot honestly be reconstructed from a dynamic request rejection. Both variants map to
the same `VALIDATION_ERROR`/400 and the same `into_api_error()` machinery, so the wire result is
identical to a domain validation failure while existing variants stay untouched.

### Documented limitation (per brief)

The offending field name is **not** structurally recoverable from axum's `JsonRejection` (plain
`axum::Json` does not use `serde_path_to_error`), so `details` carries a single **generic**
`FieldError { field: "body", message: <rejection text> }`. The rejection text includes serde's
description of the failure. Recovering the exact field would require adding `serde_path_to_error`
(a new dependency) — deliberately not done, to keep the fix minimal; the generic `FieldError`
satisfies the contract's "populate details (Vec<FieldError>)" requirement.

## Observable outcomes (what the re-verification gate re-runs)

1. ✅ A well-formed-JSON body with an invalid DTO field value returns **400** + `ApiError{code:
   VALIDATION_ERROR, details:[FieldError…]}` (`details` non-empty). Covered by the flipped
   integration test and a new `error.rs` unit test (`invalid_body_maps_to_validation_code_with_a_generic_field_detail`).
2. ✅ Happy paths and every other error status (401/403/404/409/500) unchanged — all prior tests pass.
3. ✅ Characterization test updated to assert the 400 contract and renamed; no test pins 422.

## Local verification (all clean, authoritative gate commands)

| Check | Command | Result |
|-------|---------|--------|
| build | `cargo build --workspace` | ✅ exit 0 |
| test  | `cargo test` | ✅ all pass — chirp-server **24** lib (was 23 + 1 new error test) + **20** integration (incl. the flipped F1 test), no DB; other crates unchanged |
| fmt   | `cargo fmt -p chirp-server --check` | ✅ clean |
| clippy| `cargo clippy --all-targets -- -D warnings` | ✅ no warnings |

## Constraints honored

- One shared clone at `../checkout`; corrective commit `714d50f` added to `work/chirp-server`; **did not re-clone**.
- `main` untouched (HEAD still `25e90c0`; `714d50f` is not an ancestor of `main`). No force-push. **No commit-attribution trailers.**
- Wire types imported from `chirp-types`; **no DTO re-declared** (`ValidatedJson` is a transport wrapper, not a wire type).
- Fixed **only** F1. Did not touch the repository trait, other error variants' behavior, the frontend/#9, CI/#10–#13, or the F2 rustdoc intra-doc-link cleanup (left to its separate, non-gating concern).
