# Review — honesty / scope / operability lens (PR #20, infra-bootstrap #10)

**Lens:** `honesty_scope_ops` · **Owned concerns:** honest-blocker handling (k3d-vs-native), scope conformance, operability
**Subject:** PR #20 `Nousix-LLC/nswe-demo` `work/infra-bootstrap`→`main`, head `016bd44`, +912/-0 across 11 files under `deploy/bootstrap/` (OPEN, not merged).
**Posture:** review-only — read the working tree, the PR body, and the code DAG's `SYNTHESIS.md` as INPUT; performed an independent scope scan; made no repository modification.

---

## 1. Lens summary

Through this lens PR #20 is **honest, in-scope, and operable**, with no block- or major-severity defect. The k3d
substitution is a *genuine* k3s cluster (same pinned k3s version, real readiness proof) and is disclosed
transparently in three places with exact environment facts and remediation — it is an honest, documented caveat,
not a hidden weakening. The staged tree is strictly infra-only: an independent scan found zero app
`Dockerfile` / `kind: Deployment` / `kind: Application` artifacts; ArgoCD's own install workloads (the only
Kubernetes objects introduced, fetched at runtime from the pinned upstream manifest) are in scope. The unified
`deploy/bootstrap/README.md` is a real newcomer-grade runbook: clear two-track run order, a genuinely gating
per-track verification step, and thorough kubeconfig / ArgoCD access + credential-retrieval documentation. Three
non-blocking items are raised (one honest-blocker follow-up, one operability doc gap on the native path, one PR-body
nit). The honesty of AC1's "Ready" claim holds; AC2 and AC4 are well served by the documentation.

---

## 2. Concern-by-concern assessment

### Concern 6 — Honest-blocker handling (k3d-vs-native substitution)

**Disposition: findings raised (one minor follow-up, one nit); honesty itself is CLEAN; k3d judged a genuine k3s env.**

- **(a) Genuine k3s vs. weakening/substitution — GENUINE.** k3d runs real k3s inside Docker containers; this is
  Rancher's first-class tool for k3s-in-Docker (dev/CI/rootless), not a different or reduced distribution. The
  pinned version is identical across modes — native tag `v1.35.5+k3s1`, k3d node image
  `docker.io/rancher/k3s:v1.35.5-k3s1` (`cluster/install-k3s.sh:32-33`) — and `install-k3s.sh` header asserts
  "Both modes produce a genuine k3s cluster; `verify-cluster.sh` proves readiness identically for both"
  (`:17-18`). Readiness is a real gate, not a claim: `verify-cluster.sh` runs `kubectl wait
  --for=condition=Ready nodes --all` and a CoreDNS `Running` check, exiting non-zero on failure
  (`verify-cluster.sh:40-44,55-61`). Observed: `k3d-nswe-server-0` + `k3d-nswe-agent-0` Ready at `v1.35.5+k3s1`
  with CoreDNS / local-path-provisioner / metrics-server / traefik healthy (`cluster/README.md:54-57`).
  **Downstream #12/#13 targetability:** a k3d cluster runs arbitrary Deployments/Services and ArgoCD
  `Application`s exactly as native k3s does — it *is* k3s — so #13's app deploy and ArgoCD `Application` can
  legitimately target it, and #12 images load into it via a registry or `k3d image import`. The substitution does
  **not** misrepresent the #10 deliverable, whose scope is explicitly "stand up and *prove* the environment,"
  which a genuine, proven-Ready k3s cluster satisfies.
- **(b) Caveat honesty/completeness — HONEST and COMPLETE, not hidden, not overstated.** The blocker is disclosed
  in three independent places, each with exact environment facts, the exact failing command, and remediation:
  - PR body, dedicated section "Honest environment caveat (documented blocker, not a hidden failure)" — names the
    rootless-sandbox facts (uid 1001, no non-interactive sudo, `/usr/local/bin` + `/etc/systemd/system` not
    writable), states k3d was auto-selected (genuine k3s, proven Ready), and that the native path is carried
    unchanged for a privileged host.
  - `cluster/README.md:59-69` "Native production install — blocker on this build host + remediation" — exact env
    facts, exact failing command (`curl -sfL https://get.k3s.io | sh -`), and a 3-step native remediation.
  - unified `README.md:115-122` "Environment caveat (honest reporting)".
  Nothing is overstated: the readiness claim is backed by a real gating check, and the native path is described as
  *carried-but-for-a-privileged-host*, not as exercised here.
- **(c) Escalation / tracked follow-up — YES, recommended (non-blocking).** Two honest forward-dependencies are
  worth tracking: (i) the NATIVE systemd install path is shipped but **cannot be exercised** on the sandbox host,
  so it is an *unproven* code path in the deliverable; (ii) a durable #13 app deploy will need a persistent /
  privileged cluster that the sandbox k3d instance (ephemeral, local to the build host) does not provide. Neither
  blocks #10 (which proves the environment via genuine k3d); both are legitimate tracked-issue material. See HSO-1.

