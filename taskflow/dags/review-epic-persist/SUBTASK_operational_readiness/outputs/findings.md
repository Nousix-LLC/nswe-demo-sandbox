# Findings — Operational readiness — PR #113 @ 09fa453

Question this concern answers: would the provisioned store be **safe and available in the running
system**, traced against `design/operational-readiness.md` (the `REQ-OPS-*` register) and ADR-0001?
Scope is the deployment surface the PR adds: `deploy/chirp/` manifests, probes, the reclaim CronJob,
the AppProject extension, and the image/credential wiring — read against the retention/capacity doc,
the durability drill, and the server-side sweep code the manifests invoke.

## What I checked

- **Provisioning shape** — `deploy/chirp/40-postgres-statefulset.yaml` (single-primary StatefulSet,
  `volumeClaimTemplates` per-ordinal PVC, `persistentVolumeClaimRetentionPolicy`, storage request,
  access mode, StorageClass selection) and `deploy/chirp/45-postgres-service.yaml` (headless
  Service, `clusterIP: None`, selector scoping), traced to REQ-OPS-001 (pod-independent storage),
  REQ-OPS-004 (reschedule), REQ-OPS-005 (single-writer), REQ-OPS-012 (capacity/fail-safe).
- **Restricted-PSA posture of the DB pod** — nonroot uid/gid 70, `fsGroup`, dropped capabilities,
  seccomp, and the deliberate non-use of `readOnlyRootFilesystem` on the Postgres container.
- **Readiness gating** — `deploy/chirp/10-deployment.yaml` probe wiring: readiness on `/readyz`
  (store health), liveness/startup on `/healthz`; and that the server's `/readyz` gates on
  `store_health`, traced to REQ-DOM-021's operational face.
- **Reclaim CronJob** — `deploy/chirp/50-transient-sweep-cronjob.yaml` schedule, `concurrencyPolicy`,
  deadlines, history/TTL limits, retry behaviour, and the three `DELETE` statements — compared
  line-for-line against the schema (`crates/chirp-server/migrations/0002_domain_schema.sql`) and the
  repository method it mirrors (`ChirpRepository::sweep_expired_transient_state`,
  `crates/chirp-server/src/repository/postgres.rs`). Traced to REQ-OPS-010.
- **Capacity commitments** — `deploy/chirp/retention-capacity.md` (growth assumption, 2Gi headroom,
  expansion caveat, exhaustion-fails-safe path) against REQ-OPS-009/010/012.
- **Image/credential activation** — the placeholder digest in `10-deployment.yaml`, the rollout
  strategy, the out-of-band credential model (`deploy/chirp/README.md`), the AppProject allow-list
  (`deploy/argocd/appproject.yaml`), the CI `image` job (`.github/workflows/ci.yml`), and how the
  durability drill (`deploy/chirp/drill/durability-drill.sh`) treats the placeholder — against the
  PR body's "what remains" framing and the open-issue posture of #64.
- Live cluster state was in scope read-only but not exercised: the PR's own position is that the
  durable workload does not go live until merge plus the digest follow-up, so the committed manifests
  and the drill are the authoritative surface for this judgment; a live read at the pre-merge state
  would add nothing to it.

## What I found clean

- **The pod-independence shape is correct.** A single-primary StatefulSet with a per-ordinal PVC from
  `volumeClaimTemplates`, fronted by a headless Service, is the right construction for durable state
  whose lifecycle is decoupled from any `chirp-server` pod (REQ-OPS-001). Domain state lives on the
  PVC, not pod memory or an `emptyDir`.
- **PVC retention is set explicitly, not left to default.**
  `persistentVolumeClaimRetentionPolicy: whenDeleted: Retain / whenScaled: Retain`
  (`40-postgres-statefulset.yaml:43-45`) means neither a scale-down nor a StatefulSet deletion drops
  the data volume. Making the retention choice explicit rather than relying on an unstated default is
  the right call for a volume that holds the product.
- **Single-writer posture is documented as a store property.** `replicas: 1` on the StatefulSet is
  tied to ADR-0001 §2 and the README/retention doc as a deliberate, documented limitation (one
  writable primary, no HA this release; consistency preserved, availability bounded). That satisfies
  the "single writer enforced and documented" arm of REQ-OPS-005 rather than leaving an undocumented
  single replica.
- **Readiness genuinely gates traffic on store health.** Readiness probes `/readyz`
  (`10-deployment.yaml:107-109`) while liveness/startup probe `/healthz` (`:93-102`). Because the
  Service adds only Ready pods to its endpoints, a server whose store is unreachable is kept out of
  rotation instead of serving 5xx. The split between "process up" (`/healthz`) and "store healthy"
  (`/readyz`) is the correct operational reading of REQ-DOM-021, and the drill asserts it
  (`durability-drill.sh:196`: readiness gates on `/readyz` = `store_health`).
