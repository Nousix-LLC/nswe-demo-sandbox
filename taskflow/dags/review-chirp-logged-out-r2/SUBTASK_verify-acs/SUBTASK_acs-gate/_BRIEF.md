# Task: Synthesis Gate — Compile AC Verdicts into findings-acs.md

## Task Specification

**Slug**: SUBTASK_acs-gate  
**Task Kind**: synthesis  
**Depends on**: SUBTASK_ac1-verify, SUBTASK_ac4-verify, SUBTASK_ac235-confirm  
**Status**: Pending

### Objective

This task is the **verification gate** for the SUBTASK_verify-acs subtree. Run the four-check model: (1) verify all five required AC verdict fields are present and have valid values; (2) verify all evidence is cited; (3) confirm no duplicate or conflicting verdicts; (4) synthesize a code-review-level quality check on the evidence quality. If all checks PASS, assemble `findings-acs.md` conforming to the parent contract schema at `../../contracts/_MANIFEST.yaml`. If any check fails, schedule remediation rather than produce a defective output.

### Context

This task is part of SUBTASK_verify-acs (see `_GLOBAL.md` in the parent workspace).

**Dependencies**: SUBTASK_ac1-verify, SUBTASK_ac4-verify, SUBTASK_ac235-confirm (all three must complete first)  
**Dependents**: SUBTASK_synthesis in the parent DAG (review-chirp-logged-out-r2) consumes `../findings-acs.md`

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Subtree constraints and expected output format |
| AC-1 verdict | `../SUBTASK_ac1-verify/verdict-ac1.md` | ac_1_verdict + evidence |
| AC-4 verdict | `../SUBTASK_ac4-verify/verdict-ac4.md` | ac_4_verdict + evidence |
| AC-2/3/5 verdicts | `../SUBTASK_ac235-confirm/verdict-ac235.md` | ac_2_verdict, ac_3_verdict, ac_5_verdict + evidence |
| Internal contracts manifest | `../contracts/_MANIFEST.yaml` | Spoke output schema |
| Parent contracts manifest | `../../contracts/_MANIFEST.yaml` | Required output schema for findings-acs.md |

---

## This Task is a Verification Gate

Do NOT summarize the spoke outputs into prose. Instead, run these four checks in order:

### Check 1: Behavioral contract verification
Verify that each spoke output contains its required fields per `../contracts/_MANIFEST.yaml`:
- `verdict-ac1.md` has `ac_1_verdict: PASS | FAIL`
- `verdict-ac4.md` has `ac_4_verdict: PASS | FAIL`
- `verdict-ac235.md` has `ac_2_verdict`, `ac_3_verdict`, `ac_5_verdict` each `PASS | FAIL`

If any required field is absent or has an invalid value, STOP. File a remediation fix-task via `engine_amend_plan { add_task }` targeting the offending spoke, and suspend with status=failed.

### Check 2: Wiring verification
Verify that all five AC verdicts map correctly to the five ACs in issue #35. No AC can be silently skipped. No verdict can be "SKIP" or blank.

### Check 3: Duplication / conflict detection
Verify that no AC appears in more than one spoke output with conflicting verdicts. (AC-1 is in verdict-ac1.md only; AC-4 is in verdict-ac4.md only; AC-2/3/5 are in verdict-ac235.md only.) If any overlap exists, record the conflict.

### Check 4: Evidence quality review
For each AC verdict, verify that evidence is cited (a file reference, a line number, or an explicit "not in diff" statement). A bare "PASS" with no evidence is insufficient. If evidence is thin, flag it in the output but do not block the assembly.

If all four checks PASS, proceed to assembly.

---

## Assembly

Produce `findings-acs.md` at `../findings-acs.md` using the following structure (required by `../../contracts/_MANIFEST.yaml`):

```markdown
# Findings: AC Re-Verification

**PR**: #263 (`work/chirp-logged-out`)
**HEAD reviewed**: 7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4

## AC verdicts

| AC | Verdict | Evidence |
|----|---------|----------|
| AC-1 | PASS or FAIL | [evidence from verdict-ac1.md] |
| AC-2 | PASS or FAIL | [evidence from verdict-ac235.md] |
| AC-3 | PASS or FAIL | [evidence from verdict-ac235.md] |
| AC-4 | PASS or FAIL | [evidence from verdict-ac4.md] |
| AC-5 | PASS or FAIL | [evidence from verdict-ac235.md] |

## Per-AC detail

### AC-1: [verdict]
[Detail from verdict-ac1.md]

### AC-2: [verdict]
[Detail from verdict-ac235.md]

### AC-3: [verdict]
[Detail from verdict-ac235.md]

### AC-4: [verdict]
[Detail from verdict-ac4.md]

### AC-5: [verdict]
[Detail from verdict-ac235.md]

## Non-blocking findings
| ID | Location | Severity | Description |
|----|----------|----------|-------------|
[List any new non-blockers found by spokes, if any. Leave empty if none.]
```

After writing `../findings-acs.md`, write `SYNTHESIS.md` at `../SYNTHESIS.md` (the fold record) recording how the checks passed and the assembly completed. Then call `engine_resume_suspended` to fold the parent (`SUBTASK_verify-acs`) SUSPENDED → COMPLETED.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Primary output (required by parent DAG) | `../findings-acs.md` |
| Synthesis fold record | `../SYNTHESIS.md` |

---

## Success Criteria

- [ ] All four verification checks run explicitly
- [ ] All five AC verdict fields present and valid
- [ ] `../findings-acs.md` written conforming to `../../contracts/_MANIFEST.yaml`
- [ ] `../SYNTHESIS.md` written as the fold record
- [ ] `engine_resume_suspended` called to fold SUBTASK_verify-acs SUSPENDED → COMPLETED

---

## Suggested Methodology Files

**Task type row matched**: "Synthesizing / verifying a hub-and-spoke decomposition | Synthesis (primary) | Code Review, Code Quality (supporting)"

**Primary files to load:**
- `synthesis/Synthesis_Overview_Methodology.md` — the four-check gate model (always load first)
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify spoke outputs match the declared contract
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — verify all required fields are wired
- `synthesis/Synthesis_Remediation_Methodology.md` — if any check fails, how to schedule remediation

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but is the final judge of what its work requires.

## Inherited Constraints

- HEAD under review is `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`
- Do NOT paraphrase spoke outputs — transcribe verdict and evidence faithfully
- Non-blockers already tracked as issues #264–#271 — note as "already tracked" if re-encountered
- Do NOT name host paths, tailnet addresses, or review DAG internal paths in any GitHub-posted content
- Repo is `Nousix-LLC/nswe-demo`

## Out-of-Scope Methodologies

- `synthesis/Synthesis_Duplication_Detection_Methodology.md` — not needed; spokes own disjoint ACs with no overlapping responsibilities
- `code-review/CodeReview_Process_Methodology.md` — synthesis is a gate, not a first-pass review
