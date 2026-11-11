# Task: Operational readiness for release — design requirements for chirp

## Task Specification
**Slug**: SUBTASK_operational_readiness
**Task Kind**: standard
**Status**: Pending

### Objective
Design what must be true in production **beyond "it runs"**, as release requirements: durable data, a backup and
recovery path, limits/quotas, observability, and a status/incident posture — to the bar of **a product that can
be operated, not just started**.

### Context
Part of design-chirp-r1 (see `../_GLOBAL.md`, `../contracts/`). You own `design/operational-readiness.md` and
`REQ-OPS-*`. You **consume** the durable-persistence model from `SUBTASK_domain_app_design` and design backups,
recovery, limits, and observability around it. Existing open follow-ups #23/#24/#25 are
hardening/polish items — **fold them in where they belong** in your requirements and (later) the backlog,
rather than duplicating them.
**Dependencies**: `SUBTASK_product_requirements`, `SUBTASK_domain_app_design`.
**Dependents**: `SUBTASK_release_bar` consolidates `REQ-OPS-*`.

## Distinct concerns in this task
Evaluate your own scope against these and decompose if warranted:
- **Durable data** — what durability/retention the product requires in production (built on the domain
  persistence requirement).
- **Backups & recovery** — the path to recover from data loss or a bad deploy.
- **Limits & quotas** — rate/size limits a public product needs.
- **Observability** — what must be visible to operate the product (health, logs, metrics as requirements).
- **Status & incident** — how operators and users learn when something is wrong.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context/constraints |
| Contract | `../contracts/` (read-only) | `REQ-OPS-*` scheme; your file + required sections |
| Domain/app design | `../SUBTASK_domain_app_design/outputs/domain-application-design.md` | The persistence model to build operations on |
| Product requirements | `../SUBTASK_product_requirements/outputs/product-requirements.md` | Product scope that sets operational needs |
| Repo + board | `Nousix-LLC/nswe-demo` @ `c805525`; issues #23/#24/#25 | Current deploy/CI; follow-ups to fold in |

## Methodology
Bundle IDs (Domain Mapping): **Release Readiness** (primary — operational expectations for release);
**Release Definition**, **Product Strategy**, **Identity and Trust** (supporting).

## Output
- `SUBTASK_operational_readiness/outputs/operational-readiness.md` with the required sections in
  `../contracts/design_artifact_map.yaml` and `REQ-OPS-*` ids. Repository-ready content.

## Success criteria
- [ ] Composes against `../contracts/`; `REQ-OPS-*` used; schema not redefined.
- [ ] Durable data, backups/recovery, limits/quotas, observability, and status/incident are each stated as
      testable requirements consistent with the domain persistence model.
- [ ] #23/#24/#25 placed where they belong (folded, not duplicated).
- [ ] Every `REQ-OPS-*` has testable acceptance criteria and a release-gating flag; traces to `REQ-PROD-*`/`REQ-DOM-*`.

## Constraints
- Requirements only — defer operational implementation to code DAGs.
- Repository-ready hygiene (no host/system/taskflow detail — describe operations by repository/product
  identity, never by cluster/host address; no attribution trailers).
