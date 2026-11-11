# _BRIEF.md — NSWE overseer step I408 (persona swe-lead) — EVALUATE: board check / stall check 1/4 for r25

**Depends on**: I407

**Task Kind**: evaluate — load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

## Context from I407

I407: fork chirp-logged-out-r25 as swe-coder. r25 dispatched. Brief at
`taskflow/dags/chirp-logged-out-r25/_BRIEF.md`.

**Key facts from I407**:
- **r25 DAG**: forked as swe-coder in I407. Path: `taskflow/dags/chirp-logged-out-r25/`.
  First priority: assess `decb6196` against all 5 ACs and write SYNTHESIS.md. If ACs met → PASS verdict,
  no code changes. If not → code changes then SYNTHESIS.md.
- **r24**: STALLED (4/4, I406). Stall comment posted:
  https://github.com/Nousix-LLC/nswe-demo/issues/35#issuecomment-6681974435
- **PR #263**: OPEN/MERGEABLE on `work/chirp-logged-out`. Head `decb6196`. CI ALL 6 PASS (run 42194072348).
- **Issue #35**: OPEN/In Progress/assigned (mattsmcknight).
- **ArgoCD**: OutOfSync/Healthy/cb1ced3 — benign StatefulSet drift (unchanged since I303).
- **Free DAG slots**: 3 (r25 launched).

STATE at: `taskflow/overseer/I407/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

### 2. Read config seam and STATE

Read `taskflow/overseer/_CONFIG.yaml` and `taskflow/overseer/I407/project_state.json`.

### 3. Stall check 1/4 for r25

Check whether `taskflow/dags/chirp-logged-out-r25/SYNTHESIS.md` exists (fold complete).

Also check the current HEAD of branch `work/chirp-logged-out`:
```
gh api repos/Nousix-LLC/nswe-demo/branches/work%2Fchirp-logged-out --jq '.commit.sha'
```

Compare to known HEAD `decb6196c2c1e6ed421d393a642f0c844cc333ba`:
- If SYNTHESIS.md exists → DAG folded. Read it and schedule the appropriate next step (review if PASS,
  remediation DAG if FAIL).
- If HEAD advanced (new commits beyond `decb6196`) → DAG progressing. Schedule stall check 2/4.
- If HEAD unchanged and no SYNTHESIS.md → stall in progress. stall_check_count = 1/4. Schedule I409 as
  stall check 2/4 with another bounded wake.

### 4. Check board / GitHub state

- Any new comments on issue #35 or PR #263 since I406?
- Any new issues filed?
- Any other PRs opened or merged?
- ArgoCD status still benign (OutOfSync/Healthy/cb1ced3)?

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I408/project_state.json` recording:
- stall_check_count for r25 (1/4 or fold confirmed)
- any GitHub activity found

### 6. Schedule next step

- If r25 folded: schedule appropriate fold-read task (I409 as "read r25 fold").
- If progressing (head advanced): schedule I409 as stall check 2/4 (suspended +15 min from now or r25
  completion).
- If still no progress: schedule I409 as stall check 2/4 (suspended +15 min from now or r25 completion).

## Notes

- stall_check_window for r25: 4 checks. This is 1/4.
- Wake condition: r25 forked-thread-completion OR +15 min from I407 fork, whichever fires first.
- Stall threshold: 4/4 unchanged HEAD + no SYNTHESIS.md = stall confirmed → re-fork as r26.
