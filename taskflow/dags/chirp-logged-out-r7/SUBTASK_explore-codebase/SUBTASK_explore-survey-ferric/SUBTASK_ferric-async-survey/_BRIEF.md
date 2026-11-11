# Task: Ferric Async Resource Primitives Survey (PR #193)

## Task Specification

**Slug**: SUBTASK_ferric-async-survey
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-coder

### Objective

Read `crates/ferric/` in `Nousix-LLC/nswe-demo` at `main` (commit `cb1ced3`) and document the async data-fetching primitives, loading/error/data state model, component creation patterns, and form/event binding introduced by PR #193. Produce `ferric-async-notes.md` conforming to the subtree contract schema.

### Context

This task is part of the Ferric Framework Survey subtree. See `../_GLOBAL.md` for subtree constraints and context.

**Dependents**: SUBTASK_ferric-survey-synthesis (reads ferric-async-notes.md)

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Subtree constraints and contract reference |
| Contract schema | `../contracts/notes-schema.yaml` | Required sections for ferric-async-notes.md |
| Ferric crate | `crates/ferric/` in `Nousix-LLC/nswe-demo` | Source of PR #193 async resource APIs |

**Accessing the codebase**: Use `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/` to list files, then `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/<path>` to read individual files. The content will be base64-encoded; decode it.

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `ferric-async-notes.md` |
| Location | `SUBTASK_ferric-async-survey/` (this workspace) |

The output MUST conform to `../contracts/notes-schema.yaml`. Required sections: Source Locations, Public API (with Rust type signatures), State Model, Usage Example.

### What to Document (from PR #193)

PR #193 added async resources and form/event binding to Ferric. Document:

1. **Async resource types**: The primary type(s) used to represent an in-flight or resolved async fetch. Include the full type definition(s) with Rust syntax.

2. **Loading / error / data state model**: How the resource represents its three (or more) states. Include the enum or state type with all variants.

3. **Resource creation**: The function, macro, or method used to create an async resource in a component (the `use_resource`-style API or equivalent). Include the full signature.

4. **Consuming the resource**: How component code reads the current state (e.g. a `.read()` method, a signal, a hook). Include the access pattern.

5. **Form and event binding**: Any types or macros added for form submission or event handling (e.g. `use_server_future`, action types, form submission helpers). Include signatures.

---

## Success Criteria

- [ ] `ferric-async-notes.md` written at this workspace
- [ ] At least one Rust type signature in a fenced code block
- [ ] State model section present and describes all state variants
- [ ] Source locations list actual `crates/ferric/` file paths
- [ ] Usage example shows create-and-consume pattern

---

## Suggested Methodology Files

**Task-type row matched**: "Building a UI framework / framework primitive (signals, fine-grained reactivity vs virtual DOM, SSR + hydration)" → Framework Design + Rust + Frontend; also "Rust ↔ WebAssembly / browser bindings" → Rust + Framework Design

**Primary files to load**:
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — rationale: documents the signals, component, and async data-fetching design space that Ferric's PR #193 implements; provides vocabulary for describing the resource primitive (signal vs. future-based, fine-grained vs. virtual DOM reactivity)
- `rust/Rust_WebAssembly_Browser_Methodology.md` — rationale: Ferric targets WASM; understanding wasm-bindgen and web-sys helps read the async resource internals and binding mechanisms

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.

## Inherited Constraints

- Exploration only — no code changes to `crates/ferric/` or any other crate
- Repository: `Nousix-LLC/nswe-demo`; codebase on `main` at `cb1ced3`
- No host paths, internal addresses, or taskflow references in output
- Output `ferric-async-notes.md` MUST conform to `../contracts/notes-schema.yaml`

## Out-of-Scope Methodologies

- Testing methodologies — this task writes no tests
- Backend/server methodologies — deferred; focus only on client-side async resource primitives and component patterns from PR #193
- Router API — documented by SUBTASK_ferric-router-survey
- SSR/hydration — documented by SUBTASK_ferric-ssr-survey
