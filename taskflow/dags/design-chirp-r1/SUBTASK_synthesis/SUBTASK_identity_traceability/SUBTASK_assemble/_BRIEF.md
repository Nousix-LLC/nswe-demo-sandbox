# Task: Assemble the matrix skeleton, assert BAR_COVERS_GATING_REQS, collect the eight verdicts, and fold

## Task Specification
**Slug**: SUBTASK_assemble
**Task Kind**: synthesis
**Depends on**: SUBTASK_matrix_prod_dom, SUBTASK_matrix_ux, SUBTASK_matrix_id_ops, SUBTASK_bar_mapping, SUBTASK_backlog_pr, SUBTASK_concern_surface
**Status**: Pending

### Objective
Join the six spoke outputs into the whole-DAG **traceability-matrix skeleton** (every inherited column except
`live_status`), assert the one inherently **cross-source** identity `BAR_COVERS_GATING_REQS`, collect **all eight**
identity verdicts with their evidence into the gate deliverable, and **fold** this subtree so
`SUBTASK_identity_traceability` reaches COMPLETED with the deliverable present for the sibling `SUBTASK_fold`.

### Context
This is the synthesis/verification gate for `SUBTASK_identity_traceability` (see `../_GLOBAL.md` and
`../contracts/_MANIFEST.yaml`). The six spokes are COMPLETED; read their outputs directly. Its job is mechanical:
join the owned slices, run the cross-source assertion, verify each spoke recorded its identity verdict (no silent
plugs), and produce the one deliverable — then fold.

**Dependencies**: the six spokes above. **Dependents**: `SUBTASK_fold` (the gate's fold node, which reads the
deliverable and joins the sibling's per-`BAR-*` `live_status`).

### Inputs
| Input | Source (from this workspace) | Purpose |
|-------|------------------------------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, the join rule |
| Subtree sub-contract | `../contracts/_MANIFEST.yaml` | Column + identity ownership, the `join_rule`, `BAR_COVERS_GATING_REQS` assignment, fold wiring — READ-ONLY |
| Gate sub-contract | `../../contracts/_MANIFEST.yaml` | How this gate's deliverable is keyed for the fold's `live_status` join — READ-ONLY |
| Inherited contracts | `../../../contracts/` | The id scheme, matrix columns, `live_status`/verification-method vocab, the eight identity statements — READ-ONLY |
| Design skeleton (PROD+DOM) | `../SUBTASK_matrix_prod_dom/outputs/skeleton-prod-dom.md` | `req_id`, `release_gating`, `design_doc_ref` for PROD + DOM |
| Design skeleton (UX) | `../SUBTASK_matrix_ux/outputs/skeleton-ux.md` | Same columns for UX |
| Design skeleton (ID+OPS) | `../SUBTASK_matrix_id_ops/outputs/skeleton-id-ops.md` | Same columns for ID + OPS |
| Bar mapping | `../SUBTASK_bar_mapping/outputs/bar-mapping.md` | `REQ → bar_ids`; the `BAR_TESTABLE` verdict |
| Backlog/PR mapping | `../SUBTASK_backlog_pr/outputs/backlog-pr.md` | `REQ/BAR → (epic, issue_numbers)`; `ISSUE_TRACES`, `GAP_HAS_ISSUE`, `GITHUB_HYGIENE`, `ONE_OWNER_PER_FILE` verdicts |
| Concern/surface | `../SUBTASK_concern_surface/outputs/concern-surface.md` | `CONCERN_COVERAGE`, `SURFACE_COVERAGE` verdicts |

### Process (described, not prescribed)
- **Join** one matrix row per `REQ-*` per the sub-contract `join_rule`: `req_id`/`release_gating`/`design_doc_ref`
  from the owning design spoke; `bar_ids` from the bar mapping; `epic`/`issue_numbers` from the backlog mapping;
  `live_status` left empty (the sibling's, joined by `SUBTASK_fold`). Key the matrix so the fold can attach each
  `BAR-*`'s `live_status` by `bar_id` without re-deriving the mapping. Flag any `req_id` present in one slice but
  missing from another.
- **Assert `BAR_COVERS_GATING_REQS`** (cross-source): every release-gating `REQ-*` (from the design slices) is
  covered by ≥1 `BAR-*` (from the `REQ → bar_ids` map). Record the verdict with evidence; list every release-gating
  `REQ-*` with no `BAR-*` as a `FAIL`/gap with whether it is fixable — do not hide it.
- **Collect** all eight identity verdicts (the six produced by the spokes — `ONE_OWNER_PER_FILE`, `CONCERN_COVERAGE`,
  `SURFACE_COVERAGE`, `BAR_TESTABLE`, `ISSUE_TRACES`, `GAP_HAS_ISSUE` — plus the just-asserted
  `BAR_COVERS_GATING_REQS`; note `GAP_HAS_ISSUE`'s live-measurement half is the sibling's). Verify each carries a
  verdict with evidence; if any spoke left one bare, that is a reportable failure of this gate, not something to plug.

### Output
- `../outputs/identity-and-traceability.md` — the gate deliverable: the eight identity verdicts (each `PASS`/`FAIL`
  with recorded evidence and, on `FAIL`, what is missing and whether it is fixable), followed by the
  traceability-matrix skeleton (one row per `REQ-*`: `req_id`, `release_gating`, `bar_ids`, `epic`, `issue_numbers`,
  `design_doc_ref`; `live_status` left for the fold). Keyed/formatted so the fold joins the sibling's per-`BAR-*`
  `live_status` mechanically. Uses inherited column names and ids verbatim.
- `../SYNTHESIS.md` — the fold record at the subtree root (the SUSPENDED parent's directory): ownership coverage
  (every owned artifact produced by its one owner), the eight identity dispositions, and how the slices composed
  into the deliverable. Then resume the parent `SUBTASK_identity_traceability` (SUSPENDED → COMPLETED) with this
  `SYNTHESIS.md` as the fold seam.

### Success criteria
- [ ] Every release-gating `REQ-*` is a matrix row with `bar_ids` (≥1), covering `epic`/`issue_numbers`, and a
      `design_doc_ref`; any gating `REQ-*` lacking a `BAR-*` or an issue is a surfaced `FAIL`/gap, not hidden.
- [ ] All eight identities carry a verdict with recorded evidence in the deliverable; none bare, none silently plugged.
- [ ] The matrix uses the inherited column names and `REQ-*`/`BAR-*`/`EPIC-*`/issue ids verbatim; `live_status` is
      present-but-empty and keyed for the fold's per-`bar_id` join.
- [ ] Ownership coverage holds: each owned artifact was produced by its one declared owner; no double-writes.
- [ ] The deliverable and `SYNTHESIS.md` carry no host/system/taskflow detail and no attribution trailer.

### Constraints
- Synthesis is mechanical join + assertion + collection; do not re-derive a spoke's slice or overwrite a spoke output.
- No silent plugs: a failing identity or an uncovered gating `REQ-*` is reported with evidence (and flagged fixable
  where it is) for the gate's fold to act on; it is never reconciled quietly or passed bare.
- Read-only over completed inputs; this subtree edits no design/bar/backlog output.
- The `design` methodology loader is unavailable run-wide (`agent_domain_unset`); record the limitation and proceed.
- Deliverable and fold record carry repository identity only (`owner/repo`, commit SHA, repo-relative paths, ids).
