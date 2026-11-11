# Correction Inventory — PR #113 `doc` hazards
## Branch `work/epic-persist` · head `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`
## Schema version: 1

Survey scope: the `chirp-server` crate, all public `///` and `//!` doc comments.
CI command under analysis: `cargo doc --workspace --no-deps --locked` (default features, no `--features postgres`).

---

## Link hazards (classes 1 & 2) — break `cargo doc` under `-D warnings`

These two records are the only doc-link hazards visible under the default feature set that causes
the CI `doc` check to fail. rustdoc reports only the first failing crate; CI-01 is the current
failure. H-02 is the next error in queue — it fires once CI-01 is cleared.

---

### CI-01

```yaml
id: CI-01
file: crates/chirp-server/src/repository/in_memory.rs
anchor: "fn export_user_data (~L787)"
hazard_kind: public_to_private_link
current: >
  serialized through the shared [`ExportDocument`](super::export::ExportDocument) so the two
  backings produce byte-identical exports.
rework: >
  serialized through the shared `ExportDocument` so the two
  backings produce byte-identical exports.
criterion: CI-01
```

**Diagnosis.** The `export_user_data` method on `InMemoryRepository` is `pub` (it implements the
public `ChirpRepository` trait). Its doc comment links to `super::export::ExportDocument` via the
intra-doc path `super::export::ExportDocument`. The `export` module is declared `mod export;` (no
`pub`) in `crates/chirp-server/src/repository/mod.rs` — private. Under
`RUSTDOCFLAGS=-D warnings`, the `rustdoc::private_intra_doc_links` lint promotes this to a hard
error, which is the current CI `doc` failure.

**Fix.** Replace the intra-doc link `` [`ExportDocument`](super::export::ExportDocument) `` with
the plain code span `` `ExportDocument` ``. The prose remains accurate; the link target is removed.

---

### H-02

```yaml
id: H-02
file: crates/chirp-server/src/repository/export.rs
anchor: "module doc (~L7)"
hazard_kind: ungated_to_gated_link
current: >
  [`PostgresRepository`](crate::repository::postgres::PostgresRepository) and the retained
rework: >
  `PostgresRepository` and the retained
criterion: "#118"
```

**Diagnosis.** The `export` module is compiled unconditionally. Its module-level doc (`//!`) at
~L7 contains an intra-doc link to
`crate::repository::postgres::PostgresRepository`, which lives in `pub mod postgres;` — gated by
`#[cfg(feature = "postgres")]`. Under a default `cargo doc` (no `--features postgres`), the target
path does not resolve, producing a `rustdoc::broken_intra_doc_links` warning that becomes a hard
error under `-D warnings`. This is the next error that surfaces once CI-01 is fixed.

**Fix.** Replace `` [`PostgresRepository`](crate::repository::postgres::PostgresRepository) ``
with the plain code span `` `PostgresRepository` ``.

---

## Stale scaffold / placeholder docs (class 3) — #118

These records address public `///`/`//!` doc comments that describe fully-implemented methods or
the fully-implemented module as unimplemented stubs or scaffold placeholders. None of these break
`cargo doc` directly, but they satisfy the #118 acceptance criterion "persistence-layer public docs
are accurate (no implemented-as-stub/placeholder descriptions)."

---

### H-03

```yaml
id: H-03
file: crates/chirp-server/src/repository/postgres.rs
anchor: "module doc — title line (~L1)"
hazard_kind: stale_scaffold_doc
current: >
  The durable PostgreSQL backing for [`ChirpRepository`] — compiling scaffold (EPIC-PERSIST, #66).
rework: >
  The durable PostgreSQL backing for [`ChirpRepository`].
criterion: "#118"
```

**Diagnosis.** The first line of the module doc appends "— compiling scaffold (EPIC-PERSIST, #66)"
to the module description. All 24 capability methods have real durable implementations with
integration tests; the module is not a scaffold. The `EPIC-PERSIST` label and `#66` reference are
internal build-tracking vocabulary that does not belong in shipped documentation.

**Fix.** Remove " — compiling scaffold (EPIC-PERSIST, #66)" from the title sentence.

---

### H-04

