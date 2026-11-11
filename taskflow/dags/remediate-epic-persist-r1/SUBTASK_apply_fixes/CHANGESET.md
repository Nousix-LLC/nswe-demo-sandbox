# Changeset — doc corrections applied to `work/epic-persist`

**Branch**: `Nousix-LLC/nswe-demo` `work/epic-persist`
**Commit**: `e63e607` (`docs(chirp-server): fix doc-link errors and stale scaffold vocabulary (#118)`)
**Prior head**: `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`

---

## Corrections applied

| id | file (repo-relative) | doc item | change |
|----|----------------------|----------|--------|
| CI-01 | `crates/chirp-server/src/repository/in_memory.rs` | `fn export_user_data` doc (~L787) | Replaced `` [`ExportDocument`](super::export::ExportDocument) `` with `` `ExportDocument` `` — removes public→private intra-doc link. |
| H-02 | `crates/chirp-server/src/repository/export.rs` | module doc (~L7) | Replaced `` [`PostgresRepository`](crate::repository::postgres::PostgresRepository) `` with `` `PostgresRepository` `` — removes ungated→gated intra-doc link. |
| H-03 | `crates/chirp-server/src/repository/postgres.rs` | module doc title (~L1) | Removed ` — compiling scaffold (EPIC-PERSIST, #66)` from the title line. |
| H-04 | `crates/chirp-server/src/repository/postgres.rs` | module doc `# Scaffold boundary` section (~L9-25) | Replaced with `# Implementation` section accurately describing the fully-implemented module. |
| H-05 | `crates/chirp-server/src/repository/postgres.rs` | `fn store_health` doc (~L1580) | Removed `Unlike the other scaffold methods this is **not** a stub — ` prefix. |
| H-06 | `crates/chirp-server/src/repository/in_memory.rs` | `fn store_health` doc (~L927) | Removed `, not a placeholder that masks unimplemented behaviour` trailing clause. |
| H-07 | `crates/chirp-server/src/repository/in_memory.rs` | module doc SQLite sentence (~L5-7) | Replaced hypothetical SQLite-backing sentence with present-tense description of the `postgres` feature providing `PostgresRepository`. |
| H-08 | `crates/chirp-server/src/repository/mod.rs` | module doc SQLite sentence (~L6-8) | Replaced hypothetical SQLite/`sqlx` sentence with factual two-backing description referencing `PostgresRepository`. |
| H-09 / H-14 | `crates/chirp-server/src/repository/mod.rs` | module doc `Release-bar additions` paragraph (~L63-66) | Combined edit: replaced paragraph stating durable behaviour is "implemented downstream (the EPIC-PERSIST durable implementation)" and that `InMemoryRepository` provides error-contract-consistent placeholders, with accurate present-tense prose that all methods are fully implemented and the test suite requires no database. The `EPIC-PERSIST` label (H-14) was removed as part of this single edit. |
| H-10 | `crates/chirp-server/src/lib.rs` | module doc layering section (~L10-22) | Updated ASCII diagram to show both `InMemoryRepository` and `PostgresRepository`, and updated prose to reflect both implementors exist today. |
| H-11 | `crates/chirp-server/src/error.rs` | module doc `# Ownership of the error seam` section (~L10-17) | Corrected false claim that the module does not own `IntoResponse`; updated to state it owns the enum definition, `IntoResponse`, and wire-type translation. |
| H-12 | `crates/chirp-server/src/repository/postgres.rs` | `const DEFAULT_MAX_CONNECTIONS` doc (~L128-130) | Removed "the scaffold" and "downstream operational-readiness work" build-stage vocabulary; replaced with present-tense operational description. |
| H-13 | `crates/chirp-server/src/repository/postgres.rs` | `pub mod mapping` doc (~L2262-2267) | Removed `SUBTASK_mapping_validation` and `SUBTASK_durable_impl` workstream identifiers; replaced with factual description of what the module provides. |

---

## Scope assertion

All 13 inventory records (CI-01, H-02 through H-14 with H-09/H-14 as a single combined edit) are
accounted for. The diff is strictly documentation: doc comment text, intra-doc links, and module
doc (`//!`) blocks. No logic, schema, migration, `ChirpRepository` seam, or wiring was touched.
