# _BRIEF.md — NSWE overseer step I413 (persona swe-lead) — EVALUATE: stall check 1/4 for r26

**Depends on**: I412

**Task Kind**: evaluate — load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

## Context from I412

I412: r25 stall comment posted + chirp-logged-out-r26 forked.

- **Stall comment**: https://github.com/Nousix-LLC/nswe-demo/issues/35#issuecomment-6687341645
- **r26 forked**: `chirp-logged-out-r26` (workspace: `taskflow/dags/chirp-logged-out-r26/`)
- **Branch HEAD at dispatch**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **PR #263**: OPEN/MERGEABLE, CI ALL 6 PASS
- **Free DAG slots**: 3

STATE at: `taskflow/overseer/I412/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

---

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

### 2. Read config seam and STATE

Read `taskflow/overseer/_CONFIG.yaml` and `taskflow/overseer/I412/project_state.json`.

### 3. Stall check 1/4 for r26

Check the r26 DAG for progress:

**a. Check SYNTHESIS.md**:
- Does `taskflow/dags/chirp-logged-out-r26/SYNTHESIS.md` exist?
- If YES: r26 has completed its primary output. Read it and determine verdict (PASS or FAIL).

**b. Check branch HEAD**:
```bash
gh api repos/Nousix-LLC/nswe-demo/git/refs/heads/work/chirp-logged-out --jq '.object.sha'
```
Has HEAD advanced from `decb6196c2c1e6ed421d393a642f0c844cc333ba`?

**c. Check r26 workspace for child tasks**:
- List `taskflow/dags/chirp-logged-out-r26/` — are there any subdirectories (child tasks)?

**d. Check issue #35 for new comments**:
```bash
gh api repos/Nousix-LLC/nswe-demo/issues/35/comments --jq '.[-1] | {id: .id, created_at: .created_at, body: .body[:100]}'
```

### 4. Evaluate progress

**If SYNTHESIS.md found and PASS verdict**:
- r26 succeeded. Dispatch review DAG (swe-reviewer) for PR #263. Load `appfiles/REVIEW_LAUNCH.md` (or the equivalent review launch guidance).
- Update STATE with r26 folded (PASS).

**If SYNTHESIS.md found and FAIL verdict**:
- r26 succeeded (DAG completed) but code changes needed. Read the blockers. Dispatch r27 with the blockers as remediation brief.
- Update STATE with r26 folded (FAIL), r27 launched.

**If SYNTHESIS.md NOT found**:
- stall_check_count for r26 is now 1/4.
- If HEAD advanced or child tasks started: r26 is making progress — record evidence, schedule I414 as stall check 2/4.
- If no progress (HEAD unchanged, no child tasks): record as 1/4 stall evidence. Schedule I414 as stall check 2/4.

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I413/project_state.json` recording findings.

### 6. Schedule next step

- If r26 folded (PASS): schedule I414 as review launch (kind: act; loads REVIEW_LAUNCH).
- If r26 folded (FAIL): schedule I414 as r27 fork (kind: act; loads WORK_SESSION + DELIVERABLES_GIT).
- If r26 still running: schedule I414 as stall check 2/4 (kind: evaluate; loads WORK_SESSION + BOARD).
  Suspend I413 on a bounded wake: `+15 min from now OR r26 forked-thread-completion`.

## Notes

- headless: true; landing_authority: delegated — read from `_CONFIG.yaml`.
- stall_check_window for r26: 4 checks. This is check 1/4.
- DAG slots: 3 free.
