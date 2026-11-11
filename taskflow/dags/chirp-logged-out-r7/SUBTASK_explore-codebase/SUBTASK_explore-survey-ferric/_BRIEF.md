# Task: Ferric Framework Primitives Survey

## Task Specification

**Slug**: SUBTASK_explore-survey-ferric  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

Read `crates/ferric/` and document the async data-fetching primitives, component patterns, SSR/hydration support, and router API available after PRs #193, #203, and #228 were merged. This survey tells SUBTASK_frontend-ui exactly which Ferric APIs it can use for loading/error/empty/end-of-list states.

### Context

This task is part of the Codebase Exploration subtree for Chirp Logged-Out r7. See `../_GLOBAL.md` for subtree context. The parent `../../_GLOBAL.md` notes that Ferric PRs #193 (async resources and form/event binding), #203 (router), and #228 (SSR + hydration + Axum integration) were merged to `main` at `cb1ced3`.

**Dependents**: SUBTASK_explore-synthesis (reads ferric-survey.md)

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Subtree constraints and context |
| Project context | `../../_GLOBAL.md` | Framework context (PRs #193, #203, #228) |
| Ferric codebase | `crates/ferric/` | Async resource primitives, router, SSR, hydration APIs |

The Ferric codebase lives in `Nousix-LLC/nswe-demo` on `main` at `cb1ced3`. Read via the cloned repository on the build server (SSH) or `gh api`.

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `ferric-survey.md` |
| Location | `SUBTASK_explore-survey-ferric/` (this workspace) |

### Output Structure

`ferric-survey.md` MUST include:

1. **Crate Structure** — Top-level file layout of `crates/ferric/`; module organization; re-exported public API surface.

2. **Async Resource Primitives** (from PR #193) — The types, functions, or macros available for async data fetching. For each:
   - Name and type signature
   - Loading/error/data state model
   - How to create and consume it in a component

3. **Router API** (from PR #203) — How routes are declared; navigation API; any support for not-found / redirect handling.

4. **SSR and Hydration** (from PR #228) — What `render_to_string` or equivalent provides; how client-side hydration is initiated; Axum integration point.

5. **Component Pattern** — The idiomatic pattern for a component that:
   - Triggers an async fetch on mount
   - Shows a loading indicator while pending
   - Shows an error state with recovery option on failure
   - Shows content when resolved
   - Shows an empty/end-of-list state when the response is empty

6. **Gaps or Limitations** — Any capability the frontend task will need that is NOT yet in the framework, requiring a workaround or fallback.

---

## Success Criteria

- [ ] Async resource primitives documented with type signatures
- [ ] Router API documented (route declaration and navigation)
- [ ] SSR + hydration API documented with Axum integration point
- [ ] Four-state component pattern described in enough detail for SUBTASK_frontend-ui to implement without re-reading the whole codebase
- [ ] ferric-survey.md written at this workspace

---

## Suggested Methodology Files

**Task-type row matched**: "Building a UI framework / framework primitive (signals, fine-grained reactivity vs virtual DOM, SSR + hydration)" → Framework Design + Rust + Frontend

**Primary files to load**:
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — rationale: documents the signals, component, SSR, and hydration design space that Ferric implements; provides vocabulary for describing the primitives
- `rust/Rust_WebAssembly_Browser_Methodology.md` — rationale: Ferric targets WASM; understanding the wasm-bindgen / web-sys surface helps read the Ferric internals

These are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.

## Inherited Constraints

- Exploration only — no code changes to `crates/ferric/` or any other crate
- Repository: `Nousix-LLC/nswe-demo`; codebase is on `main` at `cb1ced3`
- No host paths, internal addresses, or taskflow references in output

## Out-of-Scope Methodologies

- Testing methodologies — this task writes no tests
- Backend/server methodologies — deferred to survey-backend
