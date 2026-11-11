# Chirp Logged-Out Experience — Subtree Hub

## Project Context

**Status**: Active
**Issue**: GitHub issue #35 — "Logged-out reading and a useful landing with accurate states"
**Branch**: `work/chirp-logged-out` (from main at `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`)
**Repository**: `Nousix-LLC/nswe-demo`

### Objective

Implement the logged-out visitor experience for Chirp: a public timeline readable without an
account, public user profiles reachable from it, and a landing that is useful even when there
is no content yet. No authentication must be required to reach these screens.

### Scope

**In Scope:**
- Public timeline API endpoint (unauthenticated GET) in chirp-server
- Public user profile API endpoint (unauthenticated GET) in chirp-server
- chirp-frontend home/landing route showing the public timeline with accurate states
- Public user profile view in chirp-frontend
- Visible sign-up and sign-in navigation from the landing
- Unit and integration tests for new API endpoints
- Component/wasm tests for frontend states (loading, empty, error, end-of-list)
- One PR into main closing issue #35

**Out of Scope:**
- Authenticated features (posting, following, notifications)
- Removing existing authentication where it already exists
- Force-push to main

### Success Criteria (Acceptance Criteria from issue #35)

- **AC-1**: Logged-out visitor can load home/public timeline and open user profile without sign-up/sign-in.
- **AC-2**: On arrival with no content, visitor sees a clear "what chirp is" statement + sign-up/sign-in route.
- **AC-3**: If timeline fails to load, a clear recoverable message is shown (not a broken screen).
- **AC-4**: "Create an account" route is visible on landing and sign-in screen, and leads to sign-up.
- **AC-5**: Loading, empty, error, and end-of-list states are each visually distinct, never blank.

---

## Constraints and Requirements

### Technical Constraints

