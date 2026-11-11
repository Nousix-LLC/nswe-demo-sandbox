# Findings — Durability proof (test coverage, depth, and the drill) — PR #113 @ 09fa453

Scope: whether the tests and the durability drill actually *prove* the acceptance criteria of #65/#66/#67
and the failure paths, or pass vacuously. I read the tests as closely as the code. Retention/expiry
enforcement (session/recovery/export lifetimes) and the reclaim CronJob are scoped to the operational-readiness
and correctness concerns and are not re-reported here; I confirmed only that durable *session* state is proven
(see below).

## What I checked

- **The two integration test files** at the pinned commit:
  - `crates/chirp-server/tests/concurrency_invariants.rs` (884 lines) — the store-free half (in-memory, always
    compiled) and the `#[cfg(feature = "postgres")]` durable half, which drives concurrent load against
    `PostgresRepository` and reconciles stored state against edge sets.
  - `crates/chirp-server/tests/api.rs` (814 lines) — the end-to-end in-memory HTTP suite (happy paths, the
    `error_mapping` table, pagination) and the `/readyz` readiness tests.
- **The in-crate unit/live tests** in `crates/chirp-server/src/repository/postgres.rs`:
  `substrate_tests` and `capacity_failsafe_tests` (store-free), and the `substrate_live_tests` and per-method
  durable modules gated on `CHIRP_TEST_DATABASE_URL` — the rollback, capacity-fail-safe, monotonic-id, and
  commit-durability proofs.
- **The drill**: `deploy/chirp/drill/durability-drill.sh` (261 lines) and `deploy/chirp/drill/PROCEDURE.md`
  (105 lines) — the store layer (always run) and the system layer (run only when `CHIRP_IMAGE` is supplied),
  the restart/redeploy/reschedule modes, the pass check, and the documented caveats.
- **The CI wiring and feature gating**: `.github/workflows/ci.yml` (the `test`, `clippy`, and `doc` jobs),
  `crates/chirp-server/Cargo.toml` (`postgres = ["dep:sqlx"]`, `sqlx … optional = true`), and
  `crates/chirp-server/src/repository/mod.rs` (`#[cfg(feature = "postgres")] pub mod postgres`).
- **The composition root** `crates/chirp-server/src/main.rs` — the config-driven durable-vs-in-memory
  selection and its startup fail-closed behaviour.
- **The acceptance criteria** read from the source issues #65, #66, #67 (not only the hub paraphrase), traced
  to the `BAR-020/021/022` and `REQ-*` they name.

## What I found clean

- **The durable concurrency assertions check real surviving state, not `count == count`.** Each count is
  reconciled against the actual durable edge set read back through the public listing API
  (`follower_count_matches_edge_set_under_concurrent_distinct_followers` compares the denormalized count AND
  `list_followers` paged to the end: `concurrency_invariants.rs:337-359`). A denormalized-count regression
  cannot pass by agreeing with itself.
- **"Durable across a fresh connection" is labelled as the proxy it is.** The durable half reconnects a new
  pool and reads back, and the module says this is the proxy for "a different pod / after restart"
  (`concurrency_invariants.rs:287-295`, `:643-666`, `:668-760`). It does not claim a process-restart proof it
  did not run — that burden is the drill's, and the file is clear about the seam.
- **The fail-closed substrate proofs read back absence, not just an error.**
  `a_failed_transaction_rolls_back_and_is_never_confirmed` fails *after* the write and then asserts the row is
  gone (`postgres.rs:2798-2842`); `an_exhausted_connection_pool_fails_safe_as_unavailable` injects a
  capacity-of-one pool, asserts `ServerError::Unavailable` (never a false confirmation), then reads back to
  confirm nothing persisted (`postgres.rs:2844-2915`). `capacity_failsafe_tests` also asserts that
  non-capacity SQLSTATEs (`unique_violation`, `connection_failure`, `serialization_failure`) are **not**
  misclassified as `Unavailable` (`postgres.rs:2695-2709`), so the category stays truthful.
- **The concurrency fan-out is sized not to become a capacity test.** `FANOUT = 8` is held at or below the
  pool's connection ceiling so the suite exercises in-flight concurrency without starving the pool
  (`concurrency_invariants.rs:57-61`).
