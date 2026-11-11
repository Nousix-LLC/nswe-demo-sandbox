# Task: Synthesis Gate — Compile Code-Quality Review for PR #263

## Task Specification

**Slug**: spoke-synthesis
**Task Kind**: synthesis
**Depends on**: spoke-tests, spoke-correctness, spoke-code-health, spoke-safety-idiom, spoke-prose
**Status**: Pending

### Objective

Verify that all five analysis spokes have covered their assigned concerns, then compile their
findings into the single `REVIEW.md` declared by the parent `spoke-code-quality` brief.
This is a **verification gate**, not a prose summary.

### Context

This task is part of the code-quality review decomposition. See `../_GLOBAL.md` for the full
concern assignment table, the dependency graph, and the ownership manifest in `../contracts/`.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Concern assignments, ownership table, identities |
| Contract schema | `../contracts/findings_schema.md` | Expected FINDINGS.md structure |
| Manifest | `../contracts/_MANIFEST.yaml` | Ownership assertions and identities |
| Tests findings | `../spoke-tests/FINDINGS.md` | Concerns 1, 2, 5 |
| Correctness findings | `../spoke-correctness/FINDINGS.md` | Concerns 3, 4 |
| Code health findings | `../spoke-code-health/FINDINGS.md` | Concerns 6, 7 |
| Safety/idiom findings | `../spoke-safety-idiom/FINDINGS.md` | Concerns 8, 10 |
| Prose findings | `../spoke-prose/FINDINGS.md` | Concern 9 |

---

## Process Specification — Verification Gate

This task MUST run as a verification gate against the four-check model. Do not produce a
prose summary first. Run the checks, then produce the output.

### Check 1: Coverage — are all 10 concerns accounted for?

For each of the 10 concerns in `../_GLOBAL.md § Concern Assignments`, verify that it appears in
exactly one FINDINGS.md's Clean Account section. Flag any concern missing from every spoke's
Clean Account.

### Check 2: Structure — does each FINDINGS.md conform to the schema?

Verify each FINDINGS.md against `../contracts/findings_schema.md`:
- Has a `## Verdict` section (PASS or FINDINGS)
- Has a `## Clean Account` section with an entry for each assigned concern
- Each finding (when present) has Location, Principle, Why it matters, Severity, Satisfying condition

### Check 3: Identity — do the ownership and identity assertions hold?

Per `../contracts/_MANIFEST.yaml`:
- Each analysis spoke owns exactly its declared output file
- No concern is claimed by two spokes simultaneously
- All five FINDINGS.md files are present

### Check 4: Prose — does the combined output pass the plain-voice bar?

Scan findings and clean-account entries across all five spokes for AI-writing tells
(per `../contracts/findings_schema.md § Prose Bar`). Note any cluster-level violations
that slipped through the spoke-prose spoke's own assessment.

### On gate failure

If any check fails (a concern is uncovered, a FINDINGS.md is missing or malformed, an
identity is broken, or a prose cluster is blocker-level), do NOT silently plug the gap.
Either:
- If the gap is fixable within this invocation (e.g., a structurally present finding that
  just needs re-labeling), fix it and document the correction in SYNTHESIS.md
- If the gap requires re-running an analysis spoke, inject a remediation task via
  `engine_amend_plan { add_task }` and suspend rather than producing a defective REVIEW.md

### On gate pass

Compile the REVIEW.md. The structure must be:

```markdown
# Code Quality Review — PR #263

## Verdict
[PASS | FINDINGS]

## Summary
[One short paragraph: what was reviewed and the overall verdict. No inflated filler.]

## Concern Findings

### Concern 1 — [label]
[Finding or clean-account entry, citing spoke-tests/FINDINGS.md]

... (all 10 concerns)

## Findings Log

[All findings from all spokes, deduplicated, with their Location / Principle / Severity /
Satisfying condition. Blockers listed first.]

## Clean Account

[Consolidated clean-account: for each concern found clean across spokes, what was checked
and what was found sound.]
```

---

## Output Specification

| Artifact | Location | Role |
|----------|----------|------|
| `REVIEW.md` | `../REVIEW.md` (= `spoke-code-quality/REVIEW.md`) | The declared output of `spoke-code-quality` |
| `SYNTHESIS.md` | `../SYNTHESIS.md` (= `spoke-code-quality/SYNTHESIS.md`) | Fold record — gate results, checks run, identities verified |

After writing both files, call:
```
engine_report_status { status: "completed", outputs: ["../REVIEW.md"], artifact_path: "../SYNTHESIS.md" }
engine_resume_suspended { target_task_id: <spoke-code-quality task id>, synthesized_task_id: <this task id>, seam_path: "../SYNTHESIS.md" }
```

---

## Success Criteria

- All four gate checks run and documented in SYNTHESIS.md
- All 10 concerns covered in REVIEW.md
- Blockers listed before non-blocking findings
- REVIEW.md prose passes the plain-voice bar
- No internal infrastructure details in REVIEW.md
- `../REVIEW.md` exactly matches the path declared in the parent brief

---

## Suggested Methodology Files

Domain Mapping match: **Synthesizing / verifying a hub-and-spoke decomposition** →
Primary: `Synthesis`, Supporting: `Code Review`, `Code Quality`

Specific files (required, not suggested):
- `synthesis/Synthesis_Overview_Methodology.md` — the four-check gate model; load first
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify the contracts/ manifest
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — verify all concerns are wired to
  exactly one spoke
- `synthesis/Synthesis_Code_Review_Methodology.md` — the prose bar and overall quality gate
- `synthesis/Synthesis_Remediation_Methodology.md` — how to inject a remediation task if a
  gate check fails

These are required starting points for a synthesis gate. Load them in this order.

## Inherited Constraints

- Write `../REVIEW.md`, not `REVIEW.md` in this workspace — the output must be at the parent path
- Write `../SYNTHESIS.md` for the fold record
- Do not post to the PR
- Prose in REVIEW.md must pass the plain-voice bar
- Findings point at repository file paths and lines at pinned commit
  `decb6196c2c1e6ed421d393a642f0c844cc333ba`; no host paths, private IPs, or infrastructure details
- Repository: `Nousix-LLC/nswe-demo` only
