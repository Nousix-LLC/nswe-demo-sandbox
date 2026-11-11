# Task: Turn the design into a traceable board backlog

## Task Specification
**Slug**: SUBTASK_delivery_backlog
**Task Kind**: standard
**Status**: Pending

### Objective
Turn the design and its release bar into a backlog on the project board: epics (one epic = one coherent,
landable code goal, with dependencies on other epics stated) and issues with acceptance criteria that **trace**
to `REQ-*`/`BAR-*` and to the design document in the repository, de-duplicated against the existing board, each
issue placed under its epic in a dependency order that reaches a usable product early and the release bar after.

### Context
Part of design-chirp-r1 (see `../_GLOBAL.md`, `../contracts/`). You own the epics/issues and the trace map. The
tickets say **what** the product needs and **how it will be judged**, not how to build it, and read as the
repository's own (they trace to the design doc in the repo, not to any taskflow). Check the board before filing
so you extend/supersede rather than duplicate.
**Dependencies**: `SUBTASK_design_pr` (so the design files exist at known repo paths on the branch),
`SUBTASK_release_bar`. **Dependents**: `SUBTASK_synthesis`.

## Distinct concerns in this task
Evaluate your own scope against these and decompose if warranted:
- **Epic structure** — grouping the work into coherent, landable code goals that extend the existing EPIC
  trackers (#1 ferric, #2 chirp, #3 devops) or add new epics, with inter-epic dependencies stated.
- **Issues with traceable acceptance criteria** — each issue citing >=1 `REQ-*`/`BAR-*` and the design doc
  section, with acceptance criteria someone can test.
- **De-duplication & ordering** — reconcile against existing open issues (#23/#24/#25/#27), place each issue
  under exactly one epic, and order by dependency (usable product early, release bar after).

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context/constraints |
| Contract | `../contracts/` (read-only) | Epic/issue schema; `REQ-*`/`BAR-*` trace scheme |
| Design PR record | `../SUBTASK_design_pr/outputs/design-pr.md` | PR #, branch, and repo paths of the design docs to trace to |
| Release bar | `../SUBTASK_release_bar/outputs/release-bar.md` | `BAR-*` criteria to build the order around |
| Board | `Nousix-LLC/nswe-demo` issues/epics (#1,#2,#3; #23,#24,#25,#27) | De-duplicate and place |

## Methodology
Bundle IDs (Domain Mapping): **Delivery** (primary — design-to-backlog planning); **Product Strategy**,
**Release Definition** (supporting).

## Output
- Epics and issues filed/updated on the board, placed under their epics in dependency order.
- `SUBTASK_delivery_backlog/outputs/backlog.md` — the index of epics and issue numbers with the
  `issue ↔ REQ/BAR ↔ design-doc` trace map (for the synthesis gate to verify).

## Success criteria
- [ ] Composes against `../contracts/`; every issue cites >=1 `REQ-*`/`BAR-*` and a design-doc section.
- [ ] One epic = one coherent landable code goal; each issue under exactly one epic; inter-epic deps stated.
- [ ] De-duplicated against the existing board (#23/#24/#25/#27 folded, not duplicated); order reaches a usable
      product early and the bar after.
- [ ] Every tracked item reads as repository-native (no host/system/taskflow detail, no attribution trailers).

## Constraints
- Tickets, not code; tickets describe what/how-judged, never how-to-build.
- Scope limited to `Nousix-LLC/nswe-demo`'s board. Repository-ready hygiene throughout.
