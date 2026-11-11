# _BRIEF.md — SUBTASK_ac4-path

## Task Specification

**Slug**: SUBTASK_ac4-path
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Trace the AC-4 sign-in-to-sign-up path: starting from `sign_in.rs`, find the "Create an
account" link (or equivalent CTA), verify its destination against the route table in `app.rs`,
and confirm that the linked sign-up page is a usable functional form rather than the
placeholder stub (`sign_up.rs`).

### Context

This task is part of the SUBTASK_routing-ctas sub-decomposition.
See `../_GLOBAL.md` for route table and shared context.

Key context from hub:
- Route `/signup` → `signup_view` (compose.rs — functional form)
- Route `/signin` → `sign_in_view` (sign_in.rs)
- `sign_up.rs` exports `sign_up_view` (placeholder stub with disabled button) — NOT in route table
- Any visitor following a `/signup` link reaches compose.rs `signup_view`, not sign_up.rs

**Dependencies**: none
**Dependents**: SUBTASK_synthesis (reads `concern-ac4.md`)

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Route table and shared context |
| sign-in source | `crates/chirp-frontend/src/sign_in.rs` at commit `decb6196` | Find the "Create an account" CTA and its link target |
| route table | `crates/chirp-frontend/src/app.rs` at commit `decb6196` | Verify route resolution for the CTA's target path |
| sign-up stub | `crates/chirp-frontend/src/sign_up.rs` at commit `decb6196` | Confirm it is the placeholder, not the functional form |
| compose source | `crates/chirp-frontend/src/compose.rs` at commit `decb6196` | Confirm signup_view is the functional sign-up form |

GitHub repository: `Nousix-LLC/nswe-demo`, pinned commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`

---

## Process Specification

1. Read `sign_in.rs`. Find the "Create an account" CTA link (or equivalent). Note the exact path
   it links to and the line number at the pinned commit.
2. Cross-reference that path with the route table in `app.rs`. What handler does it resolve to?
3. Read the resolved handler (`compose.rs` signup_view or `sign_up.rs` sign_up_view). Confirm
   whether the destination renders a usable form or a disabled placeholder.
4. Write verdict: does following the "Create an account" link from sign-in reach a working
   sign-up form?

If the path is correct (links to `/signup` → compose.rs `signup_view`, which is functional):
write a clean item with evidence. If the path leads to the placeholder stub or is broken:
write a finding with severity.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `concern-ac4.md` |
| Location | `SUBTASK_ac4-path/` (this workspace) |

The file MUST follow the concern_output_schema in `../contracts/_MANIFEST.yaml`:

```markdown
# AC-4 path concern

## Concern: AC-4 sign-in-to-sign-up path

## Checked
[What was examined, with file + line references at commit decb6196]

## Verdict
pass | fail

## Finding or Clean Item
[If fail: location, principle, rationale, severity (blocker | non-blocking), resolution]
[If pass: checked, result]
```

---

## Success Criteria

- [ ] `sign_in.rs` CTA link target identified and cited (file + line at pinned commit)
- [ ] Route table resolution confirmed (which handler the target path resolves to)
- [ ] Destination handler confirmed as functional form or placeholder (with file + line evidence)
- [ ] Verdict (pass/fail) stated with reasoning
- [ ] `concern-ac4.md` written to this workspace

---

## Suggested Methodology Files

**Task-type row matched**: Code review → Primary: `code-review`, Supporting: `frontend`

- `code-review/CodeReview_Process_Methodology.md` — review process and verdict reasoning; use
  to structure the examination of the sign-in-to-sign-up navigation path
- `code-review/CodeReview_Checklist_Methodology.md` — checklist items for navigation/routing

The above are the parent's flagged suggestions based on task type. Load fewer if some are
clearly inapplicable; load more if your reading of the brief reveals additional needs.

## Inherited Constraints

- Repository: `Nousix-LLC/nswe-demo` only
- Pinned commit: `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Do not post to the PR
- Cite file paths and lines; never name host paths, private IPs, or infrastructure details
- Scope: AC-4 sign-up path only; do not investigate the CTA link in render_signup() or the
  annotation anomaly — those are sibling tasks
