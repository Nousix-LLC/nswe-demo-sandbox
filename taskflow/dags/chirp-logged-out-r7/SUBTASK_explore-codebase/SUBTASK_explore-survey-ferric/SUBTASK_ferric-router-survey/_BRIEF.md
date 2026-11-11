# Task: Ferric Router API Survey (PR #203)

## Task Specification

**Slug**: SUBTASK_ferric-router-survey
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-coder

### Objective

Read `crates/ferric/` in `Nousix-LLC/nswe-demo` at `main` (commit `cb1ced3`) and document the router API introduced by PR #203: how routes are declared, the navigation API, and how not-found and redirect cases are handled. Produce `ferric-router-notes.md` conforming to the subtree contract schema.

### Context

This task is part of the Ferric Framework Survey subtree. See `../_GLOBAL.md` for subtree constraints and context.

**Dependents**: SUBTASK_ferric-survey-synthesis (reads ferric-router-notes.md)

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Subtree constraints and contract reference |
| Contract schema | `../contracts/notes-schema.yaml` | Required sections for ferric-router-notes.md |
| Ferric crate | `crates/ferric/` in `Nousix-LLC/nswe-demo` | Source of PR #203 router APIs |

**Accessing the codebase**: Use `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/` to list files, then `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/<path>` to read individual files. The content will be base64-encoded; decode it.

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `ferric-router-notes.md` |
| Location | `SUBTASK_ferric-router-survey/` (this workspace) |

The output MUST conform to `../contracts/notes-schema.yaml`. Required sections: Source Locations, Public API (with Rust type signatures), State Model (or explicit note that the router is stateless), Usage Example.

### What to Document (from PR #203)

PR #203 added a router to Ferric. Document:

1. **Router type and initialization**: The primary `Router` type (or equivalent) and how it is initialized. Include the type definition and constructor signature.

2. **Route declaration**: How routes are declared — whether via a macro, builder API, enum, or other mechanism. Include the full signature and example.

3. **Navigation API**: Functions or methods for programmatic navigation (e.g. `navigate_to`, `use_navigate`, link components). Include signatures.

4. **Route matching and parameters**: How the router extracts URL parameters or segments. Include the types involved.

5. **Not-found handling**: How the router handles unmatched routes. Include the type or configuration option.

6. **Redirect handling**: Whether the router supports redirects and how they are expressed.

7. **Link component**: Whether there is a `<Link>` component or equivalent and its signature.

---

## Success Criteria

- [ ] `ferric-router-notes.md` written at this workspace
- [ ] At least one Rust type signature in a fenced code block
- [ ] State model section present (even if router is stateless — state that explicitly)
- [ ] Source locations list actual `crates/ferric/` file paths
- [ ] Route declaration, navigation API, and not-found handling are covered

---

## Suggested Methodology Files

**Task-type row matched**: "Building a UI framework / framework primitive (signals, fine-grained reactivity vs virtual DOM, SSR + hydration)" → Framework Design + Rust + Frontend

**Primary files to load**:
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — rationale: documents the router design space (client-side routing, nested routes, URL parameters) for Rust UI frameworks; provides vocabulary for describing a router built in Ferric's style
- `rust/Rust_WebAssembly_Browser_Methodology.md` — rationale: Ferric targets WASM; the browser's URL/history API is what the router wraps, and understanding wasm-bindgen / web-sys surface helps read the router internals

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but is the final judge of what its work requires.

## Inherited Constraints

- Exploration only — no code changes to `crates/ferric/` or any other crate
- Repository: `Nousix-LLC/nswe-demo`; codebase on `main` at `cb1ced3`
- No host paths, internal addresses, or taskflow references in output
- Output `ferric-router-notes.md` MUST conform to `../contracts/notes-schema.yaml`

## Out-of-Scope Methodologies

- Testing methodologies — this task writes no tests
- Async resource primitives — documented by SUBTASK_ferric-async-survey
- SSR/hydration — documented by SUBTASK_ferric-ssr-survey
