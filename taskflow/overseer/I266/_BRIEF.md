# _BRIEF.md — NSWE overseer step I266 (persona swe-lead) — ACT: process review (review-ferric-ssr-r1)

**Depends on**: I265
**Task Kind**: act — load `appfiles/REVIEW_GATE.md` and `appfiles/BOARD.md`.

## Context from I265

- review-ferric-ssr-r1 (swe-reviewer) **folded** with **REQUEST-CHANGES**.
- Synthesis seam: `taskflow/dags/review-ferric-ssr-r1/SYNTHESIS.md`
- Two blockers:
  - **B1 (REQ-HYD-003)**: `hydrate()` never called from WASM entry point. `crates/chirp-frontend/src/app.rs::start()` calls `ferric::dom::mount` not `ferric::hydrate`. SSR+hydration is not functional end-to-end.
  - **B2 (REQ-SSR-006 / Area E)**: Zero `wasm-bindgen-test` in `hydrate.rs`. Issues #224 and #226 require headless wasm-bindgen-test coverage (adopt walk, event wiring, mismatch detection).
- 14 non-blocking findings already filed by the review DAG as GitHub issues #229–#242:
  - #229: Stale todo-panic comments in `chirp-server/src/ssr.rs`
  - #230: `ferric::hydrate` naming collision (module and function share crate-root path)
  - #231: `ssr_handler` name stutters module name
  - #232: `pub mod dom;` missing `#[cfg(target_arch = "wasm32")]` gate
  - #233: `strip_sentinels` discards `remove_child` result with `let _ =`
  - #234: `wasm_script_path` insertion uses `debug_assert!` stripped in release
  - #235: Seven private helpers duplicated between `hydrate.rs` and `dom.rs`
  - #236: `render_to_string` signature has no seam for async resource injection (#130)
  - #237: `hydrate()` doc missing calling contract
  - #238: `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER` missing stability note
  - #239: Missing `subscriber_count == 0` assertion in SSR isolation tests
  - #240: `adopt_children` warns on trailing DOM nodes but does not remove them
  - #241: Attribute names not HTML-escaped; convention undocumented
  - #242: No end-to-end injection test through `assemble_document`
- Review was posted as a comment on PR #228: https://github.com/Nousix-LLC/nswe-demo/pull/228#issuecomment-6647644348
- Remediation budget: 2 of 2 consumed. No further automatic code DAG (escalation follows in I267).
- ferric-ssr goal: issues #223, #224, #226 (branch `work/ferric-ssr-r1`, PR #228).
- STATE at: `taskflow/overseer/I265/project_state.json`
- Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/REVIEW_GATE.md` and `appfiles/BOARD.md`.

### 2. Read the config seam

Read `taskflow/overseer/_CONFIG.yaml`.

### 3. Confirm review is on PR #228

Verify the review comment is on PR #228. The SYNTHESIS.md records it was posted at:
https://github.com/Nousix-LLC/nswe-demo/pull/228#issuecomment-6647644348
Confirm it is there; if not, post the review content as a comment.

### 4. Sort findings and confirm non-blockers are on the board

The review DAG filed all 14 non-blocking findings as issues #229–#242. These issues need to be added to the
GitHub project board if they are not already there. For each issue #229–#242:
- Add to the GitHub project board (`PVT_kwDOEB9jls4BlZH4`) if not already present.
- Place in the backlog (Todo status).
- Record the new project item IDs in `taskflow/overseer/_CONFIG.yaml` (issue_229 through issue_242).

### 5. Record outcome in STATE

Write updated project state at `taskflow/overseer/I266/project_state.json`:
- Move review-ferric-ssr-r1 from dags_in_flight to dags_folded with verdict: REQUEST-CHANGES
- Update PR #228's reviews field with the review verdict and comment link
- Update ferric_ssr_goal with current_review_dag verdict
- Record non-blockers #229–#242 as filed

### 6. Schedule what follows

Schedule I267: escalate to user (BOARD.md + RETENTION.md).

## Notes

- The two blockers are real and unresolved; remediation budget (2/2) is exhausted. I267 escalates.
- The 14 non-blockers are already filed as GitHub issues. The board add is the remaining work here.
- ferric-async-forms escalation (PR #193): do not close or touch it.
