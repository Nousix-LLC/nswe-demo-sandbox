# Task: Synthesis — Assemble review-report.md

## Task Specification

**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_validate-crossrefs
**Status**: Pending
**Assigned To**: swe-designer

### Objective

Read all ten findings files (nine concern-findings.md + one crossrefs-findings.md) and assemble
`review-report.md` at the parent workspace (`SUBTASK_review-validate/review-report.md`),
conforming to the parent contract at
`../../contracts/_MANIFEST.yaml` §review_report_schema.

### Context

Part of the review-validate subtree (see `_GLOBAL.md` in the parent workspace). This task is the
synthesis gate: it integrates all prior findings into the single deliverable that SUBTASK_remediate
will act on. The output path is at the parent workspace level, not inside this task's own directory.

SUBTASK_validate-crossrefs depends on all nine concern validators, so by the time this task runs,
all eleven prior outputs are available.

**Dependencies**: SUBTASK_validate-crossrefs (which in turn depends on all nine concern validators)  
**Dependents**: SUBTASK_remediate (via parent contract), SUBTASK_synthesize-root

---

## Inputs

| Input | Location | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Context |
| Parent contract | `../../contracts/_MANIFEST.yaml` | review_report_schema (output structure) |
| Child contract | `../contracts/_MANIFEST.yaml` | concern_findings_schema and crossrefs_findings_schema |
| Scope findings | `../SUBTASK_validate-scope/concern-findings.md` | Concern 1 |
| SSR findings | `../SUBTASK_validate-ssr/concern-findings.md` | Concern 2 |
| Authoring findings | `../SUBTASK_validate-authoring/concern-findings.md` | Concern 3 |
| Async findings | `../SUBTASK_validate-async/concern-findings.md` | Concern 4 |
| Router findings | `../SUBTASK_validate-router/concern-findings.md` | Concern 5 |
| Docs findings | `../SUBTASK_validate-docs/concern-findings.md` | Concern 6 |
| Release findings | `../SUBTASK_validate-release/concern-findings.md` | Concern 7 |
| Perf findings | `../SUBTASK_validate-perf/concern-findings.md` | Concern 8 |
| Plan findings | `../SUBTASK_validate-plan/concern-findings.md` | Concern 9 |
| Cross-refs findings | `../SUBTASK_validate-crossrefs/crossrefs-findings.md` | REQ reconciliation + issue traceability |

---

## What to Produce

Assemble `review-report.md` with the five sections required by the parent contract
(`../../contracts/_MANIFEST.yaml` §review_report_schema):

1. **validation_summary** — one-paragraph overall verdict (complete / mostly-complete / has-gaps)
   grounded in the aggregate status across all nine concerns and the cross-reference check
2. **per_concern_findings** — nine entries, one per concern, drawn from the nine concern-findings.md
   files; preserve the specific issues and gaps found; do not summarize away details
3. **req_register_reconciliation** — drawn from crossrefs-findings.md §req_register_reconciliation;
   list duplicate ids, orphaned references, BAR-FERRIC-* without REQ-* citations
4. **issue_traceability** — drawn from crossrefs-findings.md §issue_traceability; per-epic summary
   with per-issue citation status; include the #137 special check result
5. **gaps_for_remediation** — consolidated and prioritized list of all GAP-NNN items from all ten
   findings files; each item retains its id, description, severity, and action_required

---

## Output

| Attribute | Value |
|---|---|
| Filename | `review-report.md` |
| Location | `../` (the parent workspace: `SUBTASK_review-validate/`) |
| Format | Markdown, per `../../contracts/_MANIFEST.yaml` §review_report_schema |

---

## Success Criteria

- [ ] All ten findings files read
- [ ] `review-report.md` written at `SUBTASK_review-validate/review-report.md`
- [ ] All five required sections present
- [ ] Every GAP-NNN item from all findings included in gaps_for_remediation
- [ ] Validation summary accurately reflects the aggregate status
