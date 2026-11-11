# Task: Ferric 1.0 Design — Root Synthesis

## Task Specification

**Slug**: SUBTASK_synthesize-root
**Task Kind**: synthesis
**Depends on**: SUBTASK_remediate
**Status**: Pending
**Assigned To**: swe-designer

### Objective

Produce the root `SYNTHESIS.md` for the Ferric 1.0 design DAG. This file is the
observation seam for the overseer: it states the Ferric 1.0 release bar and indexes the
filed issues by epic. After writing it, fold the parent SUSPENDED node to COMPLETED by
calling `mcp__hal__resume_suspended`.

### Context

This task is part of the design-ferric-1_0-r2 recovery DAG (see `_GLOBAL.md` in the parent workspace).

SUBTASK_review-validate has validated the design. SUBTASK_remediate has applied any fixes. This task
reads those outputs, reads the finalized design on the branch, and produces the root synthesis.

The root `SYNTHESIS.md` is the artifact the overseer reads (disposition: `reap-whole-after-land`).
It must be a self-contained summary: someone who has not read any other file in this taskflow can read it
and understand what Ferric 1.0 is, what the release bar is, and where to find the filed issues.

This task has NO SEPARATE `COMPLETE.md`. It writes `SYNTHESIS.md` at the parent workspace and then
reports `status="completed"` with `artifact_path` pointing to `SYNTHESIS.md`. It then calls
`mcp__hal__resume_suspended` to fold the parent.

**Dependencies**: SUBTASK_remediate — read `SUBTASK_remediate/remediation-report.md` before starting.  
**Dependents**: none (this is the synthesis gate).

---

## Inputs

| Input | Location | Purpose |
|---|---|---|
| Remediation report | `SUBTASK_remediate/remediation-report.md` | Source for synthesis_inputs (release bar, epic index) |
| Review report | `SUBTASK_review-validate/review-report.md` | Confirm validation is clean |
| `release-bar.md` | `design/ferric/release-bar.md` on branch `work/design-ferric-1_0` | Complete release bar criteria |
| `release-plan.md` | `design/ferric/release-plan.md` on same branch | Epic ordering and dependencies |
| Filed issues | #129–#164 on `Nousix-LLC/nswe-demo` | Final issue list for index |
| PR | #128 on `Nousix-LLC/nswe-demo` | PR number and readiness |
| Hub context | `../_GLOBAL.md` | Project constraints and issue register |

---

## What to Produce

### The root `SYNTHESIS.md`

File path: `../SYNTHESIS.md` (i.e., at the parent workspace:
`/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-ferric-1_0-r2/SYNTHESIS.md`)

Content requirements:

1. **Header** — "Ferric 1.0 — Design Synthesis"

2. **Design verdict** — a brief statement (2–4 sentences) that the design is complete: all nine concern
   areas are covered, the release bar is defined, the backlog is filed. Mention PR #128 and the branch.

3. **The Ferric 1.0 release bar** — the key criteria from `release-bar.md`:
   - The `usable_early` criteria (what makes the framework buildable for real apps)
   - The `one_oh` criteria (what is additionally required for a credible public 1.0)
   - Call out `BAR-FERRIC-004` (or whichever id carries the SSR + hydration must-have gate) explicitly
   Present as a table: `BAR-FERRIC-NNN | statement | stage | must-have?`
   Use the actual ids and statements from `release-bar.md`; do not paraphrase.

4. **Issues by epic** — a table indexed by epic:
   ```
   Epic # | Title | Stage | Child issues
   ```
   List each of the eight epics (#129–#136) with their titles, `usable_early` or `one_oh` stage, and the
   comma-separated list of child issue numbers. Use the finalized list from the remediation report's
   `synthesis_inputs` section.

5. **Design documents** — a one-line reference to each of the ten design documents and where they live
   (branch + path).

6. **PR** — note that PR #128 carries the design artifacts.

### Writing voice

Write for the overseer reading this file cold. State facts, not aspirations. Do not say "comprehensive" or
"thorough." Name the specific documents, criteria, and issue numbers. Do not pad the document — every
sentence should be checkable.

---

## The fold

After writing `SYNTHESIS.md` and calling `engine_report_status { status: "completed", artifact_path: "<path_to_SYNTHESIS.md>", outputs: ["<path_to_SYNTHESIS.md>"] }`, call:

```
mcp__hal__resume_suspended {
  target_task_id:      "<the parent DAG node's task id — read from your dispatch context or from ../_GLOBAL.md>",
  synthesized_task_id: "<your own task id — from your dispatch context>",
  seam_path:           "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-ferric-1_0-r2/SYNTHESIS.md"
}
```

This folds the parent (design-ferric-1_0-r2) from SUSPENDED to COMPLETED, discharging the overseer's
observation seam.

If `mcp__hal__resume_suspended` is not in your tools array (indicating this is a human-driven session), skip
the call and note in your COMPLETE.md that the fold must be applied manually.

---

## Output

| Artifact | Path | Notes |
|---|---|---|
| Root SYNTHESIS.md | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-ferric-1_0-r2/SYNTHESIS.md` | The fold record — serves as both this task's terminal artifact AND the fold record. No separate COMPLETE.md. |

---

## Success Criteria

- [ ] `SYNTHESIS.md` written at the parent workspace path above
- [ ] Contains the Ferric 1.0 release bar with actual `BAR-FERRIC-*` ids from `release-bar.md`
- [ ] Contains the issue index (all 8 epics, all child issues)
- [ ] References PR #128
- [ ] Every statement in SYNTHESIS.md is checkable against the design documents
- [ ] `mcp__hal__resume_suspended` called to fold the parent (or fold noted as manual if unavailable)
