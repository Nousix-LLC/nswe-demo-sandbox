# Operational readiness

This is the operational-readiness section of the chirp design: what must be true in production **beyond "it
runs"**, stated as testable `REQ-OPS-*` requirements to the bar of **a product that can be operated, not just
started**. It states requirements and acceptance criteria, not operational implementation — every engineering
"how" (which backup tool, which metrics backend, which rate-limiter) is stated as a property the operated
product must have and deferred to later code work.

The section covers five operational concerns, each carried to testable requirements:

- **`durable_data`** — the production durability posture around chirp's persistence model: a running
  deployment loses no user data to restart, update, or redeploy; acknowledged writes survive; invariants hold
  across restart and restore; and a stated data-retention and deletion posture.
- **`backups_and_recovery`** — a backup and recovery path: cadence and retention, recovery-point and
  recovery-time objectives, a defined and exercised restore, recovery from a bad deploy, and proof that
  backups restore a correct product.
- **`limits_and_quotas`** — the rate, size, and volume limits a public internet-facing product needs so no
  single client can overwhelm the service or flood other users.
- **`observability`** — what the product must expose to be operated: the health-vs-readiness distinction,
  structured logs under a no-secrets/no-PII rule, serving metrics, and an operator audit trail.
- **`status_and_incident`** — how operators and users learn when something is wrong: incident detection and
  response built on the observability signals, status and maintenance communication to users, the degraded-
  state experience join, and a stated, measured availability commitment.

Two cross-cutting sections follow the five concerns: `existing_followups` folds the open board follow-ups
#23/#24/#25 into the concern each belongs to, and `requirements_and_acceptance_criteria` is the consolidated
`REQ-OPS-*` register with an operational-readiness traceability table. Each requirement carries a testable
acceptance criterion, a verification method, a release-gating flag, and — where it refines a product or domain
requirement — a trace to the `REQ-PROD-*` / `REQ-DOM-*` it serves. Requirements that refine the domain
persistence model build on it by reference (`REQ-DOM-100..118`) rather than restating it.

Entities are named by the domain model's canonical vocabulary (Account, Chirp, Follow, Like, Session,
Credential, Verified contact). The product and its in-memory backing are named by repository identity —
`Nousix-LLC/nswe-demo @ c805525`, the `ChirpRepository` seam in the `chirp-server` crate.
