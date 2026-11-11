# Task: Validate — Framework Scope & 1.0 Requirements

## Task Specification

**Slug**: SUBTASK_validate-scope
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-designer

### Objective

Read `scope-and-requirements.md` on branch `work/design-ferric-1_0` of `/home/user/nswe-demo`,
validate it against the criteria below, and produce `concern-findings.md` conforming to the
contract at `../contracts/_MANIFEST.yaml` §concern_findings_schema.

### Context

Part of the review-validate subtree (see `_GLOBAL.md` in the parent workspace). This is one of
nine parallel concern validators. The concern-findings.md produced here is consumed by
SUBTASK_validate-crossrefs and SUBTASK_synthesis.

**Dependencies**: none  
**Dependents**: SUBTASK_validate-crossrefs, SUBTASK_synthesis

---

## Inputs

| Input | Location | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Context, shared inputs reference |
| Contract schema | `../contracts/_MANIFEST.yaml` | Output structure requirements |
| Design document | `git show work/design-ferric-1_0:design/ferric/scope-and-requirements.md` at `/home/user/nswe-demo` | Primary subject of validation |

No prior-art document exists for this concern — the document was designed fresh.

---

## What to Validate

The validation covers:

- Whether every stated requirement is testable: a stranger with no context could read it and
  determine whether the product passes or fails
- Whether the MVP-vs-1.0 line is drawn clearly, with out-of-1.0 items explicitly listed
- Whether cross-references to other REQ-* registers name IDs that actually exist in those
  documents (this is noted for SUBTASK_validate-crossrefs to confirm formally)
- Whether the document is complete: no obvious framework-scope question is left unaddressed
- Consistency with the overall Ferric 1.0 framing (Rust + WebAssembly frontend framework)

---

## Output

| Attribute | Value |
|---|---|
| Filename | `concern-findings.md` |
| Location | `SUBTASK_validate-scope/` (this workspace) |
| Format | Markdown, per `../contracts/_MANIFEST.yaml` §concern_findings_schema |

Required sections: concern_name, document_validated, req_ids_found, status,
specific_issues, gaps (GAP-001 through GAP-009 if any).

---

## Success Criteria

- [ ] `scope-and-requirements.md` read from branch
- [ ] All REQ-FW-* ids listed
- [ ] Each validation criterion assessed
- [ ] `concern-findings.md` written with all required sections
- [ ] Every gap assigned a GAP-NNN id with severity
