# Task: Implement the `chirp-types` crate

## Task Specification

**Slug**: SUBTASK_implement_crate
**Task Kind**: standard
**Status**: Pending
**Dependencies**: none

### Objective

Author `crates/chirp-types` in full — the coherent, stable, serde-serializable shared type surface
(domain model + client↔server API-contract DTOs) that both the future server and frontend import —
make it build and its tests pass locally, and commit it to the `work/chirp-types` branch in the
isolated clone.

### Context

This task is the implementation spoke of the `chirp-types` subtree (see `../_GLOBAL.md` and the
frozen conventions in `../contracts/_MANIFEST.yaml`). A sibling verification gate
(`SUBTASK_synthesis_gate`) runs AFTER you and depends on your output: it builds the whole workspace,
runs the quality gates, pushes the branch, and opens the PR. You are responsible for producing a
crate that is genuinely ready for that gate — do not push the branch or open the PR yourself; that
is the gate's job.

**Dependents**: `SUBTASK_synthesis_gate`.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Objective, scope, constraints |
| Contract | `../contracts/_MANIFEST.yaml` | Frozen conventions (clone path, branch, crate path/name, dependency policy) — READ-ONLY |
| Repository | `Nousix-LLC/nswe-demo` | Base `main`; read root `Cargo.toml` + `crates/ferric` for edition/lint/style conventions to match |

`gh` is authenticated on this host; `git`, `cargo`, `rustup` are available.

---

## What to produce (scope, not a runbook)

This is a single coherent responsibility — authoring one crate whose entire value is a well-designed,
internally consistent type surface. Treat it as one artifact; the pieces below are facets of that one
surface, not separable deliverables:

- **Crate scaffolding**: a new workspace member `crates/chirp-types` (plain library crate, native
  host target, edition 2021+), added to the root workspace members, matching the conventions already
  on `main`.
- **Domain model**: coherent types for `User`, `Chirp`/`Post`, `Timeline`, `Follow`, `Like` — ids,
  timestamps, relationships, with documented invariants and sensible field types.
- **API-contract DTOs**: the request/response types forming the REST contract (create-chirp,
  timeline query, follow/unfollow, like/unlike, and auth/user DTOs as needed), designed as the single
  source of truth both server and frontend import.
- **Serde**: every domain + DTO type derives `Serialize`/`Deserialize` with stable, explicit JSON
  field naming (document the casing/`rename` convention); round-trip stable.
- **Tests**: native `cargo test` unit tests covering serde round-trips and any invariants/constructors
  (no browser/network dependence).
- **Docs**: rustdoc on all public items, and a short `crates/chirp-types/README.md` describing the
  contract and how server + frontend consume it.

Work entirely inside the single isolated clone at the `clone_dir` named in the contract; create it
with `gh repo clone`. Commit your work to branch `work/chirp-types`. Ensure `cargo build -p
chirp-types` and `cargo test -p chirp-types` pass locally before you finish — but leave the
authoritative workspace-wide build, fmt/clippy gates, branch push, and PR to the synthesis gate.

> The atomic-vs-decompose decision for this task is yours to make at dispatch per the kernel. If, on
> your own reading, the type surface genuinely spans several independent responsibilities, evaluate
> accordingly — do not treat this brief as pre-deciding it.

### Declared output

| Attribute | Value |
|-----------|-------|
| Primary declared output | `SUBTASK_implement_crate/IMPLEMENTATION_NOTES.md` |
| Substantive product | `crates/chirp-types/**` committed to `work/chirp-types` in the clone |

`IMPLEMENTATION_NOTES.md` is the handoff to the gate: summarize the public type surface and the
serde field-naming convention, the local `cargo build -p chirp-types` / `cargo test -p chirp-types`
results, the exact clone path and branch name, any dependency added (with justification), and any
design decisions or open questions.

---

## Suggested Methodology Files

Matched Domain-Mapping row (verbatim): **"Writing new code" → Primary: Core; Supporting: Code
Quality"**, specialized here by the Rust and Architecture rows (**"Writing Rust code" → Rust | Core,
Code Quality**; **"Authoring a design note" → Architecture**). Load bundles on-demand via
`engine_load_methodology { name: "<bundle>" }`.

- Bundle `rust`:
  - `rust/Rust_Type_System_Methodology.md` — designing the domain/DTO type surface.
  - `rust/Rust_Trait_Design_Methodology.md` — derive conventions, trait bounds on public types.
  - `rust/Rust_Error_Handling_Methodology.md` — constructor/validation error types (no panics in a library).
  - `rust/Rust_Cargo_Ecosystem_Methodology.md` — workspace-member layout, feature/dependency hygiene.
  - `rust/Rust_Testing_Methodology.md` — native unit tests, serde round-trip test patterns.
- Bundle `core`:
  - `core/BestPractices_Coding_Standards_Methodology.md` — naming, module layout, rustdoc discipline.
  - `core/BestPractices_Error_Handling_Methodology.md` — library error surface.
  - `core/CodeManagement_Commit_Practices_Methodology.md` — clean commits on `work/chirp-types`.
- Bundle `architecture`:
  - `architecture/Architecture_API_Design_Methodology.md` — this is a client↔server contract; design the DTO surface deliberately and for stability.
  - `architecture/Architecture_Data_Modeling_Methodology.md` — entity/relationship modeling for User/Chirp/Timeline/Follow/Like.
  - `architecture/Architecture_Design_Notes_Methodology.md` — capture the contract rationale in the README/notes.

*The above are the parent's flagged methodologies based on the task type. You SHOULD load these as a
starting point but are the final judge of what your work requires — load fewer if some are clearly
inapplicable; load more if your own reading of the brief reveals additional methodology surface the
parent did not anticipate.*

## Inherited Constraints

- Crate name **`chirp-types`** at `crates/chirp-types`; edition 2021+; stable toolchain.
- **Dependency-light**: serde + serde_json; a uuid/time crate ONLY if justified; **no** server or
  wasm dependencies (both server and frontend depend on this crate).
- Match the conventions already on `main` (read root `Cargo.toml` + `crates/ferric` for edition,
  lints, style before writing).
- All repo work in the single isolated clone at the contract's `clone_dir`; never reuse another
  process's clone.
- **Never** commit to or force-push `main`; commit only to `work/chirp-types`. No commit-attribution
  trailers.

## Out-of-Scope Methodologies

- Do NOT load the `synthesis` bundle — verification/gate work belongs to `SUBTASK_synthesis_gate`,
  not here.
- Do NOT load `decomposition/` content — that is decomposer-side; you are implementing.
- No wasm/frontend or server/axum methodology — you build only the shared types now.

## Success Criteria

- [ ] `crates/chirp-types` exists as a workspace member and `cargo build -p chirp-types` succeeds in the clone.
- [ ] Domain + DTO types present, coherent, documented, with explicit serde field naming; `cargo test -p chirp-types` passes (serde round-trips + invariants).
- [ ] `README.md` present; rustdoc on all public items.
- [ ] Work committed to `work/chirp-types` in the clone at the contract's `clone_dir`.
- [ ] `IMPLEMENTATION_NOTES.md` written with the type surface, local build/test results, branch + clone path, and any dependency justifications.
