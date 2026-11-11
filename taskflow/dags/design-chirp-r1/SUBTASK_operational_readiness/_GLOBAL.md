# _GLOBAL.md — operational-readiness subtree hub (chirp design-chirp-r1)

## Project Context

**Status**: Active

This subtree designs **operational readiness for release** as the `REQ-OPS-*` requirement area of the
chirp product design. It states what must be true in production **beyond "it runs"** — durable data, a
backup and recovery path, limits and quotas, observability, and a status/incident posture — each as a
testable release requirement, to the bar of **a product that can be operated, not just started**. It
writes requirements and acceptance criteria, **not** operational implementation; every engineering "how"
(which backup tool, which metrics backend, which rate-limiter) is stated as a requirement and deferred to
later code work.

The parent task `SUBTASK_operational_readiness` owns `design/operational-readiness.md` and the `REQ-OPS-*`
area (see `../_GLOBAL.md` and `../contracts/`). It decomposed because its brief enumerates five distinct
operational concerns held to a testable bar; this hub and the `contracts/` beside it freeze the seam those
five share — one consolidated requirements document, one `REQ-OPS-NNN` number space partitioned per child,
and the coverage/traceability invariants the synthesis gate asserts — **before any child runs**.

### Objective

Produce `outputs/operational-readiness.md`: the operational-readiness section of the chirp design, with
the seven required sections named in `../contracts/design_artifact_map.yaml` and a consolidated `REQ-OPS-*`
register whose every requirement is testable, carries a release-gating flag, and traces to the product and
domain requirements it serves.

### Scope

**In Scope:**
- The five operational concerns, each carried to testable `REQ-OPS-*` requirements: durable data in
  production; backups and recovery; limits and quotas; observability; status and incident posture.
- Folding the existing non-release-gating follow-ups #23 / #24 / #25 into the section each belongs to,
  rather than duplicating them.
- A consolidated `REQ-OPS-*` register and an OPS traceability table, assembled and verified by the
  synthesis gate.

**Out of Scope:**
- Operational *implementation* — backup scripts, deployment manifests, dashboards, alert rules, running
  product code. Deferred to later code DAGs; stated here only as requirements with a testable bar.
- Any `REQ-DOM-*`, `REQ-ID-*`, `REQ-UX-*`, `REQ-PROD-*`, or `BAR-*` content — owned by the sibling design
  tasks. This subtree references those ids at the seam; it does not mint or restate them.
- Host, cluster, or taskflow detail in any repository-bound content (hygiene; see below).

### Success Criteria

- [ ] `outputs/operational-readiness.md` exists with all seven required sections from
      `../contracts/design_artifact_map.yaml`, in order.
- [ ] Each of the five concerns is stated as testable `REQ-OPS-*` requirements consistent with the domain
      persistence model (`REQ-DOM-100..118`).
- [ ] Every `REQ-OPS-*` carries a testable `acceptance_criteria`, a `verification_method` from the schema
      vocabulary, a `release_gating` flag, and `traces_to` a `REQ-PROD-*` / `REQ-DOM-*` where one applies.
- [ ] #23 / #24 / #25 are each placed in the section they belong to, folded and not duplicated.
- [ ] No `REQ-OPS-NNN` number is used by two children; the consolidated register is the verbatim union.

---

## Constraints and Requirements

### Process Constraints
- **Compose against `../contracts/` and this subtree's `contracts/`** — use the `REQ-OPS-*` scheme and the
  `verification_methods` vocabulary; do not redefine the id scheme or the file map. This subtree's contract
  **extends** the ancestor additively (it sub-partitions the OPS number space); it does not override it.
- **Requirements only** — defer every operational implementation to later code DAGs.
- **Build on, do not restate, the domain persistence model.** `durable_data` consumes `REQ-DOM-100..118`;
  reference those ids rather than re-deriving the persistence requirement.

### Hygiene (binding on everything that reaches the repository)
Every requirement, acceptance criterion, and narrative line that will land in `design/operational-readiness.md`
is written for the repository's readers and carries **no** host/cluster address, filesystem or taskflow path,
agent/DAG/run id, or attribution footer. Name things by repository and product identity (`owner/repo`,
repo-relative path, issue/PR number, commit SHA, product endpoint by role). Acceptance criteria describe
operations by product/repository identity, never by a specific host or cluster.

