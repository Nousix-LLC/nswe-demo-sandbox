# Synthesis: Assemble Code Quality Findings — PR #228

## Task Specification

**Slug**: SUBTASK_synthesis_cq
**Task Kind**: synthesis
**Depends on**: SUBTASK_A_api_surface, SUBTASK_B_abstraction, SUBTASK_C_error_handling, SUBTASK_D_function_design, SUBTASK_E_test_coverage, SUBTASK_F_documentation
**Status**: Pending

### Objective

Read the six completed area finding files and assemble them into the single `code_quality_findings.md` deliverable declared by the parent task (SUBTASK_code_quality). Verify the contract identities hold before assembling. Produce the final output at the declared path.

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Hub | `../_GLOBAL.md` | PR coordinates, citation constraints, output path |
| Contract manifest | `../contracts/_MANIFEST.yaml` | Ownership and identity assertions to verify |
| Findings schema | `../contracts/findings_schema.yaml` | Schema each area file must conform to |
| Area A findings | `../SUBTASK_A_api_surface/area_a_api_surface.md` | API surface and naming findings |
| Area B findings | `../SUBTASK_B_abstraction/area_b_abstraction.md` | Abstraction boundary findings |
| Area C findings | `../SUBTASK_C_error_handling/area_c_error_handling.md` | Error handling findings |
| Area D findings | `../SUBTASK_D_function_design/area_d_function_design.md` | Function design findings |
| Area E findings | `../SUBTASK_E_test_coverage/area_e_test_coverage.md` | Test coverage findings |
| Area F findings | `../SUBTASK_F_documentation/area_f_documentation.md` | Documentation findings |

---

## Contract Verification (Pre-Assembly Gate)

Before assembling, verify the contract identities from `_MANIFEST.yaml`:

1. Every area file exists and has exactly one verdict (CLEAN, FINDING (NON-BLOCKER), or FINDING (BLOCKER))
2. Every FINDING verdict includes at least one citation with a repository-relative path and line number
3. Every area file has a non-empty "What Was Checked" section
4. No finding cites #225 / REQ-SSR-007 as a code quality finding

If any identity fails, report it as a structured failure in the output (do not silently plug it).

---

## Review Scope

This is the assembly and gate task. Its own work is:
- Verifying the contract identities above
- Assembling the six area sections into `code_quality_findings.md` following the declared output structure
- Writing a one-paragraph overall summary that characterizes the code quality of the PR as a whole, drawing on the six area verdicts
- Not re-reviewing code; not second-guessing area findings; not introducing new findings not backed by the area files

---

## Output

| Attribute | Value |
|-----------|-------|
| File | `code_quality_findings.md` |
| Location | parent workspace (`../code_quality_findings.md` relative to this task, i.e., `SUBTASK_code_quality/code_quality_findings.md`) |

### Output Structure

```markdown
# PR #228 Code Quality and Design Findings

## Summary
<one-paragraph assessment of code quality overall, based on the six area verdicts>

## Findings by Area

### A. API surface and naming
**Status**: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
**What was checked**: ...
**Evidence**: ...
**Finding** (if any): ...

### B. Abstraction boundaries
...

### C. Error handling
...

### D. Function size, duplication, extensibility
...

### E. Test coverage
...

### F. Documentation
...
```

---

## Success Criteria

- All six area files pass the contract identity checks before assembly
- `code_quality_findings.md` exists at `SUBTASK_code_quality/code_quality_findings.md` before this task reports completed
- The file contains sections A through F, each with a named verdict
- The summary characterizes the overall quality faithfully, without inflating or minimizing the area verdicts
- Any failed identity check is reported explicitly in the output rather than silently resolved

## Inherited Constraints

- Read-only: do not modify source code or the area finding files
- Citations carry through from the area files unchanged — do not alter file paths or line numbers
- #225 / REQ-SSR-007 is not a code quality finding; remove any such citation found in area files before assembly and note the removal
- Non-blockers are faithfully carried through for the outer synthesis to track
