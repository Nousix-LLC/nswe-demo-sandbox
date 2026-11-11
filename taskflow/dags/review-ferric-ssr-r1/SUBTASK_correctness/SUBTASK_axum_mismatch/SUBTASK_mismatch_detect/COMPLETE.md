# COMPLETE — SUBTASK_mismatch_detect

**Task**: SUBTASK_mismatch_detect
**Status**: completed
**Completed at**: 2026-11-04

## Declared Output

`mismatch_detect_findings.md` — written to this workspace before this terminal record.

## Summary

Reviewed `crates/ferric/src/hydrate.rs` (PR #228, branch `work/ferric-ssr-r1`) against
the REQ-SSR-009 mismatch-detection acceptance criterion from issue #226.

**Verdict: FINDING (BLOCKER)**

- Detection logic and warn-not-panic error handling: CLEAN
- Recovery (fresh mount for mismatched subtree): FINDING NON-BLOCKER (extra DOM nodes not removed)
- Test coverage: FINDING BLOCKER (no `wasm-bindgen-test` for mismatch path; criterion
  explicitly requires one)

**Marker format documented**: Text-boundary HTML comment sentinels `<!--$t-->` /
`<!--/$t-->` (constants `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER` in
`crates/ferric/src/ssr.rs`). No attribute-based hydration markers exist. Client imports
constants from the same source as the server — consistent by construction.

**Requirement ID note**: Brief labels criterion "REQ-SSR-006"; issue #226 and the code
both use "REQ-SSR-009". Same criterion; synthesis should note the divergence.
