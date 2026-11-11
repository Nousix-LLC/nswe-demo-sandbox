# Task: Durable data in production — operational requirements

## Task Specification
**Slug**: SUBTASK_ops_durable_data
**Task Kind**: standard
**Status**: Pending

### Objective
State, as testable `REQ-OPS-*` requirements, the **production durability posture** a release of chirp
requires — the operational half of the domain persistence model: that the product's authoritative state
lives durably, survives the normal operations of running a service, and is retained for as long as the
product promises.

### Context
Part of the operational-readiness subtree (see `../_GLOBAL.md`, `../contracts/`). You own the
`durable_data` section of `design/operational-readiness.md`, written as the fragment `outputs/durable-data.md`,
and the `REQ-OPS-001..019` number range. The domain design already fixed the persistence *model* as
`REQ-DOM-100..118` (authoritative state in a durable store distinct from the serving process; acknowledged
writes survive; invariants hold across restart/redeploy/restore; readiness reflects store reachability;
upgrades preserve data). Your job is the **operational posture around that model** — what an operator and a
user are owed in production — stated as requirements, **building on** those `REQ-DOM-*` ids by reference,
not restating them. The backups-and-recovery child depends on your section, so state the durability posture
it will build its backup/restore requirements on.

**Dependencies**: none.
**Dependents**: `SUBTASK_ops_backups_recovery` builds on your section; `SUBTASK_ops_synthesis` consolidates it.

### Distinct aspects to cover (evaluate scope; decompose further only if warranted)
- The production durability expectation: an operated deployment does not lose user data to a restart,
  update, or redeploy (the operational statement of `REQ-DOM-100`, `REQ-DOM-113/114`).
- Acknowledged-write durability as an operated property (`REQ-DOM-109`).
- Integrity across operational events: invariants still hold after a restart and a restore (`REQ-DOM-107/110/111/112`).
- A **data-retention posture**: how long user data and deleted-account data are kept, consistent with the
  defined deletion outcome (`REQ-DOM-037/112`) and with export (`REQ-DOM-117`); what retention a releasable
  product states.
- The durable store's reachability as part of readiness (`REQ-DOM-115`, `REQ-PROD-039`) — stated here as a
  durability requirement; the readiness *signal* itself is the observability child's.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, partition, identities |
| Contract | `../contracts/` (read-only) | `REQ-OPS-*` scheme, your number range, verification vocabulary |
| Domain & app design | `../../SUBTASK_domain_app_design/outputs/domain-application-design.md` | Persistence model `REQ-DOM-100..118` to build on |
| Product requirements | `../../SUBTASK_product_requirements/outputs/product-requirements.md` | `REQ-PROD-037` and the operator journey J9 |

## Methodology
Bundle IDs (Domain Mapping): **Release Readiness** (primary); **Release Definition**, **Product Strategy**
(supporting). The `design` loader is unavailable in this environment; apply the product-design persona and
this relayed guidance, and record the unavailability rather than blocking.

## Output
- `outputs/durable-data.md` — the `durable_data` section prose plus the full `REQ-OPS-001..019` requirements,
  each with `statement`, testable `acceptance_criteria`, `verification_method`, `release_gating`, and
  `traces_to`. Repository-ready content.

## Success criteria
- [ ] Composes against `../contracts/`; uses only `REQ-OPS-001..019`; does not redefine the schema.
- [ ] The production durability posture and a stated data-retention posture are each testable requirements
      consistent with `REQ-DOM-100..118`.
- [ ] Each requirement traces to `REQ-PROD-037` / the relevant `REQ-DOM-*` where one applies.
- [ ] Builds on the domain persistence model by reference; does not restate `REQ-DOM-*` content as new rules.

## Constraints
- Requirements only — defer durability implementation (store engine, replication, snapshots) to code DAGs.
- Repository-ready hygiene — no host/cluster/taskflow detail; describe operations by product/repository
  identity; no attribution trailers.
