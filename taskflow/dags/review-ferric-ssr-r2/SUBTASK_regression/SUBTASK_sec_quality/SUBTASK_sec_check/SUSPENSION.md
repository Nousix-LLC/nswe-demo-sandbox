# SUBTASK_sec_check — Suspension Record

**Status**: Suspended — NeedsDecompose  
**Suspended at**: 2026-11-05  
**Resumption**: When all child tasks reach terminal state (SUBTASK_seccheck_synth COMPLETED folds this node)

## Decomposition

This node decomposed into four children:

| Task ID | Kind | Depends on | Output |
|---------|------|------------|--------|
| `SUBTASK_html_inj` | standard | none | `SUBTASK_html_inj/html_inj_finding.md` |
| `SUBTASK_dom_spoof` | standard | none | `SUBTASK_dom_spoof/dom_spoof_finding.md` |
| `SUBTASK_test_inj` | standard | none | `SUBTASK_test_inj/test_inj_finding.md` |
| `SUBTASK_seccheck_synth` | synthesis | SUBTASK_html_inj, SUBTASK_dom_spoof, SUBTASK_test_inj | `security_raw_findings.md`, `SYNTHESIS.md` (at this workspace root) |

## Resumption Condition

SUBTASK_seccheck_synth must complete, having:
- Written `security_raw_findings.md` at this workspace root
- Written `SYNTHESIS.md` at this workspace root
- Called `engine_resume_suspended` with `target_task_id = proc-329f53fb-256d-41c0-8873-0894bcf81914`

## Declared Output

`security_raw_findings.md` at this workspace root — security findings per `../contracts/spoke_output_schema.md` §SUBTASK_sec_check.
