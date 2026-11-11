# _BRIEF.md — SUBTASK_check-ac4p

## Task Specification

**Slug**: SUBTASK_check-ac4p
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Read ALL branches of `view_tree` (or the equivalent state-dispatch logic) in
`crates/chirp-frontend/src/landing.rs` at pinned commit
`decb6196c2c1e6ed421d393a642f0c844cc333ba` and adjudicate AC-4 (partial):

> Is `header_nav()` present in EVERY rendered state of `landing_view` — including
> loading, error, empty/populated, and any other branch?

### Context

This task is a spoke in the SUBTASK_landing-states sub-decomposition
(see `../_GLOBAL.md`). It covers the `header_nav()` aspect of AC-4 only. The
sign-up path correctness, CTA link, and route annotation aspects of AC-4 are
covered by SUBTASK_routing-ctas (a sibling of the parent spoke).

**Dependencies**: none  
**Dependents**: SUBTASK_synthesis-findings

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Sub-decomposition hub | `../_GLOBAL.md` | Shared context, constraints |
| Parent hub | `../../_GLOBAL.md` | Broader review context |
| Contract | `../contracts/_MANIFEST.yaml` | concern_ac4p.md output schema |
| Source file | `crates/chirp-frontend/src/landing.rs` at pinned commit | File under review |

Fetch `landing.rs` from the GitHub API or repository at the pinned commit.
Optionally also read `crates/chirp-frontend/src/app.rs` to confirm how `landing_view`
is called at the route level (but do not duplicate routing-system work from SUBTASK_routing-ctas).

---

## Process Specification

Enumerate ALL branches in `view_tree` (or the equivalent state-dispatch logic in
`landing_view`). For each branch:

1. Name the branch (e.g. loading state, error state, empty content, populated content,
   any other arms in a match expression or conditional).
2. Check whether `header_nav()` is called in that branch.
3. If `header_nav()` is defined elsewhere and conditionally called, trace where.

Report the exact branches and whether `header_nav()` appears in each one.
If `header_nav()` is absent from any branch, that is a finding; if it is present in all
branches, that is a clean note.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `concern_ac4p.md` |
| Location | `SUBTASK_check-ac4p/` (this workspace) |
| Schema | `../contracts/concern_findings_schema.yaml` |

```markdown
## Concern: AC-4 (partial) — header_nav() in every rendered state

**Status**: [clean | has_findings]

## Checked
[What code was read; branches enumerated; criteria applied; pinned commit noted]

## Branch Inventory
| Branch | header_nav() present? | Line reference |
|--------|-----------------------|----------------|
| loading state | yes / no | ... |
| error state | yes / no | ... |
| empty state | yes / no | ... |
| populated state | yes / no | ... |
| (other) | yes / no | ... |

## Findings
[List of findings with location/principle/rationale/severity/resolution, or "None."]

## Clean Notes
[For each branch where header_nav() is present: what was examined and what was found]
```

---

## Success Criteria

- [ ] ALL branches of `view_tree`'s dispatch logic enumerated and accounted for
- [ ] `header_nav()` presence or absence in each branch noted with specific line
- [ ] Every finding or clean note cites file + line at `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- [ ] `concern_ac4p.md` written to this workspace

---

## Suggested Methodology Files

**Task-type row matched**: Code review → Primary: `code-review`, Supporting: `frontend`

- `code-review/CodeReview_Process_Methodology.md` — review process framework; use to structure
  the branch-by-branch examination
- `code-review/CodeReview_Checklist_Methodology.md` — review checklist; apply navigation/UX
  consistency items
- `frontend/Frontend_Component_Design_Methodology.md` — Leptos component patterns; useful for
  understanding view_tree dispatch and component composition

These are the parent's flagged suggestions. Load fewer if inapplicable; load more if your
reading of the brief reveals additional needs.

## Inherited Constraints

- Repository: `Nousix-LLC/nswe-demo` only
- Pinned commit: `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Do not post to the PR
- Cover ONLY the `header_nav()` aspect of AC-4; do not investigate sign-up path correctness,
  CTA link, or route annotation (those belong to SUBTASK_routing-ctas)
- Findings point at repository file paths and lines; never name host paths, private IPs,
  or internal infrastructure details

## Out-of-Scope

- AC-2 (empty_view content) — owned by SUBTASK_check-ac2
- AC-3 (error state recoverability) — owned by SUBTASK_check-ac3
- AC-4 sign-up path, CTA link, route annotation — owned by SUBTASK_routing-ctas
