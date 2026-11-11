# Task: Map BAR-* to REQ-* and assert BAR_TESTABLE

## Task Specification
**Slug**: SUBTASK_bar_mapping
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
From the release bar, produce (a) a per-`BAR-*` table carrying each criterion's `stage`, `verification_method`, and
the `REQ-*` ids it references, and (b) the inverted **`REQ → bar_ids`** map the matrix needs; and **assert the
`BAR_TESTABLE` identity** with recorded evidence.

### Context
Part of `SUBTASK_identity_traceability` (see `../_GLOBAL.md`). This spoke owns the matrix's `bar_ids` column (as the
`REQ → bar_ids` map) and the `BAR_TESTABLE` identity. It does not build design rows, epic/issue traces, or the
cross-source `BAR_COVERS_GATING_REQS` identity (the synthesis child owns that, consuming this spoke's map).

**Dependencies**: none. **Dependents**: `SUBTASK_assemble`.

### Inputs
| Input | Source (from this workspace) | Purpose |
|-------|------------------------------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints |
| Subtree sub-contract | `../contracts/_MANIFEST.yaml` | `bar_ids` ownership + the `BAR_TESTABLE` assignment — READ-ONLY |
| Inherited schema | `../../../contracts/id_and_traceability_schema.yaml` | `BAR-NNN` format; the closed `verification_method` vocabulary; the `stage` values |
| DAG-root identities | `../../../contracts/_MANIFEST.yaml` | The exact `BAR_TESTABLE` statement to assert (do not restate it differently) |
| Release bar | `../../../SUBTASK_release_bar/outputs/release-bar.md` | The `BAR-*` criteria |

Each criterion reads `**BAR-NNN** (stage · verification_method) — statement _Enforces REQ-<AREA>-NNN[, …]._`.
The `verification_method` must be one of the inherited closed vocabulary (`manual_user_check`, `automated_test`,
`inspection`, `operational_check`).

### Output
- `outputs/bar-mapping.md` — containing:
  1. A per-`BAR-*` table (`bar_id`, `stage`, `verification_method`, referenced `REQ-*` ids), using ids verbatim;
     report the actual `BAR-*` count found.
  2. The inverted `REQ → bar_ids` map (one entry per `REQ-*` that any `BAR-*` enforces), for the synthesis join.
  3. The **`BAR_TESTABLE`** verdict (`PASS`/`FAIL`) with evidence: that every `BAR-*` names a `verification_method`
     from the vocabulary **and** references ≥1 `REQ-*`. On `FAIL`, list every offending `BAR-*` (missing/invalid
     method, or no `REQ-*` reference) and whether it is fixable.

### Success criteria
- [ ] Every `BAR-*` in the bar appears once in the per-`BAR-*` table with its `stage`, `verification_method`, and
      referenced `REQ-*`; count stated.
- [ ] The `REQ → bar_ids` map is complete over the bar's references and uses ids verbatim.
- [ ] `BAR_TESTABLE` carries a `PASS`/`FAIL` verdict with evidence; any offending `BAR-*` is named, not hidden.
- [ ] A `verification_method` outside the closed vocabulary is reported as a `BAR_TESTABLE` failure, not normalized.

### Constraints
- Own only `bar_ids` + `BAR_TESTABLE`; do not assert other identities or build other matrix columns.
- Read-only over the completed bar; report findings, do not edit it.
- The `design` methodology loader is unavailable run-wide (`agent_domain_unset`); record the limitation and proceed.
- Output carries no host/system/taskflow detail and no attribution trailer.
