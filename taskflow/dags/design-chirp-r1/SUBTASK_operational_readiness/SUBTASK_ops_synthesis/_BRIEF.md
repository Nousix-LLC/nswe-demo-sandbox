# Task: Operational-readiness synthesis — verification gate + fold

## Task Specification
**Slug**: SUBTASK_ops_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective
Assemble the five concern fragments into the single `outputs/operational-readiness.md` deliverable with all
seven required sections; author the two cross-cutting sections (`existing_followups` and the consolidated
`requirements_and_acceptance_criteria` register); **verify** the contract identities with recorded evidence;
and fold the result back into the suspended parent task `SUBTASK_operational_readiness`.

### Context
Part of the operational-readiness subtree (see `../_GLOBAL.md`, `../contracts/`). This is the subtree's
verification gate, not a prose summary. It consolidates the five siblings' outputs into the deliverable the
parent owns (`design/operational-readiness.md`), reconciles the cross-concern references (backups → durable
data; status/incident → observability), and asserts the identities in `../contracts/_MANIFEST.yaml` with
recorded evidence. Where it finds a gap it reports it; it does **not** silently plug a failing identity. The
method for running a synthesis gate is engineering practice in the `software` domain's `synthesis` bundle,
reached by prose; do not duplicate it here.

**Dependencies**: `SUBTASK_ops_durable_data`, `SUBTASK_ops_backups_recovery`, `SUBTASK_ops_limits_quotas`,
`SUBTASK_ops_observability`, `SUBTASK_ops_status_incident`.
**Dependents**: the parent `SUBTASK_operational_readiness` resolves via this fold.

### What this gate must produce and verify
- **Assemble** `outputs/operational-readiness.md` with the seven required sections from
  `../contracts/design_artifact_map.yaml`, in order: `durable_data`, `backups_and_recovery`,
  `limits_and_quotas`, `observability`, `status_and_incident`, `existing_followups`,
  `requirements_and_acceptance_criteria`. The five concern bodies are the siblings' fragments, carried
  faithfully; do not rewrite their requirements.
- **Author `existing_followups`**: place issues #23, #24, and #25 in the section each belongs to and record
  the placement here — candidate homes the fragments flagged are #23 → observability/availability, #24 →
  limits/access and operational security, #25 → durable-data/deploy posture; decide the final placement.
  Fold them (note where an existing `REQ-OPS-*` already covers the substance); do not duplicate them as new
  requirements, and note they are non-release-gating hardening/polish.
- **Author `requirements_and_acceptance_criteria`**: the consolidated `REQ-OPS-*` register as the verbatim
  union of the five fragments, plus the OPS traceability table (`REQ-OPS-* → REQ-PROD-*/REQ-DOM-*`,
  release_gating) — the derived artifact the contract declares.
- **Assert the identities** in `../contracts/_MANIFEST.yaml` (`ALL_SECTIONS_PRESENT`, `CONCERN_COVERAGE`,
  `NO_NUMBER_COLLISION`, `OPS_TESTABLE`, `OPS_TRACES`, `FOLLOWUPS_FOLDED`) with recorded evidence; report any
  failure rather than plugging it.
- **Fold**: author `SYNTHESIS.md` at the parent's workspace (the fold location) recording the evidence, then
  resume the suspended parent `SUBTASK_operational_readiness` with that record so the parent reaches
  COMPLETED with `outputs/operational-readiness.md` as its output.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, partition, identities |
| Contract | `../contracts/` (read-only) | Identities to assert; the required sections and the number-space partition |
| Durable-data fragment | `../SUBTASK_ops_durable_data/outputs/durable-data.md` | `durable_data` section + `REQ-OPS-001..019` |
| Backups/recovery fragment | `../SUBTASK_ops_backups_recovery/outputs/backups-recovery.md` | `backups_and_recovery` section + `REQ-OPS-020..039` |
| Limits/quotas fragment | `../SUBTASK_ops_limits_quotas/outputs/limits-quotas.md` | `limits_and_quotas` section + `REQ-OPS-040..059` |
| Observability fragment | `../SUBTASK_ops_observability/outputs/observability.md` | `observability` section + `REQ-OPS-060..079` |
| Status/incident fragment | `../SUBTASK_ops_status_incident/outputs/status-incident.md` | `status_and_incident` section + `REQ-OPS-080..099` |
| Product & domain designs | `../../SUBTASK_product_requirements/outputs/product-requirements.md`, `../../SUBTASK_domain_app_design/outputs/domain-application-design.md` | Check `traces_to` targets resolve |

## Methodology
Bundle IDs (Domain Mapping): **Release Definition** (primary — CompletenessAndGapReview, ReleaseBar posture);
**Release Readiness** (supporting). Synthesis-gate method from the `software`/`synthesis` bundle by prose.
The `design` loader is unavailable in this environment; apply the product-design persona and this relayed
guidance, and record the unavailability rather than blocking.

## Output
- `outputs/operational-readiness.md` — the assembled deliverable with all seven sections and the
  consolidated register + traceability table. Repository-ready content.
- `SYNTHESIS.md` at the parent fold location — the fold record carrying the identity evidence.

## Success criteria
- [ ] All seven required sections present and in order; the five concern bodies carried faithfully.
- [ ] `existing_followups` places #23/#24/#25 where they belong, folded and not duplicated, marked non-gating.
- [ ] Consolidated `REQ-OPS-*` register is the verbatim union with no number collisions; traceability table present.
- [ ] Every contract identity asserted with recorded evidence; any failure reported, none plugged.
- [ ] The parent `SUBTASK_operational_readiness` is resolved via the fold with `outputs/operational-readiness.md`.

## Constraints
- Requirements only; do not rewrite the siblings' requirements or invent new `REQ-OPS-*` beyond the
  consolidation and the followups-folding judgment.
- Repository-ready hygiene — no host/cluster/taskflow detail anywhere in `operational-readiness.md`;
  no attribution trailers. (`SYNTHESIS.md` is an internal fold record, not repository content.)
