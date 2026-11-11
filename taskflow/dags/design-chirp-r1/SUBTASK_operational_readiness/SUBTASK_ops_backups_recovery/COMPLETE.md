# COMPLETE — SUBTASK_ops_backups_recovery

## What was done
Authored the `backups_and_recovery` section of `design/operational-readiness.md` as the fragment
`outputs/backups-recovery.md`: section prose (what the backup/recovery path owes an operator, what it
defers) plus the `REQ-OPS-020..033` requirements (within the assigned `REQ-OPS-020..039` range).

## What was produced
- `outputs/backups-recovery.md` — repository-ready. 14 requirements, each with `statement`, testable
  `acceptance_criteria`, a `verification_method` from the contract vocabulary, a `release_gating` flag, and
  `traces_to`:
  - Backup posture — cadence (`REQ-OPS-020`), bounded retention (`REQ-OPS-021`), point-in-time consistency
    (`REQ-OPS-022`), independent storage (`REQ-OPS-023`).
  - Recovery objectives — recovery-point objective / tolerable data loss (`REQ-OPS-024`), recovery-time
    objective / tolerable downtime (`REQ-OPS-025`).
  - Restore procedure — defined and operator-performable (`REQ-OPS-026`), returns data intact and
    consistent (`REQ-OPS-027`), meets the stated RPO/RTO when exercised (`REQ-OPS-028`).
  - Bad-deploy recovery — rollback of a failed deploy with no data loss (`REQ-OPS-029`), restore after a
    data-damaging deploy (`REQ-OPS-030`).
  - Verifiability — periodic restore drill (`REQ-OPS-031`), backup failures surfaced not silent
    (`REQ-OPS-032`), posture documented where an operator can find it (`REQ-OPS-033`).

## How it composes with the parent
Owns exactly the `backups_and_recovery` section and the `REQ-OPS-020..039` number space per
`../contracts/reqs_ops_partition.yaml`; mints only `REQ-OPS-020..033` (gaps deliberate). Builds on the
durable-data fragment (`REQ-OPS-007` invariants-after-restore bar; `REQ-OPS-012` deleted-account backup
bound) by reference without restating it, and on `REQ-DOM-116` / `REQ-DOM-110/111/107` / `REQ-DOM-118` /
`REQ-PROD-038` / `REQ-PROD-040`. `SUBTASK_ops_synthesis` consolidates this fragment into
`outputs/operational-readiness.md` and the consolidated register.

## Contract conformance
- Uses only `REQ-OPS-020..039`; does not renumber outside range; does not write another child's section;
  does not redefine the ancestor id scheme or verification vocabulary.
- Every requirement carries the six schema fields; every `verification_method` is from the vocabulary;
  every requirement carries a `release_gating` flag; every `traces_to` names a real `REQ-PROD-*`/`REQ-DOM-*`.

## Environment note
The Phase-B `design` methodology loader was unavailable (`agent_domain_unset`); produced by applying the
product-design persona and the relayed Release Readiness / Release Definition guidance. Recorded in the
fragment's methodology note rather than treated as a blocker.
