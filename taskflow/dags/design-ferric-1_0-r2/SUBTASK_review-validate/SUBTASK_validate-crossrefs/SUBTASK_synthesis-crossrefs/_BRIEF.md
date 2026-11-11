# Task: Synthesis — Assemble crossrefs-findings.md

## Task Specification

**Slug**: SUBTASK_synthesis-crossrefs
**Task Kind**: synthesis
**Depends on**: SUBTASK_req-reconciliation, SUBTASK_issue-traceability
**Status**: Pending
**Assigned To**: swe-designer

### Objective

Read the two intermediate outputs (`req-reconciliation.md` and `issue-traceability.md`),
assemble `crossrefs-findings.md` conforming to `../../contracts/_MANIFEST.yaml`
§crossrefs_findings_schema (the parent contract), assign any additional gap ids in the
range GAP-090 through GAP-099, and write `SYNTHESIS.md` to fold this subtree.

### Context

Part of the SUBTASK_validate-crossrefs subtree (see `_GLOBAL.md` in the parent workspace).
This synthesis task is the gate for its two sibling spokes. Its output (`crossrefs-findings.md`)
is consumed by the parent's synthesis task (SUBTASK_synthesis).

The final `crossrefs-findings.md` must be written at the SUBTASK_validate-crossrefs level
(i.e., the parent of this task's workspace), not inside this task's own directory. This matches
the parent contract ownership declaration: `artifact: SUBTASK_validate-crossrefs/crossrefs-findings.md`.

**Dependencies**: SUBTASK_req-reconciliation, SUBTASK_issue-traceability  
**Dependents**: none within this subtree (SUBTASK_synthesis in the parent subtree depends on it)

---

## Inputs

| Input | Location | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Context |
| Parent contract | `../../contracts/_MANIFEST.yaml` §crossrefs_findings_schema | Output structure |
| This subtree's contract | `../contracts/_MANIFEST.yaml` | Identities to verify |
| REQ reconciliation | `../SUBTASK_req-reconciliation/req-reconciliation.md` | Reconciliation findings |
| Issue traceability | `../SUBTASK_issue-traceability/issue-traceability.md` | Traceability findings |

---

## What to Produce

### crossrefs-findings.md

Assemble the three sections required by `../../contracts/_MANIFEST.yaml` §crossrefs_findings_schema:

1. **req_register_reconciliation** — drawn from `req-reconciliation.md`:
   - duplicate_ids: list (or "none")
   - orphaned_references: list (or "none")
   - bar_without_req: list (or "none")
   - Status: clean | has-issues

2. **issue_traceability** — drawn from `issue-traceability.md`:
   - epics_summary table
   - issues_without_req list
   - requirements_without_issue list
   - issue_137_check
   - Status: clean | has-issues

3. **gaps** — any additional gaps found during cross-reference checking that did not appear in
   the nine concern-findings.md files. Assign ids in the range GAP-090 through GAP-099.
   If no new gaps, state "No additional gaps found."

Verify the identities from `../contracts/_MANIFEST.yaml`:
- All GAP-NNN ids are in range 090–099 and do not duplicate ids from concern-findings.md files
- crossrefs-findings.md contains all three required sections

Write `crossrefs-findings.md` to `../crossrefs-findings.md` (one level up from this workspace,
which places it at `SUBTASK_validate-crossrefs/crossrefs-findings.md`).

### SYNTHESIS.md

Write `SYNTHESIS.md` to `../SYNTHESIS.md` (the fold location — the SUBTASK_validate-crossrefs
workspace directory). Record: what was synthesized, identities verified, any issues found.

---

## Output

| Attribute | Value |
|---|---|
| crossrefs-findings.md | `../crossrefs-findings.md` (SUBTASK_validate-crossrefs level) |
| SYNTHESIS.md | `../SYNTHESIS.md` (SUBTASK_validate-crossrefs level — fold location) |
| Format | Markdown |

---

## Success Criteria

- [ ] `req-reconciliation.md` and `issue-traceability.md` both read
- [ ] `crossrefs-findings.md` written with all three required sections conforming to parent schema
- [ ] All GAP ids in range 090–099 and unique across all findings
- [ ] Contract identities verified (no silent failures)
- [ ] `SYNTHESIS.md` written at the fold location recording how the subtree resolved
