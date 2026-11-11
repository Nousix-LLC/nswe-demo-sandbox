# SUBTASK_correctness_synthesis — COMPLETE

**Task**: Correctness Review Verification Gate
**Status**: completed
**Output**: `../correctness_findings.md`

## Gate Checks Run

### Check 1: Coverage — PASS
All 11 in-scope criteria have verdicts across the three spokes:
- REQ-SSR-001–005: all present in `ssr_render_findings.md`
- REQ-HYD-001–004: all present in `hydration_findings.md`
- REQ-SSR-006, REQ-MIS-001–002: all present in `axum_mismatch_findings.md`
- REQ-SSR-007 non-goal confirmation: present in `axum_mismatch_findings.md`

### Check 2: Marker Format Consistency — PASS (CONSISTENT)
Both spokes document identical HTML comment sentinel constants (`TEXT_OPEN_MARKER = "<!--$t-->"`,
`TEXT_CLOSE_MARKER = "<!--/$t-->"`) defined once in `crates/ferric/src/ssr.rs` and imported by
`crates/ferric/src/hydrate.rs`. Agreement by construction; confirmed by the axum_mismatch
cross-check section. Documentation note: three spokes cite different line numbers for the two
constants (ssr_render: 835/842; hydration: 28/35; axum_mismatch: 33/50) — functional information
consistent; line citations require verification.

### Check 3: Non-Goal Confirmed — PASS
`axum_mismatch_findings.md` contains an explicit "CONFIRMED NON-GOAL" verdict for REQ-SSR-007
with three evidence citations from `crates/chirp-server/src/ssr.rs`.

### Check 4: Spoke Output Quality — PASS
All three spokes cite concrete code evidence at file:line references in `crates/` repository paths.
No host paths appear in any spoke's evidence. Blockers clearly labeled with actionable remediation.

## Gate Verdict: FAIL (2 blockers)

**BLOCKER 1 — REQ-HYD-003**: `hydrate()` never called from WASM entry point.
`crates/chirp-frontend/src/app.rs::start()` calls `ferric::dom::mount()` instead of
`ferric::hydrate()`. PR #228 does not modify that file. SSR+hydration is non-functional end-to-end.

**BLOCKER 2 — REQ-SSR-006**: No `wasm-bindgen-test` covering mismatch detection, warning, or
recovery. Acceptance criterion (issue #226) explicitly requires this test. No `#[cfg(test)]` block
in `crates/ferric/src/hydrate.rs`; no `crates/ferric/tests/` directory on branch.

## Non-Blockers (4)
- REQ-SSR-002: SSR tests do not directly assert `subscriber_count == 0` after render
- REQ-SSR-005: Stale comment at `crates/chirp-server/src/ssr.rs:236–237` claiming `todo!()` panic
- REQ-HYD-002: No `wasm_bindgen_test` for hydrate→signal→DOM sequence
- REQ-MIS-001: Stale comment at `crates/chirp-server/src/ssr.rs:165–168` describing `render_to_string` as stub
- REQ-SSR-006 (secondary): Extra DOM nodes warned but not removed
- Label discrepancy: REQ-SSR-006 (spec) vs REQ-SSR-009 (code/issue)
