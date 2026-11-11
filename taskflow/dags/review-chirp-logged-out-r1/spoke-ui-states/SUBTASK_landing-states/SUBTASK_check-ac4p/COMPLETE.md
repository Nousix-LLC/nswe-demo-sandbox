# COMPLETE — SUBTASK_check-ac4p

**Task**: AC-4 (partial) — `header_nav()` in every rendered state of `landing_view`  
**Pinned commit**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`  
**Output**: `concern_ac4p.md` (this workspace)

## What Was Done

Read `crates/chirp-frontend/src/landing.rs` at the pinned commit. Located `view_tree` (lines 238–267) — the pure dispatch function called by `landing_view`. Enumerated all four branches of the if/else dispatch logic (loading state, initial error state, empty/loaded state, populated state). Confirmed that `header_nav()` is called at line 264 in the **outer wrapper**, outside and after all branch arms, making its presence structural and not per-branch.

Verified `header_nav()` definition (lines 270–277): non-conditional, always renders `div.chirp-landing-nav` with both `/signup` and `/signin` links.

Also read the `footer()` sub-branches (lines 352–375) to confirm they operate inside `body` only and do not affect the `header_nav()` placement.

## Result

**Status: clean.** `header_nav()` is present in every rendered state via the outer wrapper at line 264. No branch can render without it. No findings.

## Success Criteria Check

- [x] ALL branches of `view_tree`'s dispatch logic enumerated and accounted for (4 branches)
- [x] `header_nav()` presence or absence in each branch noted with specific line (line 264 for all)
- [x] Every clean note cites file + line at pinned commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- [x] `concern_ac4p.md` written to this workspace
