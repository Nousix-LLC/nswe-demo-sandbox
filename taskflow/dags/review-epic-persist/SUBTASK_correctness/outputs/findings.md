# Findings — Correctness vs acceptance criteria & design (#65 / #66 / #67 / durable-persistence requirement + #64) — PR #113 @ 09fa453

Concern: does PR `Nousix-LLC/nswe-demo#113` at commit `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`
deliver the behavior that acceptance criteria **#65**, **#66**, **#67** and the design's
**durable-persistence requirement** specify — behavior, not assertion. This document consolidates four
per-area reviews (#65 invariants under concurrency; #66 seam fidelity, single-writer safety, migration;
#67 retention/capacity + fail-closed; the durable-persistence design requirement + #64 framing). Each
finding keeps its area's `COR-NN` id. Read-only review; no repository or GitHub changes were made.

Where a finding touches another review concern (seam shape, drill/test depth, CI health, operational
readiness, security, code quality), the overlap is recorded here by concern name and left for the overall
PR review to de-duplicate — it is not reconciled away or dropped.

## What I checked

**#65 — domain invariants, derived counts, and opaque monotonic ids under concurrency (proved, not asserted):**
- Issue #65's acceptance criteria traced to the change: boundary value-object validation; entity invariants
  in the durable store; opaque/server-assigned/monotonic ids stable across restart with exactly-once cursor
  paging; atomic multi-write (follow/unfollow, like/unlike, create-chirp, create-user+handle index,
  account-deletion cascade) so a reader never sees a count disagreeing with its edges under concurrency.
- Durable schema (`crates/chirp-server/migrations/0001_baseline.sql`, `0002_domain_schema.sql`): id
  `SEQUENCE`s, denormalized count columns and their `CHECK (... >= 0)`, the `follows`/`likes` composite
  PKs, `follows_no_self`, the `users_username_key` unique index, the `ON DELETE CASCADE`/`SET NULL` FKs,
  the `id DESC` timeline indexes.
- Store implementation (`crates/chirp-server/src/repository/postgres.rs`): `with_transaction`, the id
  allocators, `create_user`/`create_chirp`/`follow`/`unfollow`/`like`/`unlike`/`delete_account`/`timeline`,
  the count-bump and count-read helpers, and `classify_write_error`'s SQLSTATE mapping.
- The seam invariant contract (`crates/chirp-server/src/repository/mod.rs`) and the concurrency proof
  (`crates/chirp-server/tests/concurrency_invariants.rs`) together with the CI gate meant to run it
  (`.github/workflows/ci.yml`, `crates/chirp-server/Cargo.toml` `postgres` feature, `Dockerfile`).

**#66 — the durable store plugs into the `ChirpRepository` seam soundly:**
- Issue #66's four acceptance criteria traced: second implementor of the existing trait with the in-memory
  implementor retained and the transport unchanged; every release-bar capability expressed; single-writer /
  single consistent dataset; a defined, inspectable schema version applied by a forward-migration path.
- The full 494-line `ChirpRepository` trait and its capability set (24 `async fn`s); confirmation that every
  one of the 24 methods has a real durable body in `impl ChirpRepository for PostgresRepository`; the
  security/integrity-sensitive bodies read in full; a stub/weakening scan across the backend
  (`todo!`/`unimplemented!`/`panic!`/`TODO`/`FIXME`).
- The single-writer mechanism (backend selection, `with_transaction` commit/rollback, and the deployment
  topology under `deploy/chirp/`); the embedded `sqlx::migrate!()` runner, its invocation at connect,
  `schema_version()`, and both migration files (ordering, idempotency, fail-safety, and whether any DDL is
  applied outside the runner); that `InMemoryRepository` remains the default and routing is additive.

**#67 — retention/capacity commitments and fail-closed-on-non-durable-write:**
- No automatic expiry/eviction of user content (REQ-OPS-009): the user tables carry no `expires_at` and are
  reached by no lifetime/sweep path; both migrations are additive; the account-deletion cascade and
  `delete_user` transaction; deploy manifests for any TTL/eviction/cron on user data; the written
  no-auto-expiry commitment (`deploy/chirp/retention-capacity.md`, `repository/mod.rs` module docs).
- Enforced lifetime for transient state (REQ-OPS-010): the three transient tables and their `expires_at`
  columns + indexes; read-time enforcement in `resolve_token`/`complete_account_recovery`; the reclaim path
  `sweep_expired_transient_state()`; the scheduled sweep CronJob (`deploy/chirp/50-transient-sweep-cronjob.yaml`);
  whether the server itself invokes the sweep (it does not).
- Capacity fail-safe + fail-closed write (REQ-OPS-012): the whole durable write surface routed through
  `with_transaction`; the capacity/error classifiers and the wire mapping in `error.rs`; capacity
  provisioning and the documented growth assumption; the capacity fail-safe test and the SQLSTATE
  classification tests; the store-full / timeout / unreachable / commit-failure edge paths.

**durable-persistence design requirement + #64 framing:**
- The requirement of record (`design/domain-application-design.md` §3: REQ-DOM-012/013/014), the release-bar
  item BAR-019 and its REQ-OPS reference set (`design/release-bar.md` §E), and the operational face of that
  bar (`design/operational-readiness.md` §`durable_data`).
- What issue #64 actually claims (its criteria phrased against the *running deployment*), what PR #113 claims
  ("#64 stays open"), and the change that wires durability into the live system
  (`deploy/chirp/10-deployment.yaml`: image pin, `CHIRP_DATABASE_URL` injection, `/readyz` readiness move).
- The closes/open split against the verification methods: #65→BAR-020 (automated_test), #66→BAR-021
  (inspection), #67→BAR-022 (operational_check via drill), #64→BAR-019 (operational_check against the live
  deployment), to judge whether closing #67 while leaving #64 open is coherent.

