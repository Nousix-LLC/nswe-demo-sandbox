# Findings — Correctness / #65 invariants, derived counts, opaque-id monotonicity under concurrency — PR #113 @ 09fa453

Area: acceptance criterion **#65** only (domain invariants, denormalized counts, opaque monotonic
ids in the durable store **under concurrency** — proved, not merely asserted). The sibling concerns
(#66 seam/single-writer, #67 retention/fail-closed, the design requirement + #64) and the root-level
`SUBTASK_architecture_contract` (seam shape) and `SUBTASK_durability_proof` (drill / general test
depth) are out of scope here; where my reading touches them I record the overlap and leave it for
synthesis.

## What I checked

- **Issue #65** acceptance criteria (via `gh issue view 65`), traced to the change: validated value
  objects at the boundary; entity invariants in the durable store; opaque/server-assigned/monotonic
  ids stable across restart with exactly-once cursor paging; atomic multi-write (follow/unfollow,
  like/unlike, create-chirp, create-user+handle index, account-deletion cascade) so a reader never
  sees a count disagreeing with its edges under concurrency; a concurrency-safe seam.
- **Durable schema** — `crates/chirp-server/migrations/0001_baseline.sql`,
  `crates/chirp-server/migrations/0002_domain_schema.sql`: the id `SEQUENCE`s (`user_id_seq`,
  `chirp_id_seq`, `token_seq`); the denormalized count columns and their `CHECK (... >= 0)`; the
  `follows`/`likes` composite primary keys (idempotent follow/like); `follows_no_self`; the
  `users_username_key` unique handle index; the `ON DELETE CASCADE` / `ON DELETE SET NULL` foreign
  keys; the `id DESC` timeline/listing indexes.
- **Store implementation** — `crates/chirp-server/src/repository/postgres.rs`: `with_transaction`
  (isolation level, confirmed-write-on-commit), the id allocators (`allocate_user_id` /
  `allocate_chirp_id` / `allocate_token_value` → `next_sequence_value` → `nextval`), `create_user`,
  `create_chirp`, `follow`, `unfollow`, `like`, `unlike`, `delete_account`, `timeline`, the
  `ensure_user_exists` / `ensure_chirp_exists` / `bump_follow_counts` / `bump_like_count` /
  `read_follower_count` / `read_like_count` helpers, and `classify_write_error`'s SQLSTATE mapping.
- **Seam** — `crates/chirp-server/src/repository/mod.rs`: the `ChirpRepository` invariant contract
  the durable store must uphold (counts track edges, no self-follow, ≤1 like per pair,
  reverse-chronological timelines).
- **The concurrency proof** — `crates/chirp-server/tests/concurrency_invariants.rs` (both halves and
  the two gates), and the CI gate that is meant to run it — `.github/workflows/ci.yml`,
  `crates/chirp-server/Cargo.toml` (`postgres` feature), `Dockerfile`.

## What I found clean

- **Id mechanism (opaque, server-assigned, monotonic, never-reused, stable).** Ids come from
  PostgreSQL `SEQUENCE`s via `nextval`, allocated on the transaction's own connection
  (`postgres.rs:211`, `:484`, `allocate_*` at `:2178-2219`). `nextval` is atomic and never hands the
  same value to two callers, so concurrent creation yields distinct, monotonic ids; sequence state
  is durable, so values never go backwards across a restart and are never reused (a rolled-back
  allocation leaves a gap, which #65 permits). The columns carry no `DEFAULT nextval` — allocation
  is deliberately the store's job (`0002_domain_schema.sql:18-21`) — and the code matches.
- **Counts move in lockstep with edges, in one transaction.** `follow`/`unfollow`/`like`/`unlike`
  (`postgres.rs:611-822`) each run existence-check → idempotent `INSERT … ON CONFLICT DO NOTHING` /
  `DELETE` → count bump **only when `rows_affected == 1`** → read, all inside one
  `with_transaction`. The bump is a single `UPDATE … SET c = c + $delta` (`bump_follow_counts` /
  `bump_like_count`, `:1792-1831`), so PostgreSQL's row lock serializes concurrent increments on the
  same row — no lost update. The `CHECK (... >= 0)` columns are an in-store backstop against
  underflow. The concurrent-distinct-followers, concurrent-distinct-likers, concurrent-duplicate
  (idempotent), and like-then-unlike-churn cases are correct, and the tests that assert them
  reconcile the stored count against the edge set read back through the public listing API rather
  than only re-reading the count (`concurrency_invariants.rs:316-464`) — these would fail if a count
  drifted from its edges.
- **Handle uniqueness under concurrency.** `create_user` (`:208-249`) does not SELECT-then-INSERT;
  it inserts and maps the unique-index violation to `Conflict` (`:236-240`). Two concurrent
  registrations of the same handle resolve to one success and one clean `Conflict`, with no count or
  index drift.
- **Timeline cursor paging.** `timeline` (`:539-589`) scans `id < cursor ORDER BY id DESC LIMIT
  n+1`; the cursor is the last returned id, so paging is exactly-once (no skips, no duplicates) and
  ordered by the stable durable id. A malformed cursor fails safe to the first page. The
  exactly-once/descending assertion in `assert_exactly_once_descending` (`:824-839`) would fail on a
  skip or a duplicate.
- **Domain-boundary validation.** Values cross the boundary through `chirp-types`
  unrepresentable-if-invalid value objects, and stored rows are lifted back through the validating
  constructors (`mapping` module, `:2268+`), so a corrupt row surfaces as an error, not a bad value
  or a panic. The schema's length/`CHECK` constraints mirror the domain invariants as defence in
  depth.

## Findings

### COR-01 — #65's "under concurrency" guarantee is asserted by tests that run in no CI gate
- **severity**: blocker
- **blocks_landing**: true
- **location**: `.github/workflows/ci.yml:86-96` (the `test` job) with
  `crates/chirp-server/tests/concurrency_invariants.rs:267-309` and
  `crates/chirp-server/Cargo.toml` (`postgres = ["dep:sqlx"]`, off by default) @ 09fa453
- **acceptance-criterion / design ref**: #65 (final criterion: "covered by automated tests that
  assert them against a durable backing store under concurrent access, so the guarantee is checkable
  by someone who never met the author")
- **principle**: a guarantee is proved by a test that actually executes in the gate, not by a
  well-written test that the gate never runs.
- **why it matters here**: the durable concurrency suite is doubly gated — it compiles only under
  `--features postgres`, and even then every durable test returns early via `store_or_skip!` unless
  `CHIRP_TEST_DATABASE_URL` is set (`concurrency_invariants.rs:299-309`). The CI `test` job runs
  `cargo test --workspace --locked` with no `postgres` feature, no Postgres service, and no
  `CHIRP_TEST_DATABASE_URL`, so the entire `durable` module is not even compiled there. The `clippy`
  job compiles `--features postgres` but does not execute tests and has no database. The result: not
  one assertion about counts, ids, or multi-write atomicity **against the durable store under
  concurrency** executes in any automated gate. The only concurrency test that runs is the
  `store_free` half against `InMemoryRepository` — the store that issue #65 itself says "gets
  consistency for free from one global lock," so it is no evidence for the durable store. A stranger
  who clones the repo and runs the standard `cargo test` reproduces exactly zero of #65's durable
  concurrency coverage. #65 is therefore asserted, not proved.
- **confidence**: verified
- **what would satisfy me**: a required CI job that provisions a throwaway PostgreSQL, sets
  `CHIRP_TEST_DATABASE_URL`, and runs `cargo test -p chirp-server --features postgres` so the
  `durable` suite executes on every PR (e.g. a `services: postgres` job, or a compose step); and the
  suite failing CI if the database is unreachable rather than skipping green. Overlaps the root
  `SUBTASK_durability_proof` (general test depth / the drill) and `SUBTASK_ci_doc_diagnosis` (CI
  health) — recorded here because it is exactly #65's invariant-under-concurrency proof that is
  missing from the gate; left for synthesis to de-duplicate.

### COR-02 — `delete_account` reconcile-then-cascade can drift a surviving count against a concurrent edge write on the victim
- **severity**: major
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/repository/postgres.rs:1251-1329` (reconcile UPDATEs at
  `:1267-1308` run before the `DELETE FROM users` cascade at `:1315`); isolation is READ COMMITTED
  (`with_transaction` → `self.pool.begin()`, `:2142`, no `SET TRANSACTION ISOLATION`);
  `ensure_user_exists` is a plain `SELECT EXISTS` with no row lock (`:1750-1766`) @ 09fa453
- **acceptance-criterion / design ref**: #65 ("under concurrent requests … a reader never observes a
  count that disagrees with the edges"; "account-deletion cascade" named as a multi-write op)
- **principle**: reconciling denormalized counts from the edge set and then cascading the edges must
  be atomic with respect to a concurrent writer that adds an edge the cascade will remove.
- **why it matters here**: consider `delete_account(A)` racing `follow(C → A)` under READ COMMITTED.
  `delete_account` reconciles survivors' counts by reading `follows` (`UPDATE users SET
  following_count = following_count - 1 WHERE id IN (SELECT follower_id FROM follows WHERE
  followee_id = A)`), then deletes `A`, cascading the follow edges. If the concurrent `follow(C → A)`
  commits *after* the reconcile subquery's snapshot but *before* the cascade removes the edge, then:
  the reconcile did not see the `C → A` edge (so `C.following_count` is not decremented), `follow`
  incremented `C.following_count` by one, and the cascade then deletes the `C → A` edge. Net:
  `C.following_count` is one greater than `C`'s actual following edges — a count/edge disagreement
  that survives the operation. The reconcile-then-cascade sequence takes no lock on `A` before the
  final `DELETE` (existence is a plain `SELECT`), so nothing serializes the concurrent
  FK-referencing insert against the reconcile. The same shape applies to `like(C, chirpOfA)` or
  `follow(A → C)` racing `delete_account(A)`. No test exercises a mutation on the victim concurrent
  with its deletion — `delete_account_cascade_reconciles_counts_atomically_under_concurrency`
  (`concurrency_invariants.rs:470-544`) builds all edges sequentially and only deletes concurrently
  with *other deletes*, so this interleaving is uncovered.
- **confidence**: suspected
- **what would satisfy me**: a test that runs `follow(C → A)` (and `like` of one of A's chirps)
  concurrently with `delete_account(A)` and asserts every surviving neighbour's denormalized count
  equals its actual edge set afterward — and, if it reproduces, one of: `SELECT 1 FROM users WHERE
  id = A FOR UPDATE` at the top of `delete_account` (so a concurrent FK insert serializes and then
  fails cleanly against the gone account), recomputing counts from the surviving edges *after* the
  cascade, or raising the transaction to SERIALIZABLE for this path. If confirmed, this is a direct
  #65 count/edge violation and would be blocker-class.

### COR-03 — lock-order deadlock aborts a valid reciprocal concurrent follow (surfaced as `Internal`)
- **severity**: major
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/repository/postgres.rs:1792-1815` (`bump_follow_counts`
  updates the follower's `following_count` first, then the followee's `follower_count`);
  `classify_write_error` maps SQLSTATE class `40` — which includes `40P01 deadlock_detected` — to
  `Internal`, not a retry signal (`:2043-2095`, `:2093`) @ 09fa453
- **acceptance-criterion / design ref**: #65 ("concurrent follow/unfollow"; the durable store "must
  provide the equivalent guarantee" to the in-memory store's global lock)
- **principle**: a multi-row count update must acquire its row locks in a global order, or concurrent
  operations that touch the same two rows in opposite order deadlock.
- **why it matters here**: `bump_follow_counts` always locks `follower` then `followee`. A concurrent
  `follow(A → B)` and `follow(B → A)` therefore lock `A` then `B` versus `B` then `A` — a lock-order
  inversion. PostgreSQL detects the cycle and aborts one transaction with `40P01`, which
  `classify_write_error` turns into `ServerError::Internal`. The losing follow — a legitimate
  operation — fails spuriously under concurrency, where the in-memory reference (one global lock)
  would serialize and succeed. Counts are not corrupted (the aborted transaction rolls back
  cleanly), so this is a liveness/robustness divergence from the reference rather than an invariant
  break; hence major, not blocker. It is untested (no reciprocal-follow race in the suite) and would
  show up in production as intermittent 5xx on mutual follows.
- **confidence**: suspected
- **what would satisfy me**: acquire the two user rows in a canonical order (e.g. by ascending id) in
  `bump_follow_counts` so no inversion is possible; plus a test that races `follow(A → B)` with
  `follow(B → A)` and asserts both succeed with correct counts. (If a deadlock-retry policy is
  preferred instead, `40P01` should map to a retryable/`Unavailable`-class signal rather than
  `Internal`.) Overlaps `SUBTASK_code_quality` (lock-ordering idiom) and `SUBTASK_architecture_contract`
  (concurrency-safety of the seam) — noted for synthesis.

### COR-04 — "ids stable across restart" is proved only by a fresh connection pool, not an actual restart
- **severity**: minor
- **blocks_landing**: false
- **location**: `crates/chirp-server/tests/concurrency_invariants.rs:551-601`
  (`concurrently_allocated_ids_are_unique_and_stable_across_a_fresh_connection`) and `:289-295`
  (`connect` opens a new pool, the stated restart proxy) @ 09fa453
- **acceptance-criterion / design ref**: #65 ("entities created after a restart receive ids strictly
  greater than every id assigned before it … remain stable across restarts")
- **principle**: "stable across restart" and "strictly greater after restart" are claims about an
  actual process/database restart, which a second connection pool against the same running database
  does not exercise.
- **why it matters here**: the test reconnects with a fresh pool and confirms ids resolve to the same
  records — it demonstrates stability across a connection, not across a restart, and the test's own
  doc comment calls the pool "the across-restart proxy." The monotonic-after-restart clause
  (new ids strictly greater than every pre-restart id) is not asserted at all here. The actual
  restart/redeploy/reschedule proof lives in the durability drill, which is the root
  `SUBTASK_durability_proof`'s concern — so this is a coverage gap for #65's restart clause that is
  discharged (if at all) elsewhere, not a defect in the store. Recorded so synthesis can confirm the
  restart clause is proved by the drill rather than left to the proxy.
- **confidence**: verified
- **what would satisfy me**: the id monotonic-and-stable-across-restart clause is covered by the
  durability drill against a real restart (restart the database/pod, then create an entity and assert
  its id exceeds every pre-restart id and prior records are unchanged), and the #65 review can point
  to that drill step. Overlaps `SUBTASK_durability_proof`; left for synthesis.

## Concern sub-verdict
- **HAS-BLOCKERS**
- COR-01 blocks landing: #65's central "domain invariants, derived counts, and opaque monotonic ids
  hold under concurrency — proved, not asserted" is not proved, because the durable-store concurrency
  tests execute in no automated gate. The store implementation is otherwise well-built for #65 (sound
  id mechanism, counts maintained in-transaction with the edges, idempotent edge ops, exactly-once
  cursor paging); the two suspected concurrency hazards (COR-02 count drift on delete-vs-concurrent-
  write, COR-03 reciprocal-follow deadlock) and the restart-proof proxy gap (COR-04) are recorded for
  confirmation and for synthesis to weigh against the sibling concerns they overlap.
