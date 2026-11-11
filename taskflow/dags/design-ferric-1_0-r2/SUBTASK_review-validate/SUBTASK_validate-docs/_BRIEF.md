# Task: Validate — Documentation & Developer Experience

## Task Specification

**Slug**: SUBTASK_validate-docs
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-designer

### Objective

Read `docs-and-dx.md` on branch `work/design-ferric-1_0` and produce `concern-findings.md`
conforming to `../contracts/_MANIFEST.yaml` §concern_findings_schema.

### Context

Part of the review-validate subtree (see `_GLOBAL.md` in the parent workspace). No prior-art
document exists for this concern — it was designed fresh. Check freshness and completeness.

**Dependencies**: none  
**Dependents**: SUBTASK_validate-crossrefs, SUBTASK_synthesis

---

## Inputs

| Input | Location | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Context |
| Contract schema | `../contracts/_MANIFEST.yaml` | Output structure |
| Design document | `git show work/design-ferric-1_0:design/ferric/docs-and-dx.md` at `/home/user/nswe-demo` | Primary subject |

---

## What to Validate

- Whether a conceptual guide is stated as a 1.0 requirement (not just a wish)
- Whether a start-to-finish tutorial is required, with a stated acceptance bar
- Whether API reference docs are required with a stated scope
- Whether a cargo-generate starter template is addressed
- Whether the DX acceptance bar is stated in terms a newcomer could check (time-to-first-build,
  error message quality, etc.)
- Whether freshness is evident — no stale references to prior framework versions

---

## Output

| Attribute | Value |
|---|---|
| Filename | `concern-findings.md` |
| Location | `SUBTASK_validate-docs/` (this workspace) |
| Format | Markdown, per `../contracts/_MANIFEST.yaml` §concern_findings_schema |

Required sections: concern_name, document_validated, req_ids_found, status,
specific_issues, gaps (GAP-050 through GAP-059 if any).

---

## Success Criteria

- [ ] `docs-and-dx.md` read from branch
- [ ] All REQ-DX-* ids listed
- [ ] Each validation criterion assessed
- [ ] `concern-findings.md` written with all required sections
