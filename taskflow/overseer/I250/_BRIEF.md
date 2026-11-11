# _BRIEF.md — NSWE overseer step I250 (persona swe-lead) — EVALUATE: board check

**Depends on**: I249
**Task Kind**: evaluate — load `appfiles/WORK_SESSION.md`, `appfiles/BOARD.md`.

## Context from I249 (ACT: fork ferric-ssr-r1 code DAG)

- **ferric-ssr-r1 DAG forked**: covers BAR-003 (#223), BAR-004 (#224), BAR-006 (#226) on branch `work/ferric-ssr-r1`.
- Issues #223, #224, #226 assigned and moved to In Progress on the project board.
- `dags_in_flight`: 1 (ferric-ssr-r1)
- **Escalation**: `escalation_ferric_async_forms_budget_exhausted` STILL ACTIVE — no user response on PR #193.
- **#35 unblocked**: its only dependency (#56 durable persistence) is Done. Hold for dispatch until ferric-ssr-r1 lands (higher strategic priority first).
- **Config**: `landing_authority: delegated`, `auto_land: true`, `headless: true`
- **Repo**: `Nousix-LLC/nswe-demo`, `main` SHA: `945fade38abd6b053268501f3801734756f02502`
- **STATE**: `taskflow/overseer/I249/project_state.json`

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

### 2. Full board check

Check the board:
- Has the ferric-ssr-r1 DAG folded? (look for `taskflow/dags/ferric-ssr-r1/SYNTHESIS.md`)
- Has the ferric-async-forms escalation clearing condition been met? (user response on PR #193?)
- Any new issues, comments, or PRs filed since last check?
- Is #35 (Logged-out reading) now the next ready item in the backlog after ferric-ssr lands?
- Anything else changed on the board?

### 3. Decide and schedule what follows

Per `WORK_SESSION.md` board-check priority:
- If ferric-ssr-r1 folded: read the fold (schedule read-fold task for ferric-ssr-r1).
- If escalation clearing condition met: schedule resolution task.
- If new requests filed: schedule intake task.
- If nothing actionable: suspend on bounded wake (5–10 min floor, or DAG fold / board change, whichever first).

### 4. Write CONTINUE.md

## Notes

- Config: `landing_authority: delegated`, `auto_land: true`, `headless: true`
- main_sha: `945fade38abd6b053268501f3801734756f02502`
- ferric-async-forms escalation: ACTIVE, clearing condition NOT yet met
- #35 unblocked: dispatch after ferric-ssr-r1 lands
- After ferric-ssr-r1 lands: review gate → review DAG → landing → then #35
