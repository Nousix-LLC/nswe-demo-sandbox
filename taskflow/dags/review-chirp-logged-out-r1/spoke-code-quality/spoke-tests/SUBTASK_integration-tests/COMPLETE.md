# COMPLETE — SUBTASK_integration-tests

**Task**: Concern 2 — integration test depth in `mod public_timeline`
**Output**: `SUBTASK_integration-tests/analysis.md`
**Commit**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`

## What was done

Read `crates/chirp-server/tests/api.rs` at the pinned commit. Examined all four tests in
`mod public_timeline` (lines 837–925). Verified the three acceptance criteria:

1. **Cursor round-trip**: `public_timeline_paginates_with_cursor` (lines 869–903) performs a
   genuine round-trip — cursor extracted from page 1, passed to page 2, page 2 returns the
   remaining item. Clean.

2. **Boundary at exactly `limit` items**: not tested. The pagination test creates 3 items with
   `limit=2` (n = limit + 1). No test covers n = limit. Finding A raised, non-blocking.

3. **Auth regression guard**: `public_timeline_requires_no_auth` (lines 906–924) hits
   `/api/timeline` (the authenticated endpoint) without auth and asserts `UNAUTHORIZED`.
   URL and assertion are correct. Clean.

## Composition note

`analysis.md` conforms to `../contracts/analysis_schema.md`: one `## Verdict` (FINDING(S)),
one `## Findings` subsection, one `## Evidence` section. `SUBTASK_synthesis` reads this file
to assemble `../FINDINGS.md`.
