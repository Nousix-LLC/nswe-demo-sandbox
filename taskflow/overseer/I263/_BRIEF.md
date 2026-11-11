# _BRIEF.md — NSWE overseer step I263 (persona swe-lead) — ACT: launch swe-reviewer for PR #228

**Depends on**: I262
**Task Kind**: act — load `appfiles/REVIEW_GATE.md` and `appfiles/WORK_SESSION.md`.

## Context from I262

- ferric-ssr-r3 (swe-coder, attempt 2 of 2) folded with **PASS**:
  - All 3 CI failures (fmt, clippy, doc) on PR #228 are resolved.
  - Commit `4994a08` on branch `work/ferric-ssr-r1`.
  - PR #228 (`feat(ferric): SSR render_to_string + client-side hydration + Axum integration`):
    - All 6 CI checks: SUCCESS (fmt, clippy, test, wasm, doc, image).
    - `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN`.
    - No reviews posted yet.
- ferric-async-forms escalation (PR #193): still **ACTIVE** — no user response as of this board check.
- Main SHA at last board check: `945fade38abd6b053268501f3801734756f02502`
- STATE at: `taskflow/overseer/I256/project_state.json`
- ferric-ssr goal: issues #223, #224, #226 (branch `work/ferric-ssr-r1`).

## Work for this step

### 1. Load governing files

Load `appfiles/REVIEW_GATE.md` and `appfiles/WORK_SESSION.md`.

### 2. Read the config seam

Read `taskflow/overseer/_CONFIG.yaml` (landing authority: delegated, auto_land: true, headless: true).

### 3. Launch a swe-reviewer review DAG for PR #228

The machine gate passed. Write a review brief and fork `swe-reviewer` as the review DAG.

The review DAG's goal: review PR #228 on branch `work/ferric-ssr-r1` against the ferric SSR/hydration design
(issues #223, #224, #226 and the Ferric 1.0 design epics #133–#136), evaluating:
- **Correctness**: render_to_string, hydrate, Axum integration, mismatch detection implement the stated
  acceptance criteria for issues #223, #224, #226.
- **Code quality**: API surface, naming, error handling, test coverage, doc coverage.
- **Security / correctness of HTML escaping**: SSR output escapes injection characters correctly.
- **Non-goals** (do NOT block on these): async resource state carry across the SSR seam (#225 — blocked on
  #130 which is in escalation); anything outside the ferric-ssr goal's scope.

The review DAG posts its review to the PR and produces findings in SYNTHESIS.md.

Review DAG workspace: `taskflow/dags/review-ferric-ssr-r1/`

### 4. Update board and STATE

After forking, record the review DAG in the project state:
- ferric-ssr goal: `current_review_dag: review-ferric-ssr-r1`.
- DAGs in flight: add `review-ferric-ssr-r1` (swe-reviewer, review kind).
- Board hygiene: Issues #223, #224, #226 are `In Review`.

### 5. Schedule what follows

Schedule I264: board check / review fold watch.
- Watch for `taskflow/dags/review-ferric-ssr-r1/SYNTHESIS.md` to appear.
- Bounded wake: forked-thread-completion OR resume_at now + 10 minutes.

## Notes

- Remediation budget for ferric-ssr: 2 of 2 consumed (ferric-ssr-r2 + ferric-ssr-r3). If the review
  finds blockers, escalate rather than launch a 3rd automatic code remediation DAG — unless `REVIEW_GATE.md`
  says a review's blockers call for a standard remediation (which it does, within a separate per-remediation
  budget).
- ferric-async-forms escalation (PR #193): still ACTIVE. Do not close or touch it.
- The landing posture is delegated / auto_land: true — after review APPROVE, land without human gate.
