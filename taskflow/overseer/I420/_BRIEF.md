# _BRIEF.md — NSWE overseer step I420 (persona swe-lead) — ACT: launch review-chirp-logged-out-r2

**Depends on**: I419

**Task Kind**: act — load `appfiles/REVIEW_GATE.md`, `appfiles/WORK_SESSION.md`.

## Context from I419

I419: stall check 1/4 for chirp-logged-out-r27 — DAG FOLDED PASS. Both blockers from review-chirp-logged-out-r1 fixed. All 5 ACs met. CI 6/6 green on new HEAD `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`.

- **chirp-logged-out-r27**: FOLDED PASS — `taskflow/dags/chirp-logged-out-r27/SYNTHESIS.md`
  - B1 ✅ FIXED: `crates/chirp-frontend/src/timeline.rs:218` — reverted `pub_timeline(&query)` to `timeline(&query)`
  - B2 ✅ FIXED: `crates/chirp-frontend/src/compose.rs:519` — `link("/compose", "Log in →")` → `link("/signin", "Log in →")`
  - All 5 ACs confirmed. CI run 42249419769, 6/6 green.
- **PR #263**: OPEN/MERGEABLE on `work/chirp-logged-out`, HEAD `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`
- **Issue**: #35 ("Logged-out reading and a useful landing with accurate states")
- **Previous review**: review-chirp-logged-out-r1 — REQUEST-CHANGES (confirmed I417). 8 non-blockers filed as issues #264–#271.

STATE at: `taskflow/overseer/I419/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

---

## Work for this step

### 1. Load governing files

Load `appfiles/REVIEW_GATE.md`, `appfiles/WORK_SESSION.md`.

### 2. Read config seam and STATE

Read `taskflow/overseer/_CONFIG.yaml` and `taskflow/overseer/I419/project_state.json`.

### 3. Verify PR state

Check PR #263 current state:
- Confirm HEAD is `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4` (advanced from `decb6196`)
- Confirm PR is OPEN/MERGEABLE
- Note CI status on new HEAD

### 4. Write review brief and fork review-chirp-logged-out-r2

Write `taskflow/dags/review-chirp-logged-out-r2/_BRIEF.md` for the re-review DAG and fork it as `swe-reviewer`.

The brief must cover:
- **Target**: PR #263 (`Nousix-LLC/nswe-demo`, branch `work/chirp-logged-out`, HEAD `7f4b684`), issue #35, all 5 ACs, previous review REQUEST-CHANGES with both blockers now purportedly fixed
- **Code DAG synthesis**: `taskflow/dags/chirp-logged-out-r27/SYNTHESIS.md` as the machine-gate record
- **Previous review**: `taskflow/dags/review-chirp-logged-out-r1/SYNTHESIS.md` — REQUEST-CHANGES, 2 blockers (B1 timeline.rs:218, B2 compose.rs:519), 8 non-blockers filed as issues #264–#271
- **Review concerns** (fresh selection for this diff):
  - *Correctness of the two blocker fixes*: Does B1 fix route authenticated users to the personalized `/api/timeline` feed (not global pub feed)? Does B2 fix the sign-up "Log in →" CTA to route to `/signin`? Are the fixes correct and complete?
  - *Correctness of all 5 ACs*: Confirm each AC still holds on the new HEAD (the two fixes are targeted changes; confirm they do not break logged-out public access, empty state, error state, navigation)
  - *Code quality*: Are the two changes minimal and clean? No unintended side effects?
  - *Test coverage*: Are the fixes adequately tested? Do any tests explicitly cover the fixed behavior?
  - *Security*: No new surface introduced by either single-line change
  - *Regression check*: Does the new commit introduce any other changes beyond the two targeted fixes?
- **Declared output**: Posted review (or comment) on PR #263, root `SYNTHESIS.md` with APPROVE or REQUEST-CHANGES verdict, any new non-blocking findings filed as backlog issues linked to PR #263

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I420/project_state.json` recording review-chirp-logged-out-r2 IN-FLIGHT.

### 6. Schedule next step

Schedule I421 as stall check 1/4 for review-chirp-logged-out-r2. Suspend on: `+15 min from now OR review-chirp-logged-out-r2 forked-thread-completion`.

## Notes

- headless: true; landing_authority: delegated — read from `_CONFIG.yaml`
- The review concerns are fresh for this diff; do not reuse review-chirp-logged-out-r1's selection wholesale
- After APPROVE: land PR #263 (`gh pr merge 263 --squash --delete-branch -R Nousix-LLC/nswe-demo`), close issue #35, deployment check
- free_dag_slots: 4 (chirp-logged-out-r27 folded, no other DAGs in flight)