```yaml
id: H-04
file: crates/chirp-server/src/repository/postgres.rs
anchor: "module doc — '# Scaffold boundary' section (~L9-27)"
hazard_kind: stale_scaffold_doc
current: |
  # Scaffold boundary

  This is the **foundation scaffold**, not the durable implementation. What it stands up:

  * a connection pool constructed from a connection string ([`PostgresRepository::connect`]);
  * a **versioned, inspectable schema** driven by [`sqlx`]'s embedded, forward-only migration
    runner (the `migrations/` directory, applied at startup) with a readable
    [schema-version surface](PostgresRepository::schema_version);
  * a truthful [`store_health`](PostgresRepository::store_health) that round-trips the live pool.

  What it deliberately does **not** do: the durable method **bodies**. Every
  [`ChirpRepository`] write/read below is a skeleton stub that returns
  [`ServerError::Internal`] — error-contract-consistent, so an operation whose durable behaviour is
  not yet built reports a **failed** action and NEVER falsely confirms success (the
  `confirmed_write_durable` identity). The real DDL, migration content, and method bodies are the
  downstream EPIC-PERSIST `SUBTASK_durable_impl` work; this scaffold only makes them compile
  against a live, migratable store.
rework: |
  # Implementation

  The module provides the full [`ChirpRepository`] capability set backed by a live PostgreSQL
  database:

  * a connection pool constructed from a connection string ([`PostgresRepository::connect`]);
  * a **versioned, inspectable schema** driven by [`sqlx`]'s embedded, forward-only migration
    runner (the `migrations/` directory, applied at startup) with a readable
    [schema-version surface](PostgresRepository::schema_version);
  * every [`ChirpRepository`] read and write method implemented as a durable SQL operation,
    returning only after the write has committed (`confirmed_write_durable`);
  * a truthful [`store_health`](PostgresRepository::store_health) that round-trips the live pool.
criterion: "#118"
```

**Diagnosis.** The "# Scaffold boundary" section describes the module as a "foundation scaffold"
whose "every write/read is a skeleton stub" with durable method bodies "downstream." All 24 methods
have real durable bodies with integration tests — this description is entirely false. The section
also contains the internal build labels `EPIC-PERSIST` and `SUBTASK_durable_impl` (see H-09 for the
same pattern in the internal-vocab class).

**Fix.** Replace the "# Scaffold boundary" section with an "# Implementation" section that
accurately describes the fully-implemented module.

---

### H-05

```yaml
id: H-05
file: crates/chirp-server/src/repository/postgres.rs
anchor: "fn store_health (~L1578)"
hazard_kind: stale_scaffold_doc
current: >
  Unlike the other scaffold methods this is **not** a stub — store reachability is exactly what
  the `store_health` capability (REQ-DOM-021) reports, and it is meaningful for the durable
  backing from day one.
rework: >
  Store reachability is exactly what the `store_health` capability (REQ-DOM-021) reports, and it
  is meaningful for the durable backing from day one.
criterion: "#118"
```

**Diagnosis.** The doc for `store_health` opens with "Unlike the other scaffold methods this is
**not** a stub", contrasting it with the other methods that were stubs at the time of writing.
Since all methods now have real durable implementations, the "unlike the other scaffold methods"
framing is both stale and misleading — it implies the other methods are still stubs.

**Fix.** Remove the contrast phrase "Unlike the other scaffold methods this is **not** a stub —";
the remainder accurately describes what the method does.

---

### H-06

```yaml
id: H-06
file: crates/chirp-server/src/repository/in_memory.rs
anchor: "fn store_health (~L927)"
hazard_kind: stale_scaffold_doc
current: >
  a truthful trivially-correct result, not a placeholder that masks unimplemented behaviour.
rework: >
  a truthful trivially-correct result.
criterion: "#118"
```

**Diagnosis.** The `store_health` doc on `InMemoryRepository` says its result is "not a
placeholder that masks unimplemented behaviour." This contrast referred to the time when the other
release-bar methods were placeholders. Since all in_memory methods are now fully implemented, the
"not a placeholder" qualifier references a state that no longer exists and misleads a reader about
the current state of the other methods.

**Fix.** Remove ", not a placeholder that masks unimplemented behaviour" from the sentence.

---

### H-07

