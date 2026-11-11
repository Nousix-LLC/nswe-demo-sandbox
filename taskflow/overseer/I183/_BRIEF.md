# _BRIEF.md — NSWE overseer step I183 (persona swe-lead) — EVALUATE: read fold for review-update-sweep-digest-r1

**Depends on**: I182
**Task Kind**: evaluate — load `WORK_SESSION` + `REVIEW_GATE`; check if `review-update-sweep-digest-r1` has folded; read verdict; schedule I184 (land if APPROVE) or I184-remediation (if REQUEST-CHANGES).

## Context from I182

- **Review DAG launched**: `review-update-sweep-digest-r1` (swe-reviewer, `taskflow/dags/review-update-sweep-digest-r1`).
- **PR under review**: #187 — `deploy(chirp): pin sweep CronJob to febeb151 image`. Machine gate PASS. MERGEABLE.
- **Config seam**: `landing_authority: delegated`, `auto_land: true`, `headless: true`.
- **STATE**: `taskflow/overseer/I164-S1/project_state.json`.

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/REVIEW_GATE.md`.

### 2. Read config seam
Read `taskflow/overseer/_CONFIG.yaml`.

### 3. Check review fold
Check `taskflow/dags/review-update-sweep-digest-r1/SYNTHESIS.md` (or `COMPLETE.md` for an atomic review DAG).

**If folded:**
- Read the verdict (APPROVE or REQUEST-CHANGES).
- If **APPROVE**: machine PASS + review APPROVE → schedule I184 (land PR #187, delegated authority).
- If **REQUEST-CHANGES**: record blockers; schedule I184 as "remediation" or escalation if within budget.

**If not folded:**
- Note the DAG is still running. Self-suspend until fold or 15 minutes; re-check on wake.

### 4. Update STATE
- Move `review-update-sweep-digest-r1` from `dags_in_flight` to `dags_folded` with verdict (if folded).
- Record review findings. Non-blockers become backlog issues via a later board task.
- `current_pointer`: overseer/I184.
- Update `forward_series` for I183.

### 5. Schedule I184
Schedule I184 (`depends_on` I183):
- If APPROVE: "act — land PR #187; update board; update STATE" (loads `DELIVERABLES_GIT`, `RETENTION`).
- If not yet folded: "evaluate — re-check review fold" (re-evaluate).