## What I found clean

**#65:**
- Ids are opaque, server-assigned, monotonic, never-reused, and durable: they come from PostgreSQL
  `SEQUENCE`s via `nextval` on the transaction's own connection (`postgres.rs:211`, `:484`, `:2178-2219`),
  with no `DEFAULT nextval` on the columns (`0002_domain_schema.sql:18-21`), so concurrent creation yields
  distinct monotonic ids that never go backwards across a restart.
- Counts move in lockstep with edges inside one transaction: `follow`/`unfollow`/`like`/`unlike`
  (`postgres.rs:611-822`) do existence-check → idempotent `INSERT … ON CONFLICT DO NOTHING`/`DELETE` →
  single-statement count bump only when `rows_affected == 1` → read, all inside `with_transaction`; the row
  lock serializes concurrent increments; the `CHECK (... >= 0)` columns backstop underflow. The tests
  reconcile the stored count against the edge set read back through the public API, not only against the
  count column (`concurrency_invariants.rs:316-464`).
- Handle uniqueness holds under concurrency: `create_user` (`:208-249`) inserts and maps the unique-index
  violation to `Conflict` rather than SELECT-then-INSERT.
- Timeline cursor paging is exactly-once and descending (`timeline` `:539-589`); a malformed cursor fails
  safe to the first page.
- Domain-boundary validation round-trips: stored rows are lifted back through validating constructors, so a
  corrupt row surfaces as an error rather than a bad value or a panic.

**#66:**
- The full capability set is implemented behind the seam, not around it: all 24 `ChirpRepository` methods
  have durable bodies in `PostgresRepository`; none is stubbed, `todo!()`, or silently weakened, and the
  in-memory backing is retained as the default (AC1, AC2).
- Writes are confirmed-durable: `with_transaction` (`postgres.rs:2137-2166`) returns `Ok` only after the
  commit succeeds, rolls back on the closure's `Err`, and maps a failed start/commit to `Unavailable`/`Internal`.
- Session expiry is enforced at the serve path, not only by the sweep: `resolve_token` (`:396-418`) filters
  `expires_at IS NULL OR expires_at > now`, the complement of the sweep predicate.
- Recovery is fail-secure and single-use; the account-deletion cascade reconciles survivor counts before the
  cascade removes the edges, inside one transaction.
- Single-writer is satisfied and documented: the Postgres StatefulSet pins `replicas: 1` as a documented
  limitation (`40-postgres-statefulset.yaml:34-37`, ADR-0001 §2), one primary over one RWO PVC.
- The migration path is a real, versioned, forward-only runner: `sqlx::migrate!()` runs before the
  repository is served, a failure surfaces as a failed startup, migrations are ordered and idempotent, sqlx
  checksums applied versions, and `schema_version()` exposes the version. No DDL is applied outside the runner.

**#67:**
- User content has no expiry path: user tables carry no `expires_at`; the only `ON DELETE` edges are the
  account-deletion cascade and `chirps.reply_to … ON DELETE SET NULL` (which preserves a reply, it does not
  remove content); the reclaim path references only the three transient tables; the no-auto-expiry
  commitment is stated in prose as REQ-OPS-009 requires.
- Fail-closed-on-non-durable-write is correct end to end: `with_transaction` returns `Ok` only after commit;
  a failed `begin()`/`commit()` is a failed action and the value is never returned; an ambiguous commit is
  reported as failed, the safe direction; every write goes through this one path, none uses the bare pool.
