# Findings — Code quality, design & Rust idiom — PR #113 @ 09fa453

Scope: craftsmanship of the change across the store backend (`repository/postgres.rs`,
`repository/in_memory.rs`, `repository/export.rs`), the `ChirpRepository` seam (`repository/mod.rs`),
and the wiring (`main.rs`, `api/router.rs`, `error.rs`, `Cargo.toml`, `lib.rs`, `api/mod.rs`). Rust
idiom and `#[cfg(feature = "postgres")]` gating hygiene examined. Read-only; one findings document.
This concern judges craftsmanship, not whether a criterion is delivered — where a quality defect
touches the substance of #65/#66/#67, it is handed to correctness / durability-proof via synthesis
rather than re-judged here.

## What I checked

- The seam `repository/mod.rs`: object-safety (`async_trait`, `Arc<dyn ChirpRepository>`), the
  additive release-bar method set, the error contract (`Result<_, ServerError>`), and the documented
  invariants.
- The durable backend `repository/postgres.rs` whole (≈2,600 lines of implementation + a `mapping`
  module + ≈3,100 lines of `#[cfg(test)]` tests): the `ChirpRepository` impl for all 22 methods, the
  store-access substrate (`with_transaction`, sequence allocation, `classify_write_error`, capacity
  detection), and the `chirp-types ⇄ row` mapping.
- The in-memory backend `repository/in_memory.rs`: the release-bar method additions and their
  consistency with the durable backend.
- `repository/export.rs`: the shared export document and its feature-gating posture.
- The wiring: `main.rs` (config-driven backend selection, shutdown signals), `api/router.rs`
  (`/readyz` vs `/healthz`), `error.rs` (the `ServerError` enum + the added `Unavailable` variant),
  `Cargo.toml` (the `postgres` feature + `sqlx` dependency shape), `lib.rs`, `api/mod.rs`.
- Rust idiom: error handling, ownership/borrowing, `async`/transaction structure, SQL parameterization
  vs string building, panic-freedom in production paths, and feature-gating leakage.
- Diff provenance: whether each flagged item is newly introduced by this PR or pre-existing, via
  `gh pr diff 113`.
- Plain-voice scan of the shipped comments/naming.

## What I found clean

- **The seam is additive and object-safe.** Every release-bar capability (`set_credential`,
  `delete_account`, `export_user_data`, …) is added as a new `async fn` over the same `chirp-types`
  surface and the same `ServerError` contract; the original operations are untouched, so the trait
  stays `dyn`-compatible and the transport layer is not disturbed (`repository/mod.rs:189-494`). This
  is the right way to grow a frozen seam.
- **`with_transaction` enforces confirmed-write-before-success** (`postgres.rs:2137-2166`): the value
  is returned only after `commit()` itself succeeds; a failed commit is a failed action, a closure
  error rolls back. This is the load-bearing durability primitive and it is correct and centralized.
- **One fail-safe error-mapping point.** `classify_write_error` (`postgres.rs:2093-2100`) is the
  single place the write path routes failures through, and capacity detection
  (`is_capacity_exhaustion` / `is_capacity_exhaustion_sqlstate`, `postgres.rs:2056-2081`) is a pure,
  database-free function unit-tested directly against SQLSTATE strings — a well-chosen boundary.
- **Boundary re-validation, no panics.** The `mapping` module lifts every stored row back through the
  `chirp-types` validating constructors and surfaces a corrupt column as a typed error
  (`postgres.rs:2302-2345`, `UserRow::into_user` / `ChirpRow::into_chirp`); id/count overflow is
  handled via `try_from`, never a silent wrap. Every `unwrap`/`expect`/`panic!` in the file lives in
  `#[cfg(test)]` modules (all at line ≥ 2629); production paths are panic-free.
- **SQL is uniformly parameterized.** All statements use `sqlx::query*` with `.bind(...)`; the
  `format!` calls build error messages, not SQL. The one place SQL varies by input
  (`list_follow_edge`, `postgres.rs:1888-1903`) selects between two fixed `&'static str` literals and
  still binds the user value.
