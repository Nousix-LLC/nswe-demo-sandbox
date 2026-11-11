# Task: Produce partial_findings.md from Prior Concern 7 Analysis

## Task Specification

**Slug**: SUBTASK_produce_partial_findings
**Task Kind**: synthesis
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Read the completed analysis in `../findings_concern7.md` (produced by a prior atomic execution of the parent task), verify that every finding conforms to `../../contracts/findings_format.md`, reformat as `../partial_findings.md` with the correct section headers, then write `../SYNTHESIS.md` as the fold record and call `engine_resume_suspended` to fold the parent (`SUBTASK_concern7_api_stability`) from SUSPENDED → COMPLETED.

### Context

The parent task (`SUBTASK_concern7_api_stability`) declared `NeedsDecompose`. A prior atomic execution already analyzed PR #193's API stability in full and wrote `../findings_concern7.md`. That file contains 6 findings (C7-1 through C7-6) covering all three sub-questions: `EventHandler` backward compatibility, `on_input_event_handler()` documentation/naming, and `create_resource` naming conventions.

Your job is to reformat and validate that prior analysis into the declared output format, then complete the fold.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Prior findings | `../findings_concern7.md` | The analysis to reformat and validate |
| Findings format contract | `../../contracts/findings_format.md` | Required output schema for `partial_findings.md` |
| Parent hub | `../_GLOBAL.md` | Inherited constraints, success criteria, identities |

---

## Review Scope (Validation, Not Re-analysis)

Validate that `../findings_concern7.md` satisfies all of these before writing the output:

1. **EventHandler backward compatibility** (C7-1, C7-2): Both should be `clean`. The `VElement::on()` method signature must be verified unchanged; the type alias → enum change must not break prelude callers.

2. **`on_input_event_handler()` on `Bind<T>`** (C7-4): Should be `clean` (documented, `wasm32`-gated, tested).

3. **`create_resource` naming** (C7-5): Should be `clean` (follows `create_*` convention).

4. **Non-blockers**: C7-3 (`EventHandler` not in prelude alongside `Bind`) and C7-6 (`#[non_exhaustive]` missing) should be present and correctly severity-rated.

5. **No re-raises of #196–#201**: Confirm none of the findings duplicate the already-filed issues.

---

## Output Specification

**Primary Output 1:** `partial_findings.md` at the **parent workspace root** (`../partial_findings.md`)
- Must have `## Findings` as the section header (not `## Findings — Concern 7 (...)`)
- Must have `## What was examined` as the examination section header
- All findings must use `concern: api-stability`
- Severity values from `{blocker, non-blocker, clean}`
- Repository-relative paths only
- Must conform to `../../contracts/findings_format.md`

**Terminal Record:** `../SYNTHESIS.md` at the parent workspace root (fold record)
- Write this as the synthesis terminal record before calling `engine_resume_suspended`
- Report `artifact_path: "../SYNTHESIS.md"` on the terminal `engine_report_status`
- After writing both files and reporting `status: completed`, call `engine_resume_suspended` to fold the parent

**Output contract (`engine_report_status` outputs field):**
- `outputs: ["<abs_path_to_partial_findings.md>"]`
- `artifact_path: "<abs_path_to_SYNTHESIS.md>"`

---

## Synthesis Terminal Sequence

This is a synthesis task (kind: synthesis). The correct terminal sequence is:

1. Write `../partial_findings.md` (the declared output) via `engine_write`
2. Write `../SYNTHESIS.md` (the fold record) via `engine_write`
3. Call `engine_report_status { status: "completed", outputs: ["<abs>/partial_findings.md"], artifact_path: "<abs>/SYNTHESIS.md", decompose_evaluation: "Atomic" }`
4. Call `engine_resume_suspended { target_task_id: "<parent_task_id>", synthesized_task_id: "<my_task_id>", seam_path: "<abs>/SYNTHESIS.md" }`

---

## Suggested Methodology Files

Task-type row (Domain Mapping): **Ferric PR review (Rust library)** → Primary: `code-review`, Supporting: `rust`, `framework-design`

Specific files:
- `code-review/CodeReview_Checklist_Methodology.md` — provides the structural frame for evaluating API stability findings; rationale: validating that the prior findings cover all required API review gates.
- `synthesis/Synthesis_Overview_Methodology.md` — synthesis gate contract; rationale: this is a synthesis task that must verify findings against the contract before combining.
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify findings conform to the findings_format.md contract; rationale: the output must mechanically conform to the declared schema.

These are SUGGESTIONS. Load fewer if some are clearly inapplicable; load more if needed.

---

## Inherited Constraints

- Repository-relative paths only in all findings
- Issues #196–#201 MUST NOT be re-raised
- Severity `blocker` only if `EventHandler` redesign breaks existing callers; `non-blocker` for missing documentation or naming inconsistencies
- Concerns 1–6 are out of scope; this task covers only Concern 7 (API and contract stability)
- `concern` label must be `api-stability` for all findings

---

## Success Criteria

- [ ] `../partial_findings.md` exists with correct section headers (`## Findings`, `## What was examined`)
- [ ] All 6 findings (or subset, if any do not apply) validated and reformatted
- [ ] `../SYNTHESIS.md` exists as fold record
- [ ] `engine_resume_suspended` called to fold parent SUSPENDED → COMPLETED
