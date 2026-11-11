# _BRIEF.md — NSWE overseer step I407 (persona swe-lead) — ACT: launch chirp-logged-out-r25

**Depends on**: I406

**Task Kind**: act — load `appfiles/WORK_SESSION.md` and `appfiles/DELIVERABLES_GIT.md`.

## Context from I406

I406: board check / stall check 4/4 for r24. **4/4 stall confirmed.** Branch `work/chirp-logged-out` HEAD
UNCHANGED at `decb6196c2c1e6ed421d393a642f0c844cc333ba`. No SYNTHESIS.md in
`taskflow/dags/chirp-logged-out-r24/` (only `_BRIEF.md` and `_FORK.md`). stall_check_count for r24 = 4/4.
Stall comment posted on issue #35:
https://github.com/Nousix-LLC/nswe-demo/issues/35#issuecomment-6681974435

**Key facts from I406**:
- **r24 DAG**: STALLED (4/4 confirmed I406, dispatched I402). No SYNTHESIS.md. Only `_BRIEF.md` and
  `_FORK.md` in `taskflow/dags/chirp-logged-out-r24/`.
- **PR #263**: OPEN/MERGEABLE (head `decb6196`). CI run 42194072348: ALL 6 PASS. CI-green and ready for
  review once SYNTHESIS.md appears.
- **Issue #35**: OPEN/In Progress/assigned (mattsmcknight).
- **ArgoCD**: OutOfSync/Healthy/cb1ced3 — benign StatefulSet drift (unchanged since I303).
- **Free DAG slots**: 3 (only need 1 for r25).
- **Stall history**: r1–r24 all stalled. r13–r17 at `21dca556`; r18–r22 at `617f2539`; r23 advanced to
  `decb6196` (I399) then stalled (4/4, I402); r24 dispatched I402, stalled at `decb6196` (4/4, I406).

STATE at: `taskflow/overseer/I406/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md` and `appfiles/DELIVERABLES_GIT.md`.

### 2. Read config seam

Read `taskflow/overseer/_CONFIG.yaml`. Confirm:
- `landing_authority: delegated`, `auto_land: true`, `headless: true`.
- Repo: `Nousix-LLC/nswe-demo`.

### 3. Check DAG slot availability

Confirm free DAG slots (STATE says 3). One slot is enough for r25.

### 4. Write r25 _BRIEF.md and fork chirp-logged-out-r25

Write `taskflow/dags/chirp-logged-out-r25/_BRIEF.md` with the full context below, then fork it as
`swe-coder`.

#### r25 brief content

The DAG brief must carry:

**Objective**: Complete issue #35 — "Logged-out reading and a useful landing with accurate states" — on
branch `work/chirp-logged-out`. PR #263 is OPEN and CI-green (ALL 6 PASS on `decb6196`).

**FIRST PRIORITY**: Assess the current state of `work/chirp-logged-out` at `decb6196c2c1e6ed421d393a642f0c844cc333ba`
against all 5 acceptance criteria below. If they are all met, write `SYNTHESIS.md` IMMEDIATELY — do not
proceed to any code changes before writing it.

This is the defining pattern across r1–r24: code work was done (the head advanced r18, r23), but
SYNTHESIS.md was never written. CI is ALL 6 PASS. If the ACs are met, write SYNTHESIS.md and stop.

**Acceptance criteria** (from issue #35):
1. A logged-out visitor can load the home/public timeline and open a user profile and read chirps
   without being forced to sign up or sign in first. (`REQ-PROD-013`, `BAR-011`)
2. On arrival with no content, the visitor sees a clear statement of what chirp is plus an obvious way
   to sign up or sign in — never a blank page or an unexplained error. (`REQ-PROD-014`, `BAR-011`)
3. If the timeline fails to load, a clear, recoverable message is shown instead of a broken screen.
   (`REQ-PROD-014`, `BAR-011`)
4. A "create an account" route is visible on the landing and on the sign-in screen, and following it
   reaches sign-up. (`REQ-PROD-015`, `BAR-011`)
5. The logged-out landing/timeline exercises its loading, empty, error, and end-of-list states
   accurately and distinctly. (`REQ-UX-002/030/031/032`, `BAR-011`, and the one-state-model criterion)

**Inputs**:
- Repository: `Nousix-LLC/nswe-demo`
- Branch: `work/chirp-logged-out` at `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- PR: #263 (OPEN, MERGEABLE, CI-green — all 6 checks PASS: fmt, clippy, test, wasm, doc, image)
- Design references (in repo):
  - `design/product-requirements.md` — §3 User journeys; §4 `REQ-PROD-013`, `REQ-PROD-014`, `REQ-PROD-015`
  - `design/experience-design.md` — §1 Information architecture & interaction; §2 Screens, flows & states;
    §6 `REQ-UX-002`, `REQ-UX-030`, `REQ-UX-031`, `REQ-UX-032`
  - `design/release-bar.md` — §C `BAR-011`
- Epic: EPIC-CORELOOP (#34) — Core product loop & accurate UX states
- Dependencies: Durable persistence (#56) DONE. ferric-ssr (#223/#224/#226) DONE. ferric-async-forms
  (#130/#143/#144/#145) DONE.

**Stall history** (r1–r24, all produced `_BRIEF.md` and `_FORK.md` only, never `SYNTHESIS.md`):
- r1–r12: stalled at various heads
- r13–r17: stalled at `21dca556` (4/4 each)
- r18: advanced from `21dca556` to `617f2539`, then stalled (4/4)
- r19–r22: stalled at `617f2539` (4/4 each)
- r23: advanced from `617f2539` to `decb6196`, then stalled (4/4, confirmed I402)
- r24: dispatched I402, stalled at `decb6196` (4/4, confirmed I406)

**Declared output**:
- Root `taskflow/dags/chirp-logged-out-r25/SYNTHESIS.md` with verdict (PASS or FAIL) and accounting for
  each of the 5 acceptance criteria
- If code changes are needed: commits on `work/chirp-logged-out` and PR #263 updated (no force-push)
- If ACs are already met: SYNTHESIS.md with PASS verdict, no code changes needed

**Constraints**:
- Branch: `work/chirp-logged-out` only
- No force-push
- Repo scope: `Nousix-LLC/nswe-demo`
- PR #263 is the target PR — do not open a new PR
- CI is ALL 6 PASS on `decb6196` — confirm the ACs in the existing code first

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I407/project_state.json` recording:
- r24 moved to dags_stalled (stall confirmed I406, comment posted)
- r25 dispatched
- chirp_logged_out_goal.current_dag updated to r25
- free_dag_slots = 3 (r25 launched, leaves 3)

### 6. Schedule next step

Schedule I408 as board check / stall check 1/4 for r25, suspended until r25 forked-thread-completion OR
+15 min from fork, whichever fires first.

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD: same benign StatefulSet drift since I303. Main HEAD = cb1ced3.
- r25 DAG path: `taskflow/dags/chirp-logged-out-r25/`.
- PR #263: OPEN/MERGEABLE on `work/chirp-logged-out`. Head: `decb6196c2c1e6ed421d393a642f0c844cc333ba`.
  CI run 42194072348: ALL 6 PASS — PR is CI-green and ready for review once SYNTHESIS.md appears.
- Issues #254–#262 on board as Todo.
- Once SYNTHESIS.md appears with PASS: dispatch review DAG for PR #263 as swe-reviewer.
