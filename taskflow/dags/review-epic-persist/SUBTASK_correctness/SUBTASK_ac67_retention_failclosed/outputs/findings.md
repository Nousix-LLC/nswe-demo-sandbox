# Findings — #67 retention/capacity + fail-closed-on-non-durable-write — PR #113 @ 09fa453

## What I checked

Acceptance criterion #67 (REQ-OPS-009 no-auto-expiry, REQ-OPS-010 enforced transient lifetimes,
REQ-OPS-012 capacity fail-safe + fail-closed write) traced for behavioral correctness against the
change at `09fa453`. Specifically:

- **No automatic expiry / eviction of user content (REQ-OPS-009).** The domain schema
  (`crates/chirp-server/migrations/0002_domain_schema.sql`) for `users`, `credentials`, `chirps`,
  `follows`, `likes` — confirmed none carries an `expires_at` and none is reached by any
  lifetime/expiry/sweep path. Both migrations (`0001_baseline.sql`, `0002_domain_schema.sql`) read
  for destructive statements (DROP / TRUNCATE / user-content DELETE / `ALTER … DROP`) — none present;
  both are additive `CREATE TABLE/INDEX IF NOT EXISTS`. Account-deletion cascade
  (`users … ON DELETE CASCADE` on credentials, sessions, recovery_tokens, export_artifacts, chirps,
  follows, likes) and the `delete_user` transaction (`postgres.rs` L1252–L1317). Deploy manifests
  (`40-postgres-statefulset.yaml`, `10-deployment.yaml`) for any TTL / eviction / pg_cron on user
  data — none. The written statement that no auto-expiry occurs (`deploy/chirp/retention-capacity.md`,
  `repository/mod.rs` module docs).
- **Enforced lifetime for transient state (REQ-OPS-010).** The three transient tables (`sessions`,
  `recovery_tokens`, `export_artifacts`) and their `expires_at` columns + expiry indexes (migration
  0002 L84–L147); read-time enforcement in `resolve_token` and `complete_account_recovery`
  (`postgres.rs` L398–L409, serve condition `expires_at IS NULL OR expires_at > now`); the reclaim
  path `sweep_expired_transient_state()` (`postgres.rs` L1618–L1659); the scheduled CronJob
  (`deploy/chirp/50-transient-sweep-cronjob.yaml`); whether the server itself invokes the sweep
  (it does not — checked `main.rs`, `lib.rs`, `api/mod.rs`, `api/router.rs`).
- **Capacity fail-safe + fail-closed write (REQ-OPS-012).** The whole durable write surface routed
  through `with_transaction` (`postgres.rs` L2137–L2166) — every INSERT/UPDATE/DELETE confirmed to run
  inside it, with the sole bare-pool statement being the `SELECT 1` health read (L1588); the error
  classifiers `is_capacity_exhaustion_sqlstate`, `is_capacity_exhaustion`, `classify_write_error`
  (L2056–L2100); the wire mapping in `error.rs` (both `Internal` and `Unavailable` → `ErrorCode::Internal`
  → HTTP 500); capacity provisioning (2Gi per-replica PVC, `whenDeleted/whenScaled: Retain`) and the
  documented growth assumption (`retention-capacity.md`); the capacity fail-safe test
  (`postgres.rs` L2844–L2910) and the SQLSTATE classification tests (L2686–L2708).
- The failure/edge paths #67 calls out: store full (SQLSTATE 53100), write timeout / pool-acquire
  timeout (`PoolTimedOut`), backend unreachable (`begin()` failure), and commit failure.

## What I found clean

- **User content has no expiry path.** The user tables carry no `expires_at`; the only `ON DELETE`
  edges are account-deletion CASCADE and `chirps.reply_to … ON DELETE SET NULL` (which preserves a
  reply when its parent is removed — it does not remove user content). The reclaim path references
  only the three transient tables, so no reclaim/TTL/migration path can remove user content. The
  repository states the no-auto-expiry commitment in prose, which REQ-OPS-009 explicitly requires.
- **Fail-closed-on-non-durable-write is correctly implemented end to end.** `with_transaction` returns
  `Ok(value)` only after `commit()` succeeds; a failed `begin()` or `commit()` is mapped to a failed
  action and the value is never returned; a closure `Err` triggers rollback and propagates. Both
  `Internal` and `Unavailable` surface as HTTP 500, so a write that is not durably committed is
  reported as failed, never as a 2xx false confirmation. A commit whose outcome is ambiguous is
  reported as failed (not confirmed), which is the safe direction. Every write goes through this one
  path; no write uses the bare pool.