```yaml
id: H-07
file: crates/chirp-server/src/repository/in_memory.rs
anchor: "module doc (~L5-7)"
hazard_kind: stale_scaffold_doc
current: >
  It is the demo's default backing; a persistent store (SQLite via
  `sqlx`, etc.) would be a second implementor of [`ChirpRepository`], never a replacement that the
  tests require.
rework: >
  It is the demo's default backing; the `postgres` feature adds [`PostgresRepository`] as the
  durable implementor without requiring the test suite to use a database.
criterion: "#118"
```

**Diagnosis.** The module doc presents a persistent store as a hypothetical future addition ("would
be a second implementor"). `PostgresRepository` already exists under the `postgres` feature flag.
The description is stale and misleads the reader about the current state of the codebase.

**Fix.** Update the sentence to describe the current state: the postgres feature provides
`PostgresRepository`; the in-memory backing remains the default and keeps the test suite
store-free.

---

### H-08

```yaml
id: H-08
file: crates/chirp-server/src/repository/mod.rs
anchor: "module doc — SQLite sentence (~L6-8)"
hazard_kind: stale_scaffold_doc
current: >
  a SQLite/`sqlx`
  backing could be added as a second implementor of this same trait, but is explicitly optional
  and is never required for `cargo test`.
rework: >
  the `postgres` feature provides [`PostgresRepository`] as the durable implementor; the default
  build uses [`InMemoryRepository`] so `cargo test` runs without a database.
criterion: "#118"
```

**Diagnosis.** The seam's module doc describes "a SQLite/`sqlx` backing" as a hypothetical future
addition. `PostgresRepository` already exists and is the durable implementor under the `postgres`
feature. The description is stale.

**Fix.** Replace the hypothetical sentence with a factual description of the current two-backing
architecture.

---

### H-09

```yaml
id: H-09
file: crates/chirp-server/src/repository/mod.rs
anchor: "module doc — 'Release-bar additions' paragraph (~L63-66)"
hazard_kind: stale_scaffold_doc
current: >
  These signatures fix the *surface*; the durable behaviour behind them is implemented downstream
  (the EPIC-PERSIST durable implementation). The retained [`InMemoryRepository`] satisfies them
  with error-contract-consistent placeholders (it never falsely confirms an unimplemented durable
  operation), so the store-free test suite keeps compiling and passing.
rework: >
  These signatures are fully implemented in both [`InMemoryRepository`] and
  [`PostgresRepository`]. The store-free test suite continues to use [`InMemoryRepository`] and
  requires no database.
criterion: "#118"
```

**Diagnosis.** This paragraph states the durable behaviour is "implemented downstream (the
EPIC-PERSIST durable implementation)" and that `InMemoryRepository` provides "error-contract-
consistent placeholders" for unimplemented durable operations. Both statements are false: all
methods are implemented in both repositories, and the in-memory methods are not placeholders. The
`EPIC-PERSIST` label is also internal build vocabulary (class 4, see H-10).

**Fix.** Replace the paragraph with a factual description of the current state.

---

### H-10

```yaml
id: H-10
file: crates/chirp-server/src/lib.rs
anchor: "module doc — layering section (~L10-22)"
hazard_kind: stale_scaffold_doc
current: |
  ```text
  transport (axum handlers, router, middleware)   ← api-layer spoke
      │
      ▼
  persistence (ChirpRepository trait)             ← this module tree
      │
      ▼
  InMemoryRepository (default backing, no DB)
  ```

  Persistence is abstracted behind the [`ChirpRepository`] trait so
  the server runs entirely in memory for the demo (the default [`InMemoryRepository`]) and could
  adopt a real database later by adding another implementor — without changing a single handler.
rework: |
  ```text
  transport (axum handlers, router, middleware)   ← api-layer spoke
      │
      ▼
  persistence (ChirpRepository trait)             ← this module tree
      │
      ├── InMemoryRepository  (default; no DB required)
      └── PostgresRepository  (postgres feature; durable backing)
  ```

  Persistence is abstracted behind the [`ChirpRepository`] trait: the default
  [`InMemoryRepository`] keeps all state in process (no database required), and the optional
  `postgres` feature selects [`PostgresRepository`] as the durable backing — without changing a
  single handler.
criterion: "#118"
```

