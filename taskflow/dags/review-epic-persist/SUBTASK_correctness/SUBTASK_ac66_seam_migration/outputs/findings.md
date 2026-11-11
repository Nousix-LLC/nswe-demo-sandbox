# Findings — #66 ChirpRepository seam fidelity, single-writer safety, migration/versioning — PR #113 @ 09fa453

## What I checked

- **Issue #66's four acceptance criteria**, read on GitHub, traced to the change: (1) durable store is a
  second implementor of the existing `ChirpRepository` trait with the in-memory implementor retained and the
  transport unchanged; (2) the seam expresses every release-bar capability; (3) single-writer / single
  consistent dataset across replicas; (4) a defined, inspectable schema version applied by a forward-migration
  path.
- **The seam itself** — `crates/chirp-server/src/repository/mod.rs` at the pinned commit (the full 494-line
  trait). Enumerated the capability set: 10 original methods plus 13 release-bar additions plus
  `sweep_expired_transient_state` = 24 `async fn`s, all returning `Result<_, ServerError>`, trait kept
  object-safe via `async_trait`.
- **The durable backend** — `crates/chirp-server/src/repository/postgres.rs` (5763 lines). Confirmed every one
  of the 24 trait methods has a real body in `impl ChirpRepository for PostgresRepository` (lines 208–1659).
  Read in full the security- and integrity-sensitive bodies: `create_user`, `login`, `resolve_token`,
  `verify_credential`, `begin_account_recovery`, `complete_account_recovery`, `invalidate_session`,
  `delete_account`, `export_user_data`, `remove_chirp`, `set_account_suspension`, `store_health`,
  `sweep_expired_transient_state`, and the `with_transaction` / id-allocation / mapping machinery.
- **Stub / weakening scan** — grepped for `todo!`/`unimplemented!`/`unreachable!`/`panic!`/`TODO`/`FIXME`
  across the backend. Only hit: one `panic!` at `postgres.rs:2893`, inside a `#[cfg(test)]` helper. No method
  is a stub, a `todo!()`, or an error-swallow.
- **Single-writer mechanism** — `main.rs` backend selection, `with_transaction` commit/rollback semantics, and
  the deployment topology in `deploy/chirp/40-postgres-statefulset.yaml`, `deploy/chirp/10-deployment.yaml`,
  `deploy/chirp/45-postgres-service.yaml`.
- **Migration / versioning** — the embedded `sqlx::migrate!()` runner (`postgres.rs:52`), its invocation at
  `connect` (`postgres.rs:80–94`), `schema_version()` (`postgres.rs:117–124`), and both migration files
  (`migrations/0001_baseline.sql`, `migrations/0002_domain_schema.sql`). Checked ordering, idempotency,
  fail-safety, and whether any DDL is applied outside the runner.
- **Second-implementor / transport-unchanged** — that `InMemoryRepository` remains the default and still
  implements the full trait (`in_memory.rs`, +1563), and that routing is additive (`api/router.rs` +52/−3,
  `api/mod.rs` +2/−1) rather than a transport rewrite.

## What I found clean

