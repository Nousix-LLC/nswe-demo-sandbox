# Task: Validate — Authoring Model

## Task Specification

**Slug**: SUBTASK_validate-authoring
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-designer

### Objective

Read `authoring-model.md` on branch `work/design-ferric-1_0`, compare it against the prior-art
draft at `../prior-art/authoring-model.md`, and produce `concern-findings.md` conforming to
`../contracts/_MANIFEST.yaml` §concern_findings_schema.

### Context

Part of the review-validate subtree (see `_GLOBAL.md` in the parent workspace). The prior-art
file is a reference draft; the branch version should reconcile it (carry forward its content,
address its open questions, or explicitly supersede it with rationale).

**Dependencies**: none  
**Dependents**: SUBTASK_validate-crossrefs, SUBTASK_synthesis

---

## Inputs

| Input | Location | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Context |
| Contract schema | `../contracts/_MANIFEST.yaml` | Output structure |
| Design document | `git show work/design-ferric-1_0:design/ferric/authoring-model.md` at `/home/user/nswe-demo` | Primary subject |
| Prior-art draft | `../prior-art/authoring-model.md` | Reference to reconcile against |

---

## What to Validate

- Whether the branch version reconciles the prior-art draft (nothing important dropped without
  rationale, open questions resolved or noted)
- Whether `view!` macro surface is given testable requirements
- Whether props, children, and named slots are each given testable requirements
- Whether context and dependency injection are addressed
- Whether component type-level diagnostics are addressed
- Whether requirements are stated in terms a stranger could check against a running framework

---

## Output

| Attribute | Value |
|---|---|
| Filename | `concern-findings.md` |
| Location | `SUBTASK_validate-authoring/` (this workspace) |
| Format | Markdown, per `../contracts/_MANIFEST.yaml` §concern_findings_schema |

Required sections: concern_name, document_validated, req_ids_found, status,
specific_issues, gaps (GAP-020 through GAP-029 if any).

---

## Success Criteria

- [ ] `authoring-model.md` read from branch
- [ ] Prior-art draft read and compared
- [ ] All REQ-API-* ids listed
- [ ] Each validation criterion assessed
- [ ] `concern-findings.md` written with all required sections
