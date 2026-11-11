# Task: Validate — Router + HTTP/JSON Client

## Task Specification

**Slug**: SUBTASK_validate-router
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-designer

### Objective

Read `router-and-http.md` on branch `work/design-ferric-1_0`, compare it against the prior-art
drafts at `../prior-art/router-and-http.md` and `../prior-art/router-and-http.SYNTHESIS.md`,
and produce `concern-findings.md` conforming to `../contracts/_MANIFEST.yaml` §concern_findings_schema.

### Context

Part of the review-validate subtree (see `_GLOBAL.md` in the parent workspace). The prior-art
files represent earlier design thinking; the branch version is additive over the surfaces already
landed in issues #5 and #6.

**Dependencies**: none  
**Dependents**: SUBTASK_validate-crossrefs, SUBTASK_synthesis

---

## Inputs

| Input | Location | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Context |
| Contract schema | `../contracts/_MANIFEST.yaml` | Output structure |
| Design document | `git show work/design-ferric-1_0:design/ferric/router-and-http.md` at `/home/user/nswe-demo` | Primary subject |
| Prior-art draft | `../prior-art/router-and-http.md` | Reference to reconcile against |
| Prior-art synthesis | `../prior-art/router-and-http.SYNTHESIS.md` | Synthesis of prior-art thinking |

---

## What to Validate

- Whether the branch version is clearly additive over the surfaces already landed in issues #5/#6
  (no duplication, no contradiction)
- Whether the branch version reconciles the prior-art drafts without dropping content
- Whether nested routes are addressed with testable requirements
- Whether route parameters are addressed
- Whether active-link state is addressed
- Whether typed JSON request/response is addressed
- Whether per-request timeouts are addressed
- Whether requirements use REQ-RT-* and REQ-HTTP-* prefixes correctly (no mixing)

---

## Output

| Attribute | Value |
|---|---|
| Filename | `concern-findings.md` |
| Location | `SUBTASK_validate-router/` (this workspace) |
| Format | Markdown, per `../contracts/_MANIFEST.yaml` §concern_findings_schema |

Required sections: concern_name, document_validated, req_ids_found, status,
specific_issues, gaps (GAP-040 through GAP-049 if any).

---

## Success Criteria

- [ ] `router-and-http.md` read from branch
- [ ] Prior-art drafts read and compared
- [ ] All REQ-RT-* and REQ-HTTP-* ids listed
- [ ] Each validation criterion assessed
- [ ] `concern-findings.md` written with all required sections
