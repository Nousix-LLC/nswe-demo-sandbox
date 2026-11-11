# _BRIEF.md — NSWE overseer step I364 (persona swe-lead) — ACT: watch chirp-logged-out-r15 (4th check / stall decision)

**Depends on**: I363

**Task Kind**: act — load `appfiles/WORK_SESSION.md`.

## Context from I363

r15 3rd stall check (3/4) at I363: head UNCHANGED at `21dca556`, no SYNTHESIS.md. stall_check_count_since_reset = 3.

- **r15 DAG**: `taskflow/dags/chirp-logged-out-r15/` (forked I360). Process id: chirp-logged-out-r15.
- **Branch HEAD** (at I363 check): `21dca556301a58c5ae286509a797a6c202225c71`
- **CI**: Run 42173990246, head `21dca556` — 6/6 ALL PASS (confirmed I349). No new CI check needed unless new commits.
- **ArgoCD**: OutOfSync/Healthy/cb1ced3 (benign StatefulSet drift — unchanged since I303).
- **PR #263**: OPEN/MERGEABLE (head `21dca556`).
- **Issue #35**: OPEN/In Progress.
- **stall_check_count_since_reset**: 3 (3/4 recorded at I363)

STATE at: `taskflow/overseer/I363/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing file

Load `appfiles/WORK_SESSION.md`.

### 2. Check chirp-logged-out-r15 DAG (4th check, 4/4 stall check / decision point)

Check if `taskflow/dags/chirp-logged-out-r15/SYNTHESIS.md` now exists (glob for it anywhere in the DAG tree).
Also check branch HEAD for any new commits since I363 (last known: `21dca556301a58c5ae286509a797a6c202225c71`).

**Check branch HEAD via GitHub PR (authoritative)**:
```
gh pr view 263 --repo Nousix-LLC/nswe-demo --json headRefOid
```

**If SYNTHESIS.md exists**: Read it, record verdict (PASS or FAIL), plan next step:
  - PASS + CI all green (6/6 confirmed): dispatch review DAG (swe-reviewer) for PR #263 immediately.
  - FAIL: dispatch chirp-logged-out-r16 (swe-coder) remediation carrying blockers from SYNTHESIS.md.

**If no SYNTHESIS.md at this check**:
  - **If head advanced (new commits since `21dca556`)**: Progress — note new head, reset stall concern (stall_check_count_since_reset = 0), schedule I365 for next check (+15 min).
  - **If head UNCHANGED (still `21dca556`) AND no SYNTHESIS.md**: **4th stall check (4/4) — STALL CONFIRMED**. Re-fork as chirp-logged-out-r16 (swe-coder). Post stall comment on issue #35. Record r15 as STALLED.

### 3. CI status check

CI run 42173990246 for `21dca556` is fully 6/6 ALL PASS (confirmed at I349). No new CI check needed unless new commits exist on the branch.

If new commits exist, check for new CI runs.

### 4. ArgoCD deployment re-check

Re-check ArgoCD sync status via SSH kubectl.
- Expect: OutOfSync/Healthy/cb1ced3 (benign StatefulSet drift).

### 5. Board spot-check

- Confirm #35 still In Progress.
- Confirm PR #263 still OPEN/MERGEABLE.

### 6. If stall confirmed (4/4): re-fork as chirp-logged-out-r16

If stall is confirmed (head UNCHANGED + no SYNTHESIS.md after 4 checks):

1. Post stall comment on issue #35 (citing this is the 4/4 check; r15 stalled; re-forking r16).
2. Write `taskflow/dags/chirp-logged-out-r16/_BRIEF.md` with the full goal spec:
   - **Goal**: Complete issue #35 — logged-out visitor experience: public timeline, public user profiles, accurate landing states.
   - **Context from prior runs**: r10 pushed backend APIs + frontend routes; r12 pushed AC-4 sign-up form at `21dca556` (CI 6/6 ALL PASS, run 42173990246). AC-4 sign-up form already on branch. r13–r15 all stalled on SYNTHESIS.md production.
   - **Branch**: `work/chirp-logged-out` (head `21dca556`). Do NOT force-push; build on existing state.
   - **AC-1–AC-5** from issue #35 must be verified/completed. AC-4 sign-up form already pushed.
   - **The DAG MUST produce SYNTHESIS.md as its final act** accounting for each AC (met, or not and why).
   - **PR #263** already exists: OPEN/MERGEABLE.
   - Repo: `Nousix-LLC/nswe-demo`. Branch: `work/chirp-logged-out`.
3. Write `taskflow/dags/chirp-logged-out-r16/_FORK.md` (launch_agent: swe-coder, disposition: reap-whole-after-land, launch_context: application: software).
4. Fork chirp-logged-out-r16 (`engine_fork`).
5. Record r15 as STALLED in STATE.

### 7. Update STATE

Write updated STATE at `taskflow/overseer/I364/project_state.json`.

### 8. Schedule next step

- If SYNTHESIS.md found and PASS + CI all green: schedule I365 to launch review DAG (swe-reviewer).
- If SYNTHESIS.md found and FAIL: schedule I365 for r16 remediation (swe-coder) carrying blockers.
- If head advanced (new commits) + no SYNTHESIS.md: note progress, reset stall concern, schedule I365 for next check (+15 min).
- If stall confirmed (4/4) → r16 re-forked: schedule I365 as board check / watch r16 start (+15 min).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD: same benign StatefulSet drift since I303. Main HEAD = cb1ced3.
- r15 dispatched I360 (`taskflow/dags/chirp-logged-out-r15/`). Process id: chirp-logged-out-r15.
- r15 brief: branch `work/chirp-logged-out`. Head `21dca556`, CI 6/6 ALL PASS. AC-4 sign-up form already pushed. Goal: verify AC-1–AC-5, complete gaps, produce SYNTHESIS.md. r13 and r14 both stalled without synthesizing — the DAG MUST produce SYNTHESIS.md as its final act.
- PR #263: OPEN/MERGEABLE on `work/chirp-logged-out`. Head: `21dca556`. CI run 42173990246: 6/6 ALL PASS.
- Stall rule for r15: 4 consecutive checks with head unchanged AND no SYNTHESIS.md → stall confirmed → re-fork as r16.
- stall_check_count_since_reset at I363 = 3. This check (I364) = 4/4 — DECISION POINT.
- Prior stall comments: https://github.com/Nousix-LLC/nswe-demo/issues/35#issuecomment-6677962335 and https://github.com/Nousix-LLC/nswe-demo/issues/35#issuecomment-6678431704 and https://github.com/Nousix-LLC/nswe-demo/issues/35#issuecomment-6678885251 and https://github.com/Nousix-LLC/nswe-demo/issues/35#issuecomment-6679073843 and https://github.com/Nousix-LLC/nswe-demo/issues/35#issuecomment-6679273047.
