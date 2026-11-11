# Chirp Logged-Out Visitor Experience (r7)

## Project Context

**Status**: Active  
**Repository**: Nousix-LLC/nswe-demo  
**Branch**: `work/chirp-logged-out` (create from main at `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`)  
**GitHub Issue**: #35 — "Logged-out reading and a useful landing with accurate states"

### Objective

Implement the logged-out visitor experience for Chirp: a public timeline readable without an account, public user profiles reachable from it, and a landing that is useful even when there is no content yet. No authentication must be required to reach these screens.

### Acceptance Criteria (from issue #35)

- **AC-1 (REQ-PROD-013 / BAR-011):** A logged-out visitor can load the home/public timeline and open a user profile and read chirps without being forced to sign up or sign in first.
- **AC-2 (REQ-PROD-014 / BAR-011):** On arrival with no content, the visitor sees a clear statement of what chirp is plus an obvious way to sign up or sign in — never a blank page or an unexplained error.
- **AC-3 (REQ-PROD-014 / BAR-011):** If the timeline fails to load, a clear, recoverable message is shown instead of a broken screen.
- **AC-4 (REQ-PROD-015 / BAR-011):** A "create an account" route is visible on the landing and on the sign-in screen, and following it reaches sign-up.
- **AC-5 (REQ-UX-002 / REQ-UX-030–032 / BAR-011 / one-state-model criterion):** The logged-out landing/timeline renders its loading, empty, error, and end-of-list states accurately and distinctly — each state is a visually distinct screen, never a blank page or a stale view.

### Scope

**In scope:**
- Public timeline API endpoint (unauthenticated GET)
- Public user profile API endpoint (unauthenticated GET if not present)
- chirp-frontend home/landing route showing the public timeline with accurate states
- Public user profile view
- Visible sign-up and sign-in navigation from the landing

**Out of scope:**
- Authenticated features (posting, following, notifications)
- Adding authentication where it did not exist
- Removing authentication where it did exist

### Success Criteria

- [ ] All 5 acceptance criteria met
- [ ] CI passes: `fmt`, `clippy`, `test`, `wasm`, `doc`, `image` checks
- [ ] One PR into `main` with `Closes #35` in the plain-text description body
- [ ] Root SYNTHESIS.md accounts for each AC

---

## What This Builds On

**Ferric framework** (landed, `main` at `cb1ced3`):
- Reactive signals, component model, DOM rendering, router (PR #203 merged)
- Async resources and form/event binding (PR #193 merged)
- SSR render_to_string + client-side hydration + Axum integration (PR #228 merged)

**Chirp server** (`crates/chirp-server`): Axum REST API + persistence + static SPA serving. Durable persistence complete (epic #56, PRs #182/#183 merged).

**Design documents** (in `design/` on `main`):
- `design/product-requirements.md` — §3 User journeys; §4 REQ-PROD-013, REQ-PROD-014, REQ-PROD-015
- `design/experience-design.md` — §1 Information architecture; §2 Screens, flows & states; §6 REQ-UX-002, REQ-UX-030–032
- `design/release-bar.md` — §C BAR-011

---

## Constraints

- Repository: `Nousix-LLC/nswe-demo`
- Branch: `work/chirp-logged-out` (create from `main` at `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`)
- One PR into `main` with `Closes #35` as plain text in the description
- No force-push to `main`
- No host paths, internal addresses, or taskflow references in committed code or GitHub content
- Written for the Rust toolchain, Ferric UI framework, Axum server

---

## Task Structure

```
_GLOBAL.md (this document)
├── contracts/
│   ├── _MANIFEST.yaml          (ownership, identities)
│   └── public_api_contract.md  (API surface contract)
├── SUBTASK_explore-codebase/
│   └── _BRIEF.md
├── SUBTASK_backend-api/
│   └── _BRIEF.md
├── SUBTASK_frontend-ui/
│   └── _BRIEF.md
└── SUBTASK_synthesis/
    └── _BRIEF.md
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_explore-codebase` | none | Explore codebase, read design docs, create branch from main | `analysis.md` |
| `SUBTASK_backend-api` | `SUBTASK_explore-codebase` | Implement public (unauthenticated) API endpoints in chirp-server | `backend-impl.md` |
| `SUBTASK_frontend-ui` | `SUBTASK_backend-api` | Implement frontend: home route, public timeline with 4 states, user profile, navigation | `frontend-impl.md` |
| `SUBTASK_synthesis` | `SUBTASK_frontend-ui` | Verify ACs, create PR closing #35, produce SYNTHESIS.md | `../SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_explore-codebase → SUBTASK_backend-api → SUBTASK_frontend-ui → SUBTASK_synthesis
```

---

## Contract

**Contract location**: `contracts/`  
**Contract kind**: `yaml_schema` (API surface) + ownership manifest

The backend task OWNS the public API surface; the frontend task MUST only call endpoints the backend task has established. The synthesis task verifies that every AC is covered by the combined implementation.

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/public_api_contract.md` | API spec | Public endpoint URL patterns and response shapes that the backend task MUST implement and the frontend task MUST compose against |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `crates/chirp-server` changes | `SUBTASK_backend-api` |
| `crates/chirp-frontend` changes (or `crates/ferric` integration) | `SUBTASK_frontend-ui` |
| `analysis.md` | `SUBTASK_explore-codebase` |
| `backend-impl.md` | `SUBTASK_backend-api` |
| `frontend-impl.md` | `SUBTASK_frontend-ui` |
| `SYNTHESIS.md` (at this workspace root) | `SUBTASK_synthesis` |

### Identities

- [ ] Every public API endpoint called by the frontend MUST be declared and implemented by SUBTASK_backend-api
- [ ] Every AC (AC-1 through AC-5) MUST be covered by at least one implementation artifact
- [ ] CI checks (fmt, clippy, test, wasm, doc, image) MUST pass on the branch

---

## Subtree Methodology Posture

**Dominant task type**: Writing Rust code (backend + frontend), with Framework Design (Ferric) and PR creation

**Primary bundles** that subtree leaf tasks draw on:
- `rust` (ownership, error handling, Axum, testing, WebAssembly)
- `core` (coding standards, error handling, commit practices)
- `framework-design` (UI Reactivity & Rendering Internals — for Ferric framework patterns)
- `testing` (unit and integration testing, wasm-bindgen tests)
- `operations` (PR lifecycle, branching)

**Cross-cutting bindings** across the entire subtree:
- Rust 2021 edition; Cargo workspace conventions per the existing repository
- Ferric framework APIs as established by PRs #193, #203, #228
- Axum API patterns as established in existing `crates/chirp-server`
- No host paths, internal addresses, or taskflow references in committed code
- `Closes #35` must appear literally in the PR description body

**Note**: Descendant agents retain final judgment over which methodology files they load and how they apply them.

---

## Output Specifications

| Deliverable | Format | Location | Description |
|-------------|--------|----------|-------------|
| analysis.md | Markdown | `SUBTASK_explore-codebase/analysis.md` | Current state of API and frontend, gap analysis per AC |
| backend-impl.md | Markdown | `SUBTASK_backend-api/backend-impl.md` | What was implemented, endpoint shapes, test coverage |
| frontend-impl.md | Markdown | `SUBTASK_frontend-ui/frontend-impl.md` | What was implemented, component structure, test coverage |
| SYNTHESIS.md | Markdown | `./SYNTHESIS.md` | Per-AC verdict, PR URL |
