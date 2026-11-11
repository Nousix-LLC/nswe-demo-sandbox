# SUSPENSION — SUBTASK_review-validate

**Status**: Suspended (NeedsDecompose)  
**Suspended at**: 2026-11-03T04:10:09Z

## Decomposition Summary

SUBTASK_review-validate decomposed into 11 child tasks after evaluating the scope trigger:
the brief explicitly enumerates nine distinct concern areas (each reading different source
documents) plus REQ register cross-referencing and issue traceability — three distinct
analysis responsibilities that each fire the enumerated-concerns rule.

## Child Subtree

### Phase 1 — Parallel concern validators (no dependencies)

| Task id | Concern | Output |
|---|---|---|
| `SUBTASK_validate-scope` | Framework scope & 1.0 requirements | `SUBTASK_validate-scope/concern-findings.md` |
| `SUBTASK_validate-ssr` | SSR + hydration | `SUBTASK_validate-ssr/concern-findings.md` |
| `SUBTASK_validate-authoring` | Authoring model | `SUBTASK_validate-authoring/concern-findings.md` |
| `SUBTASK_validate-async` | Async, forms & events | `SUBTASK_validate-async/concern-findings.md` |
| `SUBTASK_validate-router` | Router + HTTP/JSON client | `SUBTASK_validate-router/concern-findings.md` |
| `SUBTASK_validate-docs` | Documentation & DX | `SUBTASK_validate-docs/concern-findings.md` |
| `SUBTASK_validate-release` | Release & distribution | `SUBTASK_validate-release/concern-findings.md` |
| `SUBTASK_validate-perf` | Performance & benchmark | `SUBTASK_validate-perf/concern-findings.md` |
| `SUBTASK_validate-plan` | The plan (release-bar + release-plan) | `SUBTASK_validate-plan/concern-findings.md` |

### Phase 2 — Cross-reference validator (depends on all Phase 1)

| Task id | Purpose | Output |
|---|---|---|
| `SUBTASK_validate-crossrefs` | REQ id reconciliation + issue traceability (#129–#164) | `SUBTASK_validate-crossrefs/crossrefs-findings.md` |

### Phase 3 — Synthesis (depends on Phase 2)

| Task id | Purpose | Output |
|---|---|---|
| `SUBTASK_synthesis` | Assemble review-report.md from all findings | `review-report.md` (at this workspace) |

## Resumption Condition

All 11 child tasks reach terminal lifecycle states. The synthesis task (SUBTASK_synthesis)
produces `review-report.md` at this workspace, which is the declared output of SUBTASK_review-validate.

## Named State Authored

- `_GLOBAL.md` — subtree hub at this workspace
- `contracts/_MANIFEST.yaml` — concern_findings_schema and crossrefs_findings_schema
- `SUBTASK_validate-scope/_BRIEF.md`
- `SUBTASK_validate-ssr/_BRIEF.md`
- `SUBTASK_validate-authoring/_BRIEF.md`
- `SUBTASK_validate-async/_BRIEF.md`
- `SUBTASK_validate-router/_BRIEF.md`
- `SUBTASK_validate-docs/_BRIEF.md`
- `SUBTASK_validate-release/_BRIEF.md`
- `SUBTASK_validate-perf/_BRIEF.md`
- `SUBTASK_validate-plan/_BRIEF.md`
- `SUBTASK_validate-crossrefs/_BRIEF.md`
- `SUBTASK_synthesis/_BRIEF.md`