### Methodology posture (environment note)
The Phase-B `design` methodology loader is **unavailable in this environment** (the methodology surface
returns `agent_domain_unset`). Each child's brief names the design bundle ID(s) its concern maps to
(Release Readiness primary; Release Definition, Product Strategy, Identity and Trust supporting); a child
applies the persona's product-design judgment and that relayed guidance, and records the loader
unavailability rather than blocking on it.

---

## Input Specifications

| Source | Identity | Role |
|--------|----------|------|
| Subtree hub | `_GLOBAL.md` (this file) | Shared context, task tree, contract pointer |
| Ancestor contract | `../contracts/` (read-only) | `REQ-OPS-*` scheme, verification vocabulary, design-artifact map |
| This subtree's contract | `contracts/` (read-only for children) | OPS number-space partition, per-section ownership, identities |
| Domain & app design | `../SUBTASK_domain_app_design/outputs/domain-application-design.md` | Persistence model `REQ-DOM-100..118`; readiness/store seam `REQ-DOM-113..115`, `226`; backup/export `REQ-DOM-116/117` |
| Product requirements | `../SUBTASK_product_requirements/outputs/product-requirements.md` | Product-level operational needs `REQ-PROD-037..041`; operator journey J9 |
| Current board | issues #23, #24, #25 (non-release-gating hardening/polish follow-ups) | Fold into the section each belongs to; do not duplicate |

---

## Task Structure

### Overview

```
SUBTASK_operational_readiness/
├── _GLOBAL.md                          (this hub)
├── contracts/                          (READ-ONLY for children)
│   ├── _MANIFEST.yaml                  (kind, ownership, identities, derived artifacts)
│   └── reqs_ops_partition.yaml         (REQ-OPS number-space partition + per-section ownership)
├── SUBTASK_ops_durable_data/_BRIEF.md
├── SUBTASK_ops_backups_recovery/_BRIEF.md
├── SUBTASK_ops_limits_quotas/_BRIEF.md
├── SUBTASK_ops_observability/_BRIEF.md
├── SUBTASK_ops_status_incident/_BRIEF.md
├── SUBTASK_ops_synthesis/_BRIEF.md
└── outputs/operational-readiness.md    (the subtree deliverable — produced by the synthesis fold)
```

### Task Summary

This table is the machine-readable DAG for this subtree. Each `Task id` is the child's directory name;
`Depends on` lists only sibling task ids, comma-separated, or `none`.

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_ops_durable_data` | none | State the production durability posture for release as `REQ-OPS-*`, consuming the domain persistence model: authoritative state in a durable store distinct from the serving process, acknowledged writes survive, invariants hold across restart/redeploy/restore, data-retention posture (including deleted-account data). Owns `REQ-OPS-001..019`. | `outputs/durable-data.md` |
| `SUBTASK_ops_backups_recovery` | `SUBTASK_ops_durable_data` | State the backup and recovery path as `REQ-OPS-*`: backup cadence and retention, a recovery-point and recovery-time target, an exercised restore procedure, recovery from a bad deploy (rollback), and verification that backups restore a correct product. Owns `REQ-OPS-020..039`. | `outputs/backups-recovery.md` |
| `SUBTASK_ops_limits_quotas` | none | State the rate, size, and volume limits a public internet-facing product needs as `REQ-OPS-*`: request and write-rate limits, payload and page-size caps, and the overload/abuse first line — proportionate, testable, and deferring enforcement mechanics. Owns `REQ-OPS-040..059`. | `outputs/limits-quotas.md` |
| `SUBTASK_ops_observability` | none | State what must be visible to operate the product as `REQ-OPS-*`: the health-vs-readiness distinction (readiness reflects store reachability), structured logs with a no-secrets/no-PII rule, the metrics that answer "is it serving users," and an operator/admin audit trail. Owns `REQ-OPS-060..079`. | `outputs/observability.md` |
| `SUBTASK_ops_status_incident` | `SUBTASK_ops_observability` | State how operators and users learn when something is wrong as `REQ-OPS-*`: an incident-detection-and-response posture built on observability, a way to communicate outages and maintenance to users, and the user-facing degraded-state expectation. Owns `REQ-OPS-080..099`. | `outputs/status-incident.md` |
| `SUBTASK_ops_synthesis` | `SUBTASK_ops_durable_data`, `SUBTASK_ops_backups_recovery`, `SUBTASK_ops_limits_quotas`, `SUBTASK_ops_observability`, `SUBTASK_ops_status_incident` | **Verification gate + fold.** Assemble the five fragments into `outputs/operational-readiness.md` with all seven required sections; author the `existing_followups` section folding #23/#24/#25 where they belong; build the consolidated `REQ-OPS-*` register and the OPS traceability table; assert the contract identities with recorded evidence; write the fold record. | `outputs/operational-readiness.md`, `SYNTHESIS.md` |

### Dependency Graph (human-readable; the table above is authoritative)

```
durable_data ───────────────> backups_recovery ──┐
limits_quotas ────────────────────────────────────┤
observability ──> status_incident ────────────────┤
                                                   └─> ops_synthesis ─> (fold → operational-readiness.md)
