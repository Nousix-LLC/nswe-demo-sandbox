# Task: Validate — REQ Cross-References & Issue Traceability

## Task Specification

**Slug**: SUBTASK_validate-crossrefs
**Task Kind**: standard
**Depends on**: SUBTASK_validate-scope, SUBTASK_validate-ssr, SUBTASK_validate-authoring, SUBTASK_validate-async, SUBTASK_validate-router, SUBTASK_validate-docs, SUBTASK_validate-release, SUBTASK_validate-perf, SUBTASK_validate-plan
**Status**: Pending
**Assigned To**: swe-designer

### Objective

Using the nine concern-findings.md files as the authoritative REQ-* id inventory, perform two
checks: (1) REQ register cross-reference reconciliation across all design documents, and
(2) GitHub issue traceability for issues #129–#164. Produce `crossrefs-findings.md` conforming
to `../contracts/_MANIFEST.yaml` §crossrefs_findings_schema.

### Context

Part of the review-validate subtree (see `_GLOBAL.md` in the parent workspace). This task runs
after all nine per-concern validators complete. It does not re-read design documents from scratch;
it uses the req_ids_found lists from the concern findings plus targeted re-reads for cross-reference
verification.

**Dependencies**: all nine SUBTASK_validate-* tasks  
**Dependents**: SUBTASK_synthesis

---

## Inputs

| Input | Location | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Context, issue register table |
| Contract schema | `../contracts/_MANIFEST.yaml` | Output structure |
| Scope findings | `../SUBTASK_validate-scope/concern-findings.md` | REQ-FW-* id list |
| SSR findings | `../SUBTASK_validate-ssr/concern-findings.md` | REQ-SSR-* id list |
| Authoring findings | `../SUBTASK_validate-authoring/concern-findings.md` | REQ-API-* id list |
| Async findings | `../SUBTASK_validate-async/concern-findings.md` | REQ-ASYNC-* id list |
| Router findings | `../SUBTASK_validate-router/concern-findings.md` | REQ-RT-* and REQ-HTTP-* id lists |
| Docs findings | `../SUBTASK_validate-docs/concern-findings.md` | REQ-DX-* id list |
| Release findings | `../SUBTASK_validate-release/concern-findings.md` | REQ-REL-* id list |
| Perf findings | `../SUBTASK_validate-perf/concern-findings.md` | REQ-PERF-* id list |
| Plan findings | `../SUBTASK_validate-plan/concern-findings.md` | BAR-FERRIC-* → REQ-* citations |
| Design documents | Branch `work/design-ferric-1_0` at `/home/user/nswe-demo` | For targeted cross-reference spot-checks |
| GitHub issues | `gh issue view <N> --repo Nousix-LLC/nswe-demo` | Issues #129–#164 |

---

## What to Validate

### REQ Register Reconciliation

Build the full REQ-* id inventory from the nine concern findings. Then:
- Check for duplicate ids: any REQ-* id that appears in more than one document's req_ids_found list
- Check for orphaned cross-references: for each cross-document REQ-* citation noted by the concern
  validators, confirm the cited id exists in the owning register (spot-check by re-reading the
  relevant design document section)
- Check that every BAR-FERRIC-* criterion (from SUBTASK_validate-plan findings) cites at least
  one REQ-* id that appears in the full inventory

### Issue Traceability

For each epic (#129–#136): read the issue body and verify it references the relevant design
document and at least one REQ-* id.

For each child issue (#137–#164): read the issue body and check for at least one REQ-* citation.

Special check: issue #137 (Reactive state) — confirm its epic assignment and whether it is
correctly scoped relative to the authoring model and async concerns.

Flag:
- Any issue body lacking a clear requirement reference
- Any significant REQ-* requirement that has no corresponding issue

---

## Output

| Attribute | Value |
|---|---|
| Filename | `crossrefs-findings.md` |
| Location | `SUBTASK_validate-crossrefs/` (this workspace) |
| Format | Markdown, per `../contracts/_MANIFEST.yaml` §crossrefs_findings_schema |

Required sections: req_register_reconciliation, issue_traceability, gaps
(GAP-090 through GAP-099 for any additional gaps found).

---

## Success Criteria

- [ ] All nine concern-findings.md read and REQ id inventories aggregated
- [ ] All 36 GitHub issues queried and checked for REQ citations
- [ ] REQ reconciliation complete (clean or with issues flagged)
- [ ] Issue traceability complete (clean or with issues flagged)
- [ ] `crossrefs-findings.md` written with all required sections
