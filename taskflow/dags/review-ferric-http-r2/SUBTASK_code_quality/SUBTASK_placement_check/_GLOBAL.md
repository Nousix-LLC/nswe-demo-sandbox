# SUBTASK_placement_check: Placement and Duplication Analysis Hub

## Project Context

**Status**: Active

### Objective

This decomposition splits the two concern areas of SUBTASK_placement_check into focused
single-concern sub-tasks and a synthesis gate:

- **SUBTASK_placement_analysis** — Concern 2 (placement correctness)
- **SUBTASK_duplication_analysis** — Concern 3 (duplication)
- **SUBTASK_synthesis** — combines both sub-spoke outputs into `placement_review_partial.md`
  and folds the parent (SUBTASK_placement_check) SUSPENDED→COMPLETED via SYNTHESIS.md

### Scope

**In Scope:**
- Concern 2: placement correctness — are CHANGELOG entries in the correct version sections?
- Concern 3: duplication — does the same content appear more than once?

**Out of Scope:**
- Rust/signature correctness (sibling spoke SUBTASK_correctness in parent DAG)
- Formatting style (sibling SUBTASK_format_check)
- Security findings (sibling SUBTASK_security in parent DAG)
- Documentation completeness (sibling SUBTASK_completeness_check)

### Success Criteria

- [ ] Concern 2 (placement correctness) assessed with explicit findings or CLEAN entries
- [ ] Concern 3 (duplication) assessed with explicit findings or CLEAN entries
- [ ] `placement_review_partial.md` written at the SUBTASK_placement_check workspace root,
      following `../contracts/spoke_partial_schema.yaml`
- [ ] `SYNTHESIS.md` written at this workspace root; parent SUSPENDED→COMPLETED via fold

---

## Shared Inputs (all sub-tasks read these)

| Input | How to retrieve |
|-------|----------------|
| CHANGELOG.md | `gh api repos/Nousix-LLC/nswe-demo/contents/CHANGELOG.md --jq '.content' \| base64 -d` |
| PR #210 diff | `gh pr diff 210 --repo Nousix-LLC/nswe-demo` |
| PR commit list | `gh pr view 210 --repo Nousix-LLC/nswe-demo --json commits` |
| Parent partial schema | `../contracts/spoke_partial_schema.yaml` |
| Sub-spoke schema | `contracts/sub_spoke_findings_schema.yaml` (this level) |

---

## Task Structure

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_placement_analysis` | none | Check placement correctness (Concern 2) | `SUBTASK_placement_analysis/placement_findings.md` |
| `SUBTASK_duplication_analysis` | none | Check for duplication (Concern 3) | `SUBTASK_duplication_analysis/duplication_findings.md` |
| `SUBTASK_synthesis` | `SUBTASK_placement_analysis`, `SUBTASK_duplication_analysis` | Gate + produce `placement_review_partial.md`; fold parent | `placement_review_partial.md`, `SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_placement_analysis  ──┐
                               ├── SUBTASK_synthesis
SUBTASK_duplication_analysis ──┘
```

---

## Contract

**Contract location**: `contracts/`
**Contract kind**: `yaml_schema`

Extends the ancestor contract at `../contracts/spoke_partial_schema.yaml` (which defines
the final `placement_review_partial.md` shape). Does NOT override or redefine it.

---

## Subtree Methodology Posture

**Dominant task type:** Code review (CHANGELOG.md quality assessment)
**Primary bundles:** Code Review, Operations (Documentation)
**Cross-cutting methodology:** `code-review/CodeReview_Checklist_Methodology.md`,
`operations/BestPractices_Documentation_Methodology.md`

Descendant agents retain final judgment over what they load.

---

## Subtree-Wide Constraints

- Repo: `Nousix-LLC/nswe-demo`
- Assess only content added or changed by PR #210; use the diff for precision
- Do not expose server addresses, SSH key paths, user names, or internal host paths in any artifact
- Rust/signature correctness and security: out of scope for this subtree
