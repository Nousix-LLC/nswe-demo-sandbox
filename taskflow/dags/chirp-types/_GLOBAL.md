# chirp-types — shared domain model + client↔server API contract (subtree hub)

## Project Context

**Status**: Active (decomposed; awaiting subtree resolution)

This subtree delivers **work-item #7** of the `Nousix-LLC/nswe-demo` engagement: the
`crates/chirp-types` crate — the shared domain model and the client↔server API contract for the
`chirp` Twitter-style app. It is dependency-light (serde only, plus serde_json and, if justified,
a uuid/time crate) and is imported by BOTH the future `chirp-server` (#8, axum) and
`chirp-frontend` (#9, ferric SPA). It therefore fans out in parallel with the ferric framework
crates and is delivered as a PR into `main`.

### Objective

Produce a clean, coherent, well-documented, **stable** type surface — the single source of truth
both server and frontend compose against — and deliver it as a reviewed PR with a verification
verdict.

### Scope

**In scope:**
- A new workspace member crate `crates/chirp-types` (plain library crate; native host target; no
  wasm/browser dependence).
- Domain model: `User`, `Chirp`/`Post`, `Timeline`, `Follow`, `Like` (ids, timestamps,
  relationships, documented invariants).
- API-contract DTOs: request/response types for create-chirp, timeline query, follow/unfollow,
  like/unlike, and auth/user as needed.
- Serde on every type with stable, explicit JSON field naming; round-trip-stable.
- Native `cargo test` unit tests (serde round-trips + invariants/constructors).
- Quality: `cargo fmt --check` clean, `cargo clippy --all-targets -- -D warnings` clean, rustdoc
  on all public items, a short `crates/chirp-types/README.md`.
- Delivery: branch `work/chirp-types`, PR into `main` titled `chirp-types: shared domain model +
  API contract`, body ending `Closes #7`.

**Out of scope:** the server (#8), the frontend (#9), any wasm/browser code, any change to
`main` or to other crates beyond slotting the new member into the workspace.

### Success Criteria

- [ ] `crates/chirp-types` slots cleanly into the existing virtual workspace and compiles on the
      native host target.
- [ ] Domain + DTO types coherent, documented, serde round-trip-stable with explicit field naming.
- [ ] Native tests pass; `cargo fmt --check` and `cargo clippy --all-targets -- -D warnings` clean.
- [ ] README describes the contract and how server + frontend consume it.
- [ ] PR opened into `main`; `SYNTHESIS.md` at this workspace records a PASS/FAIL verdict with
      evidence and the PR URL.

---

## Constraints and Requirements

- **Crate identity**: name `chirp-types` at `crates/chirp-types`; edition 2021+; stable toolchain.
- **Dependency-light**: serde + serde_json; a uuid/time crate ONLY if justified; NO server/wasm deps.
- **Match `main` conventions**: read the root `Cargo.toml` + `crates/ferric` for edition, lints,
  and style before authoring.
- **Isolated clone**: all repo work happens in a single clone at `checkout/` under this workspace
  (`/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-types/checkout`). Do NOT reuse any
  other process's clone.
- **Never** commit to or force-push `main`. Local commits + push `work/chirp-types` + open the PR.
- No commit-attribution trailers.

---

## Input Specifications

| Source | Location | Purpose |
|--------|----------|---------|
| This hub | `_GLOBAL.md` | Shared context, constraints, contract pointer |
| Contract | `contracts/_MANIFEST.yaml` | Frozen shared conventions + the gate's assertion set |
| Repo | `Nousix-LLC/nswe-demo` (clone to `checkout/`) | Base `main` with the landed virtual workspace + `crates/ferric` |

---

## Subtree Methodology Posture

- **Dominant task type**: *Writing new code* (a shared contract crate) → primary bundle **`rust`**;
  plus **`core`** (coding standards, error handling, commit practices) and **`architecture`**
  (this is a deliberately-designed boundary both sides compose against). The terminal gate is a
  *Synthesizing/verifying a hub-and-spoke decomposition* task → **`synthesis`** (+ `code-review`).
- **Primary bundles in scope subtree-wide**: `rust`, `core`, `architecture` for implementation;
  `synthesis`, `code-review` for the gate. Descendants may assume these without re-justifying.
- **Cross-cutting bindings**: the type surface is a *stable public contract* — API-design and
  data-modeling discipline bind the whole crate even though only the implementation leaf loads them
  as primary; serde field-naming must be explicit and documented as a convention.
- **Suggestion, not prescription**: descendant agents retain final judgment over what they load.

## Subtree-Wide Constraints

- Crate name/path, edition, dependency-light rule, isolated-clone path, branch name, and
  never-touch-`main` are fixed above and in `contracts/_MANIFEST.yaml`; descendants conform and do
  not re-litigate them.

---

## Task Structure

### Overview

```
_GLOBAL.md (this hub)
├── contracts/_MANIFEST.yaml                 (frozen conventions + gate assertion set)
├── SUBTASK_implement_crate/_BRIEF.md        (author the whole crate; build+test+commit locally)
└── SUBTASK_synthesis_gate/_BRIEF.md         (verification gate; push + PR; SYNTHESIS.md verdict)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_implement_crate` | none | Author `crates/chirp-types` fully (domain + DTOs + serde + inline tests + rustdoc + README) in the `checkout/` clone; ensure it builds and tests pass locally; commit to branch `work/chirp-types`. | `SUBTASK_implement_crate/IMPLEMENTATION_NOTES.md` (handoff: type surface, local build/test status, branch + clone path) |
| `SUBTASK_synthesis_gate` | `SUBTASK_implement_crate` | Verification gate: run authoritative `cargo build --workspace` / `cargo test` / `fmt --check` / `clippy -D warnings` on the clone, push the branch, open the PR, and record the PASS/FAIL verdict. | `SYNTHESIS.md` (at this hub workspace — the fold location / observation seam) |

### Dependency Graph

```
SUBTASK_implement_crate ──► SUBTASK_synthesis_gate
```

---

## Contract

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` (a thin handoff/convention manifest)

The single cross-sibling edge (the gate consumes the implemented crate) is **serialized** by the
dependency, so the gate reads the real built clone rather than a mock — no interface freeze is
needed for the data itself. What the manifest DOES freeze, before any child runs, are the
*forced/stable* shared conventions both children must agree on (clone path, branch name, crate
path/name, workspace membership) plus the gate's **assertion set** — the build/test/fmt/clippy
checks, each with a runnable command. See `contracts/_MANIFEST.yaml`.

### Ownership (summary; authoritative in the manifest)

| Artifact | Owner |
|---|---|
| `checkout/` clone + `crates/chirp-types/**` source + `work/chirp-types` commits | `SUBTASK_implement_crate` |
| The PR into `main` + `SYNTHESIS.md` verdict | `SUBTASK_synthesis_gate` |

### Identities (the gate asserts these; no silent plug)

- [ ] `cargo build --workspace` succeeds (crate slots into the workspace).
- [ ] `cargo test` passes on the native host target.
- [ ] `cargo fmt --check` clean.
- [ ] `cargo clippy --all-targets -- -D warnings` clean.
- [ ] A PR into `main` exists with body ending `Closes #7`.

---

## Output Specifications

| Deliverable | Location | Description |
|-------------|----------|-------------|
| `chirp-types` crate | `checkout/crates/chirp-types/` (committed to `work/chirp-types`) | The shared domain model + API contract |
| Implementation handoff | `SUBTASK_implement_crate/IMPLEMENTATION_NOTES.md` | Type surface + local build/test status + branch/clone pointers |
| Verdict / fold record | `SYNTHESIS.md` (this workspace) | Build/test/fmt/clippy verdict, diff manifest, PR URL, PASS/FAIL |