- **Denormalized counts move inside the same transaction as the edge** (`follow`/`unfollow`/`like`/
  `unlike`, and the `delete_account` cascade reconciliation at `postgres.rs:1261-1308`), and only on a
  genuine state change (`rows_affected == 1`). Idempotency is via `ON CONFLICT DO NOTHING` / zero-row
  deletes.
- **The two backings stay consistent.** Both share `ExportDocument` for byte-identical
  exports, share `RECOVERY_TOKEN_VALIDITY_MILLIS` / `SESSION_LIFETIME_MILLIS`, and mirror fail-secure
  indistinguishable auth errors (`verify_credential`, `complete_account_recovery`). The parallel
  structure makes the layer easy to reason about and extend.
- **Wiring is tidy.** `main.rs` selects the backend from config with no code edit, warns loudly when a
  DB URL is set but the `postgres` feature is absent (`main.rs:81-92`), and drains on both SIGINT and
  SIGTERM (`main.rs:129-157`). `/readyz` deliberately returns 503 (not the API seam's 500) and is
  backend-agnostic through `store_health` (`api/router.rs:103-143`). The `Cargo.toml` `postgres`
  feature is off by default so the store-free test suite needs no database (`Cargo.toml:26-33,63-75`).

## Findings

### CQ-01 — Source comments across the persistence layer describe fully-implemented methods as unimplemented "scaffold stubs" / "placeholders"
- **severity**: major
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/repository/postgres.rs:1,9-25,186-188,824,1578-1582` and
  `crates/chirp-server/src/repository/in_memory.rs:522-527` @ 09fa453
- **acceptance-criterion / design ref**: #66 (full capability set behind the seam)
- **principle**: Comments must describe the code as it is. A comment that states the opposite of what
  the code does is worse than no comment — it misleads every later reader and erodes trust in the
  (otherwise strong) documentation.
- **why it matters here**: The `postgres.rs` module header calls the module a "compiling scaffold …
  What it deliberately does **not** do: the durable method **bodies**. Every `ChirpRepository`
  write/read below is a skeleton stub that returns `ServerError::Internal`" (L9-25), and the section
  banners repeat "scaffold stubs" (L186, L824). `store_health`'s doc even says "Unlike the other
  scaffold methods this is **not** a stub" (L1580), naming the others as stubs. In fact `create_user`,
  `login`, `create_chirp`, `follow`, `delete_account`, `sweep_expired_transient_state` and the rest
  are fully implemented, with real transactions and SQL. `in_memory.rs:522-527` carries the same false
  framing ("Each placeholder … reports a `ServerError` and NEVER falsely confirms success"), yet those
  methods fully implement their behaviour against the in-memory store. A maintainer — or a reviewer
  tracing #66's "full capability set, no capability dropped" claim — who believes the module header
  will conclude the durable bodies are unwritten. The contradiction is a pattern, not a slip: it
  recurs in five places in `postgres.rs` and once in `in_memory.rs`, all reading as stale leftovers
  from an earlier skeleton phase that the filled-in bodies never corrected. Newly introduced
  (`postgres.rs` is a new file; the `in_memory.rs` release-bar section is new in this PR).
- **confidence**: verified
- **what would satisfy me**: Rewrite the module header and the four section/`store_health` comments in
  `postgres.rs`, and the `in_memory.rs:522-527` banner, to describe the methods as implemented. If any
  method is in fact intended to remain a stub, make the code and the comment agree. **Handoff to
  correctness / durability-proof via synthesis:** my lens confirms the bodies are present; whether
  they are *proven* (the backend is `#[cfg(feature = "postgres")]`-gated, so default `cargo test` does
  not compile it) is their call — if they find #66 is not actually exercised, the severity of this
  mismatch should be reconsidered there.

