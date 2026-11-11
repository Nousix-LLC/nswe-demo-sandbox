# _BRIEF.md — NSWE overseer step I380 (persona swe-lead) — ACT: dispatch chirp-logged-out-r19

**Depends on**: I379

**Task Kind**: act — load `appfiles/WORK_SESSION.md` and `appfiles/DELIVERABLES_GIT.md`.

## Context from I379

I379: r18 stall confirmed 4/4 against head `617f2539` — STALL CONFIRMED. No SYNTHESIS.md. Head UNCHANGED.
- Stall comment posted: https://github.com/Nousix-LLC/nswe-demo/issues/35#issuecomment-6680286236
- **CI 42183715802**: completed/success (all green) on head `617f2539`.
- **PR #263**: OPEN/MERGEABLE/CLEAN (head `617f2539`).
- **Issue #35**: OPEN/In Progress.
- **ArgoCD**: OutOfSync/Healthy/cb1ced3 (benign StatefulSet drift — unchanged since I303).

- **r18 DAG**: `taskflow/dags/chirp-logged-out-r18/` (dispatched I372). STALLED.
- **Branch HEAD**: `617f25395eebe9475f19a90e0b1dac5921215ea3`
- **stall_check_count_since_reset**: 4 (4/4 — stall confirmed)

STATE at: `taskflow/overseer/I379/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md` and `appfiles/DELIVERABLES_GIT.md`.

### 2. Check DAG slots

Confirm dags_in_flight count. r18 is confirmed STALLED, so it no longer counts as in-flight. 0 DAGs currently in flight after r18 stall. Slot is free for r19.

### 3. Fork chirp-logged-out-r19

Write `taskflow/dags/chirp-logged-out-r19/_FORK.md` and `taskflow/dags/chirp-logged-out-r19/_BRIEF.md` and fork as `swe-coder`.

**r19 brief objective**: Continue from the r18 branch state to complete issue #35 — Logged-out reading and a useful landing with accurate states. The branch `work/chirp-logged-out` is at head `617f25395eebe9475f19a90e0b1dac5921215ea3` (CI all green, PR #263 OPEN/MERGEABLE/CLEAN). r10–r18 made substantial progress: backend APIs, public timeline endpoint, user profile endpoint, frontend routes, sign-up form, and auth-gating work are all present in the existing code. The goal for r19 is to: (a) verify the full AC-1–AC-5 checklist against the live code, (b) address any gaps or regressions, and (c) produce `SYNTHESIS.md` at the DAG root reporting whether each acceptance criterion is met.

**Acceptance criteria to verify** (from issue #35):
- AC-1: A logged-out visitor can load the home/public timeline and open a user profile and read chirps without being forced to sign up or sign in first. (`REQ-PROD-013`, `BAR-011`)
- AC-2: On arrival with no content, the visitor sees a clear statement of what chirp is plus an obvious way to sign up or sign in — never a blank page or an unexplained error. (`REQ-PROD-014`, `BAR-011`)
- AC-3: If the timeline fails to load, a clear, recoverable message is shown instead of a broken screen. (`REQ-PROD-014`, `BAR-011`)
- AC-4: A "create an account" route is visible on the landing and on the sign-in screen, and following it reaches sign-up. (`REQ-PROD-015`, `BAR-011`)
- AC-5: The logged-out landing/timeline exercises its loading, empty, error, and end-of-list states accurately and distinctly. (`REQ-UX-002/030/031/032`, `BAR-011`, and the one-state-model criterion)

**Branch**: `work/chirp-logged-out` (existing PR #263). No new PR needed — push to the same branch; PR #263 remains open.
**Output**: commits on `work/chirp-logged-out`, root `SYNTHESIS.md` at `taskflow/dags/chirp-logged-out-r19/SYNTHESIS.md` accounting for each AC (met, or not and why).

**Prior stall history**: r10–r18 all stalled; stall comments on issue #35. r12 pushed to 21dca556, r18 advanced to 617f2539. The pattern of stalling without synthesizing suggests the DAG may be missing the final synthesis step — r19 must explicitly produce `SYNTHESIS.md` as its declared output.

**Prior DAG**: `taskflow/dags/chirp-logged-out-r18/` (process id: chirp-logged-out-r18).

### 4. Assign issue #35

Assign issue #35 to the authenticated `gh` user to mark it in-flight:
```
gh issue edit 35 --repo Nousix-LLC/nswe-demo --add-assignee @me
```

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I380/project_state.json`:
- Move `chirp-logged-out-r18` from `dags_in_flight` to `dags_stalled` (confirmed I379).
- Add `chirp-logged-out-r19` to `dags_in_flight` with dispatched_in = overseer/I380.
- Note stall comment URL in r18 stalled entry.
- Update PR #263 note.

### 6. Schedule next step

Schedule I381 as a watch step (+15 min from now):
- Load `appfiles/WORK_SESSION.md`.
- Check if `taskflow/dags/chirp-logged-out-r19/SYNTHESIS.md` exists (stall check 1/4 against new r19 branch state).
- Record new branch HEAD.
- If SYNTHESIS.md exists: read and act on verdict.
- If no SYNTHESIS.md and head advanced: stall check 1/4 against new head, schedule I382 (+15 min).
- If no SYNTHESIS.md and head UNCHANGED: stall check 1/4, schedule I382 (+15 min).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD: same benign StatefulSet drift since I303. Main HEAD = cb1ced3.
- r19 DAG path: `taskflow/dags/chirp-logged-out-r19/`. Process id: chirp-logged-out-r19.
- r18 stall confirmed I379. Prior stalls: r1–r18 all stalled. r18 comment: https://github.com/Nousix-LLC/nswe-demo/issues/35#issuecomment-6680286236
- PR #263: OPEN/MERGEABLE/CLEAN on `work/chirp-logged-out`. Head: `617f2539`. CI run 42183715802: completed/success.
