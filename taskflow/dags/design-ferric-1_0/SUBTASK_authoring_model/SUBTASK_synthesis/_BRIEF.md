# Task: Ferric 1.0 — authoring model synthesis (fold → authoring-model.md)

## Task Specification
**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective
Verify the authoring-seam identities and fold the three section drafts into the single, coherent
`authoring-model.md` deliverable with one merged `REQ-API-*` register — the authoring model as a reviewer and a
code DAG will consume it — then fold the parent `SUBTASK_authoring_model`.

### Context
The synthesis gate of the authoring-model subtree (hub: `../_GLOBAL.md`). It reads the three completed section
drafts and this subtree's contract, asserts identities IA1–IA6 (`../contracts/_MANIFEST.yaml`) as mechanical
checks with no silent plugs, and consolidates everything into the one declared deliverable the outer Ferric 1.0
design expects at `SUBTASK_authoring_model/authoring-model.md` (which the outer `SUBTASK_design_pr` places at
`design/ferric/authoring-model.md`).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, success criteria, the contract summary. |
| Subtree contract | `../contracts/_MANIFEST.yaml`, `../contracts/req_api_partition.yaml` | IA1–IA6 to assert; the band map to check for collisions. READ-ONLY. |
| View-macro section | `../SUBTASK_view_macro/view-macro.md` | The macro surface + `REQ-API-001..029`. |
| Components section | `../SUBTASK_components_props_slots/components-props-slots.md` | The component model + `REQ-API-030..059`. |
| Context section | `../SUBTASK_context/context.md` | Context + `REQ-API-060..079`. |
| Parent 1.0 requirements | `../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | Trace `REQ-API-*` back to `REQ-FW-005`/`009`/`014` (read-only). |

### Declared output
- `../authoring-model.md` (this spoke's workspace root) — the consolidated authoring model: a coherent
  narrative across the macro, the component model, and context; the merged, collision-free `REQ-API-*`
  register; the macro's relationship to the existing `VNode`/keyed-diff model stated as additive; and a
  by-name peer view-macro comparison (Leptos/Sycamore/Dioxus/Yew). This is the deliverable the outer design
  PR places at `design/ferric/authoring-model.md`.
- `../SYNTHESIS.md` (fold location = parent workspace root) — the fold record: how the three sections
  composed, the IA1–IA6 assertion results, and the merged register summary.

### Success criteria
- [ ] IA1–IA6 each asserted with a pass/fail result; any failure reported as a structured signal, not plugged.
      (IA1 bands disjoint; IA2 invocation seam closed; IA3 context seam closed; IA4 additive over frozen
      surface; IA5 one deliverable, no section unplaced/double-placed, no id collision; IA6 testable
      diagnostics + inherited verification methods.)
- [ ] `authoring-model.md` reads as one coherent authoring story, not three stapled sections, with example
      snippets of what an author writes throughout.
- [ ] The merged `REQ-API-*` register is complete and collision-free, conforming to
      `../../contracts/id_and_traceability_schema.yaml`.
- [ ] The avoid-ai-writing pass is run over the consolidated document and flagged tells fixed before
      finalizing.
- [ ] The parent `SUBTASK_authoring_model` is folded: `../SYNTHESIS.md` authored at the fold location and the
      parent resumed `SUSPENDED → COMPLETED`.

### Constraints
- Mint no new `REQ-API-*` ids; consolidate the three bands as written (additive-only).
- Report identity failures; do not silently reconcile divergent sections — request an amendment if a section
  is inadequate.
- Honor the writing-voice rules; the avoid-ai-writing pass over the consolidated document is mandatory.
- This is the subtree's fold: author `../SYNTHESIS.md` at the fold location and resume the parent per the DAG
  synthesis-fold contract.
