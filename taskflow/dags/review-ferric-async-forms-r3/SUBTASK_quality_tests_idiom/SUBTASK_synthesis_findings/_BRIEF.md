# Task: Synthesis — Integrate Concern Findings into findings.md (PR #193)

## Task Specification

**Slug**: SUBTASK_synthesis_findings
**Task Kind**: synthesis
**Depends on**: SUBTASK_concern2_quality_design, SUBTASK_concern3_tests, SUBTASK_concern6_idiom, SUBTASK_concern7_api_stability
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

This task is a **verification gate**. Read the four partial findings files produced by the concern spokes, verify full coverage (every concern, every sub-question), integrate them into the consolidated `findings.md` at the parent workspace root, and author `SYNTHESIS.md` there to fold the parent task SUSPENDED → COMPLETED.

The gate fails if any concern sub-question was left unanswered or if severity assignments are inconsistent across concerns. The gate does not silently plug gaps — it surfaces them or schedules remediation.

---

## Context

See `../_GLOBAL.md` for full project context, constraints, and task structure.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Constraints, success criteria, full scope |
| Concern 2 findings | `../SUBTASK_concern2_quality_design/findings_concern2.md` | Code quality and design |
| Concern 3 findings | `../SUBTASK_concern3_tests/findings_concern3.md` | Test coverage and depth |
| Concern 6 findings | `../SUBTASK_concern6_idiom/findings_concern6.md` | Rust language idiom |
| Concern 7 findings | `../SUBTASK_concern7_api_stability/findings_concern7.md` | API and contract stability |

---

## Process

This task runs as a **verification gate** in four checks:

1. **Coverage check:** Did each spoke cover all its assigned sub-questions? Flag any concern where a sub-question from `_GLOBAL.md` has no corresponding finding entry.

2. **Severity calibration check:** Are severity assignments consistent with the inherited constraint (blocker only if requirement unmet or API contract broken; style observations at most non-blocker)? Flag any finding where the severity label appears miscalibrated.

3. **De-duplication check:** If the same code location or pattern appears in multiple concern findings, consolidate them into one entry in the output with the highest severity assigned.

4. **Integration:** Merge all entries into the `findings.md` format below, grouped by concern. Add a verdict line summarizing whether any blocker was found.

If a coverage gap is found (a concern sub-question with no finding), the gate does NOT fabricate a finding — it surfaces the gap as a `concern: [area], severity: gap, description: sub-question X was not addressed` entry in findings.md, and notes it in SYNTHESIS.md.

---

## Output Specification

**Primary Output:** `findings.md` at the PARENT workspace root (`../findings.md` = `SUBTASK_quality_tests_idiom/findings.md`)

The findings.md MUST follow this structure:

```markdown
## Verdict

[overall: approved | approved-with-comments | blocked]
[Blockers: none | list each blocker finding by identifier]

## Findings

### Concern 2 — Code Quality and Design

[entries from findings_concern2.md, normalized format]

### Concern 3 — Test Coverage and Depth

[entries from findings_concern3.md, normalized format]

### Concern 6 — Rust Language Idiom

[entries from findings_concern6.md, normalized format]

### Concern 7 — API and Contract Stability

[entries from findings_concern7.md, normalized format]

## What was examined

[Union of all "What was examined" sections from all spokes]
```

Each finding entry uses:
```
- severity: blocker | non-blocker | clean
- concern: code-quality | tests | idiom | api-stability
- location: crates/ferric/src/file.rs:LINE (where applicable)
- description: what was found
```

**Fold Record:** `SYNTHESIS.md` at the PARENT workspace root (`../SYNTHESIS.md` = `SUBTASK_quality_tests_idiom/SYNTHESIS.md`)

SYNTHESIS.md records: what each spoke found, the gate verdicts (coverage, severity calibration, de-duplication), and the fold outcome. After writing both files, call `engine_resume_suspended` to fold the parent task SUSPENDED → COMPLETED.

---

## Suggested Methodology Files

Task type row (Domain Mapping): **Synthesizing / verifying a hub-and-spoke decomposition** → Primary: `synthesis`, Supporting: `code-review`

Specific files to load:
- `synthesis/Synthesis_Overview_Methodology.md` — the four-check gate model (always load first)
- `synthesis/Synthesis_Code_Review_Methodology.md` — synthesis code review gate
- `code-review/CodeReview_Checklist_Methodology.md` — review completeness checklist

These are SUGGESTIONS. Load fewer if some are clearly inapplicable; load more if the brief reveals additional gate surface.

## Inherited Constraints

- Repository-relative paths only in all findings
- Non-blockers #196–#201 must not be re-raised
- Severity calibration: blocker only if requirement unmet or API contract broken
- Findings must be actionable: location + principle + why + what satisfies it
- Do NOT fabricate findings for coverage gaps — surface the gap explicitly

## Success Criteria

- All four concern files read and their "What was examined" sections confirmed
- Coverage check complete: every sub-question from `_GLOBAL.md` has a finding or explicit gap entry
- Severity calibration check complete
- De-duplication check complete
- `findings.md` produced at `../findings.md` with all concerns present and a verdict line
- `SYNTHESIS.md` produced at `../SYNTHESIS.md` as the fold record
- `engine_resume_suspended` called to fold the parent SUSPENDED → COMPLETED
