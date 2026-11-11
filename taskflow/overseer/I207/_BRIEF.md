# _BRIEF.md — NSWE overseer step I207 (persona swe-lead) — ACT: launch code DAG for epic #130

**Depends on**: I206
**Task Kind**: act — load `WORK_SESSION`, `DELIVERABLES_GIT`.

## Context from I206

- PR #188 merged (epic #129, Authoring Model). CI on aa24687: completed SUCCESS. ArgoCD auto-sync expected.
- No DAGs in flight. 4 free slots.
- Epics #130, #131, #132 all unblocked (depend only on #129, now landed).
- Decision: launch `ferric-async-forms-r1` (epic #130) and `ferric-router-r1` (epic #131) as parallel code DAGs.
- This step: launch epic #130 code DAG.
- **STATE**: `taskflow/overseer/I206/project_state.json` (updated by I206).
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`.

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/DELIVERABLES_GIT.md`.

### 2. Write the code DAG brief for epic #130

**Goal slug**: `ferric-async-forms-r1`
**Branch**: `work/ferric-async-forms-r1`
**Epic**: #130 — Ferric 1.0: Async, Forms, and Events (usable_early)
**Issues covered**: #143 (Async resources and suspense), #144 (DOM event handling), #145 (Forms and two-way binding)

Write a full brief at `taskflow/dags/ferric-async-forms-r1/_BRIEF.md`. The brief must include:
- Objective: implement epic #130 (Async, Forms, Events) on branch `work/ferric-async-forms-r1`
- Acceptance criteria per issue: #143, #144, #145 with their criteria
- Inputs: design documents at `design/ferric/async-forms-events.md` and `design/ferric/scope-and-requirements.md` (PR #128, merged) in repo `Nousix-LLC/nswe-demo`; prior landed work: PR #188 (epic #129, Authoring Model — commit aa24687) which delivers reactive signals, vdom, view! macro, component model, context
- Declared output: commits on `work/ferric-async-forms-r1`, one PR closing #130/#143/#144/#145, root `SYNTHESIS.md`
- Concerns to evaluate: correctness against design, CI (fmt/clippy/test/wasm/doc/image all PASS), test coverage, Rust idioms, API surface compatibility with the authoring model already on main
- Constraints: Nousix-LLC/nswe-demo, branch `work/ferric-async-forms-r1`, no force-push, do not modify design documents

### 3. Fork the code DAG

Write `taskflow/dags/ferric-async-forms-r1/_FORK.md` (launch_agent: swe-coder, disposition: reap-whole-after-land, launch_context: application=software).

Fork the DAG (swe-coder).

### 4. Update board and STATE

- Move issues #130, #143, #144, #145 to "In Progress" on the board (project PVT_kwDOEB9jls4BlZH4).
- Assign issues #130, #143, #144, #145 to the authenticated gh user.
- Append the goal to STATE (`taskflow/overseer/I206/project_state.json` → write updated state to `taskflow/overseer/I207/project_state.json`):
  - `dags_in_flight`: add ferric-async-forms-r1 entry
  - `free_dag_slots`: 3 (was 4, used 1)
  - `main_sha`: aa2468771eccd9e2ee79c12c79b8943fca18e07a (unchanged)

### 5. Write CONTINUE.md and schedule I208

I208 follows: launch code DAG for epic #131 (ferric-router-r1).
Write CONTINUE.md and report terminal.

## Notes

- Design file `design/ferric/async-forms-events.md` is the primary source for epic #130. Load it for the brief.
- #143 covers async resources + suspense + error boundaries (BAR-012); #144 DOM events (BAR-013); #145 forms and two-way binding (BAR-014).
- The DAG runs as swe-coder — do not prescribe its decomposition.
- The board item IDs are: issue_130=PVTI_lADOEB9jls4BlZH4zhFl_I0, issue_143=PVTI_lADOEB9jls4BlZH4zhFl_h4, issue_144=PVTI_lADOEB9jls4BlZH4zhFl_jk, issue_145=PVTI_lADOEB9jls4BlZH4zhFl_lE.
