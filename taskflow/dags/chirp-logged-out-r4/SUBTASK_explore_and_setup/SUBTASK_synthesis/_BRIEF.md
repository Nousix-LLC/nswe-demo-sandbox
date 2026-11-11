# Task: Synthesis — Integrate Findings into analysis.md

## Task Specification

**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_git_branch, SUBTASK_design_analysis, SUBTASK_server_analysis, SUBTASK_frontend_analysis, SUBTASK_ferric_analysis
**Status**: Pending
**Assigned To**: swe-coder

### Objective

**This task is a VERIFICATION GATE.** It does not merely summarize — it asserts that all
upstream findings are complete and consistent, then integrates them into the final `analysis.md`
at the parent workspace. It also writes `SYNTHESIS.md` (the fold record) and calls
`engine_resume_suspended` to fold the SUBTASK_explore_and_setup parent SUSPENDED → COMPLETED.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/_GLOBAL.md` | Project context, identities |
| Contracts manifest | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/contracts/_MANIFEST.yaml` | Required sections identity assertions |
| Parent brief | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/_BRIEF.md` | Declared analysis.md structure |
| Git status | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/SUBTASK_git_branch/git_status.md` | Branch name and HEAD SHA |
| Design findings | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/SUBTASK_design_analysis/design_findings.md` | Requirements, routes, BAR-011 |
| Server findings | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/SUBTASK_server_analysis/server_findings.md` | Routes, auth extractor, API spec verdict |
| Frontend findings | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/SUBTASK_frontend_analysis/frontend_findings.md` | Router file, existing routes, API pattern |
| Ferric findings | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/SUBTASK_ferric_analysis/ferric_findings.md` | Framework APIs |

---

## Process Specification

### Four-Check Verification Gate

Before writing `analysis.md`, verify ALL of the following (record gate results in `SYNTHESIS.md`):

**Check 1 — Contract verification**: Each findings file contains all required sections as declared
in `contracts/_MANIFEST.yaml`. If any required section is missing or vague ("not found" with no
explanation), schedule a remediation fix-task via `engine_amend_plan { add_task }` for that
specific gap before proceeding.

**Check 2 — Wiring verification**: The five findings files together cover all 5 analysis areas
(A-E) from the parent brief with no area left as "unknown" without explanation. Specifically:
- A (design requirements) → `design_findings.md` — covered
- B (server API) → `server_findings.md` — covered
- C (frontend) → `frontend_findings.md` — covered
- D (ferric APIs) → `ferric_findings.md` — covered
- E (API spec verdict) → `server_findings.md` — covered

**Check 3 — Duplication detection**: Confirm no contradictions across findings (e.g., the
frontend findings' API call pattern should be consistent with what the server analysis expects).
Note any contradictions explicitly.

**Check 4 — Code review / quality**: Each findings file uses specific file paths, type names,
and code patterns — not vague descriptions. If a finding says "some router file" rather than
naming the actual file path, that is a gate failure.

If ALL four checks pass: write `analysis.md` (the unified document).
If a check fails: schedule a remediation fix-task before proceeding.

### Writing analysis.md

Write to `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/analysis.md`.

The document structure MUST follow the parent brief's Output Structure exactly:

```
# Chirp Logged-Out — Codebase Analysis

## Branch Status
## Design Requirements Summary
## chirp-server: Existing API Surface
## chirp-frontend: Existing Structure
## Ferric Framework: Relevant APIs
## API Spec Verdict
## Implementation Guidance for SUBTASK_backend
## Implementation Guidance for SUBTASK_frontend
```

### Fold Sequence

After writing `analysis.md`, complete the fold:

1. Write `SYNTHESIS.md` at `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/SYNTHESIS.md`
   (the fold location — the SUSPENDED parent's directory, NOT this task's workspace).
2. Report `status="completed"` via terminal `engine_report_status` with
   `artifact_path=".../SUBTASK_explore_and_setup/SYNTHESIS.md"` and
   `outputs=[".../SUBTASK_explore_and_setup/analysis.md", ".../SUBTASK_explore_and_setup/SYNTHESIS.md"]`.
3. Call `engine_resume_suspended` with:
   - `target_task_id`: the task id of `SUBTASK_explore_and_setup` (the parent)
   - `synthesized_task_id`: this task's id (`SUBTASK_synthesis`)
   - `seam_path`: `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/SYNTHESIS.md`

---

## Output Specification

| Artifact | Location | Note |
|----------|----------|------|
| `analysis.md` | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/` | PRIMARY — declared output of the parent task |
| `SYNTHESIS.md` | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/` | Fold record (at parent workspace, not this workspace) |

**Note on SYNTHESIS.md location**: SYNTHESIS.md is written at the PARENT's workspace
(`SUBTASK_explore_and_setup/`), NOT at this task's workspace (`SUBTASK_synthesis/`).
This is the fold location per the kernel's named-state contract.

---

## Success Criteria

- [ ] All four gate checks run; failures remediated or noted
- [ ] `analysis.md` written at the parent workspace with all 7 required sections
- [ ] `SYNTHESIS.md` written at the parent workspace
- [ ] `engine_resume_suspended` called successfully to fold parent SUSPENDED → COMPLETED

---

## Suggested Methodology Files

**Task-type row:** Synthesis / verification gate — Primary: `synthesis`, Supporting: `code-review`

**Specific files:**
- `synthesis/Synthesis_Overview_Methodology.md` — Rationale: this task IS a synthesis gate; the Overview defines the four-check model this task MUST run.
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — Rationale: Check 1 is a contract verification against the `contracts/_MANIFEST.yaml`.
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — Rationale: Check 2 verifies that all 5 analysis areas from the parent brief are wired to findings outputs.
- `synthesis/Synthesis_Remediation_Methodology.md` — Rationale: if a gate check fails, this method governs how to schedule a remediation fix-task.

**These are SUGGESTIONS.** The child agent is the final judge — fewer if a check is clearly inapplicable, more if the subtree's shape reveals additional surface.

## Inherited Constraints

- Repository is at `/home/user/nousix-runtime/nswe-demo`
- `analysis.md` MUST be written at the PARENT workspace, not this task's workspace
- `SYNTHESIS.md` MUST be written at the PARENT workspace (fold location)
- Do NOT put host paths, internal addresses, or taskflow references in git commits
- Note: the cluster SSH pattern from CLAUDE.md is NOT needed for this task
