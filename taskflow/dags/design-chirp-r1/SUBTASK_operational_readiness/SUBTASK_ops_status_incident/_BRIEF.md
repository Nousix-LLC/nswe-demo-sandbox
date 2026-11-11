# Task: Status and incident posture — operational requirements

## Task Specification
**Slug**: SUBTASK_ops_status_incident
**Task Kind**: standard
**Status**: Pending

### Objective
State, as testable `REQ-OPS-*` requirements, **how operators and users learn when something is wrong** — an
incident-detection-and-response posture built on the observability signals, a way to communicate outages
and planned maintenance to users, and the user-facing degraded-state expectation.

### Context
Part of the operational-readiness subtree (see `../_GLOBAL.md`, `../contracts/`). You own the
`status_and_incident` section of `design/operational-readiness.md`, written as the fragment
`outputs/status-incident.md`, and the `REQ-OPS-080..099` number range. You **depend on**
`SUBTASK_ops_observability`: read its completed `outputs/observability.md` and build your incident-detection
requirements on the signals it defines, referencing its `REQ-OPS-*` ids. The product's "reachable and
reasonably available" requirement is `REQ-PROD-040`; the user-facing error/degraded states are chiefly the
experience design's (`REQ-UX-*`) — reference that boundary rather than owning it.

**Dependencies**: `SUBTASK_ops_observability`.
**Dependents**: `SUBTASK_ops_synthesis` consolidates your section.

### Distinct aspects to cover (evaluate scope; decompose further only if warranted)
- Incident detection and response: that a degradation visible in the observability signals is detected and
  acted on, with a proportionate severity notion and a stated responsible-operator expectation — kept to the
  scale of a small hosted product, not a large on-call programme.
- User-facing status communication: a proportionate way for users to learn that the product is down or
  degraded (a status surface or in-product notice), and advance notice of planned maintenance.
- The degraded-state experience boundary: what the product owes a user during an outage or partial failure,
  referencing the experience design's error/degraded states (`REQ-UX-*`, `REQ-PROD-033/034`) rather than
  redesigning them here.
- Availability as an operated commitment: a stated, testable availability expectation that supports
  `REQ-PROD-040` (the numeric target is this design's to state; keep it proportionate).

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, partition, identities |
| Contract | `../contracts/` (read-only) | `REQ-OPS-*` scheme, your number range, verification vocabulary |
| Observability fragment | `../SUBTASK_ops_observability/outputs/observability.md` | The signals incident detection builds on |
| Product requirements | `../../SUBTASK_product_requirements/outputs/product-requirements.md` | `REQ-PROD-040/033/034`, operator journey J9 |

## Methodology
Bundle IDs (Domain Mapping): **Release Readiness** (primary); **Release Definition**, **Product Strategy**
(supporting). The `design` loader is unavailable in this environment; apply the product-design persona and
this relayed guidance, and record the unavailability rather than blocking.

## Output
- `outputs/status-incident.md` — the `status_and_incident` section prose plus the full `REQ-OPS-080..099`
  requirements, each with `statement`, testable `acceptance_criteria`, `verification_method`,
  `release_gating`, and `traces_to`. Repository-ready content.

## Success criteria
- [ ] Composes against `../contracts/`; uses only `REQ-OPS-080..099`; does not redefine the schema.
- [ ] Incident detection/response, user-facing outage and maintenance communication, and a stated
      availability expectation are each testable requirements that build on the observability signals.
- [ ] Each requirement traces to `REQ-PROD-040` / the relevant requirement where one applies; the
      degraded-state experience boundary with `REQ-UX-*` is referenced, not owned.

## Constraints
- Requirements only — defer status-page tooling, paging/alerting setup, and runbooks to code DAGs.
- Proportionate to a small hosted product; do not design an enterprise incident programme.
- Repository-ready hygiene — no host/cluster/taskflow detail; describe operations by product/repository
  identity; no attribution trailers.
