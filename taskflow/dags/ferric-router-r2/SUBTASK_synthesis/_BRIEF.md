# Task: Synthesis gate — verify and fold ferric-router-r2 remediation

## Task Specification

**Slug**: SUBTASK_synthesis  
**Task Kind**: synthesis  
**Depends on**: SUBTASK_router-branch, SUBTASK_macros-assessment  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

This task is the **verification gate** for the ferric-router-r2 remediation DAG. It does NOT summarize the spokes in prose — it verifies the three contract identities from `../contracts/_MANIFEST.yaml`, resolves any violations by injecting fix tasks (or escalating), and writes the fold record `SYNTHESIS.md` at the parent workspace root that the overseer reads.

The gate MUST run the four-check model:
1. **Contract verification** — do the spoke outputs satisfy the declared identities?
2. **Wiring verification** — do the spoke outputs compose correctly (router PR + assessment document exist and are well-formed)?
3. **Duplication detection** — does the router branch accidentally contain macros commits or vice versa?
4. **Code review of combined output** — is the router-pr.md accurate? Is the macros-assessment.md actionable?

### Context

This task is part of the ferric-router-r2 remediation DAG (see `../_GLOBAL.md`).

**Observation seam**: The overseer reads `../SYNTHESIS.md` (this task writes it at that path).  
**Fold action**: After writing `SYNTHESIS.md`, call `engine_resume_suspended` to fold the parent.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Understand what was decomposed and what success looks like |
| Contract manifest | `../contracts/_MANIFEST.yaml` | The three identities to verify |
| Router PR output | `../SUBTASK_router-branch/outputs/router-pr.md` | Verify branch + PR identity |
| Macros assessment output | `../SUBTASK_macros-assessment/outputs/macros-assessment.md` | Verify assessment completeness |
| Review synthesis (original) | `../../review-ferric-router-r1/SYNTHESIS.md` | Cross-check: does router-pr.md match the review's passing commits? |

---

## Process Specification

**This task MUST run the verification gate — not write a summary.** The four checks:

### Check 1: Contract verification
Verify each identity in `../contracts/_MANIFEST.yaml`:
- `router_branch_clean`: Confirm via GitHub or git that `work/ferric-router-r2` exists on remote with exactly `89687da`, `cab18b9`, `3868b2c` versus `main` and NO ferric-macros files
- `router_pr_correct_issues`: Confirm the open PR closes #131, #146, #147
- `macros_assessment_complete`: Confirm the assessment covers all 12 macros commits and maps them to #137–#142

### Check 2: Wiring verification
- Both output files exist at their declared paths
- router-pr.md has a valid PR URL
- macros-assessment.md has an executive summary, issue mapping, and recommended PR structure

### Check 3: Duplication detection
- The `work/ferric-router-r2` diff should show ONLY `crates/ferric-router/` changes
- The assessment should NOT recommend including macros in the router PR

### Check 4: Code review of combined output
- Is the router PR well-formed? Correct title, body, closing keywords?
- Is the macros assessment actionable? Does it give the overseer enough to commission the follow-on review?

**Gate verdict**: If all four checks PASS → write SYNTHESIS.md at `../SYNTHESIS.md` and fold.  
**If any check FAILS** → inject fix tasks via `engine_amend_plan { add_task }` before the terminal call; do NOT silently plug a failure.

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `SYNTHESIS.md` |
| Location | `../` (the parent workspace root — the fold location) |

### Output Structure

```markdown
# SYNTHESIS.md — ferric-router-r2

## Gate Verdict: PASS / PARTIAL / FAIL

## Contract Identities

### router_branch_clean
<PASS/FAIL + evidence>

### router_pr_correct_issues
<PASS/FAIL + evidence>

### macros_assessment_complete
<PASS/FAIL + evidence>

## Router PR Summary
<Branch, PR URL, commits, CI status>

## Macros Assessment Summary
<Key findings from the macros assessment, recommended next step>

## Remediation Status
<Did this attempt resolve B1? What remains?>

## Next Steps for the Overseer
<What needs to happen next — macros PR commissioning, router PR review/merge, etc.>
```

---

## Success Criteria

- [ ] All three contract identities verified (PASS or documented FAIL with injected fix tasks)
- [ ] All four checks of the gate run explicitly
- [ ] `SYNTHESIS.md` written at `../SYNTHESIS.md` (the fold location)
- [ ] `engine_resume_suspended` called with `seam_path: "../SYNTHESIS.md"` to fold the parent
- [ ] No silent plugging of failures

---

## Suggested Methodology Files

**Task-type row matched**: "Synthesizing / verifying a hub-and-spoke decomposition (contract + wiring + dedup + review gate)" → Primary: `synthesis`, Supporting: `code-review`

**Specific files to load**:
- `synthesis/Synthesis_Overview_Methodology.md` — the four-check gate model, the go/no-go decision table, the SYNTHESIS.md schema. Load this first (the anchor).
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — how to verify behavioral contracts against the manifest identities.
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — how to verify the spoke outputs compose (exist, are well-formed, satisfy their wiring).

*Rationale*: This is a synthesis gate task; the synthesis bundle is the primary methodology. Contract verification covers the three identities. Wiring verification covers the structural composition check (both files exist, well-formed, router PR has PR URL, etc.).*

**These are the parent's suggestions; the child loads what the gate requires — the synthesis anchor is mandatory; additional files at the child's judgment.**

---

## Inherited Constraints

- Write `SYNTHESIS.md` at the FOLD LOCATION: `../SYNTHESIS.md` (the parent workspace root, NOT inside SUBTASK_synthesis/)
- After writing SYNTHESIS.md, call `engine_resume_suspended` per the fold contract
- Do NOT modify the spoke outputs — read-only
- Use SSH for any server commands needed to verify the branch/PR
- The overseer reads ONLY `../SYNTHESIS.md` — make it complete and actionable
