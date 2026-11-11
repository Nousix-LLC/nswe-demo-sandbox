# Task: Ferric 1.0 — the release plan / traceable backlog (concern 9b)

## Task Specification
**Slug**: SUBTASK_release_plan
**Task Kind**: standard
**Status**: Pending

### Objective
Turn the design and the release bar into **epics and work-items under the Ferric epic (#1)**: each epic a
coherent capability that one code DAG can build, review, and land as one change; each work-item's acceptance
criteria tracing back to the `REQ-*`/`BAR-FERRIC-*` and the design section; with dependencies and an order that
reaches a usable framework early and the full 1.0 bar after. **Fold the existing router (#5) and HTTP (#6)
issues into this structure** — extend or supersede, never duplicate.

### Context
Part of the Ferric 1.0 framework design (see `../_GLOBAL.md`). This is the planning artifact `SUBTASK_file_backlog`
consumes to create/extend the board issues; it is not the issues themselves. It conforms to the epic/work-item
schema in `../contracts/id_and_traceability_schema.yaml`.

**Dependencies**: `SUBTASK_scope_and_requirements`, all seven capability spokes, and `SUBTASK_release_bar`.

### Distinct concerns to cover (name them; let your own evaluation decide how to split)
- **The epics**: the coherent, landable capabilities under #1 (e.g. authoring macro, SSR+hydration,
  async/forms/events, router, HTTP client, docs/starter, release/semver, benchmark) — each mapped to its
  design area(s) and staged (usable-early vs one_oh).
- **The work-items**: per epic, the work-items whose acceptance criteria cite the `REQ-*`/`BAR-*` they satisfy.
- **Dependencies & order**: the dependency edges between epics and the order that reaches a usable framework
  early then the full bar; which epic is the SSR must-have.
- **The #5/#6 fold**: exactly how board issues #5 and #6 are superseded/extended by the router/HTTP epic(s), so
  `file_backlog` edits them rather than filing duplicates (identity I7).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context + constraints. |
| Contract | `../contracts/` | The epic/work-item schema, trace rules (I6), fold rule (I7). |
| Release bar | `../SUBTASK_release_bar/release-bar.md` | The `BAR-FERRIC-*` + stages the work-items cover. |
| All REQ registers | `../SUBTASK_scope_and_requirements/…` + each capability `../SUBTASK_*/<area>.md` | The requirements each work-item traces to. |
| Board | epic #1 + its children #5, #6 (and any others) | The existing structure to extend/supersede, de-duplicated. |

### Declared output
- `release-plan.md` (this task's workspace) — the epics + work-items under #1, acceptance criteria tracing to
  REQ/BAR, dependencies + order, and the explicit #5/#6 fold. Repo target `design/ferric/release-plan.md`.

### Success criteria
- [ ] Every epic sits under #1, maps to ≥1 design area, and is a single coherent landable capability with its
      dependencies stated (identity I6).
- [ ] Every `one_oh` `BAR-FERRIC-*` is covered by ≥1 work-item; every work-item cites the `REQ-*`/`BAR-*` and
      design section it traces to.
- [ ] The order reaches a usable framework early and the full 1.0 bar after; the SSR must-have epic is marked.
- [ ] The #5/#6 fold is explicit and actionable (what each issue becomes), feeding identity I7 — no duplicates.
- [ ] Tickets say what the framework needs and how it will be judged, not how to build it.

### Constraints
- Do not redefine any `REQ-*`/`BAR-*` (identity I1). Design the plan; `file_backlog` files it.
- Honor the writing-voice rules; GitHub-bound text names only repository identities, no system details.
