# SUBTASK_hyd_synthesis — hydrate() Findings Synthesis Gate

## Task Specification

**Slug**: SUBTASK_hyd_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_hyd001, SUBTASK_hyd002, SUBTASK_hyd003, SUBTASK_hyd004
**Status**: Pending

### Objective

This task is the **verification gate** for the SUBTASK_hydration subtree. It reads the four criterion
findings, verifies that every acceptance criterion (REQ-HYD-001–004) has an evidence-backed verdict,
cross-checks the marker schema from SUBTASK_hyd004 against the SSR render findings, and produces
the declared output `hydration_findings.md` at the SUBTASK_hydration workspace. It then writes
`SYNTHESIS.md` there and folds the parent.

This is NOT a prose summary. It MUST run the verification gate: either assert coverage (PASS) or
schedule remediation fix-tasks (FAIL).

---

## Context

This task is part of the SUBTASK_hydration subtree (see `../_GLOBAL.md`).

**Depends on**: SUBTASK_hyd001, SUBTASK_hyd002, SUBTASK_hyd003, SUBTASK_hyd004 (all must be COMPLETED)
**Produces**: `../hydration_findings.md` (at SUBTASK_hydration/) and `../SYNTHESIS.md` (fold record)

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Shared context | `../_GLOBAL.md` | Constraints and expected output structure |
| REQ-HYD-001 finding | `../SUBTASK_hyd001/criterion_001.md` | DOM walk verdict |
| REQ-HYD-002 finding | `../SUBTASK_hyd002/criterion_002.md` | Signal propagation verdict |
| REQ-HYD-003 finding | `../SUBTASK_hyd003/criterion_003.md` | WASM entry point verdict |
| REQ-HYD-004 finding | `../SUBTASK_hyd004/criterion_004.md` | Marker schema verdict (critical) |

---

## Verification Gate

Run the following four checks before writing the output:

### Check 1 — Coverage: Every criterion has an evidence-backed verdict
Verify that each of `criterion_001.md` through `criterion_004.md` exists and contains:
- A named status (CLEAN / FINDING (BLOCKER) / FINDING (NON-BLOCKER))
- At least one file:line evidence citation in `Nousix-LLC/nswe-demo`

If any criterion file is missing or its verdict is unsupported by evidence, this check FAILS and
you MUST inject a fix-task via `engine_amend_plan { add_task }` targeting the gap rather than
papering over it.

### Check 2 — Marker Schema: Cross-check with SUBTASK_ssr_render
Verify that `criterion_004.md` contains the mandatory `## Marker Schema` section with attribute
name, value format, and determinism mechanism.

Note: the full cross-check against what SUBTASK_ssr_render found for REQ-SSR-004 belongs to the
parent synthesis (SUBTASK_correctness_synthesis). Your obligation here is to verify the section
exists and is populated, and to surface any internal inconsistency you observe.

### Check 3 — No finding inflated or deflated
Review each criterion verdict for severity calibration:
- A BLOCKER must be a genuine correctness or safety issue
- A preference must not be called a BLOCKER
- An absence of test evidence should be flagged (non-blocker unless criterion explicitly requires a test)

### Check 4 — Prose hygiene
Review the combined text for AI-writing tells: moral/character adjectives ("honest", "genuine"),
narrated candor ("stated plainly"), unnamed contrast pairs, slot-fill templates, inflated filler
(*seamless*, *robust*, *comprehensive*). Request changes where the density is flagged.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| File 1 | `hydration_findings.md` at `../` (the SUBTASK_hydration workspace) |
| File 2 | `SYNTHESIS.md` at `../` (fold record — also your terminal artifact) |

### hydration_findings.md Structure

```markdown
# hydrate() Findings (REQ-HYD-001–004)

## Summary
<one paragraph: overall verdict on the hydrate() implementation>

## Findings by Criterion

### REQ-HYD-001 — hydrate() attaches without re-creating nodes
**Status**: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
**What was checked**: ...
**Evidence**: `<file>:<line>` (or `<file>:<start>–<end>`)
**Finding** (if any): ...

### REQ-HYD-002 — Signal updates propagate post-hydration
[same structure]

### REQ-HYD-003 — hydrate() called once from WASM entry point
[same structure]

### REQ-HYD-004 — Marker format consistency
[same structure]

## Marker Schema (REQ-HYD-004) — for synthesis cross-check
**Attribute name**: ...
**Value format**: ...
**Determinism mechanism**: ...
```

### SYNTHESIS.md (fold record) Structure

The SYNTHESIS.md at `../` (the SUBTASK_hydration workspace) is BOTH your terminal record AND the
fold record consumed by `engine_resume_suspended`. Write it at `../SYNTHESIS.md` before your
terminal `engine_report_status { status: "completed", artifact_path: "../SYNTHESIS.md" }` call.
Then call `engine_resume_suspended` with:
- `target_task_id`: the SUBTASK_hydration task id (find it from the taskflow context)
- `synthesized_task_id`: your own task id
- `seam_path`: the absolute path to `../SYNTHESIS.md`

---

## Success Criteria

- [ ] Check 1 passes: all 4 criteria have evidence-backed verdicts
- [ ] Check 2 passes: marker schema section is present and populated in criterion_004.md
- [ ] Check 3 passes: no severity inflation or deflation found (or fix-tasks injected)
- [ ] Check 4 passes: prose is clean (or findings noted)
- [ ] `hydration_findings.md` exists at `../hydration_findings.md`
- [ ] `SYNTHESIS.md` exists at `../SYNTHESIS.md`
- [ ] `engine_resume_suspended` called to fold the SUBTASK_hydration parent

---

## Suggested Methodology Files

**Task-type row matched**: "Synthesizing / verifying a hub-and-spoke decomposition (contract + wiring
+ dedup + review gate)" → Primary: `synthesis`; Supporting: `code-review`, `code-quality`.

Specific files (Synthesis bundle):
- `synthesis/Synthesis_Overview_Methodology.md` — ALWAYS first; the four-check model, the gate
  pass/fail decision, the SYNTHESIS.md schema. Required before any other synthesis file.
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify that each spoke satisfied its
  declared contract (each criterion has an evidence-backed verdict).
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — verify that the wiring between spokes
  is correct (the marker schema from hyd004 flows into the cross-check).
- `synthesis/Synthesis_Code_Review_Methodology.md` — synthesis-level code review over combined
  output; prose hygiene; severity calibration.
- `synthesis/Synthesis_Remediation_Methodology.md` — how to inject fix-tasks when a check fails
  rather than papering over the gap.

Also:
- `code-review/CodeReview_Checklist_Methodology.md` — severity calibration; CLEAN vs FINDING.

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting
point but is the final judge.

---

## Inherited Constraints

- Scope is synthesis of REQ-HYD-001–004 only
- Read-only: do not modify source code
- All findings cite files and line numbers in `Nousix-LLC/nswe-demo`, never host paths
- Non-blockers: flag but do not hold landing
- **The marker schema section in `hydration_findings.md` is mandatory** — the parent synthesis
  (SUBTASK_correctness_synthesis) depends on it
- If a gate check FAILS, inject fix-tasks; do not paper over the gap

## Out-of-Scope Methodologies

- Decomposition methodologies (`decomposition/`) — synthesis is reassembly, not splitting
- `rust/Rust_Web_Services_Axum_Methodology.md` — Axum is covered by SUBTASK_axum_mismatch
