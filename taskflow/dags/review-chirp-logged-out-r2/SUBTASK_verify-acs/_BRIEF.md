# Task: Verify All 5 ACs Still Hold on New HEAD

## Task Specification

**Slug**: SUBTASK_verify-acs  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  

### Objective

For PR #263 (`work/chirp-logged-out`) at HEAD `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`, verify that all five acceptance criteria from issue #35 still hold. In r1, AC-1 and AC-4 FAILED (due to B1 and B2 respectively); AC-2, AC-3, and AC-5 PASSED. The remediation commit claims to fix B1 and B2 — if those fixes are correct, AC-1 and AC-4 should now PASS. AC-2, AC-3, and AC-5 should remain PASS. Produce `findings-acs.md` in this task's workspace.

### Context

This task is part of review-chirp-logged-out-r2 (see `_GLOBAL.md` in the parent workspace).

**Dependencies**: none — runs in parallel with SUBTASK_verify-fixes  
**Dependents**: SUBTASK_synthesis consumes this task's output

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | AC definitions, blocker context, constraints |
| r1 review output | `taskflow/dags/review-chirp-logged-out-r1/SYNTHESIS.md` | Per-AC verdicts from r1 and what evidence each AC was checked on |
| PR diff | `gh pr diff 263 -R Nousix-LLC/nswe-demo` | The diff under review |
| PR content (if needed) | `gh pr view 263 -R Nousix-LLC/nswe-demo` or repo files | Specific source files for each AC |
| contracts manifest | `../contracts/_MANIFEST.yaml` | Required output schema |

---

## Acceptance criteria to verify

The five ACs from issue #35:

| ID | Criterion | r1 verdict |
|----|-----------|------------|
| AC-1 | Logged-out visitor reads home/public timeline and user profiles without being forced to sign up or sign in. No auth wall on `/` or `/@:handle`. | FAIL (caused by B1) |
| AC-2 | On arrival with no content: clear statement of what Chirp is plus an obvious way to sign up or sign in. Never a blank page or unexplained error. | PASS |
| AC-3 | If timeline fails to load: clear, recoverable error message shown; retry path exists. | PASS |
| AC-4 | "Create an account" route visible on landing and sign-in screen; following it reaches sign-up. Sign-up page "Log in →" CTA routes to `/signin`. | FAIL (caused by B2) |
| AC-5 | Logged-out landing/timeline renders loading, empty, error, and end-of-list states accurately and distinctly. No two states collapse. | PASS |

### AC-1 (was FAIL due to B1)

The B1 fix changes `timeline.rs:218` back to `timeline()`. Verify:
- The B1 fix addresses the root cause of AC-1's failure (authenticated `timeline_view` was routing through the public feed, not AC-1's public endpoints which were already correctly unguarded)
- The public endpoints (`public_chirps`, `user_chirps`, `public_timeline` server-side) remain unguarded — no `AuthUser` extractor, no auth layer added
- `/` and `/@:handle` frontend routes remain unguarded in the route table
- The B1 fix does not accidentally break any previously correct public access path

The r1 review found in `spoke-access-auth`: public endpoints were correctly unguarded at `decb6196`. Confirm this is unchanged at `7f4b684`.

### AC-2 (was PASS)

The r1 review found `empty_view()` at `landing.rs:286–306` correct at `decb6196`. The remediation commit targets only `timeline.rs:218` and `compose.rs:519`. Confirm:
- `landing.rs` is unmodified or any modification is in unrelated lines
- `empty_view()` still renders product identity and two correctly-routed CTAs (`/signup`, `/signin`)
- If `landing.rs` was not in the diff, explicitly note it as unchanged

### AC-3 (was PASS)

The r1 review found `AppError::user_message()` and `error_banner` correct at `decb6196`. Confirm:
- Error handling code in `landing.rs` and `error.rs` is unmodified by the remediation commit
- If not in the diff, explicitly note as unchanged

### AC-4 (was FAIL due to B2)

