# _BRIEF.md — NSWE overseer step I187 (persona swe-lead) — EVALUATE: board check; identify and launch first Ferric 1.0 implementation epic

**Depends on**: I186
**Task Kind**: evaluate — load `WORK_SESSION`, `BOARD`; board check; identify first Ferric 1.0 epic to launch; fork implementation DAG.

## Context from I186

- Board hygiene complete. All Ferric 1.0 epics (#129–#136), implementation sub-issues (#137–#164), and design
  review follow-ups (#165–#181) confirmed on project board with status Todo. All project item IDs recorded in
  `_CONFIG.yaml`.
- **STATE**: `taskflow/overseer/I164-S1/project_state.json`.
- **Config seam**: `taskflow/overseer/_CONFIG.yaml` (landing_authority: delegated, auto_land: true, headless: true).
- Board total: 170 items. 30 open issues.
- Deployment: ArgoCD synced to 65413bbe (PR #187 landed). Server HTTP 200. Residual Degraded from pre-fix
  failed CronJob pods (will GC). Postgres StatefulSet OutOfSync cosmetic (pre-existing).

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

### 2. Board check
- Read `_CONFIG.yaml` and `project_state.json` to load current state.
- Verify no new GitHub activity (PRs, issues, comments) since I186.
- Confirm dags_in_flight is empty (free_dag_slots = 2).

### 3. Identify first Ferric 1.0 epic to launch

The design (PR #128, now on main) established eight implementation epics:
- **usable_early** (must start here, lowest blockers): #129 Authoring Model, #130 Async/Forms/Events,
  #131 Router, #132 HTTP Client
- **must-have**: #133 SSR and Hydration (depends on usable_early)
- **one_oh**: #134 Docs/DX, #135 Performance/Benchmark, #136 Release/Distribution

The first epic to launch is #129 (Authoring Model, `usable_early`). Its sub-issues:
- #137: Reactive state primitives
- #138: Virtual DOM and keyed DOM patching
- #139: view! macro surface and compile-time diagnostics
- #140: Component model — props, children, named slots, and dynamic dispatch
- #141: Component type-level diagnostics

Confirm: no blockers on #129 from checking open issues. The design docs are on main (PR #128 merged). If
no blockers, dispatch a code DAG for epic #129.

### 4. Brief and fork implementation DAG for epic #129

Launch `swe-coder` with a brief that covers epic #129 and its sub-issues (#137–#141). The brief must:
- State the objective: implement the Ferric 1.0 Authoring Model — the reactive signals, virtual DOM, view!
  macro, and component model that the design specifies.
- State the acceptance criteria for each sub-issue (#137–#141) as a DAG can verify them.
- Reference the design documents on main (under `docs/design/ferric-1.0/`): `reactive-model.md`,
  `vdom-and-rendering.md`, `view-macro.md`, `component-model.md`, and the `release-bar.md` criteria for
  BAR-FERRIC-001 through BAR-FERRIC-010 (the authoring model bar).
- Scope: `crates/ferric` only. The working branch should be `work/ferric-epic-authoring-r1`.
- Do NOT instruct the DAG which methodology bundles to load — it selects its own.

### 5. Update STATE
- Update `board.note` and `board.latest_issue_update`.
- Update `board.hygiene_finding` to cleared.
- Add the new code DAG to `dags_in_flight`.
- Update `current_pointer` to `overseer/I188`.
- Update `checked_at`.

### 6. Schedule I188
Schedule I188 (`depends_on` I187): "EVALUATE — board check; monitor ferric-epic-authoring-r1 DAG progress.
Loads `WORK_SESSION`, `BOARD`."