```

---

## Contract

**Contract location**: `contracts/` (read-only for every child)
**Contract kind**: `yaml_schema` — extends the ancestor `../contracts/` additively; overrides nothing.

The children are parts of one operational-readiness design. They share a real seam: one consolidated
`operational-readiness.md`, one `REQ-OPS-NNN` number space, one verification vocabulary, and the
coverage/traceability invariants the gate asserts. `contracts/reqs_ops_partition.yaml` fixes that seam.

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| id & traceability schema | `../contracts/id_and_traceability_schema.yaml` | `REQ-OPS-NNN` format; `AREA=OPS → SUBTASK_operational_readiness`; the `verification_methods` vocabulary; the per-requirement fields (`statement`, `acceptance_criteria`, `release_gating`) |
| design artifact map | `../contracts/design_artifact_map.yaml` | `design/operational-readiness.md` owner and its seven required sections |

Children MUST compose against these and MUST NOT redefine them.

### Structural Declarations
- `contracts/reqs_ops_partition.yaml` — the per-child `REQ-OPS-*` number-space partition, the per-section
  ownership of the seven required sections, and the per-concern output-fragment paths.

### Ownership (one producer per artifact)

| Artifact | Owning task |
|----------|-------------|
| `outputs/durable-data.md` + `REQ-OPS-001..019` + section `durable_data` | `SUBTASK_ops_durable_data` |
| `outputs/backups-recovery.md` + `REQ-OPS-020..039` + section `backups_and_recovery` | `SUBTASK_ops_backups_recovery` |
| `outputs/limits-quotas.md` + `REQ-OPS-040..059` + section `limits_and_quotas` | `SUBTASK_ops_limits_quotas` |
| `outputs/observability.md` + `REQ-OPS-060..079` + section `observability` | `SUBTASK_ops_observability` |
| `outputs/status-incident.md` + `REQ-OPS-080..099` + section `status_and_incident` | `SUBTASK_ops_status_incident` |
| `outputs/operational-readiness.md`, section `existing_followups`, section `requirements_and_acceptance_criteria`, `SYNTHESIS.md` | `SUBTASK_ops_synthesis` |

### Identities (asserted by `SUBTASK_ops_synthesis` with recorded evidence; no silent plugs)
1. All seven required sections from `../contracts/design_artifact_map.yaml` are present in
   `operational-readiness.md`, in order.
2. Each of the five concerns is covered by its fragment's `REQ-OPS-*` requirements.
3. No `REQ-OPS-NNN` number is used by two children; the consolidated register is the verbatim union of the
   five fragments.
4. Every `REQ-OPS-*` names a `verification_method` from the vocabulary and carries a `release_gating` flag,
   and every release-gating `REQ-OPS-*` has a testable `acceptance_criteria`.
5. Every `REQ-OPS-*` that refines a product/domain requirement `traces_to` a real `REQ-PROD-*` / `REQ-DOM-*`.
6. #23, #24, and #25 each appear exactly once, folded into the section they belong to, recorded in
   `existing_followups`, and not duplicated as new requirements where an existing requirement already covers them.

### Derived Artifacts
- **OPS traceability table** (`REQ-OPS-* → REQ-PROD-*/REQ-DOM-*`, release_gating) — assembled and checked by
  `SUBTASK_ops_synthesis` from the five fragments' requirement lists.

### Thin-Seam Note
The seam is not thin: a shared document, a shared number space, a shared verification vocabulary, and
cross-concern references (backups → durable data; status/incident → observability) are a rich contract.
Children compose against `contracts/` and MUST NOT redefine the partition or the id scheme.
