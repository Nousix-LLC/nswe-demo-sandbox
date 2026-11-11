# COMPLETE — SUBTASK_remediate

**Task:** SUBTASK_remediate  
**DAG:** design-ferric-1_0-r2  
**Status:** completed  

## Summary

All 19 GAP-NNN items from the SUBTASK_review-validate review report were addressed. All 6 major gaps
and 13 minor gaps are resolved; 1 minor gap (GAP-031) was confirmed to require no fix because the
condition it described was already corrected in the committed branch file.

Document fixes were committed to `work/design-ferric-1_0` (commit `bbdeb48` plus prior session commits).
GitHub issues #143 and #146 were updated to correct traceability gaps. PR #128 is complete and
ready to merge.

## Declared output

- `SUBTASK_remediate/remediation-report.md` — remediation report conforming to
  `../contracts/_MANIFEST.yaml` §remediation_report_schema, with all four required sections:
  `remediation_summary`, `actions_taken`, `pr_readiness_verdict`, `synthesis_inputs`.

## For SUBTASK_synthesize-root

Read `SUBTASK_remediate/remediation-report.md` §synthesis_inputs for:
- `release_bar_summary`: 29 BAR-FERRIC-* criteria in two stages; BAR-FERRIC-004 is the single
  `must_have: true` criterion
- `epic_index`: 8 epics (#129–#136) with titles, stages, and child issue numbers (#137–#164)
- `pr_number`: 128