- **The reclaim CronJob's SQL matches the code and the schema.** The three deletes
  (`50-transient-sweep-cronjob.yaml:88-92`) are semantically identical to
  `sweep_expired_transient_state` (`postgres.rs`): `sessions` carries the `expires_at IS NOT NULL`
  guard that the nullable column requires; `recovery_tokens` and `export_artifacts` (both
  `NOT NULL`) use the bare `expires_at <= now` predicate. All three columns and their supporting
  indexes exist in migration 0002. Under `--single-transaction`, `now()` is fixed once at
  transaction start, matching the method's single `now` cutoff. User-content tables are not touched,
  so life-of-account retention (REQ-OPS-009) is upheld.
- **CronJob hygiene is sound.** `concurrencyPolicy: Forbid`, `activeDeadlineSeconds`, bounded
  `backoffLimit`, `ttlSecondsAfterFinished`, and history limits mean runs do not overlap, a hung run
  is bounded, and finished Jobs do not accumulate.
- **Capacity fails safe, and that is tested.** A write that cannot be durably committed maps to an
  error reported as a failed action, not a false confirmation, per the documented
  `with_transaction` / `classify_write_error` path and the `confirmed_write_durable` /
  `capacity_fail_safe_never_false_confirms` tests (retention-capacity.md). 2Gi with a stated
  growth assumption is adequate headroom for the demo corpus (REQ-OPS-012).
- **The placeholder digest fails closed.** An all-zeros `sha256` cannot resolve to any image, so a
  premature rollout cannot silently pull and serve the wrong binary. Choosing an unpullable digest
  over a movable tag is the safe direction.

## Findings

### OPS-01 — Node-local default storage leaves cross-node reschedule unmet on the target
- **severity**: major
- **blocks_landing**: false
- **location**: `deploy/chirp/40-postgres-statefulset.yaml:150-168` @ 09fa453 (`storageClassName`
  omitted → cluster default; `accessModes: ["ReadWriteOnce"]`); design-level trace to ADR-0001 §2
- **acceptance-criterion / design ref**: REQ-OPS-004 (survive reschedule to another node,
  release_gating: true); ADR-0001 §2; #64
- **principle**: a release-gating durability requirement that the implementation does not fully
  deliver must be visible as unmet, not treated as satisfied by the StatefulSet shape alone.
- **why it matters here**: on the k3d target the default StorageClass is `local-path`, whose PV is
  bound to the node that first provisioned it. The per-ordinal PVC therefore pins the Postgres pod
  to one node: a true reschedule onto a *different* node cannot re-bind the volume, so REQ-OPS-004's
  node-independent arm is not met on this target. The drill discloses this
  (`durability-drill.sh:159-178`: on the single-node demo a cross-node reschedule is "physically
  impossible" and only a same-node re-bind is demonstrated). This is why #64 remains open rather than
  a defect the PR hides — but a reader tracing REQ-OPS-004 should see it stated, because a same-node
  re-bind is a weaker guarantee than the requirement's wording.
- **confidence**: verified
- **what would satisfy me**: the limitation stays explicitly recorded against #64 (not presented as
  satisfied) — which ADR-0001, the retention doc, and the drill already do; and, to actually clear
  REQ-OPS-004, a networked/CSI StorageClass (or external managed PostgreSQL via `DATABASE_URL`) whose
  volume is not node-affine. No change is required to land this PR.

### OPS-02 — The reclaim CronJob re-implements the sweep's delete logic, creating a second source of truth
- **severity**: major
- **blocks_landing**: false
- **location**: `deploy/chirp/50-transient-sweep-cronjob.yaml:88-92` @ 09fa453 (hand-written SQL)
  vs `crates/chirp-server/src/repository/postgres.rs` `sweep_expired_transient_state` @ 09fa453
- **acceptance-criterion / design ref**: REQ-OPS-010 (time-bounded state has an enforced lifetime)
- **principle**: the set of transient tables and their expiry predicates should have one definition;
  a schedule that reclaims them should invoke that definition, not restate it.
- **why it matters here**: the CronJob copies the three `DELETE`s out of the Rust method into YAML.
  They agree today (verified line-for-line). The risk is drift on a future schema change: if a fourth
  kind of transient durable state with an `expires_at` is added, `sweep_expired_transient_state` would
  be updated and tested, while the CronJob's hard-coded three deletes would silently keep sweeping only
  the original three. The new table would then accumulate expired rows with no signal — a slow storage
  leak that read-time expiry hides (expired rows still resolve as absent). The PR chose the CronJob
  specifically to avoid a server-image rebuild, which is a reasonable constraint; the cost is this
  duplicated definition.
