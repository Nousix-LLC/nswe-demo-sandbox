# _BRIEF.md — SUBTASK_backend_check

**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  

## Objective

Inspect the backend implementation in `crates/chirp-server` on branch `work/chirp-logged-out`
(HEAD `fed1fc8e`) and verify that it satisfies **AC-5** of issue #35:

> AC-5: `GET /api/chirps` returns recent public chirps **without authentication required**,
> and `GET /api/users/:username/chirps` returns that user's chirps **without authentication
> required**.

If any gaps are found (missing route registrations, auth guards that should not be there,
compilation errors, panics, incorrect response shapes), fix them and push commits to
`work/chirp-logged-out`. Produce a verdict file recording the findings.

## Context

This task is part of chirp-logged-out-r12 (see `../_GLOBAL.md` for full context).

**Dependencies**: None — this task can run immediately.  
**Dependents**: `SUBTASK_synthesis` reads `backend_verdict.md`.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Constraints, branch, CI requirements |
| Contract manifest | `../contracts/_MANIFEST.yaml` | Verdict file format to produce |
| Backend source | `crates/chirp-server` on `work/chirp-logged-out` | The code under inspection |
| GitHub PR #263 | gh CLI | Current state, CI results |

The repository is `Nousix-LLC/nswe-demo`. Clone/checkout as needed. Kubernetes commands run
via SSH per CLAUDE.md (see `../_GLOBAL.md` §Subtree-Wide Constraints for the SSH form).

---

## Process

1. **Orient**: Read the brief and `../_GLOBAL.md`. Read `../contracts/_MANIFEST.yaml` for the
   verdict schema.

2. **Inspect the backend routes**: In `crates/chirp-server`, find:
   - The route for `GET /api/chirps` — verify it is registered, public (no auth guard),
     returns a list of recent chirps with author names and timestamps.
   - The route for `GET /api/users/:username/chirps` — verify it is registered, public,
     returns that user's chirps.
   - The route handler implementations — verify they query the database and return the correct
     JSON shape.

3. **Test the routes**: If the app is deployed on k3s, hit `http://100.90.75.93:8081/api/chirps`
   and `http://100.90.75.93:8081/api/users/:username/chirps` without auth headers. Verify
   correct responses.

4. **Fix any gaps**: If issues are found, fix them on `work/chirp-logged-out`. Push commits
   (do not force-push). CI must pass on the resulting HEAD.

5. **Write verdict**: Produce `backend_verdict.md` following the contract schema.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `backend_verdict.md` |
| Location | `SUBTASK_backend_check/` (this workspace) |
| Format | Markdown following `../contracts/_MANIFEST.yaml` schema |

The verdict file MUST contain:

```markdown
# Backend Verification — AC-5

## Summary
Overall verdict: PASS | FAIL

## AC-5: Backend routes serve public chirps without auth

verdict: PASS | FAIL

evidence:
- [Concrete evidence: file path, line numbers, curl output, or compilation result]

blockers: (only if FAIL)
- [Specific blocker description]

## Commits
- [commit hash] [commit message] — or "None" if no changes were needed
```

---

## Success Criteria

- [ ] All relevant backend source files in `crates/chirp-server` have been read
- [ ] Both API routes (`GET /api/chirps` and `GET /api/users/:username/chirps`) have been
      located and their implementations reviewed
- [ ] Any gaps found have been fixed and committed (or "None" recorded if no fixes needed)
- [ ] CI passes on the resulting HEAD (or was already passing with no new commits)
- [ ] `backend_verdict.md` exists at this workspace with PASS or FAIL verdict and evidence

---

## Suggested Methodology Files

**Domain Mapping row matched**: "Code review" → primary: `Code Review`, supporting: `Core, Testing`

**Suggested files**:
- `code-review/CodeReview_Checklist_Methodology.md` — the standard code review checklist;
  apply the backend/API section to assess route implementation quality
- `code-review/CodeReview_Process_Methodology.md` — the review process; this is a focused
  one-pass review of the backend route implementations
- `core/BestPractices_Error_Handling_Methodology.md` — verify the route handlers handle
  errors correctly (DB not found → 404, DB error → 500, etc.)
- `operations/GitWorkflow_PR_Lifecycle_Methodology.md` — governs any commits pushed

The above are the parent's flagged methodologies based on the task type. The child agent
SHOULD load these as a starting point but is the final judge of what its work requires —
load fewer if some are clearly inapplicable; load more if the child's own reading of the
brief reveals additional methodology surface the parent did not anticipate.

---

## Inherited Constraints

1. **Branch**: `work/chirp-logged-out` only. No force-push.
2. **PR**: Do not open a new PR. PR #263 already covers this branch.
3. **CI**: Any new commits must result in passing CI (all 6 checks: clippy/doc/fmt/image/test/wasm).
4. **Repository**: `Nousix-LLC/nswe-demo` only.
5. **Host facts**: Never put server address, SSH key path, user name, or host paths in GitHub
   issues, PRs, comments, or committed files.

---

## Out-of-Scope Methodologies

- `frontend/` — this task covers only the backend (`crates/chirp-server`); frontend routes
  are SUBTASK_frontend_check's scope
- `architecture/` — this is a verification task, not a design task
- `testing/Testing_E2E_Testing_Methodology.md` — full E2E testing is not in scope; a
  focused smoke-test against the live deployment is sufficient for verification