- **The suite is rerunnable against a shared store.** Handles are minted from a process- and run-unique seed
  (`concurrency_invariants.rs:71-108`), so a second run against the same durable store does not collide.
- **Feature gating keeps the default build/test store-free.** `postgres` is off by default and pulls `sqlx`
  only when enabled (`Cargo.toml:33`, `:75`); the durable module is `#[cfg(feature = "postgres")]`
  (`repository/mod.rs:117-118`); every durable test additionally skips unless `CHIRP_TEST_DATABASE_URL` is set.
  `cargo build`/`cargo test` need no database.
- **Readiness fail-closed is tested on both arms, with a double standing in for a boundary.**
  `/readyz` returns 200 when `store_health` is `Ok` and 503 (not 500) with no error detail leaked when it errs,
  driven by an `UnhealthyStore` double whose only live method is `store_health` (`api.rs:629-680`). The double
  stands in for the store-reachability boundary, not for the logic under test.
- **Startup is fail-closed.** When a durable URL is configured, `PostgresRepository::connect(...).await?`
  propagates, so the process exits non-zero rather than serving non-durably (`main.rs:68-79`).
- **The drill is stranger-runnable and its caveats are disclosed.** `PROCEDURE.md` lists prerequisites, the
  pass check, how to obtain a pre-merge image, and the node-local-storage and throwaway-namespace limitations
  (`PROCEDURE.md:19-106`); the script refuses a movable tag or the all-zeros placeholder digest for the system
  layer (`durability-drill.sh:90-97`).

## Findings

### DUR-01 — No required CI check executes any durable-store proof
- **severity**: major
- **blocks_landing**: false
- **location**: `.github/workflows/ci.yml:80-90` (the `test` job runs `cargo test --workspace --locked`, no
  `--features postgres`, no `services:` database) and `.github/workflows/ci.yml:57-77` (the `clippy` job
  compiles `--features postgres --all-targets` but only lints); the proofs it does not run live at
  `crates/chirp-server/tests/concurrency_invariants.rs:273` and `:299-309` (durable half, feature- and
  env-gated) and `crates/chirp-server/src/repository/postgres.rs:2712-2916` and `:3114+` (live durable tests)
  @ 09fa453
- **acceptance-criterion / design ref**: #65 (BAR-020, "verified by automated test"); #67 (BAR-022)
- **principle**: Green is a claim about what the gate asserts. A proof that no required check runs cannot catch
  a behaviour regression; only compile-rot is caught.
- **why it matters here**: The durable store has a deep, non-vacuous proof suite — concurrency identities,
  fail-closed rollback, capacity fail-safe, monotonic ids, total-state-across-a-fresh-pool. None of it executes
  in any required check: the `test` job builds only default (in-memory) features, and `clippy --features
  postgres` compiles the durable tests but runs none. After merge, every required check can stay green while
  the durable write path silently regresses in behaviour; the in-memory suite, which `test` does run, is not
  durability evidence. #65's test criterion is *met* in substance — the automated tests exist and a stranger
  can run them (`concurrency_invariants.rs:19-25` documents the command) — so this is an enforcement/rot gap,
  not an unproven criterion, which is why it is major and not a blocker.
- **confidence**: verified
- **what would satisfy me**: a CI job that provisions an ephemeral PostgreSQL (`services:` in the workflow),
  sets `CHIRP_TEST_DATABASE_URL`, and runs `cargo test -p chirp-server --features postgres`. GitHub Actions
  service containers make this a few lines, and it turns the existing proofs into an enforced gate.

### DUR-02 — The drill's always-on store layer proves a synthetic table, but the summary claims user data survived
- **severity**: major
- **blocks_landing**: false
- **location**: `deploy/chirp/drill/durability-drill.sh:135-148` (creates `drill_evidence`, inserts four text
  literals, checksums them), `:184-185` (system layer SKIPPED when `CHIRP_IMAGE` is unset), `:256` (final
  `ALL MODES PASS — user data survived restart, redeploy and reschedule`) @ 09fa453
