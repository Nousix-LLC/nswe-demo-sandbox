# Task: Synthesis — assemble concern 4 and fold (Ferric 1.0, concern 4 synthesis)

## Task Specification
**Slug**: SUBTASK_afe_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective
Verify the three concern-4 capability fragments composed against the sub-contract, then merge them into
the single design doc `async-forms-events.md` — one continuous `REQ-ASYNC-*` register with sections for
async resources, events + payloads, and forms + binding — and fold this subtree's parent
(`SUBTASK_async_forms_events`) to COMPLETED.

### Context
This is the synthesis gate for concern 4 (see `../_GLOBAL.md`). Its three sibling spokes each wrote a
fragment and a disjoint slice of the `REQ-ASYNC-*` register. The parent decomposition expects exactly
one output doc from concern 4 (`async-forms-events.md`, repo target `design/ferric/async-forms-events.md`
per `../../contracts/design_artifact_map.yaml`), so this task assembles the fragments into that one doc.

**Dependencies**: `SUBTASK_afe_async_resources`, `SUBTASK_afe_events_payloads`, `SUBTASK_afe_forms_binding`.

### Scope to cover
- **Evaluate sub-identities J1–J7** from `../contracts/_MANIFEST.yaml` as assertions over the three
  fragments (disjoint id ranges; coverage of every `REQ-FW-006` clause; the payload seam defined once
  and referenced read-only by forms; additive-over-frozen; SSR by reference only; one assembled artifact;
  conformance to the parent schema). Report any failure as a structured signal — **no silent plugs**; if
  an identity fails, say so rather than patching the fragment.
- **Assemble** `async-forms-events.md`: a short framing (what concern 4 settles, traced to `REQ-FW-006`),
  then the three capability sections carrying their `REQ-ASYNC-*` requirements in one continuous register
  (ascending id order), then a metadata section (owning task, repo target, conformance, grounding commit,
  register summary). Preserve each fragment's requirements verbatim in substance; do not mint new ids.
- Confirm cross-references resolve (the forms payload-handler reference points at the real
  `REQ-ASYNC-02x` id the events fragment registered).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | The assembly target and output spec. |
| Sub-contract | `../contracts/_MANIFEST.yaml` | J1–J7 to assert; ownership and ranges. |
| Parent contract | `../../contracts/id_and_traceability_schema.yaml`, `../../contracts/design_artifact_map.yaml` | Schema conformance; the repo path for the assembled doc. |
| Async fragment | `../SUBTASK_afe_async_resources/async-resources.md` | REQ-ASYNC-001..019 to merge. |
| Events fragment | `../SUBTASK_afe_events_payloads/events-and-payloads.md` | REQ-ASYNC-020..039 to merge. |
| Forms fragment | `../SUBTASK_afe_forms_binding/forms-binding.md` | REQ-ASYNC-040..059 to merge. |

### Declared output
- `../async-forms-events.md` (the parent workspace) — the one assembled concern-4 design doc + register.
- `../SYNTHESIS.md` (the parent workspace, the fold location) — the J1–J7 verdict and how the fragments
  composed; the record the fold consumes.

### Success criteria
- [ ] J1–J7 each evaluated with a pass/fail verdict recorded in `../SYNTHESIS.md`; any failure surfaced,
      not plugged.
- [ ] `../async-forms-events.md` carries one continuous `REQ-ASYNC-*` register (all three ranges, in
      order) covering every `REQ-FW-006` clause, conforming to the parent schema.
- [ ] The doc is placed exactly once at the parent workspace (serves parent identity I8 for this doc).
- [ ] The writing-voice pass is run over the assembled doc before finalizing.

### Constraints
- Assemble and verify; do not mint new `REQ-ASYNC-*` ids or redesign the capabilities.
- After authoring `../async-forms-events.md` and `../SYNTHESIS.md`, complete and fold the parent
  (`engine_resume_suspended` with `seam_path` = `../SYNTHESIS.md`).
- Honor the writing-voice rules in `../_GLOBAL.md`.
