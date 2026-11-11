# Task: Scaffold `chirp-server` + the repository (persistence) layer

## Task Specification

**Slug**: SUBTASK_scaffold_and_repository
**Task Kind**: standard
**Status**: Pending

### Objective

Stand up the `crates/chirp-server` crate in an isolated clone and deliver its **persistence layer**:
the `ChirpRepository` trait (the seam the rest of the server composes against) plus its default
**in-memory implementation**, with unit tests — committed to `work/chirp-server`.

### Context

This is the **precursor stage** of the chirp-server pipeline (work-item #8). You create the clone and
the crate skeleton that the two downstream spokes (`SUBTASK_api_layer`, then
`SUBTASK_integration_tests_and_docs`) build on; you own the repository-trait seam and the server error
enum. Read this subtree's hub `_GLOBAL.md` and the frozen `contracts/_MANIFEST.yaml` (the clone path,
branch, crate id, module-layout skeleton, the repository-trait **capability seam**, and the
**error-mapping table**) — they bind you.

**Dependencies**: none (you are first).
**Dependents**: `SUBTASK_api_layer` (reads your committed trait + error enum + in-memory impl).

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, success criteria |
| Contract | `../contracts/_MANIFEST.yaml` | Clone path, branch, crate id, module layout, repository capability seam, error-mapping table |
| Wire contract | `crates/chirp-types` on `main` (in your clone) | The domain entities + DTOs your trait signatures are expressed in terms of (import; never re-declare) |
| Repo | `Nousix-LLC/nswe-demo` | Clone to the contract's `clone_path` with `gh repo clone` |

Before authoring, read the root `Cargo.toml` and the landed `crates/chirp-types` source in your clone so
the new crate matches the workspace's edition, lints, and style, and so your trait signatures use the
real `chirp-types` types.

---

## Process / Approach

This is the data layer; keep it free of HTTP/axum concerns (those belong to the api_layer spoke). In broad strokes:
clone the repo and cut the branch; scaffold the member crate (manifest + lib/bin skeleton + workspace entry);
define the `ChirpRepository` trait covering the capability set in the contract seam, expressed over `chirp-types`
types; define the `ServerError` enum matching the contract's error-mapping table (you own the enum; the api_layer
owns its `IntoResponse`); implement the in-memory backing (maintaining denormalized counts and the documented
`chirp-types` invariants); and unit-test the impl against the trait. Build + test locally, then commit. The exact
trait signatures, module names, and concurrency choice (sync-behind-`Mutex` vs `async`) are YOUR design calls —
document them. Leave how you internally structure this to your own judgment, and re-run your own decompose-evaluation:
if the trait + in-memory impl + unit tests genuinely prove to be more than one responsibility for one invocation,
decompose further rather than pushing through.

### Methodology

Apply the suggested methodology below; you are the final judge of what you load.

---

## Output Specification

### Primary Output (handoff)

| Attribute | Value |
|-----------|-------|
| Filename | `IMPLEMENTATION_NOTES.md` |
| Location | this workspace (`SUBTASK_scaffold_and_repository/`) |

Record: the `ChirpRepository` trait signature (final), the `ServerError` enum variants and how they map to the
error table, the crate module layout, the concurrency choice + rationale, the clone path + branch, and the local
`cargo build`/`cargo test` status. This is the input the api_layer spoke reads.

### Code output

The scaffolded `crates/chirp-server` (manifest + workspace entry + lib skeleton + `repository/**` + `error.rs`
enum) committed to `work/chirp-server` in the shared clone.

---

## Success Criteria

- [ ] Clone exists at the contract's `clone_path`; branch `work/chirp-server` created off `main`.
- [ ] `crates/chirp-server` is a workspace member; `cargo build -p chirp-server` succeeds.
- [ ] `ChirpRepository` trait covers every operation in the contract's `repository_seam`, typed over `chirp-types`.
- [ ] `ServerError` enum exists and lines up with the contract's `error_mapping` table (api_layer will add `IntoResponse`).
- [ ] In-memory impl maintains denormalized counts + the documented invariants; repository unit tests pass (no DB).
- [ ] Work committed to `work/chirp-server`; `IMPLEMENTATION_NOTES.md` written.

---

## Suggested Methodology Files

Matched Domain-Mapping row: **Writing Rust code → primary `rust`; supporting `core`, `code-quality`**; plus
**Designing systems / architecture → `architecture`** for the trait boundary. Load the bundle IDs on demand:

- `rust` — `rust/Rust_Trait_Design_Methodology.md` (the repository trait as the persistence seam — object-safe vs generic, async-in-trait choice), `rust/Rust_Error_Handling_Methodology.md` (the `ServerError` enum as error-as-value), `rust/Rust_Ownership_Borrowing_Methodology.md` + `rust/Rust_Concurrency_Methodology.md` (shared in-memory state behind `Mutex`/`RwLock` vs async).
- `core` — `core/BestPractices_Coding_Standards_Methodology.md`, `core/BestPractices_Error_Handling_Methodology.md`, `core/CodeManagement_Commit_Practices_Methodology.md` (clean local commit on the branch).
- `architecture` — `architecture/Architecture_Dependency_Management_Methodology.md` (the repository boundary that keeps persistence swappable; why transport does not leak into the data layer).

These are the parent's flagged methodologies based on the task type. Load them as a starting point but you are the
final judge of what your work requires — load fewer if some are clearly inapplicable, more if your reading reveals
additional surface.

## Inherited Constraints

- Crate `chirp-server` at `crates/chirp-server`; **path dependency on `chirp-types`**; edition 2021 / rust 1.82 / stable.
- Inherit workspace lints (`[lints] workspace = true`) AND keep `cargo clippy --all-targets -- -D warnings` clean.
- **In-memory repository is the default**; the server + tests MUST run with no database. SQLite/`sqlx` is optional + documented only.
- ALL work in the ONE shared clone at the contract's `clone_path`; do NOT reuse another process's clone.
- Never commit to / force-push `main`; no commit-attribution trailers.

## Out-of-Scope Methodologies

- Do NOT build axum handlers, routing, `IntoResponse`, static serving, the health endpoint, `tracing`, or `main.rs` —
  those are `SUBTASK_api_layer`'s. Keep this layer HTTP-free.
- Do NOT write the end-to-end API integration tests or the README — those are `SUBTASK_integration_tests_and_docs`'s.
  (Repository-level unit tests belong here; API integration tests do not.)
