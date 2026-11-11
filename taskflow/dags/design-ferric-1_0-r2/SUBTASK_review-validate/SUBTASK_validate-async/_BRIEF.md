# Task: Validate — Async, Forms & Events

## Task Specification

**Slug**: SUBTASK_validate-async
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-designer

### Objective

Read `async-forms-events.md` on branch `work/design-ferric-1_0`, compare it against the
prior-art draft at `../prior-art/async-forms-events.md`, and produce `concern-findings.md`
conforming to `../contracts/_MANIFEST.yaml` §concern_findings_schema.

### Context

Part of the review-validate subtree (see `_GLOBAL.md` in the parent workspace). The prior-art
file is a reference draft; the branch version should reconcile it.

**Dependencies**: none  
**Dependents**: SUBTASK_validate-crossrefs, SUBTASK_synthesis

---

## Inputs

| Input | Location | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Context |
| Contract schema | `../contracts/_MANIFEST.yaml` | Output structure |
| Design document | `git show work/design-ferric-1_0:design/ferric/async-forms-events.md` at `/home/user/nswe-demo` | Primary subject |
| Prior-art draft | `../prior-art/async-forms-events.md` | Reference to reconcile against |

---

## What to Validate

- Whether the branch version reconciles the prior-art draft
- Whether async resources are addressed with testable requirements
- Whether suspense-style loading and error states are addressed
- Whether two-way form binding is addressed
- Whether full DOM event handling surface is addressed
- Whether requirements are testable by a stranger checking a running framework

---

## Output

| Attribute | Value |
|---|---|
| Filename | `concern-findings.md` |
| Location | `SUBTASK_validate-async/` (this workspace) |
| Format | Markdown, per `../contracts/_MANIFEST.yaml` §concern_findings_schema |

Required sections: concern_name, document_validated, req_ids_found, status,
specific_issues, gaps (GAP-030 through GAP-039 if any).

---

## Success Criteria

- [ ] `async-forms-events.md` read from branch
- [ ] Prior-art draft read and compared
- [ ] All REQ-ASYNC-* ids listed
- [ ] Each validation criterion assessed
- [ ] `concern-findings.md` written with all required sections
