# SUBTASK_synthesis: Consolidate CHANGELOG Quality Findings

## Task Specification

**Slug**: SUBTASK_synthesis  
**Task Kind**: standard  
**Depends on**: SUBTASK_format_check, SUBTASK_placement_check, SUBTASK_completeness_check  
**Status**: Pending

### Objective

Produce `code_quality_findings.md` — the final output of the SUBTASK_code_quality task — by consolidating the three partial findings files from the analysis spokes into the structure required by `../../contracts/findings_schema.yaml`.

### Context

This is the synthesis task for the SUBTASK_code_quality subtree. See `../_GLOBAL.md` for subtree structure and `../../_GLOBAL.md` for the full review background.

The three input partial files each follow `../contracts/spoke_partial_schema.yaml`. The final output must follow `../../contracts/findings_schema.yaml` and must cover all five concern areas that the parent SUBTASK_code_quality was asked to assess.

**Dependents**: `SUBTASK_verdict` (in review-ferric-http-r2) reads `code_quality_findings.md`

---

## Input Specification

| Input | Source |
|-------|--------|
| Format and structure findings | `../SUBTASK_format_check/format_review_partial.md` |
| Placement and duplication findings | `../SUBTASK_placement_check/placement_review_partial.md` |
| Completeness findings | `../SUBTASK_completeness_check/completeness_review_partial.md` |
| Output schema | `../../contracts/findings_schema.yaml` |
| Ownership manifest | `../contracts/_MANIFEST.yaml` |
| Subtree context | `../_GLOBAL.md` |

---

## Output Specification

**File**: `code_quality_findings.md`  
**Location**: `SUBTASK_code_quality/` — the PARENT workspace root (one level above this workspace at `../`)  
**Absolute path**: `../code_quality_findings.md` relative to this workspace  
**Schema**: `../../contracts/findings_schema.yaml`

Required sections (per schema):
- `## Summary` — what was checked across all five concern areas; overall result
- `## Findings` — consolidated per-finding entries; where the same item appears in multiple partials, it appears once at the highest severity assigned
- `## Verdict contribution` — APPROVE or REQUEST-CHANGES

Verdict rule: APPROVE is valid only if no BLOCKER findings remain across all three partials.

---

## Success Criteria

- [ ] All five concern areas represented in the consolidated findings
- [ ] Every finding from all three partial files present in the output with no omission
- [ ] Any finding appearing in more than one partial recorded once at the highest assigned severity
- [ ] `code_quality_findings.md` written to `../code_quality_findings.md` following `../../contracts/findings_schema.yaml`

---

## Suggested Methodology Files

**Task-type row (from Domain Mapping):** "Code review" — Primary: Code Review; Supporting: Core

Suggested files:
- `code-review/CodeReview_Checklist_Methodology.md` — provides the review structure for consolidation and verdict assignment

---

## Inherited Constraints

- Repo: `Nousix-LLC/nswe-demo`
- Do not expose server addresses, SSH key paths, user names, or internal host paths in any artifact
