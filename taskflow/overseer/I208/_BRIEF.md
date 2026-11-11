# _BRIEF.md — NSWE overseer step I208 (persona swe-lead) — ACT: launch code DAG for epic #131

**Depends on**: I207
**Task Kind**: act — load `WORK_SESSION`, `DELIVERABLES_GIT`.

## Context from I207

- ferric-async-forms-r1 DAG forked (epic #130, issues #130/#143/#144/#145). Board: #130/#143/#144/#145 moved to In Progress, all assigned to mattsmcknight.
- 3 free DAG slots (was 4, used 1 for ferric-async-forms-r1).
- Next step: launch ferric-router-r1 (epic #131) code DAG.
- **STATE**: `taskflow/overseer/I207/project_state.json` (updated by I207).
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`.

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/DELIVERABLES_GIT.md`.

### 2. Write the code DAG brief for epic #131

**Goal slug**: `ferric-router-r1`
**Branch**: `work/ferric-router-r1`
**Epic**: #131 — Ferric 1.0: Client-side Router (usable_early)
**Issues covered**: #146 (Nested routes and outlet), #147 (Navigation, active links, and accessibility)

Write a full brief at `taskflow/dags/ferric-router-r1/_BRIEF.md`. The brief must include:
- Objective: implement epic #131 (Client-side Router) on branch `work/ferric-router-r1`
- Acceptance criteria per issue: #146, #147 with their criteria
- Inputs: design documents at `design/ferric/router.md` and `design/ferric/scope-and-requirements.md` (PR #128, merged) in repo `Nousix-LLC/nswe-demo`; prior landed work: PR #188 (epic #129, Authoring Model — commit aa24687) which delivers reactive signals, vdom, view! macro, component model, context
- Declared output: commits on `work/ferric-router-r1`, one PR closing #131/#146/#147, root `SYNTHESIS.md`
- Concerns: correctness against design, CI (fmt/clippy/test/wasm/doc/image all PASS), test coverage, Rust idioms, API surface compatibility with the authoring model on main
- Constraints: Nousix-LLC/nswe-demo, branch `work/ferric-router-r1`, no force-push, do not modify design documents

### 3. Fork the code DAG

Write `taskflow/dags/ferric-router-r1/_FORK.md` (launch_agent: swe-coder, disposition: reap-whole-after-land, launch_context: application=software).

Fork the DAG (swe-coder).

### 4. Update board and STATE

- Move issues #131, #146, #147 to "In Progress" on the board (project PVT_kwDOEB9jls4BlZH4).
- Assign issues #131, #146, #147 to the authenticated gh user.
- Append the goal to STATE (`taskflow/overseer/I207/project_state.json` → write updated state to `taskflow/overseer/I208/project_state.json`):
  - `dags_in_flight`: add ferric-router-r1 entry (update ferric-async-forms-r1 state to RUNNING)
  - `free_dag_slots`: 2 (was 3, used 1)
  - `main_sha`: aa2468771eccd9e2ee79c12c79b8943fca18e07a (unchanged)

### 5. Write CONTINUE.md and schedule I209

I209 follows: board check / watch DAG folds (ferric-async-forms-r1, ferric-router-r1).
Write CONTINUE.md and report terminal.

## Notes

- Design file `design/ferric/router.md` is the primary source for epic #131. Load it for the brief.
- #146 covers nested routes + outlet; #147 navigation, active-route awareness, accessible links.
- The board item IDs are: issue_131=PVTI_lADOEB9jls4BlZH4zhFl_Kc, issue_146=PVTI_lADOEB9jls4BlZH4zhFl_mw, issue_147=PVTI_lADOEB9jls4BlZH4zhFl_n8.
- The DAG runs as swe-coder — do not prescribe its decomposition.
