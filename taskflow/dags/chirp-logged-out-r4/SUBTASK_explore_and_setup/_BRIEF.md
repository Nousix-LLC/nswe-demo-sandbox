# Task: Codebase Exploration and Branch Setup

## Task Specification

**Slug**: SUBTASK_explore_and_setup
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-coder

### Objective

Read the existing Chirp codebase and design documents to understand the current API surface,
routing structure, and what needs to be added for the logged-out experience. Create the
`work/chirp-logged-out` branch from main at the specified commit. Produce a detailed analysis
document that the backend and frontend children can use as their primary reference.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `taskflow/dags/chirp-logged-out-r4/_GLOBAL.md` | Project constraints and context |
| API contract | `taskflow/dags/chirp-logged-out-r4/contracts/public_api_spec.md` | The frozen API spec to validate against |
| Product requirements | `design/product-requirements.md` | §3 User journeys; §4 REQ-PROD-013..015 |
| Experience design | `design/experience-design.md` | §1 IA; §2 Screens/flows/states; §6 REQ-UX-002, 030-032 |
| Release bar | `design/release-bar.md` | §C BAR-011 |
| Chirp server routes | `crates/chirp-server/src/` | Existing route handlers, auth middleware, router setup |
| Chirp frontend | `crates/chirp-frontend/src/` | Existing components, router, state management |
| Ferric framework | `crates/ferric/src/` | Router API, Resource/async, SSR/hydrate APIs |

### Input Verification

Before processing, verify:
- [ ] All design docs exist under `design/`
- [ ] `crates/chirp-server/` directory exists with Rust source
- [ ] `crates/chirp-frontend/` directory exists with Rust source
- [ ] `crates/ferric/` directory exists

---

## Process Specification

This task does two things: (1) git setup, and (2) codebase analysis. Both are needed before
the backend and frontend spokes can begin work.

### Git Setup

1. Check if `work/chirp-logged-out` branch already exists (locally and on remote).
2. If it does not exist: create it from main at commit `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`.
   Command: `git checkout -b work/chirp-logged-out cb1ced3ffe6efc678d96a26ae16a63cb948d4237`
3. If it already exists: check it out and verify it is at or ahead of the base commit.
4. Push the branch to origin if not already there.
5. Record the current HEAD SHA in the analysis document.

### Codebase Analysis

Read and analyze the following areas, recording findings in the analysis document:

**A. Design requirements**
- Extract the specific screen/state requirements from experience-design.md §2
- Note the BAR-011 requirements from release-bar.md
- Identify the exact sign-up/sign-in route names mentioned in the design

**B. chirp-server: existing API surface**
- Find all existing GET endpoints — which ones require auth, which do not
- Identify whether a public timeline endpoint exists (unauthenticated GET for chirps)
- Identify whether a public user profile endpoint exists
- Find where new routes need to be registered (the router setup file)
- Find the auth middleware extractor type (e.g. `AuthUser`, `OptionalAuthUser`, or similar)
- Understand the existing persistence layer types used by route handlers
- Record the exact file paths that need to be modified

**C. chirp-frontend: existing routing and components**
- Find the router setup and how routes are registered
- Identify the existing sign-in and sign-up routes (paths like `/login`, `/sign-in`, `/sign-up`, `/register`)
- Find any existing public/landing page or home route
- Understand how components are structured (module layout)
- Understand how the frontend calls the API (fetch wrapper, URL construction)
- Find where new routes/components need to be registered

**D. Ferric framework APIs**
- Identify the `Resource` / async data-loading API and how it represents loading/error/loaded states
- Find the Router API and how routes are defined and mounted
- Find the SSR and hydration APIs (whether the new public route should use SSR)
- Note any relevant component/signal patterns for distinct UI states

