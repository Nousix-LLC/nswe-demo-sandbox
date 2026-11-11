# Task: Design Document Survey

## Task Specification

**Slug**: SUBTASK_explore-survey-design  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

Read the three Chirp design documents and extract the acceptance criteria (AC-1 through AC-5), their associated requirement IDs, and the screen and state specifications each AC implies.

### Context

This task is part of the Codebase Exploration subtree for Chirp Logged-Out r7. See `../_GLOBAL.md` for full subtree context, and `../../_GLOBAL.md` for the project-level context and ACs.

**Dependents**: SUBTASK_explore-synthesis (reads design-survey.md)

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Subtree context and constraints |
| Project context | `../../_GLOBAL.md` | Full project context and ACs |
| Product requirements | `design/product-requirements.md` on repo `main` (cloned) | §3 User journeys; §4 REQ-PROD-013, REQ-PROD-014, REQ-PROD-015 |
| Experience design | `design/experience-design.md` on repo `main` (cloned) | §1 Information architecture; §2 Screens, flows & states; §6 REQ-UX-002, REQ-UX-030–032 |
| Release bar | `design/release-bar.md` on repo `main` (cloned) | §C BAR-011 |

The design documents live in the working tree of repository `Nousix-LLC/nswe-demo`. Read them from the cloned repository on the build server or via `gh api` / `gh repo view`.

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `design-survey.md` |
| Location | `SUBTASK_explore-survey-design/` (this workspace) |

### Output Structure

`design-survey.md` MUST include:

1. **Acceptance Criteria** — For each of AC-1 through AC-5:
   - Requirement IDs (REQ-PROD-*, REQ-UX-*, BAR-*)
   - Verbatim text from the issue / design docs
   - Which design document section it comes from
   - What it implies for the UI: concrete screens, states, or interactions

2. **Screen and State Inventory** — List every distinct UI state the design docs specify for the logged-out experience:
   - Loading state
   - Empty state (no content)
   - Error / failed-to-load state
   - Populated / end-of-list state
   - Any screen for sign-up / sign-in navigation

3. **Open Questions** — Any ambiguities in the design docs that the backend or frontend tasks should be aware of.

---

## Success Criteria

- [ ] All five ACs extracted with their requirement IDs
- [ ] Screen and state inventory covers all states mentioned in the design docs
- [ ] design-survey.md written at this workspace

---

## Suggested Methodology Files

**Task-type row matched**: "Designing systems" → Architecture (for evaluating existing pattern against requirements)

**Primary files to load**:
- `architecture/Architecture_API_Design_Methodology.md` — rationale: provides the lens for reading requirement documents and mapping them to concrete API and UI contract needs

These are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.

## Inherited Constraints

- Exploration only — no code changes
- Repository: `Nousix-LLC/nswe-demo`; design docs are on `main` at `cb1ced3`
- No host paths, internal addresses, or taskflow references in output

## Out-of-Scope Methodologies

- Testing methodologies — this task writes no tests
- Operations / CI methodologies — not applicable to a reading task
