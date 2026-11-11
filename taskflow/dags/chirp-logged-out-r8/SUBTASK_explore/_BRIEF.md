# SUBTASK_explore: Codebase Exploration and Branch Setup

## Task Specification

**Slug**: SUBTASK_explore  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

Read the existing codebase and design documents to understand what already exists and what must be built for the logged-out visitor experience. Determine the precise API changes needed in chirp-server and the component/routing structure needed in chirp-frontend. Create the git branch `work/chirp-logged-out` from main. Produce a detailed analysis document that downstream tasks use as their primary input.

### Context

This task is part of the Chirp Logged-Out Visitor Experience (r8) implementation (see `_GLOBAL.md` in the parent workspace). It is the first task in the pipeline and has no dependencies.

**Dependents**: SUBTASK_backend depends on this task's output.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Acceptance criteria, scope, constraints |
| Product requirements | `/home/user/nousix-runtime/nswe-demo/design/product-requirements.md` | REQ-PROD-013, 014, 015 |
| Experience design | `/home/user/nousix-runtime/nswe-demo/design/experience-design.md` | Screens, states, REQ-UX-002, 030-032 |
| Release bar | `/home/user/nousix-runtime/nswe-demo/design/release-bar.md` | BAR-011 |
| Chirp server | `/home/user/nousix-runtime/nswe-demo/crates/chirp-server/` | Existing routes, auth middleware, models |
| Chirp frontend | `/home/user/nousix-runtime/nswe-demo/crates/chirp-frontend/` | Existing components, routes, App structure |
| Ferric framework | `/home/user/nousix-runtime/nswe-demo/crates/ferric/src/` | Router API, AsyncResource, SSR/hydration APIs |
| CLAUDE.md | `/home/user/nousix-runtime/nswe-demo/CLAUDE.md` | SSH command patterns for kubectl |

---

## Process Specification

Explore the codebase to answer these questions:

1. **Backend API surface**: What routes does chirp-server currently expose? Is there already a public (unauthenticated) timeline endpoint or public user profile endpoint? What authentication middleware is in use? What are the Chirp data models (Chirp struct, User struct)?

2. **Frontend structure**: What routes does chirp-frontend currently register? What is the existing App component structure? How is the router configured (Ferric router API)?

3. **Ferric API surface**: What APIs exist in the ferric crate for async resources, SSR, hydration, and routing? What is the idiomatic pattern for a component with loading/empty/error states?

4. **API shape design**: Based on what exists, design the minimal public API additions needed:
   - `GET /api/chirps` or similar — returns a list of recent chirps without auth (pagination?)
   - `GET /api/users/:username` or similar — returns a public user profile without auth
   Document the exact URL paths, HTTP methods, query parameters, and response body shapes.

5. **Frontend shape design**: Based on the router and design docs, design:
   - The home/landing route that shows the public timeline
   - The state machine: loading → (empty | populated | error), plus end-of-list detection
   - The public user profile route/component structure
   - Sign-up and sign-in navigation links

6. **Git branch**: Create the branch `work/chirp-logged-out` from main at `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`. Verify it does not already exist (if it does, check if it's up-to-date or needs resetting).

### Methodology

Apply `rust` and `architecture` bundles. Prioritize understanding existing patterns so downstream tasks extend them consistently rather than introducing new patterns.

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `analysis.md` |
| Location | `SUBTASK_explore/` (this task's workspace) |

### Output Structure

The `analysis.md` must cover:

```markdown
# Chirp Logged-Out: Codebase Analysis

## Branch Status
- Whether `work/chirp-logged-out` was created or already existed
- Current HEAD SHA

## Backend: Existing API Routes
- List of current routes with auth/unauth status
- Whether public timeline endpoint exists
- Whether public user profile endpoint exists

## Backend: Data Models
- Chirp struct fields (from server models)
- User/Profile struct fields
- Relevant response/serialization types

## Backend: Auth Middleware
- How existing authenticated routes are protected
- What needs to change for public routes

## Proposed Backend API Contract
- Exact route paths, HTTP methods, query params, response shapes
- Example response JSON for timeline and user profile

## Frontend: Existing Structure
- Current router registration
- Existing routes and components
- App component structure

## Frontend: Ferric API Patterns
- How to create a route in this app
- AsyncResource pattern for data fetching
- Component pattern for loading/empty/error states

## Proposed Frontend Structure
- Home/landing route: path, component name, state handling
- Public user profile route: path, params, component name
- Sign-up/sign-in navigation approach

## Implementation Notes for SUBTASK_backend
- Specific files to modify
- Specific changes needed

## Implementation Notes for SUBTASK_frontend
- Specific files to create/modify
- Specific Ferric APIs to use
```

---

## Success Criteria

- [ ] All design documents read and key requirements extracted
- [ ] Existing backend routes catalogued with auth status
- [ ] Existing frontend routes and structure understood
- [ ] Ferric async resource and state patterns identified
- [ ] Public API endpoint shapes designed (URL, method, params, response shape)
- [ ] Frontend component/route structure designed
- [ ] Git branch `work/chirp-logged-out` created or verified
- [ ] `analysis.md` written with all required sections

---

## Suggested Methodology Files

**Task-type row matched**: "Writing Rust code" → Primary: `rust`, Supporting: `core`, `code-quality`

Specific files:
- `rust/Rust_Web_Services_Axum_Methodology.md` — understanding the existing Axum route registration patterns in chirp-server; rationale: this task reads Axum handler code to catalogue existing routes
- `architecture/Architecture_API_Design_Methodology.md` — designing the new public API shapes; rationale: this task designs the endpoint contract that downstream tasks build against
- `operations/GitWorkflow_PR_Lifecycle_Methodology.md` — git branch creation pattern; rationale: this task creates the work branch

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but is the final judge of what its work requires.

## Inherited Constraints

- Repository is at `/home/user/nousix-runtime/nswe-demo`
- Branch: `work/chirp-logged-out`, branched from `main` at `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`
- Do not modify production code in this task — exploration and branch setup only
- No host paths, internal addresses, or taskflow references in any committed content
- SSH commands required for kubectl — see `CLAUDE.md`

## Out-of-Scope Methodologies

- Testing methodologies — this task does not write tests; that belongs to SUBTASK_backend and SUBTASK_frontend
- Synthesis methodology — this is not the synthesis gate task
