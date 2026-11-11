# SUBTASK_backend: Backend Public API Endpoints

## Task Specification

**Slug**: SUBTASK_backend  
**Task Kind**: standard  
**Depends on**: SUBTASK_explore  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

Implement public (unauthenticated) API endpoints in chirp-server for the logged-out visitor experience: a public timeline endpoint (GET list of recent chirps) and a public user profile endpoint (GET user profile + their chirps). Include integration tests for both endpoints. Commit the changes to the `work/chirp-logged-out` branch.

### Context

This task is part of the Chirp Logged-Out Visitor Experience (r8) (see `../_GLOBAL.md`). It depends on SUBTASK_explore, which provides `SUBTASK_explore/analysis.md` — the design of exactly what routes to add and what response shapes to use.

**Dependents**: SUBTASK_frontend reads this task's committed API so it can build frontend components against it.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Scope, constraints, CI requirements |
| Codebase analysis | `../SUBTASK_explore/analysis.md` | Exact API shapes, files to modify, auth patterns |
| Chirp server source | `/home/user/nousix-runtime/nswe-demo/crates/chirp-server/` | Base for all modifications |
| CLAUDE.md | `/home/user/nousix-runtime/nswe-demo/CLAUDE.md` | SSH patterns if cluster verification needed |

---

## Process Specification

Using the analysis from SUBTASK_explore:

1. **Implement the public timeline endpoint**: Add a route that serves recent chirps without requiring authentication. The route shape, URL, and response format are specified in `analysis.md`.

2. **Implement the public user profile endpoint**: Add a route for fetching a public user profile (and their recent chirps) without authentication. Shape from `analysis.md`.

3. **Auth middleware**: Ensure the new routes bypass the authentication middleware that protects existing authenticated routes. Do not remove auth from existing routes.

4. **Pagination**: If `analysis.md` specifies pagination for the timeline (cursor-based or page-based), implement it.

5. **Integration tests**: Write Rust integration tests for both new endpoints. Each test should:
   - Test the happy path (endpoint returns expected data shape)
   - Test an empty state (no chirps returns valid empty response)
   - Test a not-found case (for user profile with unknown username, returns 404)
   These tests run with `cargo test`.

6. **Verify CI requirements**: Run `cargo fmt --check`, `cargo clippy`, `cargo test` locally (or via the SSH remote if local tooling is not available). All must pass.

7. **Commit**: Commit all backend changes to the `work/chirp-logged-out` branch with a clear commit message. Do not include host paths, internal addresses, or taskflow references in commit messages.

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Format | Git commits on `work/chirp-logged-out` |
| Scope | `crates/chirp-server/` only |

The committed code is the deliverable. Additionally produce:

| Attribute | Value |
|-----------|-------|
| Filename | `backend_summary.md` |
| Location | `SUBTASK_backend/` (this task's workspace) |

The `backend_summary.md` documents:
- Which routes were added (URL, method, auth status)
- Response shapes (as Rust types or example JSON)
- Test coverage (which test cases were added)
- Any deviations from the analysis document and why

---

## Success Criteria

- [ ] Public timeline endpoint implemented and returns chirps without auth
- [ ] Public user profile endpoint implemented and returns profile without auth
- [ ] No existing authenticated routes were modified to remove auth
- [ ] Integration tests added for both endpoints (happy path, empty, not-found where applicable)
- [ ] `cargo fmt --check` passes
- [ ] `cargo clippy` passes (warnings treated as errors per project CI)
- [ ] `cargo test` passes
- [ ] Changes committed to `work/chirp-logged-out` branch
- [ ] `backend_summary.md` written with route shapes and test coverage

---

## Suggested Methodology Files

**Task-type row matched**: "Rust web services / Axum / Tower / server-side HTTP" → Primary: `rust`, Supporting: `framework-design`

Specific files:
- `rust/Rust_Web_Services_Axum_Methodology.md` — Axum route registration, handler patterns, state extraction, middleware layering; rationale: this is the core methodology for adding routes to the existing Axum-based chirp-server
- `rust/Rust_Error_Handling_Methodology.md` — consistent error type usage; rationale: new handlers must return errors in the same style as existing ones
- `rust/Rust_Testing_Methodology.md` — Rust integration test patterns; rationale: writing integration tests for HTTP endpoints
- `core/BestPractices_Error_Handling_Methodology.md` — error handling principles

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but is the final judge of what its work requires.

## Inherited Constraints

- All changes go to `crates/chirp-server/` only (do not modify chirp-frontend or ferric in this task)
- Branch: `work/chirp-logged-out`
- `cargo fmt`, `cargo clippy`, `cargo test` must all pass after this task's work
- Do not remove authentication from existing routes
- No host paths, internal addresses, or taskflow references in committed code or commit messages
- Implement the route shapes exactly as specified in `SUBTASK_explore/analysis.md`

## Out-of-Scope Methodologies

- Frontend methodologies (Framework Design, React/WASM patterns) — that belongs to SUBTASK_frontend
- Synthesis methodology — this task is not the synthesis gate
