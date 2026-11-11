# Task: Synthesis — Combine Verdicts and Fold Parent

## Task Specification

**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_regression-check, SUBTASK_code-quality, SUBTASK_security
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Read the three spoke verdicts (regression-check, code-quality, security), verify the
gate checks all pass, combine them into a single `verdict-regression-quality-sec.md`
output file, and fold the parent task (SUBTASK_regression-quality-sec) from SUSPENDED
to COMPLETED by writing `SYNTHESIS.md` and calling `engine_resume_suspended`.

This is the terminal gate for the SUBTASK_regression-quality-sec subtree.

### Context

SUBTASK_regression-quality-sec decomposed into three parallel spokes:
- `SUBTASK_regression-check` → `regression-check.md` (9 previously-clean criteria)
- `SUBTASK_code-quality` → `code-quality.md` (cfg-gate pattern, test file)
- `SUBTASK_security` → `security.md` (HTML injection, escaping gaps)

This synthesis task depends on all three. It runs after all spokes are complete.

The parent spoke in the DAG is `SUBTASK_regression-quality-sec`. Its declared output
(`verdict-regression-quality-sec.md`) is owned by this synthesis task. The fold record
(`SYNTHESIS.md`) must also be written here, then `engine_resume_suspended` must be called
to close out the parent.

---

## Input Specification

### Required Inputs

| Input | Location | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Subtree constraints, identities, task structure |
| Contracts manifest | `../contracts/_MANIFEST.yaml` | Identity checks to verify before combining |
| Regression check verdict | `../SUBTASK_regression-check/regression-check.md` | Spoke 1 output |
| Code quality verdict | `../SUBTASK_code-quality/code-quality.md` | Spoke 2 output |
| Security verdict | `../SUBTASK_security/security.md` | Spoke 3 output |
| Parent GLOBAL | `../../_GLOBAL.md` | Full DAG context (constraints, brief of parent spoke) |
| Parent brief | `../../SUBTASK_regression-quality-sec/_BRIEF.md` | Declared success criteria for this spoke overall |

---

## Process: Four-Check Gate

Before combining, run all four identity checks from `contracts/_MANIFEST.yaml`.
If any check fails, do NOT write the verdict — write a `FAILURE.md` and report failed.

### Check 1: all-9-criteria-covered

`regression-check.md` must contain a named section for every one of the 9 previously-clean
criteria: REQ-SSR-001, REQ-SSR-002, REQ-SSR-003, REQ-SSR-004, REQ-SSR-005,
REQ-HYD-001, REQ-HYD-002, REQ-HYD-004, REQ-MIS-001, REQ-MIS-002.

Verify by reading `regression-check.md` and confirming all 9 appear.

### Check 2: verdict-covers-all-spoke-areas

The combined `verdict-regression-quality-sec.md` must address all three areas:
regression check (9 criteria), code quality (app.rs + hydrate_wasm.rs), and security
(injection paths, escaping gaps). Verify after drafting the combined verdict.

### Check 3: overall-verdict-consistent

The overall PASS/FAIL verdict in `verdict-regression-quality-sec.md` must be consistent
with findings across all three spokes. If any spoke returns FAIL, the overall verdict
must be FAIL. If all spokes return PASS or UNCHANGED, the overall may be PASS.
Verify before writing.

### Check 4: spoke completeness

Each spoke file exists and contains an Overall Verdict line. If a file is missing or
malformed, treat it as a gate failure.

---

## Output Specification

### Primary output: verdict-regression-quality-sec.md

**File**: `verdict-regression-quality-sec.md`
**Location**: `../` (parent workspace: `SUBTASK_regression-quality-sec/`)

This is the declared output of the whole SUBTASK_regression-quality-sec task. The parent
DAG's synthesis task reads this file. Write it only after all four gate checks pass.

The combined verdict must be a cohesive document — not a concatenation of the three
spoke files. It should:
- Have a brief summary up front (overall verdict + one-sentence rationale)
- Address all three areas in clearly labeled sections
- Include all FAIL findings from any spoke at the detail level needed to act on them
- Summarize PASS/UNCHANGED findings concisely — the reader should be able to verify
  without having to open the spoke files, but the spoke files are the detail record
