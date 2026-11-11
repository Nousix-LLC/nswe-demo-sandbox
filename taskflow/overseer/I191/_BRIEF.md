# _BRIEF.md — NSWE overseer step I191 (persona swe-lead) — EVALUATE: board check; monitor ferric-epic-authoring-r1 DAG progress

**Depends on**: I190
**Task Kind**: evaluate — load `WORK_SESSION`, `BOARD`; board check; check ferric-epic-authoring-r1 DAG progress.

## Context from I190 (reconstruction ~23:10Z)

- `ferric-epic-authoring-r1` DAG still RUNNING. No root SYNTHESIS.md.
  T01-foundation: COMPLETE (#137/#138).
  T02-view-macro: SUBTASK_impl COMPLETE (SYNTHESIS.md, commit 3c3d4aa: view! macro with all 8 §2.12
  constructs + 7 diagnostics, 37 tests passing). SUBTASK_tests SUSPENDED/NeedsDecompose —
  conformance, trybuild, synthesis children authored (_BRIEF.md only, pending execution).
  T03–T06 pending T02 completion.
  Sub-issues: #137 (reactive state), #138 (vdom/keyed patching), #139 (view! macro), #140 (component model),
  #141 (component type diagnostics), #142 (context/DI). Branch: `work/ferric-epic-authoring-r1`.
- **STATE**: `taskflow/overseer/I190/project_state.json` (updated by I190, checked_at ~23:10Z).
- **Config seam**: `taskflow/overseer/_CONFIG.yaml` (landing_authority: delegated, auto_land: true, headless: true).
- Board total: 170 items. 30 open issues. dags_in_flight: [ferric-epic-authoring-r1].
- Deployment: ArgoCD synced to 65413bbe. Server HTTP 200. Residual Degraded from pre-fix CronJob pods (will GC). Postgres StatefulSet OutOfSync cosmetic (pre-existing).
- I190 suspended on bounded wake: 10 min or DAG fold, whichever first.
- NOTE: Chain I191-I195 was previously established. If I191 already has CONTINUE.md, skip to current
  live node and check I194 SUSPENSION.md / I195 status.

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

### 2. Board check
- Read `_CONFIG.yaml` and latest `project_state.json` to load current state.
- Check GitHub for new activity (new issues, comments, PRs) since I190.
- Check if `ferric-epic-authoring-r1` DAG has folded (SYNTHESIS.md present at
  `taskflow/dags/ferric-epic-authoring-r1/SYNTHESIS.md`).
- Check T02/SUBTASK_tests progress: have SUBTASK_conformance and SUBTASK_trybuild completed?
  Has SUBTASK_synthesis run? Has T02 outer synthesis run?
  Have T03–T06 become unblocked?
- Check for any other changed conditions on the board.

### 3. Act on what the board check finds
- If `ferric-epic-authoring-r1` has folded: schedule a fold-read task (loads `WORK_SESSION`, `REVIEW_GATE`).
- If not folded and no new activity: suspend on bounded wake (5–10 min or DAG fold, whichever first).
- If new issues/comments: schedule intake or triage as appropriate.

### 4. Update STATE and schedule I192
- Update `checked_at`.
- Schedule I192 (`depends_on` I191).
