# Findings — test-adequacy (SUBTASK_test_adequacy_review)
- PR: #19 (chirp-server), head 714d50f, reviewing main...HEAD
- Lens: test-adequacy
- Acceptance criteria owned: AC8
- F1 sub-questions owned: F1_2, F1_4
- Overall lens disposition: findings-only-minor-or-nit

## Summary

The suite is **adequate and well-constructed**. 44 tests (24 in-module unit + 20 integration),
**no database anywhere**, driving the **real assembled app** through the crate's single composition
root `chirp_server::build_router(AppState::new(Arc::new(InMemoryRepository::new())))` in-process via
`tower::ServiceExt::oneshot` — not mocks that bypass the app. Every error-row the contract declares
(400/401/403/404/409) has an integration test that asserts **both** the HTTP status **and** the
decoded `ApiError.code` (wire-contract body shape), not status codes alone. The F1 remediation is
genuinely pinned at 400/`ValidationError`/non-empty `details`, and no test anywhere pins `422`. The
behavioral rules (reverse-chronological timeline, limit-clamp, cursor paging, follow/unfollow and
like/unlike idempotency, duplicate-conflict) are each covered at both the unit and integration
level. No `block` or `major`. Two low-impact coverage gaps are raised below (`minor`/`nit`).

Evidence base (read-only inspection of the `714d50f` checkout): `crates/chirp-server/tests/api.rs`
(20 `#[tokio::test]`), in-module `#[cfg(test)]` in `src/repository/in_memory.rs` (14),
`src/api/handlers.rs` (5), `src/error.rs` (5); corroborating greps for `422`, DB, `sleep`, and mocks.

## Findings

### TEST-01  — Static-file / SPA-fallback route has no integration test
- **Severity**: minor
- **AC / F1 ref**: AC8
- **Location**: `crates/chirp-server/src/api/router.rs:77` (`.fallback_service(spa)`); absent from `tests/api.rs`
- **Observation**: `build_router` mounts a `ServeDir`+`index.html` SPA fallback for every unmatched
  path (`router.rs:55-57,77`), but no integration test exercises it. The suite covers all nine
  `/api/...` routes plus `GET /healthz` (`happy_path::healthz_reports_liveness`,
  `tests/api.rs:209`), yet never asserts that an unmatched path returns the placeholder `index.html`
  (200) rather than a 404 or a routing surprise.
