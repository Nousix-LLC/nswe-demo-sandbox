# Task: Extract the design-side matrix skeleton rows for REQ-ID-* and REQ-OPS-*

## Task Specification
**Slug**: SUBTASK_matrix_id_ops
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Produce the traceability-matrix skeleton's **design-side columns** (`req_id`, `release_gating`, `design_doc_ref`)
for every `REQ-ID-*` (identity, security & trust) and every `REQ-OPS-*` (operational readiness), so the synthesis
child can join them with the other slices.

### Context
Part of `SUBTASK_identity_traceability` (see `../_GLOBAL.md`). This spoke owns the design-side columns for two areas.
It does **not** compute `bar_ids`, `epic`, or `issue_numbers`, and asserts no identity.

**Dependencies**: none. **Dependents**: `SUBTASK_assemble`.

### Inputs
| Input | Source (from this workspace) | Purpose |
|-------|------------------------------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints |
| Subtree sub-contract | `../contracts/_MANIFEST.yaml` | Column ownership + the matrix row key (`req_id`) — READ-ONLY |
| Inherited schema | `../../../contracts/id_and_traceability_schema.yaml` | The `REQ-<AREA>-NNN` id format and matrix columns (do not redefine) |
| Design-artifact map | `../../../contracts/design_artifact_map.yaml` | The repo-relative `design_doc_ref` path for each area |
| Identity, security & trust | `../../../SUBTASK_identity_trust/outputs/identity-security.md` | `REQ-ID-*` entries |
| Operational readiness | `../../../SUBTASK_operational_readiness/SUBTASK_ops_synthesis/outputs/operational-readiness.md` | `REQ-OPS-*` entries |

Each requirement entry carries a `- **release_gating**: true|false` field; `design_doc_ref` is the area's
repo-relative design path (from the artifact map) plus the requirement's own section/heading. Note the operational
area's design lives at the ops subtree's synthesis-child output path shown above.

### Output
- `outputs/skeleton-id-ops.md` — one row per `REQ-ID-*` and `REQ-OPS-*`, keyed by `req_id`, carrying
  `release_gating` (verbatim true/false) and `design_doc_ref` (repo-relative path + section). Use the inherited
  `req_id` strings verbatim. Format as a table the synthesis child can join on `req_id`.

### Success criteria
- [ ] Every `REQ-ID-*` and `REQ-OPS-*` present in the two design files appears as exactly one row (count stated;
      expected on the order of 110 + 109, but report the actual count found).
- [ ] Each row's `release_gating` matches the design file verbatim; each `design_doc_ref` resolves to the correct
      repo-relative design file + the requirement's section.
- [ ] `req_id` strings are used verbatim; no renamed scheme; no row for a non-existent id.
- [ ] Any requirement whose `release_gating` field is absent or malformed is flagged in the output, not guessed.

### Constraints
- Design-side columns only; do not compute `bar_ids`, `epic`, or `issue_numbers`, and assert no identity.
- Read-only over completed inputs; report anomalies, do not edit the design files.
- The `design` methodology loader is unavailable run-wide (`agent_domain_unset`); record the limitation and proceed.
- Output carries no host/system/taskflow detail and no attribution trailer.
