# SUSPENSION.md — SUBTASK_release_plan

## Status: Suspended (NeedsDecompose)

**Decompose evaluation**: NeedsDecompose  
**Suspended at**: 2026-10-29

## Why this task decomposed

The brief named four explicit distinct concerns — epics definition, work-items
with traced acceptance criteria, dependencies/order, and the #5/#6 fold — firing
the enumerated-concerns scope trigger. The expected output (a full
epic+work-item backlog for ~8 design areas, ~5–7 work-items each) also exceeded
the 400-line output-size threshold. Reading nine predecessor files plus the
GitHub board would consume significant context. The three concerns form a natural
sequential pipeline (define epics → populate work-items → assemble document) that
maps cleanly to three atomic tasks.

## Child tasks materialized

| Task id | Description | Output |
|---------|-------------|--------|
| `SUBTASK_rplan_epics` | Define the epic landscape: what epics exist under #1, their design-area mappings, stages, dependencies, and the explicit #5/#6 fold | `epics-and-order.md` |
| `SUBTASK_rplan_work_items` | For each epic, write work-items with acceptance criteria citing REQ-*/BAR-FERRIC-* and design section | `work-items.md` |
| `SUBTASK_rplan_synthesis` | Assemble final `release-plan.md`; verify identities J1/J2/J3 | `release-plan.md` |

## Resumption condition

All three child tasks reach terminal lifecycle states (COMPLETED or FAILED). The
synthesis child (`SUBTASK_rplan_synthesis`) is the gate; it produces `release-plan.md`
at this workspace root, which SUBTASK_design_pr and SUBTASK_file_backlog depend on.

## Named-state authored

- `_GLOBAL.md` — subtree hub for this decomposition
- `contracts/_MANIFEST.yaml` — thin seam contract declaring intermediate artifact
  ownership and inherited parent contracts
- `SUBTASK_rplan_epics/_BRIEF.md` — brief for child 1
- `SUBTASK_rplan_work_items/_BRIEF.md` — brief for child 2
- `SUBTASK_rplan_synthesis/_BRIEF.md` — brief for child 3 (synthesis gate)