### Concern 7 — Scope conformance (infra-only)

**Disposition: CLEAN.**

Independent scope scan over the staged tree (`deploy/bootstrap/**`):
`find . -iname 'Dockerfile*'` → none; `grep -rniE 'kind:\s*(Application|Deployment|Service|StatefulSet|DaemonSet|
Ingress)|docker\s+build|dockerfile'` → **zero matches**; file inventory = 4 `.md`, 6 `.sh`, 1 `.txt` (no YAML
manifest, no Dockerfile). The only Kubernetes objects the PR introduces are ArgoCD's **own** install workloads,
and they are not even staged as manifests in the diff — `install-argocd.sh:41,62` applies the pinned *upstream*
`manifests/install.yaml` at tag `v3.5.4` at runtime via server-side apply. Every script/README states the #12/#13
boundary explicitly (`install-argocd.sh:6-8`, `gitops/README.md:8-11`, unified `README.md:10-12`,
`wasm/README.md:7-9`). No app `Application`, Deployment, Service, or Dockerfile is staged. The infra-only boundary
is held. This matches — and independently re-confirms — the code DAG's I6 scope result.

### Concern 8 — Operability (newcomer-follows-the-runbook)

**Disposition: STRONG; one minor documentation gap on the native path (HSO-2).**

- **Run order:** unified `README.md:53-79` gives two tracks — cluster→gitops (strictly ordered, "REQUIRED before
  step 2" called out) and an independent wasm track — with copy-pasteable, repo-root-relative commands. Clear.
- **Per-track verification is a real gate, not a claim:** `README.md:83-96` maps each track to a gating proof.
  Confirmed in the scripts: `verify-cluster.sh` and `verify-argocd.sh` both run real `kubectl wait` / `rollout
  status` checks and exit non-zero on any failure (`verify-argocd.sh:28,41-50,56-58`); the wasm build self-asserts
  the artifact + wasm magic header (`wasm/README.md:44-51`). No step is assumed green.
- **kubeconfig / ArgoCD access docs:** thorough. Unified `README.md:99-112` (kubeconfig retrieval for both modes;
  ArgoCD port-forward to `https://localhost:8080`; admin-credential retrieval + rotate/delete), expanded in
  `gitops/README.md:58-100` and `cluster/README.md:29-49`. Satisfies AC2.
- **Logging to stdout:** scripts log operator-visible progress via `log()` (stderr) + `echo` (stdout); readable
  during a run.
- **Minor gap (HSO-2):** the unified run-order block's verify step (`README.md:63`
  `deploy/bootstrap/cluster/verify-cluster.sh`) does not note that **NATIVE** mode needs `KUBE_CONTEXT=default`
  (+ `KUBECONFIG=/etc/rancher/k3s/k3s.yaml`); `verify-cluster.sh:23` defaults `KUBE_CONTEXT=k3d-nswe`. A newcomer on
  the native path following only the unified runbook would hit a confusing context failure. The proven k3d default
  works out of the box, and `cluster/README.md:69` does document the native invocation — so this is minor.

---

## 3. Findings (schema per `contracts/finding_schema.md`)

- [HSO-1] severity=minor concern=honest_blocker_k3d_substitution lens=honesty_scope_ops
  location=`cluster/install-k3s.sh:59-67` (native path) + `cluster/README.md:59-69`
  acceptance_criteria_touched=[AC1_cluster]
  statement: The NATIVE systemd install path is shipped but is **unproven** — it cannot be exercised on the
  rootless sandbox build host — and a durable #13 app deploy will require a persistent/privileged cluster the
  sandbox-hosted k3d instance does not provide. This is an honest forward-dependency, not a defect in the landed
  artifact.
  evidence: `install-k3s.sh` carries `install_native()` unchanged; `cluster/README.md:59-69` records that the
  native install "cannot run here" (uid 1001 / no non-interactive sudo / protected paths); the proven cluster is
  k3d (`cluster/README.md:54-57`). #10 is satisfied by the genuine k3d cluster; #13 durability is out of this PR.
  remediation: Open a tracked follow-up issue to (a) exercise/verify the native systemd install on a privileged
  host before relying on it, and (b) provision a durable target cluster (native k3s on a privileged host or a
  managed cluster) ahead of the #13 app deploy. Non-blocking for #10.

