# SUBTASK_synthesis — PR #228 Review Synthesis (Verification Gate)

## Task Specification

**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_correctness, SUBTASK_code_quality, SUBTASK_security_xss, SUBTASK_security_infra
**Status**: Pending

### Objective

This task is a **verification gate**. It reads the four spoke findings, determines the final
APPROVE or REQUEST-CHANGES verdict, posts the review on GitHub PR #228, files any non-blocking
findings as board issues (de-duplicated against the board), and writes the authoritative `SYNTHESIS.md`
at the parent workspace root (`taskflow/dags/review-ferric-ssr-r1/SYNTHESIS.md`).

---

## Context

See `_GLOBAL.md` (parent workspace) for PR coordinates, acceptance criteria, and constraints.

**Depends on**: SUBTASK_correctness, SUBTASK_code_quality, SUBTASK_security_xss, SUBTASK_security_infra
**Dependents**: none (this is the synthesis hub; it folds the parent into COMPLETED)

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Shared context | `../_GLOBAL.md` | PR coordinates, criteria, constraints |
| Correctness findings | `../SUBTASK_correctness/correctness_findings.md` | Acceptance-criteria verdict |
| Code quality findings | `../SUBTASK_code_quality/code_quality_findings.md` | Quality verdict |
| XSS security findings | `../SUBTASK_security_xss/security_xss_findings.md` | XSS / HTML escaping verdict |
| Infra exposure findings | `../SUBTASK_security_infra/security_infra_findings.md` | Infrastructure and supply-chain verdict |
| PR #228 | `gh pr view 228 --repo Nousix-LLC/nswe-demo` | PR metadata for posting review |
| Open issues board | `gh issue list --repo Nousix-LLC/nswe-demo` | De-duplicate non-blocking findings before filing |

---

## Verification Gate: Four Checks

This task MUST run all four checks. It passes only if all checks pass. If any check fails, it
schedules remediation (or records the blocker) rather than silently plugging.

### Check 1 — Blocker scan

Review all four spoke outputs for any finding classified as BLOCKER. If any blocker finding exists:
- The verdict is **REQUEST-CHANGES**
- The blocker finding is included in the GitHub review with clear remediation guidance
- The synthesis halts (does NOT approve)

### Check 2 — Coverage verification

Verify that every acceptance criterion from #223, #224, #226 has a named finding (clean or
finding) in `correctness_findings.md`. Every criterion must be accounted for. Missing criteria
coverage is a gap in the review — record the gap in the SYNTHESIS.md under "Review gaps".

### Check 3 — Non-blocker triage

