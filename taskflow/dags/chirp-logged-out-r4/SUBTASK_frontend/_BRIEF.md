# Task: Frontend — Public Timeline and Profile Components

## Task Specification

**Slug**: SUBTASK_frontend
**Task Kind**: standard
**Depends on**: SUBTASK_explore_and_setup
**Status**: Pending
**Assigned To**: swe-coder

### Objective

Implement the public (logged-out) user experience in `crates/chirp-frontend` using the Ferric
reactive framework: a home/landing route showing the public timeline with accurate loading,
empty, error, and end-of-list states; a public user profile view; visible sign-up and sign-in
navigation. Write wasm-bindgen-test or component tests for each distinct UI state. The
frontend composes against the frozen API spec in `contracts/public_api_spec.md`.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `taskflow/dags/chirp-logged-out-r4/_GLOBAL.md` | Project constraints |
| API spec (frozen) | `taskflow/dags/chirp-logged-out-r4/contracts/public_api_spec.md` | JSON response shapes to deserialize |
| Ownership manifest | `taskflow/dags/chirp-logged-out-r4/contracts/_MANIFEST.yaml` | File ownership rules |
| Codebase analysis | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/analysis.md` | Existing router, component patterns, sign-in/sign-up route paths, Ferric API usage |
| Existing frontend source | `crates/chirp-frontend/src/` | Current Ferric app code to build on |
| Ferric framework | `crates/ferric/src/` | Router, Resource, signals, SSR/hydration APIs |

### Input Verification

Before processing:
- [ ] `analysis.md` exists (dependency was completed)
- [ ] `contracts/public_api_spec.md` is readable
- [ ] `crates/chirp-frontend/src/` exists
- [ ] `crates/ferric/src/` exists

---

## Process Specification

This task implements the client-side changes. It owns ALL files under `crates/chirp-frontend/`.

### Reading Phase (do first)

1. Read `analysis.md` — this gives you the existing router file, sign-in/sign-up route paths,
   component module conventions, Ferric API usage patterns, and SSR recommendation.
2. Read the existing Ferric `Resource` and `Router` API source (or relevant portion thereof).
3. Read the existing chirp-frontend components to understand the pattern.

### Implementation Phase

**Data types and API client**

Define Rust structs matching the JSON response shapes in `contracts/public_api_spec.md`:
- `Chirp { id, content, author: ChirpAuthor, created_at, like_count }` (for timeline)
- `ChirpAuthor { username, display_name }`
- `TimelineResponse { chirps: Vec<Chirp>, has_more: bool }`
- `UserChirpResponse { user: UserInfo, chirps: Vec<OwnChirp>, has_more: bool }`
- `UserInfo { username, display_name, bio, chirp_count }`
  
Add `serde::Deserialize` derives (and `serde_json` as a dependency if not already present).

**UI state model**

Define an enum (or use the Ferric Resource states directly) for the five distinct states each
page can be in:
- `Loading` — data fetch in progress
- `Empty` — data loaded, zero items
- `Loaded(data)` — data loaded, items present
- `EndOfList` — last page loaded (has_more=false, after at least one page shown)
- `Error(message)` — fetch failed

Each state MUST render a visually distinct view — never collapse them or show a blank screen.

**Home/Landing route (public timeline)**

Create a component for the home/landing route at whatever path analysis.md identifies as the
home route (e.g. `/` or `/home`). The component MUST:
- Use Ferric's `Resource` or equivalent async primitive to fetch `GET /api/chirps`
- Render all five states distinctly:
  - `Loading`: show a spinner or "Loading..." indicator
  - `Empty`: show a "Welcome to Chirp — the place for short thoughts" (or similar) statement
    PLUS prominent "Sign in" and "Create an account" links (AC-2)
  - `Loaded`: render the list of chirps, each showing author username, content, timestamp
  - `EndOfList`: show "You've reached the end" (or similar) after the last page
  - `Error`: show "Failed to load — try again" with a retry action (AC-3)
- Always show sign-in and sign-up navigation links in the page header or landing area (AC-4)
- Support pagination: when `has_more` is true, provide a "Load more" action

**SSR integration** (if analysis.md recommends it)
- If analysis.md says SSR is beneficial for the public timeline, use Ferric's `render_to_string`
  for the initial render and `hydrate` for client-side takeover
- If not recommended or if the complexity is high, skip SSR for this feature; note the decision

**Public user profile route**

Create a component for the user profile route at a path like `/users/:username`. The component MUST:
- Accept `:username` as a route parameter
- Fetch `GET /api/users/:username/chirps`
- Render all six states: loading, empty (user exists, no chirps), loaded, end-of-list, not-found, error

**Sign-up / Sign-in navigation**

Verify that the existing sign-in and sign-up routes identified in `analysis.md` are accessible
from the landing/home page. If a "Create an account" link does not exist on the landing or
sign-in page, add one (AC-4).

**Route registration**

Register the new home route and user profile route in the existing Ferric router setup file
(identified in `analysis.md`).

**Tests**

Write tests for each distinct UI state. Options (use whatever the analysis shows is in the existing test infrastructure):
- Wasm-bindgen-test with mocked fetch responses, or
- Component render tests that assert the correct DOM structure for each state, or
- Unit tests on the state enum logic

At minimum:
- One test verifying the `Loading` state renders a loading indicator
- One test verifying the `Empty` state renders the "what is chirp" message AND sign-up/sign-in links
- One test verifying the `Error` state renders a recoverable error message (not blank)
- One test verifying the `EndOfList` state is distinct from `Loaded`

### Quality Phase

After implementation:
- Run `cargo fmt` and fix formatting
- Run `cargo clippy` on the frontend crate and fix warnings
- Run `cargo test` for the frontend crate (native tests if any)
- Run `wasm-pack test` or equivalent for wasm tests (or note in COMPLETE.md what test command to use)

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `COMPLETE.md` |
| Location | `taskflow/dags/chirp-logged-out-r4/SUBTASK_frontend/` |

The COMPLETE.md MUST list:
- Files created or modified under `crates/chirp-frontend/`
- UI states implemented and how each is visually distinct
- Tests written and what they verify
- SSR decision (used or skipped, with rationale)
- Results of `cargo fmt --check`, `cargo clippy`, `cargo test`, wasm test command

---

## Success Criteria

- [ ] Home/landing route exists and is accessible without authentication
- [ ] Loading, empty, error, and end-of-list states each render distinctly (not blank, not identical)
- [ ] Empty state shows "what chirp is" statement plus sign-up and sign-in links
- [ ] Error state shows a recoverable message (not a blank screen)
- [ ] "Create an account" / sign-up link is visible from the landing page
- [ ] User profile route exists and handles loading, empty, loaded, not-found, error states
- [ ] At least one test per distinct state (loading, empty, error, end-of-list)
- [ ] `cargo fmt --check` passes on `crates/chirp-frontend/`
- [ ] `cargo clippy` passes on `crates/chirp-frontend/`
- [ ] COMPLETE.md written and status reported as completed

---

## Suggested Methodology Files

**Task-type rows matched:**
- "Rust ↔ WebAssembly / browser bindings (wasm-bindgen, web-sys)" — Primary: `rust`, Supporting: `framework-design`
- "Building a UI framework primitive" — Primary: `framework-design`, Supporting: `rust`, `frontend`
- "Writing Rust code" — Primary: `rust`, Supporting: `core`
- "Rust testing" — Primary: `rust`, Supporting: `testing`

**Specific files:**
- `rust/Rust_WebAssembly_Browser_Methodology.md` — Rationale: Ferric is a Rust/WASM UI framework; this task builds browser-side components. Load first.
- `rust/Rust_Error_Handling_Methodology.md` — Rationale: each UI state corresponds to an outcome type; Rust error handling patterns apply.
- `rust/Rust_Testing_Methodology.md` — Rationale: wasm-bindgen-test + component state tests.
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — Rationale: Ferric's reactivity model (signals, Resources) is the core rendering mechanism.

**These are SUGGESTIONS.** The child agent is the final judge.

## Inherited Constraints

- Owns ONLY files under `crates/chirp-frontend/` — do NOT touch `crates/chirp-server/` or any other crate
- Compose against `contracts/public_api_spec.md` for the JSON response structures — do NOT design a different response shape
- Use existing Ferric API patterns identified in `analysis.md` — do NOT introduce new framework changes
- The sign-in and sign-up routes will have specific paths identified by `analysis.md` — use those paths, do not invent new ones
- Branch is already `work/chirp-logged-out` (from explore_and_setup) — no branch operations
- Do NOT put host paths, internal addresses, or taskflow references in source code or comments

## Out-of-Scope Methodologies

- `auth/` bundle — no new auth flows; the page is intentionally unauthenticated
- `rust/Rust_Web_Services_Axum_Methodology.md` — backend only; this task is client-side
- `gitops/` bundle — no cluster deployment
