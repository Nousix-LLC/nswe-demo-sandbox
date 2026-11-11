# SUBTASK_placement_check: Placement and Duplication Review

## Task Specification

**Slug**: SUBTASK_placement_check  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending

### Objective

Assess placement correctness and duplication in the CHANGELOG.md additions of PR #210 of Nousix-LLC/nswe-demo. Two concern areas: whether entries appear in the correct version section, and whether the same content appears more than once.

### Context

This is an analysis spoke in the SUBTASK_code_quality subtree. See `../_GLOBAL.md` for subtree constraints and `../../_GLOBAL.md` for full review background.

The PR under review (`work/ferric-http-r1` → `main`, head `0436218`) includes a remediation commit on top of the original PR changes. Both sets of changes touch CHANGELOG.md. That history is relevant for duplication assessment.

**Dependents**: `SUBTASK_synthesis` reads `placement_review_partial.md`

---

## Input Specification

| Input | Source |
|-------|--------|
| CHANGELOG.md | repo root (`Nousix-LLC/nswe-demo`, e.g. `gh api repos/Nousix-LLC/nswe-demo/contents/CHANGELOG.md --jq '.content' \| base64 -d`) |
| PR #210 diff | `gh pr diff 210 --repo Nousix-LLC/nswe-demo` |
| PR commit list | `gh pr view 210 --repo Nousix-LLC/nswe-demo --json commits` |
| Output schema | `../contracts/spoke_partial_schema.yaml` |
| Subtree context | `../_GLOBAL.md` |

---

## Concern Areas

**Placement correctness** (concern 2 from parent brief): Are the new entries placed in the correct version section (the unreleased or relevant version block)? Does the remediation commit add entries to the right section and not to a released version block? Is the order of version sections intact (newest first)?

**Duplication** (concern 3 from parent brief): Are there duplicate entries — the same method or type documented twice under the same version? Do the original PR changes and the remediation commit introduce entries that contradict or duplicate each other? Does any entry appear under more than one version section?

Rust/signature correctness, formatting style, and security are out of scope for this spoke; see `../_GLOBAL.md`.

---

## Output Specification

**File**: `placement_review_partial.md`  
**Location**: `SUBTASK_placement_check/`  
**Schema**: `../contracts/spoke_partial_schema.yaml`

Required sections (per schema):
- `## Concerns Covered`
- `## Summary`
- `## Findings`

---

## Success Criteria

- [ ] Both concern areas assessed with explicit findings or CLEAN entries
- [ ] `placement_review_partial.md` written following `../contracts/spoke_partial_schema.yaml`

---

## Suggested Methodology Files

**Task-type row (from Domain Mapping):** "Code review" — Primary: Code Review; Supporting: Core, Documentation

Suggested files:
- `code-review/CodeReview_Checklist_Methodology.md` — review checklist; structural placement dimensions
- `operations/BestPractices_Documentation_Methodology.md` — CHANGELOG versioning conventions

---

## Inherited Constraints

- Repo: `Nousix-LLC/nswe-demo`
- Assess only content added or changed by PR #210; use the diff for precision
- Rust/signature correctness and security: out of scope (see `../_GLOBAL.md`)
- Do not expose server addresses, SSH key paths, user names, or internal host paths in any artifact