The B2 fix changes `compose.rs:519` to `link("/signin", "Log in →")`. Verify:
- This change directly satisfies AC-4's "Sign-up page 'Log in →' CTA must route to `/signin`" requirement
- `/signin` resolves to the sign-in view in the router
- The sign-in-to-sign-up path (`sign_in.rs:68` → `/signup`) is unchanged and still correct
- The header nav on the landing page (hoist-before-branch structure) is unchanged

### AC-5 (was PASS)

The r1 review found state branches in `landing.rs` and `public_profile.rs` correct at `decb6196`. Confirm:
- Neither `landing.rs` nor `public_profile.rs` is in the diff (or if modified, the state machine logic is unaffected)
- All four states (loading, empty, error, end-of-list) remain present and distinct
- If not in the diff, explicitly note as unchanged

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `findings-acs.md` |
| Location | `SUBTASK_verify-acs/` (this task's workspace) |

### Required output structure

```markdown
# Findings: AC Re-Verification

**PR**: #263 (`work/chirp-logged-out`)
**HEAD reviewed**: 7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4

## AC verdicts

| AC | Verdict | Evidence |
|----|---------|----------|
| AC-1 | PASS or FAIL | [evidence] |
| AC-2 | PASS or FAIL | [evidence] |
| AC-3 | PASS or FAIL | [evidence] |
| AC-4 | PASS or FAIL | [evidence] |
| AC-5 | PASS or FAIL | [evidence] |

## Per-AC detail

### AC-1: [verdict]
[What was checked, what was found]

### AC-2: [verdict]
[What was checked, what was found]

### AC-3: [verdict]
[What was checked, what was found]

### AC-4: [verdict]
[What was checked, what was found]

### AC-5: [verdict]
[What was checked, what was found]

## Non-blocking findings
| ID | Location | Severity | Description |
|----|----------|----------|-------------|
[List new non-blockers found, if any. Leave empty if none.]
```

The output MUST conform to the contract schema in `../contracts/_MANIFEST.yaml`: explicit verdict for each of AC-1 through AC-5.

---

## Success criteria

- [ ] PR diff obtained via `gh pr diff 263 -R Nousix-LLC/nswe-demo`
- [ ] AC-1: public endpoint status verified at new HEAD
- [ ] AC-2: `landing.rs` `empty_view()` confirmed unchanged or checked
- [ ] AC-3: error handling confirmed unchanged or checked
- [ ] AC-4: `compose.rs:519` fix confirmed as satisfying the AC-4 requirement; `sign_in.rs` unchanged
- [ ] AC-5: state machine files confirmed unchanged or checked
- [ ] `findings-acs.md` written with explicit PASS/FAIL verdicts for each AC

---

## Suggested Methodology Files

**Task type row matched**: "Code review | Code Review (primary) | Core, Testing (supporting)"

**Primary files to load:**
- `code-review/CodeReview_Process_Methodology.md` — review process and how to record per-criterion verdicts
- `code-review/CodeReview_Checklist_Methodology.md` — per-line review checklist for any modified code encountered

**Supporting files to consider:**
- `testing/Testing_Unit_Testing_Methodology.md` — relevant when assessing whether existing AC-related tests still cover the behavior
- `rust/Rust_Trait_Design_Methodology.md` — if any trait boundaries are relevant to the access patterns

The above are the parent's flagged methodologies based on the task type. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.

## Inherited Constraints

- Scope is the remediation diff `decb6196..7f4b684` only; do not re-review the full original PR
- HEAD under review is `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`
- When a file is not in the diff, verify it is unchanged and explicitly record that finding — do not silently skip it
- Non-blockers already tracked as issues #264–#271 — note as "already tracked" if re-encountered; do not re-file
- Do NOT name host paths, tailnet addresses, or review DAG internal paths in any GitHub-posted content
- The repo is `Nousix-LLC/nswe-demo`

## Out-of-Scope Methodologies

- `code-review/CodeReview_PR_Authoring_Methodology.md` — this task reads, not authors
- Fix correctness verification (concerns 1, 3, 4, 5, 6) — that is SUBTASK_verify-fixes's responsibility; this task checks the ACs as behavioral requirements, which may overlap with the fixes but stays in the AC frame
