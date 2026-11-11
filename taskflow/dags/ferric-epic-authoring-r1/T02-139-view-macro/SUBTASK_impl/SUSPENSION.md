# SUSPENSION.md — ferric-authoring-139-view-impl

**Task:** ferric-authoring-139-view-impl  
**Status:** suspended / NeedsDecompose  
**Suspended at:** 2026-11-03

---

## Decomposition summary

This node evaluated its brief and fired the **Enumerated-concerns** trigger:
the brief listed 6 distinct concerns (crate scaffold, proc-macro implementation,
ferric crate wiring, verification, git commit, and prelude export). The
kernel's Scope-Based rule mandates `NeedsDecompose` when 2+ distinct concerns
are present — the verdict is mechanical and not subject to override.

---

## Subtree materialized

Four children were authored and registered via `amend_plan { add_task }`:

```
ferric-authoring-139-view-impl-scaffold    (no deps)
ferric-authoring-139-view-impl-macro       (depends on scaffold)
ferric-authoring-139-view-impl-wire        (depends on scaffold)
ferric-authoring-139-view-impl-synthesis   (depends on macro + wire)
```

Execution DAG:

```
scaffold → macro_impl ──┐
         └→ wire ───────┴→ synthesis
```

Parallelism opportunity: `macro_impl` and `wire` can run concurrently once
`scaffold` completes.

---

## Child briefs authored

| Child | Workspace | _BRIEF.md |
|-------|-----------|-----------|
| scaffold | SUBTASK_scaffold/ | ✅ |
| macro_impl | SUBTASK_macro_impl/ | ✅ |
| wire | SUBTASK_wire/ | ✅ |
| synthesis | SUBTASK_synthesis/ | ✅ |

Hub context and contracts also authored:
- `_GLOBAL.md` at SUBTASK_impl/
- `contracts/_MANIFEST.yaml` at SUBTASK_impl/contracts/

---

## Resumption condition

This node resumes when all four child tasks have reached terminal states
(completed or failed). HAL drives the child subtree; this node does not
re-activate until the synthesis child (`ferric-authoring-139-view-impl-synthesis`)
reaches its terminal state.

---

## Key decisions recorded

1. **Root Cargo.toml must NOT be modified.** The workspace already uses
   `members = ["crates/*"]` glob; creating `crates/ferric-macros/` is sufficient.
   This is embedded in SUBTASK_scaffold's brief and the hub contract.

2. **Wire and macro_impl run in parallel** after scaffold, reducing total
   wall-clock time for the subtree.

3. **Structural seam** frozen in `contracts/_MANIFEST.yaml`: crate name
   `ferric-macros`, rust name `ferric_macros`, macro name `view`, export line
   `pub use ferric_macros::view;`.
