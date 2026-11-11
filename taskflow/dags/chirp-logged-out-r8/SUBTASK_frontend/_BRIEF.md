# SUBTASK_frontend: Frontend Logged-Out Components

## Task Specification

**Slug**: SUBTASK_frontend  
**Task Kind**: standard  
**Depends on**: SUBTASK_backend  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

Implement the frontend logged-out visitor experience in chirp-frontend using the Ferric framework: a home/landing route that shows the public timeline with accurate loading/empty/error/end-of-list states, a public user profile view, and visible sign-up and sign-in navigation from the landing. Include wasm-bindgen tests or component tests for each distinct state. Commit to the `work/chirp-logged-out` branch.

### Context

This task is part of the Chirp Logged-Out Visitor Experience (r8) (see `../_GLOBAL.md`). It depends on SUBTASK_backend, which has already committed the public API endpoints. The backend's committed code is available on the `work/chirp-logged-out` branch; use the actual endpoints when writing fetch calls and tests.

The analysis from SUBTASK_explore (`../SUBTASK_explore/analysis.md`) describes the frontend structure and Ferric API patterns; the backend summary (`../SUBTASK_backend/backend_summary.md`) documents the exact API shapes to build against.

**Dependents**: SUBTASK_synthesis creates the PR after this task.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Acceptance criteria (AC-1 through AC-5), scope, constraints |
| Codebase analysis | `../SUBTASK_explore/analysis.md` | Frontend structure, Ferric API patterns, proposed components |
| Backend summary | `../SUBTASK_backend/backend_summary.md` | Exact API endpoint URLs, response shapes to build against |
| Ferric source | `/home/user/nousix-runtime/nswe-demo/crates/ferric/src/` | Router, AsyncResource, SSR, hydration APIs |
| Chirp frontend source | `/home/user/nousix-runtime/nswe-demo/crates/chirp-frontend/` | Existing structure to extend |
| Design docs | `design/experience-design.md` §2 Screens, §6 REQ-UX | State requirements per AC-5 |

---

## Process Specification

Using the analysis from SUBTASK_explore and the route shapes from SUBTASK_backend:

1. **Home/landing route with public timeline**: Add or update the home route in chirp-frontend to show the public timeline. This route must be accessible to unauthenticated visitors (no auth guard).

2. **State handling — four distinct states** (required by AC-5):
   - **Loading**: A visually distinct loading indicator while the timeline is being fetched
   - **Empty**: When no chirps exist, display a clear "what chirp is" statement and an obvious sign-up/sign-in route (AC-2 requirement)
   - **Error**: When the fetch fails, display a clear recoverable error message with a retry mechanism (AC-3 requirement)
   - **End-of-list**: When pagination reaches the last page, show a distinct end-of-list indicator (not a blank continuation)
   Each state must be visually distinct and must never show a blank page.

3. **Sign-up and sign-in navigation** (AC-4): Ensure visible "Sign up" and "Sign in" links are present on the landing/home view. "Create an account" (sign-up) must be reachable from the landing and from the sign-in screen.

4. **Public user profile view**: Add a route for `/user/:username` (or the path design from `analysis.md`) that shows a user's public profile and their chirps. This route must be accessible without auth.

5. **SSR consideration**: The analysis document notes whether SSR is beneficial for the home route. If SSR is used, ensure the hydration path correctly adopts the SSR-rendered DOM (Ferric's `hydrate.rs` integration).

6. **Wasm-bindgen tests**: Add at least one test per distinct state (loading, empty, error, end-of-list) for the timeline component. If the ferric framework provides component testing utilities, use them. Tests run with `cargo wasm`.

7. **Verify CI requirements**: `cargo fmt --check`, `cargo clippy`, `cargo test`, `cargo wasm` (wasm-pack test) must all pass.

8. **Commit**: Commit all frontend changes to `work/chirp-logged-out` with clear commit message. Do not include host paths, internal addresses, or taskflow references.

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Format | Git commits on `work/chirp-logged-out` |
| Scope | `crates/chirp-frontend/` only (and any shared types in `crates/chirp-types/` if needed) |

Additionally produce:

| Attribute | Value |
|-----------|-------|
| Filename | `frontend_summary.md` |
| Location | `SUBTASK_frontend/` (this task's workspace) |

The `frontend_summary.md` documents:
- Routes added/modified
- Components created (name, purpose, states handled)
- State machine summary (what triggers each state transition)
- Test coverage (which wasm tests cover which states)
- Any deviations from the analysis and why
- Whether SSR was used and how hydration is handled

---

## Success Criteria

- [ ] Home/landing route accessible without authentication
- [ ] Loading state visually distinct and never blank
- [ ] Empty state shows "what chirp is" statement + sign-up/sign-in route (AC-2)
- [ ] Error state shows recoverable message (AC-3)
- [ ] End-of-list state visually distinct from loading or error
- [ ] Sign-up and sign-in navigation visible on landing (AC-4)
- [ ] "Create an account" leads to sign-up route
- [ ] Public user profile route accessible without authentication (AC-1)
- [ ] At least one wasm test per distinct state
- [ ] `cargo fmt --check` passes
- [ ] `cargo clippy` passes
- [ ] `cargo test` passes
- [ ] `cargo wasm` (or equivalent wasm-pack test) passes
- [ ] Changes committed to `work/chirp-logged-out` branch
- [ ] `frontend_summary.md` written

---

## Suggested Methodology Files

**Task-type row matched**: "Building a UI framework / framework primitive (signals, fine-grained reactivity vs virtual DOM, SSR + hydration)" → Primary: `framework-design`, Supporting: `rust`, `frontend`

Specific files:
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — Ferric-specific: how reactive signals, async resources, SSR render_to_string, and client-side hydration work in a Rust WASM framework; rationale: this is the primary methodology for understanding how to build correct components in this framework
- `rust/Rust_WebAssembly_Browser_Methodology.md` — wasm-bindgen bindings, web-sys usage, wasm-bindgen-test patterns; rationale: the frontend code compiles to WASM and tests use wasm-bindgen-test
- `rust/Rust_Testing_Methodology.md` — Rust test organization, how to structure wasm-bindgen-test suites; rationale: AC-5 requires distinct tests per state
- `framework-design/FrameworkDesign_Incremental_Adoption_And_Interop_Methodology.md` — extending an existing app with new routes; rationale: this task adds to the existing chirp-frontend, not building from scratch

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but is the final judge of what its work requires.

## Inherited Constraints

- All changes go to `crates/chirp-frontend/` (and `crates/chirp-types/` if necessary for shared types)
- Branch: `work/chirp-logged-out`
- Build the frontend against the actual backend API committed by SUBTASK_backend
- Each distinct state (loading/empty/error/end-of-list) must be visually distinct per AC-5
- `cargo fmt`, `cargo clippy`, `cargo test`, `cargo wasm` must all pass
- Do not add authentication where there was none; do not remove it where it existed
- No host paths, internal addresses, or taskflow references in committed code

## Out-of-Scope Methodologies

- Backend Axum methodology — that work was done by SUBTASK_backend
- Synthesis methodology — this task is not the synthesis gate
