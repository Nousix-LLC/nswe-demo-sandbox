# Findings — Architecture / contract stability — PR #113 @ 09fa453

Concern: does the change keep the `ChirpRepository` seam's contract and the public/operational
surface stable and coherent, and are the additive deployment changes correct and minimal?
All locations pin to `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`.

## What I checked

- **The `ChirpRepository` seam** — `crates/chirp-server/src/repository/mod.rs`: the full trait
  method set, object-safety (`#[async_trait]`, held as `Arc<dyn ChirpRepository>`, every method
  `&self`), and the release-bar additions (`set_credential`/`verify_credential`,
  `invalidate_session`, `begin`/`complete_account_recovery`, `update_profile`, `delete_account`,
  `export_user_data`, `list_followers`/`list_following`, `remove_chirp`, `set_account_suspension`,
  `store_health`, `sweep_expired_transient_state`). Mapped the trait's capability set against
  issue #66's required capability list and REQ-DOM-014/018.
- **Second implementor, no fork** — `crates/chirp-server/src/repository/postgres.rs`:
  `impl ChirpRepository for PostgresRepository` (L185), the `connect()` startup path that runs the
  embedded `sqlx` migrator (L80–90), schema versioning via `_sqlx_migrations` / `schema_version`,
  and the `store_health` / `sweep_expired_transient_state` bodies. Confirmed `in_memory` remains the
  default implementor (`lib.rs` re-exports) with contract-consistent placeholders for the additions.
- **Wiring / composition root** — `lib.rs`, `main.rs`: config-driven backend selection, the
  `Arc<dyn ChirpRepository>` state shape identical for both backings, migrations applied on connect,
  and the fail-loud warning when a DB URL is set but the `postgres` feature is not compiled in.
- **Public HTTP surface** — `crates/chirp-server/src/api/router.rs`: the mounted route set, and
  whether the release-bar capabilities are exposed under `/api/…`.
- **Error surface** — `crates/chirp-server/src/error.rs`: the added `Unavailable` variant and the
  variant ↔ `ErrorCode` ↔ HTTP-status table.
- **Deployment contract** — `deploy/argocd/appproject.yaml`, `deploy/argocd/application.yaml`,
  `deploy/chirp/10-deployment.yaml`, `deploy/chirp/40-postgres-statefulset.yaml`,
  `deploy/chirp/45-postgres-service.yaml`, `deploy/chirp/50-transient-sweep-cronjob.yaml`: the
  additive AppProject whitelist, the Application→project binding, probes moving to `/readyz`, the
  StatefulSet single-writer posture + PVC retention, the headless Service, and the sweep CronJob.
- **Trace to design of record** — `design/operational-readiness.md` (REQ-OPS-001..005, 009..013)
  and the REQ-DOM-014/021/022 baseline it references.
- **Referenced sibling paths** — checked the committed tree at the pinned commit for every path the
  manifests' comments cite.

## What I found clean

- **The seam stays stable: additive, object-safe, not forked.** The core methods are unchanged; the
  release-bar capabilities are new `async fn`s on the same trait, returning the same `ServerError`
  contract, so object-safety and the `Arc<dyn ChirpRepository>` transport state are preserved. The
  durable backend is a *second implementor* of the one trait (`postgres.rs` L185), not a parallel or
  widened interface, and the in-memory backing remains available — the store plugs into the seam
  rather than around it.
- **Capability set complete at the contract level.** Every capability issue #66 enumerates maps to a
  trait method; nothing in the required set is missing from the seam.
- **Public HTTP surface stayed stable.** The only added route is `GET /readyz` (additive); no
  existing route changed. The error contract is frozen — `Unavailable` reuses the `INTERNAL`/500
  wire cell and introduces no new `ErrorCode` or HTTP status, and the enum is `#[non_exhaustive]`.
- **Readiness correctly gates on store health.** `/readyz` invokes `store_health` and maps
  `Ok`→200 / `Err`→503, distinct from the API error seam's 500, without leaking error detail; the
  mapping is backing-agnostic. This satisfies REQ-DOM-021's store-reachability health signal.