- **The full capability set is implemented behind the seam, not around it.** All 24 `ChirpRepository` methods
  have genuine durable bodies in `PostgresRepository`; none is stubbed, `todo!()`, or silently weakened. The
  durable store is a true second implementor and the in-memory backing is retained as the default, so the
  seam carries the swap rather than being bypassed (#66 AC1, AC2).
- **Writes are confirmed-durable.** `with_transaction` (`postgres.rs:2137–2166`) returns `Ok` only after the
  commit itself succeeds, rolls back on the closure's `Err`, and maps a failed start/commit to `Unavailable`
  (capacity) or `Internal` — so an undurable write is reported as a failed action, never falsely confirmed.
- **Session expiry is enforced at the serve path, not only by the sweep.** `resolve_token`
  (`postgres.rs:396–418`) filters `expires_at IS NULL OR expires_at > now`, the exact complement of the
  sweep's `expires_at <= now`, so an expired session is treated as absent even before its row is reclaimed.
- **Recovery is fail-secure and single-use.** `complete_account_recovery` reports one indistinguishable
  `Unauthorized` for unknown handle / unknown / mismatched / expired token, and consumes the challenge in the
  same transaction.
- **`account_deletion_cascade` reconciles survivor counts before the cascade removes the edges**
  (`postgres.rs:1261–1323`), inside one transaction, with the schema's `ON DELETE CASCADE` / `SET NULL`
  foreign keys as the in-store backstop.
- **Single-writer is satisfied and documented.** The Postgres StatefulSet pins `replicas: 1` as a deliberate,
  documented limitation (`40-postgres-statefulset.yaml:34–37`, ADR-0001 §2): one writable primary holding one
  consistent dataset, per-ordinal RWO PVC, so data cannot silently fork. Domain state is external, so the app
  tier (`10-deployment.yaml`) is safe to run at one replica or scaled against the same dataset. This is #66's
  "constrain to one replica by configuration, documented as a store limitation" branch, met.
- **The migration path is a real, versioned, forward-only runner.** `sqlx::migrate!()` embeds the
  `migrations/` set into the binary; `connect` runs it before the repository is handed to the transport layer,
  so the server never serves an un-migrated schema; a migration failure is surfaced as a failed startup
  (`postgres.rs:89–91`), never swallowed. Migrations are ordered (`0001` → `0002`), each statement is
  idempotent (`IF NOT EXISTS` / `ON CONFLICT DO NOTHING`), sqlx tracks applied versions in `_sqlx_migrations`
  and checksums them (an edited applied migration would fail), and `schema_version()` exposes `MAX(version)`
  as the inspectable version (#66 AC4). No DDL is applied ad hoc outside the runner — all table/sequence/index
  creation is confined to the two migration files.

## Findings

### COR-20 — Seam documentation still describes the durable backend as un-implemented stubs
- **severity**: major
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/repository/postgres.rs:9-28` (module "Scaffold boundary" doc),
  `:186-188` (impl-block comment), `:1580-1582` (`store_health`: "Unlike the other scaffold methods this is
  **not** a stub"); `crates/chirp-server/Cargo.toml:68` ("Durable query bodies are downstream; the scaffold
  uses only the pool + migrator") @ 09fa453
- **acceptance-criterion / design ref**: #66 (BAR-021 · REQ-DOM-018)
- **principle**: Documentation on the seam under review must describe what the code does. #66 is judged "by
  inspection"; prose that contradicts the implementation misdirects that inspection.
- **why it matters here**: The module doc states "this is the foundation scaffold, not the durable
  implementation … every write/read below is a skeleton stub that returns `Internal`." That is false at this
  commit — all 24 methods have real durable bodies, with ~3000 lines of integration tests asserting durable
  round-trips, cascades, and concurrency. A reader auditing "is the capability set actually implemented?" for
  #66 would read the module doc and conclude it is not. This is one stale-prose pattern recurring in four
  places (module doc, impl comment, `store_health` aside, Cargo.toml), left over from an earlier scaffold
  stage. It does not change behavior — the capability set is delivered — which is why it does not block #66's
  behavioral bar.
- **confidence**: verified
- **what would satisfy me**: Replace the scaffold-era prose at the four locations so the seam docs describe
  the implemented durable behavior, and confirm `cargo doc` builds clean afterward. **Overlap:** this stale
  rustdoc (and any intra-doc links it carries to the private `mapping` items) is a plausible cause of the
  failing required `doc` check; that CI blocker is owned by `SUBTASK_ci_doc_diagnosis` and the root verdict
  (ID-DOC-GATE). Recorded here as the content defect on the #66 seam and flagged for synthesis to connect to
  the CI finding, not claimed as a COR-area blocker.

### COR-21 — `remove_chirp` advertises a `Forbidden` result the store never returns
- **severity**: minor
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/repository/mod.rs:441-445` (trait doc: `Forbidden` if `actor` is not
  permitted) vs `crates/chirp-server/src/repository/postgres.rs:1473` and
  `crates/chirp-server/src/repository/in_memory.rs:884` (both take `_actor`, unused) @ 09fa453
- **acceptance-criterion / design ref**: #66 (REQ-DOM-020)
- **principle**: The seam's documented error contract should match what every implementor can produce; an
  advertised failure no backing returns is a contract the seam cannot keep.
- **why it matters here**: Both implementors ignore `actor` and perform the removal unconditionally, so the
  trait's documented `Forbidden` path is dead at the store. This is consistent across backings and matches the
  stated design (author-vs-moderator authorization is deferred upstream to `REQ-ID-*`), so it is not a dropped
  or weakened capability — the removal itself works and is idempotent. But the seam doc promises an
  authorization result the store cannot give, unlike the sibling `set_account_suspension`, which does enforce
  the one model-level `Forbidden` it owns (self-target). The asymmetry is worth resolving so the documented
  error set matches what the store can return.
- **confidence**: verified
- **what would satisfy me**: Either note in the `remove_chirp` trait doc that authorization (and therefore any
  `Forbidden`) is entirely an upstream concern with no store-level check, or add the store-level guard if the
  model expects one — matching whichever decision `set_account_suspension` follows.

### COR-22 — Single-writer guarantee rests on a replica count with no hard guard
- **severity**: minor
- **blocks_landing**: false
- **location**: `deploy/chirp/40-postgres-statefulset.yaml:34-37`, `:149-168` (RWO PVC;
  ReadWriteOncePod noted as future hardening) @ 09fa453
- **acceptance-criterion / design ref**: #66 (BAR-021 · REQ-OPS-005)
- **principle**: A single-writer guarantee enforced only by a configuration value is only as strong as the
  change control around that value.
- **why it matters here**: The no-fork guarantee is `replicas: 1` on the StatefulSet. Scaling that StatefulSet
  above 1 would not create a replication cluster — each ordinal gets its own PVC and its own independent
  Postgres with its own dataset, which is exactly the data fork #66 exists to prevent. The manifest documents
  the limitation and names `ReadWriteOncePod` as the stricter future posture, which is what #66's
  documented-single-replica branch permits, so this is not a blocker. Recording it because the guarantee is a
  convention, not an enforced invariant, and a future scale-up would silently break it.
- **confidence**: verified
- **what would satisfy me**: The documented-limitation posture already clears #66. As additive hardening, a
  `ReadWriteOncePod` access mode (on a CSI-backed class) or an admission/policy guard that prevents the
  Postgres StatefulSet from scaling past one would make the single-writer constraint enforced rather than
  conventional. **Overlap:** provisioning topology is also in scope for the root `SUBTASK_operational_readiness`
  and `SUBTASK_architecture_contract`; left for synthesis to de-duplicate.

### COR-23 — Credential at rest is stored and compared in plaintext
- **severity**: minor
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/repository/postgres.rs:928` (`stored == secret` equality compare);
  credential persisted verbatim via the `set_credential` / `complete_account_recovery` upsert
  (`postgres.rs:842-905`, `:1061+`); schema `credentials.secret TEXT` (`migrations/0002_domain_schema.sql:73-77`)
  @ 09fa453
- **acceptance-criterion / design ref**: #66 (REQ-DOM-005; and REQ-ID-* downstream)
- **principle**: The `credential_set_verify` capability is "sound" only if the at-rest representation and the
  verification are not themselves a weakness.
- **why it matters here**: The capability round-trips correctly (set then verify authenticates; the error is
  indistinguishable across unknown-handle / no-credential / mismatch), so for #66's "capability present and not
  weakened" bar it passes. But the stored `secret` is the plaintext value and the check is a non-constant-time
  `==`. The code comments defer the credential crypto scheme to EPIC-IDENTITY (`REQ-ID-*`), so this is a known,
  documented deferral rather than an oversight. Recording it because it is visible in the seam implementation
  and bears on whether the capability is soundly realized.
- **confidence**: verified
- **what would satisfy me**: Hashing at rest (e.g. a password-hashing KDF) and a constant-time verify, when
  the EPIC-IDENTITY credential work lands. **Overlap:** credential handling and the at-rest representation are
  the root `SUBTASK_security`'s bar; recorded here as it touches #66's capability soundness and left for
  synthesis to de-duplicate.

## Overlaps recorded (bear on correctness; left for root synthesis to de-duplicate, not reconciled here)

- **Proof-in-CI of the durable backend.** The entire `postgres` module and its ~3000 lines of tests are behind
  `#[cfg(feature = "postgres")]` (`Cargo.toml:33`), OFF by default, and the backend tests acquire a live
  database via a `connect() -> Option<PostgresRepository>` helper that skips when no DB is present
  (`postgres.rs:4995`, `:5310`). So the #66 capability set is implemented in code, but whether it is *proved*
  in the pipeline depends on CI running `--features postgres` against a real Postgres. That proof-depth is the
  root `SUBTASK_durability_proof`'s bar; flagged here so it is connected, not assumed.
- **Seam contract-stability / signature shape** (object-safety, breaking-change analysis of the trait) is the
  root `SUBTASK_architecture_contract`'s. I confirmed the additions are additive and the trait stayed
  object-safe for #66's behavioral purpose; the shape analysis is theirs.
- **Denormalized count maintenance under concurrency** (`follower_count` / `following_count` / `like_count`
  updated inside transactions on `follow` / `unfollow` / `like` / `unlike` / `delete_account`) is #65's
  "invariants under concurrency" bar (`SUBTASK_ac65_invariants`). I checked the counts are maintained inside
  the same transaction as the edge write; the concurrency proof is theirs.

## Concern sub-verdict

- **NON-BLOCKING-ONLY**
- #66's three behavioral pillars all hold: the full `ChirpRepository` capability set is implemented behind the
  seam as a real second implementor with no method dropped, stubbed, or weakened; single-writer safety is
  enforced by a documented single-primary posture holding one consistent dataset; and the schema is versioned
  and applied by a forward-only, ordered, idempotent, fail-safe migration runner with an inspectable version.
  The findings are documentation-accuracy and hardening issues — none defeats #66's own acceptance criteria.
  (The PR as a whole remains gated by the failing required `doc` check; that blocker is represented by
  `SUBTASK_ci_doc_diagnosis` and the root verdict, and COR-20 flags the stale seam docs as a likely contributor.)