- [HSO-2] severity=minor concern=operability lens=honesty_scope_ops
  location=`deploy/bootstrap/README.md:57-70` (Track 1 run-order block) vs. `cluster/verify-cluster.sh:23`
  acceptance_criteria_touched=[AC4_runbook]
  statement: The unified runbook's verify step does not tell a native-mode operator to set `KUBE_CONTEXT=default`
  (+ `KUBECONFIG`), while `verify-cluster.sh` defaults the context to `k3d-nswe`; a newcomer on the native path
  using only the unified README would get a confusing "API not reachable via context 'k3d-nswe'" failure.
  evidence: `README.md:63` invokes `verify-cluster.sh` with no env note; `verify-cluster.sh:23`
  `KUBE_CONTEXT="${KUBE_CONTEXT:-k3d-nswe}"`; the correct native invocation exists only in `cluster/README.md:69`.
  remediation: In the unified run-order block, add a one-line note for native mode (e.g. "NATIVE: prefix with
  `KUBE_CONTEXT=default KUBECONFIG=/etc/rancher/k3s/k3s.yaml`") or an explicit pointer to `cluster/README.md`
  step 3. Non-blocking.

- [HSO-3] severity=nit concern=honest_blocker_k3d_substitution lens=honesty_scope_ops
  location=PR #20 body, "What was installed & verified" table, Cluster row
  acceptance_criteria_touched=[AC1_cluster]
  statement: The PR-body verification table reports "k3s v1.35.5+k3s1 … 2 Ready nodes" without inline-annotating
  that this host ran **k3d mode**; full disclosure is in the caveat section immediately below, so the table is not
  misleading in context, but an inline "(k3d mode on this host)" tag would make the row self-contained.
  evidence: PR body Cluster row vs. the "Honest environment caveat" section lower in the same body; node names in
  `cluster/README.md:56` are `k3d-nswe-*`.
  remediation (optional): add "(k3d mode on this host)" to the table row. Nit — no action required to land.

**No block- or major-severity finding is raised by this lens.** The honesty of AC1's "Ready" claim is upheld (real
gating proof of a genuine k3s cluster, native/k3d difference fully disclosed); scope conformance is clean; the one
operability gap (HSO-2) is minor.

---

## 4. k3d-substitution verdict (contract identity R4)

**k3d-substitution verdict: acceptable** — k3d is a *genuine* k3s cluster (identical pinned k3s version across
modes; readiness proven by a real `kubectl wait`-based gate, not asserted), so downstream #12 image build and #13
deploy / ArgoCD `Application` can legitimately target a k3s cluster of this kind. The caveat is surfaced
**honestly and completely** in three places (PR body, unified `README.md`, `cluster/README.md`) with exact
environment facts, the exact failing native command, and remediation — not hidden, not overstated. The one residual
is an honest forward-dependency (native path unproven; #13 needs a durable/privileged cluster the sandbox cannot
host), which is **tracked-issue material, not a blocking weakening** (HSO-1). This is not a misrepresentation of the
deliverable: #10's mandate is to stand up and *prove* the environment, which the genuine proven-Ready k3d cluster
does.

## 5. F1 disposition recommendation (feeds gate R5)

**F1 recommendation: carry-as-tracked-issue** (non-blocking; additive contract-wording clarification) —
Rationale: the code DAG's F1 is a transparently-recorded ("recorded, not plugged") wording tension in that DAG's
**internal** `contracts/_MANIFEST.yaml` identity I1 — its literal enumeration clause expects all five #10 criteria
in the spoke RESULTs' `owns-criteria`, whereas `reproducible`+`honest` were deliberately carried as gate identities
I3/I5 per the decomposition's explicit design. The **substance holds** (every #10 criterion has coverage + a PASS
verdict somewhere in the gate output; none unowned, none double-owned), and F1 touches **none** of PR #20's
shippable artifacts (scripts/READMEs). Carrying it as a low-priority tracked issue (rather than dropping) preserves
the honest audit signal — a future code DAG reusing that contract template should reconcile the I1 wording with the
cross-cutting-criteria design — at essentially zero cost, consistent with the "recorded, not plugged" discipline the
code DAG already applied. Because F1 has **zero bearing on the landed artifact**, it MUST NOT influence the
APPROVE/REQUEST-CHANGES verdict; the gate may reasonably downgrade to `drop` if it prefers not to track internal
review-artifact wording, but this lens recommends `carry-as-tracked-issue`.

---

## 6. Acceptance-criteria bearing (for the gate's R2)

| AC | This lens's bearing | Lens read |
|----|---------------------|-----------|
| AC1_cluster | HSO-1 (minor, follow-up), HSO-3 (nit) | "Ready" claim is **honest** — genuine k3s, real gating proof; native/k3d difference fully disclosed. No honesty defect. |
| AC2_gitops | — (clean) | ArgoCD API/UI access + admin-credential retrieval documented thoroughly (unified README §Access + `gitops/README.md`). Access-docs bar met. |
| AC3_wasm | — | Not materially in this lens (owned by correctness/repro); no honesty/scope/operability concern observed. |
| AC4_runbook | HSO-2 (minor) | Unified runbook gives run order + real per-track gating verification; one minor native-mode `KUBE_CONTEXT` doc gap. |

Scope conformance (concern 7) is cross-cutting (reinforces the infra-only boundary underlying all ACs); it maps to
no single AC — `acceptance_criteria_touched=[]` — and is recorded CLEAN with the scan evidence above.
