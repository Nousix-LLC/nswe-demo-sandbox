# Task: Backend Public API Endpoints

## Task Specification

**Slug**: SUBTASK_backend-api  
**Task Kind**: standard  
**Depends on**: SUBTASK_explore-codebase  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

Implement the public (unauthenticated) API endpoints in `crates/chirp-server` that enable a logged-out visitor to read the public timeline and view a public user profile, satisfying AC-1. Include tests for the new endpoints.

### Context

This task is part of Chirp Logged-Out Visitor Experience r7 (see `../_GLOBAL.md` for full context, ACs, and constraints).

**Dependencies**: SUBTASK_explore-codebase (provides analysis.md — codebase survey and gap analysis)  
**Dependents**: SUBTASK_frontend-ui (reads backend-impl.md to learn API endpoint shapes)

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Parent hub | `../_GLOBAL.md` | Project context, ACs, constraints |
| Analysis | `../SUBTASK_explore-codebase/analysis.md` | Existing API surface, gaps per AC, recommended approach |
| Contracts | `../contracts/public_api_contract.md`, `../contracts/_MANIFEST.yaml` | API surface declaration to satisfy |
| Repository | `crates/chirp-server/` on branch `work/chirp-logged-out` | Codebase to modify |

---

## Output Specification

### Primary Output: `backend-impl.md`

| Attribute | Value |
|-----------|-------|
| Filename | `backend-impl.md` |
| Location | `SUBTASK_backend-api/` |

`backend-impl.md` MUST document:

1. **Endpoints Implemented**: For each public endpoint, the exact URL pattern, HTTP method, response type, and whether it was added new or made from an existing endpoint
2. **Response Shapes**: The Rust types returned (or JSON schema) so SUBTASK_frontend-ui knows what to deserialize
3. **Auth Behavior**: Explicit statement that these endpoints require no session/token
4. **Pagination Contract**: How pagination works (cursor, page number) for the timeline endpoint
5. **Test Coverage**: Which tests were added and what they verify

### Secondary Output: Code commits on branch `work/chirp-logged-out`

The backend implementation in `crates/chirp-server/` committed to the branch.

---

## Success Criteria

- [ ] At minimum one unauthenticated GET endpoint for the public timeline exists and returns chirps (or empty list) without requiring auth
- [ ] At minimum one unauthenticated GET endpoint for a public user profile exists
- [ ] Both endpoints compile cleanly with `cargo build`
- [ ] `cargo clippy` produces no errors (warnings-denied for new code)
- [ ] `cargo fmt --check` passes for modified files
- [ ] Tests exist for: successful request with chirps present, empty timeline (no chirps), user not found, and unauthenticated access (no auth headers)
- [ ] `backend-impl.md` documents the endpoint URLs and response shapes for SUBTASK_frontend-ui

---

## Suggested Methodology Files

**Task-type row matched**: "Writing new code" → Core; "Writing Rust code" → Rust; "Rust web services / Axum / Tower" → Rust Web Services Axum

**Primary files to load**:
- `rust/Rust_Web_Services_Axum_Methodology.md` — rationale: the server uses Axum; this methodology covers handler registration, state injection, middleware layering, and the right patterns for making auth optional on a route
- `rust/Rust_Error_Handling_Methodology.md` — rationale: proper error types for API responses (not found, internal error) determine downstream deserialization behavior
- `rust/Rust_Testing_Methodology.md` — rationale: Rust integration tests for Axum handlers; the endpoint tests need to run against an in-process server
- `core/BestPractices_Coding_Standards_Methodology.md` — rationale: consistency with existing handler patterns is a correctness constraint here, not just style

**Supporting files** (load if the approach reveals a need):
- `testing/Testing_Integration_Testing_Methodology.md` — if the in-process Axum test pattern needs elaboration

These are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but is the final judge of what its work requires.

## Inherited Constraints

- Branch: `work/chirp-logged-out` — all commits on this branch
- Repository: `Nousix-LLC/nswe-demo`
- Rust 2021 edition; existing Cargo workspace conventions apply
- Do NOT add authentication where it did not exist; do NOT remove authentication from existing authenticated endpoints
- Compose against `../contracts/public_api_contract.md` — the public endpoint surface MUST satisfy that declaration
- `cargo fmt --check`, `cargo clippy` (warnings-denied), and `cargo test` MUST pass for modified code
- No host paths, internal addresses, or taskflow references in committed code

## Out-of-Scope Methodologies

- Frontend/WASM methodologies — deferred to SUBTASK_frontend-ui
- Ferric framework patterns — deferred to SUBTASK_frontend-ui
- PR creation — deferred to SUBTASK_synthesis
