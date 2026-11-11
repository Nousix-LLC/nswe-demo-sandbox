# Task: Verify AC-4 at HEAD 7f4b684

## Task Specification

**Slug**: SUBTASK_ac4-verify  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending

### Objective

Verify that AC-4 ("`Create an account` route visible on landing and sign-in screen; following it reaches sign-up. Sign-up page `Log in →` CTA routes to `/signin`.") now PASSES at HEAD `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`. In r1 (HEAD `decb6196`), AC-4 FAILED due to B2: `compose.rs:519` rendered `link("/compose", "Log in →")` — routing the sign-up page's "Log in →" CTA to `/compose` instead of `/signin`. The remediation commit changes `compose.rs:519` to `link("/signin", "Log in →")`. Verify this fix and confirm the surrounding CTA routing is intact. Produce `verdict-ac4.md`.

### Context

This task is part of SUBTASK_verify-acs (see `_GLOBAL.md` in the parent workspace).

**Dependencies**: none — runs in parallel with SUBTASK_ac1-verify and SUBTASK_ac235-confirm  
**Dependents**: SUBTASK_synthesis consumes this task's output

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Subtree constraints |
| r1 SYNTHESIS | `taskflow/dags/review-chirp-logged-out-r1/SYNTHESIS.md` | r1 evidence for AC-4: what spoke-ui-states found clean |
| PR diff | `gh pr diff 263 -R Nousix-LLC/nswe-demo` | The remediation diff |
| `compose.rs` at new HEAD | repo file | Verify `compose.rs:519` is now `link("/signin", "Log in →")` |
| Router / `app.rs` (if needed) | repo file | Confirm `/signin` resolves to sign-in view |
| `sign_in.rs` (if needed) | repo file | Confirm `sign_in.rs:68` → `/signup` unchanged |
| Contracts manifest | `../contracts/_MANIFEST.yaml` | Required output schema |

---

## What to Verify

### Primary check: B2 fix

Confirm `compose.rs:519` at HEAD `7f4b684` now reads `link("/signin", "Log in →")`. The diff should show exactly this single-line change.

### Secondary checks (must remain correct from r1)

r1's `spoke-ui-states` found the following correct at `decb6196`. Confirm they are unchanged at `7f4b684`:

1. **`/signin` resolves to the sign-in view**: Check the router (e.g., `app.rs`) to confirm `/signin` or `/sign-in` maps to `sign_in_view` or equivalent. If not in the diff, record as "not modified — r1 finding carries forward."
2. **Sign-in-to-sign-up path**: `sign_in.rs:68` renders a link to `/signup` → `compose::signup_view` (the live registration form). If not in the diff, record as "not modified — r1 finding carries forward."
3. **Header nav on landing page**: `header_nav` is structurally guaranteed (hoist-before-branch at `landing.rs:264`). If `landing.rs` is not in the diff, record as "not modified — r1 finding carries forward."

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `verdict-ac4.md` |
| Location | `SUBTASK_ac4-verify/` (this task's workspace) |

### Required output structure

```markdown
# Verdict: AC-4

**ac_4_verdict**: PASS | FAIL

## Evidence

### B2 fix check
[What compose.rs:519 reads at HEAD 7f4b684; direct evidence from diff or file read]

### /signin route resolution
["not in diff — r1 finding carries forward" or evidence of route table modification]

### Sign-in-to-sign-up path (sign_in.rs:68)
["not in diff — r1 finding carries forward" or evidence of changed status]

### Header nav on landing page
["not in diff — r1 finding carries forward" or evidence of changed status]

## Conclusion
[1–2 sentences explaining why AC-4 PASS or FAIL]
```

---

## Success Criteria

- [ ] PR diff obtained via `gh pr diff 263 -R Nousix-LLC/nswe-demo`
- [ ] `compose.rs:519` at new HEAD confirmed as `link("/signin", "Log in →")`
- [ ] `/signin` route resolution confirmed unchanged or checked
- [ ] `sign_in.rs:68` confirmed unchanged or checked
- [ ] `verdict-ac4.md` written with explicit `ac_4_verdict: PASS` or `ac_4_verdict: FAIL`

---

## Suggested Methodology Files

**Task type row matched**: "Code review | Code Review (primary) | Core, Testing (supporting)"

**Primary files to load:**
- `code-review/CodeReview_Process_Methodology.md` — review process, per-criterion verdict recording
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

- B2 fix correctness from the perspective of "was the wrong link a simple typo or a deeper routing confusion" — that is SUBTASK_verify-fixes territory
- AC-1, AC-2, AC-3, AC-5 — owned by sibling spokes
