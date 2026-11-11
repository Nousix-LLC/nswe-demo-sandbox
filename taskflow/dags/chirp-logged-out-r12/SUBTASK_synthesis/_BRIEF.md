# _BRIEF.md — SUBTASK_synthesis

**Task Kind**: synthesis  
**Depends on**: SUBTASK_backend_check, SUBTASK_frontend_check  
**Status**: Pending  

## Objective

Synthesize the backend and frontend verification results into a single root-level
`SYNTHESIS.md` verdict for chirp-logged-out-r12.

This is a **verification gate**. Its job is NOT to summarize prose — it is to run the
four-check synthesis model (contract verification, wiring verification, duplication detection,
code review) over the combined outputs, then produce a structured PASS/FAIL verdict for each
acceptance criterion (AC-1 through AC-5) and an overall PASS/FAIL for the feature.

The output `SYNTHESIS.md` is the declared observation seam for this run
(`taskflow/dags/chirp-logged-out-r12/SYNTHESIS.md`), and it is what the overseer reads to
determine if the feature is complete.

## Context

This task is part of chirp-logged-out-r12 (see `../_GLOBAL.md` for full context).

**Dependencies**: SUBTASK_backend_check AND SUBTASK_frontend_check must both reach COMPLETED
before this task is dispatched. Their declared outputs (`backend_verdict.md` and
`frontend_verdict.md`) will be available.

**Dependents**: None — this is the terminal synthesis task.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Constraints, acceptance criteria, branch |
| Contract manifest | `../contracts/_MANIFEST.yaml` | Structural identities to verify |
| Backend verdict | `../SUBTASK_backend_check/backend_verdict.md` | AC-5 verdict and evidence |
| Frontend verdict | `../SUBTASK_frontend_check/frontend_verdict.md` | AC-1–4 verdicts and evidence |
| Current HEAD | branch `work/chirp-logged-out` via `gh` | Final commit SHA, CI status |

---

## Process

1. **Orient**: Read the brief, `../_GLOBAL.md`, and `../contracts/_MANIFEST.yaml`.

2. **Read the spoke outputs**:
   - `../SUBTASK_backend_check/backend_verdict.md` — the AC-5 verdict and evidence
   - `../SUBTASK_frontend_check/frontend_verdict.md` — the AC-1–4 verdicts and evidence

3. **Run contract verification**:
   - Every AC-1 through AC-5 is covered by the two verdict files combined
   - Each AC has a verdict (PASS/FAIL) and at least one evidence item
   - Structural identities from `_MANIFEST.yaml` are satisfied

4. **Verify CI status**:
   - Get the current HEAD on `work/chirp-logged-out` via `gh pr view 263`
   - Confirm CI is passing on the final HEAD (all 6/6 checks)
   - If any check task pushed commits, confirm those commits are reflected in CI

5. **Check live deployment** (if accessible):
   - The app runs on k3s; check ArgoCD sync status and that the deployed version
     reflects the final HEAD.
   - Optionally do a quick smoke-test via the SSH-accessible endpoint at port 8081.
   - Kubernetes commands use the SSH form in `../_GLOBAL.md` §Subtree-Wide Constraints.

6. **Determine overall verdict**:
   - `PASS`: ALL of AC-1 through AC-5 show PASS in the verdicts, CI is passing, no blockers
   - `FAIL`: ANY of AC-1 through AC-5 shows FAIL, OR CI is failing, OR a structural identity
     from the contract is not satisfied

