# Task: Validate — The Plan (Release Bar + Release Plan)

## Task Specification

**Slug**: SUBTASK_validate-plan
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-designer

### Objective

Read `release-bar.md` and `release-plan.md` on branch `work/design-ferric-1_0` and produce
`concern-findings.md` conforming to `../contracts/_MANIFEST.yaml` §concern_findings_schema.

### Context

Part of the review-validate subtree (see `_GLOBAL.md` in the parent workspace). These two
documents form the consolidated release gate and the ordered delivery plan. The bar-to-REQ
traceability checked here is one input into SUBTASK_validate-crossrefs's formal cross-reference
pass.

**Dependencies**: none  
**Dependents**: SUBTASK_validate-crossrefs, SUBTASK_synthesis

---

## Inputs

| Input | Location | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Context |
| Contract schema | `../contracts/_MANIFEST.yaml` | Output structure |
| Release bar | `git show work/design-ferric-1_0:design/ferric/release-bar.md` at `/home/user/nswe-demo` | Primary subject (1 of 2) |
| Release plan | `git show work/design-ferric-1_0:design/ferric/release-plan.md` at `/home/user/nswe-demo` | Primary subject (2 of 2) |

---

## What to Validate

For release-bar.md:
- Whether every BAR-FERRIC-* criterion cites at least one REQ-* id (note the REQ ids cited —
  SUBTASK_validate-crossrefs will confirm they exist in the owning documents)
- Whether the usable_early / one_oh staging is clearly defined and criteria are assigned
  to the right stage
- Whether each criterion is testable: a stranger could determine pass or fail

For release-plan.md:
- Whether the epics are ordered in a logical delivery sequence
- Whether the usable_early / one_oh staging is internally consistent with release-bar.md
- Whether the plan references specific issue numbers (or epics) that match the filed issues
  (#129–#136 for epics, #137–#164 for child issues)
- Whether the plan references specific design document sections or REQ-* ids

Cross-document consistency:
- Whether the staging (usable_early / one_oh) is consistent between release-bar.md,
  release-plan.md, and the parent `_GLOBAL.md` issue register

---

## Output

| Attribute | Value |
|---|---|
| Filename | `concern-findings.md` |
| Location | `SUBTASK_validate-plan/` (this workspace) |
| Format | Markdown, per `../contracts/_MANIFEST.yaml` §concern_findings_schema |

Note on req_ids_found: list the REQ-* ids CITED in BAR-FERRIC-* criteria (not all REQ ids from
all documents — those are collected by the individual concern validators).

Required sections: concern_name, document_validated, req_ids_found, status,
specific_issues, gaps (GAP-080 through GAP-089 if any).

---

## Success Criteria

- [ ] Both `release-bar.md` and `release-plan.md` read from branch
- [ ] BAR-FERRIC-* criteria enumerated with their REQ citations noted
- [ ] usable_early / one_oh staging assessed for consistency
- [ ] `concern-findings.md` written with all required sections
