# _BRIEF.md — NSWE overseer step I201 (persona swe-lead) — ACT: launch review for PR #188

**Depends on**: I200
**Task Kind**: act — load `REVIEW_GATE`, `WORK_SESSION`; write review brief; fork `swe-reviewer` for PR #188.

## Context from I200

- Machine gate for PR #188: **PASS** (all 6 CI jobs pass on run 41743675354, commit `e29e2f4`; PARTIAL verdict
  is test-coverage gap only — not a CI failure or functional regression; IA1–IA5 fully PASS).
- PR #188: `feat(ferric): Ferric 1.0 Authoring Model — view!, components, context (#129)`, OPEN, MERGEABLE.
  Branch: `work/ferric-epic-authoring-r1`. Closes: #129, #137, #138, #139, #140, #141, #142.
- IA6 follow-up issue filed: **#189** (`test(ferric-macros): add trybuild fixtures for view! compile-time
  diagnostics (§2.9 error cases)`). Added to board Todo. Project item ID: `PVTI_lADOEB9jls4BlZH4zhF29XE`.
- **STATE**: `taskflow/overseer/I200/project_state.json` (current_pointer: I200).
- **Config seam**: `taskflow/overseer/_CONFIG.yaml` (landing_authority: delegated, auto_land: true, headless: true).

## Work for this step

### 1. Load governing files
Load `appfiles/REVIEW_GATE.md` and `appfiles/WORK_SESSION.md`.

### 2. Write the review brief and fork the review DAG
Per `REVIEW_GATE.md`: machine PASS → launch a review DAG (`swe-reviewer`) for PR #188.

Write `_BRIEF.md` for the review DAG at `taskflow/dags/review-ferric-epic-authoring-r1/` and fork it.

**Review brief contents** (held to `REVIEW_GATE.md` "The brief describes"):

**Target:**
- PR #188: `feat(ferric): Ferric 1.0 Authoring Model — view!, components, context (#129)`
  - Branch: `work/ferric-epic-authoring-r1`, tip `e29e2f4`
  - Closes: #129 (epic), #137, #138, #139, #140, #141, #142
  - Design: PR #128 (`design: Ferric 1.0 framework design`) merged, design docs at `design/ferric/` on main
  - Code DAG synthesis: `taskflow/dags/ferric-epic-authoring-r1/SYNTHESIS.md`

**Review concerns (as distinct concerns):**
1. *Correctness*: Does the change implement each acceptance criterion of the 6 sub-issues (#137–#142) and the
   epic's integration goal (#129)? Check reactive signals (T01), virtual DOM and DOM patching (T01), view! macro
   lowering table §2.12 constructs (T02), component model props/children/slots/dyn dispatch (T03), component
   type-level diagnostics (T04), context API (T05). Edge cases: memo memoization under unchanged output;
   batch coalescing; keyed-list reorder; slot fill constraints; context shadowing; signal write after mount.
2. *Code quality and design*: Responsibilities and coupling across `crates/ferric` and `crates/ferric-macros`;
   abstraction boundaries (macro / runtime seam; component trait surface; signal/scope lifecycle); duplication;
   naming; function size (note `build_panic_builder` suppression). Does the code leave the ferric internals
   easier to extend?
3. *Test coverage and depth*: Does the test suite exercise each AC and the edge/error paths? Do the tests
   assert real behavior (not vacuous pass)? Unit tests in `crates/ferric`; proc-macro tests in
   `crates/ferric-macros/tests/lowering.rs` and `component.rs`; trybuild suite in
   `crates/ferric-macros/tests/compile_fail_component/` (T04). Note the IA6 gap: view! §2.9 trybuild
   fixtures are absent (follow-up issue #189 filed). Assess whether the absent fixtures are a blocker.
4. *Security*: Input handling in the proc-macro (untrusted token streams from user code); `unsafe` / FFI
   boundaries (wasm-bindgen); any host-specific or internal infrastructure detail committed to the diff.
5. *Rust idiom and API surface*: Proc-macro hygiene (identifier collision avoidance); pub surface of
   `ferric::prelude` additions; `#[allow(dead_code)]` and `#[allow(clippy::too_many_arguments)]` suppressions
   (acceptable short-term deferral or blocker?); backward compatibility (counter.rs example unchanged — IA4).

Add *API/contract stability* concern: the diff extends `ferric::prelude` and introduces a new crate
`ferric-macros`. Check that the additions are additive only and do not break the existing public API.

**Declared output:**
- A review posted on PR #188 as a comment (or approval, subject to platform account constraints).
- Root `SYNTHESIS.md` at `taskflow/dags/review-ferric-epic-authoring-r1/SYNTHESIS.md` with verdict
  APPROVE or REQUEST-CHANGES, findings per concern (severity + blocks), what each concern checked and
  found clean.
- Non-blocking findings filed as grouped, linked backlog issues on `Nousix-LLC/nswe-demo`.

**Repo:** `Nousix-LLC/nswe-demo`
**Branch under review:** `work/ferric-epic-authoring-r1`, tip `e29e2f4`

### 3. Record the fork in STATE and update STATE
- Add `review-ferric-epic-authoring-r1` to `dags_in_flight`.
- Update `free_dag_slots` to 1.
- Record the DAG's fork in STATE.
- Update `current_pointer` to I201.
- Schedule I202 (`depends_on` I201): board check / watch review fold.
