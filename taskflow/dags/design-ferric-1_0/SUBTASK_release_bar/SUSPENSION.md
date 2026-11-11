# SUSPENSION — SUBTASK_release_bar

**Task**: SUBTASK_release_bar
**Status**: suspended / NeedsDecompose
**Suspended at**: 2026-10-29

---

## Decomposition

SUBTASK_release_bar decomposed into two DAG children rather than the originally planned three, due to
a scheduling constraint: a sequential three-child chain (gap_review → criteria → synthesis) would
push the parent's effective completion to execution group 4, while the downstream SUBTASK_release_plan
is in group 3. The engine rejected the chain as a scheduling cycle. The resolution:

| Task id | Group | Status | Scope |
|---------|-------|--------|-------|
| `SUBTASK_release_bar/SUBTASK_rbar_gap_review` | 2 | RUNNING | Surface gap sweep → `gap-analysis.md` (supplemental) |
| `SUBTASK_release_bar/SUBTASK_rbar_synthesis` | 2 | PENDING | Full release bar: gap sweep, BAR-FERRIC-* criteria, assembly, fold parent |

Both children are in group 2, concurrent with each other and with this parent's SUSPENDED state.
SUBTASK_rbar_synthesis owns the primary outputs (`release-bar.md`, `SYNTHESIS.md`) and will fold
this task from SUSPENDED to COMPLETED when it calls `engine_resume_suspended`.

## Named-state authored

| File | Purpose |
|------|---------|
| `_GLOBAL.md` | Subtree hub; documents objective, structure, scheduling note, contract |
| `contracts/_MANIFEST.yaml` | Format contracts for gap-analysis.md rows and BAR-FERRIC-* criteria |
| `SUBTASK_rbar_gap_review/_BRIEF.md` | Surface gap sweep — sweep all expected surfaces, record status + REQ-* refs |
| `SUBTASK_rbar_criteria/_BRIEF.md` | Criteria brief (authored for reference; not added to DAG) |
| `SUBTASK_rbar_synthesis/_BRIEF.md` | Full synthesis: independent gap sweep, BAR-FERRIC-* criteria, assembly, fold |

## Resumption

This task resumes automatically when SUBTASK_rbar_synthesis completes and calls
`engine_resume_suspended` with SUBTASK_release_bar as the target, writing `SYNTHESIS.md` at this
workspace root.
