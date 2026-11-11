# Task: Validate — SSR + Hydration

## Task Specification

**Slug**: SUBTASK_validate-ssr
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-designer

### Objective

Read `ssr-hydration.md` on branch `work/design-ferric-1_0` and validate it against the
live Ferric codebase (`crates/ferric/` on `main` at HEAD `276138f`). Produce
`concern-findings.md` conforming to `../contracts/_MANIFEST.yaml` §concern_findings_schema.

### Context

Part of the review-validate subtree (see `_GLOBAL.md` in the parent workspace). No prior-art
document for this concern — it was designed fresh.

**Dependencies**: none  
**Dependents**: SUBTASK_validate-crossrefs, SUBTASK_synthesis

---

## Inputs

| Input | Location | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Context |
| Contract schema | `../contracts/_MANIFEST.yaml` | Output structure |
| Design document | `git show work/design-ferric-1_0:design/ferric/ssr-hydration.md` at `/home/user/nswe-demo` | Primary subject |
| Ferric codebase | `crates/ferric/` on `main` at `/home/user/nswe-demo` | Ground truth for accuracy |

---

## What to Validate

- Whether the architecture stated in the document is grounded in the actual Ferric codebase
  at commit `276138f` (the SSR rendering path, the hydration mechanism, the scope isolation)
- Whether "no client-side re-render on hydration" is stated as a testable acceptance criterion
  with observable behaviour a reviewer could check
- Whether state carry across the SSR seam is addressed
- Whether async resource resume on the client is addressed
- Whether this concern is marked as a must-have for 1.0 (not optional)
- Whether the document is complete for a framework that must support server rendering

---

## Output

| Attribute | Value |
|---|---|
| Filename | `concern-findings.md` |
| Location | `SUBTASK_validate-ssr/` (this workspace) |
| Format | Markdown, per `../contracts/_MANIFEST.yaml` §concern_findings_schema |

Required sections: concern_name, document_validated, req_ids_found, status,
specific_issues, gaps (GAP-010 through GAP-019 if any).

---

## Success Criteria

- [ ] `ssr-hydration.md` read from branch
- [ ] Relevant codebase paths checked at commit `276138f`
- [ ] All REQ-SSR-* ids listed
- [ ] Each validation criterion assessed
- [ ] `concern-findings.md` written with all required sections
