# Task: chirp-frontend Structure Analysis

## Task Specification

**Slug**: SUBTASK_frontend_analysis
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-coder

### Objective

Read the chirp-frontend Rust source code to map: the router setup and how routes are registered,
existing sign-in and sign-up route paths, any existing home/landing route, the component module
layout convention, and how the frontend calls the API. Record findings in `frontend_findings.md`.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/_GLOBAL.md` | Project constraints |
| chirp-frontend source | `crates/chirp-frontend/src/` | Existing components, router, state management |

All paths are relative to `/home/user/nousix-runtime/nswe-demo`.

---

## Process Specification

1. Explore `crates/chirp-frontend/src/` to understand the directory layout.
2. Find the router setup file — where routes are defined and mounted (likely `router.rs`,
   `main.rs`, `app.rs`, or similar).
3. Identify existing routes:
   - Sign-in route: path like `/login`, `/sign-in`, `/signin`
   - Sign-up route: path like `/register`, `/sign-up`, `/signup`
   - Home/landing route: what does the app show at `/`?
4. Understand the component module layout (how components are organized — by feature, by type,
   etc.; naming conventions).
5. Find how the frontend calls the API:
   - Does it use `reqwest`, a custom fetch wrapper, direct `web-sys` fetch, or something else?
   - How are API URLs constructed (base URL, path joining)?
6. Identify where new routes/components need to be registered.
7. Write `frontend_findings.md` with the required sections.
8. Write `COMPLETE.md`.

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `frontend_findings.md` |
| Location | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/SUBTASK_frontend_analysis/` |

### Required Sections in `frontend_findings.md`

```markdown
# chirp-frontend Structure Findings

## Router Setup
- Router registration file: <path>
- How routes are registered (code pattern / API used)
- Where new routes need to be added

## Existing Routes
- Sign-in route path: <path> (file: <component file>)
- Sign-up route path: <path or "not found"> (file: <component file or "n/a">)
- Home/landing route: <path or "not found"> (file: <component file or "n/a">)
- Other notable routes: <list>

## Component Module Layout
- Directory convention: <e.g. `components/`, `pages/`, feature-based>
- Naming convention: <e.g. PascalCase modules>
- Where new components should live: <recommended path>

## API Call Pattern
- HTTP client: <reqwest | web-sys fetch | custom wrapper | other>
- Base URL source: <env var | hardcoded | config>
- Request construction pattern: <brief description or code snippet>
- Error handling approach

## Files to Modify / Create
- Router file: <path> — add new route registrations here
- Recommended new component directory: <path>
```

---

## Success Criteria

- [ ] Router registration file path identified
- [ ] Sign-in and sign-up route paths documented (or "not found" with explanation)
- [ ] Component layout convention described
- [ ] API call pattern documented
- [ ] `frontend_findings.md` exists with all required sections
- [ ] `COMPLETE.md` written

---

## Suggested Methodology Files

**Task-type row:** Code analysis of a Rust/ferric frontend — Primary: `rust`, Supporting: `core`

**Specific files:**
- `rust/Rust_Ownership_Borrowing_Methodology.md` — Rationale: Rust component patterns may involve ownership; reading idiomatic Rust requires knowing Rust ownership.
- `core/BestPractices_Coding_Standards_Methodology.md` — Rationale: structured output standards.

**Note:** The ferric framework APIs are covered by a SIBLING task (`SUBTASK_ferric_analysis`),
not this task. Focus only on what the chirp-frontend code uses, not on ferric internals.

**These are SUGGESTIONS.** The child agent is the final judge.

## Inherited Constraints

- Repository is at `/home/user/nousix-runtime/nswe-demo`
- Read-only — do NOT modify any frontend source files
- Note: the cluster SSH pattern from CLAUDE.md is NOT needed for this task

## Out-of-Scope Methodologies

- ferric framework internals — covered by SUBTASK_ferric_analysis
- Backend/server analysis — covered by SUBTASK_server_analysis
