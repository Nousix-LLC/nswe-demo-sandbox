# Task: Ferric SSR + Hydration Survey (PR #228)

## Task Specification

**Slug**: SUBTASK_ferric-ssr-survey
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-coder

### Objective

Read `crates/ferric/` in `Nousix-LLC/nswe-demo` at `main` (commit `cb1ced3`) and document the server-side rendering (SSR) and client-side hydration APIs introduced by PR #228, including the Axum integration point. Produce `ferric-ssr-notes.md` conforming to the subtree contract schema.

### Context

This task is part of the Ferric Framework Survey subtree. See `../_GLOBAL.md` for subtree constraints and context.

**Dependents**: SUBTASK_ferric-survey-synthesis (reads ferric-ssr-notes.md)

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Subtree constraints and contract reference |
| Contract schema | `../contracts/notes-schema.yaml` | Required sections for ferric-ssr-notes.md |
| Ferric crate | `crates/ferric/` in `Nousix-LLC/nswe-demo` | Source of PR #228 SSR + hydration + Axum APIs |

**Accessing the codebase**: Use `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/` to list files, then `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/<path>` to read individual files. The content will be base64-encoded; decode it.

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `ferric-ssr-notes.md` |
| Location | `SUBTASK_ferric-ssr-survey/` (this workspace) |

The output MUST conform to `../contracts/notes-schema.yaml`. Required sections: Source Locations, Public API (with Rust type signatures), State Model, Usage Example.

### What to Document (from PR #228)

PR #228 added SSR + hydration + Axum integration to Ferric. Document:

1. **SSR render function**: The function or method that renders a Ferric component tree to an HTML string on the server. Include the full signature. Common names: `render_to_string`, `ssr_render`, `render_html`. Document its parameters (e.g. does it accept props? a context? async?).

2. **Feature flags**: Whether SSR is behind a Cargo feature flag (e.g. `features = ["ssr"]`) and what other flags exist. Check `Cargo.toml`.

3. **Client-side hydration initiation**: The function called in WASM to hydrate a server-rendered HTML page. Include the signature and expected usage location (e.g. in `main()` or a `#[wasm_bindgen(start)]` function).

4. **Axum integration point**: The specific Axum handler signature or extractor that integrates Ferric SSR into an Axum server. Include the handler signature and any Ferric-specific extractor types. Note whether it is provided via a helper function or the user writes it themselves.

5. **Data serialization for hydration**: Whether async resource data fetched on the server can be serialized and injected into the HTML so the client can hydrate with pre-fetched data (a common SSR + hydration concern). Document how or whether this is supported.

6. **Any SSR-specific component constraints**: Whether certain APIs (e.g. event handlers, browser-only APIs) behave differently or are unavailable in SSR mode.

---

## Success Criteria

- [ ] `ferric-ssr-notes.md` written at this workspace
- [ ] SSR render function signature documented with Rust syntax
- [ ] Client hydration initiation signature documented
- [ ] Axum integration point documented
- [ ] Feature flags documented (check `Cargo.toml`)
- [ ] Source locations list actual `crates/ferric/` file paths

---

## Suggested Methodology Files

**Task-type row matched**: "SSR / hydration in a Rust UI framework" → Framework Design + Rust; also "Rust web services / Axum / Tower / server-side HTTP" → Rust + Framework Design

**Primary files to load**:
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — rationale: documents the SSR design space (render-to-string, hydration, streaming, selective hydration); provides vocabulary for describing Ferric's SSR model and where it falls on the spectrum
- `rust/Rust_WebAssembly_Browser_Methodology.md` — rationale: documents the WASM / browser binding surface; hydration initiation is a wasm-bindgen concern, and understanding the WASM lifecycle helps describe how `#[wasm_bindgen(start)]` wires up hydration
- `rust/Rust_Web_Services_Axum_Methodology.md` — rationale: Ferric's SSR integration point is Axum; understanding Axum's handler/extractor model helps accurately describe how Ferric plugs into an Axum server

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.

## Inherited Constraints

- Exploration only — no code changes to `crates/ferric/` or any other crate
- Repository: `Nousix-LLC/nswe-demo`; codebase on `main` at `cb1ced3`
- No host paths, internal addresses, or taskflow references in output
- Output `ferric-ssr-notes.md` MUST conform to `../contracts/notes-schema.yaml`

## Out-of-Scope Methodologies

- Testing methodologies — this task writes no tests
- Async resource primitives — documented by SUBTASK_ferric-async-survey
- Router API — documented by SUBTASK_ferric-router-survey
