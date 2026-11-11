# _BRIEF.md — NSWE overseer step I262 (persona swe-lead) — EVALUATE: board check / ferric-ssr-r3 fold watch

**Depends on**: I261
**Task Kind**: evaluate — load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

## Context from I261

- ferric-ssr-r3 remediation DAG (swe-coder) was forked against branch `work/ferric-ssr-r1`.
- This is **attempt 2 of 2** (the last automatic remediation attempt). If ferric-ssr-r3 CI still fails, escalate to the user with both attempts (ferric-ssr-r2 and ferric-ssr-r3) and their outcomes.
- ferric-async-forms escalation (PR #193) is still ACTIVE — no user response has been received.
- Main SHA at last board check: `945fade38abd6b053268501f3801734756f02502`
- STATE at: `taskflow/overseer/I256/project_state.json`

## DAG to watch

- **ferric-ssr-r3**: `taskflow/dags/ferric-ssr-r3/` — forked in I261. A DAG has folded when its root `SYNTHESIS.md` exists. Do not poll it; check on the bounded wake.

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

### 2. Read the config seam

Read `taskflow/overseer/_CONFIG.yaml`.

### 3. Check the board

Perform a full board check:
- Has ferric-ssr-r3 folded (does `taskflow/dags/ferric-ssr-r3/SYNTHESIS.md` exist)?
  - If folded: read the verdict (PASS / FAIL).
    - **PASS**: machine gate passes → schedule a review-launch task (I263: load `REVIEW_GATE`, launch `swe-reviewer` review DAG for PR #228).
    - **FAIL** (attempt 2 of 2 exhausted): schedule an escalation task (I263: load `BOARD` + `RETENTION`, escalate to the user with both ferric-ssr-r2 and ferric-ssr-r3 outcomes and ask for guidance).
  - If not folded: ferric-ssr-r3 is still in flight — suspend on the bounded wake and schedule another board check.
- Check for any other board changes: new issues, comments, reviews posted, PRs that have changed state since the last board check.
- ferric-async-forms escalation (PR #193): confirm still ACTIVE (no user response has arrived). Do not interpret any board events about it as resolved.
- **Do not start any new goals while ferric-ssr-r3 is in flight.**

### 4. Bounded wake

If ferric-ssr-r3 is not yet folded: self-suspend with a bounded wake:
- `forked-thread-completion` for ferric-ssr-r3 (the DAG's terminal)
- `schedule / resume_at`: now + 10 minutes
Whichever fires first wakes this iteration.

## Notes

- Remediation budget: attempt 2 of 2 consumed. If ferric-ssr-r3 fails, escalate — do not launch a third automatic remediation.
- The ferric-async-forms escalation (PR #193) is still ACTIVE.
