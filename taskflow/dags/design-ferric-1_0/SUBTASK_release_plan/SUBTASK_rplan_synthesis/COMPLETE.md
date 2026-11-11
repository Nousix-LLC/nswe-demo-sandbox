# COMPLETE — SUBTASK_rplan_synthesis

## What this task did

Read `epics-and-order.md` and `work-items.md` from the predecessor tasks, verified the three seam identities from the SUBTASK_release_plan contract, and assembled the final `release-plan.md`.

## Identity verification results

- **J1 — epic ids consistent:** All 8 epic titles in work-items.md resolve to epics in epics-and-order.md. No orphan work items. PASSES.
- **J2 — fold explicit:** epics-and-order.md names issues #5 and #6 in the epic table and in the dedicated fold section; work-items.md section headers repeat "extends #5" / "extends #6"; release-plan.md carries the exact issue numbers in the fold table. PASSES.
- **J3 — BAR coverage:** work-items.md includes an explicit coverage verification table confirming all 17 one_oh BAR-FERRIC-* criteria are covered by ≥1 work-item acceptance criterion. No gaps found. PASSES.

No identity failures. The document was assembled without patches or gap notes.

## Outputs produced

- `release-plan.md` — in this task workspace (SUBTASK_rplan_synthesis/)
- `../release-plan.md` — in the parent workspace (SUBTASK_release_plan/)

Both copies are identical. The parent-workspace copy is the declared output that SUBTASK_design_pr and SUBTASK_file_backlog will find at the path declared in the parent _BRIEF.md.

## Declared output path

`../release-plan.md` (the copy SUBTASK_design_pr and SUBTASK_file_backlog consume)
