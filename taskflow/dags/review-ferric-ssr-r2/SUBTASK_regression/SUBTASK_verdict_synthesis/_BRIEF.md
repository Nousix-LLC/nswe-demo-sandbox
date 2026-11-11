# Task: Regression Verdict Synthesis

## Task Specification

**Slug**: SUBTASK_verdict_synthesis  
**Task Kind**: synthesis  
**Depends on**: SUBTASK_reg_criteria, SUBTASK_sec_quality  
**Status**: Pending  
**Assigned To**: swe-reviewer

### Objective

This task is a verification gate. It reads the two spoke outputs (criteria_findings.md and sec_quality_findings.md), verifies they satisfy the structural identities declared in `../contracts/_MANIFEST.yaml`, and synthesizes them into the final `regression_verdict.md` following the ancestor verdict schema.

The gate asserts:
1. Every REQ-ID in {REQ-SSR-001, REQ-SSR-002, REQ-SSR-003, REQ-SSR-005, REQ-HYD-001, REQ-HYD-002, REQ-HYD-004, REQ-MIS-001, REQ-MIS-002} has a verdict in criteria_findings.md
2. Security and code quality surfaces are covered in sec_quality_findings.md
3. The combined output assembles mechanically into regression_verdict.md per verdict_schema.md

### Context

This task is the synthesis hub of SUBTASK_regression (see `../_GLOBAL.md`). The two spokes (SUBTASK_reg_criteria and SUBTASK_sec_quality) are complete before this task runs.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Parent context | `../_GLOBAL.md` | Review scope, constraints |
| Verdict schema | `../../contracts/verdict_schema.md` | Required output format for regression_verdict.md |
| Findings schema | `../contracts/findings_schema.md` | Expected structure of spoke outputs |
| Criteria findings | `../SUBTASK_reg_criteria/criteria_findings.md` | Regression criteria results |
| Security/quality findings | `../SUBTASK_sec_quality/sec_quality_findings.md` | Security and code quality results |

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `regression_verdict.md` |
| Location | `../` (parent workspace: `SUBTASK_regression/`) |

The output MUST follow `../../contracts/verdict_schema.md`. It carries:
- **Verdict**: `PASS` (all 9 criteria clean, no security blockers) or `FAIL` (at least one criterion degraded or security blocker)
- **Requirements Covered**: REQ-SSR-001..003, REQ-SSR-005, REQ-HYD-001, REQ-HYD-002, REQ-HYD-004, REQ-MIS-001, REQ-MIS-002
- **Evidence**: Combined evidence from both spoke outputs
- **Findings**: All findings from security and code quality, enumerated with severity, location, principle, why it matters, resolution
- **What Was Examined and Found Clean**: Combined list from both spokes

---

## Gate Checks (this task MUST run as a verification gate, not a prose summary)

Before writing regression_verdict.md, verify:
1. **Contract identity 1**: criteria_findings.md has a PASS or FAIL verdict for every one of the 9 REQ-IDs. If any is missing, fail with a gap report rather than synthesizing silently.
2. **Contract identity 2**: sec_quality_findings.md has Security Findings and Code Quality Findings sections. If absent, note the gap.
3. **Wiring**: No finding from either spoke is dropped or paraphrased into oblivion; all findings are carried through with their severity, location, and resolution.
4. **Overall verdict**: FAIL if any criteria has FAIL verdict or if any security finding is Blocker-severity; PASS if all 9 criteria PASS and no Blocker security finding.

---

## Success Criteria

- [ ] Both spoke outputs read and structurally verified
- [ ] All 9 REQ-IDs present with verdicts in the output
- [ ] All findings from both spokes carried through with their severity
- [ ] Overall PASS or FAIL verdict stated with rationale
- [ ] `regression_verdict.md` written to `../` (the SUBTASK_regression workspace)

---

## Suggested Methodology Files

**Task-type row matched**: "Synthesizing / verifying a hub-and-spoke decomposition" → Primary: Synthesis; Cross-cutting: Code Review

Specific files to load:
- `synthesis/Synthesis_Overview_Methodology.md` — the four-check gate model (always load first)
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify contract identities hold
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — verify no dead/detached findings

These are the parent's suggestions. Load fewer if clearly inapplicable; load more as needed.

## Inherited Constraints

- Do NOT add new criteria checks — the spokes already did that
- Do NOT re-evaluate security or quality claims independently — read the spoke outputs
- The output path MUST be `../regression_verdict.md` (in the SUBTASK_regression workspace, not in this SUBTASK_verdict_synthesis workspace)
- Evidence in the final verdict cites the spoke evidence, which cites pinned commit `75c1eef`
