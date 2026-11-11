# _BRIEF.md — NSWE overseer step I256 (persona swe-lead) — ACT: launch ferric-ssr-r2 remediation DAG

**Depends on**: I255
**Task Kind**: act — load `appfiles/WORK_SESSION.md`, `appfiles/DELIVERABLES_GIT.md`.

## Context from I255 (fold read: ferric-ssr-r1)

### Fold verdict: FAIL — remediate

- ferric-ssr-r1 SYNTHESIS.md: `taskflow/dags/ferric-ssr-r1/SYNTHESIS.md`
- Verdict: **FAIL** — client-hydrate spoke never ran
- Remediation budget: **0 of 2 used** → within budget → remediate

### What is done on `work/ferric-ssr-r1`

- BAR-003 / #223: **MET** — `render_to_string` fully implemented in `crates/ferric/src/ssr.rs`; 56 unit tests pass; TEXT_OPEN_MARKER / TEXT_CLOSE_MARKER correct; HTML escaping complete; ReactiveScope isolation verified
- BAR-004 / #224: **NOT MET** — `crates/ferric/src/hydrate.rs` remains `todo!()` stub; `ferric-ssr-r1-client-hydrate` spoke never ran
- BAR-006 / #226: **PARTIALLY MET** — axum integration (REQ-SSR-011) done (PR #227 merged into goal branch); mismatch detection NOT done (requires BAR-004)
- Identity assertion `marker-format-agreement` FAILED — `<!--$t-->` present in `ssr.rs`, absent from `hydrate.rs` stub
- Branch `work/ferric-ssr-r1` has passing build: `cargo test -p ferric` (56+7 tests), `cargo build -p chirp-server`, all compile checks pass
- Main SHA unchanged: `945fade38abd6b053268501f3801734756f02502` — no rebase needed

### PR #227 (`work/ferric-ssr-r1-axum` → `work/ferric-ssr-r1`): MERGED into goal branch (not main)

### Operating config

- `landing_authority: delegated`, `auto_land: true`, `headless: true`
- STATE last written: `taskflow/overseer/I249/project_state.json`

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md` and `appfiles/DELIVERABLES_GIT.md`.

### 2. Check DAG slots

STATE `dags_in_flight` from I249: ferric-ssr-r1 is now FOLDED (confirmed FAIL in I254/I255). It no longer counts as in flight. 0 DAGs in flight → 4 slots free → launch is clear.

### 3. Write ferric-ssr-r2 DAG brief

Write the brief at `taskflow/dags/ferric-ssr-r2/_FORK.md` and `taskflow/dags/ferric-ssr-r2/_BRIEF.md`.

**Remediation goal — ferric-ssr-r2:**

- **Branch**: `work/ferric-ssr-r1` (continue on the existing branch; no rebase needed)
- **Repo**: `Nousix-LLC/nswe-demo`
- **Goal**: Implement BAR-004 (#224) full hydration + BAR-006 (#226) mismatch detection portion to close the full SSR+hydration goal; open a PR to main
- **Issues to close**: #223 (already MET, include for PR close), #224 (must implement), #226 (partially met — complete the mismatch detection portion)
- **Prior DAG**: `taskflow/dags/ferric-ssr-r1/SYNTHESIS.md` (read it for the full context of what is done and what is missing)

**Brief content — ferric-ssr-r2 `_BRIEF.md`:**

Objective: Complete the SSR+hydration goal by implementing `crates/ferric/src/hydrate.rs` (BAR-004 / #224) and mismatch detection/recovery (the remaining BAR-006 / #226 portion), then open a PR to main closing #223, #224, and #226.

Acceptance criteria:
- #223 / BAR-003: Already MET. `render_to_string` is in `crates/ferric/src/ssr.rs` and must remain correct and passing.
- #224 / BAR-004: `crates/ferric/src/hydrate.rs` — full implementation per `taskflow/dags/ferric-ssr-r1/contracts/ferric_ssr_contract.rs` (hydrate function signature), REQ-SSR-004 (zero structural mutations adopt pass), REQ-SSR-005 (Click/Input event handler wiring using the same Reflect-based approach as dom.rs), REQ-SSR-009 (mismatch detection in debug builds with console::warn, mismatch recovery by client-rendering the mismatched subtree without disturbing successfully adopted siblings/ancestors). The comment-sentinel TEXT_OPEN_MARKER / TEXT_CLOSE_MARKER logic (from the contract) must be respected during the DOM walk.
- #226 / BAR-006: Mismatch detection (REQ-SSR-009) is now implemented as part of BAR-004. Axum integration (REQ-SSR-011) is already done. Issue #226 is fully covered when both sub-concerns are met.
- Identity assertions must all pass:
  - `native-compile`: `cargo check --lib -p ferric` exits 0 (hydrate.rs is cfg(wasm32) only — must not break native compile)
  - `wasm-compile`: `cargo check --target wasm32-unknown-unknown -p ferric` exits 0
  - `native-tests-pass`: `cargo test -p ferric` passes (all existing + any new tests)
  - `chirp-server-compile`: `cargo build -p chirp-server` exits 0
  - `frozen-prelude-unchanged`: no diff on the 4 frozen files
  - `marker-format-agreement`: `<!--$t-->` present in both `ssr.rs` AND `hydrate.rs` (the hydration implementation imports and uses `TEXT_OPEN_MARKER`)
  - `issues-closed`: PR body includes `Closes #223`, `Closes #224`, `Closes #226`; note "BAR-005 / #225 (state carry + async resource resume) is a follow-up issue dependent on #130 and is NOT part of this goal"
