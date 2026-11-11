# Task: Frontend Logged-Out Visitor UI

## Task Specification

**Slug**: SUBTASK_frontend-ui  
**Task Kind**: standard  
**Depends on**: SUBTASK_backend-api  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

Implement the logged-out visitor frontend in the Chirp frontend crate: a home/landing route showing the public timeline with four visually distinct states (loading, empty, error, end-of-list), a public user profile view reachable from the timeline, visible sign-up and sign-in navigation, and tests for each distinct state. This satisfies AC-1 through AC-5.

### Context

This task is part of Chirp Logged-Out Visitor Experience r7 (see `../_GLOBAL.md` for full context, ACs, and constraints).

**Dependencies**: SUBTASK_backend-api (backend-impl.md defines the endpoint URLs and response shapes this task calls)  
**Dependents**: SUBTASK_synthesis (reads frontend-impl.md)

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Parent hub | `../_GLOBAL.md` | Project context, ACs, constraints |
| Analysis | `../SUBTASK_explore-codebase/analysis.md` | Existing frontend structure, Ferric primitives available |
| Backend impl | `../SUBTASK_backend-api/backend-impl.md` | Exact API endpoint URLs and response shapes to call |
| Contracts | `../contracts/public_api_contract.md`, `../contracts/_MANIFEST.yaml` | Ownership and identity constraints |
| Repository | frontend crate(s) on branch `work/chirp-logged-out` | Codebase to modify |
| Design docs | `design/experience-design.md` | Screen layouts, state specifications for AC-5 |

---

## Output Specification

### Primary Output: `frontend-impl.md`

| Attribute | Value |
|-----------|-------|
| Filename | `frontend-impl.md` |
| Location | `SUBTASK_frontend-ui/` |

`frontend-impl.md` MUST document:

1. **Components Implemented**: Each new or modified component, its file location, and which AC it addresses
2. **Four Timeline States**: For each state (loading, empty, error, end-of-list), describe the visual treatment and the code path that produces it
3. **Navigation**: Where sign-up and sign-in links appear and what routes they link to
4. **API Calls Made**: The exact endpoint URLs called (must match backend-impl.md)
5. **Test Coverage**: Which tests were added, which states they cover, and how to run them

### Secondary Output: Code commits on branch `work/chirp-logged-out`

Frontend implementation committed to the branch.

---

## Success Criteria

- [ ] A logged-out visitor can reach the home/landing route without authentication (AC-1)
- [ ] Loading state: a visually distinct "loading" indicator renders while the timeline fetch is in-flight (AC-5)
- [ ] Empty state: when no chirps exist, the visitor sees a clear statement of what Chirp is plus an obvious way to sign up / sign in — never a blank page (AC-2, AC-5)
- [ ] Error state: if the timeline fetch fails, a clear recoverable message renders — never a blank or broken screen (AC-3, AC-5)
- [ ] End-of-list state: when all chirps have been loaded (pagination exhausted), a distinct indicator renders (AC-5)
- [ ] A "create an account" link (or equivalent) is visible from the landing (AC-4)
- [ ] A user profile is reachable from the timeline without authentication (AC-1)
- [ ] `cargo build --target wasm32-unknown-unknown` (or equivalent WASM build) succeeds
- [ ] `cargo clippy` produces no errors for modified code
- [ ] `cargo fmt --check` passes for modified files
- [ ] At least one test exists for each distinct state (loading, empty, error, end-of-list)
- [ ] `frontend-impl.md` documents all of the above

---

## Suggested Methodology Files

**Task-type row matched**: "Writing Rust code" → Rust; "Building a UI framework / framework primitive" → Framework Design (UI Reactivity & Rendering Internals); "Rust ↔ WebAssembly / browser bindings" → Rust WebAssembly Browser

**Primary files to load**:
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — rationale: Ferric is the UI framework in use; this methodology covers fine-grained reactivity, signals, component lifecycles, and SSR+hydration patterns that directly apply to the four-state async timeline component
- `rust/Rust_WebAssembly_Browser_Methodology.md` — rationale: the frontend compiles to WASM; wasm-bindgen and web-sys patterns are needed for DOM interaction and test harness
- `rust/Rust_Error_Handling_Methodology.md` — rationale: the error state must render a user-visible recovery message; proper error type propagation determines how the component receives and displays the error
- `rust/Rust_Testing_Methodology.md` — rationale: wasm-bindgen-test or component test patterns for each distinct state

**Supporting files** (load if the approach reveals a need):
- `framework-design/FrameworkDesign_Incremental_Adoption_And_Interop_Methodology.md` — if adopting the existing Ferric patterns requires interop knowledge
- `testing/Testing_Unit_Testing_Methodology.md` — if component unit test structure needs elaboration

These are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but is the final judge of what its work requires.

## Inherited Constraints

- Branch: `work/chirp-logged-out` — all commits on this branch
- Repository: `Nousix-LLC/nswe-demo`
- Rust 2021 edition; existing Cargo workspace conventions apply
- MUST call only the endpoints declared in `../SUBTASK_backend-api/backend-impl.md` — do not invent API URLs
- Do NOT add authentication where it did not exist
- Each of the four timeline states (loading, empty, error, end-of-list) MUST be visually distinct per AC-5 — no collapsing into a single "not loaded" fallback
- `cargo fmt --check`, `cargo clippy`, WASM build, and state tests MUST pass
- No host paths, internal addresses, or taskflow references in committed code
- Design doc: `design/experience-design.md` §2 and §6 (REQ-UX-002, REQ-UX-030–032) are the authoritative screen/state spec

## Out-of-Scope Methodologies

- Backend/Axum methodologies — SUBTASK_backend-api owns the server
- PR creation — deferred to SUBTASK_synthesis
- SSR optimization beyond what Ferric already provides — if SSR is straightforward to add, add it; if it requires major architecture work, document it in frontend-impl.md as a future concern
