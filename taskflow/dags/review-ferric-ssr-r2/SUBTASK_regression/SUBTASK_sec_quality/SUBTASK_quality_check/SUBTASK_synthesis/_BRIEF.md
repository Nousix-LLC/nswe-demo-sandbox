# Task: Quality Findings Synthesis Gate — ferric-ssr-r4

## Task Specification

**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_app_quality, SUBTASK_test_quality
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

This task is a **verification gate**. It reads the two spoke outputs (`app_quality_raw.md` and `test_quality_raw.md`) and assembles them into `quality_raw_findings.md` conforming to `../../contracts/spoke_output_schema.md` §SUBTASK_quality_check. It verifies that every required concern from the SUBTASK_quality_check _BRIEF.md is covered before assembling, and assembles mechanically without introducing new analysis.

### Context

This task is the synthesis gate of SUBTASK_quality_check (see `../_GLOBAL.md`). Its inputs are the two spoke outputs. It does NOT perform independent code analysis — that is the spokes' responsibility. Its job is to verify coverage and assemble.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `../_GLOBAL.md` | Constraints, methodology posture |
| Spoke output contract | `../contracts/spoke_intermediate_schema.md` | Verify spokes conform to this |
| Parent spoke schema | `../../contracts/spoke_output_schema.md` | Required format for quality_raw_findings.md |
| app.rs spoke output | `../SUBTASK_app_quality/app_quality_raw.md` | Coverage + findings from app.rs review |
| hydrate_wasm.rs spoke output | `../SUBTASK_test_quality/test_quality_raw.md` | Coverage + findings from hydrate_wasm.rs review |

---

## Process

This task is a verification gate. It runs the following checks before assembling:

1. **Coverage check**: Does app_quality_raw.md cover the new conditional hydrate/mount dispatch (concern 1) AND fresh non-blockers in app.rs (concern 3 for app.rs)?
2. **Coverage check**: Does test_quality_raw.md cover hydrate_wasm.rs test code quality (concern 2) AND fresh non-blockers in hydrate_wasm.rs (concern 3 for hydrate_wasm.rs)?
3. **Schema conformance**: Does each spoke output follow spoke_intermediate_schema.md's required sections?

If any check fails, do NOT produce a passing quality_raw_findings.md — author FAILURE.md describing what was missing and why.

If all checks pass, assemble quality_raw_findings.md mechanically:
1. `## Code Quality Findings` — merge both spokes' findings sections (app.rs + hydrate_wasm.rs findings)
2. `## What Was Examined and Found Clean` — merge both spokes' "What Was Examined and Found Clean" sections

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `quality_raw_findings.md` |
| Location | `../` (parent SUBTASK_quality_check/ workspace) |

The output MUST follow `../../contracts/spoke_output_schema.md` §SUBTASK_quality_check. It MUST carry:
- `## Code Quality Findings` section conforming to the schema format
- `## What Was Examined and Found Clean` section listing every concern checked

---

## Success Criteria

- [ ] Both spoke outputs read and verified for coverage
- [ ] All required concerns from SUBTASK_quality_check _BRIEF.md covered across both spokes
- [ ] `quality_raw_findings.md` assembled at `../quality_raw_findings.md`
- [ ] Output conforms to `../../contracts/spoke_output_schema.md` §SUBTASK_quality_check
- [ ] No new independent analysis introduced by synthesis (assembly only)

---

## Suggested Methodology Files

**Task-type row matched**: "Synthesizing / verifying a hub-and-spoke decomposition" → Primary: Synthesis; Supporting: Code Review

Specific files to load:
- `synthesis/Synthesis_Overview_Methodology.md` — the four-check model; what a verification gate does. Load as anchor; this is the primary guide for running the gate.
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify spokes conform to contracts before assembling. Load to verify spoke conformance.
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — verify every declared concern is covered. Load to verify coverage.

The above are the parent's flagged methodologies based on the task type. The child agent SHOULD load these as a starting point but is the final judge of what its work requires.

## Inherited Constraints

- Scope is ferric-ssr-r4 commits only: `7fb90c7`, `e625c3f`, `75c1eef`
- Do NOT re-raise non-blockers #229–#242 (spokes already enforced this; synthesis does not independently re-raise)
- Evidence must cite file + line at pinned commit `75c1eef` (spokes already ensured this)
- Security concerns are out of scope

## Out-of-Scope

- Independent code analysis (the spokes did the analysis; this gate assembles only)
- Security surface analysis — that is SUBTASK_sec_check's concern