**Diagnosis.** The layering diagram shows only `InMemoryRepository` as the backing and the
accompanying text says "could adopt a real database later by adding another implementor." Both are
stale: `PostgresRepository` already exists as the durable implementor under the `postgres` feature.
A reader of the crate docs would incorrectly conclude no durable store exists.

**Fix.** Update the diagram to show both implementors and the text to reflect the current state.

---

### H-11

```yaml
id: H-11
file: crates/chirp-server/src/error.rs
anchor: "module doc — '# Ownership of the error seam' section (~L9-17)"
hazard_kind: stale_scaffold_doc
current: >
  It deliberately does **not** own the
  `axum::response::IntoResponse` implementation or any HTTP-status mapping: that is the api-layer
  spoke's responsibility (it depends on `axum`; this layer stays HTTP-free). The bridge this module
  provides for that spoke is [`ServerError::code`] (the machine-readable category) and
  [`ServerError::into_api_error`] (the ready-to-serialize body); the api-layer maps
  [`ErrorCode`] → `axum::http::StatusCode` in its `IntoResponse`.
rework: >
  It owns the **enum definition**, its `IntoResponse` implementation (which maps each variant to
  the correct HTTP status via [`StatusCode`](axum::http::StatusCode)), and the translation into
  the wire types [`ApiError`] / [`ErrorCode`]. The bridge the transport layer consumes is
  [`ServerError::code`] (the machine-readable category) and
  [`ServerError::into_api_error`] (the ready-to-serialize body).
criterion: "#118"
```

**Diagnosis.** The module doc's "# Ownership of the error seam" section states this module
deliberately does **not** own the `IntoResponse` implementation — "this layer stays HTTP-free."
But `error.rs` imports `axum::response::{IntoResponse, Response}` and at ~L216 implements
`impl IntoResponse for ServerError`. The header is factually wrong: `error.rs` does own
`IntoResponse`. (This is pre-existing; the PR edits this block.)

**Fix.** Update the "# Ownership of the error seam" section to correctly state that the module
owns the `IntoResponse` implementation, and remove the "HTTP-free" claim.

---

## Internal build-breakdown vocabulary (class 4) — #118

These records address public `///`/`//!` doc comments that contain workstream labels, subtask
identifiers, or in-progress phrasing that resolve to nothing in the repository and describe a
build mid-flight when the build is complete.

---

### H-12

```yaml
id: H-12
file: crates/chirp-server/src/repository/postgres.rs
anchor: "const DEFAULT_MAX_CONNECTIONS (~L129)"
hazard_kind: internal_vocab
current: >
  A conservative default for the scaffold; connection-pool sizing is an operational concern the
  downstream operational-readiness work tunes (it may be made configurable alongside
  `DATABASE_URL`).
rework: >
  A conservative default for connection-pool sizing. This value can be made configurable via an
  environment variable alongside `DATABASE_URL` if operational tuning requires it.
criterion: "#118"
```

**Diagnosis.** The doc comment refers to "the scaffold" (stale — the module is not a scaffold) and
"downstream operational-readiness work" (internal build-stage vocabulary that resolves to nothing
in the repository). Both are internal build-narrative artifacts.

**Fix.** Replace with accurate present-tense prose: the value is a conservative default;
configurability is an operational option, not a future downstream stage.

---

### H-13

```yaml
id: H-13
file: crates/chirp-server/src/repository/postgres.rs
anchor: "pub mod mapping (~L2262)"
hazard_kind: internal_vocab
current: >
  Authored once by `SUBTASK_mapping_validation`; every later `SUBTASK_durable_impl` capability
  method reuses these entry points rather than re-deriving the conversion or re-implementing the
  boundary validation. See the module-level comment above for the three faces of the pattern and
  how it expresses each entity invariant at the durable boundary.
rework: >
  The `chirp-types` ↔ durable-row mapping and the domain-boundary validation entry points,
  authored once and reused by every capability method rather than re-derived per method. See the
  module-level comment above for the three faces of the pattern and how it expresses each entity
  invariant at the durable boundary.
criterion: "#118"
```

