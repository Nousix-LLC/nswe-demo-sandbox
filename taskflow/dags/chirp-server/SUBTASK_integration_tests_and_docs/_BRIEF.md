# Task: End-to-end API integration tests + docs for `chirp-server`

## Task Specification

**Slug**: SUBTASK_integration_tests_and_docs
**Task Kind**: standard
**Status**: Pending

### Objective

Prove the assembled server works end-to-end and document it: author **API integration tests** that spin the
router against the in-memory repository and exercise the endpoints across the acceptance surface (status codes,
DTO round-trips, error paths), plus the crate **`README.md`** and rustdoc polish on public items — committed to
`work/chirp-server`.

### Context

This is the **verify-by-test + document stage** of the chirp-server pipeline. Your predecessors have committed
the full server (repository layer, then the axum API layer) into the shared clone; read
`../SUBTASK_api_layer/API_NOTES.md` for the route table and `../SUBTASK_scaffold_and_repository/IMPLEMENTATION_NOTES.md`
for the repository/error shape, and compose against the real committed code via the app builder exposed from
`lib.rs`. This stage does NOT change behavior — it tests and documents what exists. The subtree hub `_GLOBAL.md`
and `contracts/_MANIFEST.yaml` bind you.

**Dependencies**: `SUBTASK_api_layer`.
**Dependents**: `SUBTASK_synthesis_gate` (runs the authoritative build/test + opens the PR).

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, acceptance surface, success criteria |
| Contract | `../contracts/_MANIFEST.yaml` | Endpoint surface, error-mapping table (assert against it), identities |
| API handoff | `../SUBTASK_api_layer/API_NOTES.md` | Route table + how to mount the router + run instructions |
| Repository handoff | `../SUBTASK_scaffold_and_repository/IMPLEMENTATION_NOTES.md` | Trait + error enum shape for seeding/asserting |
| Committed code | the shared clone at the contract's `clone_path` | The real assembled server to test + document |
| Wire contract | `crates/chirp-types` | The DTOs to build requests from + decode responses into |

---

## Process / Approach

Mount the router via the `lib.rs` app builder against a fresh in-memory repository per test (no DB, no network
server needed — use an in-process request harness such as `tower::ServiceExt::oneshot` or an axum test client).
Cover the acceptance surface end-to-end: the happy paths (create user → login → post chirp → timeline;
follow/unfollow with follower-count changes; like/unlike with like-count changes; profile fetch; timeline
pagination) and the error paths against the contract's `error_mapping` table (validation → 400 `VALIDATION_ERROR`
with field details; missing resource → 404 `NOT_FOUND`; duplicate handle → 409 `CONFLICT`; missing/invalid token
→ 401 `UNAUTHORIZED`). Assert BOTH the HTTP status AND the decoded `chirp-types` DTO so the wire contract is
exercised, not just the status line. Then write `README.md` (endpoint list, how to run the server, the
repository-choice rationale + how to swap backings) and polish rustdoc on public items so `missing_docs` is
satisfied. Build + test locally, then commit. Which specific cases and how you structure the test modules are
YOUR calls. Re-run your own decompose-evaluation and decompose further if the test surface + docs genuinely prove
to be more than one responsibility for a single invocation.

### Methodology

Apply the suggested methodology below; you are the final judge of what you load.

---

## Output Specification

### Primary Output (handoff)

| Attribute | Value |
|-----------|-------|
| Filename | `TEST_NOTES.md` |
| Location | this workspace (`SUBTASK_integration_tests_and_docs/`) |

Record: the test inventory (what each test asserts), the local `cargo test` result, a map from each issue-#8
acceptance criterion to the test(s) covering it, and a one-line summary of the README. This is what the gate reads
to confirm coverage before it runs the authoritative build.

### Code output

`tests/**` integration tests + `crates/chirp-server/README.md` + rustdoc additions, committed to `work/chirp-server`.

---

## Success Criteria

- [ ] Integration tests mount the real router against an in-memory repo and pass with no DB/network.
- [ ] Happy-path + error-path coverage across the endpoint surface; both HTTP status AND decoded DTO asserted.
- [ ] Error paths assert the contract's `error_mapping` (400/401/404/409 with the right `ErrorCode`).
- [ ] `README.md` documents endpoints + how to run + repository-choice rationale; public items have rustdoc.
- [ ] `cargo test` passes locally; work committed to `work/chirp-server`; `TEST_NOTES.md` written.

---

## Suggested Methodology Files

Matched Domain-Mapping row: **Writing tests → primary `testing`; supporting `core`**; plus **Rust testing → `rust`**.

- `testing` — `testing/Testing_Integration_Testing_Methodology.md` (end-to-end API integration tests), `testing/Testing_Strategy_Methodology.md` (coverage of the acceptance surface), `testing/Testing_Test_Data_Management_Methodology.md` (per-test seeding of the in-memory repo).
- `rust` — `rust/Rust_Testing_Methodology.md` (Rust integration-test layout under `tests/`, async test harness for axum).
- `core` — `core/BestPractices_Coding_Standards_Methodology.md`, `core/CodeManagement_Commit_Practices_Methodology.md`; `operations/BestPractices_Documentation_Methodology.md` for the README if you load `operations`.

These are the parent's flagged methodologies; load them as a starting point and exercise your own judgment.

## Inherited Constraints

- Compose against the REAL committed server via the `lib.rs` app builder; do NOT modify handlers/repository to make tests pass (if a real defect surfaces, record it in `TEST_NOTES.md` for the gate — do not paper over it).
- No DB / no external infra for `cargo test`; edition 2021 / rust 1.82; workspace lints + `clippy -D warnings` clean.
- Import request/response types from `chirp-types`; never re-declare a DTO.
- ALL work in the ONE shared clone; never touch `main`; no commit-attribution trailers.

## Out-of-Scope Methodologies

- Do NOT add or change endpoints / repository behavior — this stage tests + documents the committed server.
- Do NOT push the branch or open the PR — that is `SUBTASK_synthesis_gate`'s job.