- Rust/WASM stack: Ferric reactive framework, Axum web server, existing durable persistence
- Ferric framework: signals, component model, DOM rendering, router (PR #203), async resources + form/event binding (PR #193), SSR render_to_string + hydration (PR #228)
- CI must pass: `fmt`, `clippy`, `test`, `wasm`, `doc`, `image` checks
- Branch: `work/chirp-logged-out` from main at `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`

### Process Constraints

- One PR into main with `Closes #35` as plain text in the description body
- No host paths, internal addresses, or taskflow references in anything committed or posted to GitHub
- No force-push to main

### Quality Requirements

- Each of loading/empty/error/end-of-list states needs at least one test
- API endpoints need unit and integration tests
- CI must pass before the PR is considered done

---

## Cut Rationale

Three candidate cuts were considered:

**A — by layer (REJECTED):** Backend layer child + Frontend layer child. Rejected because the
backend and frontend are separate crates with no shared write targets, so this would work
mechanically, but the "layer" framing puts both layers at the same dependency level with no
natural skeleton that proves the seam end-to-end before both widen.

**B — exploration-first fan-out (CHOSEN):** One exploration child reads the codebase and creates
the branch; then backend and frontend spokes run in parallel against a frozen API spec; then a
synthesis gate commits, creates the PR, and verifies. Chosen because:
- Ownership is disjoint: backend only touches `crates/chirp-server/`, frontend only touches
  `crates/chirp-frontend/`, synthesis handles git operations.
- The exploration child produces an analysis that removes redundant codebase reads from the spokes.
- The contract (public_api_spec.md) freezes the JSON response shape so frontend can be
  written against a stable spec regardless of backend progress.

**C — monolithic (REJECTED):** Single child does everything. Rejected — well over the L-band
size (this is the shape that caused r1–r3 to stall).

---

## Subtree Methodology Posture

**Dominant task type:** "Writing new code" (new feature in existing Rust codebase) across both
server-side Axum and client-side Ferric WASM.

**Primary bundles:**
- `rust` — dominant; covers Axum web services, ownership/borrowing, testing, error handling
- `core` — coding standards, error handling, commit practices
- `testing` — unit, integration, and wasm-bindgen-test coverage

**Cross-cutting methodology bindings across the subtree:**
- `rust/Rust_Web_Services_Axum_Methodology.md` binds the backend spoke (Axum route handlers)
- `rust/Rust_WebAssembly_Browser_Methodology.md` binds the frontend spoke (Ferric WASM)
- `rust/Rust_Testing_Methodology.md` binds both spokes (unit + integration tests)
- `operations/GitWorkflow_PR_Lifecycle_Methodology.md` binds the synthesis spoke

**Suggestion, not prescription:** Descendant agents retain final judgment on what they load.

---

## Subtree-Wide Constraints

1. **No authentication added to new public routes** — the new GET endpoints MUST NOT require a
   Bearer token or session cookie.
2. **Do not remove existing auth** from routes that currently require it.
3. **Branch is `work/chirp-logged-out`** — all commits go on this branch.
4. **CI must pass** — `cargo fmt --check`, `cargo clippy`, `cargo test`, `cargo wasm`, `cargo doc`, docker image build.
5. **No internal paths or addresses** in anything committed to git or posted to GitHub.
6. **Ferric API surface**: use the existing Ferric signals, `Resource`, `Router`, `hydrate`, `render_to_string` APIs — do not introduce new framework changes.
7. **JSON response shape**: compose against `contracts/public_api_spec.md` — do not independently design a different shape.

---

## Input Specifications

### Primary Data Sources

| Source | Location | Purpose |
|--------|----------|---------|
| Design docs | `design/product-requirements.md`, `design/experience-design.md`, `design/release-bar.md` | Requirements and UX specs |
| Chirp server | `crates/chirp-server/` | Existing Axum API, routes, auth, persistence |
| Chirp frontend | `crates/chirp-frontend/src/` | Existing Ferric components and router |
| Ferric framework | `crates/ferric/src/` | Router, SSR, hydration, signals, async resources |
| Contracts | `taskflow/dags/chirp-logged-out-r4/contracts/` | Frozen API spec and ownership manifest |

---

## Task Structure

### Overview

```
_GLOBAL.md (this document)
├── contracts/
│   ├── _MANIFEST.yaml
│   └── public_api_spec.md
├── SUBTASK_explore_and_setup/
│   └── _BRIEF.md
├── SUBTASK_backend/
│   └── _BRIEF.md
├── SUBTASK_frontend/
│   └── _BRIEF.md
└── SUBTASK_synthesis/
    └── _BRIEF.md
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_explore_and_setup` | none | Read design docs + existing code, create branch, produce codebase analysis | `SUBTASK_explore_and_setup/analysis.md` |
| `SUBTASK_backend` | `SUBTASK_explore_and_setup` | Implement public API endpoints in chirp-server with tests | Commits in `crates/chirp-server/` |
| `SUBTASK_frontend` | `SUBTASK_explore_and_setup` | Implement public UI components in chirp-frontend with tests | Commits in `crates/chirp-frontend/` |
| `SUBTASK_synthesis` | `SUBTASK_backend`, `SUBTASK_frontend` | Commit all work, create PR, verify CI, write SYNTHESIS.md | `SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_explore_and_setup ──┬──> SUBTASK_backend ──┐
                            └──> SUBTASK_frontend ──┴──> SUBTASK_synthesis
```

---

## Contract

**Contract location**: `contracts/` (read-only for all descendants)
**Contract kind**: `yaml_schema` + `markdown` API spec

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/public_api_spec.md` | API specification | JSON response shapes for the two public endpoints |
| `contracts/_MANIFEST.yaml` | Ownership manifest | Per-child module ownership + identities |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `crates/chirp-server/src/routes/public_*.rs` (new files) | `SUBTASK_backend` |
| `crates/chirp-server/src/routes/mod.rs` (new pub mod entry) | `SUBTASK_backend` |
| `crates/chirp-server/**` (all server files) | `SUBTASK_backend` |
| `crates/chirp-frontend/src/pages/home.rs` (or equivalent new file) | `SUBTASK_frontend` |
| `crates/chirp-frontend/src/pages/profile.rs` (or equivalent new file) | `SUBTASK_frontend` |
| `crates/chirp-frontend/**` (all frontend files) | `SUBTASK_frontend` |
| Git branch creation, staging, committing, PR creation | `SUBTASK_synthesis` |
| Codebase analysis document | `SUBTASK_explore_and_setup` |

### Identities (must hold across combined output)

- [ ] Every new GET endpoint returns 200 without an Authorization header
- [ ] The home/landing route is accessible from the frontend router without auth
- [ ] Loading, empty, error, and end-of-list states are each represented by distinct component states
- [ ] A "sign up" or "create account" link is reachable from the landing
- [ ] CI checks pass on the combined output

### Derived Artifacts

- `contracts/public_api_spec.md` — read by both `SUBTASK_backend` (implements it) and `SUBTASK_frontend` (composes against it)

---

## Output Specifications

| Deliverable | Format | Location | Description |
|-------------|--------|----------|-------------|
| Codebase analysis | Markdown | `SUBTASK_explore_and_setup/analysis.md` | Existing API surface, routing, what needs adding |
| Backend implementation | Rust code | `crates/chirp-server/` | New public GET endpoints + tests |
| Frontend implementation | Rust/WASM | `crates/chirp-frontend/` | Public timeline + profile components + tests |
| SYNTHESIS.md | Markdown | `taskflow/dags/chirp-logged-out-r4/SYNTHESIS.md` | Per-AC verification + PR URL |
