# Task: Ferric 1.0 — file the backlog on the board (delivery)

## Task Specification
**Slug**: SUBTASK_file_backlog
**Task Kind**: standard
**Status**: Pending

### Objective
Turn the release plan into the board backlog: create the epics and work-items under the **Ferric epic (#1)**,
each with acceptance criteria that trace to the design (the `REQ-*`/`BAR-*` and the design doc in the PR), in
dependency order. **Extend/supersede the existing router (#5) and HTTP (#6) issues** rather than filing
duplicates, and de-duplicate against whatever already sits under #1.

### Context
Part of the Ferric 1.0 framework design (see `../_GLOBAL.md`). The source of truth is
`../SUBTASK_release_plan/release-plan.md`; the design the issues trace to lives in the PR produced by
`SUBTASK_design_pr`.

**Dependencies**: `SUBTASK_release_plan` (the plan to file) and `SUBTASK_design_pr` (so issues can reference the
design doc paths / PR in the repo).

### What to do (approach, not a runbook)
- Read the board under epic #1 first (its current children, including #5 and #6); de-duplicate.
- Create each epic and work-item from `release-plan.md`, placing each under #1 in dependency order, with
  acceptance criteria citing the `REQ-*`/`BAR-*` and the `design/ferric/…` section it traces to.
- For #5 and #6: extend/supersede them per the plan's fold (edit scope, re-link under the router/HTTP epic, or
  close-as-superseded with a pointer) — do **not** open duplicate router/HTTP issues.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context + constraints. |
| Release plan | `../SUBTASK_release_plan/release-plan.md` | The epics/work-items + the #5/#6 fold (authoritative). |
| PR record | `../SUBTASK_design_pr/design_pr.md` | The branch/PR and repo doc paths the issues reference. |
| Board | epic #1 + children #5, #6 | The existing structure to extend; de-duplicate against it. |

### Declared output
- `filed_backlog.md` (this task's workspace) — a record of the issues created/edited, indexed by epic, with
  their numbers/URLs, and an explicit note of how #5 and #6 were folded (edited/superseded, not duplicated).

### Success criteria
- [ ] Every epic and work-item from the plan is on the board under #1, in dependency order, acceptance criteria
      tracing to the design (identity I6).
- [ ] #5 and #6 are extended/superseded, not duplicated (identity I7); the record states exactly what happened
      to each.
- [ ] No duplicate of an existing board item was created.

### Constraints
- Repo scope `Nousix-LLC/nswe-demo` only. **No attribution trailers**; issues/comments name only repository
  identities and carry no host, cluster, SSH, path, or system detail.
- Tickets say what the framework needs and how it will be judged, not how to build it.