**Diagnosis.** The `///` doc comment on `pub mod mapping` opens with "Authored once by
`SUBTASK_mapping_validation`; every later `SUBTASK_durable_impl` capability method…". Both
`SUBTASK_mapping_validation` and `SUBTASK_durable_impl` are internal build-workstream identifiers
that resolve to nothing in the repository. They are internal build-narrative artifacts that
describe the implementation sequence, not the code's current state.

**Fix.** Remove the SUBTASK references and replace with factual present-tense description of what
the module provides and how it is used.

---

### H-14

```yaml
id: H-14
file: crates/chirp-server/src/repository/mod.rs
anchor: "module doc — 'Release-bar additions' paragraph EPIC-PERSIST label (~L63)"
hazard_kind: internal_vocab
current: >
  the durable behaviour behind them is implemented downstream
  (the EPIC-PERSIST durable implementation).
rework: >
  (covered by H-09 rework — same paragraph; fix in one edit)
criterion: "#118"
```

**Note.** This record identifies the `EPIC-PERSIST` label embedded in the same paragraph as H-09.
The fixes for H-09 and H-14 are combined: applying the H-09 rework removes the EPIC-PERSIST label
in one edit. This record exists for coverage traceability; **apply_fixes should apply one edit for
the H-09/H-14 location**.

---

## Summary

| id | file | anchor | hazard_kind | criterion |
|----|------|--------|-------------|-----------|
| CI-01 | `crates/chirp-server/src/repository/in_memory.rs` | `fn export_user_data (~L787)` | `public_to_private_link` | CI-01 |
| H-02 | `crates/chirp-server/src/repository/export.rs` | `module doc (~L7)` | `ungated_to_gated_link` | #118 |
| H-03 | `crates/chirp-server/src/repository/postgres.rs` | `module doc title (~L1)` | `stale_scaffold_doc` | #118 |
| H-04 | `crates/chirp-server/src/repository/postgres.rs` | `module doc "# Scaffold boundary" section (~L9-27)` | `stale_scaffold_doc` | #118 |
| H-05 | `crates/chirp-server/src/repository/postgres.rs` | `fn store_health (~L1578)` | `stale_scaffold_doc` | #118 |
| H-06 | `crates/chirp-server/src/repository/in_memory.rs` | `fn store_health (~L927)` | `stale_scaffold_doc` | #118 |
| H-07 | `crates/chirp-server/src/repository/in_memory.rs` | `module doc SQLite sentence (~L5-7)` | `stale_scaffold_doc` | #118 |
| H-08 | `crates/chirp-server/src/repository/mod.rs` | `module doc SQLite sentence (~L6-8)` | `stale_scaffold_doc` | #118 |
| H-09 | `crates/chirp-server/src/repository/mod.rs` | `module doc "Release-bar additions" paragraph (~L63-66)` | `stale_scaffold_doc` | #118 |
| H-10 | `crates/chirp-server/src/lib.rs` | `module doc layering section (~L10-22)` | `stale_scaffold_doc` | #118 |
| H-11 | `crates/chirp-server/src/error.rs` | `module doc "# Ownership of the error seam" section (~L9-17)` | `stale_scaffold_doc` | #118 |
| H-12 | `crates/chirp-server/src/repository/postgres.rs` | `const DEFAULT_MAX_CONNECTIONS (~L129)` | `internal_vocab` | #118 |
| H-13 | `crates/chirp-server/src/repository/postgres.rs` | `pub mod mapping (~L2262)` | `internal_vocab` | #118 |
| H-14 | `crates/chirp-server/src/repository/mod.rs` | `module doc EPIC-PERSIST label (~L63)` | `internal_vocab` | #118 |

**CI-blocking hazards**: CI-01 (current failure), H-02 (next in queue once CI-01 is fixed).
**#118 accuracy hazards**: H-03 through H-14 (none break `cargo doc` but all produce inaccurate public documentation that violates the #118 acceptance criteria).

**Completeness note.** `cargo doc --workspace --no-deps --locked` (default features) does not
compile the `postgres`-gated module. Two link hazards exist in `postgres.rs` doc comments visible
only under `--features postgres` (the `export::ExportDocument` link at ~L1334 and the
`SUBTASK_*` references in module-level prose), but they do not affect the CI `doc` check and are
addressed as prose fixes in H-04 and H-13 above.
