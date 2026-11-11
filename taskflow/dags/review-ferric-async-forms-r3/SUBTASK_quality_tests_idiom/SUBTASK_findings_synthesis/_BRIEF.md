# Task: Findings Synthesis — Verification Gate, PR #193 Concerns 2/3/6/7

## Task Specification

**Slug**: SUBTASK_findings_synthesis
**Task Kind**: synthesis
**Depends on**: `SUBTASK_concern2_code_quality`, `SUBTASK_concern3_tests`, `SUBTASK_concern6_idiom`, `SUBTASK_concern7_api_stability`
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

This task is a **verification gate**. It does not summarize prose — it runs four checks over the combined spoke outputs, asserts that the contract and coverage identities hold, and either passes (producing `findings.md` and `SYNTHESIS.md`) or fails with a structured error naming which check failed and why. If any check fails, the gate remediates by filing fix-tasks before retrying; it does not silently plug a gap.

---

## Context

Part of the PR #193 concerns 2/3/6/7 subtree. See `../_GLOBAL.md` for full context, inherited constraints, and the ownership table. The contract for spoke outputs is at `../contracts/findings_format.md`.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `../_GLOBAL.md` | Acceptance criteria, ownership table, identities |
| Findings contract | `../contracts/findings_format.md` | Schema the spoke outputs must satisfy |
| Contracts manifest | `../contracts/_MANIFEST.yaml` | Ownership and identities |
| Concern 2 findings | `../SUBTASK_concern2_code_quality/partial_findings.md` | Code quality and design spoke output |
| Concern 3 findings | `../SUBTASK_concern3_tests/partial_findings.md` | Test coverage and depth spoke output |
| Concern 6 findings | `../SUBTASK_concern6_idiom/partial_findings.md` | Rust idiom spoke output |
| Concern 7 findings | `../SUBTASK_concern7_api_stability/partial_findings.md` | API stability spoke output |

---

## Process: Four-Check Gate

This task runs four sequential checks. A check that fails means the gate fails; the gate MUST NOT proceed to `findings.md` production while a check is unresolved.

**Check 1 — Contract verification**: Does each `partial_findings.md` conform to `../contracts/findings_format.md`? Both required sections (`## Findings` and `## What was examined`) present? Severity values from the allowed set? `concern` label matching the spoke's assignment? Locations repository-relative?

**Check 2 — Wiring / coverage verification**: Does the combined output of all four spokes address every sub-question in the parent brief's four concern sections (Concern 2 Q1–Q4, Concern 3 Q1–Q4, Concern 6 Q1–Q4, Concern 7 Q1–Q3)? Mark each sub-question as addressed or unaddressed. Any unaddressed sub-question is a wiring failure.

**Check 3 — Duplication detection**: Does any finding appear in more than one spoke output (same location, same issue)? A finding duplicated across spokes indicates a scope boundary violation.

**Check 4 — Code review synthesis / overall coherence**: Reading the combined findings holistically, is the severity calibration consistent (no blocker over a style issue, no clean where the concern question was unanswered)? Does the combined output make a coherent, self-consistent review document that could be acted on by the author?

**Remediation**: If any check fails, file a fix-task (via `engine_amend_plan { add_task: ... }`) targeting the specific spoke or structural gap before the gate can proceed. Do not plug the failure silently.

**On pass**: Produce `../findings.md` as the unified review output (combining all spoke findings into the two-section format declared in `../contracts/findings_format.md`, consolidating the four `## What was examined` sections), and `../SYNTHESIS.md` as the fold record (documenting what was checked and found, the four check results, and the overall verdict). Then call `engine_resume_suspended` to fold the parent.

---

## Output Specification

| Artifact | Location | Description |
|----------|----------|-------------|
| `findings.md` | `../findings.md` | Unified review output: combined `## Findings` and `## What was examined` |
| `SYNTHESIS.md` | `../SYNTHESIS.md` | Fold record: four check results, identities verified, overall verdict |

`../findings.md` MUST follow the same schema as `../contracts/findings_format.md` (two sections, entries from all four concerns combined).

---

## Suggested Methodology Files

Task type row (Domain Mapping): **Synthesizing / verifying a hub-and-spoke decomposition** → Primary: `synthesis`, Supporting: `code-review`, `code-quality`

This task is a verification gate. Load:

- `synthesis/Synthesis_Overview_Methodology.md` — the four-check model, gate pass/fail decision, SYNTHESIS.md schema. REQUIRED; load first. Rationale: this task IS a synthesis gate; this file defines exactly what that means.
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — how to assert that spoke outputs conform to the declared contract. Rationale: Check 1 is a contract verification step.
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — how to verify coverage across all required concerns. Rationale: Check 2 is a wiring/coverage verification step.
- `synthesis/Synthesis_Duplication_Detection_Methodology.md` — how to detect findings appearing across multiple spokes. Rationale: Check 3 is a duplication detection step.
- `synthesis/Synthesis_Code_Review_Methodology.md` — how to assess overall coherence and severity calibration across the combined output. Rationale: Check 4 is a code-review synthesis step.
- `synthesis/Synthesis_Remediation_Methodology.md` — how to file fix-tasks when a check fails. Rationale: the gate must remediate failures, not plug them silently.

These are SUGGESTIONS. Load fewer if some checks are clearly not applicable; load more if the spokes reveal additional review surface.

## Inherited Constraints

- Repository-relative paths only in `findings.md`
- Issues #196–#201 MUST NOT appear in `findings.md`
- Do not add new concerns or scope beyond what the four spokes covered
- Do not alter spoke findings during combination — only consolidate; any real change to a finding must come from a remediation fix-task

## Success Criteria

- All four checks run explicitly and their results documented in `SYNTHESIS.md`
- `findings.md` produced with every concern addressed and every sub-question answered
- `SYNTHESIS.md` produced at the fold location (`../SYNTHESIS.md`) documenting the gate result
- If any check fails: a fix-task filed via `engine_amend_plan { add_task: ... }` before proceeding; the gate does NOT silently plug the failure
- `engine_resume_suspended` called with `seam_path: "../SYNTHESIS.md"` to fold the parent task