- The capacity fail-safe test is not vacuous: it injects a real fault, asserts the write fails as
  `Unavailable`, and reads back to assert no row persisted; the SQLSTATE class-53 classification is
  unit-tested including negative cases.
- Transient expiry is enforced at read time independently of the sweep, so a lagging reclaim does not extend
  a lifetime; capacity is provisioned (2Gi PVC, `Retain` on scale-down/deletion) with a documented growth
  assumption and a disclosed expansion limitation.

**durable-persistence requirement + #64:**
- #64 is correctly left open and the reasoning holds: BAR-019 and its reference set verify against the
  *running* deployment; the change delivers the store, the seam wiring, and the readiness gate but cannot make
  the live deployment durable on its own (GitOps delivery of an unmerged change, and a placeholder image
  digest `@sha256:0000…0000` pending the real digest from `main`'s CI), so BAR-019's operational check cannot
  pass yet. Close #65/#66/#67, keep #64 open matches this.
- Closing #67 while keeping #64 open is coherent: BAR-022 (#67) asks that durability be *demonstrable by a
  drill*; BAR-019 (#64) asks that the *running deployment itself* be durable. A drill in a throwaway
  namespace does not make the live workload durable, so the two legitimately diverge.
- The placeholder-digest choice fails visible, not silent (ImagePullBackOff rather than serving the old
  in-memory image), and the in-memory fallback does not contradict REQ-DOM-012 because the live Deployment
  sets `CHIRP_DATABASE_URL`, selecting PostgreSQL as the release backing.

## Findings

### COR-01 — #65's "under concurrency" guarantee is asserted by tests that run in no CI gate
- **severity**: blocker
- **blocks_landing**: true
- **location**: `.github/workflows/ci.yml:86-96` (the `test` job) with
  `crates/chirp-server/tests/concurrency_invariants.rs:267-309` and `crates/chirp-server/Cargo.toml`
  (`postgres = ["dep:sqlx"]`, off by default) @ 09fa453
- **acceptance-criterion / design ref**: #65 (final criterion: invariants "covered by automated tests that
  assert them against a durable backing store under concurrent access, so the guarantee is checkable by
  someone who never met the author")
- **principle**: a guarantee is proved by a test that actually executes in the gate, not by a well-written
  test the gate never runs.
- **why it matters here**: the durable concurrency suite is doubly gated — it compiles only under
  `--features postgres`, and even then every durable test returns early via `store_or_skip!` unless
  `CHIRP_TEST_DATABASE_URL` is set (`concurrency_invariants.rs:299-309`). The CI `test` job runs
  `cargo test --workspace --locked` with no `postgres` feature, no Postgres service, and no
  `CHIRP_TEST_DATABASE_URL`, so the entire `durable` module is not compiled there; the `clippy` job compiles
  `--features postgres` but executes no tests and has no database. No assertion about counts, ids, or
  multi-write atomicity against the durable store under concurrency executes in any automated gate. The only
  concurrency test that runs is the `store_free` half against `InMemoryRepository` — the store #65 itself
  says gets consistency for free from one global lock, so it is no evidence for the durable store. A stranger
  who clones the repo and runs `cargo test` reproduces zero of #65's durable concurrency coverage, so #65 is
  asserted, not proved.
- **confidence**: verified
- **what would satisfy me**: a required CI job that provisions a throwaway PostgreSQL, sets
  `CHIRP_TEST_DATABASE_URL`, and runs `cargo test -p chirp-server --features postgres` so the `durable` suite
  executes on every PR, and that fails CI if the database is unreachable rather than skipping green.
- **overlap**: this is the same CI-gating root cause that the durability-proof concern owns as general
  test-depth and the CI doc-check concern owns as pipeline health; it is also the same mechanism COR-44 (#67)
  records for the fail-closed/sweep tests. Recorded here because it is specifically #65's
  invariant-under-concurrency proof that is absent from the gate; left for the overall PR review to
  de-duplicate against those concerns.

### COR-02 — `delete_account` reconcile-then-cascade can drift a surviving count against a concurrent edge write on the victim
- **severity**: major
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/repository/postgres.rs:1251-1329` (reconcile UPDATEs at `:1267-1308`
  run before the `DELETE FROM users` cascade at `:1315`); isolation is READ COMMITTED (`with_transaction` →
  `self.pool.begin()`, `:2142`, no `SET TRANSACTION ISOLATION`); `ensure_user_exists` is a plain
  `SELECT EXISTS` with no row lock (`:1750-1766`) @ 09fa453
- **acceptance-criterion / design ref**: #65 ("under concurrent requests … a reader never observes a count
  that disagrees with the edges"; account-deletion cascade named as a multi-write op)
- **principle**: reconciling denormalized counts from the edge set and then cascading the edges must be
  atomic with respect to a concurrent writer that adds an edge the cascade will remove.
- **why it matters here**: consider `delete_account(A)` racing `follow(C → A)` under READ COMMITTED.
  `delete_account` decrements survivors' counts by reading `follows`, then deletes `A`, cascading the follow
  edges. If the concurrent `follow(C → A)` commits after the reconcile subquery's snapshot but before the
  cascade removes the edge, then the reconcile did not see the `C → A` edge (so `C.following_count` is not
  decremented), `follow` incremented `C.following_count` by one, and the cascade then deletes the `C → A`
  edge — net, `C.following_count` is one greater than C's actual following edges, a disagreement that survives
  the operation. Nothing locks `A` before the final `DELETE` (existence is a plain `SELECT`), so nothing
  serializes the concurrent FK-referencing insert against the reconcile. The same shape applies to
  `like(C, chirpOfA)` or `follow(A → C)` racing `delete_account(A)`. No test exercises a mutation on the
  victim concurrent with its deletion — `delete_account_cascade_reconciles_counts_atomically_under_concurrency`
  (`concurrency_invariants.rs:470-544`) builds edges sequentially and only deletes concurrently with other
  deletes.
- **confidence**: suspected
- **what would satisfy me**: a test that runs `follow(C → A)` (and a like of one of A's chirps) concurrently
  with `delete_account(A)` and asserts every surviving neighbour's count equals its actual edge set
  afterward; and, if it reproduces, one of `SELECT 1 FROM users WHERE id = A FOR UPDATE` at the top of
  `delete_account`, recomputing counts from the surviving edges after the cascade, or raising this path to
  SERIALIZABLE. If confirmed, this is a direct #65 count/edge violation and would be blocker-class.

### COR-03 — lock-order deadlock aborts a valid reciprocal concurrent follow (surfaced as `Internal`)
- **severity**: major
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/repository/postgres.rs:1792-1815` (`bump_follow_counts` updates the
  follower's `following_count` first, then the followee's `follower_count`); `classify_write_error` maps
  SQLSTATE class `40` — which includes `40P01 deadlock_detected` — to `Internal`, not a retry signal
  (`:2043-2095`, `:2093`) @ 09fa453
- **acceptance-criterion / design ref**: #65 ("concurrent follow/unfollow"; the durable store must provide
  the equivalent guarantee to the in-memory store's global lock)
- **principle**: a multi-row count update must acquire its row locks in a global order, or concurrent
  operations that touch the same two rows in opposite order deadlock.
- **why it matters here**: `bump_follow_counts` always locks follower then followee, so a concurrent
  `follow(A → B)` and `follow(B → A)` lock `A` then `B` versus `B` then `A` — a lock-order inversion.
  PostgreSQL aborts one transaction with `40P01`, which becomes `ServerError::Internal`. The losing follow —
  a legitimate operation — fails spuriously under concurrency, where the in-memory reference (one global
  lock) would serialize and succeed. Counts are not corrupted (the aborted transaction rolls back cleanly),
  so this is a liveness/robustness divergence from the reference rather than an invariant break, hence major.
  It is untested and would show up in production as intermittent 5xx on mutual follows.
- **confidence**: suspected
- **what would satisfy me**: acquire the two user rows in a canonical order (e.g. by ascending id) in
  `bump_follow_counts` so no inversion is possible, plus a test that races `follow(A → B)` with
  `follow(B → A)` and asserts both succeed with correct counts. (If a deadlock-retry policy is preferred,
  `40P01` should map to a retryable/`Unavailable`-class signal rather than `Internal`.)
- **overlap**: the lock-ordering idiom touches the code-quality concern and the seam's concurrency-safety
  touches the architecture/contract-stability concern; recorded for the overall PR review to de-duplicate.

### COR-04 — "ids stable across restart" is proved only by a fresh connection pool, not an actual restart
- **severity**: minor
- **blocks_landing**: false
- **location**: `crates/chirp-server/tests/concurrency_invariants.rs:551-601`
  (`concurrently_allocated_ids_are_unique_and_stable_across_a_fresh_connection`) and `:289-295` (`connect`
  opens a new pool, the stated restart proxy) @ 09fa453
- **acceptance-criterion / design ref**: #65 ("entities created after a restart receive ids strictly greater
  than every id assigned before it … remain stable across restarts")
- **principle**: "stable across restart" and "strictly greater after restart" are claims about an actual
  process/database restart, which a second connection pool against the same running database does not
  exercise.
- **why it matters here**: the test reconnects with a fresh pool and confirms ids resolve to the same
  records — stability across a connection, not across a restart, and the test's own doc comment calls the
  pool "the across-restart proxy". The monotonic-after-restart clause (new ids strictly greater than every
  pre-restart id) is not asserted here at all. The actual restart proof lives in the durability drill, which
  the durability-proof concern owns, so this is a coverage gap for #65's restart clause discharged (if at
  all) elsewhere, not a store defect.
- **confidence**: verified
- **what would satisfy me**: the id monotonic-and-stable-across-restart clause is covered by the durability
  drill against a real restart (restart the database/pod, then create an entity and assert its id exceeds
  every pre-restart id and prior records are unchanged), and the #65 review can point to that drill step.
- **overlap**: discharged by the durability-proof concern's drill; recorded so the overall PR review confirms
  the restart clause is proved by the drill rather than left to the proxy.

### COR-20 — Seam documentation still describes the durable backend as un-implemented stubs
- **severity**: major
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/repository/postgres.rs:9-28` (module "Scaffold boundary" doc),
  `:186-188` (impl-block comment), `:1580-1582` (`store_health`: "Unlike the other scaffold methods this is
  not a stub"); `crates/chirp-server/Cargo.toml:68` ("Durable query bodies are downstream; the scaffold uses
  only the pool + migrator") @ 09fa453
- **acceptance-criterion / design ref**: #66 (BAR-021 · REQ-DOM-018)
- **principle**: documentation on the seam under review must describe what the code does; #66 is judged by
  inspection, and prose that contradicts the implementation misdirects that inspection.
- **why it matters here**: the module doc states "this is the foundation scaffold, not the durable
  implementation … every write/read below is a skeleton stub that returns `Internal`." That is false at this
  commit — all 24 methods have real durable bodies with integration tests asserting durable round-trips,
  cascades, and concurrency. A reader auditing "is the capability set actually implemented?" for #66 would
  read the module doc and conclude it is not. This is one stale-prose pattern recurring in four places (module
  doc, impl comment, `store_health` aside, `Cargo.toml`), left over from an earlier scaffold stage. It does
  not change behavior, which is why it does not block #66's behavioral bar.
- **confidence**: verified
- **what would satisfy me**: replace the scaffold-era prose at the four locations so the seam docs describe
  the implemented durable behavior, and confirm `cargo doc` builds clean afterward.
- **overlap**: this stale rustdoc (and any intra-doc links it carries to the private `mapping` items) is a
  plausible cause of the failing required `doc` check; that gate is owned by the CI doc-check concern.
  Recorded here as the content defect on the #66 seam and flagged for the overall PR review to connect to the
  CI finding — not claimed as a correctness-area blocker.

### COR-21 — `remove_chirp` advertises a `Forbidden` result the store never returns
- **severity**: minor
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/repository/mod.rs:441-445` (trait doc: `Forbidden` if `actor` is not
  permitted) vs `crates/chirp-server/src/repository/postgres.rs:1473` and
  `crates/chirp-server/src/repository/in_memory.rs:884` (both take `_actor`, unused) @ 09fa453
- **acceptance-criterion / design ref**: #66 (REQ-DOM-020)
- **principle**: the seam's documented error contract should match what every implementor can produce; an
  advertised failure no backing returns is a contract the seam cannot keep.
- **why it matters here**: both implementors ignore `actor` and remove unconditionally, so the trait's
  documented `Forbidden` path is dead at the store. This is consistent across backings and matches the stated
  design (author-vs-moderator authorization deferred upstream to `REQ-ID-*`), so it is not a dropped or
  weakened capability — the removal works and is idempotent. But the seam doc promises an authorization result
  the store cannot give, unlike `set_account_suspension`, which enforces the one model-level `Forbidden` it
  owns (self-target).
- **confidence**: verified
- **what would satisfy me**: either note in the `remove_chirp` trait doc that authorization (and any
  `Forbidden`) is entirely an upstream concern with no store-level check, or add the store-level guard if the
  model expects one — matching whichever decision `set_account_suspension` follows.

### COR-22 — Single-writer guarantee rests on a replica count with no hard guard
- **severity**: minor
- **blocks_landing**: false
- **location**: `deploy/chirp/40-postgres-statefulset.yaml:34-37`, `:149-168` (RWO PVC; ReadWriteOncePod
  noted as future hardening) @ 09fa453
- **acceptance-criterion / design ref**: #66 (BAR-021 · REQ-OPS-005)
- **principle**: a single-writer guarantee enforced only by a configuration value is only as strong as the
  change control around that value.
- **why it matters here**: the no-fork guarantee is `replicas: 1` on the StatefulSet. Scaling it above 1
  would not create a replication cluster — each ordinal gets its own PVC and its own independent Postgres with
  its own dataset, exactly the data fork #66 exists to prevent. The manifest documents the limitation and
  names `ReadWriteOncePod` as the stricter future posture, which is what #66's documented-single-replica
  branch permits, so this is not a blocker — but the guarantee is a convention, not an enforced invariant,
  and a future scale-up would silently break it.
- **confidence**: verified
- **what would satisfy me**: the documented-limitation posture already clears #66; as additive hardening, a
  `ReadWriteOncePod` access mode (on a CSI-backed class) or an admission/policy guard that prevents the
  Postgres StatefulSet from scaling past one would make the constraint enforced rather than conventional.
- **overlap**: provisioning topology is also in scope for the operational-readiness and
  architecture/contract-stability concerns; left for the overall PR review to de-duplicate.

### COR-23 — Credential at rest is stored and compared in plaintext
- **severity**: minor
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/repository/postgres.rs:928` (`stored == secret` equality compare);
  credential persisted verbatim via the `set_credential`/`complete_account_recovery` upsert
  (`postgres.rs:842-905`, `:1061+`); schema `credentials.secret TEXT` (`migrations/0002_domain_schema.sql:73-77`)
  @ 09fa453
- **acceptance-criterion / design ref**: #66 (REQ-DOM-005; and REQ-ID-* downstream)
- **principle**: the `credential_set_verify` capability is sound only if the at-rest representation and the
  verification are not themselves a weakness.
- **why it matters here**: the capability round-trips correctly (set then verify authenticates; the error is
  indistinguishable across unknown-handle / no-credential / mismatch), so for #66's "capability present and
  not weakened" bar it passes. But the stored `secret` is the plaintext value and the check is a
  non-constant-time `==`. The code defers the credential crypto scheme to EPIC-IDENTITY (`REQ-ID-*`), so this
  is a documented deferral rather than an oversight; recorded because it is visible in the seam implementation
  and bears on whether the capability is soundly realized.
- **confidence**: verified
- **what would satisfy me**: hashing at rest (a password-hashing KDF) and a constant-time verify when the
  EPIC-IDENTITY credential work lands.
- **overlap**: credential handling and the at-rest representation are the security concern's bar; recorded
  here as it touches #66's capability soundness and left for the overall PR review to de-duplicate.

### COR-40 — Deployed reclaim path (CronJob SQL) is a hand-copy of the tested Rust sweep; the two can drift
- **severity**: major
- **blocks_landing**: false
- **location**: `deploy/chirp/50-transient-sweep-cronjob.yaml:112-120` (the three inline DELETEs) vs
  `crates/chirp-server/src/repository/postgres.rs:1618-1659` (`sweep_expired_transient_state`) @ 09fa453
- **acceptance-criterion / design ref**: #67 (REQ-OPS-010)
- **principle**: one behavior should have one authority; a reclaim rule copied into two places verified
  separately will diverge.
- **why it matters here**: in the deployed system the sweep is run only by the CronJob's raw `psql` DELETEs.
  The server never calls `sweep_expired_transient_state()` (confirmed across `main.rs`/`lib.rs`/router), so
  the Rust method — and every sweep test that exercises it — covers a path that does not run in production,
  while the SQL that does run has no test. The two predicate sets match today (compared statement by
  statement), so this is not a correctness defect now; but a future change to a transient table or a Rust
  predicate would leave the CronJob silently running the old SQL with no test to catch it. Expiry is also
  honoured at read time, so a fully drifted CronJob would only lag storage reclamation — which is why this is
  major, not a blocker.
- **confidence**: verified
- **what would satisfy me**: make the CronJob invoke the server's own sweep (a `chirp-server sweep`
  subcommand, or an admin endpoint the Job calls) so there is one authority; or add a test that runs the
  CronJob's exact SQL against the real schema and asserts it reclaims the same rows the Rust sweep does.

### COR-41 — `sessions.expires_at` is nullable, so the session lifetime is enforced by convention, not by the schema
- **severity**: minor
- **blocks_landing**: false
- **location**: `crates/chirp-server/migrations/0002_domain_schema.sql:84-88` (`expires_at BIGINT`, no
  `NOT NULL`); serve condition `postgres.rs:402`; sweep guard `postgres.rs:1623` @ 09fa453
- **acceptance-criterion / design ref**: #67 (REQ-OPS-010)
- **principle**: an "enforced" lifetime should be enforced by the store, not only by the code that happens to
  write it.
- **why it matters here**: `recovery_tokens` and `export_artifacts` make `expires_at NOT NULL`; `sessions`
  alone permits NULL. A session row with NULL `expires_at` resolves forever (serve condition
  `expires_at IS NULL OR expires_at > now`) and is never reclaimed (the sweep guards `expires_at IS NOT
  NULL`) — an unbounded, never-swept session. The insert path always stamps `Some(expires_at)`, so no
  NULL-expiry session is issued by this code and the lifetime holds in practice; but the stated rationale
  (tolerate a legacy row) is weak for a table this migration creates fresh, so the nullability buys nothing
  here while leaving REQ-OPS-010's "enforced" property dependent on application code rather than the schema.
- **confidence**: verified
- **what would satisfy me**: make `sessions.expires_at NOT NULL` (matching the other two transient tables),
  or, if a nullable column must stay, state and test the invariant that the application never writes a NULL
  expiry and that read + sweep treat any NULL as already-expired.
- **overlap**: the schema shape touches #66 and the architecture/contract-stability concern; recorded here as
  the retention-enforcement angle.

### COR-42 — Capacity-exhaustion classification is not applied to statement-level errors inside capability methods
- **severity**: nit
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/repository/postgres.rs:242` (and sibling capability methods, which
  hand-map statement errors to `ServerError::Internal`) vs the capacity classifier used only at
  `begin()`/`commit()` (`:2142-2153`) and in the sweep @ 09fa453
- **acceptance-criterion / design ref**: #67 (REQ-OPS-012)
- **principle**: a classification the docs present as uniform should be applied uniformly.
- **why it matters here**: `retention-capacity.md` and the `classify_write_error` doc describe capacity
  exhaustion surfacing as `ServerError::Unavailable`. That holds at `begin()`/`commit()` and in the sweep, but
  a capacity error raised at an INSERT/UPDATE statement inside a capability method is hand-mapped to
  `ServerError::Internal`, bypassing `classify_write_error`. This has no user-facing or fail-closed impact —
  both map to HTTP 500 and both are failed actions, so the write is never falsely confirmed — so it does not
  affect #67 correctness; it is a log/metric categorization inconsistency only.
- **confidence**: verified
- **what would satisfy me**: route capability-method statement errors through `classify_write_error` too, or
  narrow the doc's claim to say capacity classification is applied at transaction begin/commit and in the
  sweep.
- **overlap**: the code-quality concern.

### COR-43 — Capacity exhaustion returns HTTP 500 rather than 503, so clients cannot distinguish it from a bug
- **severity**: nit
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/error.rs:32-36,232-234` (`Unavailable` → `ErrorCode::Internal` →
  500) @ 09fa453
- **acceptance-criterion / design ref**: #67 (REQ-OPS-012)
- **principle**: a failure a client could reasonably retry is worth distinguishing from one it cannot.
- **why it matters here**: REQ-OPS-012 requires a non-durable write be reported to the user as failed, which
  HTTP 500 satisfies — so this is not a #67 gap. But collapsing capacity pressure (retryable, transient) into
  the same `INTERNAL`/500 cell as an actual server bug means a caller cannot tell "try again shortly" from
  "this is broken." The PR documents this as a deliberate choice to keep the frozen error-code↔status contract.
- **confidence**: verified
- **what would satisfy me**: either accept the documented 500 choice, or map `Unavailable` to 503 with a retry
  signal if the contract permits an additive status.
- **overlap**: the wire-contract shape is owned by the architecture/contract-stability concern; recorded here
  only as it bears on the fail-closed user experience.

### COR-44 — Fail-closed / sweep tests skip when no test database is configured (proof-depth overlap)
- **severity**: minor
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/repository/postgres.rs:2851-2854` (and the sweep tests, which
  early-return on absent `CHIRP_TEST_DATABASE_URL`) @ 09fa453
- **acceptance-criterion / design ref**: #67 (REQ-OPS-010/012)
- **principle**: a test that silently skips proves nothing about the run it skipped in.
- **why it matters here**: the capacity fail-safe and sweep tests are well-written and non-vacuous when they
  run, but they return early (printing "skipping") when `CHIRP_TEST_DATABASE_URL` is unset. From the
  correctness lens the behavior is implemented correctly (verified by reading the code); whether CI actually
  provisions the Postgres test database and executes these rather than skipping them green is the proof-depth
  question. This is the same CI-gating mechanism COR-01 identifies for #65's concurrency suite, applied to
  #67's fail-closed/sweep tests.
- **confidence**: suspected
- **what would satisfy me**: the durability-proof concern confirms the capacity/sweep tests execute against a
  real Postgres in PR #113's CI (not skipped); otherwise the gating is made to fail loudly rather than skip.
- **overlap**: proof-depth is owned by the durability-proof concern; recorded here, not adjudicated. If those
  tests are found to skip in CI, the "proved, not asserted" bar for the fail-closed and reclaim behavior would
  not be met and the severity of that gap is the durability-proof concern's to set — the same way COR-01
  settles #65's.

### COR-60 — PR's "what remains / one follow-up" understates what activates durability in the running system
- **severity**: minor
- **blocks_landing**: false
- **location**: whole-PR — PR #113 description, "What remains" section; corroborated by
  `deploy/chirp/10-deployment.yaml:61,66-78` @ 09fa453
- **acceptance-criterion / design ref**: #64 / BAR-019 / durable-persistence requirement
- **principle**: a shipped account of "what is left" should name every precondition a reader must satisfy to
  reach the claimed end state, not just the most visible one.
- **why it matters here**: the description frames the digest-pin as "the one follow-up needed to activate the
  durable image on the cluster." Activating durability actually depends on a short sequence: (a) the change
  merges so delivery reconciles it onto `main`; (b) the out-of-band `chirp-db-credentials` Secret exists in
  the namespace, or the pod wedges in `CreateContainerConfigError` (the Deployment's `secretKeyRef` requires
  it — `10-deployment.yaml:72-78`); (c) the real durable digest is pinned, replacing the placeholder; and
  between merge and the digest-pin the app tier is intentionally not-ready (ImagePullBackOff on the
  placeholder), a brief outage window. A reader who takes "one follow-up" literally can be surprised by the
  Secret precondition and the not-ready window. This strengthens rather than weakens "#64 stays open" — it
  does not dispute the framing.
- **confidence**: verified — the Secret dependency and the placeholder digest are both in the diff at the
  cited lines; whether the Secret is already present in the namespace is live operational state not inspected
  and not claimed here.
- **what would satisfy me**: reword "What remains" to state the activation sequence rather than a single step
  — merge (delivery reconcile) → ensure the out-of-band `chirp-db-credentials` Secret is present → pin the
  real durable digest published by `main`'s CI — and note that the app tier is deliberately not-ready between
  merge and the digest-pin. No code change required.
- **overlap**: the digest-pin, readiness gating, placeholder-digest outage window, and Secret handling are
  owned by the operational-readiness concern (activation/readiness) and the architecture/contract-stability
  concern (manifest shape); COR-60 touches the same facts from the #64-framing angle, left for the overall PR
  review to de-duplicate.

## #64 status

#64 is **noted and confirmed correctly open** — not closed by this review, not filed as backlog. BAR-019 is
verified against the running deployment, which this unmerged change cannot make durable on its own; the PR's
"#64 stays open" framing is accurate (see COR-60 for the one accuracy refinement to the PR's "what remains"
prose).

## Concern sub-verdict

- **HAS-BLOCKERS**
- One area (#65) carries a `blocks_landing: true` finding, so the correctness concern is HAS-BLOCKERS. COR-01:
  #65's central guarantee — domain invariants, derived counts, and opaque monotonic ids hold under
  concurrency, proved not asserted — is not proved, because the durable-store concurrency tests execute in no
  automated gate. The store implementation is otherwise well-built for correctness across all four areas:
  #65's id mechanism, in-transaction count maintenance, idempotent edge ops, and exactly-once paging are
  sound; #66's full capability set is implemented behind the seam as a real second implementor with a
  versioned forward-migration runner and a documented single-writer posture; #67's user content has no expiry
  path, transient lifetimes are enforced at read time, and non-durable writes fail closed; and the
  durable-persistence requirement is traced with #64 correctly left open. The remaining findings are two
  suspected #65 concurrency hazards (COR-02 count drift on delete-vs-concurrent-write, COR-03 reciprocal-follow
  deadlock), documentation-accuracy and hardening issues on the seam and retention paths (COR-04, COR-20..23,
  COR-40..44, COR-60), and overlaps onto the durability-proof, CI doc-check, architecture/contract-stability,
  operational-readiness, security, and code-quality concerns that the overall PR review de-duplicates. The
  single blocker is specifically the missing proof of #65 under concurrency; it is left connected to — not
  merged into — the durability-proof and CI concerns that share its root cause.
