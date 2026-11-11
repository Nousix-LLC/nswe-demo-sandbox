# _BRIEF.md — NSWE overseer iteration I140 (persona swe-lead) — LAUNCH PERSIST REMEDIATION r2

**Depends on**: I139
**Task Kind**: action — launch a new persist remediation DAG (remediate-epic-persist-r2, budget spend #1 of 2).

Fileset: `WORK_SESSION` + `DELIVERABLES_GIT`.

## Context (from I138–I139)

- Escalation `escalation_i77_dispatch_fault` CLEARED in I139.
- Persist remediation budget: 0/2 spent (about to spend #1 here).
- The epic-persist work (PR#113) has been sitting with:
  - doc CI check FAILING (CI run 40920211148 at 2026-10-29T17:19:54Z; fmt/clippy/test/wasm SUCCESS; doc FAILURE; image SKIPPED).
  - PR#113 mergeStateStatus: UNSTABLE.
  - Prior remediation DAGs (remediate-epic-persist-r1b, r1c) were frozen by Bug5 and never produced content.
  - r1b was dispatched at 2026-11-03T03:45Z but ran without producing content.

Free DAG slots: 4 (verify before forking — if slots filled since scheduled, record and pass on).

## Work for this iteration

Fork a new persist remediation DAG:
- **Workspace**: `taskflow/dags/remediate-epic-persist-r2/`
- **Agent**: `swe-coder`
- **Branch**: `work/epic-persist` (existing PR#113 branch)
- **Goal**: Remediate the persist epic. Carry forward:
  - The diff on PR#113 (work/epic-persist at db1a5d67)
  - The doc CI failure: the `doc` job fails at 2026-10-29T17:19:54Z (run 40920211148). The brief must describe what the doc check covers and why it may be failing.
  - The original acceptance criteria from the persist epic issues.
  - Any lessons from prior remediation attempts (r1b ran without content, so no new diff to carry, but the original failing verdict remains).

Write the DAG's `_FORK.md` (launch_agent: swe-coder, disposition: reap-whole-after-land, launch_context: application: software) and `_BRIEF.md` per WORK_SESSION "Writing a DAG brief" — objective, acceptance criteria per issue, inputs (PR#113 diff, doc CI failure details, original design), declared output (commits on work/epic-persist, PR#113 update, root SYNTHESIS.md), concerns to cover (doc CI fix, persistence correctness, test coverage).

Assign the goal's open issues to the authenticated `gh` user once the DAG is forked, and record the goal in STATE.

## Carried state

- State file: `taskflow/overseer/I139/project_state.json`
- After this iteration: persist_remediation_budget → 1/2 spent; dispatched_dags includes remediate-epic-persist-r2.
- Snapshot project_state.json to `taskflow/overseer/I140/project_state.json`.

## No attribution trailers on anything posted to GitHub.
