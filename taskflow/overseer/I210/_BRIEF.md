# _BRIEF.md — NSWE overseer step I210 (persona swe-lead) — ACT: launch ferric-async-forms-r2 (remediation)

**Depends on**: I209
**Task Kind**: act — load `WORK_SESSION`, `DELIVERABLES_GIT`. Write remediation brief and fork ferric-async-forms-r2.

## Context from I209

- ferric-async-forms-r1 folded with internal SYNTHESIS verdict "PASSED", but the declared output was
  not met: **machine gate = FAIL** for two reasons:
  1. **Wrong repository**: DAG created PR in `Nousix-LLC/ferric` (PR #5) instead of
     `Nousix-LLC/nswe-demo`. Branch `work/ferric-async-forms-r1` exists in `Nousix-LLC/ferric`,
     not in `Nousix-LLC/nswe-demo`. The brief explicitly required `Repo: Nousix-LLC/nswe-demo`.
  2. **CI not run**: `statusCheckRollup: []` — no GitHub Actions CI jobs ran on the PR. The declared
     output required all 6 CI jobs (fmt, clippy, test, wasm, doc, image) to PASS on the PR head in
     `Nousix-LLC/nswe-demo`. The SYNTHESIS substituted a local `cargo check` for real CI.
- The code itself (at commits `5e49c4f`→`ab7620a`→`98a7559`→`6de5e09`→`ad657f5` on branch
  `work/ferric-async-forms-r1` in `Nousix-LLC/ferric`) may be of good quality but was delivered
  to the wrong repo.
- ferric-router-r1 is still RUNNING. This is the first remediation attempt for ferric-async-forms
  (budget: 2).
- **STATE**: `taskflow/overseer/I209/project_state.json`.
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`.

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/DELIVERABLES_GIT.md`.

### 2. Write the remediation brief

Write `taskflow/dags/ferric-async-forms-r2/_BRIEF.md`. The brief must carry:

**The lesson (prior attempt's failure):**
- ferric-async-forms-r1 created its PR in `Nousix-LLC/ferric` (PR #5) instead of
  `Nousix-LLC/nswe-demo`. The ferric repo (`Nousix-LLC/ferric`) is a separate repository and is
  NOT the target. All code for this engagement lives in `Nousix-LLC/nswe-demo` under `crates/ferric`.
- The ferric repo's PR closes issues #1–4 in that repo's tracker, not the nswe-demo board
  issues #130, #143, #144, #145. The nswe-demo board issues remain open.
- CI did not run because `Nousix-LLC/ferric` has no GitHub Actions CI configuration. All six CI
  jobs (fmt, clippy, test, wasm, doc, image) must PASS on `Nousix-LLC/nswe-demo`.

**The prior code (what was produced — examine and use if correct):**
- Commits on `work/ferric-async-forms-r1` in `Nousix-LLC/ferric`: `5e49c4f` (walking skeleton),
  `ab7620a` (async_resource), `98a7559` (FormField/Bind), `6de5e09` (EventKind set), `ad657f5`
  (prelude re-exports).
- These commits implement the three capabilities. The code may be sound but must be delivered from
  `Nousix-LLC/nswe-demo`, branched from `main` at `aa2468771eccd9e2ee79c12c79b8943fca18e07a`
  (the authoring model base).
- The DAG must examine the prior code, verify its correctness against the design, and produce the
  correct deliverable (branch + PR in nswe-demo, all 6 CI PASS, Closes #130/#143/#144/#145).

**The original acceptance criteria**: same as ferric-async-forms-r1 — issues #130, #143, #144, #145
with their full acceptance criteria from the design documents (design/ferric/async-forms-events.md
§1–§3, REQ-ASYNC-001..016, REQ-ASYNC-020..024, REQ-ASYNC-040..043, BAR-FERRIC-012..014).

### 3. Fork the remediation DAG

Fork `ferric-async-forms-r2` as `swe-coder` from the written brief.

### 4. Update STATE

Update `taskflow/overseer/I209/project_state.json`:
- Move ferric-async-forms-r1 from `dags_in_flight` to `dags_folded` with `machine_gate: FAIL`,
  reason: "wrong repo (Nousix-LLC/ferric instead of nswe-demo), CI not run".
- Add ferric-async-forms-r2 to `dags_in_flight`.
- Update `free_dag_slots` to 2 (ferric-router-r1 running + ferric-async-forms-r2 running = 2 in
  flight).
- Update board note.
- Write to `taskflow/overseer/I210/project_state.json`.

## Notes

- Do not close or modify PR #5 in `Nousix-LLC/ferric` — leave it as-is. The remediation creates
  a fresh PR in `Nousix-LLC/nswe-demo`.
- The board issues #130, #143, #144, #145 remain In Progress (they are still being worked by the
  remediation).
- main_sha: `aa2468771eccd9e2ee79c12c79b8943fca18e07a` (unchanged).
- I211 follows (board check / watch folds: ferric-async-forms-r2, ferric-router-r1).
