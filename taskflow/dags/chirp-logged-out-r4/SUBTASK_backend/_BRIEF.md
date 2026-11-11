# Task: Backend — Public API Endpoints

## Task Specification

**Slug**: SUBTASK_backend
**Task Kind**: standard
**Depends on**: SUBTASK_explore_and_setup
**Status**: Pending
**Assigned To**: swe-coder

### Objective

Implement the two public (unauthenticated) API endpoints in `crates/chirp-server` as defined in
the frozen API spec, write unit and integration tests for them, and ensure the crate compiles
cleanly with `cargo fmt`, `cargo clippy`, and `cargo test` passing.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `taskflow/dags/chirp-logged-out-r4/_GLOBAL.md` | Project constraints |
| API spec (frozen) | `taskflow/dags/chirp-logged-out-r4/contracts/public_api_spec.md` | The JSON response shapes to implement |
| Ownership manifest | `taskflow/dags/chirp-logged-out-r4/contracts/_MANIFEST.yaml` | File ownership rules |
| Codebase analysis | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/analysis.md` | Specific files to create/modify, auth extractor pattern, existing routes |
| Existing server source | `crates/chirp-server/src/` | Current Axum server code to build on |

### Input Verification

Before processing:
- [ ] `analysis.md` exists (dependency was completed)
- [ ] `contracts/public_api_spec.md` is readable
- [ ] `crates/chirp-server/src/` exists

---

## Process Specification

This task implements the server-side changes. It owns ALL files under `crates/chirp-server/`.

### Reading Phase (do first)

1. Read `analysis.md` — this gives you the exact files to modify, the auth extractor pattern, and
   whether public endpoints already exist.
2. Read the relevant existing route handler files to understand patterns and types.
3. Read the persistence layer types used in existing handlers.

### Implementation Phase

**Public timeline endpoint: `GET /api/chirps`**
- If an unauthenticated public timeline endpoint already exists: verify it matches or can be
  adapted to the API spec shape; add pagination (`before` cursor + `has_more`) if absent.
- If no public endpoint exists: create a new route handler that:
  - Uses NO auth extractor (or an optional one that does not return 401 when absent)
  - Queries the persistence layer for recent chirps
  - Returns the JSON shape defined in `contracts/public_api_spec.md`
  - Supports optional `before` and `limit` query parameters

**Public user profile endpoint: `GET /api/users/:username/chirps`**
- If an unauthenticated user profile endpoint already exists: verify and adapt to spec.
- If no public endpoint exists: create a new route handler that:
  - Accepts `:username` as a path parameter
  - Returns 404 with `{"error": "user not found"}` if the user does not exist
  - Returns the user info + chirps JSON shape from the spec

**Route registration**
- Register both new routes in the Axum router setup file (identified in `analysis.md`)
- Follow the existing module layout convention

**Tests**
- Unit tests for the new handler logic (at minimum: happy path, 404 case for profile, empty timeline case)
- Integration test: test the route returns 200 without an Authorization header (confirms the route is truly public)
- Each required test state from the spec must have at least one test

### Quality Phase

After implementation:
- Run `cargo fmt` and fix any formatting issues
- Run `cargo clippy` and fix all warnings
- Run `cargo test` and ensure all tests pass
- These checks are the CI floor — the synthesis task will re-verify but start with them passing

---

## Output Specification

### Primary Output

This task's output is code committed to files under `crates/chirp-server/`. The declared output
file (for the lifecycle record) is:

| Attribute | Value |
|-----------|-------|
| Filename | `COMPLETE.md` |
| Location | `taskflow/dags/chirp-logged-out-r4/SUBTASK_backend/` |

The COMPLETE.md MUST list:
- Files created or modified under `crates/chirp-server/`
- Tests written and what they verify
- Results of `cargo fmt --check`, `cargo clippy`, `cargo test`
- Any deviations from the API spec and rationale

---

## Success Criteria

- [ ] `GET /api/chirps` returns 200 with correct JSON shape without auth header
- [ ] `GET /api/users/:username/chirps` returns 200 for existing user, 404 for missing user, without auth header
- [ ] At least one test per handler (happy path + public-access assertion)
- [ ] `cargo fmt --check` passes on `crates/chirp-server/`
- [ ] `cargo clippy` passes (zero warnings treated as errors)
- [ ] `cargo test` passes for `crates/chirp-server/`
- [ ] COMPLETE.md written and status reported as completed

---

## Suggested Methodology Files

**Task-type rows matched:**
- "Rust web services / Axum / Tower / server-side HTTP" — Primary: `rust`, Supporting: `framework-design`
- "Writing Rust code" — Primary: `rust`, Supporting: `core`, `code-quality`
- "Rust testing" — Primary: `rust`, Supporting: `testing`

**Specific files:**
- `rust/Rust_Web_Services_Axum_Methodology.md` — Rationale: this task writes Axum route handlers. Load first.
- `rust/Rust_Error_Handling_Methodology.md` — Rationale: route handlers return Results; error handling is central.
- `rust/Rust_Testing_Methodology.md` — Rationale: writing unit + integration tests for the new endpoints.
- `core/BestPractices_Error_Handling_Methodology.md` — Rationale: error response shapes and handler errors.

**These are SUGGESTIONS.** The child agent is the final judge.

## Inherited Constraints

- Owns ONLY files under `crates/chirp-server/` — do NOT touch `crates/chirp-frontend/` or any other crate
- Do NOT add auth requirements to the new public routes
- Do NOT remove auth from routes that currently require it
- Compose against `contracts/public_api_spec.md` — if the existing server uses a different JSON shape, follow the analysis guidance; note deviations in COMPLETE.md
- Branch is already `work/chirp-logged-out` (created by SUBTASK_explore_and_setup) — no branch operations needed
- Do NOT put host paths, internal addresses, or taskflow references in source code or comments destined for the repo

## Out-of-Scope Methodologies

- `auth/` bundle — this task explicitly removes auth requirements; no new auth flow design
- `frontend/` bundle — backend only
- `gitops/` bundle — no cluster deployment
