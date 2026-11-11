# Task: Synthesis — Verdict, GitHub Review, SYNTHESIS.md

## Task Specification

**Slug**: SUBTASK_synthesis  
**Task Kind**: synthesis  
**Depends on**: SUBTASK_verify-fixes, SUBTASK_verify-acs  
**Status**: Pending  

### Objective

This task is a **verification gate**. It does not summarize prose — it asserts whether the combined spoke findings satisfy the merge bar for PR #263 at HEAD `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`. It runs four mechanical checks (B1/B2 fix verdicts, AC verdicts, regression verdict, identity assertions), applies the verdict logic from the contract, and either passes or fails. On pass, verdict is APPROVE; on fail, verdict is REQUEST-CHANGES.

Then it delivers: (1) a posted review/comment on GitHub PR #263, (2) the root `SYNTHESIS.md` at `taskflow/dags/review-chirp-logged-out-r2/SYNTHESIS.md`.

### Context

This task is part of review-chirp-logged-out-r2 (see `_GLOBAL.md` in the parent workspace).

**Dependencies**: SUBTASK_verify-fixes, SUBTASK_verify-acs — both must be COMPLETED with their outputs observable  
**Dependents**: none — this is the terminal task

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | PR metadata, ACs, verdict logic, constraints |
| r1 review output | `taskflow/dags/review-chirp-logged-out-r1/SYNTHESIS.md` | Original blockers and non-blockers for de-duplication |
| Fix findings | `../SUBTASK_verify-fixes/findings-fixes.md` | B1 and B2 fix verdicts + quality/tests/security/regression |
| AC findings | `../SUBTASK_verify-acs/findings-acs.md` | AC-1 through AC-5 verdicts |
| contracts manifest | `../contracts/_MANIFEST.yaml` | Required identity assertions to run |

---

## Verification gate: four required checks

### Check 1 — Fix verdicts

Read `findings-fixes.md`. For each of B1 and B2:
- Is the fix verdict PASS or FAIL?
- If FAIL: this is a remaining blocker → verdict = REQUEST-CHANGES
- If PASS for both: proceed

### Check 2 — AC verdicts

Read `findings-acs.md`. For each of AC-1 through AC-5:
- Is the AC verdict PASS or FAIL?
- If any AC is FAIL: this is a blocker → verdict = REQUEST-CHANGES
- If all 5 ACs PASS: proceed

### Check 3 — Regression verdict

From `findings-fixes.md`, read the regression verdict:
- If FAIL (extra changes found that introduce new problems): verdict = REQUEST-CHANGES with specific finding
- If PASS: proceed

### Check 4 — New blocking findings

Review the non-blocking findings lists from both spokes. Apply the review bar: are any of them actually blocking issues? A non-blocker finding that the spoke under-categorized must be caught here. If a new blocker is found: verdict = REQUEST-CHANGES.

### Identity assertions (from contract manifest)

Run the assertions in `../contracts/_MANIFEST.yaml`:
- `findings-fixes.md` has explicit verdict for B1 and B2 — if missing, FAIL (incomplete spoke output)
- `findings-acs.md` has explicit verdict for each of AC-1 through AC-5 — if missing, FAIL (incomplete spoke output)
- If B1=PASS and B2=PASS and all 5 ACs=PASS and regression=PASS and no new blockers: verdict = APPROVE
- If any of the above fails: verdict = REQUEST-CHANGES

Do NOT silently plug a failing assertion. Report any failure explicitly.

---

## Verdict and deliverables

### Deliverable 1: Root SYNTHESIS.md

