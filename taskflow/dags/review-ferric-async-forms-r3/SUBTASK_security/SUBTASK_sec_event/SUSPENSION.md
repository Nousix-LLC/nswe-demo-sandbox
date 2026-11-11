# SUSPENSION: SUBTASK_sec_event

**Status**: Suspended — NeedsDecompose
**Suspended at**: SUBTASK_sec_event

## Decomposition Decision

The brief for SUBTASK_sec_event enumerates two distinct review questions:
1. EventHandler::WithEvent downcast reachability (dom.rs dispatch path)
2. closure.forget() scope in the WASM test (form.rs)

The enumerated-concerns rule in TASK_DECOMPOSITION_FRAMEWORK.md fires by this enumeration alone: two numbered distinct questions in the brief, each analyzable by a different specialist. The scope-based trigger overrides the single output file (finding.md) per trigger precedence.

## Children Materialized

| Child | Workspace | Description |
|-------|-----------|-------------|
| `SUBTASK_sec_event_downcast` | `SUBTASK_sec_event_downcast/` | Assess panic-on-downcast reachability in EventHandler::WithEvent |
| `SUBTASK_sec_event_forget` | `SUBTASK_sec_event_forget/` | Verify closure.forget() scope in WASM test vs. production |
| `SUBTASK_sec_event_synthesis` | `SUBTASK_sec_event_synthesis/` | Synthesis gate: compile sub-findings into finding.md |

## Resumption Condition

All three child tasks reach terminal lifecycle state (SUBTASK_sec_event_downcast, SUBTASK_sec_event_forget, and SUBTASK_sec_event_synthesis all COMPLETED), with `finding.md` observable at this workspace root.

## State Preserved

- `_GLOBAL.md` authored at this workspace root (subtree hub)
- `contracts/_MANIFEST.yaml` authored (sub-finding schema and ownership)
- Three child `_BRIEF.md` files authored and engine_amend_plan{add_task} called for each
- All gathered evidence (PR diff, vdom.rs, dom.rs, form.rs diff sections) is available via the same `gh pr diff 193` command for child agents to re-gather — no partial state to preserve
