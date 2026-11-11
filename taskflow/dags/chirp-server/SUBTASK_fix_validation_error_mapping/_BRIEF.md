# Task: Fix the DTO-validation error path to surface the contract's 400 `ApiError`

## Task Specification

**Slug**: SUBTASK_fix_validation_error_mapping
**Task Kind**: standard
**Status**: Pending

### Objective

Make DTO-validation failures on the `chirp-server` HTTP surface conform to the frozen error
contract: a request whose body is well-formed JSON but carries an invalid field value MUST return
**HTTP 400** with a `chirp_types::api::ApiError { code: VALIDATION_ERROR, details: [FieldError…] }`
body — **not** axum's current default **422 Unprocessable Entity** with a plain-text body. This is
the single violation the synthesis gate recorded as finding **F1**; fix only this.

### Context

This is a remediation fix-task injected by the `chirp-server` synthesis gate (`SUBTASK_synthesis_gate`)
after its verification run FAILED the `contract` identity. You operate on the **same shared clone**
that the three implementation spokes already committed to — you add a corrective commit on top; you
do **not** re-clone and do **not** touch any other behavior.

**Dependencies**: none declared at the task level (the three spokes are already COMPLETED and their
committed code is present in the clone; read it directly — do not add a task dependency on a
completed task).
**Dependents**: `SUBTASK_reverify_gate` (the re-verification gate) depends on this task.

### The violation (F1), precisely

- **Observed (mechanical evidence):** `POST /api/users` with `{"username":"has space", …}` — valid
  JSON, invalid `Username` value — returns **422** with a plain-text body
  (`Failed to deserialize the JSON body into the target type: …`). The passing characterization test
  `invalid_dto_field_is_rejected_as_422_not_contract_400` in
  `crates/chirp-server/tests/api.rs` pins this current (non-conforming) behavior.
- **Expected (contract):** `contracts/_MANIFEST.yaml` `error_mapping` row 1 — "input/DTO validation
  failure (incl. chirp-types ValidationError) → `VALIDATION_ERROR` → 400", note "Populate details
  (Vec<FieldError>) for validation failures" — and `_GLOBAL.md` success criterion "typed errors →
  HTTP status + `ApiError`".
- **Root cause:** validation happens at the serde boundary of the plain `axum::Json<T>` extractor
  (the `chirp-types` value objects use `#[serde(try_from = "String")]`); a `try_from` failure becomes
  axum's `JsonRejection::JsonDataError` → 422, never routing through `ServerError::Validation` /
  `IntoResponse`. The `ServerError::Validation → 400 VALIDATION_ERROR` arm of `IntoResponse` is
  consequently unreachable via HTTP.

### Required observable outcome (the re-verification gate re-runs these)

1. A request with a well-formed-JSON body but an invalid DTO field value returns **400** with an
   `ApiError` whose `code == VALIDATION_ERROR` and whose `details` carry at least one `FieldError`.
2. The happy paths and every other error status (401/403/404/409/500) are **unchanged** and still
   pass — no regression in the existing 43 tests.
3. The characterization test is **updated to assert the contract** (400 + `ApiError` +
   `VALIDATION_ERROR` + non-empty `details`) and renamed to reflect the corrected expectation (e.g.
   `invalid_dto_field_is_rejected_as_400_validation_error`). Do not leave a test that pins 422.

### Approach (you own the mechanism; these are the degrees of freedom, not a mandate)

The idiomatic axum options are a custom JSON extractor wrapper (e.g. `ValidatedJson<T>`) that maps a
`JsonRejection` to `ServerError::Validation`, or a `From<JsonRejection> for ServerError` plus use of
axum's rejection handling. Prefer the smallest change that routes deserialization/validation failures
through `ServerError::Validation` and the existing `into_api_error()` helper so the wire body is a
proper `ApiError`. Keep wire types imported from `chirp-types` (never re-declare a DTO). Where the
offending field name is recoverable from the serde error path, populate the `FieldError.field`;
otherwise a single generic `FieldError` is acceptable (document the limitation in your note).

### Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, success criteria |
| Contract | `../contracts/_MANIFEST.yaml` | The frozen `error_mapping` table (the target) + ownership |
| Gate verdict | `../SYNTHESIS.md` | The FAIL verdict + finding F1 this task remediates |
| API-layer handoff | `../SUBTASK_api_layer/API_NOTES.md` | Where `IntoResponse`, handlers, and the `Json` extraction live |
| Test handoff | `../SUBTASK_integration_tests_and_docs/TEST_NOTES.md` | F1 write-up + the characterization test to update |
| Committed code | the shared clone at `checkout/` | The real crate to fix (`crates/chirp-server/src/**`, `tests/api.rs`) |

### Output Specification

| Attribute | Value |
|-----------|-------|
| Primary | A corrective commit on `work/chirp-server` in the shared clone implementing outcomes 1–3 above |
| Handoff | `FIX_NOTES.md` in this workspace: what changed (files + approach), local build/test/fmt/clippy results, and confirmation the characterization test now asserts the 400 contract |

### Success Criteria

- [ ] A well-formed-JSON body with an invalid DTO field value returns 400 + `ApiError{code:VALIDATION_ERROR, details:[…]}`.
- [ ] `cargo build --workspace`, `cargo test`, `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings` all clean in the clone; no regression in existing tests.
- [ ] The characterization test asserts the contract (400 + `ApiError` + `VALIDATION_ERROR`), renamed accordingly; no test pins the old 422 behavior.
- [ ] Change is committed to `work/chirp-server`; `main` untouched; no commit-attribution trailers; no DTO re-declared.
- [ ] `FIX_NOTES.md` written.

## Suggested Methodology Files

Matched Domain-Mapping row: **Fixing bugs → primary `core`; supporting `testing`** (plus `rust` as
the implementation language and light `architecture` for the extractor boundary).

- `core` — `core/BestPractices_Error_Handling_Methodology.md` (the error-surfacing discipline this fix restores).
- `rust` — `rust/Rust_Error_Handling_Methodology.md` (error-enum → `IntoResponse` / `From` conversions; the axum extractor-rejection mapping is idiomatic `From`).
- `testing` — `testing/Testing_Integration_Testing_Methodology.md` (flip the characterization test to the contract assertion without destabilizing the suite).

These are the gate's flagged methodologies; load what your reading of the fix actually requires.
Re-run your own decompose-evaluation at dispatch — if the fix turns out to span more than the one
error-surfacing concern, decompose; it is expected to be `Atomic`.

## Inherited Constraints

- Operate on the ONE shared clone at `../checkout` (the contract's `clone_path`); add a commit to `work/chirp-server`. Do NOT re-clone.
- `chirp-types` is the single source of truth for wire types — import `ApiError`/`ErrorCode`/`FieldError`/`ValidationError`; never re-declare a DTO.
- Never commit to or force-push `main`. No commit-attribution trailers.
- Fix ONLY F1 (the validation→400 error path). Do not refactor unrelated code, do not touch the frontend/#9 or CI/#10–#13, and do not change the repository trait or other error variants.

## Out-of-Scope Methodologies

- Decomposition/synthesis methodologies are not for this task — you are a leaf fix, not a gate or a decomposer.
- The rustdoc intra-doc-link cleanup (gate finding F2) is a SEPARATE, non-gating concern — do NOT fold it into this fix.
