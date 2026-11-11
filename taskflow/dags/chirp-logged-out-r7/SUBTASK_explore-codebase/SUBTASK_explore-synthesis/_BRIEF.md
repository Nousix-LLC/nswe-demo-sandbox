# Task: Exploration Synthesis — Produce analysis.md

## Task Specification

**Slug**: SUBTASK_explore-synthesis  
**Task Kind**: synthesis  
**Depends on**: SUBTASK_explore-survey-design, SUBTASK_explore-survey-backend, SUBTASK_explore-survey-frontend, SUBTASK_explore-survey-ferric  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

This task is the verification gate for the codebase exploration subtree. It reads all four survey outputs, creates the `work/chirp-logged-out` branch, synthesizes all findings into `analysis.md` at the parent workspace root, verifies that all required sections are present and self-consistent, and writes `SYNTHESIS.md` at the parent workspace root before calling `engine_resume_suspended` to un-suspend the parent task.

### Context

This task is part of the Codebase Exploration subtree for Chirp Logged-Out r7. See `../_GLOBAL.md` for subtree context, and `../../_GLOBAL.md` for the project-level context, ACs, and inherited constraints.

The parent task (SUBTASK_explore-codebase) is SUSPENDED with `decompose_evaluation=NeedsDecompose` awaiting this synthesis. Its declared output is `analysis.md` at `../` (the parent workspace root = SUBTASK_explore-codebase/).

**Dependents**: SUBTASK_backend-api (at the parent taskflow level, reads `analysis.md`)

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Subtree structure, identity assertions |
| Project context | `../../_GLOBAL.md` | Full project ACs, constraints, branch name |
| Subtree contracts | `../contracts/_MANIFEST.yaml` | Identity assertions to verify |
| Inherited API contract | `../../contracts/public_api_contract.md` | Required API surface for context |
| Design survey | `../SUBTASK_explore-survey-design/design-survey.md` | Extracted ACs and screen specs |
| Backend survey | `../SUBTASK_explore-survey-backend/backend-survey.md` | Existing API endpoints and auth |
| Frontend survey | `../SUBTASK_explore-survey-frontend/frontend-survey.md` | Existing routes and logged-out behavior |
| Ferric survey | `../SUBTASK_explore-survey-ferric/ferric-survey.md` | Available async primitives and patterns |

---

## Output Specification

### Primary Outputs

This task writes TWO files at the **parent workspace root** (`../`):

| Attribute | Value |
|-----------|-------|
| File 1 — Declared output | `analysis.md` at `../` (= `SUBTASK_explore-codebase/analysis.md`) |
| File 2 — Lifecycle record | `SYNTHESIS.md` at `../` (= `SUBTASK_explore-codebase/SYNTHESIS.md`) |

**Important**: Both files are written at `../` (the parent's workspace = SUBTASK_explore-codebase/), NOT at this task's own workspace (SUBTASK_explore-synthesis/).

After both files are written, this task MUST call:
```
engine_resume_suspended {
  target_task_id: <SUBTASK_explore-codebase task id>,
  synthesized_task_id: <this task id>,
  seam_path: <absolute path to ../SYNTHESIS.md>
}
```
to fold the parent from SUSPENDED to COMPLETED.

### Output Structure — analysis.md

`analysis.md` MUST include all six sections from the parent brief:

1. **Branch Status** — Confirm `work/chirp-logged-out` exists and was created from `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`

2. **API Endpoint Survey** — From backend-survey.md:
   - Whether the public timeline endpoint exists; its URL, auth, response type or recommendation
   - Whether the public user profile endpoint exists; same details
   - Auth middleware pattern summary
   - Final recommendation per endpoint

3. **Frontend Route Survey** — From frontend-survey.md:
   - What the home/landing route currently renders for a logged-out visitor
   - What the user profile route currently renders (or whether it exists)
   - Router configuration summary (Ferric router setup)

4. **Ferric Primitives Available** — From ferric-survey.md:
   - Async resource primitives and their loading/error state model
   - Four-state component pattern
   - SSR + hydration support
   - Any gaps or limitations

5. **Per-AC Gap Analysis** — From design-survey.md + all code surveys, for each of AC-1 through AC-5:
   - What currently exists that satisfies or partially satisfies it
   - What must be added or changed to fully satisfy it
   - Which task (backend-api or frontend-ui) owns the gap

6. **Implementation Plan Summary** — Specific files to change:
   - For SUBTASK_backend-api: which files in crates/chirp-server/ to modify or add
   - For SUBTASK_frontend-ui: which files in crates/chirp-frontend/ to modify or add

### Output Structure — SYNTHESIS.md

`SYNTHESIS.md` is the synthesis lifecycle record. It MUST include:

1. **Verification Summary** — Did all identity assertions from `../contracts/_MANIFEST.yaml` pass?
   - analysis_sections: all six sections present? (PASS / FAIL)
   - branch_first: branch created before analysis.md was written? (PASS / FAIL)
   - no_code_changes: no crate files modified? (PASS / FAIL)

2. **Survey Completeness** — Brief note confirming each of the four survey inputs was read and incorporated.

3. **Fold Record** — Confirms this task called `engine_resume_suspended` to un-suspend the parent.

---

## Operational Sequence

Execute in this order:
1. Read all inputs
2. Create the branch (`work/chirp-logged-out` from `cb1ced3` via SSH to build server per CLAUDE.md)
3. Verify branch creation succeeded
4. Write `analysis.md` at `../` (parent workspace root)
5. Write `SYNTHESIS.md` at `../` (parent workspace root)
6. Call `engine_report_status { status: "completed", decompose_evaluation: "Atomic", outputs: [...], artifact_path: "../SYNTHESIS.md" }`
7. Call `engine_resume_suspended { ... }`

---

## Success Criteria

- [ ] Branch `work/chirp-logged-out` created from `cb1ced3` before analysis.md is written
- [ ] analysis.md contains all six required sections
- [ ] Per-AC gap analysis covers AC-1 through AC-5
- [ ] SYNTHESIS.md verifies all three identity assertions
- [ ] `engine_resume_suspended` called successfully with the correct seam path
- [ ] No code changes made to any crate

---

## Suggested Methodology Files

**Task-type row matched**: "Synthesizing / verifying a hub-and-spoke decomposition" → Synthesis; "Designing systems" → Architecture (for the gap analysis framing)

**Primary files to load**:
- `synthesis/Synthesis_Overview_Methodology.md` — rationale: anchor for the synthesis verification gate; defines the four-check model and pass/fail criteria
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — rationale: how to verify that the survey outputs satisfy the structural contract (all six analysis sections present, all identity assertions met)
- `architecture/Architecture_API_Design_Methodology.md` — rationale: provides the lens for evaluating whether existing endpoints are appropriate for the public use case
- `operations/CodeManagement_Branching_Strategy_Methodology.md` — rationale: branch creation from an exact commit hash is an operational step that must be executed correctly

These are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.

## Inherited Constraints

- Branch MUST be `work/chirp-logged-out` from EXACTLY `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`
- Both analysis.md and SYNTHESIS.md MUST be written at `../` (parent workspace root), NOT at this task's workspace
- No code changes to any crate — exploration only
- Repository: `Nousix-LLC/nswe-demo`
- Build server access per CLAUDE.md: `ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@<server> 'bash -lc "<command>"'`
- No host paths, internal addresses, or taskflow references in any output or committed content
