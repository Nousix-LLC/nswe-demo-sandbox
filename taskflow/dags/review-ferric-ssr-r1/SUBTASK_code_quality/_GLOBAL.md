# PR #228 Code Quality Review — Subtree Hub

## Project Context

**Status**: Active
**Parent task**: SUBTASK_code_quality (review-ferric-ssr-r1 DAG)

### Objective

Review PR #228 (`work/ferric-ssr-r1`, repo `Nousix-LLC/nswe-demo`) for code quality across six distinct areas: API surface and naming, abstraction boundaries, error handling, function size/duplication/extensibility, test coverage, and documentation. Each area is reviewed independently; a synthesis task assembles all six section files into the final `code_quality_findings.md` deliverable.

### Scope

**In Scope:**
- Area A: API surface and naming (`render_to_string`, `hydrate`, Axum integration exports)
- Area B: Abstraction boundaries (SSR vs client-side separation, cfg/feature gates)
- Area C: Error handling (Result types, panic-safety, `unwrap`/`expect` in new code)
- Area D: Function size, duplication, extensibility seams
- Area E: Test coverage (against #223, #224, #226 acceptance criteria, edge cases, assertion quality)
- Area F: Documentation (pub API doc comments, examples, caveats)

**Out of Scope:**
- #225 / REQ-SSR-007 (not a code quality finding for this PR — inherited non-goal)
- Modifying source code (read-only review)

### Success Criteria

- [ ] Every area file exists at its declared path before synthesis runs
- [ ] Every area has exactly one verdict (CLEAN, FINDING (NON-BLOCKER), or FINDING (BLOCKER))
- [ ] Every FINDING cites file and line number in `Nousix-LLC/nswe-demo`
- [ ] `code_quality_findings.md` exists at `SUBTASK_code_quality/code_quality_findings.md`

---

## PR Coordinates

| Attribute | Value |
|-----------|-------|
| PR number | 228 |
| Repository | `Nousix-LLC/nswe-demo` |
| Branch | `work/ferric-ssr-r1` |
| Fetch diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` |
| Primary crate under review | `crates/ferric/` |
| Issues referenced | #223, #224, #226 (acceptance criteria); #225 / REQ-SSR-007 (out-of-scope non-goal) |

---

## Shared Inputs

Every spoke reads the PR diff and relevant source files from the branch:

```bash
gh pr diff 228 --repo Nousix-LLC/nswe-demo
gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric --ref work/ferric-ssr-r1
```

---

## Inherited Constraints

- **Non-goal**: #225 / REQ-SSR-007 is not a code quality finding for this PR
- **Read-only**: Do not modify source code
- **Line citations**: All findings cite repository-relative file paths and line numbers in `Nousix-LLC/nswe-demo`, never host filesystem paths
- **Non-blockers**: Flag them; the outer synthesis (SUBTASK_synthesis in the parent DAG) will file them as issues

---

## Contract

**Contract location**: `contracts/` (read-only for all descendants)
**Contract kind**: `taxonomy`

Structural seam: every spoke produces one area finding file (`area_<letter>_<name>.md`) conforming to `contracts/findings_schema.yaml`. The synthesis task (`SUBTASK_synthesis_cq`) assembles all six into `code_quality_findings.md`.

---

## Task Structure

```
_GLOBAL.md (this document)
├── contracts/
│   ├── _MANIFEST.yaml
│   └── findings_schema.yaml
├── SUBTASK_A_api_surface/_BRIEF.md      → area_a_api_surface.md
├── SUBTASK_B_abstraction/_BRIEF.md      → area_b_abstraction.md
├── SUBTASK_C_error_handling/_BRIEF.md   → area_c_error_handling.md
├── SUBTASK_D_function_design/_BRIEF.md  → area_d_function_design.md
├── SUBTASK_E_test_coverage/_BRIEF.md    → area_e_test_coverage.md
├── SUBTASK_F_documentation/_BRIEF.md   → area_f_documentation.md
└── SUBTASK_synthesis_cq/_BRIEF.md       → code_quality_findings.md
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_A_api_surface` | none | Review API surface and naming | `SUBTASK_A_api_surface/area_a_api_surface.md` |
| `SUBTASK_B_abstraction` | none | Review abstraction boundaries | `SUBTASK_B_abstraction/area_b_abstraction.md` |
| `SUBTASK_C_error_handling` | none | Review error handling | `SUBTASK_C_error_handling/area_c_error_handling.md` |
| `SUBTASK_D_function_design` | none | Review function size, duplication, extensibility | `SUBTASK_D_function_design/area_d_function_design.md` |
| `SUBTASK_E_test_coverage` | none | Review test coverage | `SUBTASK_E_test_coverage/area_e_test_coverage.md` |
| `SUBTASK_F_documentation` | none | Review documentation | `SUBTASK_F_documentation/area_f_documentation.md` |
| `SUBTASK_synthesis_cq` | `SUBTASK_A_api_surface`, `SUBTASK_B_abstraction`, `SUBTASK_C_error_handling`, `SUBTASK_D_function_design`, `SUBTASK_E_test_coverage`, `SUBTASK_F_documentation` | Assemble all area findings into final deliverable | `code_quality_findings.md` |

### Dependency Graph

```
SUBTASK_A_api_surface    ──┐
SUBTASK_B_abstraction    ──┤
SUBTASK_C_error_handling ──┤── SUBTASK_synthesis_cq
SUBTASK_D_function_design──┤
SUBTASK_E_test_coverage  ──┤
SUBTASK_F_documentation  ──┘
```
