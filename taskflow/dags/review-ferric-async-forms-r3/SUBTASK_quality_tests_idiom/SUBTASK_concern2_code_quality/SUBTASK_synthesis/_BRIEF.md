# Task: Synthesis — Concern 2 Code Quality Partial Findings

## Task Specification

**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_q1_coupling, SUBTASK_q2_eventhandler, SUBTASK_q3_gen_counter, SUBTASK_q4_correct_use
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Merge four `sub_findings.md` files produced by the four spoke tasks into a single `partial_findings.md` conforming to the parent subtree's findings format contract, then fold the suspended parent task (`SUBTASK_concern2_code_quality`) by calling `engine_resume_suspended`.

---

## Inputs

| Input | Location | Precondition |
|-------|----------|-------------|
| Q1 findings | `../SUBTASK_q1_coupling/sub_findings.md` | SUBTASK_q1_coupling COMPLETED |
| Q2 findings | `../SUBTASK_q2_eventhandler/sub_findings.md` | SUBTASK_q2_eventhandler COMPLETED |
| Q3 findings | `../SUBTASK_q3_gen_counter/sub_findings.md` | SUBTASK_q3_gen_counter COMPLETED |
| Q4 findings | `../SUBTASK_q4_correct_use/sub_findings.md` | SUBTASK_q4_correct_use COMPLETED |
| Output contract | `../../contracts/findings_format.md` | Static |
| Sub-task schema | `../contracts/_MANIFEST.yaml` | Static |
| Subtree hub | `../_GLOBAL.md` | Static |
| Parent workspace | `..` (i.e., the SUBTASK_concern2_code_quality directory) | Static — fold target |

---

## Synthesis Procedure

1. **Read all four `sub_findings.md` files in full.** Do not skim. Every entry in every file must appear in the merge unless it is a duplicate of another entry at the same location.

2. **Deduplicate.** If two spokes reported the same issue at the same location, include it once; do not silently drop either's reasoning — retain the richer description.

3. **Produce `../../partial_findings.md`** (i.e., the file at the SUBTASK_concern2_code_quality parent directory, path relative to this workspace: `../partial_findings.md`). This file must conform to `../../contracts/findings_format.md`:
   - `## Findings` section with all entries, in severity order (blockers first, then non-blockers, then clean)
   - `## What was examined` section covering all four sub-questions and all files examined

4. **Verify against the contract** before writing:
   - All findings use `concern: code-quality`
   - No finding duplicates issues #196–#201
   - Severity `blocker` appears only where a requirement is unmet or an API contract is broken
   - All `location` values are repository-relative paths or `"structural"`

5. **Author `SYNTHESIS.md` at the FOLD LOCATION** — which is the PARENT workspace, `..` relative to this task (i.e., `SUBTASK_concern2_code_quality/SYNTHESIS.md`, NOT this workspace's root). The fold location is the SUSPENDED task's workspace root. SYNTHESIS.md is the seam record, not a summary document; write a brief record of what was merged and the fold declaration.

6. **Call `mcp__hal__resume_suspended`** with:
   - `target_task_id`: `SUBTASK_concern2_code_quality`
   - `synthesized_task_id`: this task's own ID (SUBTASK_synthesis)
   - `seam_path`: the absolute path to the SYNTHESIS.md you authored at the fold location

7. Report your own terminal status:
   - `status: "completed"`
   - `decompose_evaluation: "Atomic"`
   - `outputs`: `["<abs path to partial_findings.md>", "<abs path to SYNTHESIS.md at fold location>"]`
   - `artifact_path`: your own COMPLETE.md at this task's workspace root

---

## Output Specification

**Primary output (fold output):** `../partial_findings.md`
Path: `SUBTASK_concern2_code_quality/partial_findings.md` (parent workspace)

**Fold seam record:** `../SYNTHESIS.md`
Path: `SUBTASK_concern2_code_quality/SYNTHESIS.md` (fold location = parent workspace)

**Own completion record:** `COMPLETE.md` at this task's workspace root

---

## Success Criteria

- All four `sub_findings.md` files consumed; every entry accounted for in the merge
- `../partial_findings.md` conforms to `../../contracts/findings_format.md`
- `../SYNTHESIS.md` authored at the correct fold location (parent workspace, not this workspace)
- `mcp__hal__resume_suspended` called with the correct `target_task_id` and `seam_path`
- Own terminal `report_status { status: "completed" }` called — then STOP

---

## Methodology Note

No new methodology loading is required for synthesis. The spoke tasks loaded and applied the methodologies; this task's work is structural: merge, deduplicate, conform to the output contract, and fold. If any spoke's finding is unclear, re-read that spoke's `sub_findings.md` — do not re-open the source files or re-examine the code.

---

## Inherited Constraints

- Repository-relative paths only in all outputs
- Issues #196–#201 MUST NOT appear as new findings in the merged output
- Do not add new code-quality findings not surfaced by the four spoke tasks; this is a synthesis, not a fresh review pass
- The `../partial_findings.md` output file belongs to this task as declared in `../contracts/_MANIFEST.yaml`
