# Task: Validate — Release & Distribution

## Task Specification

**Slug**: SUBTASK_validate-release
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-designer

### Objective

Read `release-and-distribution.md` on branch `work/design-ferric-1_0`, compare it against the
prior-art draft at `../prior-art/release-and-distribution.md`, and produce `concern-findings.md`
conforming to `../contracts/_MANIFEST.yaml` §concern_findings_schema.

### Context

Part of the review-validate subtree (see `_GLOBAL.md` in the parent workspace).

**Dependencies**: none  
**Dependents**: SUBTASK_validate-crossrefs, SUBTASK_synthesis

---

## Inputs

| Input | Location | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Context |
| Contract schema | `../contracts/_MANIFEST.yaml` | Output structure |
| Design document | `git show work/design-ferric-1_0:design/ferric/release-and-distribution.md` at `/home/user/nswe-demo` | Primary subject |
| Prior-art draft | `../prior-art/release-and-distribution.md` | Reference to reconcile against |

---

## What to Validate

- Whether the branch version reconciles the prior-art draft
- Whether crates.io metadata requirements are stated and testable (name, description, keywords,
  license, repository URL, documentation URL)
- Whether a semver policy is stated with clear rules for what constitutes a breaking change
- Whether a changelog format is required (Keep a Changelog 1.1.0 or equivalent)
- Whether multi-crate workspace versioning is addressed (whether all ferric-* crates must
  version-lock or whether independent versioning is permitted)
- Whether requirements are testable

---

## Output

| Attribute | Value |
|---|---|
| Filename | `concern-findings.md` |
| Location | `SUBTASK_validate-release/` (this workspace) |
| Format | Markdown, per `../contracts/_MANIFEST.yaml` §concern_findings_schema |

Required sections: concern_name, document_validated, req_ids_found, status,
specific_issues, gaps (GAP-060 through GAP-069 if any).

---

## Success Criteria

- [ ] `release-and-distribution.md` read from branch
- [ ] Prior-art draft read and compared
- [ ] All REQ-REL-* ids listed
- [ ] Each validation criterion assessed
- [ ] `concern-findings.md` written with all required sections
