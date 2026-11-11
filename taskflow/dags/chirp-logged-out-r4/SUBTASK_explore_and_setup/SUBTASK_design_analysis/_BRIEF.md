# Task: Design Documents Analysis

## Task Specification

**Slug**: SUBTASK_design_analysis
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-coder

### Objective

Read the three design documents and extract: (1) specific screen/state requirements for the
logged-out experience, (2) the sign-up and sign-in route names specified in the design, and
(3) the BAR-011 checklist items relevant to logged-out acceptance criteria AC-1 through AC-5.
Record findings in `design_findings.md`.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/_GLOBAL.md` | Project constraints |
| Product requirements | `design/product-requirements.md` | §3 User journeys; §4 REQ-PROD-013..015 |
| Experience design | `design/experience-design.md` | §1 IA; §2 Screens/flows/states; §6 REQ-UX-002, 030-032 |
| Release bar | `design/release-bar.md` | §C BAR-011 |

All paths are relative to `/home/user/nousix-runtime/nswe-demo`.

---

## Process Specification

1. Read `design/product-requirements.md` — focus on §3 (user journeys for logged-out users)
   and §4 (REQ-PROD-013 through REQ-PROD-015).
2. Read `design/experience-design.md` — focus on:
   - §1: Information architecture (what routes/pages exist for logged-out users)
   - §2: Screen states for the public home/timeline (loading, empty, error, end-of-list)
   - §6: REQ-UX-002 and REQ-UX-030 through REQ-UX-032
   - Note the EXACT route names/paths used for sign-up and sign-in in the design
3. Read `design/release-bar.md` — focus on §C BAR-011 and identify all checklist items
   relevant to logged-out acceptance criteria (AC-1, AC-2, AC-3, AC-4, AC-5).
4. Write `design_findings.md` with the required sections.
5. Write `COMPLETE.md`.

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `design_findings.md` |
| Location | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/SUBTASK_design_analysis/` |

### Required Sections in `design_findings.md`

```markdown
# Design Documents Findings

## Screen States Required
- Public home/timeline states: (list: loading, empty, error, end-of-list)
- Any other required states from §2 experience-design.md

## Route Names from Design
- Sign-in route name/path: <exact name as specified>
- Sign-up route name/path: <exact name as specified>
- Public home/timeline route: <exact name as specified>
- Any other logged-out routes mentioned

## Product Requirements (REQ-PROD-013..015)
- REQ-PROD-013: <text or summary>
- REQ-PROD-014: <text or summary>
- REQ-PROD-015: <text or summary>

## UX Requirements
- REQ-UX-002: <text or summary>
- REQ-UX-030: <text or summary>
- REQ-UX-031: <text or summary>
- REQ-UX-032: <text or summary>

## BAR-011 Checklist Items
- AC-1: <checklist item text>
- AC-2: <checklist item text>
- AC-3: <checklist item text>
- AC-4: <checklist item text>
- AC-5: <checklist item text>
```

---

## Success Criteria

- [ ] All three design docs read
- [ ] `design_findings.md` contains sign-in and sign-up route names (exact strings from design)
- [ ] `design_findings.md` contains all BAR-011 items for AC-1 through AC-5
- [ ] `design_findings.md` lists required screen states
- [ ] `COMPLETE.md` written

---

## Suggested Methodology Files

**Task-type row:** Codebase/document analysis feeding a larger deliverable — Primary: `core`

**Specific files:**
- `core/BestPractices_Coding_Standards_Methodology.md` — Rationale: sets standards for structured output documents.

**These are SUGGESTIONS.** The child agent is the final judge.

## Inherited Constraints

- Repository is at `/home/user/nousix-runtime/nswe-demo`
- Read-only — do NOT modify any design docs
- Note: the cluster SSH pattern from CLAUDE.md is NOT needed for this task
