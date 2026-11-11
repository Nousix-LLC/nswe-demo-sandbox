# _BRIEF.md — SUBTASK_synthesis

## Task Specification

**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_landing-states, SUBTASK_routing-ctas
**Status**: Pending

### Objective

This task is the **verification gate** for the spoke-ui-states subtree. It reads the two spoke
FINDINGS.md outputs, verifies they satisfy the identity assertions in `../contracts/_MANIFEST.yaml`,
and assembles the final `REVIEW.md` with explicit verdicts for AC-2, AC-3, and AC-4.

This is NOT a prose summary. It is a gate: the task asserts that all concerns are covered,
no finding is omitted or contradicted, and the combined REVIEW.md is correct — or it schedules
a remediation fix-task if a gap is detected.

### Context

This task is part of the spoke-ui-states subtree (see `_GLOBAL.md` in the parent workspace).

**Dependencies**: SUBTASK_landing-states (must be COMPLETED), SUBTASK_routing-ctas (must be COMPLETED)
**Dependents**: The parent DAG's `synthesis/` spoke reads `REVIEW.md` from this workspace

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, scope, constraint list |
| Ancestor hub | `../../_GLOBAL.md` | Full PR context and route table |
| Contract manifest | `../contracts/_MANIFEST.yaml` | Identity assertions to verify |
| Spoke A findings | `../SUBTASK_landing-states/FINDINGS.md` | AC-2, AC-3, header_nav review |
| Spoke B findings | `../SUBTASK_routing-ctas/FINDINGS.md` | AC-4 routing, CTA link, route annotation |

---

## Process Specification

This task runs the **four-check verification gate**:

### Check 1 — Contract verification
- Verify both FINDINGS.md files exist and follow the schema in `contracts/_MANIFEST.yaml`
- Verify the identity assertions hold:
  - Every AC-2, AC-3, and AC-4 sub-concern named in the hub's Scope section is addressed
  - The concern partition is clean (no concern claimed by both spokes)
  - Every finding cites the pinned commit + file + line

### Check 2 — Wiring / no-gap verification
- Enumerate the five concerns from the parent brief
- Confirm each concern appears in exactly one spoke's FINDINGS.md
- If a concern is unaddressed or duplicated, that is a gate failure requiring remediation

### Check 3 — Duplication detection
- Check whether both spokes reached the same code areas unexpectedly
- If both spokes assessed the same code path, the partition was violated — flag and remediate

### Check 4 — Code review of the combined findings
- Read all findings across both spokes
- Assess whether findings are supported by the evidence each spoke cited
- Assess severity labels for consistency: blockers in one spoke must be treated as blockers here
- Assess whether the combined findings form a coherent, complete verdict on AC-2, AC-3, and AC-4

### Gate decision
- **PASS**: All checks pass → proceed to assemble REVIEW.md and SYNTHESIS.md
- **FAIL**: Any check fails → schedule a remediation fix-task via `engine_amend_plan { add_task }`,
  author SUSPENSION.md, and suspend rather than producing a partial REVIEW.md

### Assembling REVIEW.md (gate PASS path)

Write `../REVIEW.md` (at the parent spoke-ui-states workspace). The file MUST include:

1. **Overall verdict**: PASS or FINDINGS
2. **AC-2 verdict**: with the evidence the spoke cited (clean or finding with location/severity)
3. **AC-3 verdict**: with evidence (clean or finding)
4. **AC-4 verdict**: synthesized from both spoke findings (header_nav from landing-states; routing from routing-ctas)
5. **Additional findings**: CTA link correctness and route annotation anomaly (from routing-ctas)
6. **Account of what was clean**: for each concern that passed, say what was examined and what was found sound

### Authoring SYNTHESIS.md

Write `../SYNTHESIS.md` at the parent workspace (`spoke-ui-states/SYNTHESIS.md`). This is both
this task's terminal record and the fold record that folds the parent node back to COMPLETED.

The file MUST record: how the spoke outputs were composed, which checks passed, and that REVIEW.md
was produced.

After writing both files, call:
1. `engine_report_status { status: "completed", artifact_path: "../SYNTHESIS.md", outputs: ["../REVIEW.md"] }`
2. `engine_resume_suspended { target_task_id: "<spoke-ui-states task id>", synthesized_task_id: "<this task id>", seam_path: "../SYNTHESIS.md" }`

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Primary output | `../REVIEW.md` (at spoke-ui-states workspace root) |
| Terminal record | `../SYNTHESIS.md` (fold record at spoke-ui-states workspace root) |

**REVIEW.md structure**:
```markdown
# Review — AC-2/3/4 UI States, Error Messages, and CTAs

## Verdict
[PASS | FINDINGS]

## AC-2 — Empty state
[verdict with evidence]

## AC-3 — Error state recoverability
[verdict with evidence]

## AC-4 — Sign-up / sign-in CTAs
[verdict with evidence; covers header_nav + routing path + link targets]

## Additional findings
[CTA link correctness, route annotation anomaly — each with location, principle, severity, resolution]

## What was checked and found clean
[Account of each concern that passed]
```

---

## Success criteria

- [ ] All four gate checks pass or gate failure is handled via remediation
- [ ] All five concerns from the parent brief appear exactly once in the combined findings
- [ ] Every finding cites file + line at pinned commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- [ ] `REVIEW.md` written at `spoke-ui-states/REVIEW.md` with explicit verdicts for AC-2, AC-3, AC-4
- [ ] `SYNTHESIS.md` written at `spoke-ui-states/SYNTHESIS.md` as the fold record
- [ ] `engine_resume_suspended` called to fold the parent spoke-ui-states node to COMPLETED

---

## Suggested Methodology Files

**Task-type row matched**: Synthesis/verification gate → Primary: `synthesis`, Supporting: `code-review`

Suggested files (from the methodology loader):
- `synthesis/Synthesis_Overview_Methodology.md` — the four-check gate model (always load first)
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify the contracts/_MANIFEST.yaml assertions
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — verify all concerns are covered with no gaps
- `synthesis/Synthesis_Code_Review_Methodology.md` — review the combined findings for quality and coherence
- `synthesis/Synthesis_Remediation_Methodology.md` — if the gate fails, how to schedule fix-tasks

These are the parent's flagged suggestions. The gate posture is mandatory (this task IS a
verification gate); the specific files and depth are your judgment.

## Inherited Constraints

- Repository: `Nousix-LLC/nswe-demo` only
- Pinned commit: `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Do not post to the PR (the parent DAG's synthesis child handles that)
- Findings point at repository file paths and lines; never name host paths, private IPs, or internal infrastructure
- REVIEW.md must be at `spoke-ui-states/REVIEW.md` (the declared output of the parent node)
- SYNTHESIS.md must be at `spoke-ui-states/SYNTHESIS.md` (the fold record location = parent workspace)
