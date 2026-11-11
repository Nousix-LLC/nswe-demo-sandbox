# _BRIEF.md — SUBTASK_cta-link

## Task Specification

**Slug**: SUBTASK_cta-link
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Assess the correctness of `link("/compose", "Log in →")` in `compose.rs`'s `render_signup()`.
Determine whether `/compose` is the right destination for a "Log in" CTA on the sign-up page,
or whether it exposes an internal app route inappropriately to a logged-out visitor.

### Context

This task is part of the SUBTASK_routing-ctas sub-decomposition.
See `../_GLOBAL.md` for route table and shared context.

Key context from hub:
- Route `/signup` → `signup_view` (compose.rs — the sign-up page where `render_signup()` appears)
- Route `/compose` is the write-a-chirp / post-composition route for authenticated users
- The expected destination for a "Log in →" CTA from the sign-up form is the sign-in page (`/signin`)

**Dependencies**: none
**Dependents**: SUBTASK_synthesis (reads `concern-cta.md`)

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Route table and shared context |
| compose source | `crates/chirp-frontend/src/compose.rs` at commit `decb6196` | Find render_signup() and the link target |
| route table | `crates/chirp-frontend/src/app.rs` at commit `decb6196` | Confirm what /compose routes to |

GitHub repository: `Nousix-LLC/nswe-demo`, pinned commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`

---

## Process Specification

1. Read `compose.rs`. Find `render_signup()`. Locate `link("/compose", "Log in →")`.
   Note the exact line number at the pinned commit.
2. Confirm what `/compose` routes to in `app.rs`. Is it the write-chirp / authenticated compose
   route?
3. Assess: is `/compose` the appropriate destination for a "Log in →" CTA shown on the sign-up
   page? A logged-out visitor clicking "Log in →" would be redirected to the compose (write-chirp)
   view — assess whether that is the intended behavior or a bug.
4. The correct destination for "Log in" from a sign-up form is the sign-in page (`/signin`).
   State whether the link target is a bug, assess severity, and state what would resolve it.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `concern-cta.md` |
| Location | `SUBTASK_cta-link/` (this workspace) |

The file MUST follow the concern_output_schema in `../contracts/_MANIFEST.yaml`:

```markdown
# CTA link concern

## Concern: CTA link correctness — link("/compose", "Log in →")

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

- [ ] `render_signup()` link target identified with file + line at pinned commit
- [ ] `/compose` route destination confirmed (what it renders for a logged-out visitor)
- [ ] Verdict stated with reasoning: is `/compose` the correct destination for a "Log in" CTA?
- [ ] `concern-cta.md` written to this workspace

---

## Suggested Methodology Files

**Task-type row matched**: Code review → Primary: `code-review`, Supporting: `frontend`

- `code-review/CodeReview_Process_Methodology.md` — review process and verdict reasoning; apply
  to assess whether the link target is the correct route for this user journey

The above are the parent's flagged suggestions. Load fewer if inapplicable; load more if your
reading reveals additional needs.

## Inherited Constraints

- Repository: `Nousix-LLC/nswe-demo` only
- Pinned commit: `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Do not post to the PR
- Cite file paths and lines; never name host paths, private IPs, or infrastructure details
- Scope: CTA link in render_signup() only; do not investigate the AC-4 path or annotation anomaly
  — those are sibling tasks
