# COMPLETE — SUBTASK_correctness

**Task**: SUBTASK_correctness — Signature correctness verification  
**Status**: completed  
**Commit reviewed**: `0436218`

## Outputs

- `correctness_findings.md` — findings per schema `../contracts/findings_schema.yaml`

## Summary

All five carry-over items verified against source at commit `0436218`:

| Item | Status |
|------|--------|
| B1 — `RequestBuilder::query()` signature | RESOLVED |
| B2 — `Response::text()` signature | RESOLVED |
| SF3 — `header()` / `default_header()` use `&str` | RESOLVED |
| SF4 — missing public API members added | RESOLVED |
| SF5 — `Method` `#[non_exhaustive]` deferral note | RESOLVED |

One ADVISORY finding recorded: `RequestBuilder::url()` is public in source but absent from the CHANGELOG surface inventory.

**Verdict contribution: APPROVE**
