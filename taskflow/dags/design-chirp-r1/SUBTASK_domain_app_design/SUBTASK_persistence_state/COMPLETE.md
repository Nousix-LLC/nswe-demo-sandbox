# COMPLETE — SUBTASK_persistence_state

## What this task produced

The `persistence_requirement` section of `design/domain-application-design.md`, as
`outputs/persistence-state.md`: the durable-persistence requirement for chirp stated as requirements
`REQ-DOM-100..118` (the owned `100..149` range), each with a statement from the operator's/user's side,
testable acceptance criteria, a `release_gating` flag, and traces to `REQ-PROD-*` and the domain-model
`REQ-DOM-*` it builds on.

## What it states

- **What must survive a restart/redeploy** (REQ-DOM-100..108): Accounts in full, the account-associated
  Credential and Verified contact (durable + non-public), Chirps, the Follow graph, Likes, and active
  Sessions; ended sessions stay ended; server-maintained counts stay correct; the derived Timeline is
  reconstructable from durable data (it is recorded as not itself required to be durable).
- **Durability as correctness** (REQ-DOM-109..112): acknowledged writes are durable before acknowledgement
  (no data loss); referential integrity, id uniqueness/non-reuse, and an applied account-deletion outcome all
  hold across restart and restore, with no half-applied state.
- **Where state lives** (REQ-DOM-113..115): authoritative state lives in a durable store distinct from the
  serving process; the `ChirpRepository` seam is backed by that store (the in-memory backing at `c805525` is
  named as the blocker this closes); readiness reflects durable-store availability.
- **Backup / recovery / export** (REQ-DOM-116..117): durable data can be backed up and restored intact, and
  is enumerable per account for self-service export.
- **Change over time** (REQ-DOM-118): upgrading the product preserves existing durable data.

## How it composes

- Entities referenced only by the domain model's canonical vocabulary; introduces no new entity.
- `REQ-DOM-*` kept within `100..149` (no collision with the domain-model `001..049` or module `200..249`
  ranges); the `REQ-<AREA>-NNN` scheme and per-requirement fields are used, not redefined.
- Every engineering *how* (store engine, schema, migrations, connection handling, migration mechanics) is
  deferred by prose to the `software` domain. Operational targets (backup cadence/retention, RPO/RTO, restore
  runbook, availability) are deferred to the operational-readiness design (`REQ-OPS-*`), which consumes this
  section as its `durable_data` input. The Credential/Verified-contact structure is deferred to the
  identity/security design (`REQ-ID-*`).

## Downstream

- `SUBTASK_dad_synthesis` folds these `REQ-DOM-*` into the consolidated file's
  `requirements_and_acceptance_criteria` register and asserts the subtree contract identities
  (`ONE_ENTITY_VOCABULARY`, `REQ_DOM_NO_COLLISION`, `REQ_DOM_WELL_FORMED`, `DURABILITY_TESTABLE`,
  `REQ_DOM_TRACES_PROD`).
- `design-chirp-r1`'s `SUBTASK_operational_readiness` consumes the persistence model; `SUBTASK_release_bar`
  turns the `release_gating: true` requirements (core durability REQ-DOM-100/109/113, backup/restore
  REQ-DOM-116, readiness REQ-DOM-115) into `BAR-*` criteria.

## Output

- `outputs/persistence-state.md` — the repository-ready `persistence_requirement` section content.
