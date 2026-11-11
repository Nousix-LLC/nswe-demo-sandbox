# Task: Ferric 1.0 release plan — synthesis into release-plan.md

## Task Specification

**Slug**: SUBTASK_rplan_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_rplan_epics, SUBTASK_rplan_work_items
**Status**: Pending
**Assigned To**: swe-designer

### Objective

Assemble the final `release-plan.md` from the epic landscape (`epics-and-order.md`) and
the work-items (`work-items.md`). Verify identities J1, J2, J3 from the subtree contract
(and by extension I6, I7 from the parent contract). Produce a clean, self-contained
document that SUBTASK_design_pr can place at `design/ferric/release-plan.md` and
SUBTASK_file_backlog can consume to file/extend board issues.

### Context

The synthesis task of the SUBTASK_release_plan subtree (see `../_GLOBAL.md`). It reads
the two predecessor outputs, verifies the seam identities, and consolidates into the
declared output of the parent task node.

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context + constraints. |
| Grand subtree hub | `../../_GLOBAL.md` | Project-level constraints and success criteria. |
| Contracts (parent) | `../../contracts/id_and_traceability_schema.yaml` | Epic/work-item schemas; trace rules (I6, I7). |
| Contracts (this level) | `../contracts/_MANIFEST.yaml` | Intermediate artifact ownership; identities J1/J2/J3. |
| Epic landscape | `../SUBTASK_rplan_epics/epics-and-order.md` | The authoritative epic structure to assemble. |
| Work-items | `../SUBTASK_rplan_work_items/work-items.md` | The work-items to embed under each epic. |

---

## What this task does

1. **Verify the seam identities** before writing the final document:
   - J1: every work-item's epic reference matches an epic in epics-and-order.md (no orphans)
   - J2: the router/HTTP epic(s) name the exact #5/#6 issue numbers and state the fold action
   - J3: every `one_oh` BAR-FERRIC-* is covered by ≥1 work-item acceptance criterion
   If any identity fails, record the specific gap explicitly in the output rather than
   silently patching it.

2. **Assemble release-plan.md** as a clean, ordered document:
   - An intro paragraph (2-3 sentences) orienting a reader who picks it up cold
   - The epic structure: for each epic, its title, design-doc area(s), stage, depends_on,
     and for router/HTTP epics: the #5/#6 fold
   - Under each epic, its work-items with acceptance criteria
   - The ordering narrative (which epics reach a usable framework early)
   - The #5/#6 fold table (explicit, for SUBTASK_file_backlog to act on)

3. **Do not modify** epics-and-order.md or work-items.md. If a gap or inconsistency is
   found, record it in the output and note what SUBTASK_file_backlog or a follow-on
   amendment should do — but do not patch silently.

---

## Declared output

- `release-plan.md` — in this task's workspace (`SUBTASK_rplan_synthesis/`)
  AND also write it to the parent workspace as:
  - `../release-plan.md`
  Both copies must be identical. The `../` copy is the declared output that SUBTASK_design_pr
  and SUBTASK_file_backlog will find via the paths declared in the parent _BRIEF.md.

The document is the single source of truth that SUBTASK_design_pr places at
`design/ferric/release-plan.md` in the repo and SUBTASK_file_backlog reads to file/extend
issues.

---

## Success criteria

- [ ] Identity J1 checked: no orphan work-items (every epic reference resolves).
- [ ] Identity J2 checked: #5/#6 fold is explicit in the document with exact issue numbers.
- [ ] Identity J3 checked: every `one_oh` BAR-FERRIC-* is covered; any gap is recorded.
- [ ] release-plan.md is a clean, self-contained document (readable without the working files).
- [ ] The #5/#6 fold table is present and actionable for SUBTASK_file_backlog.
- [ ] Writing-voice rules honored: no machine-writing tells, plain checkable prose.
- [ ] Both copies written: `release-plan.md` (here) and `../release-plan.md`.

## Constraints

- No REQ-*/BAR-FERRIC-* is redefined.
- GitHub-bound content (epic titles used as issue titles) names only repository
  identities — no system paths, no attribution trailers.
- Do not write implementation guidance. The plan says what and how to judge; code
  DAGs handle how to build.
