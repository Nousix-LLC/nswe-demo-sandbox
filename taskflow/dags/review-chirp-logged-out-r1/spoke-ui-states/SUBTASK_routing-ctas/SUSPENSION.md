# SUSPENSION.md — SUBTASK_routing-ctas

## Status: Suspended (NeedsDecompose)

This task has decomposed into a sub-DAG of four children and is suspended until the entire
subtree resolves to terminal states.

## Decomposition rationale

The brief enumerated three distinct concerns — AC-4 sign-up path, CTA link correctness in
compose.rs, and the route annotation anomaly in app.rs — each requiring independent analysis
of different source files. The scope trigger fired by that enumeration; the Distinct Concerns
Test confirmed parallel fan-out is possible. Per the kernel's decomposition rules and the
reviewer system prompt's explicit instruction to honor the trigger over professional instinct,
the task was declared NeedsDecompose.

## Children materialized

| Task id (DAG) | Workspace | Concern | Depends on |
|---------------|-----------|---------|------------|
| `SUBTASK_ac4-path` | `SUBTASK_ac4-path/` | AC-4 sign-in-to-sign-up path | none |
| `SUBTASK_cta-link` | `SUBTASK_cta-link/` | CTA link correctness (compose.rs) | none |
| `SUBTASK_annotation` | `SUBTASK_annotation/` | Route annotation anomaly (app.rs) | none |
| `SUBTASK_ctas-synthesis` | `SUBTASK_synthesis/` | Assemble FINDINGS.md + fold parent | ac4-path, cta-link, annotation |

## Resumption condition

This task resumes (SUSPENDED→COMPLETED via fold) when SUBTASK_ctas-synthesis completes
and calls `engine_resume_suspended` with `seam_path: .../SUBTASK_routing-ctas/SYNTHESIS.md`.

## Named state authored

- `_GLOBAL.md` — subtree hub
- `contracts/_MANIFEST.yaml` — structural contract for concern outputs and FINDINGS.md
- `SUBTASK_ac4-path/_BRIEF.md` — AC-4 path concern brief
- `SUBTASK_cta-link/_BRIEF.md` — CTA link concern brief
- `SUBTASK_annotation/_BRIEF.md` — annotation anomaly concern brief
- `SUBTASK_synthesis/_BRIEF.md` — synthesis/verification gate brief
