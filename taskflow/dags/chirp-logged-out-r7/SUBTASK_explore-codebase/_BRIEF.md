# Task: Codebase Exploration and Branch Creation

## Task Specification

**Slug**: SUBTASK_explore-codebase  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

Understand the current state of the Chirp codebase — existing API endpoints and their authentication requirements, frontend routing structure, the Ferric framework's available primitives — and read the design documents to map each acceptance criterion to a concrete implementation gap. Create the work branch from main.

### Context

This task is part of Chirp Logged-Out Visitor Experience r7 (see `_GLOBAL.md` in the parent workspace for full context, acceptance criteria, and constraints).

**Dependencies**: none  
**Dependents**: SUBTASK_backend-api (reads analysis.md)

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Parent hub | `../_GLOBAL.md` | Project context, ACs, constraints |
| Design docs | `design/product-requirements.md`, `design/experience-design.md`, `design/release-bar.md` on main branch | AC requirements, screen/state specs |
| Server codebase | `crates/chirp-server/` | Existing routes, auth middleware, handler patterns |
| Frontend codebase | `crates/chirp-frontend/` or similar | Existing routes, component structure |
| Ferric framework | `crates/ferric/` | Available primitives for async resources, router, SSR, hydration |
| Contracts | `../contracts/public_api_contract.md`, `../contracts/_MANIFEST.yaml` | API surface declaration to validate against |

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `analysis.md` |
| Location | `SUBTASK_explore-codebase/` |

### Output Structure

`analysis.md` MUST include:

1. **Branch Status**: Confirmation that `work/chirp-logged-out` has been created from `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`

2. **API Endpoint Survey**: For each of the following, document whether it exists and its auth requirements:
   - Public timeline endpoint (unauthenticated GET returning list of chirps)
   - Public user profile endpoint (unauthenticated GET)
   - Recommendation: add new endpoint, make auth optional, or reuse with changes

3. **Frontend Route Survey**: Document:
   - Home/landing route — what it currently renders for a logged-out visitor
   - User profile route — what it currently renders
   - Router configuration (Ferric router setup)

4. **Ferric Primitives Available**: List the resource/async primitives and component patterns available after PRs #193, #203, #228 — specifically what's available for async data fetching with loading/error states

5. **Per-AC Gap Analysis**: For each of AC-1 through AC-5, document what currently exists and what must be added or changed

6. **Implementation Plan Summary**: A brief account of the specific files to change for SUBTASK_backend-api and SUBTASK_frontend-ui

---

## Success Criteria

- [ ] Branch `work/chirp-logged-out` exists and is at commit `cb1ced3` (or branched from it)
- [ ] `analysis.md` documents the API endpoint survey with authentication requirements
- [ ] `analysis.md` documents the frontend route survey
- [ ] `analysis.md` has a gap analysis entry for each of AC-1 through AC-5
- [ ] No code changes made — this task is exploration only

---

## Suggested Methodology Files

**Task-type row matched**: "Writing new code" → Core; "Designing systems" → Architecture (for understanding existing patterns)

**Primary files to load**:
- `core/BestPractices_Coding_Standards_Methodology.md` — rationale: establishes the standard by which existing code quality should be evaluated when reading the codebase
- `rust/Rust_Web_Services_Axum_Methodology.md` — rationale: Axum is the server framework; understanding handler patterns, router setup, and middleware wiring is essential for the endpoint survey
- `architecture/Architecture_API_Design_Methodology.md` — rationale: provides the lens for evaluating whether the existing API surface is appropriate or needs extension for the public use case

These are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.

## Inherited Constraints

- Branch MUST be created from `main` at exactly `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`
- Branch name MUST be `work/chirp-logged-out`
- No code changes in this task — exploration and analysis only
- Repository is `Nousix-LLC/nswe-demo`
- Rust 2021 edition; existing Cargo workspace conventions apply
- No host paths, internal addresses, or taskflow references in any committed content

## Out-of-Scope Methodologies

- Testing methodologies — this task writes no tests
- Frontend/component design — deferred to SUBTASK_frontend-ui
- Operations/CI methodologies — deferred to SUBTASK_synthesis
