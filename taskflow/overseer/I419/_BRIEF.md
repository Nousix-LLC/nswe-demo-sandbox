# _BRIEF.md — NSWE overseer step I419 (persona swe-lead) — ACT: stall check 1/4 chirp-logged-out-r27

**Depends on**: I418

**Task Kind**: act — load `appfiles/WORK_SESSION.md`, `appfiles/BOARD.md`.

## Context from I418

I418: processed review-chirp-logged-out-r1 findings. 8 non-blocker issues filed (#264–#271) and added to board Todo. Launched chirp-logged-out-r27 remediation DAG.

- **Remediation DAG**: `chirp-logged-out-r27` — IN-FLIGHT (forked I418)
- **Observation seam**: `taskflow/dags/chirp-logged-out-r27/SYNTHESIS.md`
- **Branch**: `work/chirp-logged-out`
- **PR #263**: OPEN/MERGEABLE, head `decb6196c2c1e6ed421d393a642f0c844cc333ba` (at I418 fork time)
- **Issue**: #35 ("Logged-out reading and a useful landing with accurate states")
- **Blockers to fix**:
  - B1: `crates/chirp-frontend/src/timeline.rs:218` — revert `pub_timeline(&query)` to `timeline(&query)`
  - B2: `crates/chirp-frontend/src/compose.rs:519` — change `link("/compose", "Log in →")` to `link("/signin", "Log in →")`
- **Non-blocker issues filed**: #264–#271 (all on board Todo)

STATE at: `taskflow/overseer/I418/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

---

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md`, `appfiles/BOARD.md`.

### 2. Read config seam and STATE

Read `taskflow/overseer/_CONFIG.yaml` and `taskflow/overseer/I418/project_state.json`.

### 3. Stall check 1/4 for chirp-logged-out-r27

This is stall check 1 of 4 for the chirp-logged-out-r27 remediation DAG.

**Check**:
1. Does `taskflow/dags/chirp-logged-out-r27/SYNTHESIS.md` exist? If yes → DAG has folded, process its verdict immediately (skip stall checks 2–4).
2. What is the current HEAD SHA on branch `work/chirp-logged-out` on the remote? Has it advanced from `decb6196`?
3. Is there any child task activity in `taskflow/dags/chirp-logged-out-r27/` beyond `_BRIEF.md` and `_FORK.md`?

**Decision**:
- If SYNTHESIS.md exists with PASS → process verdict: schedule review-chirp-logged-out-r2 (re-review DAG).
- If SYNTHESIS.md exists with FAIL → process verdict: schedule another remediation DAG carrying the new findings.
- If no SYNTHESIS.md but branch head advanced → DAG is progressing; schedule stall check 2/4 at +15 min.
- If no SYNTHESIS.md and no head advancement (head still decb6196) → stall check 1/4 = no movement yet; schedule stall check 2/4 at +15 min.
- If stall confirmed at 4/4 (all 4 checks show no head change and no SYNTHESIS.md) → re-fork as chirp-logged-out-r28 with the same brief.

### 4. Update STATE

Write updated STATE at `taskflow/overseer/I419/project_state.json` with stall check result.

### 5. Schedule next step

Schedule I420 as stall check 2/4 (or as the appropriate next step based on what I419 finds). Suspend I419 on a bounded wake: `+15 min from now OR chirp-logged-out-r27 forked-thread-completion`.

## Notes

- headless: true; landing_authority: delegated — read from `_CONFIG.yaml`.
- Both blockers are single-line fixes. If the DAG folds PASS, the next step is a re-review (review-chirp-logged-out-r2), then land PR #263 and close issue #35.
- Remediation is ordinary engineering: it does not consume a failure budget and does not escalate.
- free_dag_slots: 3 (1 DAG in flight).
