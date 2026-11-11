# Task: The release bar + completeness/gap review for chirp

## Task Specification
**Slug**: SUBTASK_release_bar
**Task Kind**: standard
**Status**: Pending

### Objective
Consolidate the per-area requirements into (a) an **MVP-vs-releasable scoping** (what reaches a usable product
early vs what the release requires on top) and (b) the concrete, testable **release bar** (`BAR-*`), and run a
**completeness & gap review** over the whole design to catch missing surfaces and record in/out-of-scope
judgments. The bar must be specific enough that a later gap review, each code DAG, and each PR review can hold
the product to it **criterion by criterion**. "It deploys / is reachable / CI is green / a working skeleton"
is NOT a release bar.

### Context
Part of design-chirp-r1 (see `../_GLOBAL.md`, `../contracts/`). You own `design/release-bar.md` and the `BAR-*`
criteria. You read every concern design and tie its release-gating requirements to testable bar criteria.
**Dependencies**: `SUBTASK_product_requirements`, `SUBTASK_domain_app_design`, `SUBTASK_experience_design`,
`SUBTASK_identity_trust`, `SUBTASK_operational_readiness`.
**Dependents**: `SUBTASK_design_pr`, `SUBTASK_delivery_backlog`, `SUBTASK_synthesis`.

## Distinct concerns in this task
Evaluate your own scope against these and decompose if warranted:
- **MVP vs releasable scoping** — the honest line between what is usable early and what release requires;
  hidden cuts are worse than stated ones.
- **The release bar** — `BAR-*` criteria, each testable (a named verification method) and each referencing the
  `REQ-*` it enforces, across the stages.
- **Completeness & gap review** — a deliberate sweep (using the Product Surfaces lens) over the whole design
  for surfaces a product of this kind is expected to have but that no concern file covered — sign-up/in/
  recovery, account deletion, data export, onboarding, settings, notifications, admin/support, billing — and a
  recorded in-scope/out-of-scope judgment for each, so absence is a decision, not an oversight.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context/constraints |
| Contract | `../contracts/` (read-only) | `BAR-*` scheme, verification-method vocabulary, required sections |
| All five concern designs | `../SUBTASK_product_requirements/outputs/`, `../SUBTASK_domain_app_design/outputs/`, `../SUBTASK_experience_design/outputs/`, `../SUBTASK_identity_trust/outputs/`, `../SUBTASK_operational_readiness/outputs/` | The requirements to consolidate into the bar |

## Methodology
Bundle IDs (Domain Mapping): **Release Definition** (primary — MVP/release scoping, the release bar,
completeness & gap review); **Release Readiness**, **Product Strategy**, **Identity and Trust**,
**Product Surfaces** (supporting — the gap-review lens for missing surfaces).

## Output
- `SUBTASK_release_bar/outputs/release-bar.md` with the required sections in
  `../contracts/design_artifact_map.yaml`, `BAR-*` ids each referencing `REQ-*` and naming a verification
  method from the schema vocabulary. Repository-ready content.

## Success criteria
- [ ] Composes against `../contracts/`; `BAR-*` used; schema not redefined.
- [ ] Every release-gating `REQ-*` across all areas is covered by >=1 `BAR-*`.
- [ ] Every `BAR-*` is testable (named verification method) and references >=1 `REQ-*`; staged usable_early vs releasable.
- [ ] The gap review records an in/out-of-scope judgment for each expected surface, with reasons.

## Constraints
- A bar, not an aspiration — each criterion checkable by someone who was not in the room.
- Repository-ready hygiene (no host/system/taskflow detail, no attribution trailers).
