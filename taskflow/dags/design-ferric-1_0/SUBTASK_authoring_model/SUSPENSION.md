# SUSPENSION.md — SUBTASK_authoring_model (NeedsDecompose)

## Why suspended

This task (Ferric 1.0 authoring model, concern 3) decomposed. Its brief names three genuinely distinct design
concerns — the `view!` macro (a macro/DSL grammar + lowering + compile-diagnostics problem), the component
props/children/slots/composition model (a Rust type-system ergonomics problem), and context (a reactivity +
scoped-cleanup problem tied to the reactive owner tree). The Scope-Based trigger and the enumerated-concerns
rule fire on that enumeration; the Distinct-Concerns and Single-Responsibility tests both fire. Per the
disjunction rule and the normative decompose bias, the task is not atomic. The single declared output
(`authoring-model.md`) and the token/output estimates do not override a fired scope trigger.

## Decomposition (hub-and-spoke + synthesis fold)

Authored at this workspace: `_GLOBAL.md` (hub), `contracts/_MANIFEST.yaml` + `contracts/req_api_partition.yaml`
(the REQ-API band partition + authoring-seam identities IA1–IA6), and one `_BRIEF.md` per child.

| Child (task id) | Group | REQ-API band | Output | Depends on |
|---|---|---|---|---|
| `SUBTASK_view_macro` | 0 | 001–029 | `view-macro.md` | none |
| `SUBTASK_components_props_slots` | 0 | 030–059 | `components-props-slots.md` | none |
| `SUBTASK_context` | 0 | 060–079 | `context.md` | none |
| `SUBTASK_authoring_model_synthesis` | 1 | (consolidates) | `../authoring-model.md`, `../SYNTHESIS.md` | the three spokes |

The synthesis child is the gate (Task Kind: synthesis): it asserts IA1–IA6, folds the three section drafts
into the single `authoring-model.md` with a merged, collision-free `REQ-API-*` register and a by-name peer
view-macro comparison, runs the avoid-ai-writing pass, and folds this parent `SUSPENDED → COMPLETED`.

## Contract

`contracts/` extends the parent Ferric 1.0 contract (REQ-API id shape, verification/stage vocab, identities
I1/I9) and overrides nothing. It fixes the one seam the three spokes share: a disjoint REQ-API band per spoke
(IA1), the macro↔component invocation seam (IA2), the context↔component/reactive-scope seam (IA3), additivity
over the frozen surface (IA4), one consolidated deliverable (IA5), and testable diagnostics/criteria (IA6).

## Resumption condition

All four child tasks reach terminal lifecycle states; the synthesis fold resumes this task via
`engine_resume_suspended` with `../SYNTHESIS.md` as the seam, flipping it `SUSPENDED → COMPLETED` and producing
`authoring-model.md` as this spoke's deliverable.
