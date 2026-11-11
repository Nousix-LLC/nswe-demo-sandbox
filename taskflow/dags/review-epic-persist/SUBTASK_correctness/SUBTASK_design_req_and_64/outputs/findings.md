# Findings — durable-persistence design requirement + applicable BAR-*/REQ- + #64 "stays open" — PR #113 @ 09fa453

Area: the design-of-record trace for the durable-persistence requirement and the `BAR-*` / `REQ-*` it rests
on, plus whether PR #113's claim that **#64 stays open** is an accurate account of what the change does and
does not make durable. Read-only; no GitHub writes; #64 is neither closed nor filed as backlog.

## What I checked

- **The requirement the change answers to.** `design/domain-application-design.md` §3 `persistence_requirement`
  — REQ-DOM-012 (all domain state persists across restart/redeploy/reschedule; the in-memory store is not an
  acceptable release backing), REQ-DOM-013 (state lives outside the pod's in-process memory and ephemeral
  filesystem), and REQ-DOM-014 (durable store plugs into the existing `ChirpRepository` seam as a second
  implementor).
- **The release bar item for #64.** `design/release-bar.md` §E — **BAR-019** ("All domain state is durable and
  survives restart, redeploy, and reschedule; a confirmed write is durable before it is confirmed; the
  in-memory store is replaced"), `verification_method: operational_check`, `stage: usable_early`. Its
  reference set: REQ-PROD-026, REQ-DOM-012, REQ-DOM-013, REQ-OPS-001, REQ-OPS-002, REQ-OPS-003, REQ-OPS-004,
  REQ-OPS-006, REQ-OPS-007.
- **The operational face of that bar.** `design/operational-readiness.md` §`durable_data` — REQ-OPS-001
  (pod-independent storage; verified by *inspection of the running deployment*), REQ-OPS-002/003/004
  (restart / redeploy / reschedule survival; operational_check), REQ-OPS-006 (confirmed write durable before
  confirmed; operational_check), REQ-OPS-007 (coverage of every kind of state; operational_check + inspection).
