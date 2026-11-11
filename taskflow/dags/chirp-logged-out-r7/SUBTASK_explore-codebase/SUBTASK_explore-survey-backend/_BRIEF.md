# Task: Backend API Survey

## Task Specification

**Slug**: SUBTASK_explore-survey-backend  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

Read `crates/chirp-server/` and document every existing API endpoint: its URL pattern, HTTP method, authentication requirements, and handler signature. For each of the two target endpoints — public timeline and public user profile — determine whether it exists and what changes (if any) are needed to satisfy the inherited API surface contract.

### Context

This task is part of the Codebase Exploration subtree for Chirp Logged-Out r7. See `../_GLOBAL.md` for subtree context.

**Dependents**: SUBTASK_explore-synthesis (reads backend-survey.md)

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Subtree constraints and context |
| Project context | `../../_GLOBAL.md` | Project ACs and scope |
| Public API contract | `../../contracts/public_api_contract.md` | Required endpoints to survey against (READ-ONLY) |
| Ownership manifest | `../../contracts/_MANIFEST.yaml` | Contract bindings (READ-ONLY) |
| Server codebase | `crates/chirp-server/` | Existing routes, handlers, middleware |

The server codebase lives in `Nousix-LLC/nswe-demo` on `main` at `cb1ced3`. Read via the cloned repository on the build server (SSH) or `gh api`.

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `backend-survey.md` |
| Location | `SUBTASK_explore-survey-backend/` (this workspace) |

### Output Structure

`backend-survey.md` MUST include:

1. **Crate Structure** — Top-level file layout of `crates/chirp-server/`; entrypoint; Cargo.toml dependencies relevant to routing and auth.

2. **Endpoint Inventory** — Table of all current routes:
   - HTTP method + URL pattern
   - Handler function name and file
   - Authentication requirement (required / optional / none)
   - Brief description

3. **Public Timeline Endpoint Assessment** — Does an unauthenticated GET endpoint for a list of chirps exist?
   - If yes: URL, auth requirement, response type
   - If no: suggested URL and handler location

4. **Public User Profile Endpoint Assessment** — Does an unauthenticated GET endpoint for a user's public profile and chirps exist?
   - If yes: URL, auth requirement, response type
   - If no: suggested URL and handler location

5. **Auth Middleware Pattern** — How is authentication enforced in the router? (Axum extractors, middleware layers, JWT validation)

6. **Recommendation** — For each target endpoint: add new, make auth optional, or reuse with changes? Brief rationale.

7. **Handler Patterns** — The two or three handler implementations that best illustrate the existing patterns SUBTASK_backend-api should follow.

---

## Success Criteria

- [ ] Endpoint inventory covers all current routes
- [ ] Public timeline endpoint assessed with finding documented
- [ ] Public user profile endpoint assessed with finding documented
- [ ] Auth middleware pattern documented
- [ ] Recommendation recorded for each target endpoint
- [ ] backend-survey.md written at this workspace

---

## Suggested Methodology Files

**Task-type row matched**: "Writing new code" → Core; "Rust web services / Axum / Tower / server-side HTTP" → Rust (Web Services / Axum)

**Primary files to load**:
- `rust/Rust_Web_Services_Axum_Methodology.md` — rationale: Axum is the server framework; understanding how routes are registered, how middleware layers apply authentication, and what handler patterns exist is the core of this survey
- `core/BestPractices_Coding_Standards_Methodology.md` — rationale: provides the lens for evaluating existing code quality and identifying idiomatic patterns to follow in SUBTASK_backend-api

These are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.

## Inherited Constraints

- Exploration only — no code changes to `crates/chirp-server/`
- Repository: `Nousix-LLC/nswe-demo`; codebase is on `main` at `cb1ced3`
- Parent contracts at `../../contracts/` are READ-ONLY
- No host paths, internal addresses, or taskflow references in output

## Out-of-Scope Methodologies

- Testing methodologies — this task writes no tests
- Frontend/component methodologies — deferred to survey-frontend
