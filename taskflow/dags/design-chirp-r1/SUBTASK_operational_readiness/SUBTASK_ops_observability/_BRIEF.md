# Task: Observability — operational requirements

## Task Specification
**Slug**: SUBTASK_ops_observability
**Task Kind**: standard
**Status**: Pending

### Objective
State, as testable `REQ-OPS-*` requirements, **what must be visible to operate chirp** — the health and
readiness signal, the logs, the metrics, and the audit trail an operator needs to answer "is it serving
users, and what is it doing?" — each as a requirement on what the product exposes, not a choice of tooling.

### Context
Part of the operational-readiness subtree (see `../_GLOBAL.md`, `../contracts/`). You own the
`observability` section of `design/operational-readiness.md`, written as the fragment
`outputs/observability.md`, and the `REQ-OPS-060..079` number range. The product already exposes a
liveness probe and needs a *readiness* meaning (`REQ-PROD-039`, `REQ-DOM-115/226`): readiness must reflect
that the durable store is reachable. The status-and-incident child depends on your section — state the
signals it will build incident detection and communication on. The operator journey J9 and the supported
admin surface `REQ-PROD-028` imply an audit trail for operator/admin actions. The existing follow-up **#23**
(exercise/harden the native install path) touches operational visibility of a deployment; reference it for
the synthesis fold rather than re-filing it.

**Dependencies**: none.
**Dependents**: `SUBTASK_ops_status_incident` builds on your section; `SUBTASK_ops_synthesis` consolidates it.

### Distinct aspects to cover (evaluate scope; decompose further only if warranted)
- The health-vs-readiness distinction: a readiness signal that reports not-ready when the product cannot
  serve users (including when its durable store is unreachable) and ready when it can (`REQ-PROD-039`,
  `REQ-DOM-115/226`).
- Structured logs: what operational events the product records, with a firm rule that credentials, session
  tokens, verified-contact values, and other private account data are never logged (`REQ-DOM-035`, privacy).
- Metrics that answer "is it serving users": request and error rates, latency, and a saturation/availability
  signal, sufficient to detect that the product is degraded (feeding `REQ-PROD-040`).
- An operator/admin audit trail: that supported administrative actions (`REQ-PROD-028`) are recorded so an
  operator can see who did what.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, partition, identities |
| Contract | `../contracts/` (read-only) | `REQ-OPS-*` scheme, your number range, verification vocabulary |
| Product requirements | `../../SUBTASK_product_requirements/outputs/product-requirements.md` | `REQ-PROD-039/040/028`, operator journey J9 |
| Domain & app design | `../../SUBTASK_domain_app_design/outputs/domain-application-design.md` | Readiness/store seam `REQ-DOM-115/226`; no-public-private-data `REQ-DOM-035` |
| Board follow-up | issue #23 (native install path hardening) | Reference where operational visibility is implied; defer placement to synthesis |

## Methodology
Bundle IDs (Domain Mapping): **Release Readiness** (primary); **Release Definition**, **Identity and Trust**
(supporting). The `design` loader is unavailable in this environment; apply the product-design persona and
this relayed guidance, and record the unavailability rather than blocking.

## Output
- `outputs/observability.md` — the `observability` section prose plus the full `REQ-OPS-060..079`
  requirements, each with `statement`, testable `acceptance_criteria`, `verification_method`,
  `release_gating`, and `traces_to`. Repository-ready content.

## Success criteria
- [ ] Composes against `../contracts/`; uses only `REQ-OPS-060..079`; does not redefine the schema.
- [ ] A trustworthy readiness signal, structured logs with a no-secrets/no-PII rule, serving-health metrics,
      and an operator-action audit trail are each testable requirements.
- [ ] Each requirement traces to `REQ-PROD-039/040/028` / the relevant `REQ-DOM-*` where one applies.
- [ ] Any substance of #23 relevant to observability is referenced for the synthesis fold, not duplicated.

## Constraints
- Requirements only — defer the logging stack, metrics backend, and dashboards to code DAGs.
- Repository-ready hygiene — no host/cluster/taskflow detail; describe signals by product/repository
  identity (endpoint by role, not by address); no attribution trailers.
