# Task: chirp-server API Surface Analysis

## Task Specification

**Slug**: SUBTASK_server_analysis
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-coder

### Objective

Read the chirp-server Rust source code to map the existing API surface: all GET endpoints and
their auth requirements, the router setup file, the auth middleware extractor type, and the
persistence layer types used by handlers. Also read `contracts/public_api_spec.md` and produce
an API spec verdict: does a matching public timeline endpoint exist, and is the existing
pagination pattern consistent with the spec's `before`/`has_more` approach.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/_GLOBAL.md` | Project constraints |
| Contracts manifest | `taskflow/dags/chirp-logged-out-r4/contracts/_MANIFEST.yaml` | Required output structure |
| API contract spec | `taskflow/dags/chirp-logged-out-r4/contracts/public_api_spec.md` | The frozen public API spec |
| chirp-server source | `crates/chirp-server/src/` | Server route handlers, auth middleware, router |

All paths are relative to `/home/user/nousix-runtime/nswe-demo`.

---

## Process Specification

1. Explore `crates/chirp-server/src/` to understand directory layout (Glob, then read key files).
2. Find the router setup file (likely `main.rs`, `router.rs`, or `routes/mod.rs`) — identifies
   where new routes are registered.
3. Read route handler files to list all GET endpoints with their auth requirements:
   - Which extractors do they use? (e.g. `AuthUser`, `OptionalAuthUser`, `Extension<...>`, or no auth)
   - Does a public (unauthenticated) timeline endpoint already exist?
   - Does a public user profile endpoint already exist?
4. Find and document the auth middleware extractor type(s) — the type name the handlers use to
   require or optionally accept an authenticated user.
5. Identify persistence types used in route handlers (e.g. connection pool, repository pattern,
   `State<...>` extractors).
6. Read `taskflow/dags/chirp-logged-out-r4/contracts/public_api_spec.md` — the frozen API spec.
7. Compare the spec against the existing server:
   - Public timeline GET: does one exist? Path match? Response shape match? Pagination match?
   - Public user profile GET: does one exist? Path match?
   - Recommend: adopt existing shape or spec shape (the backend spoke makes the final call)
8. Write `server_findings.md` with the required sections.
9. Write `COMPLETE.md`.

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `server_findings.md` |
| Location | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/SUBTASK_server_analysis/` |

### Required Sections in `server_findings.md`

```markdown
# chirp-server API Surface Findings

## Existing Routes

| Path | Method | Auth Required | Handler File |
|------|--------|---------------|--------------|
| ...  | GET    | yes/no/optional | ...         |

## Public Endpoint Status
- Public timeline GET: exists at <path> | does not exist
  - If exists: response shape summary, pagination approach
- Public user profile GET: exists at <path> | does not exist

## Router Setup
- Router registration file: <path>
- Recommended new file for public handlers: <path>

## Auth Extractor
- Auth extractor type name: <e.g. AuthUser / Extension<User> / etc.>
- Optional auth extractor type name: <if any>
- Usage pattern (how to require vs make optional)

## Persistence Types
- Primary state/pool type: <type>
- Usage in handlers: <brief description>

## API Spec Verdict
- Spec endpoint: GET <path> (public timeline) → <match | conflict | absent>
  - If conflict: existing path=<x>, spec path=<y>, response diff=<z>
- Spec endpoint: GET <path> (user profile) → <match | conflict | absent>
- Pagination approach: spec uses `before` cursor + `has_more` → consistent with existing? yes/no
  - If inconsistent: existing pattern=<describe>
- Recommendation for SUBTASK_backend: <adopt existing | use spec shape> — rationale

## Files to Modify
- Router registration: <path> — add new public route registrations
- Recommended new handler file: <path>
- Any other files that need changes
```

---

## Success Criteria

- [ ] All GET routes listed with auth requirements
- [ ] Public timeline endpoint status determined (exists/absent)
- [ ] Router registration file path identified
- [ ] Auth extractor type name documented
- [ ] API spec verdict produced (match/conflict/absent for each public endpoint)
- [ ] `server_findings.md` exists with all required sections
- [ ] `COMPLETE.md` written

---

## Suggested Methodology Files

**Task-type row:** Code analysis of an Axum-based Rust server — Primary: `rust`, Supporting: `core`

**Specific files:**
- `rust/Rust_Web_Services_Axum_Methodology.md` — Rationale: understanding Axum route handlers, extractors, router setup, and state types requires knowing Axum patterns.
- `core/BestPractices_Coding_Standards_Methodology.md` — Rationale: structured output standards.

**These are SUGGESTIONS.** The child agent is the final judge.

## Inherited Constraints

- Repository is at `/home/user/nousix-runtime/nswe-demo`
- Read-only — do NOT modify any server source files
- Note: the cluster SSH pattern from CLAUDE.md is NOT needed for this task

## Out-of-Scope Methodologies

- Frontend methodologies — the server analysis is backend/Axum only
