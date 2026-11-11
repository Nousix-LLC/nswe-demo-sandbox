# SYNTHESIS.md — SUBTASK_findings-synthesis

**Task**: SUBTASK_findings-synthesis  
**Subtree**: design-doc-review (SUBTASK_design-doc-review)  
**Status**: COMPLETED

## What This Task Did

Read the three spoke findings files produced by the design-doc-review subtree, asserted all four identities declared in `contracts/_MANIFEST.yaml`, and merged them into the final `../design-doc-findings.md` conforming to the ancestor `contracts/findings_schema.yaml`.

## Output Produced

**`../design-doc-findings.md`** (`taskflow/dags/design-ferric-1_0-r3/SUBTASK_design-doc-review/design-doc-findings.md`)

A YAML findings file with:
- `spoke: design-doc-review`
- `concern_ids: [1, 2, 3]`
- 17 findings from all three spokes, IDs preserved as-is (DDR-C-*, DDR-B-*, DDR-T-*)
- `summary.blocking_count: 5`, `summary.blocking_count: 12`

## Identity Assertions

All four identities from `contracts/_MANIFEST.yaml` were asserted before writing the output.

**I-1 — Each spoke's concern_ids names exactly its assigned concern: PASSED**  
- completeness-review: concern_ids [1] — exactly concern 1 only.
- release-bar-quality: concern_ids [2] — exactly concern 2 only.
- traceability-review: concern_ids [3] — exactly concern 3 only.
- No overlap; together they cover [1, 2, 3].

**I-2 — Every finding has severity, concern, location, statement, recommendation: PASSED**  
All 17 findings (DDR-C-001..003, DDR-B-001..011, DDR-T-001..003) have all five required fields populated with non-empty values.

**I-3 — Merged output contains every finding from every spoke: PASSED**  
Pre-merge count: 3 (completeness) + 11 (release-bar) + 3 (traceability) = 17.  
Post-merge count: 17. All findings present; none dropped or renamed.

**I-4 — summary.blocking_count equals count of severity==BLOCKING findings: PASSED**  
BLOCKING findings identified: DDR-B-001, DDR-B-002, DDR-B-003, DDR-B-004, DDR-B-005 = 5.  
summary.blocking_count in output: 5. Match confirmed.

No identity failures. No silent plugs.

## Findings Summary

| Spoke | Concern | Findings | BLOCKING |
|---|---|---|---|
| completeness-review | 1 | 3 | 0 |
| release-bar-quality | 2 | 11 | 5 |
| traceability-review | 3 | 3 | 0 |
| **Total** | **1–3** | **17** | **5** |

The five BLOCKING findings (all concern 2) require changes to `release-bar.md` before PR#128 can merge:
- DDR-B-001, DDR-B-004, DDR-B-005: no version anchor on the "baseline" API surfaces in the backward-compatibility criteria for `ferric`, `ferric-router`, and `ferric-http`.
- DDR-B-002: no named sanitizer and no specified assertion for the HTML injection safety test.
- DDR-B-003: no observable outcome (warning, panic, log, re-render) specified for hydration mismatch detection.
