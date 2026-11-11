# Task: Frontend Route Survey

## Task Specification

**Slug**: SUBTASK_explore-survey-frontend  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

Read `crates/chirp-frontend/` (or the equivalent frontend crate) and document the router configuration, existing routes, and what each route currently renders for a logged-out visitor. Identify which routes need changes to support the logged-out experience.

### Context

This task is part of the Codebase Exploration subtree for Chirp Logged-Out r7. See `../_GLOBAL.md` for subtree context.

**Dependents**: SUBTASK_explore-synthesis (reads frontend-survey.md)

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Subtree constraints and context |
| Project context | `../../_GLOBAL.md` | Project ACs and scope |
| Frontend codebase | `crates/chirp-frontend/` (or equivalent) | Existing router, routes, components |

The frontend codebase lives in `Nousix-LLC/nswe-demo` on `main` at `cb1ced3`. Read via the cloned repository on the build server (SSH) or `gh api`. First glob the crate roots to confirm which crate contains the frontend source.

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `frontend-survey.md` |
| Location | `SUBTASK_explore-survey-frontend/` (this workspace) |

### Output Structure

`frontend-survey.md` MUST include:

1. **Crate Structure** — Top-level file layout of the frontend crate; relevant Cargo.toml dependencies; build target (WASM / native).

2. **Router Configuration** — How the Ferric router is set up: file path, route registration pattern, any authentication guards or redirects.

3. **Route Inventory** — Table of all current routes:
   - Path pattern
   - Handler/component
   - Authentication gate (yes/no/conditional)
   - What a logged-out visitor currently sees (redirected to login, blank, error, or rendered content)

4. **Home/Landing Route Assessment** — What does the home/root route currently render for a logged-out visitor?
   - Is it gated behind authentication?
   - Does it show any timeline content?
   - Does it show a useful empty/signup state?

5. **User Profile Route Assessment** — Does a `/user/:username` or equivalent route exist?
   - If yes: what does it currently render? Is it gated?
   - If no: what path pattern would fit the existing convention?

6. **Component Inventory** — List existing components that could be reused or adapted for the public timeline and profile views.

7. **Gaps** — What routes or components clearly need to be added or changed.

---

## Success Criteria

- [ ] Router configuration documented with file location
- [ ] Route inventory covers all current routes
- [ ] Home/landing route assessed for logged-out behavior
- [ ] User profile route presence/absence and current behavior documented
- [ ] Component inventory complete enough for SUBTASK_frontend-ui to plan its work
- [ ] frontend-survey.md written at this workspace

---

## Suggested Methodology Files

**Task-type row matched**: "Building React components" / frontend architecture → Frontend; "SSR / hydration in a Rust UI framework" → Framework Design + Rust

**Primary files to load**:
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — rationale: Ferric is a Rust UI framework with signals and SSR; understanding the router and component patterns requires the UI-reactivity lens
- `frontend/Frontend_Application_Architecture_Methodology.md` — rationale: provides the architecture vocabulary for describing routing, component structure, and authentication gating

These are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.

## Inherited Constraints

- Exploration only — no code changes to `crates/chirp-frontend/` or any other crate
- Repository: `Nousix-LLC/nswe-demo`; codebase is on `main` at `cb1ced3`
- No host paths, internal addresses, or taskflow references in output

## Out-of-Scope Methodologies

- Testing methodologies — this task writes no tests
- Backend/API methodologies — deferred to survey-backend