- **The capacity fail-safe test is not vacuous.** `an_exhausted_connection_pool_fails_safe_as_unavailable`
  injects a real fault (capacity-of-one pool, connection held), asserts the write fails as
  `Unavailable`, then reads back to assert no row persisted — it checks both the failed-action
  classification and the absence of a durable write. The SQLSTATE class-53 classification is
  unit-tested directly, including negative cases (`40053`, `25301` not matched).
- **Transient expiry is enforced at read time independently of the sweep.** An expired session
  resolves as absent and an expired recovery token is rejected whether or not the sweep has run, so
  the lifetime is honoured even if reclamation lags. `recovery_tokens.expires_at` and
  `export_artifacts.expires_at` are `NOT NULL`. No export artifacts are produced this release
  (`get`/export path does not persist to `export_artifacts`, L1341), so REQ-OPS-010's export clause is
  satisfied vacuously with the enforcement mechanism already in place.
- **Capacity is provisioned and documented.** 2Gi PVC with `Retain` on scale-down and deletion, a
  stated growth assumption, and a disclosed expansion limitation (local-path has no online
  expansion). REQ-OPS-012's "provisioned capacity and expected-growth assumption are documented" is met.

## Findings

### COR-40 — Deployed reclaim path (CronJob SQL) is a hand-copy of the tested Rust sweep; the two can drift
- **severity**: major
- **blocks_landing**: false
- **location**: `deploy/chirp/50-transient-sweep-cronjob.yaml:112-120` (the three inline DELETEs) vs
  `crates/chirp-server/src/repository/postgres.rs:1618-1659` (`sweep_expired_transient_state`) @ 09fa453
- **acceptance-criterion / design ref**: #67 (REQ-OPS-010)
- **principle**: One behavior should have one authority; a reclaim rule copied into two places that are
  verified separately will diverge.
- **why it matters here**: In the deployed system the sweep is run *only* by the CronJob's raw
  `psql` DELETEs. The server never calls `sweep_expired_transient_state()` (confirmed across
  `main.rs`/`lib.rs`/router), so the Rust method — and every sweep test that exercises it — covers a
  path that does not run in production, while the SQL that does run in production has no test. The two
  predicate sets match today (I compared them statement by statement: `sessions … expires_at IS NOT NULL
  AND expires_at <= now`, `recovery_tokens … expires_at <= now`, `export_artifacts … expires_at <= now`),
  so this is not a correctness defect today. But if a future change adds a transient table or alters a
  predicate in the Rust sweep, the CronJob will silently keep running the old SQL, and no test would
  catch it. Expiry is also honoured at read time, so even a fully drifted CronJob would only lag
  storage reclamation of the new table — which is why this is major, not a blocker.
- **confidence**: verified
- **what would satisfy me**: make the CronJob invoke the server's own sweep (a `chirp-server sweep`
  subcommand, or an admin endpoint the Job calls) so there is one authority; OR add a test that runs
  the CronJob's exact SQL against the real schema and asserts it reclaims the same rows the Rust sweep
  does, so the copy is pinned to the original.

### COR-41 — `sessions.expires_at` is nullable, so the session lifetime is enforced by convention, not by the schema
- **severity**: minor
- **blocks_landing**: false
- **location**: `crates/chirp-server/migrations/0002_domain_schema.sql:84-88` (`expires_at BIGINT`, no
  `NOT NULL`); serve condition `postgres.rs:402`; sweep guard `postgres.rs:1623` @ 09fa453
- **acceptance-criterion / design ref**: #67 (REQ-OPS-010)
- **principle**: An "enforced" lifetime should be enforced by the store, not only by the code that
  happens to write it.
- **why it matters here**: `recovery_tokens` and `export_artifacts` make `expires_at NOT NULL`;
  `sessions` alone permits NULL. A session row with NULL `expires_at` resolves forever (serve condition
  `expires_at IS NULL OR expires_at > now`) and is never reclaimed (the sweep guards `expires_at IS NOT
  NULL`), i.e. an unbounded, never-swept session. The insert path always stamps `Some(expires_at)`, so
  no NULL-expiry session is issued by this code — the lifetime holds in practice. But the stated
  rationale (tolerate a legacy row) is weak for a table this migration creates fresh: there are no
  legacy session rows for a brand-new table, so the nullability buys nothing here while leaving the
  REQ-OPS-010 "enforced" property dependent on application code rather than the schema. The session
  lifetime *value* and its security are owned by identity & trust; the *schema shape* overlaps #66 /
  the root `SUBTASK_architecture_contract` — recorded here as the retention-enforcement angle.
- **confidence**: verified
- **what would satisfy me**: make `sessions.expires_at NOT NULL` (matching the other two transient
  tables), or, if a nullable column must stay, state and test the invariant that the application never
  writes a NULL expiry and that read + sweep treat any NULL as already-expired.

