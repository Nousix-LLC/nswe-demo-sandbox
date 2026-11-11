# _BRIEF.md — NSWE overseer step I417 (persona swe-lead) — EVALUATE: stall check 3/4 for review-chirp-logged-out-r1

**Depends on**: I416

**Task Kind**: evaluate — load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

## Context from I416

I416: stall check 2/4 performed. review-chirp-logged-out-r1 was IN-FLIGHT as of I416 (checked ~15:05Z).

- **Review DAG**: `review-chirp-logged-out-r1` — RUNNING, active progress
- **Review DAG workspace**: `taskflow/dags/review-chirp-logged-out-r1/`
- **PR #263**: OPEN/MERGEABLE, head `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Branch**: `work/chirp-logged-out`
- **Issue**: #35 ("Logged-out reading and a useful landing with accurate states")
- **Stall check 2/4 observation**: DAG in-flight with significant progress:
  - `spoke-access-auth`: COMPLETE — **1 BLOCKER found**: `timeline.rs:218` calls `ctx.client().pub_timeline(&query)` instead of `ctx.client().timeline(&query)` — authenticated users on `/timeline` see global public feed instead of personalized home feed. Fix: restore `ctx.client().timeline(&query)`.
  - `spoke-state-machine`: COMPLETE — PASS. AC-5 states correct and distinct. 5 non-blocking findings (F-1 through F-5).
  - `spoke-ui-states`: SUSPENDED/NeedsDecompose — running subtasks (landing-states, routing-ctas, synthesis)
  - `spoke-code-quality`: SUSPENDED/NeedsDecompose — running subtasks (tests, correctness, code-health, safety-idiom, prose, synthesis)
  - No SYNTHESIS.md at root, no PR review posted.
- **Free DAG slots**: 3

STATE at: `taskflow/overseer/I416/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

---

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

### 2. Read config seam and STATE

Read `taskflow/overseer/_CONFIG.yaml` and `taskflow/overseer/I416/project_state.json`.

### 3. Check review-chirp-logged-out-r1 progress

Check the review DAG's progress:
- Look for `taskflow/dags/review-chirp-logged-out-r1/SYNTHESIS.md` (terminal: folded)
- Check spoke subtask completions (spoke-ui-states subtasks, spoke-code-quality subtasks)
- Check PR #263 for a posted review (`gh pr view 263 --repo Nousix-LLC/nswe-demo`)

### 4. Decide

- **SYNTHESIS.md found with verdict**: DAG has folded. Read it. Evaluate the verdict (APPROVE → land path; REQUEST-CHANGES → remediation path, noting 1 known BLOCKER from spoke-access-auth). Schedule the appropriate next step.
- **No SYNTHESIS.md**: DAG still in-flight. Record stall check 3/4 observation. Schedule stall check 4/4 (I418).

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I417/project_state.json`.

### 6. Schedule next step

- If folded APPROVE: schedule I418 as a process-review / landing step (loads `REVIEW_GATE` + `DELIVERABLES_GIT`).
- If folded REQUEST-CHANGES: schedule I418 as a process-review / remediation-launch step (loads `REVIEW_GATE` + `BOARD`).
- If still in-flight: schedule I418 as stall check 4/4. Suspend I417 on a bounded wake: `+15 min from now OR review-chirp-logged-out-r1 forked-thread-completion`.

## Notes

- headless: true; landing_authority: delegated — read from `_CONFIG.yaml`.
- DAG slots: 3 free.
- This is stall check 3/4. If the DAG has not folded by check 4/4, classify as stalled and re-fork.
- Known partial finding: 1 BLOCKER from spoke-access-auth (pub_timeline vs timeline in timeline.rs:218). Full verdict requires SYNTHESIS.md.
- If folded REQUEST-CHANGES: the known blocker is fixable (1-line change in timeline.rs). Remediation DAG = chirp-logged-out-r27 on branch work/chirp-logged-out.
