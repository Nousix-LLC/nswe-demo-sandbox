# _BRIEF.md — NSWE overseer step I247 (persona swe-lead) — EVALUATE: check escalation + pick next epic

**Depends on**: I246
**Task Kind**: evaluate — load `appfiles/WORK_SESSION.md`, `appfiles/BOARD.md`.

## Context from I246 (EVALUATE: deployment check + board check after PR #210 land)

- **CI on merge commit `945fade38abd6b053268501f3801734756f02502`**: all 6 jobs PASS (test, fmt, wasm, doc, clippy, image)
- **Deployment**: chirp-server pod running `sha256:f845ca8c` (d8230fea build) — no change needed; PR #210 was CHANGELOG-only
- **Board confirmed**:
  - #132 (`PVTI_lADOEB9jls4BlZH4zhFl_MI`) → Done ✅
  - #148 (`PVTI_lADOEB9jls4BlZH4zhFl_pM`) → Done ✅
  - #214–#222 all on board as Todo ✅ (filed in I245, confirmed I246)
  - No items currently In Progress
- **Escalation `escalation_ferric_async_forms_budget_exhausted`**: ACTIVE — no user response on PR #193 since escalation posted (last comment 2026-11-04T20:18:24Z was the escalation itself). Clearing condition NOT met.
- **usable_early epics**: #129 Done, #131 Done, #132 Done; #130 (async-forms) escalated/blocked
- **one_oh / must-have next**: #133 (SSR and Hydration, must-have), #134 (Docs/DX), #135 (Performance), #136 (Release/Distribution) all Todo
- **Product epics**: #34–#43 (core product loop, UX accuracy) all Todo
- **STATE**: `taskflow/overseer/I246/project_state.json`
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`. Read `_CONFIG.yaml`.

### 2. Check ferric-async-forms escalation clearing condition

The clearing condition is: user comments on PR #193 (https://github.com/Nousix-LLC/nswe-demo/pull/193) or files a follow-up issue indicating choice (extend budget or defer).

Check PR #193 comments for any new user response since 2026-11-04T20:18:24Z:
```bash
gh pr view 193 --repo Nousix-LLC/nswe-demo --comments
```

If cleared (user chose extend OR defer):
- Record the decision in STATE
- If extend: schedule I248 as ACT to fork ferric-async-forms-r3 code DAG
- If defer: close PR #193, move #130/#143/#144/#145 back to Todo backlog, clear escalation, pick the next non-escalated item

If NOT cleared: note it and move on to next item from non-escalated backlog.

### 3. Identify next ready item

The backlog priority order per BOARD.md:
1. Bugs and security findings (none known)
2. Delivery blockers (none)
3. Product work moving toward release bar

The most ready non-escalated items are:
- **#133** (Ferric 1.0 — SSR and Hydration, must-have one_oh): Next major epic to implement. Check whether sub-issues exist under #133 and what the design spec says.
  ```bash
  gh issue view 133 --repo Nousix-LLC/nswe-demo
  gh issue list --repo Nousix-LLC/nswe-demo --state open --milestone 3 --limit 30
  ```
- **Product epics #34–#43** (core product loop): The app-layer work. Check their acceptance criteria and dependencies.

Assess: does #133 have sub-issues filed? Is the design for SSR/Hydration in the design documents (from PR #128)? If the design exists and sub-issues are filed, #133 is ready to brief.

### 4. Decide next action and write I248 brief

Based on board assessment:
- If #133 is ready (design exists, sub-issues filed): schedule I248 as ACT to fork code DAG for #133
- If #133 needs design first: schedule I248 as ACT to fork design DAG for #133 scope
- If product epics are higher priority: schedule I248 as ACT to fork code DAG for the top product epic

Write I248's `_BRIEF.md`. Per WORK_SESSION.md: a code DAG brief states objective, acceptance criteria (the issues' acceptance criteria, translated), scope, inputs (design docs, existing code), declared output (PR, SYNTHESIS.md), and concerns to cover. Tell the DAG *what to evaluate*; it chooses its own methodologies.

### 5. Update STATE

Write `taskflow/overseer/I247/project_state.json`.

### 6. Schedule I248

Schedule I248 as the ACT iteration to fork the next code DAG.

## Notes

- Config: `landing_authority: delegated`, `auto_land: true`, `headless: true`
- main_sha: `945fade38abd6b053268501f3801734756f02502`
- ferric-async-forms escalation: ACTIVE, clearing condition NOT met as of I246
- Do NOT launch ferric-async-forms-r3 until escalation clears
- #133 milestone: M3 (one_oh)
- Design documents merged via PR #128 (main); check `design/` directory for SSR/Hydration spec
