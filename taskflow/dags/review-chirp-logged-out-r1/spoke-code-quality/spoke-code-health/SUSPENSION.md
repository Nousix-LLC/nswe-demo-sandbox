# SUSPENSION — spoke-code-health

**Task**: spoke-code-health (Dead Code + Scope Analysis — PR #263, Concerns 6 and 7)
**Status**: Suspended (NeedsDecompose)
**Suspended at**: 2026-11-06

## Decomposition Decision

The brief for `spoke-code-health` enumerates two distinct analyses:
- **Concern 6**: Reachability of `sign_up::sign_up_view` from any live route (reads route table,
  sign_up.rs, compose.rs)
- **Concern 7**: Scope and sync assessment of the `hydrate.rs` EventKind expansion (reads
  hydrate.rs, PR diff)

These are independent analyses of different parts of the codebase, which could be conducted by
different specialists in parallel (Distinct Concerns Test fires). The brief's explicit numbered
enumeration also fires the Enumerated-Concerns rule. The scope trigger fires and overrides the
cleared token and output-size triggers. Verdict: NeedsDecompose.

## Children Materialized

| Task ID | Workspace | Dependency |
|---------|-----------|------------|
| `child-dead-code` | `spoke-code-health/child-dead-code/` | none |
| `child-hydrate-scope` | `spoke-code-health/child-hydrate-scope/` | none |
| `child-synthesis` | `spoke-code-health/child-synthesis/` | child-dead-code, child-hydrate-scope |

## Resumption Condition

All three child tasks reach terminal lifecycle state. The synthesis child (`child-synthesis`)
produces `spoke-code-health/FINDINGS.md`, which is the declared output of this task.

## Authored State Files

- `_GLOBAL.md` — subtree hub
- `contracts/_MANIFEST.yaml` — ownership and identities
- `contracts/concern_finding_schema.md` — per-concern finding file schema
- `child-dead-code/_BRIEF.md` — concern 6 analysis brief
- `child-hydrate-scope/_BRIEF.md` — concern 7 analysis brief
- `child-synthesis/_BRIEF.md` — synthesis gate brief