- **What #64 actually claims.** Issue #64 on `Nousix-LLC/nswe-demo` (BAR-019, `usable_early`, child of epic
  #56) and epic #56's scope split across BAR-019/020/021/022. #64's acceptance criteria are all phrased against
  the *running deployment* ("Inspecting the running deployment shows…", "Deleting a pod and letting it be
  recreated…preserves all user data").
- **What the PR claims and how it wires durability into the running system.** PR #113 description (the "What
  remains" section and the `Closes #65/#66/#67` + "#64 stays open" lines), and the change that activates the
  store in the live system: `deploy/chirp/10-deployment.yaml` @ 09fa453 (the image pin, the
  `CHIRP_DATABASE_URL` injection, the readiness-probe move to `/readyz`).
- **The closes/open split against the verification methods.** Cross-checked which issues the PR closes
  (#65 → BAR-020 automated_test; #66 → BAR-021 inspection; #67 → BAR-022 operational_check-via-drill) against
  which it leaves open (#64 → BAR-019 operational_check against the live deployment), to judge whether leaving
  #64 open while closing #67 is coherent.

## What I found clean

- **#64 is correctly left open, and the reasoning holds.** BAR-019 and its whole reference set are verified
  against the *running* deployment — REQ-OPS-001 by inspection of the running deployment, REQ-OPS-002/003/004/006
  and REQ-DOM-012 by operational_check. The change delivers the store, the seam wiring
  (`deploy/chirp/10-deployment.yaml:65-78` injects `CHIRP_DATABASE_URL` and the server selects the PostgreSQL
  backend when it is set), and the readiness gate (`/readyz`), but it does not and cannot make the *live*
  deployment durable on its own: delivery is GitOps (ArgoCD reconciles `main`), this change is unmerged, and
  even once merged the Deployment pins a placeholder image digest
  (`deploy/chirp/10-deployment.yaml:61` — `@sha256:0000…0000`) until the real durable digest from `main`'s CI
  is pinned as the follow-up. So BAR-019's operational check cannot pass yet. The PR's posture — close
  #65/#66/#67, keep #64 open — matches this exactly.
- **Closing #67 while keeping #64 open is coherent, not contradictory.** Both BAR-022 (#67) and BAR-019 (#64)
  carry `operational_check`, so "one closes, one stays open" invites suspicion. It holds up: BAR-022's bar is
  that "durability is **demonstrable** by a repeatable drill" (a capability, which the throwaway-namespace
  drill shows), whereas BAR-019's bar is that the **running deployment itself** is durable (REQ-OPS-001's
  "inspecting the running deployment"). The drill demonstrating survival in a throwaway namespace does not make
  the live workload durable, so the two can legitimately diverge. (BAR-022/#67's own adjudication belongs to
  `SUBTASK_ac67_retention_failclosed` and the drill-depth to the root `SUBTASK_durability_proof` — overlap
  recorded, not re-decided here.)
- **The placeholder-digest choice fails visible rather than failing silent.** Pinning
  `@sha256:0000…0000` with `imagePullPolicy: IfNotPresent` makes a pre-digest-pin rollout wedge in
  ImagePullBackOff rather than silently serving the old non-durable in-memory image. For a change whose entire
  point is durability, failing visibly on an un-activated store is the safer default, and the inline comment
  states the intent.
- **The in-memory fallback is consistent with the design.** The server falling back to the in-memory store
  when `CHIRP_DATABASE_URL` is unset does not contradict REQ-DOM-012's "in-memory store is not an acceptable
  release backing": the design keeps `InMemoryRepository` as the test/local backing
  (`domain-application-design.md` §2.1, "Default backing…is **not** the release backing"), and the live
  Deployment sets `CHIRP_DATABASE_URL`, so the production backing is PostgreSQL.

## Findings

### COR-60  — PR's "what remains / one follow-up" understates what activates durability in the running system
- **severity**: minor
- **blocks_landing**: false
- **location**: whole-PR — PR #113 description, "What remains" section; corroborated by
  `deploy/chirp/10-deployment.yaml:61,66-78` @ 09fa453
- **acceptance-criterion / design ref**: #64 / BAR-019 / durable-persistence requirement
- **principle**: a shipped account of "what is left" should name every precondition a reader must satisfy to
  reach the claimed end state, not just the most visible one.
- **why it matters here**: the description frames the digest-pin as "the one follow-up needed to activate the
  durable image on the cluster." Activating durability in the running system actually depends on a short
  sequence, not a single step: (a) the change merges so ArgoCD reconciles it onto `main`; (b) the out-of-band
  `chirp-db-credentials` Secret exists in the namespace, or the pod wedges in `CreateContainerConfigError`
  (the Deployment's `secretKeyRef` requires it — `10-deployment.yaml:72-78`); (c) the real durable digest is
  pinned, replacing the placeholder; and in between merge and the digest-pin the app tier is intentionally
  not-ready (ImagePullBackOff on the placeholder), i.e. a brief outage window. A reader who takes "one
  follow-up" literally during post-merge activation can be surprised by the Secret precondition and the
  not-ready window. This strengthens rather than weakens "#64 stays open" — it does not dispute the framing.
- **confidence**: verified — the Secret dependency and the placeholder digest are both in the diff at the cited
  lines; whether the Secret is already present in the namespace is live operational state I did not inspect and
  is not claimed here.
- **what would satisfy me**: reword "What remains" to state the activation sequence rather than a single step —
  merge (ArgoCD reconcile) → ensure the out-of-band `chirp-db-credentials` Secret is present → pin the real
  durable digest published by `main`'s CI — and note that the app tier is deliberately not-ready between merge
  and the digest-pin. No code change required.

## Overlaps recorded for synthesis (not re-adjudicated here)

- **Seam fidelity / migration (BAR-021, #66)** → `SUBTASK_ac66_seam_migration`. My clean finding that the store
  plugs in behind `ChirpRepository` as the production backing leans on #66's behavioral adjudication of the
  seam; I did not re-check capability coverage or the migration runner.
- **Invariants under concurrency (BAR-020, #65)** → `SUBTASK_ac65_invariants`. My acceptance that the delivered
  store is the right backing assumes #65's "proved, not asserted" adjudication of invariants/derived
  counts/opaque-id monotonicity.
- **Drill depth and BAR-022/#67** → `SUBTASK_ac67_retention_failclosed` + root `SUBTASK_durability_proof`. I use
  the BAR-022-vs-BAR-019 distinction (demonstrable-by-drill vs. live-durable) to confirm the closes/open split;
  the drill's proof-depth and #67's own verdict are theirs.
- **Digest-pin, readiness gating on `/readyz`, placeholder-digest outage window, Secret handling** → root
  `SUBTASK_operational_readiness` (activation/readiness) and `SUBTASK_architecture_contract` (manifest shape).
  COR-60 touches the same facts from the #64-framing angle; the operational and manifest-shape verdicts are
  theirs to render and de-duplicate.
- **Failing required `doc` CI check** → root `SUBTASK_ci_doc_diagnosis`. Out of my area; noted only as context
  that the PR is not clean to land regardless of this area's verdict.

## Concern sub-verdict

- **NON-BLOCKING-ONLY**
- The durable-persistence requirement (REQ-DOM-012/013/014), BAR-019, and its REQ-OPS reference set are traced,
  and the PR's "#64 stays open" framing is **accurate**: store, seam wiring, and drill are delivered, and the
  running system becomes durable only after merge plus the follow-up digest-pin, which is what BAR-019's
  operational check gates on. #64 is confirmed correctly open — not closed, not filed as backlog. The one
  finding (COR-60) is a minor accuracy refinement to the PR's "what remains" prose; it does not block landing
  and reinforces, rather than disputes, leaving #64 open.
