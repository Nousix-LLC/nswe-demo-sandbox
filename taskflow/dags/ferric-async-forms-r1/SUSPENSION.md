# SUSPENSION — ferric-async-forms-r1

## Status
Suspended: NeedsDecompose. Subtree materialized; execution continues via child tasks.

## Decomposition Shape
Contract-first fan-out with disjoint module ownership.

## Execution Groups

### Group 0 (serial)
- **SUBTASK_walking_skeleton** — creates branch + issues + extends EventKind + stubs

### Group 1 (parallel, all depend on Group 0)
- **SUBTASK_async_resource** — `async_resource.rs`: Resource<T>, ResourceState<T>, suspense
- **SUBTASK_dom_events** — `dom.rs`: full EventKind binding dispatch
- **SUBTASK_form_binding** — `form.rs`: FormField<T>, Bind<T>

### Group 2 (serial, depends on all Group 1)
- **SUBTASK_synthesis** — PR creation, wiring verification, issue closure, SYNTHESIS.md

## Module Ownership (frozen seam)
No two spokes touch the same file. Skeleton pre-declares all shared artifacts.

## Observation Seam
`/home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-async-forms-r1/SYNTHESIS.md`
Authored by SUBTASK_synthesis on completion; records PR URL, issue numbers, and final commit SHA.

## Resumption Condition
Resume when SUBTASK_synthesis completes and SYNTHESIS.md is present at the observation seam.
