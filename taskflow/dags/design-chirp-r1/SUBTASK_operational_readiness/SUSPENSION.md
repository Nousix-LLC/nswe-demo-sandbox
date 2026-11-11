# SUSPENSION — SUBTASK_operational_readiness (NeedsDecompose)

## Decision
`decompose_evaluation = NeedsDecompose`. This task's brief enumerates five distinct operational concerns
(durable data; backups & recovery; limits & quotas; observability; status & incident) held to a testable
release bar. The Scope-Based trigger and Distinct Concerns Test fire by that enumeration (the enumerated-concerns
rule), and the Output-Size trigger aligns (a seven-section testable `REQ-OPS-*` register exceeds 400 lines).
The only arguments for `Atomic` were "one coherent operations picture one specialist holds whole" and "a
sibling area design was done in one invocation" — both of which the standing contract and the Task Generation
Invariant forbid as grounds for Atomic. The decomposition was taken.

## Subtree materialized
Hub `_GLOBAL.md` and the sub-contract (`contracts/_MANIFEST.yaml`, `contracts/reqs_ops_partition.yaml`) are
authored at this workspace. Six children were materialized via `engine_amend_plan { add_task }`:

| Child | Depends on | Owns | Output |
|-------|-----------|------|--------|
| `SUBTASK_ops_durable_data` | none | `REQ-OPS-001..019`, section `durable_data` | `outputs/durable-data.md` |
| `SUBTASK_ops_backups_recovery` | `SUBTASK_ops_durable_data` | `REQ-OPS-020..039`, section `backups_and_recovery` | `outputs/backups-recovery.md` |
| `SUBTASK_ops_limits_quotas` | none | `REQ-OPS-040..059`, section `limits_and_quotas` | `outputs/limits-quotas.md` |
| `SUBTASK_ops_observability` | none | `REQ-OPS-060..079`, section `observability` | `outputs/observability.md` |
| `SUBTASK_ops_status_incident` | `SUBTASK_ops_observability` | `REQ-OPS-080..099`, section `status_and_incident` | `outputs/status-incident.md` |
| `SUBTASK_ops_synthesis` (synthesis gate) | all five above | `existing_followups`, consolidated register, fold | `outputs/operational-readiness.md`, `SYNTHESIS.md` |

## Contract (the frozen seam)
`contracts/` extends the ancestor `../contracts/` additively: it sub-partitions the one `REQ-OPS-*` number
space across the five concern children (no collisions), assigns the seven required sections to owners, and
declares the identities the synthesis gate asserts (all sections present; concern coverage; no number
collision; every `REQ-OPS-*` testable with a verification method and release-gating flag; traceability;
#23/#24/#25 folded not duplicated).

## Resumption condition
All children reach terminal state. `SUBTASK_ops_synthesis` folds the subtree: it assembles
`outputs/operational-readiness.md`, authors `SYNTHESIS.md` at this workspace (the fold location), and resumes
this task, which then reaches COMPLETED with `outputs/operational-readiness.md` as its declared output.

## Environment note
The Phase-B `design` methodology loader is unavailable here (`agent_domain_unset`); methodology bundle IDs
are relayed to each child in its brief, and children apply the product-design persona and that guidance.