### CQ-02 — Feature-gating doc leak: an always-compiled module links an intra-doc path into the `postgres`-gated module
- **severity**: minor
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/repository/export.rs:7` @ 09fa453
- **acceptance-criterion / design ref**: n/a (feature-gating hygiene; see the brief)
- **principle**: An item compiled under all feature sets must not carry a rustdoc intra-doc link to an
  item that exists only under one feature; the link cannot resolve when that feature is off.
- **why it matters here**: `export.rs` is compiled unconditionally (`mod export;`,
  `repository/mod.rs:110`), but its module doc links
  `[`PostgresRepository`](crate::repository::postgres::PostgresRepository)`, and `postgres` is
  `#[cfg(feature = "postgres")] pub mod postgres;` (`repository/mod.rs:117-118`). In a default
  (no-feature) `cargo doc` the link target does not exist, which `rustdoc::broken_intra_doc_links`
  flags; with the workspace lint set denying it, the doc build errors. This is the one ungated → gated
  doc link in the crate (`mod.rs`'s `[`postgres`]` reference sits on the doc of the gated item itself,
  so it is fine). It is feature-gating leakage from an ungated module — exactly the "does the
  `#[cfg]` stay clean or leak" question in scope here. **Possible connection to the failing `doc` CI
  check** — I flag it so `SUBTASK_ci_doc_diagnosis` can confirm or rule it out; root-causing the `doc`
  job is that spoke's, not mine.
- **confidence**: verified (that the link targets a gated path from an always-compiled module);
  suspected (that it is the cause of the `doc` check failure — depends on how CI invokes `cargo doc`)
- **what would satisfy me**: Make the reference not a resolvable-link in the default build — e.g. drop
  the intra-doc link and name the type in plain backticks, or gate the doc text, or use a path that
  resolves without the feature. Then `cargo doc` with default features is clean.

### CQ-03 — `FollowRow` / `LikeRow` mapping types and their converters are unused outside their own tests
- **severity**: minor
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/repository/postgres.rs:2550-2626` (defined) vs only
  `postgres.rs:3013-3028` (used, inside `#[cfg(test)]`) @ 09fa453
- **acceptance-criterion / design ref**: n/a
- **principle**: Don't ship abstraction without a caller. Speculative generality adds surface area and
  test weight and misleads the reader about how the code actually flows.
- **why it matters here**: The `mapping` module's banner says "every later method author reuses them
  rather than re-deriving the mapping" (`postgres.rs:2244-2248`). That holds for `UserRow` /
  `ChirpRow` (used across `create_user`, `get_user`, `timeline`, `update_profile`, …), but
  `FollowRow` / `LikeRow` and `from_follow` / `into_follow` / `from_like` / `into_like` have no
  production caller — `follow`/`unfollow`/`like`/`unlike` write edge SQL directly. Their only
  references are in the `mapping_tests` module. Because they are `pub`, `dead_code` does not fire, so
  the unused abstraction ships silently and a maintainer may assume edges round-trip through row types
  when they do not.
- **confidence**: verified
- **what would satisfy me**: Either route the edge writes through these row types (so the symmetry the
  comment claims is real), or remove `FollowRow`/`LikeRow` and their converters (and the tests that
  only exist to exercise them) until a caller needs them.

