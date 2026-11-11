# SUSPENSION — SUBTASK_code-quality

**Status**: Suspended / NeedsDecompose
**Suspended at**: 2026-11-06

## Decomposition

This task split into three children:

| Child | Depends on | Output |
|---|---|---|
| `SUBTASK_app-rs-quality` | none | `SUBTASK_app-rs-quality/app-rs-notes.md` |
| `SUBTASK_hydrate-wasm-quality` | none | `SUBTASK_hydrate-wasm-quality/hydrate-wasm-notes.md` |
| `SUBTASK_quality-synthesis` | both spokes | `code-quality.md` |

## Resumption

This task resumes when `SUBTASK_quality-synthesis` reaches COMPLETED and folds the result
back via `engine_resume_suspended`. The synthesis task is responsible for the fold call.

## Named-State Written

- `_GLOBAL.md` — subtree hub
- `contracts/_MANIFEST.yaml` — ownership manifest and finding format contract
- `SUBTASK_app-rs-quality/_BRIEF.md` — app.rs review spoke brief
- `SUBTASK_hydrate-wasm-quality/_BRIEF.md` — hydrate_wasm.rs review spoke brief
- `SUBTASK_quality-synthesis/_BRIEF.md` — synthesis/gate brief
