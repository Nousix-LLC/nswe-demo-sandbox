# COMPLETE — SUBTASK_rplan_work_items

## What was done

Produced `work-items.md` — a structured list of 28 work items across all 8 epics from
`epics-and-order.md`, each with a title stating what the framework needs, acceptance
criteria citing the specific `REQ-*` and `BAR-FERRIC-*` ids the item satisfies plus the
design-doc section it traces to, a `depends_on` edge, and one verification method from the
schema vocabulary.

## Declared output

- `work-items.md` in this workspace (`SUBTASK_rplan_work_items/`)

## Coverage

All 29 BAR-FERRIC-* criteria are covered (12 usable_early, 17 one_oh). Every one_oh
criterion appears in ≥1 work-item acceptance criterion (identity J3 satisfied). No
REQ-*/BAR-FERRIC-* id was redefined; all ids come from epics-and-order.md and
release-bar.md.

## Inputs consumed

- `../SUBTASK_rplan_epics/epics-and-order.md` — the epic landscape
- `../../SUBTASK_release_bar/release-bar.md` — the BAR-FERRIC-* register with
  stage and REQ-* references for each criterion
- `../../contracts/id_and_traceability_schema.yaml` — work-item schema and
  verification_method vocabulary
- `../contracts/_MANIFEST.yaml` — intermediate seam contract and identity J3 definition

## Composes into

`SUBTASK_rplan_synthesis` reads `work-items.md` alongside `epics-and-order.md` to
assemble the final `release-plan.md`.
