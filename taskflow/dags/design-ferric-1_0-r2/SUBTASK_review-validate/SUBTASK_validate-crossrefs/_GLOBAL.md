# SUBTASK_validate-crossrefs — Subtree Hub

## Context

**Status**: Active  
**Part of**: review-validate subtree (design-ferric-1_0-r2 recovery DAG)  
**Purpose**: Validate REQ cross-references and GitHub issue traceability, producing
`crossrefs-findings.md` conforming to `../contracts/_MANIFEST.yaml` §crossrefs_findings_schema.

### Objective

Two distinct analyses run in parallel after reading the nine concern-findings.md files:

1. **REQ register reconciliation** — build the full REQ-* inventory from all nine
   concern-findings.md files, check for duplicate ids, spot-check orphaned cross-references
   against the design documents, and verify that every BAR-FERRIC-* criterion cites at least
   one REQ-* id present in the inventory.

2. **Issue traceability** — query GitHub issues #129–#164 (8 epics, 28 child issues), check
   each for REQ-* citations, flag issues with no requirement reference, flag significant REQ-*
   requirements with no corresponding issue, and perform the special #137 scope check.

A synthesis task then combines both intermediate outputs into the single `crossrefs-findings.md`
required by the parent contract.

### Success Criteria

- [ ] `SUBTASK_req-reconciliation` produces `req-reconciliation.md` with all three checks complete
- [ ] `SUBTASK_issue-traceability` produces `issue-traceability.md` with all 36 issues checked
- [ ] `SUBTASK_synthesis-crossrefs` produces `crossrefs-findings.md` conforming to the parent
  schema (sections: req_register_reconciliation, issue_traceability, gaps GAP-090 through GAP-099)

---

## Key Inputs Shared Across All Tasks

| Resource | Location | Notes |
|---|---|---|
| Concern findings (all 9) | `../SUBTASK_validate-*/concern-findings.md` (relative to parent workspace) | Already completed; REQ inventory source |
| Design documents | `design/ferric/` on branch `work/design-ferric-1_0` at `/home/user/nswe-demo` | For targeted spot-checks; `git show work/design-ferric-1_0:design/ferric/<file>` |
| GitHub issues | `gh issue view <N> --repo Nousix-LLC/nswe-demo` | Issues #129–#164 |
| Parent contract schema | `../contracts/_MANIFEST.yaml` §crossrefs_findings_schema | Output structure for crossrefs-findings.md |

### Concern-Findings Paths (relative to parent workspace)

| Concern | Path | REQ prefix |
|---|---|---|
| Framework scope | `SUBTASK_validate-scope/concern-findings.md` | REQ-FW-* |
| SSR + hydration | `SUBTASK_validate-ssr/concern-findings.md` | REQ-SSR-* |
| Authoring model | `SUBTASK_validate-authoring/concern-findings.md` | REQ-API-* |
| Async/forms/events | `SUBTASK_validate-async/concern-findings.md` | REQ-ASYNC-* |
| Router + HTTP | `SUBTASK_validate-router/concern-findings.md` | REQ-RT-*, REQ-HTTP-* |
| Docs & DX | `SUBTASK_validate-docs/concern-findings.md` | REQ-DX-* |
| Release | `SUBTASK_validate-release/concern-findings.md` | REQ-REL-* |
| Performance | `SUBTASK_validate-perf/concern-findings.md` | REQ-PERF-* |
| Release bar/plan | `SUBTASK_validate-plan/concern-findings.md` | BAR-FERRIC-* → REQ-* citations |

---

## Task Structure

```
_GLOBAL.md (this document)
├── contracts/_MANIFEST.yaml
├── SUBTASK_req-reconciliation/_BRIEF.md
├── SUBTASK_issue-traceability/_BRIEF.md
└── SUBTASK_synthesis-crossrefs/_BRIEF.md
```

### Task Summary

| Task id | Depends on | Description | Output |
|---|---|---|---|
| `SUBTASK_req-reconciliation` | none | Build REQ inventory; check duplicates, orphaned refs, BAR-FERRIC citations | `SUBTASK_req-reconciliation/req-reconciliation.md` |
| `SUBTASK_issue-traceability` | none | Query GitHub issues #129–#164; check REQ citations; special #137 check | `SUBTASK_issue-traceability/issue-traceability.md` |
| `SUBTASK_synthesis-crossrefs` | `SUBTASK_req-reconciliation`, `SUBTASK_issue-traceability` | Assemble crossrefs-findings.md from both intermediate outputs | `crossrefs-findings.md`, `SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_req-reconciliation   ──┐
                               ├──> SUBTASK_synthesis-crossrefs
SUBTASK_issue-traceability   ──┘
```

---

## Contract

**Contract location**: `contracts/`  
**Contract kind**: `yaml_schema`  
**Inherits from**: `../contracts/_MANIFEST.yaml` §crossrefs_findings_schema (READ-ONLY)

The `contracts/_MANIFEST.yaml` in this workspace declares the structure of the two
intermediate artifacts (`req-reconciliation.md`, `issue-traceability.md`) and the
ownership of the final `crossrefs-findings.md`. See `contracts/_MANIFEST.yaml` for details.
