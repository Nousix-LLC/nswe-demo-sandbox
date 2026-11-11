# Chirp Logged-Out Visitor Experience (r8)

## Project Context

**Status**: Active  
**Repository**: `Nousix-LLC/nswe-demo`  
**Branch**: `work/chirp-logged-out` (create from `main` at `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`)  
**GitHub Issue**: #35 — "Logged-out reading and a useful landing with accurate states"

### Objective

Implement the logged-out visitor experience for Chirp: a public timeline readable without an account, public user profiles reachable from it, and a landing that is useful even when there is no content yet. No authentication must be required to reach these screens.

### Scope

**In Scope:**
- Public timeline API endpoint (unauthenticated GET) in chirp-server
- Public user profile API endpoint (unauthenticated GET if not present) in chirp-server
- chirp-frontend home/landing route showing the public timeline with accurate states (loading, empty, error, end-of-list)
- Public user profile view in chirp-frontend
- Visible sign-up and sign-in navigation from the landing
- Unit and integration tests for new API endpoints
- wasm-bindgen-test or component tests for frontend states

**Out of Scope:**
- Authenticated features (posting, following, notifications)
- Removing existing authentication where it already exists
- Adding authentication where it did not exist

### Success Criteria

All five acceptance criteria from GitHub issue #35 must be met:

- **AC-1 (REQ-PROD-013 / BAR-011):** Logged-out visitor can load the public timeline and open a user profile without being forced to sign up or sign in first.
- **AC-2 (REQ-PROD-014 / BAR-011):** With no content, visitor sees a clear "what chirp is" statement plus an obvious sign-up/sign-in route — never a blank page.
- **AC-3 (REQ-PROD-014 / BAR-011):** Timeline load failure shows a clear, recoverable message.
- **AC-4 (REQ-PROD-015 / BAR-011):** "Create an account" route is visible from the landing and from the sign-in screen, and leads to sign-up.
- **AC-5 (REQ-UX-002 / REQ-UX-030–032 / BAR-011 / one-state-model criterion):** Loading, empty, error, and end-of-list states are each visually distinct — never blank, never stale.

**CI must pass:** `fmt`, `clippy`, `test`, `wasm`, `doc`, `image` checks.

---

## Input Specifications

### Repository

- Repository root: `/home/user/nousix-runtime/nswe-demo`
- Chirp server: `crates/chirp-server/`
- Chirp frontend: `crates/chirp-frontend/`
- Ferric framework: `crates/ferric/`
- Design documents: `design/`
  - `design/product-requirements.md` — §3 User journeys; §4 REQ-PROD-013, REQ-PROD-014, REQ-PROD-015
  - `design/experience-design.md` — §1 Information architecture; §2 Screens, flows & states; §6 REQ-UX-002, REQ-UX-030–032
  - `design/release-bar.md` — §C BAR-011
- SSH access to k3d cluster: see `CLAUDE.md` in repository root

### Key Dependencies

- **Ferric framework** (complete): reactive signals, component model, DOM rendering, router, async resources, SSR render_to_string + client-side hydration + Axum integration.
- **Chirp server** (existing): Axum REST API + persistence. The exploration task must determine whether a public timeline/profile endpoint already exists.

---

## Cut Rationale

**Selected cut: Linear phase pipeline (Explore → Backend → Frontend → Synthesis)**

Candidates considered:

- **(A) Layer cut** (backend task / frontend task / test task): Rejected — the test task would have to know the full implementation details of both backend and frontend, requiring fragile dependencies.
- **(B) Linear phase pipeline** (selected): Explore produces the API contract and git branch; backend implements server-side endpoints + tests; frontend implements UI components + tests building on the backend's implementation; synthesis creates the PR. Each child owns disjoint files; no concurrent writes to the same files. Serialization avoids git merge conflicts.
- **(C) Contract-first fan-out** (explore → backend/frontend parallel → synthesis): Rejected — backend and frontend committing to the same branch in parallel risks git merge conflicts and complicates the execution model.

**Why linear serialization works here**: Frontend code uses a Ferric `AsyncResource` to fetch from the backend endpoints. The frontend agent should build against the actually-implemented backend (not just a contract document), so the sequential dependency (backend before frontend) is correct.