- **AppProject additions are additive and minimal.** `StatefulSet`, `PersistentVolumeClaim`, and
  `CronJob` are added to the namespaced allow-list by explicit kind; the existing kinds are
  untouched, there is no `*/*` wildcard, and `Secret` is deliberately excluded. Each added kind is
  actually used by a shipped manifest.
- **Single-writer posture is correct and documented.** The StatefulSet is `replicas: 1` with a
  per-ordinal `volumeClaimTemplates` PVC, `ReadWriteOnce`, and an explicit `Retain`/`Retain`
  reclaim policy; the headless Service gives stable DNS. This is the REQ-OPS-005 "one replica,
  documented as a store limitation" path.
- **Schema is versioned with a forward migration path at the contract level.** The migrator runs at
  the composition root on connect and the applied version is inspectable (REQ-DOM-022).

## Findings

### ARC-01  — Scheduled sweep bypasses the `ChirpRepository` seam and duplicates it as raw SQL
- **severity**: major
- **blocks_landing**: false
- **location**: `deploy/chirp/50-transient-sweep-cronjob.yaml` (the three `DELETE` args) @ 09fa453,
  against `crates/chirp-server/src/repository/postgres.rs:1618-1659` @ 09fa453
- **acceptance-criterion / design ref**: REQ-DOM-014 (all durable state crosses the one seam); #67 / REQ-OPS-010
- **principle**: one durable-state operation should have one source of truth; the seam is that source.
- **why it matters here**: `sweep_expired_transient_state` is a trait method with a durable
  implementation, but the operational sweep does not call it — the CronJob re-expresses the three
  `DELETE`s as raw `psql` statements in a manifest and mutates durable state outside the seam. The
  SQL matches the Rust method today (same predicates, the `IS NOT NULL` guard on `sessions` only,
  one transaction), so this is a drift risk rather than a current divergence: a future change to the
  sweep's predicates, the `expires_at` representation, or the transient table set must be made in two
  places that no test ties together, and the manifest copy can silently fall out of step with the
  schema. It also sits in tension with REQ-DOM-014's "all durable state crosses the one seam."
- **confidence**: verified
- **what would satisfy me**: either invoke the seam method from the scheduled job (e.g. a
  `chirp-server sweep` subcommand the CronJob runs against the already-pinned image), or, if the raw
  SQL path is kept deliberately, add a test/assertion that pins the CronJob's DELETE predicates to
  the seam method's so drift is caught, and note in the manifest that REQ-DOM-014 is consciously
  scoped to exclude this ops job.