- **acceptance-criterion / design ref**: #67 (BAR-022, REQ-OPS-013)
- **principle**: A drill must not assert more than the path that ran actually proved.
- **why it matters here**: The documented default invocation (`durability-drill.sh` with no image,
  `PROCEDURE.md:30-31`) runs only the store layer, which creates its own `drill_evidence` table and checksums
  hand-written rows. It never writes through chirp's migrated schema or repository, so it proves "a Postgres
  row on this StatefulSet's PVC survives pod loss" — the persistence substrate — but not that chirp's own
  tables, wiring, and read-back survive. Yet the run prints `user data survived restart, redeploy and
  reschedule`. The chirp user-data claim is proven only by the system layer, which is optional. A stranger —
  the intended audience of #67 — running the headline command gets a green that overstates what was checked.
- **confidence**: verified
- **what would satisfy me**: either make the store-layer MODE/summary lines state precisely what they proved
  (PVC/row durability, not chirp user-data), or have the store layer write and read back through chirp's actual
  domain tables, or make the system layer the default so the headline command proves the headline claim. The
  system layer itself (`durability-drill.sh:220-250`) already asserts sign-in + content + counts end-to-end and
  is a sound proof when an image is supplied.

### DUR-03 — "reschedule" mode degrades to eviction-and-rebind on node-local storage
- **severity**: nit
- **blocks_landing**: false
- **location**: `deploy/chirp/drill/durability-drill.sh:159-178` and `deploy/chirp/drill/PROCEDURE.md:92-99`
  @ 09fa453
- **acceptance-criterion / design ref**: #67 (BAR-022, REQ-OPS-013)
- **principle**: A mode's pass line should not read as a stronger guarantee than the environment allowed.
- **why it matters here**: On a node-local StorageClass (e.g. `local-path`) a cross-node reschedule is
  physically impossible; the drill cordons the node, observes the `Pending` state, and rebinds on the same
  node. This is disclosed in both the script note and `PROCEDURE.md`, and cross-node/failover durability is
  explicitly deferred by ADR-0001 — so this is an honest, documented limitation rather than a defect. The only
  residual risk is that the `MODE reschedule PASS` line, read without the surrounding note, reads as a full
  cross-node reschedule proof.
- **confidence**: verified
- **what would satisfy me**: fold the node-affinity fact into the `reschedule` PASS detail string (as the other
  modes carry a detail), so the pass line itself names what was and was not exercised.

### DUR-04 — Fail-closed-on-non-durable-write is proven at the substrate, not end-to-end to the user
- **severity**: minor
- **blocks_landing**: false
- **location**: substrate proof present at `crates/chirp-server/src/repository/postgres.rs:2798-2842` and
  `:2844-2915`; no end-to-end counterpart in `crates/chirp-server/tests/api.rs` (the suite drives writes only
  against a healthy in-memory store, and the one store-failure test, `api.rs:651-680`, covers `/readyz`, not a
  write) @ 09fa453
- **acceptance-criterion / design ref**: #67 (BAR-022, REQ-OPS-012 — "a write that cannot be durably stored is
  reported to the user as failed, not falsely confirmed")
- **principle**: #67 phrases the guarantee at the user boundary ("reported to the user"); the proof should
  reach that boundary.
- **why it matters here**: The substrate tests prove `with_transaction` and the pool return a failure and
  persist nothing. What no test drives is a write whose durable commit fails, through the HTTP handler, to
  assert the client receives a 5xx rather than a false 2xx. The HTTP error mapping is tested for other classes
  and the substrate proof is solid, so the end-to-end behaviour is most likely correct — but it is inferred,
  not asserted. I frame this as the missing test, not a claim the behaviour is wrong.
- **confidence**: suspected
- **what would satisfy me**: one end-to-end test using the same double pattern as `UnhealthyStore` — a
  repository whose `create_chirp` (or `follow`) returns `ServerError::Unavailable` — asserting
  `POST /api/chirps` returns a 5xx `ApiError` and no success body. The readiness test already shows the pattern
  is cheap.

## Concern sub-verdict
- **NON-BLOCKING-ONLY**
- The durability proofs exercise concurrent load and reconcile stored state against the edge sets, and every
  durable acceptance criterion of #65/#66/#67 has a runnable, stranger-checkable proof, so this concern leaves
  no criterion unproven and carries no blocker. The
  open items are an un-enforced CI gate (DUR-01) and a drill whose default run overstates what it checked
  (DUR-02), both major and both backlog, plus two smaller gaps. (The failing required `doc` check — the actual
  landing blocker — is the CI-diagnosis concern's to record, not this one's.)