Collect all findings classified as NON-BLOCKER across all four spoke outputs. For each:
- Check whether a substantially identical issue already exists as an open GitHub issue on the board
- File each genuinely new non-blocking finding as a backlog GitHub issue, linked to PR #228 and
  the relevant acceptance-criterion issue (#223, #224, or #226)
- Record the filed issue numbers in SYNTHESIS.md

### Check 4 — Prose quality pass

Before posting, run the avoid-ai-writing checklist over your own review text (the GitHub review
comment/review body):
- Remove moral/character adjectives attached to code artifacts (honest, genuine, robust, seamless,
  comprehensive as decoration)
- Remove narrated candor (stated plainly, to be honest, let's be clear)
- Remove unnamed contrast pairs (real X vs. fake kind; not X, it's Y)
- Remove slot-fill templates (a [adjective] step toward [noun])
- Remove padding threes and stacked Moreover/Furthermore
The review text must pass this check before it is posted.

---

## Action Sequence

1. Read all four spoke outputs and the shared context
2. Run Check 1 — classify verdict (APPROVE or REQUEST-CHANGES)
3. Run Check 2 — verify criterion coverage; note any gaps
4. Run Check 3 — triage non-blockers; check board for duplicates; file new issues
5. Run Check 4 — apply prose quality check to draft review text
6. Post the review on PR #228 (using `gh pr review` or `gh pr comment`; if same-account
   restrictions prevent formal review status, post as a review comment that carries the verdict)
7. Write `SYNTHESIS.md` at the parent workspace root (`../SYNTHESIS.md` = `taskflow/dags/review-ferric-ssr-r1/SYNTHESIS.md`)
8. Report `status: "completed"`, `artifact_path: "taskflow/dags/review-ferric-ssr-r1/SYNTHESIS.md"`,
   `outputs: [...]`

---

## Output Specification

### Primary Output

`SYNTHESIS.md` at the **parent workspace root**: 
`/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-ferric-ssr-r1/SYNTHESIS.md`

This file is both the synthesis task's terminal record AND the fold record that completes the
parent. Write it once at the parent workspace root; do not write a separate `COMPLETE.md`.

### SYNTHESIS.md Structure

```markdown
# Review Synthesis — PR #228 ferric SSR/hydration

## Verdict
APPROVE | REQUEST-CHANGES

## Concern-by-Concern Account

### 1. Correctness
<what was checked, what was found — finding or clean, severity>

### 2. Code Quality and Design
<what was checked, what was found — finding or clean, severity>

### 3. Security — HTML Escaping
<what was checked, what was found — finding or clean, severity>

### 4. Security — Infrastructure Exposure
<what was checked, what was found — finding or clean, severity>

## Blockers
<list blockers that must be resolved before landing, or "None">

## Non-Blocking Findings Filed as Issues
<list each finding, its severity, and the GitHub issue filed>

## Review Gaps
<any criteria not covered, or "None">

## GitHub Review
<link to the posted review comment or review on PR #228>
```

### Additional Outputs

- Filed GitHub issues (non-blocking findings): list in SYNTHESIS.md
- GitHub review posted on PR #228: include the URL in SYNTHESIS.md

---

## Success Criteria

- SYNTHESIS.md exists at `taskflow/dags/review-ferric-ssr-r1/SYNTHESIS.md`
- Every acceptance criterion has a verdict entry in SYNTHESIS.md
- Every blocker (if any) appears in both the GitHub review and SYNTHESIS.md
- Every non-blocking finding is either de-duplicated against an existing issue or filed as a new one
- The GitHub review is posted on PR #228
- Prose in the GitHub review and SYNTHESIS.md passes the avoid-ai-writing check

---

## Suggested Methodology Files

**Task-type row matched**: "Synthesizing / verifying a hub-and-spoke decomposition" → Primary: `Synthesis`; Supporting: `Code Review`, `Code Quality`

Specific files:
- `synthesis/Synthesis_Overview_Methodology.md` — the four-check model, what a synthesis/verification gate is and how it works (always load first)
- `synthesis/Synthesis_Code_Review_Methodology.md` — synthesis code review of combined output; applicable to assembling findings across spokes
- `code-review/CodeReview_Process_Methodology.md` — how to structure and post the final review
- `code-review/CodeReview_Feedback_Guidelines_Methodology.md` — writing actionable, evidence-backed, non-inflated findings

These are the parent's flagged methodologies. Load fewer if some are clearly inapplicable; load more if the brief reveals additional surface.

## Inherited Constraints

- **Non-goal**: #225 / REQ-SSR-007 must NOT appear as a blocker or finding in the posted review
- **Read-only**: Do not modify source code
- **Verdict authority**: SYNTHESIS.md is the authoritative landing decision; GitHub review status
  may be downgraded by platform same-account rules but SYNTHESIS.md verdict stands
- **Host detail**: The SYNTHESIS.md and GitHub review must not contain any host paths, Tailscale
  IPs, internal server URLs, or taskflow directory paths
- **Non-blockers as issues**: Every genuine non-blocking finding must be filed as an issue on the
  board (de-duplicated), not suppressed
- **Prose quality**: The avoid-ai-writing check applies to both the GitHub review text and the
  SYNTHESIS.md prose — this is Check 4 and is mandatory

## Out-of-Scope Methodologies

- `decomposition/` — synthesis is reassembly, not splitting; never load decomposition content here
- `rust/Rust_Unsafe_FFI_Methodology.md` — not applicable to this SSR review
- `testing/` spoke-level methodologies — the spokes already evaluated tests; do not re-audit at the synthesis level
