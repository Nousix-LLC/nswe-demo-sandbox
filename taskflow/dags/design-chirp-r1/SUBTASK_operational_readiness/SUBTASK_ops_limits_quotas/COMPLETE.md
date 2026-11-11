# COMPLETE — SUBTASK_ops_limits_quotas

## What was done
Authored the `limits_and_quotas` section of the chirp operational-readiness design as the fragment
`outputs/limits-quotas.md`: section prose plus the `REQ-OPS-040..048` requirements (within the owned
`REQ-OPS-040..059` range), each with a `statement`, testable `acceptance_criteria`, a `verification_method`
from the contract vocabulary, a `release_gating` flag, and `traces_to`.

## Output produced
- `outputs/limits-quotas.md` — repository-ready. Covers the four aspects named in the brief:
  - **Rate / write-rate / volume limits** — REQ-OPS-040 (per-client request rate), REQ-OPS-041 (tighter
    write-rate on posting/following/liking), REQ-OPS-042 (sustained per-account created-volume bound).
  - **Payload and size caps at the edge** — REQ-OPS-043 (max request body size, consistent with the fixed
    content bounds `REQ-DOM-012`/`REQ-DOM-002`, referenced not restated), REQ-OPS-044 (page-size cap on all
    list reads, enforcing `REQ-DOM-027`/`REQ-DOM-218` operationally).
  - **Over-limit behaviour** — REQ-OPS-045 (reject/throttle the excess; tell the caller with a typed error
    category, consistent with `REQ-DOM-220`); REQ-OPS-046 (the unauthenticated surface is limited too);
    REQ-OPS-047 (aggregate-overload shedding, protecting `REQ-PROD-040`).
  - **Boundary with identity** — prose only; `REQ-ID-*` account-level abuse controls (and `REQ-PROD-025`/
    `REQ-PROD-028`) referenced, not owned. REQ-OPS-048 states the user-protecting guard (limits sit above
    ordinary use).

## How it composes with the subtree
- Composes against `../contracts/reqs_ops_partition.yaml` and the ancestor `../../contracts/`: uses only the
  assigned `REQ-OPS-040..059` range, the closed `verification_methods` vocabulary, and the per-requirement
  field set; redefines nothing.
- The synthesis gate (`SUBTASK_ops_synthesis`) will concatenate this fragment as the `limits_and_quotas`
  section and fold its `REQ-OPS-*` into the consolidated register and the OPS traceability table.

## Board follow-up #24 (referenced for the synthesis fold, not re-filed)
#24 (least-privilege delivery RBAC + supply-chain hardening) is an operational **access-control** matter —
privileged control-plane/delivery actors, distinct from the public client-facing limits owned here. The
fragment references it in the boundaries note and explicitly defers final placement across the
operational-readiness sections to the synthesis gate. It is not duplicated as a `REQ-OPS-04x` requirement.

## Honest scope cuts recorded
- **REQ-OPS-047** (aggregate-overload shedding) and **REQ-OPS-048** (limits above ordinary use) are marked
  `release_gating: false`. The gated floor is per-client/per-account limiting (040–046), which satisfies the
  `REQ-PROD-041` acceptance criterion; whole-service overload shedding and the "clears normal use" guard are
  strengthenings expected of a mature service but not minimum-release blockers. This cut is deliberate and
  recorded rather than hidden.
- Numeric thresholds, the limiting algorithm, the enforcement point, and client-identification basis are
  intentionally deferred to later code DAGs (requirements-only constraint); the fragment fixes behaviour, not
  numbers.

## Methodology note (environment)
The Phase-B `design` methodology loader is unavailable in this environment
(`engine_methodology_glob` → `agent_domain_unset`). Per the subtree hub and the brief, I applied the
product-design persona and the relayed bundle guidance (Release Readiness primary; Product Strategy,
Identity and Trust supporting) and record the unavailability here rather than blocking.

## Hygiene
Repository-ready: no host/cluster/taskflow detail; operations described by product/repository identity
(endpoints by role, issue by number); no attribution trailers.