- **confidence**: verified
- **what would satisfy me**: either invoke the existing method rather than restating its SQL (e.g. a
  small server subcommand or endpoint the CronJob triggers, once the image-rebuild sequencing is
  resolved), or a tracked follow-up plus a test/check that fails if the schema grows a transient table
  the CronJob does not sweep, so the two cannot drift apart unnoticed.

### OPS-03 — A failing sweep is not observable
- **severity**: minor
- **blocks_landing**: false
- **location**: `deploy/chirp/50-transient-sweep-cronjob.yaml:43-51` @ 09fa453 (schedule,
  `startingDeadlineSeconds`, `backoffLimit`)
- **acceptance-criterion / design ref**: REQ-OPS-010; capacity-monitoring explicitly deferred to the
  observability area (`REQ-OPS-060..079`), per retention-capacity.md §Scope
- **principle**: a scheduled reclamation job whose repeated failure produces no signal can leave a
  slow resource leak running unnoticed.
- **why it matters here**: after `backoffLimit: 3` the Job fails; with the DB unreachable for longer
  than `startingDeadlineSeconds: 200` at the scheduled minute, the run is skipped entirely. Either way
  nothing surfaces the miss. The blast radius is bounded — read-time expiry keeps correctness, and 2Gi
  gives headroom — so this is not a safety or availability defect, and the design deliberately assigns
  alerting to observability. I record it so the gap is deliberate rather than assumed covered here.
- **confidence**: verified
- **what would satisfy me**: a note in the retention doc or #64/observability backlog that sweep
  success/freshness is owned by the observability area and not yet wired, so operators do not assume
  a failed sweep raises a signal in this release.

### OPS-04 — Activation is a manual, un-gated step, and the "visibly not-ready" framing overstates the post-merge state
- **severity**: major
- **blocks_landing**: false
- **location**: `deploy/chirp/10-deployment.yaml:66` @ 09fa453 (placeholder digest) with
  `:27-28` (`maxSurge: 1` / `maxUnavailable: 0`); PR #113 body, "What remains"
- **acceptance-criterion / design ref**: REQ-OPS-001..004 (durable state live in the running system);
  #64 (stays open); durable-persistence requirement
- **principle**: the described activation path should match what an operator would actually observe,
  and a required manual step with no guard should be called out as such.
- **why it matters here**: two points about the digest-pin follow-up framing.
  (1) The PR body says the placeholder makes a pre-merge rollout "visibly not-ready rather than
  silently serving the non-durable in-memory image." At the new pod / ArgoCD layer that holds — the
  new ReplicaSet pod cannot pull the all-zeros digest and shows `ImagePullBackOff`, and ArgoCD shows
  the app unhealthy. But `maxUnavailable: 0` means the rollout will not remove the previous pod until
  the new one is Ready, which it never becomes. So on merge the *previously-deployed, non-durable*
  revision keeps serving until a human pins the real digest. The system does keep serving the
  non-durable image in the interim; what is "visible" is the stalled rollout, not a stopped service.
  (2) The body names the digest pin as "the one follow-up needed," but activating the durable system
  also requires the out-of-band `chirp-db-credentials` Secret to exist (without it the pod wedges in
  `CreateContainerConfigError`). That prerequisite is documented in `deploy/chirp/README.md`, but a
  reader of the PR body alone would conclude a single step suffices. Neither point blocks landing —
  #64 is kept open precisely because the running system is not durable until merge plus the follow-up
  — but the review should state that durability is not live on merge, and that the pin is a manual
  step nothing in CI or ArgoCD enforces.
- **confidence**: verified
- **what would satisfy me**: the PR's "what remains" (or the merge note) states both prerequisites —
  pin the published digest *and* create the out-of-band credential Secret — before the durable
  workload serves; and, optionally, a check that fails if a placeholder digest reaches the deployable
  manifest on `main`, so a forgotten pin cannot sit behind a green merge. #64 staying open already
  carries the "not durable until activated" status correctly.

## Concern sub-verdict
- **NON-BLOCKING-ONLY**
- Nothing in the provisioning, readiness gating, reclaim job, or image wiring would make the store
  unsafe or unavailable *on the deployment target this PR ships for*: the store is pod-independent and
  single-writer-safe, readiness gates traffic on store health, the sweep reclaims exactly the
  transient tables it should, and capacity fails safe. The four findings are a disclosed gating-gap
  tied to #64 (cross-node reschedule, OPS-01), two maintainability/observability risks in the reclaim
  path (OPS-02, OPS-03), and a framing/activation accuracy point (OPS-04) — all consistent with #64
  remaining open and none claiming a durability guarantee this PR does not deliver.