7. **Write `SYNTHESIS.md`** at the root workspace:
   `taskflow/dags/chirp-logged-out-r12/SYNTHESIS.md`

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `SYNTHESIS.md` |
| Location | `taskflow/dags/chirp-logged-out-r12/SYNTHESIS.md` (the PARENT workspace, not this task's) |
| Format | Structured Markdown — the synthesis gate record |

The `SYNTHESIS.md` MUST contain:

```markdown
# SYNTHESIS — chirp-logged-out-r12

**Overall Verdict**: PASS | FAIL  
**Branch**: work/chirp-logged-out  
**Final HEAD**: <commit SHA>  
**CI Status**: <PASS/FAIL — list all 6 checks>  
**Date**: <ISO date>

## Per-Criterion Verdicts

| AC | Criterion | Verdict | Evidence summary |
|----|-----------|---------|-----------------|
| AC-1 | Logged-out visitor sees chirps at `/` | PASS/FAIL | <1-line summary> |
| AC-2 | Logged-out visitor sees user chirps at `/users/:username` | PASS/FAIL | <1-line summary> |
| AC-3 | Landing page shows sign-up/sign-in CTA | PASS/FAIL | <1-line summary> |
| AC-4 | sign_in and sign_up show accurate logged-out states | PASS/FAIL | <1-line summary> |
| AC-5 | Backend routes serve data without auth | PASS/FAIL | <1-line summary> |

## Detailed Findings

### AC-1 — [PASS/FAIL]
[Evidence from frontend_verdict.md for AC-1]

### AC-2 — [PASS/FAIL]
[Evidence from frontend_verdict.md for AC-2]

### AC-3 — [PASS/FAIL]
[Evidence from frontend_verdict.md for AC-3]

### AC-4 — [PASS/FAIL]
[Evidence from frontend_verdict.md for AC-4]

### AC-5 — [PASS/FAIL]
[Evidence from backend_verdict.md for AC-5]

## Commits Pushed During This Run

[List of commits pushed by SUBTASK_backend_check and SUBTASK_frontend_check,
or "None — no new commits were needed."]

## CI Verification

[CI status for the final HEAD. List all 6 checks (clippy/doc/fmt/image/test/wasm).]

## Live Deployment

[ArgoCD sync status and/or smoke-test result, or "Not verified — CI pass is sufficient."]

## Blockers (if FAIL)

[Specific description of what failed and what would be needed to fix it.]
```

This `SYNTHESIS.md` MUST be written at `taskflow/dags/chirp-logged-out-r12/SYNTHESIS.md`,
NOT at this task's own workspace. That path is the declared observation seam.

After writing `SYNTHESIS.md`, the terminal `engine_report_status` call MUST report
`artifact_path` as `SYNTHESIS.md` at that root path.

---

## Success Criteria

- [ ] Both spoke verdict files have been read and their AC verdicts understood
- [ ] CI status has been checked for the final HEAD on `work/chirp-logged-out`
- [ ] All structural identities from `../contracts/_MANIFEST.yaml` are satisfied
- [ ] `SYNTHESIS.md` exists at `taskflow/dags/chirp-logged-out-r12/SYNTHESIS.md`
- [ ] `SYNTHESIS.md` contains verdicts for ALL 5 acceptance criteria (AC-1 through AC-5)
- [ ] `SYNTHESIS.md` contains the overall PASS/FAIL verdict
- [ ] If any AC is FAIL, the specific blocker is described

---

## Suggested Methodology Files

**Domain Mapping row matched**: 
- "Synthesizing / verifying a hub-and-spoke decomposition" → primary: `Synthesis`, supporting: `Code Review, Code Quality`
- "Verify a big build wired up correctly" → `Synthesis (Overview, Contract/Wiring/Dedup Verification), Code Review`

**Suggested files** (this task MUST load the synthesis bundle — it is a verification gate):
- `synthesis/Synthesis_Overview_Methodology.md` — the four-check model; this task IS a
  verification gate and must behave as one
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify that the structural
  identities in `../contracts/_MANIFEST.yaml` are satisfied
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — verify that every AC declared in
  the briefs is covered by an output from the check tasks
- `code-review/CodeReview_Process_Methodology.md` — brief review of the final diff and CI

The above are the parent's flagged methodologies based on the task type. This task IS
declared as synthesis kind; loading `Synthesis_Overview_Methodology.md` is not optional —
it defines the four-check gate this task must run.

---

## Inherited Constraints

1. **Branch**: `work/chirp-logged-out` only. All fix work was done by SUBTASK_backend_check
   and SUBTASK_frontend_check; this task does NOT push new commits except in extreme
   circumstances (and must not do so without CI evidence of correctness).
2. **PR**: Do not open a new PR. PR #263 already covers this branch.
3. **CI**: Verify that CI is passing on the final HEAD.
4. **Repository**: `Nousix-LLC/nswe-demo` only.
5. **Host facts**: Never put server address, SSH key path, user name, or host paths in GitHub
   issues, PRs, comments, or committed files.
6. **Output path**: `SYNTHESIS.md` MUST be written to the root workspace
   (`taskflow/dags/chirp-logged-out-r12/SYNTHESIS.md`), not to this task's subdirectory.

---

## Out-of-Scope Methodologies

- `decomposition/` — synthesis is the reassembly, not the split; never loads decomposition
  bundle content
- `frontend/` and `code-review/CodeReview_Checklist_Methodology.md` in depth — the spoke
  tasks already did the detailed code review; this task synthesizes their verdicts