Write to `taskflow/dags/review-chirp-logged-out-r2/SYNTHESIS.md` (the observation seam path, NOT inside this task's workspace directory). This is the kernel fold record for this decomposition and must follow the named-state convention for `SYNTHESIS.md`.

The SYNTHESIS.md must contain:
- **Verdict**: APPROVE or REQUEST-CHANGES
- **Head reviewed**: `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`
- **B1 verdict**: PASS or FAIL with evidence
- **B2 verdict**: PASS or FAIL with evidence
- **Per-AC table**: AC-1 through AC-5, each with verdict and key evidence
- **Per-concern findings**: what each of the 6 concerns checked and found (clean or not)
- **New non-blocking findings**: any new findings from either spoke (with IDs, severity, description), de-duplicated against issues #264–#271
- **What was clean**: explicit account of what was examined and found sound

**Prose standard**: Write in plain, direct prose. No "honest metrics," "genuine reliability," or other moral adjectives. No narrated candor ("stated plainly," "to be honest"). No unnamed contrast pairs. No slot-fill templates. If the verdict is APPROVE, say so plainly and say why each concern was satisfied. If REQUEST-CHANGES, name the specific blocking finding and what would satisfy it.

**Do not name** host paths, tailnet addresses (`100.x`), or review DAG internal paths in the SYNTHESIS.md — it may be read by the PR author and filed as a public record.

### Deliverable 2: GitHub PR review/comment

Post to PR #263 on `Nousix-LLC/nswe-demo`. Because the PR author and reviewer share the same account, a formal GitHub approval may not be possible; post the verdict and findings as a PR comment covering each concern.

The posted comment must contain:
- Verdict: APPROVE or REQUEST-CHANGES (stated plainly at the top)
- Verdict on B1 fix and B2 fix
- Verdict on each of the 5 ACs (table form is clean)
- Any new non-blocking findings (brief, actionable)
- What was examined and found clean

Do NOT name host paths, tailnet addresses, DAG internal paths, or review tooling infrastructure in the posted comment.

Use `gh pr comment 263 -R Nousix-LLC/nswe-demo --body "..."` or `gh pr review 263 -R Nousix-LLC/nswe-demo ...` as appropriate.

### Deliverable 3: New non-blocking issues (if any)

If either spoke found new non-blocking findings not already tracked in issues #264–#271, file each as a GitHub issue in Nousix-LLC/nswe-demo, linked to PR #263 and issue #35. Use `gh issue create -R Nousix-LLC/nswe-demo ...`.

Write each issue for the repository's readers: point at files and lines in the repository. Do not name host paths, tailnet addresses, or DAG internal paths.

---

## Output Specification

| Artifact | Location | Note |
|----------|----------|------|
| Root `SYNTHESIS.md` | `taskflow/dags/review-chirp-logged-out-r2/SYNTHESIS.md` | Kernel fold record — NOT in this task's directory |
| `COMPLETE.md` | `SUBTASK_synthesis/COMPLETE.md` | Kernel task completion record |

The `SYNTHESIS.md` at the parent's root is the observation seam path and the fold record per the named-state contract. It must be written before the terminal `engine_report_status` call. The `artifact_path` in the terminal call must point to this `SYNTHESIS.md`.

**IMPORTANT on the terminal call**: After writing `SYNTHESIS.md` at the parent root path, call `engine_resume_suspended` to fold the parent. Then report status with `status: "completed"` and `artifact_path: "taskflow/dags/review-chirp-logged-out-r2/SYNTHESIS.md"`.

---

## Success criteria

- [ ] Read both spoke output files (`findings-fixes.md`, `findings-acs.md`)
- [ ] All four gate checks run; results recorded
- [ ] All contract identity assertions evaluated
- [ ] Verdict (APPROVE or REQUEST-CHANGES) determined with explicit justification
- [ ] Root `SYNTHESIS.md` written at `taskflow/dags/review-chirp-logged-out-r2/SYNTHESIS.md`
- [ ] GitHub PR review/comment posted on PR #263
- [ ] New non-blocking findings (if any) filed as GitHub issues
- [ ] `COMPLETE.md` written in task workspace
- [ ] Terminal lifecycle event reported with `artifact_path` pointing to the root `SYNTHESIS.md`

---

## Suggested Methodology Files

**Task type row matched**: "Synthesizing / verifying a hub-and-spoke decomposition | Synthesis (primary) | Code Review, Code Quality (supporting)"  
Plus: this synthesis integrates code review findings, so Code Review bundle is relevant.

**Primary files to load (Synthesis bundle):**
- `synthesis/Synthesis_Overview_Methodology.md` — ALWAYS first; defines the four-check gate model and what a synthesis task is
- `synthesis/Synthesis_Code_Review_Methodology.md` — the synthesis-side code review pass over combined spoke outputs
- `synthesis/Synthesis_Remediation_Methodology.md` — in case any gate check fails and a remediation task needs to be scheduled

**Supporting files to consider (Code Review bundle):**
- `code-review/CodeReview_Checklist_Methodology.md` — verify the spoke findings covered the review checklist
- `code-review/CodeReview_Feedback_Guidelines_Methodology.md` — how to frame the GitHub-posted review comment

The above are the parent's flagged methodologies based on the task type. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.

## Inherited Constraints

- Write `SYNTHESIS.md` at the parent workspace root (`taskflow/dags/review-chirp-logged-out-r2/SYNTHESIS.md`), NOT inside this task's directory
- If verdict is APPROVE, the overseer will land the PR (headless: true; landing_authority: delegated) — be certain before approving
- De-duplicate new non-blocking findings against issues #264–#271 from review-r1
- Do NOT name host paths, tailnet addresses, or DAG internal paths in any GitHub-posted content
- The repo is `Nousix-LLC/nswe-demo`

## Out-of-Scope Methodologies

- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — not applicable; this is a code review synthesis, not a code wiring check
- `synthesis/Synthesis_Duplication_Detection_Methodology.md` — not applicable for this review synthesis
- `synthesis/Synthesis_AI_BDD_Spec_Methodology.md` — not applicable; we're assessing fix correctness, not authoring a behavioral spec
