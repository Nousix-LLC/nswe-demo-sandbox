# COMPLETE — SUBTASK_ops_durable_data

## What was done
Authored the `durable_data` section of `design/operational-readiness.md` as the fragment
`outputs/durable-data.md`: the production **durability** and **data-retention** posture of chirp, stated as
testable `REQ-OPS-*` requirements that build on the domain persistence model (`REQ-DOM-100..118`) by
reference rather than restating it.

## What was produced
- `outputs/durable-data.md` — the `durable_data` section prose plus requirements **REQ-OPS-001..016**
  (within the assigned `REQ-OPS-001..019` range; range not filled, gaps deliberate). Each requirement has
  `statement`, testable `acceptance_criteria`, a `verification_method` from the contract vocabulary
  (`operational_check` / `manual_user_check` / `inspection`), a `release_gating` flag (all true), and
  `traces_to` a `REQ-PROD-*` / `REQ-DOM-*`.

Coverage of the brief's distinct aspects:
- Production durability expectation (no data loss to restart/update/redeploy): REQ-OPS-001..004 — operational
  face of REQ-DOM-100/113/114/118.
- Acknowledged-write durability as an operated property: REQ-OPS-005 — REQ-DOM-109.
- Integrity across operational events (invariants after restart and after restore; no half-applied state):
  REQ-OPS-006..008 — REQ-DOM-107/110/111/112/116.
- Durable-store reachability as a durability requirement (readiness signal deferred to observability):
  REQ-OPS-009 — REQ-DOM-115 / REQ-PROD-039.
- Data-retention posture (live-account retention, deleted-account window, backup retention bound,
  retention↔export parity, sessions, private identity data, stated/discoverable posture): REQ-OPS-010..016 —
  REQ-DOM-037/112/117/102/106, REQ-PROD-037/038/019.

## How it composes with the parent
- Composes against `../contracts/` (`reqs_ops_partition.yaml`, `_MANIFEST.yaml`) and the ancestor
  `../../contracts/` (id/traceability schema, design-artifact map): uses only the `durable_data` section and
  the `REQ-OPS-001..019` range; redefines nothing.
- The dependent `SUBTASK_ops_backups_recovery` builds on the durability posture here — specifically
  REQ-OPS-007 (invariants hold after a restore) and REQ-OPS-012 (a stated backup-retention bound) — which it
  turns into backup cadence, retention schedule, recovery-point/recovery-time targets, and the restore
  procedure in `REQ-OPS-020..039`.
- `SUBTASK_ops_synthesis` consolidates this fragment's prose and requirements into
  `outputs/operational-readiness.md` and the consolidated register, and asserts the contract identities
  (ALL_SECTIONS_PRESENT, CONCERN_COVERAGE, NO_NUMBER_COLLISION, OPS_TESTABLE, OPS_TRACES).

## Constraints honored
- Requirements only; durability implementation (store engine, replication, snapshots, migrations) deferred
  by prose to the code DAGs.
- Repository-ready hygiene: named by product/repository identity (`Nousix-LLC/nswe-demo @ c805525`,
  `ChirpRepository`, `chirp-server`); no host/cluster/taskflow detail; no attribution trailer.

## Environment note
The Phase-B `design` methodology loader was unavailable (`agent_domain_unset`). Per the brief and subtree
hub, the product-designer persona's release-readiness judgment and the relayed bundle guidance (Release
Readiness primary; Release Definition, Product Strategy supporting) were applied, and the unavailability is
recorded in the fragment and here rather than treated as a blocker.
