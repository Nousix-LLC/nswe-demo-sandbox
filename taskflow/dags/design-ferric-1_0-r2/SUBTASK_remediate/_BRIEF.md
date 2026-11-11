# Task: Ferric 1.0 Design — Gap Remediation

## Task Specification

**Slug**: SUBTASK_remediate
**Task Kind**: standard
**Depends on**: SUBTASK_review-validate
**Status**: Pending
**Assigned To**: swe-designer

### Objective

Read the review report from SUBTASK_review-validate and apply the identified fixes. For each
`GAP-NNN` item in the review report, either fix it (updating design documents, adding or
correcting issues on the board) or confirm it requires no fix. Confirm PR #128 is complete
and ready to merge. Produce a remediation report that SUBTASK_synthesize-root can use to
build the root SYNTHESIS.md.

### Context

This task is part of the design-ferric-1_0-r2 recovery DAG (see `_GLOBAL.md` in the parent workspace).

SUBTASK_review-validate has already read and validated all ten design documents and the backlog. This task
acts on its findings. If the review found everything solid (no `GAP-NNN` items or only minor ones), this
task's job is lightweight: confirm no action is needed and produce the remediation report so the synthesis
can proceed. The work is proportional to what the review found.

**Dependencies**: SUBTASK_review-validate — read `SUBTASK_review-validate/review-report.md` before starting.  
**Dependents**: SUBTASK_synthesize-root (reads this task's remediation report).

---

## Inputs

| Input | Location | Purpose |
|---|---|---|
| Review report | `SUBTASK_review-validate/review-report.md` | Governs what this task must do |
| Design documents | `design/ferric/` on branch `work/design-ferric-1_0` | Subject of any fixes |
| Filed issues | #129–#164 on `Nousix-LLC/nswe-demo` | Subject of any traceability fixes |
| PR | #128 on `Nousix-LLC/nswe-demo` | Confirm completeness |
| Contract schema | `../contracts/_MANIFEST.yaml` | Governs what the remediation report must contain |
| Hub context | `../_GLOBAL.md` | Project constraints |

---

## What to Do

### For each `GAP-NNN` item in the review report

Assess the severity and act:

**Critical gaps** (must fix before synthesis):
- Missing design coverage: write the missing content and commit to `work/design-ferric-1_0`
- Broken requirement traceability: update issue bodies with correct `REQ-*` citations
- Orphaned or duplicate `REQ-*` ids: fix in the owning document and update cross-references

**Major gaps** (fix if possible; note if out of scope):
- Issues without requirement references: add citations to issue bodies
- Design requirements with no issue: file the missing issue under the correct epic
- Stale grounding (references to code that no longer exists as described): update the design doc text

**Minor gaps** (note; fix if trivial):
- Formatting, wording, or labeling inconsistencies
- Issues with weak traceability (present but thin)

### Confirm PR readiness

After applying any fixes:
- Check that PR #128 includes all ten design documents and the contracts
- Check that the PR description accurately reflects the design content
- Update the PR description if it needs a material correction
- If all is well, confirm ready-to-merge in the remediation report

### Constraints on GitHub content

Everything posted to GitHub (issue bodies, PR description updates) names only repository identities
(owner/repo, issue/PR numbers, commits). No attribution trailers. No host, cluster, SSH, path, or system
details. No taskflow-internal paths or IDs.

---

## Output

| Attribute | Value |
|---|---|
| Filename | `remediation-report.md` |
| Location | `SUBTASK_remediate/` (this workspace) |
| Format | Markdown, structured per `../contracts/_MANIFEST.yaml` §remediation_report_schema |

The report must contain these sections (per the contract schema):
- `remediation_summary` — overall result (what was fixed, what was already correct, what was out of scope)
- `actions_taken` — one entry per `GAP-NNN`, with action taken and artifacts modified
- `pr_readiness_verdict` — `ready-to-merge` | `needs-review` | `has-blockers` with rationale
- `synthesis_inputs` — summary for SUBTASK_synthesize-root:
  - `release_bar_summary`: key `BAR-FERRIC-*` criteria (usable_early bar, one_oh bar, must-have criteria)
  - `epic_index`: list of epic numbers with titles and their child issue numbers
  - `pr_number`: 128

---

## Success Criteria

- [ ] All `GAP-NNN` items from review report addressed (fixed or documented as no-fix-needed)
- [ ] All critical gaps resolved before completing this task
- [ ] PR #128 readiness confirmed (or updated)
- [ ] `remediation-report.md` written with all required sections
- [ ] `synthesis_inputs` section complete and accurate (SUBTASK_synthesize-root can build from it directly)