### CQ-04 — Shipped source comments carry internal task-decomposition / build-stage vocabulary
- **severity**: minor
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/repository/postgres.rs:1662-1669,1940-1962,2222-2260` (e.g.
  "SUBTASK_store_access_substrate", "SUBTASK_mapping_validation", "SUBTASK_durable_impl",
  "SUBTASK_content_timeline_impl", "the retention stage", "the graph stage's") @ 09fa453
- **acceptance-criterion / design ref**: n/a
- **principle**: Library source comments should describe the code, not the process that produced it.
  References to internal work-breakdown identifiers are unresolvable to anyone outside that process.
- **why it matters here**: The comments repeatedly name construction stages and subtask ids and write
  in present/future tense ("the durable bodies are downstream", "a later retention stage adds") as if
  the build were mid-flight, when the committed file already contains every stage. A future
  maintainer cannot resolve "SUBTASK_mapping_validation" or "the graph stage" against anything in the
  repository. This is the same stale-build-narrative root as CQ-01, expressed as vocabulary rather
  than false status.
- **confidence**: verified
- **what would satisfy me**: Replace the stage/subtask references and the in-progress tense with
  descriptions of the code as it stands (what the section does, what invariant it upholds), dropping
  the internal identifiers.

### CQ-05 — `error.rs` module docs claim the module is HTTP-free and does not own `IntoResponse`, contradicted by its own code (pre-existing)
- **severity**: nit
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/error.rs:8-17` vs `error.rs:40-43,216-241`, cross-checked
  against `crates/chirp-server/src/api/mod.rs:13-15` @ 09fa453
- **acceptance-criterion / design ref**: n/a
- **principle**: Internal consistency of a module's own documentation.
- **why it matters here**: `error.rs`'s header says it "stays HTTP-free" and "deliberately does **not**
  own the `axum::response::IntoResponse` implementation", but the same file imports axum and
  implements `impl IntoResponse for ServerError` (L216), and `api/mod.rs:13-15` states the impl "lives
  alongside the error enum in `crate::error` (so `error.rs` owns the full error seam)". The code and
  `api/mod.rs` agree; the `error.rs` header is the stale one. **Pre-existing** — the `IntoResponse`
  impl and this doc are context lines, not introduced by #113; the PR's only `error.rs` additions are
  the `Unavailable` variant, added cleanly. I raise it only because #113 edits this exact module-doc
  block (to add the `Unavailable` mapping row), so correcting the contradiction was within reach.
- **confidence**: verified
- **what would satisfy me**: Update the `error.rs` header to say the module owns the full error seam
  including `IntoResponse` (matching `api/mod.rs` and the code). Optional, opportunistic.

### CQ-06 — Mild plain-voice tell: "truthful/genuinely/truthfully" moral-tone adjectives cluster on the health/confirmation comments
- **severity**: nit
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/repository/postgres.rs:1578,1580` and
  `crates/chirp-server/src/repository/in_memory.rs:527,927,1802` @ 09fa453
- **acceptance-criterion / design ref**: BAR / plain-voice bar (per the brief and `_GLOBAL.md`)
- **principle**: Avoid gluing moral adjectives ("truthful", "genuinely", "honest") to artifacts that
  cannot hold them; a health check reports a state, it is not "truthful".
- **why it matters here**: "truthful durable-store health", "genuinely, truthfully healthy", "a
  truthful result … not a placeholder" read as the moral-adjective tell the plain-voice bar names.
  The density is low and the surrounding prose is otherwise plain and precise, so this is a light nit,
  not a pattern that pervades the file — but the brief asks that shipped comments meet the same bar as
  the review. (These comments are internal to the Rust source, not posted to GitHub, so they do not
  touch the posted-prose identities — raising only as craftsmanship.)
- **confidence**: verified
- **what would satisfy me**: Reword to the behaviour — e.g. "`store_health` round-trips the live pool
  and reports the real reachability state" — dropping "truthful"/"genuinely".

## Concern sub-verdict
- **NON-BLOCKING-ONLY**
- The persistence layer is well-crafted — object-safe additive seam, a correct central durability
  primitive, a single fail-safe error-mapping point, panic-free parameterized production paths, and
  two consistent backings. No code-quality defect blocks landing on its own. The findings are a
  documentation-integrity pattern that materially misdescribes the implementation (CQ-01/CQ-04), one
  feature-gating doc leak that may bear on the separately-owned `doc` blocker (CQ-02, deferred to
  `SUBTASK_ci_doc_diagnosis`), an unused abstraction (CQ-03), and two nits (CQ-05 pre-existing, CQ-06
  plain-voice).
