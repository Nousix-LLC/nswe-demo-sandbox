# Task: GitHub Issue Traceability

## Task Specification

**Slug**: SUBTASK_issue-traceability
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-designer

### Objective

Read the nine concern-findings.md files to build the REQ-* inventory, then query all 36
GitHub issues (#129–#164) and check each for REQ-* citations. Flag issues lacking a
requirement reference and significant requirements lacking a corresponding issue. Perform
the special check on issue #137. Produce `issue-traceability.md` conforming to
`../contracts/_MANIFEST.yaml` §issue_traceability_schema.

### Context

Part of the SUBTASK_validate-crossrefs subtree (see `_GLOBAL.md` in the parent workspace).
This task runs in parallel with SUBTASK_req-reconciliation; both read the nine
concern-findings.md files independently. The GitHub repo is `Nousix-LLC/nswe-demo`.
Issues #129–#136 are epics; #137–#164 are child issues (28 total).

**Dependencies**: none (all nine concern-findings.md are already present)  
**Dependents**: SUBTASK_synthesis-crossrefs

---

## Inputs

| Input | Location | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Context |
| Contract | `../contracts/_MANIFEST.yaml` | Output schema |
| All nine concern-findings.md | `../../SUBTASK_validate-*/concern-findings.md` | REQ-* id inventory |
| GitHub issues #129–#164 | `gh issue view <N> --repo Nousix-LLC/nswe-demo` | Issue bodies to check |

---

## What to Produce

### Epic and Child Issue Survey

For each of the 8 epics (#129–#136):
- Read the issue body
- Record the epic title
- List the child issues mentioned or linked
- Note whether the epic body itself references a design document and at least one REQ-* id

For each of the 28 child issues (#137–#164):
- Read the issue body
- Check for at least one REQ-* citation

### Issues Without REQ Citation

List every child issue whose body contains no REQ-* citation. Include issue number and title.

### Requirements Without Issue

Build the REQ-* inventory from the nine concern-findings.md files (same as SUBTASK_req-reconciliation
does, independently). Identify significant REQ-* ids that have no corresponding GitHub issue.
"Significant" means the requirement is in scope for Ferric 1.0 (not explicitly marked deferred
or out-of-scope in the design documents). Use judgment on borderline cases and document the
rationale.

### Issue #137 Special Check

Query issue #137 specifically. Verify:
1. Which epic it is assigned to
2. Whether its title/body scope is correctly bounded relative to the authoring-model concern
   (REQ-API-*) and the async-forms-events concern (REQ-ASYNC-*)
3. Whether there is overlap with either concern or a gap between them

---

## Output

| Attribute | Value |
|---|---|
| Filename | `issue-traceability.md` |
| Location | `SUBTASK_issue-traceability/` (this workspace) |
| Format | Markdown, per `../contracts/_MANIFEST.yaml` §issue_traceability_schema |

Required sections: epics_summary, issues_without_req, requirements_without_issue,
issue_137_check, traceability_status.

---

## Success Criteria

- [ ] All nine concern-findings.md read; REQ inventory built
- [ ] All 36 GitHub issues (#129–#164) queried and checked
- [ ] issues_without_req list complete
- [ ] requirements_without_issue list complete with rationale for "significant" judgment
- [ ] issue_137_check complete
- [ ] `issue-traceability.md` written with all required sections and a traceability_status
