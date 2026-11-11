# COMPLETE — SUBTASK_hyd004

**Task**: REQ-HYD-004 Marker Schema Consistency
**Status**: completed
**Verdict**: CLEAN

## Output

- `criterion_004.md` — REQ-HYD-004 finding with mandatory `## Marker Schema` section

## Summary

The PR uses HTML comment sentinels (`<!--$t-->` / `<!--/$t-->`) as text-boundary markers, not
`data-hydration-id` attributes. Both sides import the same `pub const` values from
`crates/ferric/src/ssr.rs`; there is no local copy in `hydrate.rs`. The scheme is deterministic
(static constants, no per-render state). REQ-HYD-004 is satisfied.
