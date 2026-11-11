# COMPLETE — SUBTASK_rbar_gap

## Task

Independent gap sweep of all canonical Ferric 1.0 framework surfaces against the 8 spoke REQ-* registers.

## Output

`gap-analysis-internal.md` — written at this workspace root.

## Summary

- 25 canonical surfaces assessed (the brief's table has 25 rows; the success criteria reference "24" — all rows were assessed).
- 3 additional surfaces found in spoke docs and assessed.
- **18 surfaces: covered** — each cites ≥1 real REQ-* id from a spoke register.
- **2 surfaces: gap** — accessibility of framework output (no REQ-FW-* for general ARIA/semantic HTML in app-authored components) and testing story for app authors (no register entry for a testing harness or methodology offered to app authors).
- **7 surfaces: out-of-1.0** — 4 canonical (scoped CSS REQ-FW-015, devtools REQ-FW-016, hot reload REQ-FW-017, desktop/mobile REQ-FW-018) plus 3 additional (URL query parameters REQ-RT-009, streaming SSR / server functions / islands, typed enum routes).

## Success criteria check

- [x] All 24 (25) canonical surfaces assessed with a status and notes
- [x] Additional surfaces from spoke docs assessed and added
- [x] All four required out-of-1.0 surfaces present with status=out-of-1.0
- [x] All covered surfaces cite at least one real REQ-* id from a spoke register
- [x] Accessibility assessed (gap); testing story assessed (gap)
- [x] gap-analysis-internal.md written at this workspace root

## Downstream

`SUBTASK_rbar_criteria` may proceed: it reads `gap-analysis-internal.md` to write BAR-FERRIC-* criteria for every covered surface.