### COR-42 — Capacity-exhaustion classification is not applied to statement-level errors inside capability methods
- **severity**: nit
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/repository/postgres.rs:242` (and the sibling capability
  methods, which hand-map statement errors to `ServerError::Internal`) vs the capacity classifier used
  only at `begin()`/`commit()` (L2142-L2153) and in the sweep @ 09fa453
- **acceptance-criterion / design ref**: #67 (REQ-OPS-012)
- **principle**: A classification the docs present as uniform should be applied uniformly.
- **why it matters here**: `retention-capacity.md` and the `classify_write_error` doc describe capacity
  exhaustion surfacing as `ServerError::Unavailable`. That holds for failures at `begin()`/`commit()`
  and for the sweep, but a capacity error raised at an INSERT/UPDATE statement *inside* a capability
  method is hand-mapped to `ServerError::Internal`, bypassing `classify_write_error`. This has **no**
  user-facing or fail-closed impact — both map to HTTP 500 and both are failed actions, so the write is
  never falsely confirmed either way — so it does not affect #67 correctness. It is a log/metric
  categorization inconsistency only (a disk-full at statement time is recorded as `Internal`, not
  `Unavailable`). Overlaps `SUBTASK_code_quality`.
- **confidence**: verified
- **what would satisfy me**: route capability-method statement errors through `classify_write_error`
  too (so capacity exhaustion is categorized consistently wherever it surfaces), or narrow the doc's
  claim to say capacity classification is applied at transaction begin/commit and in the sweep.

### COR-43 — Capacity exhaustion returns HTTP 500 rather than 503, so clients cannot distinguish it from a bug
- **severity**: nit
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/error.rs:32-36,232-234` (`Unavailable` → `ErrorCode::Internal`
  → 500) @ 09fa453
- **acceptance-criterion / design ref**: #67 (REQ-OPS-012)
- **principle**: A failure a client could reasonably retry is worth distinguishing from one it cannot.
- **why it matters here**: REQ-OPS-012 requires a non-durable write be "reported to the user as failed,"
  which HTTP 500 satisfies — so this is not a #67 gap. But collapsing capacity pressure (retryable,
  transient) into the same `INTERNAL`/500 cell as a genuine server bug means a caller cannot tell
  "try again shortly" from "this is broken." The PR documents this as a deliberate choice to keep the
  frozen error-code↔status contract. The wire-contract shape is owned by `SUBTASK_architecture_contract`;
  recorded here only as it bears on the fail-closed user experience.
- **confidence**: verified
- **what would satisfy me**: left to `SUBTASK_architecture_contract` — either accept the documented
  500 choice, or map `Unavailable` to 503 with a retry signal if the contract permits an additive
  status.

### COR-44 — Fail-closed / sweep tests skip when no test database is configured (proof-depth overlap)
- **severity**: minor
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/repository/postgres.rs:2851-2854` (and the sweep tests, which
  early-return on absent `CHIRP_TEST_DATABASE_URL`) @ 09fa453
- **acceptance-criterion / design ref**: #67 (REQ-OPS-010/012)
- **principle**: A test that silently skips proves nothing about the run it skipped in.
- **why it matters here**: The capacity fail-safe and sweep tests are well-written and non-vacuous
  *when they run*, but they return early (printing "skipping") when `CHIRP_TEST_DATABASE_URL` is unset.
  From the correctness lens the behavior is implemented correctly (verified by reading the code);
  whether CI actually provisions the Postgres test database and executes these — rather than skipping
  them green — is the proof-depth question and is **owned by the root `SUBTASK_durability_proof`**. I am
  recording the overlap, not adjudicating it: if durability-proof finds these tests skip in the PR's
  CI, the "proved, not asserted" bar for the fail-closed and reclaim behavior would not be met and the
  severity of *that* gap is theirs to set.
- **confidence**: suspected
- **what would satisfy me**: `SUBTASK_durability_proof` confirms the capacity/sweep tests execute
  against a real Postgres in PR #113's CI (not skipped); otherwise the gating is made to fail loudly
  rather than skip.

## Concern sub-verdict
- **NON-BLOCKING-ONLY**
- The behavior #67 requires in this area is delivered correctly: user content has no expiry path and
  the commitment is documented, transient lifetimes are enforced at read time with a scheduled reclaim,
  and non-durable writes fail closed (reported as failed, never falsely confirmed) across the whole
  write surface. The findings are a real reclaim-path drift risk (COR-40, major), a schema-enforcement
  hardening gap (COR-41, minor), two categorization/wire nits (COR-42, COR-43), and a proof-depth
  overlap left to `SUBTASK_durability_proof` (COR-44). None makes #67 fail as implemented, so none
  blocks landing from this area.