### ARC-02  — Release-bar capabilities live on the seam but are not on the public `/api/…` surface
- **severity**: major
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/api/router.rs` (mounted route set) @ 09fa453; seam at
  `crates/chirp-server/src/repository/mod.rs` @ 09fa453
- **acceptance-criterion / design ref**: #66 (seam capabilities "each mapped to the existing `/api/…` surface")
- **principle**: the public surface and the stated acceptance criterion should agree.
- **why it matters here**: the router mounts no `/api` routes for the release-bar capabilities
  (`set_credential`, `delete_account`, `export_user_data`, `list_followers`/`list_following`,
  `remove_chirp`, `set_account_suspension`, recovery, etc.), and the in-memory default returns
  placeholders for them. Issue #66's second acceptance criterion says each capability is "mapped to
  the existing `/api/…` surface." Two readings are possible: (a) the capabilities must be reachable
  over `/api` in this PR, or (b) the criterion means they are expressed in the `chirp-types`
  surface at the seam, with HTTP wiring staged — which matches the PR's own framing that #64 stays
  open because the running system becomes durable only after merge plus follow-up. The seam contract
  (this concern's core judgment) is sound either way; what is unresolved is whether the acceptance
  criterion is met in this PR.
- **confidence**: suspected
- **what would satisfy me**: a confirmation from the correctness concern / #66 of which reading
  governs. If routes are required in this PR, that is a correctness-owned blocker (not re-filed
  here); if seam-level expression suffices with wiring deferred, say so explicitly so the gap is a
  recorded, intended stage rather than a silent omission.

### ARC-03  — Committed manifests cite sibling scaffolding paths that are not in the repo
- **severity**: major
- **blocks_landing**: false
- **location**: `deploy/argocd/appproject.yaml`, `deploy/argocd/application.yaml`,
  `deploy/chirp/40-postgres-statefulset.yaml`, `deploy/chirp/45-postgres-service.yaml`,
  `deploy/chirp/50-transient-sweep-cronjob.yaml` (header comments) @ 09fa453
- **acceptance-criterion / design ref**: n/a (deployment-contract coherence)
- **principle**: a shipped file's references should resolve, and build-process scaffolding should not
  leak into repo-reader-facing artifacts.
- **why it matters here**: the manifests' comments say they are "composed against"
  `../contracts/deploy_contract.yaml` and `../../contracts/deploy_durability_contract.yaml`, and cite
  `../SUBTASK_discovery/outputs/ground_truth.md`, `outputs/provisioning_notes.md`, and
  `SUBTASK_store_provisioning` / `_MANIFEST.yaml`. None of those paths exist in the committed tree
  (verified against the tree at the pinned commit). A reader following them hits nothing, and the
  references expose the internal task/DAG process that produced the manifests inside files that ship
  to the repo. No runtime impact — these are comments — but they make the deployment contract read as
  anchored to artifacts that are not present.
- **confidence**: verified
- **what would satisfy me**: either commit the referenced contract artifacts (so the references
  resolve) or rewrite the comments to describe the invariant directly (single-primary, headless
  Service, out-of-band Secret, additive whitelist) without pointing at absent scaffolding files.

### ARC-04  — Deployment set is not apply-ready at this commit (placeholder image digest)
- **severity**: minor
- **blocks_landing**: false
- **location**: `deploy/chirp/10-deployment.yaml` (`image: …@sha256:0000…0000`) @ 09fa453
- **acceptance-criterion / design ref**: #64 (digest-pin follow-up)
- **principle**: a deployment manifest's coherence includes whether it can actually roll out.
- **why it matters here**: the chirp-server image is pinned to an all-zero placeholder digest, so a
  sync at this commit cannot pull a running image. This is documented and intentional — it keeps a
  pre-merge rollout visibly not-ready rather than silently serving the non-durable image, and the
  real digest is the post-merge follow-up that keeps #64 open. Flagging only so the digest-pin stays
  tracked and the manifest set is understood to be not-yet-deployable at this commit; this overlaps
  the operational-readiness and correctness (#64 framing) concerns and is not re-filed as backlog
  here.
- **confidence**: verified
- **what would satisfy me**: the #64 digest-pin follow-up remains explicitly tracked as the step that
  makes the deployment set applyable after merge.

### ARC-05  — Seam/contract self-description lags the durable backend it now has
- **severity**: nit
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/repository/mod.rs` (opening module doc),
  `crates/chirp-server/src/lib.rs` (layering diagram), `deploy/argocd/appproject.yaml` (CronJob
  comment) @ 09fa453
- **acceptance-criterion / design ref**: n/a (coherence)
- **principle**: a contract's prose should describe the contract as it now is.
- **why it matters here**: the `mod.rs` opening doc still frames a durable store as hypothetical ("a
  SQLite/`sqlx` backing could be added … explicitly optional") and names SQLite, while the actual
  backend is a PostgreSQL implementor that exists in-tree behind a feature; the `lib.rs` layering
  diagram shows only `InMemoryRepository` and "could adopt a real database later." Separately, the
  AppProject comment calls the CronJob kind "OPTIONAL … harmless if unused" though the PR ships a
  CronJob that uses it. Minor drift between the documented and the actual contract; broad doc quality
  is the code-quality concern's, noted here only where it describes the seam/deployment contract.
- **confidence**: verified
- **what would satisfy me**: update the seam/layering docs to describe the PostgreSQL backing as a
  present (feature-gated) second implementor, and drop the "optional/unused" hedge on the CronJob.

## Concern sub-verdict
- **NON-BLOCKING-ONLY**
- The `ChirpRepository` seam stays stable, object-safe, and complete at the contract level (a second
  implementor, not a fork); the public HTTP and error surfaces stayed stable; and the AppProject
  additions are additive, minimal, and single-writer-correct. The findings are maintainability and
  coherence issues plus one cross-concern acceptance-criterion question (ARC-02) owned by
  correctness — none blocks landing from this concern.
