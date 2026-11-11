# Task: Synthesis Gate — sec_quality_findings.md

## Task Specification

**Slug**: SUBTASK_secq_synthesis  
**Task Kind**: synthesis  
**Depends on**: SUBTASK_sec_check, SUBTASK_quality_check  
**Status**: Pending  
**Assigned To**: swe-reviewer

### Objective

Act as the **verification gate** for the SUBTASK_sec_quality sub-DAG. Read the two spoke outputs (`security_raw_findings.md` and `quality_raw_findings.md`), verify they satisfy the contracts, and assemble them into `sec_quality_findings.md` following `../contracts/findings_schema.md`. Run the four-check model: contract verification, wiring, duplication detection, and code review of the combined output. If violations exist, schedule fix tasks (do not silently plug them).

### Context

This task is the synthesis gate for SUBTASK_sec_quality (see `../_GLOBAL.md`). Its output `sec_quality_findings.md` is the declared output of the SUBTASK_sec_quality spoke in the parent's DAG.

---

## Verification Gate: Four Checks

This task runs the synthesis four-check model — it is NOT a prose summary:

1. **Contract Verification**: Do `security_raw_findings.md` and `quality_raw_findings.md` satisfy the structural contracts declared in `../contracts/spoke_output_schema.md` and `../contracts/_MANIFEST.yaml`?
   - Does `security_raw_findings.md` carry a `## Security Findings` section with subsections for all three required concerns (HTML Injection in ssr.rs, DOM Spoofing in app.rs, Test Injection Safety in hydrate_wasm.rs)?
   - Does `quality_raw_findings.md` carry a `## Code Quality Findings` section and a `## What Was Examined and Found Clean` section?
   - Does every finding cite file + line at pinned commit `75c1eef`?

2. **Wiring Verification**: Are all concerns from the SUBTASK_sec_quality `_BRIEF.md` present and answered — no detached/dead concerns?
   - Security: HTML injection, DOM spoofing, test injection safety
   - Quality: app.rs new code, hydrate_wasm.rs new code, fresh non-blockers

3. **Duplication Detection**: Do the two spoke outputs overlap? (A concern that appears in both security and quality outputs needs reconciliation.) Flag duplicates rather than silently picking one.

4. **Synthesis Code Review**: Does the combined output read as a coherent, correctly-assembled findings document? Are blockers clearly marked? Are findings actionable (file + line + resolution)?

**Gate decision**: If all four checks PASS, assemble and write `sec_quality_findings.md`. If any check FAILS, schedule remediation fix tasks via `engine_amend_plan { add_task }` before writing the final output — do not silently plug violations.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Parent context | `../_GLOBAL.md` | Review scope, identities, constraints |
| Contract manifest | `../contracts/_MANIFEST.yaml` | Ownership and identity assertions |
| Spoke output schema | `../contracts/spoke_output_schema.md` | Structural requirements for each spoke output |
| Findings schema | `../contracts/findings_schema.md` | Required format for sec_quality_findings.md |
| Security spoke output | `../SUBTASK_sec_check/security_raw_findings.md` | Security findings from SUBTASK_sec_check |
| Quality spoke output | `../SUBTASK_quality_check/quality_raw_findings.md` | Quality findings from SUBTASK_quality_check |

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `sec_quality_findings.md` |
| Location | `../` (parent SUBTASK_sec_quality workspace) |

The output MUST follow `../contracts/findings_schema.md`:
- `## Security Findings` — assembled from security_raw_findings.md
- `## Code Quality Findings` — assembled from quality_raw_findings.md
- `## What Was Examined and Found Clean` — merged from both spoke outputs

The synthesis task writes `SYNTHESIS.md` at this workspace (its own terminal record), then calls `engine_resume_suspended` to fold the SUBTASK_sec_quality parent node.

---

## Success Criteria

- [ ] All four synthesis checks run (contract, wiring, duplication, review) and their outcomes recorded
- [ ] No identity assertion silently plugged — if a check fails, remediation tasks are scheduled
- [ ] `sec_quality_findings.md` assembled and written to parent workspace
- [ ] Every concern from SUBTASK_sec_quality _BRIEF.md appears in sec_quality_findings.md

---

## Suggested Methodology Files

**Task-type row matched**: "Synthesizing / verifying a hub-and-spoke decomposition" → Primary: Synthesis; Supporting: Code Review

Specific files to load:
- `synthesis/Synthesis_Overview_Methodology.md` — the four-check model; gate pass/fail decision; synthesis task as a verification gate (anchor, always first)
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify spoke outputs satisfy declared structural contracts
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — verify no concerns are detached or unanswered
- `synthesis/Synthesis_Duplication_Detection_Methodology.md` — detect overlap between spoke outputs
- `synthesis/Synthesis_Code_Review_Methodology.md` — quality review of combined output
- `synthesis/Synthesis_Remediation_Methodology.md` — how to inject fix tasks when gate fails

These are the parent's suggested methodologies. Load fewer if clearly inapplicable; load more as needed. The gate posture is mandatory; coverage depth is the child's judgment.

## Inherited Constraints

- Scope is ferric-ssr-r4 commits only: `7fb90c7`, `e625c3f`, `75c1eef`
- Do NOT re-raise non-blockers #229–#242
- Evidence must cite file + line at pinned commit `75c1eef`
- Do not reference overseer escalation comments from I267

## Out-of-Scope

- Re-doing the analysis (the spokes already did that) — this task only assembles and gates
- The 9 regression criteria — those are SUBTASK_reg_criteria's concern
