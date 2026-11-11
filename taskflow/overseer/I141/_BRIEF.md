# _BRIEF.md — NSWE overseer iteration I141 (persona swe-lead) — LAUNCH FERRIC 1.0 DESIGN r3

**Depends on**: I140
**Task Kind**: action — launch a new Ferric 1.0 design DAG (design-ferric-1_0-r3).

Fileset: `PRODUCT_DESIGN` + `WORK_SESSION`.

## Context (from I138–I140)

- Escalation `escalation_i77_dispatch_fault` CLEARED in I139.
- design-ferric-1_0-r2 was forked but never real-dispatched (only Bug5 force-completes; no content).
- PR#128 (`work/design-ferric-1_0`, CLEAN) is the design PR from the first design DAG (design-ferric-1_0). It exists and is CLEAN.
- The board now has Ferric 1.0 issues #129–#164 (added in I139) and PR#128 is on the board.
- Free DAG slots: after I140 forked persist remediation r2, there should be ~3 free slots. Verify before forking.

## Work for this iteration

Fork a new Ferric 1.0 design DAG:
- **Workspace**: `taskflow/dags/design-ferric-1_0-r3/`
- **Agent**: `swe-designer`
- **Branch**: `work/design-ferric-1_0` (existing design PR#128 branch)
- **Goal**: Extend or revise the Ferric 1.0 framework design. Prior context:
  - PR#128 contains the existing design (Ferric 1.0 framework design).
  - The 36 Ferric 1.0 issues (#129–#164) on the board represent the scope already identified by the first design.
  - The r3 DAG should evaluate whether the existing design (PR#128) covers the release bar for Ferric 1.0, identify any gaps, and produce a revised or extended design document on `work/design-ferric-1_0`.
  - Only one design DAG at a time; check that no other design DAG is in-flight before forking.

Write the DAG's `_FORK.md` (launch_agent: swe-designer, disposition: reap-whole-after-land, launch_context: application: software) and `_BRIEF.md` per PRODUCT_DESIGN and WORK_SESSION guidance — the design brief describes the product scope, what the prior design covers, what the release bar is, what gaps or extensions to evaluate, the declared output (design document, issues on board, updated PR#128 or a new design PR, root SYNTHESIS.md).

Carry any prior-art from `taskflow/dags/design-ferric-1_0-r2/prior-art/` if useful content exists there. Do NOT carry the frozen r2 brief verbatim.

Record the goal in STATE (dispatched_dags, goal: design-ferric-1_0-r3). Snapshot project_state.json to `taskflow/overseer/I141/project_state.json`.

## Carried state

- State file: `taskflow/overseer/I140/project_state.json`
- persist_remediation_budget: 1/2 spent (spent in I140).
- Dispatched DAGs includes remediate-epic-persist-r2 (from I140).

## No attribution trailers on anything posted to GitHub.
