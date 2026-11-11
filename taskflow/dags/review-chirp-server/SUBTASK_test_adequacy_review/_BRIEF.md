# Task: Test adequacy review of chirp-server (PR #19)

## Task Specification
**Slug**: SUBTASK_test_adequacy_review
**Task Kind**: standard
**Status**: Pending

### Objective
Review the `chirp-server` test suite (PR #19, head `714d50f`) through the **single lens of test
adequacy**, and emit `findings_test_adequacy.md` conforming to the findings contract. You assess the
tests' adequacy; you do NOT write or edit tests, and you do NOT push.

### Context
Part of the review-chirp-server review DAG (`../_GLOBAL.md`). You own AC8 and the F1 test questions
(F1_2, F1_4). Sibling spokes own Rust soundness, architecture/contract, and code-review quality.

**Dependencies**: none. **Dependents**: `SUBTASK_synthesis_verdict`.

## Input Specification
| Input | Source | Purpose |
|-------|--------|---------|
| Hub | `../_GLOBAL.md` | Shared context, input set, discipline |
| Findings contract | `../contracts/findings_schema.md`, `../contracts/_MANIFEST.yaml` | Output shape; owned AC8, F1_2, F1_4 |
| PR diff | `gh pr diff 19 -R Nousix-LLC/nswe-demo` | The change under review |
| Tests | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/checkout/crates/chirp-server/tests/` and in-module `#[cfg(test)]` unit tests under `src/` | The suite to assess (44 = 24 unit + 20 integration, no DB) |
| App surface | `.../checkout/crates/chirp-server/src/lib.rs` | Confirm tests drive the REAL app (router + in-memory repo) via `lib.rs` |
| Contract crate | `.../checkout/crates/chirp-types/` | The error rows / DTOs the tests should exercise |
| Code DAG verdict | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/SYNTHESIS.md` | Context: test[44] passed cold, no DB |

## Review Concern (one responsibility: test adequacy)
- **AC8 — adequacy & wiring**: does the suite exercise the **real app via `lib.rs` against the
  in-memory repo** (not mocks that bypass the app), with **no database** anywhere? Assess coverage
  of the full REST surface and the behavioral rules: timeline reverse-chronological ordering,
  **limit-clamp**, cursor paging; follow/unfollow & like/unlike idempotency; conflict/duplicate (409).
- **Error-row coverage**: integration tests for each contract error row — 400 VALIDATION_ERROR,
  401 UNAUTHORIZED, 403 FORBIDDEN, 404 NOT_FOUND, 409 CONFLICT (and 500 where reachable).
- **F1_2 — flipped characterization test**: `tests/api.rs::errors::invalid_dto_field_is_rejected_as_400_validation_error`
  genuinely asserts **400 / `ErrorCode::ValidationError` / `!details.is_empty()`**; and **no test
  pins `422`** anywhere (verify any remaining `422` string is doc/comment only — a residual `422`
  assertion is a `block`).
- **F1_4 — no regression**: the other error-row tests (401/403/404/409) and the timeline limit-clamp
  test still assert correct behavior post-F1.
- **Test quality**: meaningful assertions (not just status codes — assert `ErrorCode` + body shape),
  no flakiness/ordering dependence, no over-mocking that hides the real path, clear arrange/act/assert.

A missing error-row test, a test that pins `422`, or a suite that bypasses the real app via mocks is
a `block`/`major` per impact. Thin-but-correct coverage gaps are `minor`.

## Methodology (load on demand — IDs only)
### Suggested Methodology Files
Matched rows: **"Rust testing" → Rust / Testing** and **"Code review" → Code Review**.
- `testing` — primary. Flag `Testing_Strategy_Methodology.md` (pyramid, what the 24/20 split should
  cover), `Testing_Integration_Testing_Methodology.md` (driving the real app), `Testing_Contract_Testing_Methodology.md`
  (error-row/wire-contract assertions).
- `rust` — `Rust_Testing_Methodology.md` (axum test idioms, `tower::ServiceExt::oneshot`, in-memory
  repo fixtures).
- `code-review` — `CodeReview_Checklist_Methodology.md` for severity discipline.
Load on demand. **Suggestions, not exclusive** — you are the final judge.

### Inherited Constraints
- **No DB in tests** — the whole suite MUST run against the in-memory repo; a test requiring SQLite is a defect.
- Tests drive the real app via `lib.rs`.
- Reviewer discipline (P1): read-only; do not write/edit tests; no push; never touch `main`.
- You MAY run read-only `cargo test`/`grep` against the checkout to corroborate a finding, but rely
  on the code DAG's cold gate for the PASS — do not reproduce the full build to re-derive it.

### Out-of-Scope Methodologies
- Architecture/contract mapping correctness (that is `SUBTASK_architecture_contract_review`); you
  assess whether the *tests* exercise it, not whether the mapping itself is correct.

## Output Specification
**Primary output**: `findings_test_adequacy.md` conforming to `../contracts/findings_schema.md`, with
the owned-items verdict ledger covering AC8, F1_2, F1_4.

## Success Criteria
- [ ] AC8 (real-app-via-lib.rs, no-DB, surface + behavioral-rule coverage) rendered with explicit verdict.
- [ ] Error-row coverage assessed row-by-row.
- [ ] F1_2 (flipped test asserts 400/ValidationError/!details.is_empty(); no 422 pin) and F1_4
      (no regression) answered with evidence (test names + a `grep` result for `422`).
- [ ] Every finding uses the fixed severity vocabulary and cites evidence; ledger present; file written.