- List any fresh non-blocking issues found across all spokes
- End with a clear overall verdict line: `**Overall Verdict: PASS**` or `**Overall Verdict: FAIL**`

```markdown
# Regression, Quality, and Security — Verdict

## Summary

[1–2 sentences: overall verdict and what was checked]

## Regression Check — 9 Previously-Clean Criteria

**Verdict: [PASS | FAIL]**

[Summary of each criterion — one line each; expand only where a criterion failed
or the new commits touched it. Mark each: PASS, UNCHANGED, or FAIL.]

[If any criteria FAIL: include the detail from regression-check.md needed to act on the finding]

## Code Quality — New Code

**Verdict: [PASS | FAIL]**

### app.rs
[Summary of cfg-gate pattern findings]

### hydrate_wasm.rs
[Summary of test file findings]

[If FAIL: include the specific issue and what must be fixed]

## Security — New Code

**Verdict: [PASS | FAIL]**

[Summary of HTML injection, escaping, test file security findings]

[If FAIL: include the specific issue and what must be fixed]

## Fresh Non-Blocking Issues

[List from all three spokes combined, with file:line and brief description]
[Or: "None found across all three review areas"]

---

**Overall Verdict: [PASS | FAIL]**
```

### Fold record: SYNTHESIS.md

**File**: `SYNTHESIS.md`
**Location**: `../` (parent workspace: `SUBTASK_regression-quality-sec/`)

Write this AFTER `verdict-regression-quality-sec.md` is written. It is the fold record
consumed by `engine_resume_suspended` to close out the parent task.

```markdown
# Synthesis: SUBTASK_regression-quality-sec

**Synthesized by**: SUBTASK_synthesis
**Status**: COMPLETED

## Gate Checks

- [x] all-9-criteria-covered
- [x] verdict-covers-all-spoke-areas
- [x] overall-verdict-consistent
- [x] spoke-completeness

## Outputs Produced

- `verdict-regression-quality-sec.md` — combined review verdict
- `SYNTHESIS.md` — this file (fold record)

## Fold

This record folds SUBTASK_regression-quality-sec SUSPENDED → COMPLETED.
```

---

## Fold Procedure

After writing both output files:

1. Call `engine_resume_suspended`:
   - `target_task_id`: the task id of SUBTASK_regression-quality-sec (the suspended parent)
   - `synthesized_task_id`: the task id of this synthesis task (SUBTASK_synthesis)
   - `seam_path`: absolute path to the `SYNTHESIS.md` fold record just written

2. Then take the completed terminal path:
   - `mcp__hal__report_status { status: "completed", decompose_evaluation: "Atomic",
     outputs: ["../verdict-regression-quality-sec.md", "../SYNTHESIS.md"],
     artifact_path: "COMPLETE.md" }`

Write `COMPLETE.md` before the terminal call.

---

## Suggested Methodology Files

**Task type**: "Synthesis" → Primary: `synthesis`

Specifically:
- `synthesis/Synthesis_Overview_Methodology.md` — synthesis gate checks, fold procedure
- `code-review/CodeReview_Process_Methodology.md` — verification-first review posture

These are suggested starting points. The child agent retains final judgment.

---

## Success Criteria

- [ ] All four gate checks pass before writing the combined verdict
- [ ] `verdict-regression-quality-sec.md` written to parent workspace (`../`)
- [ ] All three spoke areas addressed in the combined verdict
- [ ] Overall PASS/FAIL verdict consistent with spoke findings
- [ ] `SYNTHESIS.md` fold record written to parent workspace (`../`)
- [ ] `engine_resume_suspended` called to fold parent SUSPENDED→COMPLETED

---

## Inherited Constraints

- **Repository**: Nousix-LLC/nswe-demo, branch `work/ferric-ssr-r1`, PR #228
- **Commits under inspection**: `7fb90c7`, `e625c3f`, `75c1eef`
- **Do not re-raise**: Issues #229–#242
- **Do not reference**: Overseer I267 escalation comments
- **Non-blockers**: List in verdict only — do NOT file GitHub issues. The parent DAG's
  synthesis task (`review-ferric-ssr-r2/SUBTASK_synthesis`) decides whether to file issues.
- **Prose bar**: No AI-tell patterns in output text
