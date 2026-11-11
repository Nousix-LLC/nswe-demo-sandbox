# Subtree Hub: ferric-async-forms-r1

## Objective
Implement Ferric 1.0 epic #130 — Async, Forms, and Events — on top of the Authoring Model
(branch `work/ferric-async-forms-r1`, base `main @ aa24687`). Closes issues #130, #143, #144, #145
in `Nousix-LLC/ferric`.

## Scope
`crates/ferric/src/` — additive only. No changes to `design/`. No changes outside `crates/ferric`.

## Repository
- Repo: `Nousix-LLC/ferric` (public)
- Branch: `work/ferric-async-forms-r1` (created by SUBTASK_walking_skeleton)
- Security: never commit secrets/tokens/credentials; never force-push main; never rewrite merged history.

## Decomposition Shape
Contract-first fan-out. The walking skeleton freezes the shared `EventKind` seam and module stubs
before feature spokes execute. Feature spokes run in parallel against frozen contracts. Synthesis
gate assembles the PR and closes issues.

## Module Ownership Manifest
Each spoke owns a disjoint set of files. No two spokes touch the same file.

| Subtask                  | Files Owned                                     |
|--------------------------|--------------------------------------------------|
| SUBTASK_walking_skeleton | `crates/ferric/src/vdom.rs` (extend EventKind)  |
|                          | `crates/ferric/src/lib.rs` (pub mod declarations)|
|                          | `crates/ferric/src/async_resource.rs` (stub)    |
|                          | `crates/ferric/src/form.rs` (stub)              |
| SUBTASK_async_resource   | `crates/ferric/src/async_resource.rs` (full impl)|
| SUBTASK_dom_events       | `crates/ferric/src/dom.rs` (extend binding logic)|
| SUBTASK_form_binding     | `crates/ferric/src/form.rs` (full impl)         |
| SUBTASK_synthesis        | PR creation, CI verification, issue closure     |

## Contracts (see contracts/ directory)
- `contracts/event_kind_contract.md` — full EventKind set that skeleton declares, spokes consume
- `contracts/module_interfaces.md` — public types each new module must export at completion

## Execution Order
Group 0 (serial):
  - SUBTASK_walking_skeleton

Group 1 (parallel, all depend on skeleton completion):
  - SUBTASK_async_resource
  - SUBTASK_dom_events
  - SUBTASK_form_binding

Group 2 (serial, depends on all Group 1 completion):
  - SUBTASK_synthesis

## Observation Seam
`/home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-async-forms-r1/SYNTHESIS.md`
