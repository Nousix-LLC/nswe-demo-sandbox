# _BRIEF.md — SUBTASK_check-ac3

## Task Specification

**Slug**: SUBTASK_check-ac3
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Read the error branch in `view_tree` (or equivalent dispatch logic) in
`crates/chirp-frontend/src/landing.rs` at pinned commit
`decb6196c2c1e6ed421d393a642f0c844cc333ba` and adjudicate AC-3:

> Does the initial-error path render a user-readable message (not a raw technical
> error / Rust debug repr)? Does it offer a usable Retry action? Does the element
> carrying the error message have `role="alert"` or equivalent ARIA?

### Context

This task is a spoke in the SUBTASK_landing-states sub-decomposition
(see `../_GLOBAL.md`). It covers AC-3 only; AC-2 and AC-4-partial are covered
by sibling spokes.

**Dependencies**: none  
**Dependents**: SUBTASK_synthesis-findings

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Sub-decomposition hub | `../_GLOBAL.md` | Shared context, constraints |
| Parent hub | `../../_GLOBAL.md` | Broader review context |
| Contract | `../contracts/_MANIFEST.yaml` | concern_ac3.md output schema |
| Source file | `crates/chirp-frontend/src/landing.rs` at pinned commit | File under review |

Fetch `landing.rs` from the GitHub API or repository at the pinned commit.
If `error_banner` or the error element is defined in a separate component, read that too.

---

## Process Specification

Locate the error branch in `view_tree` (or the equivalent state-dispatch logic). Check:

1. **User-readable message**: Is the message shown to the user a plain-English string
   (or similar friendly text), rather than a Rust `{:?}` debug repr, an `Error { ... }`
   struct dump, or a raw technical value?
2. **Retry action**: Is there a button or link the user can interact with to retry the
   failed operation? Is it clearly labeled as a retry action?
3. **`role="alert"` ARIA**: Does the element rendering the error message carry
   `role="alert"` (or an equivalent ARIA live-region attribute)? Note the presence or
   absence explicitly.

For each criterion: if it passes, note what was checked and found clean with the specific
line. If it fails, state location (file + line at pinned commit), principle, rationale,
severity (blocker / non-blocking), and what would satisfy it.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `concern_ac3.md` |
| Location | `SUBTASK_check-ac3/` (this workspace) |
| Schema | `../contracts/concern_findings_schema.yaml` |

```markdown
## Concern: AC-3 — error-state recoverability and role="alert"

**Status**: [clean | has_findings]

## Checked
[What code was read; error branch located; criteria applied; pinned commit noted]

## Findings
[List of findings with location/principle/rationale/severity/resolution, or "None."]

## Clean Notes
[For each sub-criterion that passed: what was examined and what was found]
```

---

## Success Criteria

- [ ] Error branch in `view_tree` (or equivalent) located and read in full
- [ ] User-readable message criterion adjudicated with specific evidence
- [ ] Retry action criterion adjudicated with specific evidence
- [ ] `role="alert"` presence or absence noted explicitly with specific line
- [ ] Every finding or clean note cites file + line at `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- [ ] `concern_ac3.md` written to this workspace

---

## Suggested Methodology Files

**Task-type row matched**: Code review → Primary: `code-review`, Supporting: `frontend`

- `code-review/CodeReview_Process_Methodology.md` — review process framework; use to structure
  examination of error-state handling
- `code-review/CodeReview_Checklist_Methodology.md` — review checklist; apply ARIA/accessibility
  and error-handling items
- `frontend/Frontend_Component_Design_Methodology.md` — Leptos component patterns; useful for
  evaluating error_banner and error state component structure

These are the parent's flagged suggestions. Load fewer if inapplicable; load more if your
reading of the brief reveals additional needs.

## Inherited Constraints

- Repository: `Nousix-LLC/nswe-demo` only
- Pinned commit: `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Do not post to the PR
- Cover AC-3 only; do not investigate AC-2, AC-4-partial, or routing concerns
- Findings point at repository file paths and lines; never name host paths, private IPs,
  or internal infrastructure details

## Out-of-Scope

- AC-2 (empty_view content) — owned by SUBTASK_check-ac2
- AC-4-partial (header_nav presence) — owned by SUBTASK_check-ac4p
- Route annotation (`/sign-in` alias comment) — owned by SUBTASK_routing-ctas