- A PR from `work/ferric-ssr-r1` to `main` closing #223, #224, #226 must be created

Non-goals / scope constraints:
- BAR-005 / #225: out of scope (blocked on #130); include the sentence above in the PR body
- Do not modify any frozen files (crates/ferric/src/lib.rs entrypoints, crates/ferric/src/signal.rs, crates/ferric/src/dom.rs public API, crates/ferric/src/router.rs public API — exact list from the r1 DAG's skeleton task)
- Do not force-push any branch
- PR #227 (`work/ferric-ssr-r1-axum` → `work/ferric-ssr-r1`) was already merged into the goal branch; it can be closed/deleted as superseded

Inputs:
- Prior DAG synthesis: `taskflow/dags/ferric-ssr-r1/SYNTHESIS.md`
- Contract (marker constants + signatures): `taskflow/dags/ferric-ssr-r1/contracts/ferric_ssr_contract.rs`
- Existing implementation: `work/ferric-ssr-r1` branch of `Nousix-LLC/nswe-demo`
- Repo: `Nousix-LLC/nswe-demo`

Declared output:
- Commits on `work/ferric-ssr-r1` implementing `hydrate.rs` per the contract
- A PR from `work/ferric-ssr-r1` to `main` in `Nousix-LLC/nswe-demo` closing #223, #224, #226 (not #225)
- Root `SYNTHESIS.md` at `taskflow/dags/ferric-ssr-r2/SYNTHESIS.md` accounting for each acceptance criterion (MET / NOT MET and why)

What to evaluate / concerns:
- **Correctness of the DOM adopt pass**: the hydration walk correctly maps VNode children to DOM children, skips TEXT_OPEN_MARKER and TEXT_CLOSE_MARKER comment sentinels (they are not VNode children), and wires Click/Input events without any structural DOM mutation
- **Mismatch detection and recovery**: debug-build warnings are emitted correctly, and recovery renders the mismatched subtree client-side without disturbing successfully adopted neighbors
- **cfg gating**: hydrate.rs must be compiled only under `cfg(target_arch = "wasm32")` so native compile (`cargo check --lib -p ferric`) continues to pass
- **Reactive effects**: after adoption, signal updates drive the existing diff/patch cycle exactly as dom::mount does
- **All identity assertions pass**
- **PR quality**: title, body, closes syntax, the BAR-005 exclusion sentence

### 4. Fork the DAG

Fork the ferric-ssr-r2 DAG (swe-coder).

### 5. Update STATE

Write an updated project_state.json at `taskflow/overseer/I256/project_state.json`:
- Move `ferric-ssr-r1` from `dags_in_flight` to `dags_folded` with `verdict: FAIL`, `synthesis_path: taskflow/dags/ferric-ssr-r1/SYNTHESIS.md`, `folded_confirmed_in: overseer/I255`
- Add `ferric-ssr-r2` to `dags_in_flight` with its workspace_path and fork context
- Record `remediation_attempt: 1` for the ferric-ssr goal (1 of 2 budget used)
- `free_dag_slots: 3` (1 in flight now)
- Keep the ferric-async-forms escalation as ACTIVE, no change
- Keep deployment_check, main_sha, all prs unchanged
- Note I257 (board check) next

### 6. Schedule I257

I257 is already in the serial plan (scheduled from I255). No additional amend needed here.

## Notes

- ferric-ssr-r2 is remediation attempt 1 of 2
- #35 (logged-out reading): dispatch after ferric-ssr lands — still deferred
- ferric-async-forms escalation: ACTIVE, no action this iteration
- main SHA: `945fade38abd6b053268501f3801734756f02502` (unchanged)
- After ferric-ssr-r2 folds: machine gate → review launch → process review → landing decision → land → then dispatch #35
