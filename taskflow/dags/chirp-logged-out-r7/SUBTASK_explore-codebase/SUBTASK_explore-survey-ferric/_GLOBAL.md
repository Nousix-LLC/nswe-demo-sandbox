# Ferric Framework Survey — Subtree Hub

## Project Context

**Status**: Active
**Parent task**: SUBTASK_explore-survey-ferric (Ferric Framework Primitives Survey)

### Objective

Survey `crates/ferric/` in `Nousix-LLC/nswe-demo` at `main` (commit `cb1ced3`) and produce `ferric-survey.md` documenting the async data-fetching primitives, component patterns, SSR/hydration support, and router API introduced by PRs #193, #203, and #228. The output tells the downstream frontend task (SUBTASK_frontend-ui) which Ferric APIs are available for loading/error/empty/end-of-list states.

### Scope

**In Scope:**
- Reading `crates/ferric/` source (exploration only — no code changes)
- Documenting public API: type signatures, state models, usage patterns
- Identifying gaps or limitations for the frontend task
- Producing `ferric-survey.md` covering all 6 sections from the parent brief

**Out of Scope:**
- Code changes to any crate
- Backend crate documentation (deferred to survey-backend)
- Testing methodology documentation

### Success Criteria

- [ ] Async resource primitives documented with Rust type signatures
- [ ] Router API documented (route declaration and navigation)
- [ ] SSR + hydration API documented with Axum integration point
- [ ] Four-state component pattern described in enough detail for SUBTASK_frontend-ui
- [ ] `ferric-survey.md` written at this workspace (the fold location)

---

## Constraints

### Inherited Constraints (from parent)
- Exploration only — no code changes to `crates/ferric/` or any other crate
- Repository: `Nousix-LLC/nswe-demo`; codebase on `main` at `cb1ced3`
- No host paths, internal addresses, or taskflow references in output
- Use `gh api` or SSH to the build server to access the codebase

### Technical Constraints
- Rust + WASM target; understand wasm-bindgen / web-sys surface when reading internals
- Three PRs merged to main at `cb1ced3`: #193 (async resources + form/event binding), #203 (router), #228 (SSR + hydration + Axum integration)

---

## Input Specifications

| Source | Location | Description |
|--------|----------|-------------|
| Ferric crate | `crates/ferric/` in `Nousix-LLC/nswe-demo` | Async resource primitives, router, SSR, hydration APIs |
| Crate metadata | `crates/ferric/Cargo.toml` | Feature flags, dependencies, public API surface |
| Crate entry | `crates/ferric/src/lib.rs` | Re-exported public API surface |

---

## Subtree Methodology Posture

**Dominant task type**: "Building a UI framework / framework primitive (signals, fine-grained reactivity vs virtual DOM, SSR + hydration)" → Framework Design + Rust + Frontend

**Primary bundles across this subtree**:
- `framework-design` (Framework Design bundle — UI reactivity & rendering internals)
- `rust` (Rust bundle — WebAssembly browser bindings, library API)

**Cross-cutting binding for all spokes**: Each spoke must document APIs using Rust syntax. Type signatures MUST be Rust-formatted. The synthesis task provides the final document; spokes provide focused notes per PR area.

---

## Subtree-Wide Constraints

- All spokes read from the SAME source: `crates/ferric/` in the repo
- No code changes whatsoever
- Each spoke documents ONE PR area; the synthesis integrates all three plus writes the holistic sections (crate structure, component pattern, gaps)
- Use `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/...` or SSH to access the code

---

## Task Structure

```
SUBTASK_explore-survey-ferric/ (this workspace)
├── _GLOBAL.md                                      (this file — subtree hub)
├── contracts/
│   ├── _MANIFEST.yaml                              (ownership + identities)
│   └── notes-schema.yaml                           (required sections in each notes file)
├── SUBTASK_ferric-async-survey/
│   └── _BRIEF.md                                   (survey PR #193: async resources + components)
├── SUBTASK_ferric-router-survey/
│   └── _BRIEF.md                                   (survey PR #203: router API)
├── SUBTASK_ferric-ssr-survey/
│   └── _BRIEF.md                                   (survey PR #228: SSR + hydration + Axum)
└── SUBTASK_ferric-survey-synthesis/
    └── _BRIEF.md                                   (synthesis: integrate + write ferric-survey.md)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_ferric-async-survey` | none | Survey PR #193: async resource types, loading/error/data state, component patterns, form/event binding | `SUBTASK_ferric-async-survey/ferric-async-notes.md` |
| `SUBTASK_ferric-router-survey` | none | Survey PR #203: router type, route declaration, navigation API, not-found/redirect handling | `SUBTASK_ferric-router-survey/ferric-router-notes.md` |
| `SUBTASK_ferric-ssr-survey` | none | Survey PR #228: render_to_string equivalent, client hydration initiation, Axum integration point | `SUBTASK_ferric-ssr-survey/ferric-ssr-notes.md` |
| `SUBTASK_ferric-survey-synthesis` | `SUBTASK_ferric-async-survey`, `SUBTASK_ferric-router-survey`, `SUBTASK_ferric-ssr-survey` | Read all notes + crate structure + write ferric-survey.md and SYNTHESIS.md | `ferric-survey.md`, `SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_ferric-async-survey  ──┐
                               │
SUBTASK_ferric-router-survey  ─┼── SUBTASK_ferric-survey-synthesis
                               │
SUBTASK_ferric-ssr-survey     ──┘
```

---

## Contract

**Contract location**: `contracts/` (read-only for all descendants)
**Contract kind**: `yaml_schema`

### Structural Declarations

Each spoke task (async-survey, router-survey, ssr-survey) MUST produce a notes markdown file conforming to `contracts/notes-schema.yaml`. The synthesis task reads all three notes files and the crate structure to assemble `ferric-survey.md`.

### Ownership

| Artifact | Owning subtask |
|----------|----------------|
| `SUBTASK_ferric-async-survey/ferric-async-notes.md` | `SUBTASK_ferric-async-survey` |
| `SUBTASK_ferric-router-survey/ferric-router-notes.md` | `SUBTASK_ferric-router-survey` |
| `SUBTASK_ferric-ssr-survey/ferric-ssr-notes.md` | `SUBTASK_ferric-ssr-survey` |
| `ferric-survey.md` | `SUBTASK_ferric-survey-synthesis` |
| `SYNTHESIS.md` | `SUBTASK_ferric-survey-synthesis` |

### Identities

- [ ] Each notes file MUST contain at least one Rust type signature (in a code block)
- [ ] Each notes file MUST include a "State Model" or equivalent section documenting loading/error/data states
- [ ] Each notes file MUST reference actual file paths in `crates/ferric/` as source locations
- [ ] `ferric-survey.md` MUST cover all 6 sections from the parent brief (crate structure, async primitives, router API, SSR/hydration, component pattern, gaps)

---

## Output Specifications

| Deliverable | Format | Location | Description |
|-------------|--------|----------|-------------|
| `ferric-async-notes.md` | Markdown | `SUBTASK_ferric-async-survey/` | PR #193 API notes |
| `ferric-router-notes.md` | Markdown | `SUBTASK_ferric-router-survey/` | PR #203 API notes |
| `ferric-ssr-notes.md` | Markdown | `SUBTASK_ferric-ssr-survey/` | PR #228 API notes |
| `ferric-survey.md` | Markdown | This workspace root | The compiled survey for SUBTASK_frontend-ui |
| `SYNTHESIS.md` | Markdown | This workspace root | Fold record |
