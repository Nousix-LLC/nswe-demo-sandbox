# COMPLETE — SUBTASK_ac66_seam_migration

## Task
Judge whether PR #113 @ `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21` makes acceptance criterion **#66** hold —
full `ChirpRepository` capability set behind the seam, single-writer safety, and a versioned schema applied by
a migration runner — proved, not asserted. Read-only review of one area; one findings document.

## Output
- `SUBTASK_ac66_seam_migration/outputs/findings.md` — conforms to `../../contracts/finding_schema.md`;
  finding ids `COR-20 .. COR-23` (within the assigned `COR-20 .. COR-39` range).

## Result
Area sub-verdict: **NON-BLOCKING-ONLY**.

#66's three pillars all hold at the pinned commit:
- **Capability set** — all 24 `ChirpRepository` methods implemented in `PostgresRepository` with real durable
  bodies; no method stubbed, `todo!()`, or weakened; in-memory backing retained as the default second
  implementor; routing additive, transport unchanged.
- **Single-writer** — Postgres StatefulSet `replicas: 1`, one writable primary / one consistent dataset,
  documented as a store limitation (ADR-0001 §2); app tier state is external and safe to scale against it.
- **Migration / versioning** — `sqlx` forward-only embedded runner applied at `connect` before serving,
  ordered and idempotent, version-tracked and inspectable via `schema_version()`; no DDL applied outside the
  runner.

Findings (all `blocks_landing: false`):
- COR-20 (major) — stale "scaffold / stubs return Internal / bodies downstream" docs across the seam
  (`postgres.rs` module+impl+`store_health`, `Cargo.toml`) contradict the implemented bodies; flagged as a
  likely contributor to the failing required `doc` check (owned by `SUBTASK_ci_doc_diagnosis` + root verdict).
- COR-21 (minor) — `remove_chirp` advertises a `Forbidden` the store never returns (both backings ignore
  `actor`; authorization deferred upstream by design).
- COR-22 (minor) — single-writer rests on `replicas: 1` with no hard guard (scale-up would fork data); overlap
  with ops/architecture.
- COR-23 (minor) — credential stored and compared in plaintext; overlap with security.

Recorded overlaps left for root synthesis to de-duplicate: proof-in-CI of the feature-gated durable backend
(`SUBTASK_durability_proof`), seam contract-shape (`SUBTASK_architecture_contract`), denormalized-count
concurrency (`SUBTASK_ac65_invariants`).

## Constraints honored
Read-only; no repository or GitHub writes. No host/cluster/SSH/credential details or DAG internals in the
findings. Every finding pinned to `09fa453`. Plain-voice finishing pass run over the output.
