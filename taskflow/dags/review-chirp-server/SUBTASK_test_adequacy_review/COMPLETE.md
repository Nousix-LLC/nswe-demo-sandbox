# COMPLETE — SUBTASK_test_adequacy_review

**Task**: Test-adequacy review of chirp-server (PR #19, head 714d50f). One lens: test adequacy.
**Status**: completed (Atomic).

## What was done
Reviewed the chirp-server test suite read-only against the `714d50f` checkout and emitted the
single declared output `findings_test_adequacy.md`, conforming to `../contracts/findings_schema.md`
(file header, finding records, per-AC/F1 verdict ledger, fixed severity vocabulary). Owned items
AC8, F1_2, F1_4 each rendered with an explicit verdict and cited evidence. No source edited, no
push, no `gh pr review`, `main` untouched (reviewer discipline P1 observed).

## Verdicts (owned items)
- **AC8 — conforms.** 44 tests (24 unit + 20 integration), no DB, driving the real app via
  `chirp_server::build_router`/`AppState`/`InMemoryRepository` (lib.rs re-exports) with
  `tower::oneshot` in-process — not mocks. Full 9-route REST surface + `/healthz` covered; all
  behavioral rules covered (reverse-chron ordering, limit-clamp, cursor paging, follow/unfollow and
  like/unlike idempotency, 409 conflict). Error rows 400/401/403/404/409 each integration-tested
  asserting status AND decoded `ApiError.code`; 500 not reachable under the in-memory repo (mapping
  unit-tested) — correct.
- **F1_2 — conforms.** Flipped test asserts 400 / `ErrorCode::ValidationError` / `!details.is_empty()`
  (`tests/api.rs:525-536`); no test pins `422` anywhere — every `422` string is doc/comment/README
  prose, and there is no `UNPROCESSABLE_ENTITY` or `422` assertion.
- **F1_4 — conforms.** 401/403/404/409 tests and the timeline limit-clamp test still assert correct
  behavior post-F1.

## Findings raised
- `TEST-01` (minor) — SPA/static-fallback route not exercised by any integration test.
- `TEST-02` (nit) — no 500 integration test (correct: unreachable under the infallible in-memory repo).

No `block`, no `major`. This lens does not force REQUEST-CHANGES on its own.

## Evidence method
Read `tests/api.rs`, `src/lib.rs`, `src/api/{json,handlers,router}.rs`, `src/error.rs`,
`src/repository/in_memory.rs`; corroborating read-only greps for `422`, DB (`sqlx`/`sqlite`/`pool`),
`sleep`/time vectors, and mock frameworks. Resolved a potential ordering-flakiness concern: the
timeline sorts by `Reverse(chirp.id.get())` (monotonic id), not timestamp, so id-based ordering
assertions are deterministic.

## Output
- `findings_test_adequacy.md` (consumed by `SUBTASK_synthesis_verdict`).
