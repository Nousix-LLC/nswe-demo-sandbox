# Task: Backups and recovery — operational requirements

## Task Specification
**Slug**: SUBTASK_ops_backups_recovery
**Task Kind**: standard
**Status**: Pending

### Objective
State, as testable `REQ-OPS-*` requirements, the **backup and recovery path** a release of chirp requires:
how user data is backed up, how long backups are kept, how much data loss and how much downtime are
tolerable, how a restore is performed and verified, and how the product recovers from a bad deploy.

### Context
Part of the operational-readiness subtree (see `../_GLOBAL.md`, `../contracts/`). You own the
`backups_and_recovery` section of `design/operational-readiness.md`, written as the fragment
`outputs/backups-recovery.md`, and the `REQ-OPS-020..039` number range. You **depend on**
`SUBTASK_ops_durable_data`: read its completed `outputs/durable-data.md` and build your backup/recovery
requirements on the durability posture it states and on the domain backup capability `REQ-DOM-116`
(backup/restore brings data back intact and consistent) and `REQ-PROD-038`. Reference its `REQ-OPS-*` ids
where your requirements build on them; do not restate durable-data requirements as your own.

**Dependencies**: `SUBTASK_ops_durable_data`.
**Dependents**: `SUBTASK_ops_synthesis` consolidates your section.

### Distinct aspects to cover (evaluate scope; decompose further only if warranted)
- A backup posture: that durable user data is backed up on a stated cadence and that backups are retained
  for a stated period.
- Recovery objectives: a recovery-point objective (tolerable data loss) and a recovery-time objective
  (tolerable downtime), each stated as a testable target a release commits to.
- A restore procedure requirement: that a restore is a defined, exercised path that brings back accounts,
  chirps, follows, and likes intact and consistent (`REQ-DOM-116`, `REQ-DOM-110/111/107` after restore).
- Recovery from a bad deploy: that a failed or data-damaging deploy can be rolled back or recovered from,
  consistent with upgrade-preserves-data (`REQ-DOM-118`).
- Backup verifiability: that backups are periodically proven restorable, not merely produced.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, partition, identities |
| Contract | `../contracts/` (read-only) | `REQ-OPS-*` scheme, your number range, verification vocabulary |
| Durable-data fragment | `../SUBTASK_ops_durable_data/outputs/durable-data.md` | The durability posture your backup/recovery requirements build on |
| Domain & app design | `../../SUBTASK_domain_app_design/outputs/domain-application-design.md` | `REQ-DOM-116` (backup/restore), `REQ-DOM-110/111/107/118` |
| Product requirements | `../../SUBTASK_product_requirements/outputs/product-requirements.md` | `REQ-PROD-038`, operator journey J9 |

## Methodology
Bundle IDs (Domain Mapping): **Release Readiness** (primary); **Release Definition** (supporting). The
`design` loader is unavailable in this environment; apply the product-design persona and this relayed
guidance, and record the unavailability rather than blocking.

## Output
- `outputs/backups-recovery.md` — the `backups_and_recovery` section prose plus the full `REQ-OPS-020..039`
  requirements, each with `statement`, testable `acceptance_criteria`, `verification_method`,
  `release_gating`, and `traces_to`. Repository-ready content.

## Success criteria
- [ ] Composes against `../contracts/`; uses only `REQ-OPS-020..039`; does not redefine the schema.
- [ ] Backup cadence/retention, an RPO and an RTO, an exercised restore, and bad-deploy recovery are each
      testable requirements consistent with the durable-data posture and `REQ-DOM-116`.
- [ ] Each requirement traces to `REQ-PROD-038` / the relevant `REQ-DOM-*` where one applies.
- [ ] Builds on the durable-data fragment by reference; does not restate its requirements.

## Constraints
- Requirements only — defer backup tooling, storage targets, and restore scripting to code DAGs.
- Repository-ready hygiene — no host/cluster/taskflow detail; describe operations by product/repository
  identity; no attribution trailers.
