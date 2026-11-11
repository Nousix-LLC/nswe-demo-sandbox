# Task: Verify AC-1 at HEAD 7f4b684

## Task Specification

**Slug**: SUBTASK_ac1-verify  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending

### Objective

Verify that AC-1 ("Logged-out visitor reads home/public timeline and user profiles without being forced to sign up or sign in. No auth wall on `/` or `/@:handle`.") now PASSES at HEAD `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`. In r1 (HEAD `decb6196`), AC-1 FAILED due to B1: `timeline.rs:218` was changed from `ctx.client().timeline(&query)` to `ctx.client().pub_timeline(&query)`, routing authenticated users through the global unauthenticated feed. The remediation commit changes `timeline.rs:218` back to `timeline()`. Verify that this fix addresses the root cause and that all public endpoints and frontend routes remain correctly unguarded. Produce `verdict-ac1.md`.

### Context

This task is part of SUBTASK_verify-acs (see `_GLOBAL.md` in the parent workspace).

**Dependencies**: none — runs in parallel with SUBTASK_ac4-verify and SUBTASK_ac235-confirm  
**Dependents**: SUBTASK_synthesis consumes this task's output

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Subtree constraints |
| r1 SYNTHESIS | `taskflow/dags/review-chirp-logged-out-r1/SYNTHESIS.md` | r1 evidence for AC-1: what spoke-access-auth found clean |
| PR diff | `gh pr diff 263 -R Nousix-LLC/nswe-demo` | The remediation diff |
| `timeline.rs` at new HEAD | repo file | Verify `timeline.rs:218` is now `ctx.client().timeline(&query)` |
| Backend handlers (if needed) | repo files | Confirm `public_chirps`, `user_chirps`, `public_timeline` still unguarded |
| Frontend app/router (if needed) | repo files | Confirm `/` and `/@:handle` still unguarded |
| Contracts manifest | `../contracts/_MANIFEST.yaml` | Required output schema |

---

## What to Verify

### Primary check: B1 fix

Confirm `timeline.rs:218` at HEAD `7f4b684` now reads `ctx.client().timeline(&query)` (not `pub_timeline`). The diff should show exactly this single-line change. This is the root cause of B1.

### Secondary checks (must remain correct from r1)

r1's `spoke-access-auth` found the following correct at `decb6196`. Confirm they are unchanged at `7f4b684`:

1. **Public backend endpoints unguarded**: `public_chirps`, `user_chirps`, `public_timeline` have no `AuthUser` extractor and are mounted without an auth layer.
2. **Auth-gated handlers unchanged**: `create_chirp`, `timeline`, `follow`, `unfollow`, `like`, `unlike` still retain their `AuthUser` extractor.
3. **Frontend routes unguarded**: `/` → `landing_view` and `/@:handle` → `public_profile_view` are unguarded in the route table.
4. **No new auth layer added**: No shared `from_fn` or `layer` has been added that would propagate auth state across public route boundaries.

If any of these secondary items are **not** in the remediation diff, explicitly record them as "not modified by remediation diff — finding from r1 carries forward."

If any are modified, examine the modification and determine its effect on AC-1.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `verdict-ac1.md` |
| Location | `SUBTASK_ac1-verify/` (this task's workspace) |

### Required output structure

```markdown
# Verdict: AC-1

**ac_1_verdict**: PASS | FAIL

## Evidence

### B1 fix check
[What line 218 of timeline.rs reads at HEAD 7f4b684; direct evidence from diff or file read]

### Public endpoint guard status
[For each of public_chirps, user_chirps, public_timeline: "not in diff — r1 finding carries forward" or evidence of changed status]

### Frontend route table
[For / and /@:handle: "not in diff — r1 finding carries forward" or evidence of changed status]

## Conclusion
[1–2 sentences explaining why AC-1 PASS or FAIL]
```

---

## Success Criteria

- [ ] PR diff obtained via `gh pr diff 263 -R Nousix-LLC/nswe-demo`
- [ ] `timeline.rs:218` at new HEAD confirmed as `timeline()` (not `pub_timeline()`)
- [ ] Public endpoint guard status confirmed unchanged or checked for modifications
- [ ] Frontend route guard status confirmed unchanged or checked
- [ ] `verdict-ac1.md` written with explicit `ac_1_verdict: PASS` or `ac_1_verdict: FAIL`

---

## Suggested Methodology Files

**Task type row matched**: "Code review | Code Review (primary) | Core, Testing (supporting)"

**Primary files to load:**
- `code-review/CodeReview_Process_Methodology.md` — review process, how to record per-criterion verdicts with evidence
- `code-review/CodeReview_Checklist_Methodology.md` — checklist for reviewing modified code

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but is the final judge of what its work requires.

## Inherited Constraints

- Scope is the remediation diff `decb6196..7f4b684` only
- HEAD under review is `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`
- When a file is not in the diff, verify it is unchanged and explicitly record that finding
- Non-blockers already tracked as issues #264–#271 — note as "already tracked" if re-encountered
- Do NOT name host paths, tailnet addresses, or review DAG internal paths in any GitHub-posted content
- Repo is `Nousix-LLC/nswe-demo`

## Out-of-Scope

- B1 fix correctness from the perspective of "does it fix the wrong-feed bug for authenticated users" — that is SUBTASK_verify-fixes territory. This task's question is narrower: does the change at `timeline.rs:218` restore the correct public-access behavior for AC-1?
- AC-2, AC-3, AC-4, AC-5 — owned by sibling spokes
