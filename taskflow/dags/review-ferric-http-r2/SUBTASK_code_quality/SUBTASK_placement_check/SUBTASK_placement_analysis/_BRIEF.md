# SUBTASK_placement_analysis: Placement Correctness Analysis

## Task Specification

**Slug**: SUBTASK_placement_analysis
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Assess whether CHANGELOG.md entries added by PR #210 are placed in the correct version
sections. This covers Concern 2 (placement correctness) only. Duplication is handled by
SUBTASK_duplication_analysis.

### Context

Sub-spoke of SUBTASK_placement_check in SUBTASK_code_quality / review-ferric-http-r2.
See `../_GLOBAL.md` for subtree constraints.

PR under review: `work/ferric-http-r1` → `main`, head `0436218`. Includes a remediation
commit on top of original PR changes. Both sets of changes touch CHANGELOG.md.

**Dependents**: SUBTASK_synthesis reads `placement_findings.md`.

---

## Input Specification

| Input | Source |
|-------|--------|
| CHANGELOG.md | `gh api repos/Nousix-LLC/nswe-demo/contents/CHANGELOG.md --jq '.content' \| base64 -d` |
| PR #210 diff | `gh pr diff 210 --repo Nousix-LLC/nswe-demo` |
| PR commit list | `gh pr view 210 --repo Nousix-LLC/nswe-demo --json commits` |
| Subtree hub | `../_GLOBAL.md` |
| Output schema | `../contracts/sub_spoke_findings_schema.yaml` |

---

## Concern Covered

**Concern 2 (placement correctness)**: Are the new entries placed in the correct version
section (the unreleased or relevant version block)? Does the remediation commit add entries
to the right section and not to a released version block? Is the order of version sections
intact (newest first)?

Specific checks:
- Identify the version section structure in CHANGELOG.md (Unreleased header, released
  version headers and their release dates)
- For each new CHANGELOG entry added by PR #210 (original + remediation commits):
  which version section does it land in?
- Are newly added feature/fix entries under [Unreleased] (or the correct version block
  if this PR targets a specific release)?
- Did the remediation commit add any entries in a released version section by mistake?
- Is the version section ordering intact (newest/Unreleased at top, oldest at bottom)?

Rust/signature correctness, formatting style, security, and duplication: out of scope.

---

## Output Specification

**File**: `placement_findings.md`
**Location**: `SUBTASK_placement_analysis/`
**Schema**: `../contracts/sub_spoke_findings_schema.yaml`

Required sections:
- `## Concern Covered` — one line stating "Concern 2 (placement correctness)"
- `## Findings` — findings per schema; at least one CLEAN entry if no defects found

---

## Success Criteria

- [ ] All new CHANGELOG entries assessed for placement correctness
- [ ] Version section ordering verified
- [ ] Remediation commit entries specifically checked for section placement
- [ ] `placement_findings.md` written following `../contracts/sub_spoke_findings_schema.yaml`
- [ ] At least one CLEAN entry if no defects, explicitly naming what was examined

---

## Suggested Methodology Files

**Task-type row (from Domain Mapping):** "Code review" — Primary: Code Review;
Supporting: Core, Operations (Documentation)

Suggested files:
- `code-review/CodeReview_Checklist_Methodology.md` — review checklist approach for
  structural assessment; relevant for evaluating placement discipline
- `operations/BestPractices_Documentation_Methodology.md` — CHANGELOG versioning
  conventions (Keep a Changelog format, semver, Unreleased section usage)

The above are the parent's flagged methodologies. The child agent SHOULD load these as
a starting point but is the final judge of what its work requires — load fewer if some
are clearly inapplicable; load more if the child's own reading of the brief reveals
additional methodology surface the parent did not anticipate.

## Out-of-Scope Methodologies

- `synthesis/Synthesis_Overview_Methodology.md` — synthesis concerns; not applicable here
- Any Rust-specific methodology — Rust/signature correctness is out of scope

---

## Inherited Constraints

- Repo: `Nousix-LLC/nswe-demo`
- Assess only content added or changed by PR #210; use the diff for precision
- Do not expose server addresses, SSH key paths, user names, or internal host paths
  in any artifact
- Rust/signature correctness and security: out of scope
- Duplication: out of scope (SUBTASK_duplication_analysis)
- Formatting style: out of scope (SUBTASK_format_check sibling in parent subtree)
