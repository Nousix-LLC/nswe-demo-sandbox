# _BRIEF.md — NSWE overseer step I224 (persona swe-lead) — ACT: launch review-ferric-router-r3

**Depends on**: I223
**Task Kind**: act — load `REVIEW_GATE` + `WORK_SESSION`. Launch review DAG for PR #203.

## Context from I223 (EVALUATE: board check / watch ferric-router-r3 fold)

- **ferric-router-r3 FOLDED** — machine gate PASS.
  - CI run 41796577463: all 6 checks SUCCESS (fmt, clippy, test, wasm, doc, image).
  - Fix: removed unused `VNode` import from test closure in `crates/ferric-router/src/router.rs`.
  - Branch: `work/ferric-router-r3`, commit `7219e21`.
  - PR: #203 — "fix(ferric-router): remove unused VNode import from test closure (remediation r3)"
  - Base: `main`. PR OPEN/MERGEABLE.
- **ferric-router-r3 moved to dags_folded** (machine gate PASS).
- **free_dag_slots**: 2 → 3.
- **ferric-async-forms escalation**: ACTIVE, no user response yet. Hold.
- **Config**: delegated/auto_land/headless.
- **STATE**: `taskflow/overseer/I223/project_state.json`.
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`.

## Work for this step

### 1. Load governing files
Load `appfiles/REVIEW_GATE.md` + `appfiles/WORK_SESSION.md`. Read `_CONFIG.yaml` and
`taskflow/overseer/I223/project_state.json`.

### 2. Confirm PR #203 state
Verify PR #203 is OPEN/MERGEABLE with CI all 6 PASS (run 41796577463). Confirm base branch is `main` and
the head commit is `7219e21`.

### 3. Launch review-ferric-router-r3
Write the review brief at `taskflow/dags/review-ferric-router-r3/_BRIEF.md` following REVIEW_GATE.md:
- **Target**: PR #203 — `work/ferric-router-r3` (4 commits: 3 from r2 cherry-picks + r3 clippy fix).
  Issues covered: #131, #146, #147.
  Design source: `design/ferric/router-and-http.md` (Part 1, REQ-RT-001..008).
  Code DAG SYNTHESIS: `taskflow/dags/ferric-router-r3/SYNTHESIS.md`.
  Prior review: review-ferric-router-r1 (REQUEST_CHANGES — B1 PR bundled unreviewed scope; now resolved by PR split).
- **Review concerns** (5 concerns):
  1. Correctness — does the change satisfy REQ-RT-001..008 and each issue's ACs (#131, #146, #147)?
     Check edge cases, error paths, invariants, router state transitions.
  2. Code quality — responsibilities, abstraction boundaries, naming, function size, error-handling style.
  3. Test coverage — do the tests exercise each AC and edge/error paths? Do they assert real behavior?
  4. Rust idioms — lifetimes, pub surface, wasm-bindgen idioms, soundness.
  5. API/contract stability — additive vs breaking on the prelude/public surface; frozen items unchanged.
- **Declared output**: posted review on PR #203, root `SYNTHESIS.md` with APPROVE or REQUEST_CHANGES verdict,
  findings per concern with severity and blocker/non-blocker classification, non-blocking findings filed as
  backlog issues.
- Launch as `swe-reviewer`. Note: review-ferric-router-r1 already gave REQUEST_CHANGES on scope (B1 —
  bundled unreviewed scope); that issue is now resolved (PR #203 is router-only, 4 commits). This review
  is a first full code review of the router-only change.

### 4. Update project STATE
Write `taskflow/overseer/I224/project_state.json` with:
- review-ferric-router-r3 in dags_in_flight.
- free_dag_slots: 3 → 2.
- forward_series.I224 entry.

### 5. Schedule I225
I225: EVALUATE — board check / watch review-ferric-router-r3 fold.

## Notes
- Config: delegated/auto_land/headless.
- review-ferric-router-r3 runs as `swe-reviewer`.
- If review APPROVE: land PR #203 under delegated authority (land task next).
- If review REQUEST_CHANGES: escalate (remediation budget for ferric-router is exhausted — r1+r2+r3 is 3 code DAGs; the budget was 2 remediation DAGs beyond r1; we are at the limit).
- ferric-async-forms escalation (#130 / PR #193) still active — do NOT launch ferric-async-forms-r3 without user decision.
