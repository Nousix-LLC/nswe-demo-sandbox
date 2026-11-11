# SYNTHESIS — remediate-epic-persist-r1b

**PR:** Nousix-LLC/nswe-demo#113 (`work/epic-persist` → `main`)
**Verdict:** PASS — blocker cleared; all required CI checks green

---

## CI-01: `doc` blocker — CLEARED

The required `doc` check (`cargo doc --workspace --no-deps --locked` under
`RUSTDOCFLAGS=-D warnings`) is **green** on commit `a129e2b` (current HEAD of
`work/epic-persist`).

**What failed (original blocker):** The public `export_user_data` doc comment in
`crates/chirp-server/src/repository/in_memory.rs` (line 787 at the pinned head `09fa453`)
carried the intra-doc link `` [`ExportDocument`](super::export::ExportDocument) ``. Because
`ExportDocument` lives in a private module, `rustdoc::private_intra_doc_links` treated this as a
hard error under `-D warnings`. This blocked the `doc` CI check entirely.

**Fix delivered in two commits on `work/epic-persist`:**

1. **`db1a5d6`** — removed the primary blocker link and corrected 12 additional doc hazards
   identified in issue #118 (stale "scaffold stub" prose, internal work-breakdown vocabulary,
   and several explicit link paths introduced while fixing those hazards).

2. **`a129e2b`** — dropped four unresolvable explicit link paths that `db1a5d6` introduced in
   `lib.rs`, `repository/mod.rs` (×2), and `repository/in_memory.rs`. Each path referred to
   `crate::repository::postgres::PostgresRepository` (or the relative form), which lives behind
   `#[cfg(feature = "postgres")]`. With the feature disabled (the default `cargo doc` build),
   rustdoc cannot resolve these paths and emits `rustdoc::broken-intra-doc-links` errors. The fix
   replaces them with plain code spans (`PostgresRepository`), which convey the same information
   without requiring the type to be in scope.

**Verification (local):** `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps --locked`
ran to completion with zero errors or warnings after `a129e2b`. No further `-D warnings` error
surfaced behind the original blocker.

**Verification (CI):** GitHub Actions run on `a129e2b` — all five required checks green:
`doc` pass, `clippy` pass, `fmt` pass, `test` pass, `wasm` pass.

---

## Issue #118 documentation hazards — RESOLVED

All hazards named in #118 were addressed in `db1a5d6` + `a129e2b`:

- **CI-01**: Private intra-doc link on `export_user_data` → removed. ✓
- **H-02**: Feature-gated intra-doc link in `export.rs` → replaced with code span. ✓
- **H-03**: Stale "compiling scaffold (EPIC-PERSIST, #66)" in `postgres.rs` module title → removed. ✓
- **H-04**: "# Scaffold boundary" section describing all methods as skeleton stubs → replaced with
  accurate "# Implementation" section. ✓
- **H-05**: "Unlike the other scaffold methods this is not a stub" on `store_health` → removed. ✓
- **H-06**: Stale "not a placeholder" contrast in `in_memory.rs` → removed. ✓
- **H-07/H-08**: Hypothetical SQLite sentence in `in_memory.rs` / `mod.rs` → replaced with
  factual two-backing descriptions. ✓
- **H-09/H-14**: "Release-bar additions" paragraph in `mod.rs` calling `InMemoryRepository` an
  error-contract placeholder → replaced with accurate present-tense prose. ✓
- **H-10**: Layering diagram in `lib.rs` showing only `InMemoryRepository` → updated to show
  both implementors. ✓
- **H-11**: `error.rs` claiming the module does not own `IntoResponse` → corrected (it does). ✓
- **H-12**: Internal build-stage vocabulary in `DEFAULT_MAX_CONNECTIONS` doc → removed. ✓
- **H-13**: `SUBTASK_*` workstream identifiers in `pub mod mapping` doc → removed. ✓
- **Feature-gating links from `lib.rs`, `mod.rs`, `in_memory.rs`** → replaced with plain code
  spans (this was the class of issue introduced by `db1a5d6` and corrected in `a129e2b`). ✓

All changes are strictly documentation/comments. No logic, schema, migration, `ChirpRepository`
seam, test, or wiring was touched in either commit.

---

## Acceptance criteria check

### #65/#66/#67 still met — no behavioural regression

The two commits are documentation-only (zero code changes). The `test` CI check passes,
confirming no test regression. The `ChirpRepository` seam, the durable store implementation,
the versioned migrations, and the retention/fail-closed behaviour are all unchanged.

Specifically:
- **#65** (durable store behind `ChirpRepository` seam, full capability set): seam unchanged; ✓
- **#66** (versioned migrations, accurate domain model): migrations unchanged; ✓
- **#67** (fail-closed retention, capacity, durability proofs): retention behaviour unchanged;
  durability drill test (`09fa453`) unchanged; ✓

### Currently-green checks — no regression

| Check | Status on `a129e2b` |
|-------|---------------------|
| `doc` | ✅ pass |
| `clippy` | ✅ pass |
| `fmt` | ✅ pass |
| `test` | ✅ pass |
| `wasm` | ✅ pass |

### #64 stays open

Issue #64 (credential Secret + live durable image digest pin) remains open. Nothing in these
commits closes it or touches the activation path.

---

## PR state

- PR #113 is **open**, `work/epic-persist` → `main`.
- HEAD is `a129e2b` (fast-forward onto the remote's `db1a5d6`; no force-push).
- Merge state: no longer blocked by a failing required check. All five required checks are green.
- The PR was not merged (as required; the DAG never merges its own PR).
- The `blocked` label was removed to reflect the cleared CI state.