---

## Task Structure

### Overview

```
_GLOBAL.md (this document)
├── contracts/_MANIFEST.yaml                       (API surface contract)
├── SUBTASK_explore/_BRIEF.md                      (Exploration + branch setup)
├── SUBTASK_backend/_BRIEF.md                      (Server-side API + tests)
├── SUBTASK_frontend/_BRIEF.md                     (Frontend components + tests)
└── SUBTASK_synthesis/_BRIEF.md                    (PR creation + SYNTHESIS.md)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_explore` | none | Explore codebase, read design docs, design API shapes, create git branch | `SUBTASK_explore/analysis.md` |
| `SUBTASK_backend` | `SUBTASK_explore` | Implement public API endpoints + integration tests in chirp-server | Committed code on `work/chirp-logged-out` |
| `SUBTASK_frontend` | `SUBTASK_backend` | Implement frontend landing/home route and user profile view + wasm tests | Committed code on `work/chirp-logged-out` |
| `SUBTASK_synthesis` | `SUBTASK_frontend` | Create PR closing issue #35, write SYNTHESIS.md | PR URL + `SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_explore → SUBTASK_backend → SUBTASK_frontend → SUBTASK_synthesis
```

---

## Contract

**Contract location**: `contracts/`  
**Contract kind**: `yaml_schema`

The key seam in this decomposition is the shape of the public API endpoints: SUBTASK_explore defines the shapes (what routes, what request params, what response structures); SUBTASK_backend implements those shapes; SUBTASK_frontend builds against those same shapes. The contract freezes this seam before any child runs.

### Inherited Contracts

None — this is the root decomposition.

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/api_contract.yaml` | yaml_schema | URL paths, HTTP methods, query parameters, response body shapes for the two public endpoints |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `contracts/api_contract.yaml` | `SUBTASK_explore` (produces/finalizes) |
| `crates/chirp-server/` changes | `SUBTASK_backend` |
| `crates/chirp-frontend/` changes | `SUBTASK_frontend` |
| GitHub PR + `SYNTHESIS.md` | `SUBTASK_synthesis` |

### Identities

- [ ] The backend endpoints implement the URL paths and response shapes declared in `contracts/api_contract.yaml` (or equivalent output from SUBTASK_explore)
- [ ] The frontend fetch calls target the same URL paths and expect the same response shapes

### Derived Artifacts

None — the API contract is authored by SUBTASK_explore, not generated from a schema.

### Thin-Seam Note

This contract is minimal by design: the two non-overlapping implementation concerns (backend vs. frontend) share one seam (the API shape). The contract document from SUBTASK_explore is the operative contract the downstream tasks compose against.

---

## Subtree Methodology Posture

**Dominant task type**: Writing Rust code (backend Axum API + frontend Ferric WASM)  
**Primary bundles**: `rust`, `rust` (web-services-axum for backend), `framework-design` (UI framework for frontend), `testing`, `core`

**Cross-cutting bindings that apply to every leaf:**
- Repository constraint: Rust 2021 edition, Cargo workspace, CI must stay green
- Branch constraint: all code changes on `work/chirp-logged-out` only
- Quality constraint: `cargo fmt`, `cargo clippy`, `cargo test` must pass
- No secrets or host paths in anything committed to the repository

**Note on suggestion-not-prescription**: Descendant agents read these as the parent's flagged starting point. Each agent retains final judgment over what it loads and how deep it goes.

---

## Subtree-Wide Constraints

1. **Branch**: All commits go to `work/chirp-logged-out` (created from `main` at `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`).
2. **CI**: `fmt`, `clippy`, `test`, `wasm`, `doc`, `image` must all pass before the PR is opened.
3. **No auth removal**: Do not remove authentication from existing authenticated endpoints.
4. **No host paths or internal addresses** in committed code or PR description.
5. **PR**: One PR into `main` with `Closes #35` as plain text in the description body.
6. **CLAUDE.md**: The repository's `CLAUDE.md` has instructions about how to run kubectl/kubectl commands over SSH; follow them exactly.
