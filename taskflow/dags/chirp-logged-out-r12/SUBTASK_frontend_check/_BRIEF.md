# _BRIEF.md — SUBTASK_frontend_check

**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  

## Objective

Inspect the frontend implementation in `crates/chirp-frontend` on branch `work/chirp-logged-out`
(HEAD `fed1fc8e`) and verify that it satisfies **AC-1 through AC-4** of issue #35:

> AC-1: A logged-out visitor can visit `/` (the landing/public timeline) and see recent chirps
> with author names and timestamps, without being redirected to sign-in.
>
> AC-2: A logged-out visitor can visit `/users/:username` and see that user's chirps,
> without being redirected to sign-in.
>
> AC-3: The landing page `/` shows a clear call-to-action for signing up or signing in
> when the visitor is not authenticated.
>
> AC-4: The sign-in page (`/sign_in`) and sign-up page (`/sign_up`) display accurate states
> — no phantom "logged in" state, no broken UI for first-time visitors.

If any gaps are found (broken route registrations, incorrect auth-state logic, phantom auth
state on sign-in/sign-up, missing CTA, compilation errors), fix them and push commits to
`work/chirp-logged-out`. Produce a verdict file recording the findings.

## Context

This task is part of chirp-logged-out-r12 (see `../_GLOBAL.md` for full context).  
The frontend uses the **ferric framework** (Rust/WASM UI framework).

**Dependencies**: None — this task can run immediately in parallel with SUBTASK_backend_check.  
**Dependents**: `SUBTASK_synthesis` reads `frontend_verdict.md`.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Constraints, branch, CI requirements |
| Contract manifest | `../contracts/_MANIFEST.yaml` | Verdict file format to produce |
| Frontend source | `crates/chirp-frontend` on `work/chirp-logged-out` | The code under inspection |
| GitHub PR #263 | gh CLI | Current state, CI results |

The repository is `Nousix-LLC/nswe-demo`. Kubernetes commands run via SSH per CLAUDE.md
(see `../_GLOBAL.md` §Subtree-Wide Constraints for the SSH form).

---

## Process

1. **Orient**: Read the brief and `../_GLOBAL.md`. Read `../contracts/_MANIFEST.yaml`.

2. **Inspect the frontend routes**:
   - `landing` route: Does it call `GET /api/chirps` and display results (author names,
     timestamps)? Is there a CTA for sign-up/sign-in? Does it NOT redirect logged-out users?
   - `public_profile` route: Does it call `GET /api/users/:username/chirps` and display
     results? Does it NOT redirect logged-out users?
   - `sign_in` route: Is the page clean for a first-time (logged-out) visitor? No phantom
     auth state?
   - `sign_up` route: Is the page clean for a first-time visitor? No broken UI?

3. **Check auth state handling**: How does the frontend detect auth state? Verify that
   logged-out visitors reach the landing and public_profile routes without being redirected.
   Verify sign_in and sign_up don't show erroneous "logged in" states.

4. **Test the routes**: If the app is deployed on k3s, visit the routes via
   `http://100.90.75.93:8081` without an auth session. Verify correct rendering.

5. **Fix any gaps**: If issues are found, fix them on `work/chirp-logged-out`. Push commits
   (do not force-push). CI must pass on the resulting HEAD.

6. **Write verdict**: Produce `frontend_verdict.md` following the contract schema.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `frontend_verdict.md` |
| Location | `SUBTASK_frontend_check/` (this workspace) |
| Format | Markdown following `../contracts/_MANIFEST.yaml` schema |

The verdict file MUST contain:

```markdown
# Frontend Verification — AC-1 through AC-4

## Summary
Overall verdict: PASS | FAIL

## AC-1: Landing page shows chirps for logged-out visitors

verdict: PASS | FAIL

evidence:
- [File path, relevant code excerpt, or live-test result]

## AC-2: Public profile page shows user chirps for logged-out visitors

verdict: PASS | FAIL

evidence:
- [File path, relevant code excerpt, or live-test result]

## AC-3: Landing page shows sign-up/sign-in CTA

verdict: PASS | FAIL

evidence:
- [File path showing the CTA element, or screenshot description]

## AC-4: sign_in and sign_up show accurate logged-out states

verdict: PASS | FAIL

evidence:
- [File path, auth-state handling code review]

blockers: (only if any FAIL)
- [Specific blocker description]

## Commits
- [commit hash] [commit message] — or "None" if no changes were needed
```

---

## Success Criteria

- [ ] All relevant frontend source files in `crates/chirp-frontend` for the four routes
      have been read and reviewed
- [ ] Auth state handling (how the frontend distinguishes logged-in vs logged-out) has been
      understood and assessed for each of the four routes
- [ ] Any gaps found have been fixed and committed (or "None" recorded if no fixes needed)
- [ ] CI passes on the resulting HEAD (or was already passing with no new commits)
- [ ] `frontend_verdict.md` exists at this workspace with per-AC verdicts (PASS/FAIL) and evidence

---

## Suggested Methodology Files

**Domain Mapping row matched**: "Code review" → primary: `Code Review`, supporting: `Core, Testing`;
also: "Frontend architecture design" → `Frontend`, `Architecture`

**Suggested files**:
- `code-review/CodeReview_Checklist_Methodology.md` — apply the frontend/UI section
- `code-review/CodeReview_Process_Methodology.md` — the review process; focused on
  route-level logic and auth-state handling
- `frontend/Frontend_Application_Architecture_Methodology.md` — the ferric framework
  uses Rust/WASM; understand the component and routing model before inspecting state handling
- `frontend/React_Hooks_Architecture_Methodology.md` — if the ferric framework has
  hooks or similar reactive patterns, this provides the mental model for auth-state inspection
- `operations/GitWorkflow_PR_Lifecycle_Methodology.md` — governs any commits pushed

The above are the parent's flagged methodologies based on the task type. The child agent
SHOULD load these as a starting point but is the final judge of what its work requires.

---

## Inherited Constraints

1. **Branch**: `work/chirp-logged-out` only. No force-push.
2. **PR**: Do not open a new PR. PR #263 already covers this branch.
3. **CI**: Any new commits must result in passing CI (all 6 checks: clippy/doc/fmt/image/test/wasm).
4. **Repository**: `Nousix-LLC/nswe-demo` only.
5. **Host facts**: Never put server address, SSH key path, user name, or host paths in GitHub
   issues, PRs, comments, or committed files.
6. **Ferric framework**: The frontend uses the in-house Rust/WASM ferric framework. Do not
   try to apply React/Vue patterns directly; understand the ferric conventions first.

---

## Out-of-Scope Methodologies

- Backend (`crates/chirp-server`) — SUBTASK_backend_check's scope; this task covers only
  `crates/chirp-frontend`
- `architecture/Architecture_API_Design_Methodology.md` — API design is not being redesigned
- `testing/Testing_E2E_Testing_Methodology.md` — full E2E is out of scope; smoke-test only
