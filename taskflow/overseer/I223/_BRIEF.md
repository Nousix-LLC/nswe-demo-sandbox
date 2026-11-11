# _BRIEF.md — NSWE overseer step I223 (persona swe-lead) — EVALUATE: board check / watch ferric-router-r3 fold

**Depends on**: I222
**Task Kind**: evaluate — load `WORK_SESSION` + `REVIEW_GATE`. Check board, watch for ferric-router-r3 fold.

## Context from I222 (ACT: launch ferric-router-r3, 2026-11-03)

- **ferric-router-r3 FORKED** — swe-coder DAG in flight.
  - Goal: fix clippy `unused import: VNode` in `crates/ferric-router` test code; produce branch
    `work/ferric-router-r3` and PR #203, all 6 CI checks PASS.
  - Builds on `work/ferric-router-r2` (3 cherry-pick commits: c03818f, 9c9fdd8, 3404dea).
  - Remediation attempt 2/2 (FINAL attempt). If CI cannot be made green, escalate to user.
- **ferric-async-forms escalation**: ACTIVE, no user response yet. Hold.
- **Free DAG slots**: 2 (ferric-router-r3 in flight).
- **Config**: delegated/auto_land/headless.
- **STATE**: `taskflow/overseer/I222/project_state.json`.
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`.

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/REVIEW_GATE.md`. Read `_CONFIG.yaml` and
`taskflow/overseer/I222/project_state.json`.

### 2. Check if ferric-router-r3 has folded
A DAG has folded when its root `SYNTHESIS.md` exists at `taskflow/dags/ferric-router-r3/SYNTHESIS.md`.

**If ferric-router-r3 HAS FOLDED**:
- Read the SYNTHESIS.md. Determine the machine gate result (CI all PASS = PASS; any FAIL = FAIL).
- If machine gate PASS: schedule review-ferric-router-r3 launch (I224: ACT: launch review).
- If machine gate FAIL (attempt 2/2 exhausted): escalate to user with both attempt details.
  - Post a comment on the relevant PR (PR #203 if opened, otherwise PR #202) describing the two failed
    attempts and what blocks.
  - Record the escalation in STATE. Do NOT launch another remediation DAG.
- Record ferric-router-r3 in dags_folded. Update free_dag_slots (2 → 3).

**If ferric-router-r3 has NOT folded**:
- Check for any other GitHub activity (new issues, comments, escalation responses).
- Schedule the next look (bounded wake: ferric-router-r3 fold OR 8-min timer, whichever first).

### 3. Update project STATE
Write `taskflow/overseer/I223/project_state.json` with updated board, dags_in_flight, dags_folded,
and forward_series entries.

### 4. Record forward_series entry for I223
Summarize in `forward_series.I223`.

## Notes

- Config: delegated/auto_land/headless.
- This is evaluation after ferric-router-r3 launch. Primary trigger: ferric-router-r3 fold.
- If ferric-router-r3 machine gate PASS: proceed to review (auto-review under delegated authority).
- If machine gate FAIL: escalate (attempt 2/2 exhausted, cannot auto-launch r4).
- The escalation for ferric-async-forms (#130) is still active; do not launch ferric-async-forms-r3 without
  user decision.
