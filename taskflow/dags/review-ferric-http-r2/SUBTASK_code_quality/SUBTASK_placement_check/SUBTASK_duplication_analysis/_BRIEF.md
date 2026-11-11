# SUBTASK_duplication_analysis: Duplication Analysis

## Task Specification

**Slug**: SUBTASK_duplication_analysis
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Assess whether CHANGELOG.md entries added by PR #210 are duplicated — same content
appearing more than once, or entries from the original PR changes and the remediation
commit that contradict or duplicate each other. This covers Concern 3 (duplication) only.
Placement correctness is handled by SUBTASK_placement_analysis.

### Context

Sub-spoke of SUBTASK_placement_check in SUBTASK_code_quality / review-ferric-http-r2.
See `../_GLOBAL.md` for subtree constraints.

PR under review: `work/ferric-http-r1` → `main`, head `0436218`. Includes a remediation
commit on top of original PR changes. Both sets of changes touch CHANGELOG.md. The
two-commit history is relevant: the original PR commit and the remediation commit may
introduce entries that duplicate or contradict each other.

**Dependents**: SUBTASK_synthesis reads `duplication_findings.md`.

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

**Concern 3 (duplication)**: Are there duplicate entries — the same method or type
documented twice under the same version? Do the original PR changes and the remediation
commit introduce entries that contradict or duplicate each other? Does any entry appear
under more than one version section?

Specific checks:
- For each new CHANGELOG entry added by PR #210: does it appear verbatim or near-verbatim
  elsewhere in CHANGELOG.md (within the same version section, or in a different section)?
- Do the two sets of changes (original PR commits vs remediation commit) add entries that
  describe the same feature or fix in overlapping or contradictory ways?
- After applying the full PR diff, does any entry appear under more than one version section?
- Are there near-duplicate entries that describe the same thing with minor wording variation?

Rust/signature correctness, formatting style, security, and placement correctness: out of scope.

---

## Output Specification

**File**: `duplication_findings.md`
**Location**: `SUBTASK_duplication_analysis/`
**Schema**: `../contracts/sub_spoke_findings_schema.yaml`

Required sections:
- `## Concern Covered` — one line stating "Concern 3 (duplication)"
- `## Findings` — findings per schema; at least one CLEAN entry if no defects found

---

## Success Criteria

- [ ] All new CHANGELOG entries checked for duplication within their section
- [ ] Cross-section duplication checked (same entry in multiple version sections)
- [ ] Cross-commit duplication checked (original PR vs remediation commit)
- [ ] Near-duplicate/contradictory entries assessed
- [ ] `duplication_findings.md` written following `../contracts/sub_spoke_findings_schema.yaml`
- [ ] At least one CLEAN entry if no defects, explicitly naming what was examined

---

## Suggested Methodology Files

**Task-type row (from Domain Mapping):** "Code review" — Primary: Code Review;
Supporting: Core, Operations (Documentation)

Suggested files:
- `code-review/CodeReview_Checklist_Methodology.md` — review checklist approach for
  identifying content problems like duplication and contradiction
- `operations/BestPractices_Documentation_Methodology.md` — CHANGELOG conventions
  (Keep a Changelog; each entry should appear once and in the correct section)

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
- Placement correctness: out of scope (SUBTASK_placement_analysis)
- Formatting style: out of scope (SUBTASK_format_check sibling in parent subtree)