- **Why it matters**: test gap — the fallback is part of the mounted transport surface and governs
  SPA client-side routing behavior; its precedence against `/api/...` is asserted only in prose
  (`router.rs:16-22`), not by a test. Low impact: the static bundle is a committed placeholder and
  the real SPA is a later work-item (#9), so the untested behavior is a stub, not live app logic.
- **Recommendation**: add one integration test that GETs an unmatched non-`/api` path and asserts
  `200` with the `index.html` body (and, optionally, that an unknown `/api/...` path falls through
  to the SPA per the documented precedence) — or explicitly defer SPA-surface testing to #9. Do NOT
  make the change here (review only).

### TEST-02  — No integration test for 500 INTERNAL (unreachable via in-memory repo)
- **Severity**: nit
- **AC / F1 ref**: AC8
- **Location**: `crates/chirp-server/src/error.rs:199` (`ErrorCode::Internal => INTERNAL_SERVER_ERROR`); no integration test
- **Observation**: The contract's 500/`INTERNAL` row has no integration test. This is **correct**,
  not a defect: `ServerError::Internal` arises only from mutex-poisoning in `InMemoryRepository::lock`
  (`in_memory.rs:86`) and the `IntoResponse` masks internal detail (`error.rs:204-206`); with the
  infallible in-memory repo there is no HTTP path that reaches it. The Internal→500 mapping *is*
  unit-tested (`error.rs::each_variant_maps_to_its_error_code`, `error.rs:218-240`). Raised only so
  the gate sees the row was assessed, not silently skipped.
- **Why it matters**: completeness of the error-row ledger; no behavioral gap given the current
  backing store.
- **Recommendation**: none required for land. If a fallible (e.g. SQLite) backend is adopted later,
  add a fault-injection repo to cover 500 at that point; optionally add a one-line comment in the
  `errors` module noting 500 is intentionally not integration-reachable under the in-memory repo.

## Verdict ledger (owned items)

| AC / F1 id | Verdict | Evidence (file:line / test name / diff ref) | Finding id (if any) |
|------------|---------|----------------------------------------------|---------------------|
| AC8 (real-app-via-lib.rs) | conforms | `tests/api.rs:180-182` `build_app` = `build_router(AppState::new(Arc::new(InMemoryRepository::new())))`, imports `chirp_server::{build_router, AppState, InMemoryRepository}` (`:200`); driven via `tower::ServiceExt::oneshot` (`:33,:84`) in-process | — |
| AC8 (no DB) | conforms | grep `sqlx\|sqlite\|pool\|database` in `tests/` → only the `//! no database` doccomment (`tests/api.rs:6`); every harness uses `InMemoryRepository::new()`; no `sleep`/time vectors; no mock frameworks | — |
| AC8 (full REST surface) | conforms | 9 routes + healthz all driven: users POST `register`(`:134`)/`invalid_dto`(`:514`), sessions POST `login`(`:147`), users/{id} GET `create_user_then_fetch_profile`(`:220`), chirps POST `post_chirp`(`:166`)/`reply`(`:374`), timeline GET (`:249,:264,:295`), follow PUT+DELETE `follow_then_unfollow`(`:304`), like PUT+DELETE `like_then_unlike`(`:341`), `/healthz` `healthz_reports_liveness`(`:209`) | TEST-01 (SPA fallback gap) |
| AC8 (timeline reverse-chron) | conforms | `home_timeline_...newest_first` asserts `ids == [a2,b1,a1]` (`tests/api.rs:300`); unit `timeline_is_reverse_chronological...` (`in_memory.rs:539`); sort key is `Reverse(chirp.id.get())` monotonic id (`in_memory.rs:246`) ⇒ deterministic, not timestamp-flaky | — |
| AC8 (limit-clamp) | conforms | integration `timeline_clamps_an_oversized_limit_without_erroring` asserts 200 + all 3 items + no cursor (`tests/api.rs:604-617`); unit `timeline_paginates_with_cursor_and_clamps_the_limit` (`in_memory.rs:565`) | — |
| AC8 (cursor paging) | conforms | `timeline_paginates_newest_first_with_cursor_and_limit` walks 3 pages, asserts strict-older id sets + exact-once coverage of all 5 (`tests/api.rs:546-602`) | — |
| AC8 (follow/unfollow idempotency) | conforms | `follow_then_unfollow_moves_the_follower_count` asserts re-PUT stays at 1 then DELETE→0 (`tests/api.rs:324-337`); unit `follow_updates_counts_is_idempotent_and_forbids_self_follow` (`in_memory.rs:630`) | — |
| AC8 (like/unlike idempotency) | conforms | `like_then_unlike_moves_the_like_count` asserts re-PUT stays at 1 then DELETE→0 (`tests/api.rs:357-370`); unit `like_updates_count_is_idempotent...` (`in_memory.rs:683`) | — |
| AC8 (conflict/duplicate 409) | conforms | `duplicate_username_is_409_conflict` asserts 409 + `ErrorCode::Conflict` (`tests/api.rs:398-407`); unit `duplicate_username_is_a_conflict` (`in_memory.rs:421`) | — |
| AC8 error row 400 VALIDATION_ERROR | conforms | `invalid_dto_field_is_rejected_as_400_validation_error` asserts 400 + `ValidationError` + `!details.is_empty()` (`tests/api.rs:525-536`) | — |
| AC8 error row 401 UNAUTHORIZED | conforms | `missing_token_is_401_unauthorized` + `invalid_token_is_401_unauthorized` assert 401 + `ErrorCode::Unauthorized` (`tests/api.rs:431-445`) | — |
| AC8 error row 403 FORBIDDEN | conforms | `self_follow_is_403_forbidden` asserts 403 + `ErrorCode::Forbidden` (`tests/api.rs:447-461`) | — |
| AC8 error row 404 NOT_FOUND | conforms | 5 tests: unknown user, unknown login handle, follow absent user, like absent chirp, reply to absent chirp — each asserts 404 + `ErrorCode::NotFound` (`tests/api.rs:409-498`) | — |
| AC8 error row 409 CONFLICT | conforms | `duplicate_username_is_409_conflict` (`tests/api.rs:398`) | — |
| AC8 error row 500 INTERNAL | conforms | mapping unit-tested (`error.rs:218-240`); not integration-reachable under the infallible in-memory repo — correct absence | TEST-02 (nit) |
| AC8 (test quality: body-shape asserts, no over-mock) | conforms | every error test asserts status AND `api_error().code`; happy paths decode full DTOs (`Resp::json`, `tests/api.rs:56-69`); real app + real repo, no mock frameworks (grep clean); handler unit tests call handlers against a real `InMemoryRepository`, documented as non-mocking (`handlers.rs:206-209`) | — |
| F1_2 (flipped test asserts 400/ValidationError/!details) | conforms | `tests/api.rs:525` `assert_eq!(resp.status, BAD_REQUEST)`, `:532` `assert_eq!(error.code, ErrorCode::ValidationError)`, `:533-536` `assert!(!error.details.is_empty())`; unit corroboration `error.rs::invalid_body_maps_to_validation_code_with_a_generic_field_detail` (`error.rs:271-284`) | — |
| F1_2 (no 422 pin anywhere) | conforms | grep `422` → doc/comment/prose only: `tests/api.rs:501,511,524` (test docstring explaining the remediation), `README.md:99`, and `src/**` `//!`/`///` comments; **no** `StatusCode::UNPROCESSABLE_ENTITY` and **no** `422` assertion anywhere in the suite | — |
| F1_4 (no regression: 401/403/404/409 + limit-clamp) | conforms | the 401/403/404/409 tests above still assert correct status + `ErrorCode`; `timeline_clamps_an_oversized_limit_without_erroring` still green (`tests/api.rs:604`); code DAG cold gate = test[44] PASS, no DB (`chirp-server/SYNTHESIS.md`, per hub `_GLOBAL.md:63`) | — |

## Notes for the gate
- **No `block`/`major` from this lens.** AC8, F1_2, F1_4 all render **conforms**. Open findings are
  one `minor` (TEST-01, SPA-fallback coverage gap) and one `nit` (TEST-02, 500 non-reachable), so the
  test lens does not by itself force `REQUEST-CHANGES`.
- F1_3 (`details`-limitation acceptable-vs-blocking) is owned by `SUBTASK_architecture_contract_review`
  and is the gate's final call; from the test lens I only observe that the suite asserts
  `!details.is_empty()` (one generic `body` FieldError), consistent with that limitation — I do not
  rule on whether the single-detail shape satisfies the wire contract.