**E. Verdict on the API spec**
- Compare the existing server API against `contracts/public_api_spec.md`
- If a public timeline GET endpoint already exists with a different URL or response shape, note the
  discrepancy and recommend whether to adopt the existing shape or the spec shape (the backend spoke
  will make the final call)
- Confirm whether the spec's pagination approach (`before` cursor + `has_more`) is consistent with
  any existing pagination pattern in the server

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `analysis.md` |
| Location | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/` |

### Output Structure

The analysis document must contain:

```markdown
# Chirp Logged-Out — Codebase Analysis

## Branch Status
- Branch: `work/chirp-logged-out`
- HEAD: <SHA>
- Status: created / already existed

## Design Requirements Summary
- Key screen states required (loading/empty/error/end-of-list)
- Sign-up and sign-in route names as specified in design docs
- BAR-011 checklist items relevant to AC-1 through AC-5

## chirp-server: Existing API Surface
- List of all existing routes with auth requirements
- Does a public timeline GET exist? (yes/no + path if yes)
- Does a public user profile GET exist? (yes/no + path if yes)
- Exact files to modify for new routes:
  - Router registration file: <path>
  - Recommended new file for public handlers: <path>
- Auth extractor type name: <name>
- Persistence types used in route handlers: <types>

## chirp-frontend: Existing Structure
- Router registration file: <path>
- Existing sign-in route path: <path>
- Existing sign-up route path: <path or "not found">
- Existing home/landing route: <path or "not found">
- API call pattern: <how fetch is done, e.g. reqwest, fetch, custom wrapper>
- Component module layout convention

## Ferric Framework: Relevant APIs
- Resource API: <usage pattern>
- Router API: <usage pattern>
- SSR recommendation: use SSR for public timeline? (yes/no + rationale)
- Hydration API: <usage pattern if SSR is recommended>
- Signal/state pattern for distinct UI states

## API Spec Verdict
- Existing public timeline endpoint: <match / conflict / absent>
- Existing public user profile endpoint: <match / conflict / absent>
- Recommended final endpoint paths for SUBTASK_backend

## Implementation Guidance for SUBTASK_backend
- Files to create: <list>
- Files to modify: <list with what changes>
- Specific guidance on the auth extractor approach

## Implementation Guidance for SUBTASK_frontend
- Files to create: <list>
- Files to modify: <list with what changes>
- Suggested component structure for the home/landing route
- Suggested component structure for the user profile route
```

---

## Success Criteria

- [ ] `work/chirp-logged-out` branch exists and is pushed to origin
- [ ] `analysis.md` exists at the declared path
- [ ] Analysis covers all 5 sections (A through E) with specific file paths, not vague descriptions
- [ ] The API spec is validated against the existing codebase
- [ ] COMPLETE.md written and status reported as completed

---

## Suggested Methodology Files

**Task-type row:** "Writing new code" — Primary: `core`, Supporting: `code-quality`
Additionally, this task does git/branch work: `operations/GitWorkflow_PR_Lifecycle_Methodology.md`

**Specific files:**
- `core/BestPractices_Coding_Standards_Methodology.md` — Rationale: sets standards this task's output documents should follow.
- `operations/GitWorkflow_PR_Lifecycle_Methodology.md` — Rationale: branch creation and push follow the PR lifecycle workflow.
- `rust/Rust_Web_Services_Axum_Methodology.md` — Rationale: understanding the existing Axum routes requires knowing Axum patterns.

**These are SUGGESTIONS.** The child agent is the final judge of what to load — fewer if some are clearly inapplicable, more if the brief reveals additional needs.

## Inherited Constraints

- Repository is `Nousix-LLC/nswe-demo` at `/home/user/nousix-runtime/nswe-demo`
- Branch base commit: `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`
- Do NOT write any code — this task only reads and produces analysis plus creates the branch
- Do NOT put host paths, internal addresses, or taskflow references in git commits
- The SSH-tunnel pattern for kubectl/helm is NOT needed for this task (this is a git/code task, not a cluster task)
