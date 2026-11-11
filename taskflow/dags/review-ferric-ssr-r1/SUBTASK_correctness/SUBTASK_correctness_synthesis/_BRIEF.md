# SUBTASK_correctness_synthesis — Correctness Review Verification Gate

## Task Specification

**Slug**: SUBTASK_correctness_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_ssr_render, SUBTASK_hydration, SUBTASK_axum_mismatch
**Status**: Pending

### Objective

Verification gate: read the three spoke findings, assert the contract identities (marker format consistency,
all criteria covered, non-goal confirmed), and produce `correctness_findings.md` per the specified output
format. If a contract identity fails, do not silently plug it — report the gap as a finding.

---

## Context

This task is part of the PR #228 Correctness Review (see `../_GLOBAL.md`). It is a synthesis task (a gate,
not a summary): its job is to verify that the spokes compose correctly and to assemble the declared output.

**Depends on**: SUBTASK_ssr_render (must be COMPLETED), SUBTASK_hydration (must be COMPLETED),
SUBTASK_axum_mismatch (must be COMPLETED)
**Dependents**: SUBTASK_synthesis in the parent DAG reads `../correctness_findings.md`

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Shared context | `../_GLOBAL.md` | Contract, identities, output format |
| Contract | `../contracts/_MANIFEST.yaml` | Schema and identities to verify |
| SSR findings | `../SUBTASK_ssr_render/ssr_render_findings.md` | Verdicts for REQ-SSR-001–005; marker schema (REQ-SSR-004) |
| Hydration findings | `../SUBTASK_hydration/hydration_findings.md` | Verdicts for REQ-HYD-001–004; marker schema (REQ-HYD-004) |
| Axum/mismatch findings | `../SUBTASK_axum_mismatch/axum_mismatch_findings.md` | Verdicts for REQ-SSR-006, REQ-MIS-001–002; non-goal confirmation |

---

## Verification Gate: What This Task Runs

This is a **verification gate**, not a prose summary. Run the following checks before assembling the output:

### Check 1: Coverage
Verify that every in-scope criterion has a verdict in the spoke findings:
- REQ-SSR-001 through REQ-SSR-005 (from ssr_render_findings.md)
- REQ-HYD-001 through REQ-HYD-004 (from hydration_findings.md)
- REQ-SSR-006, REQ-MIS-001, REQ-MIS-002 (from axum_mismatch_findings.md)
- REQ-SSR-007 non-goal confirmation (from axum_mismatch_findings.md)

If any criterion is missing: add a FINDING (BLOCKER) in the output for that criterion.

### Check 2: Marker Format Consistency (REQ-SSR-004 vs REQ-HYD-004)
Compare the marker schema documented in `ssr_render_findings.md` (REQ-SSR-004 section) with the marker schema
documented in `hydration_findings.md` (REQ-HYD-004 section).

- If they agree: note the confirmed consistency in the output
- If they disagree or one is missing: add a FINDING (BLOCKER) reporting the inconsistency with evidence

**Do not silently plug this check.** A silent plug here would let the SSR and hydration paths ship with
incompatible marker formats — the most likely root cause of a full hydration failure.

### Check 3: Non-Goal Confirmed
Verify that axum_mismatch_findings.md contains an explicit non-goal confirmation for REQ-SSR-007. If it is
absent: add a note that the non-goal was not explicitly confirmed.

### Check 4: Spoke Output Quality
Briefly check that each spoke finding cites concrete code evidence (not just test assertions) and that no
finding conflates host paths with repository paths. Flag any spoke finding that lacks citable evidence as
needing clarification.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| File | `correctness_findings.md` |
| Location | parent workspace (`../`) — i.e., `SUBTASK_correctness/correctness_findings.md` |

### Output Structure

The output format is specified in `../_BRIEF.md` (parent task brief):

```markdown
# PR #228 Correctness Findings

## Summary
<one-paragraph verdict: which criteria are met, which have findings, overall correctness assessment>

## Findings by Criterion

### REQ-SSR-001 — render_to_string renders without DOM
**Status**: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
**What was checked**: ...
**Evidence**: ...
**Finding** (if any): ...

[Repeat for every criterion in scope]

## Marker Format Consistency
**SSR format (REQ-SSR-004)**: ...
**Hydration format (REQ-HYD-004)**: ...
**Consistency check**: CONSISTENT | INCONSISTENT (finding below)

## Non-goal boundary
### REQ-SSR-007 / #225 — Async resource state (non-goal)
**Status**: CONFIRMED NON-GOAL
**What was checked**: ...
```

**Note on file path**: The output file is `correctness_findings.md` in the **parent** workspace
(`SUBTASK_correctness/correctness_findings.md`), not in this task's own workspace. Write it at
`../correctness_findings.md` relative to this workspace, which resolves to the correct location.

---

## Success Criteria

- [ ] All four gate checks run (coverage, marker consistency, non-goal, spoke quality)
- [ ] Marker format consistency explicitly verified — no silent plug
- [ ] `correctness_findings.md` exists at `../correctness_findings.md` before this task reports completed
- [ ] The output follows the specified structure from the parent brief
- [ ] Every finding cites files and line numbers in `Nousix-LLC/nswe-demo` (never host paths)
- [ ] This task reports `status=completed` with `outputs: ["<absolute path to correctness_findings.md>"]`

---

## Suggested Methodology Files

**Task-type row matched**: "Synthesizing / verifying a hub-and-spoke decomposition" → Primary: `Synthesis`;
Supporting: `Code Review`, `Code Quality`

Specific files:
- `synthesis/Synthesis_Overview_Methodology.md` — the four-check gate model; always load this first
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verifying the contract identities (marker
  format consistency is a contract identity from `../contracts/_MANIFEST.yaml`)
- `synthesis/Synthesis_Code_Review_Methodology.md` — reviewing the spoke outputs as a combined body
- `code-review/CodeReview_Process_Methodology.md` — governs how to structure the final review output

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but
is the final judge — load fewer if some are clearly inapplicable.

---

## Inherited Constraints

- **Non-goal**: #225/REQ-SSR-007 is not a deficiency; confirm it is absent/stubbed
- **Read-only**: Do not modify source code (this is a synthesis task; it only reads spoke outputs and
  writes the final correctness_findings.md)
- **No silent plugs**: The marker format consistency check MUST produce a visible result, not be skipped
- **Line citations**: All findings cite files and line numbers in `Nousix-LLC/nswe-demo`, never host paths
- **Output path**: Write to `../correctness_findings.md` (the parent workspace), not this workspace
