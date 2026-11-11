# COMPLETE — SUBTASK_ac67_retention_failclosed

**Task**: Judge whether PR #113 @ `09fa453` makes acceptance criterion #67 hold — retention/capacity
commitments and fail-closed-on-non-durable-write — for behavioral correctness.

**Output produced**: `SUBTASK_ac67_retention_failclosed/outputs/findings.md`, conforming to
`../../contracts/finding_schema.md`, finding ids `COR-40 .. COR-44` (within the assigned
`COR-40 .. COR-59` range).

## What was done

Reviewed PR #113 read-only at the pinned commit via `gh`/`gh api` (no checkout present; no repo or
GitHub writes). Traced issue #67's three code-facing clauses:

- **REQ-OPS-009 (no auto-expiry of user content)** — schema, both migrations (no destructive ops),
  account-deletion cascade, deploy manifests (no TTL/eviction/pg_cron), and the written commitment.
- **REQ-OPS-010 (enforced transient lifetimes)** — `sessions`/`recovery_tokens`/`export_artifacts`
  expiry columns + indexes, read-time enforcement, the Rust sweep, and the scheduled CronJob.
- **REQ-OPS-012 (capacity fail-safe + fail-closed write)** — the whole write surface through
  `with_transaction`, the capacity classifiers, the `error.rs` wire mapping, capacity provisioning,
  and the fail-safe / SQLSTATE tests.

The durability *drill* proof-depth (REQ-OPS-013; restart/redeploy/reschedule; whether DB-gated tests
actually run in CI) was left to the root `SUBTASK_durability_proof` and recorded as overlap (COR-44),
not expanded. Seam-shape / wire-contract questions touched by COR-43 were left to
`SUBTASK_architecture_contract`.

## Area sub-verdict

**NON-BLOCKING-ONLY.** The #67 behavior in this area is delivered correctly: user content has no
expiry path (documented), transient lifetimes are enforced at read time with a scheduled reclaim, and
non-durable writes fail closed across the whole write surface. Findings: COR-40 (major, non-blocking —
deployed CronJob SQL diverges from the tested Rust sweep; server never invokes the sweep), COR-41
(minor — `sessions.expires_at` nullable, lifetime enforced by convention not schema), COR-42/COR-43
(nits — capacity-classification and 500-vs-503 categorization, no fail-closed impact), COR-44 (minor,
suspected — fail-closed/sweep tests skip without a test DB; proof-depth owned by durability_proof).
None blocks landing from this area.

## Constraints honored

Read-only on repo and GitHub; no host/cluster/SSH/credential details or DAG internals in the findings;
every finding pinned to `09fa453` or marked whole-PR/design-level with rationale; severity honest
(`blocker ⟺ blocks_landing`); plain-voice finishing pass run.
