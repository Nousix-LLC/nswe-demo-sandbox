# SUBTASK_rplan_epics — complete

**Status:** completed
**Output:** `epics-and-order.md`

## What was produced

`epics-and-order.md` defines eight epics under issue #1, one per capability design area:

- Four usable_early epics: Authoring Model, Async/Forms/Events, Client-side Router, HTTP/JSON Client
- Four one_oh epics: SSR and Hydration, Docs and DX, Performance and Benchmark, Release and Distribution

The document includes:
- A structured table of all epics with design areas, BAR-FERRIC coverage, stage, depends_on, and fold actions
- The #5/#6 fold: both issues are closed (done); their successor epics extend the frozen surfaces additively
- Rationale per epic (1–2 sentences each)
- An ordering narrative with a dependency diagram
- A single sentence marking SSR and Hydration (BAR-FERRIC-004, must_have: true) as the one_oh must-have

## Success criteria check

- [x] Every epic maps to ≥1 design area; every design area from the 8 capability spokes is covered
- [x] SSR and Hydration is marked as the one_oh must-have (BAR-FERRIC-004, REQ-FW-004)
- [x] Ordering narrative reaches a usable framework after the four usable_early epics land
- [x] #5 and #6 fold explicit by issue number and action (both extended, not superseded)
- [x] No REQ-* or BAR-FERRIC-* id redefined; all ids read from design spoke documents
