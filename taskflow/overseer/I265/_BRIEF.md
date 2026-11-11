# _BRIEF.md — NSWE overseer step I265 (persona swe-lead) — EVALUATE: review fold watch / board check

**Depends on**: I264
**Task Kind**: evaluate — load `appfiles/WORK_SESSION.md` and `appfiles/REVIEW_GATE.md`.

## Context from I264

- ferric-ssr-r3 (swe-coder, attempt 2 of 2) folded with **PASS**:
  - All 6 CI checks: SUCCESS (fmt, clippy, test, wasm, doc, image).
  - Commit `4994a08` on branch `work/ferric-ssr-r1`.
  - PR #228 (`feat(ferric): SSR render_to_string + client-side hydration + Axum integration`):
    - `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`.
- **review-ferric-ssr-r1** still RUNNING as of I264 (swe-reviewer):
  - Workspace: `taskflow/dags/review-ferric-ssr-r1/`
  - Synthesis seam: `taskflow/dags/review-ferric-ssr-r1/SYNTHESIS.md`
  - Scheduler: Dispatched 2026-11-05T01:02:33Z, Running since 01:03:34Z, not yet folded.
- ferric-async-forms escalation (PR #193): still **ACTIVE** — no user response as of I264.
- Main SHA at last board check: `945fade38abd6b053268501f3801734756f02502`
- STATE at: `taskflow/overseer/I264/project_state.json`
- ferric-ssr goal: issues #223, #224, #226 (branch `work/ferric-ssr-r1`), `In Review` on board.
- Remediation budget: 2 of 2 consumed. No further automatic code remediation DAGs unless review APPROVE.

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md` and `appfiles/REVIEW_GATE.md`.

### 2. Read the config seam

Read `taskflow/overseer/_CONFIG.yaml` (landing authority: delegated, auto_land: true, headless: true).

### 3. Check for the review fold

Check whether `taskflow/dags/review-ferric-ssr-r1/SYNTHESIS.md` exists (the review DAG's fold seam).

**If the review DAG has folded**:
- Read `taskflow/dags/review-ferric-ssr-r1/SYNTHESIS.md` for the verdict (APPROVE or REQUEST-CHANGES).
- Schedule the appropriate follow-on:
  - **APPROVE**: schedule I266 (process review: sort findings, confirm review is on PR #228, file
    non-blockers as backlog issues) followed by I267 (land: merge PR #228, move #223/#224/#226 to Done,
    update STATE, dispatch #35 goal after landing).
  - **REQUEST-CHANGES**: since the remediation budget (2 of 2) is exhausted, escalate to the user with the
    blockers rather than launching a 3rd automatic remediation — unless REVIEW_GATE.md specifies otherwise
    for a fresh-attempt budget per review. Schedule I266 (escalate) and record in STATE.
- Update board: record the review verdict in STATE.

**If the review DAG has NOT yet folded**:
- Also check: escalation on PR #193 (any user response?), any new GitHub activity, board hygiene.
- Schedule I266 as another bounded watch (forked-thread-completion OR now + 10 minutes).

### 4. Update STATE

Write updated project state at `taskflow/overseer/I265/project_state.json`.

### 5. Schedule what follows

If review folded: schedule the full follow-on series (I266 process, I267 land or escalate).
If review not yet folded: schedule I266 as another bounded watch.

## Notes

- Bounded wake: suspend on forked-thread-completion (review-ferric-ssr-r1) OR resume_at now + 10 minutes.
- If review is not yet folded on wake, re-evaluate and re-suspend with a fresh bounded wake.
- ferric-async-forms escalation (PR #193): do not close or touch it.
