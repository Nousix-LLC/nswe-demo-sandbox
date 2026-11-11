# Task: Limits and quotas — operational requirements

## Task Specification
**Slug**: SUBTASK_ops_limits_quotas
**Task Kind**: standard
**Status**: Pending

### Objective
State, as testable `REQ-OPS-*` requirements, the **rate, size, and volume limits** a public,
internet-facing release of chirp needs so one actor cannot overwhelm the service or flood others — the
operational first line against overload and trivial abuse.

### Context
Part of the operational-readiness subtree (see `../_GLOBAL.md`, `../contracts/`). You own the
`limits_and_quotas` section of `design/operational-readiness.md`, written as the fragment
`outputs/limits-quotas.md`, and the `REQ-OPS-040..059` number range. The product requirement `REQ-PROD-041`
asks for basic rate and volume limits as a first line against abuse; your job is to make that concrete and
testable from the operator's and user's side. Note the existing follow-up **#24** (ArgoCD least-privilege
RBAC + supply-chain hardening) touches the operational access-control posture — consider whether any of its
substance belongs to a limits/access requirement here; the synthesis gate owns the final placement of #24,
so reference it rather than re-filing it.

**Dependencies**: none.
**Dependents**: `SUBTASK_ops_synthesis` consolidates your section.

### Distinct aspects to cover (evaluate scope; decompose further only if warranted)
- Request rate limits per client/account, and write-rate limits on the actions that create state
  (posting, following, liking), stated as limits the product enforces rather than specific numbers to hard-code.
- Payload and field-size limits at the edge (request body size), consistent with the already-fixed content
  bounds (chirp text `REQ-DOM-012`, handle `REQ-DOM-002`) and page-size caps (`REQ-DOM-218/027`) — reference
  those rather than duplicating them; add what the operational edge needs beyond them.
- The behavior when a limit is exceeded: the product rejects or throttles the excess rather than serving it
  without bound, and tells the caller (consistent with the typed error contract `REQ-DOM-220`).
- The abuse/overload boundary with identity: where limits end and the identity design's abuse controls
  (`REQ-ID-*`) begin — reference, do not own.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, partition, identities |
| Contract | `../contracts/` (read-only) | `REQ-OPS-*` scheme, your number range, verification vocabulary |
| Product requirements | `../../SUBTASK_product_requirements/outputs/product-requirements.md` | `REQ-PROD-041` and the public-product abuse posture |
| Domain & app design | `../../SUBTASK_domain_app_design/outputs/domain-application-design.md` | Content bounds `REQ-DOM-012/002`, page caps `REQ-DOM-218/027`, error contract `REQ-DOM-220` |
| Board follow-up | issue #24 (ArgoCD RBAC + supply-chain hardening) | Reference where an access/limits requirement is implied; defer final placement to synthesis |

## Methodology
Bundle IDs (Domain Mapping): **Release Readiness** (primary); **Product Strategy**, **Identity and Trust**
(supporting). The `design` loader is unavailable in this environment; apply the product-design persona and
this relayed guidance, and record the unavailability rather than blocking.

## Output
- `outputs/limits-quotas.md` — the `limits_and_quotas` section prose plus the full `REQ-OPS-040..059`
  requirements, each with `statement`, testable `acceptance_criteria`, `verification_method`,
  `release_gating`, and `traces_to`. Repository-ready content.

## Success criteria
- [ ] Composes against `../contracts/`; uses only `REQ-OPS-040..059`; does not redefine the schema.
- [ ] Rate limits, write-rate limits, payload/size caps, and the over-limit behavior are each testable
      requirements consistent with the existing content/page bounds and the error contract.
- [ ] Each requirement traces to `REQ-PROD-041` where one applies; the limits/abuse boundary with `REQ-ID-*`
      is referenced, not owned.
- [ ] Any substance of #24 relevant to limits/access is referenced for the synthesis fold, not duplicated.

## Constraints
- Requirements only — defer the rate-limiter, RBAC, and supply-chain mechanics to code DAGs.
- Repository-ready hygiene — no host/cluster/taskflow detail; describe operations by product/repository
  identity; no attribution trailers.
