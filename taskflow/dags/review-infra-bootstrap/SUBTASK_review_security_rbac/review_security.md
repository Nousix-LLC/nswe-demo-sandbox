# review_security.md — PR #20 security / secrets / least-privilege lens

**Lens**: `security` · **Spoke**: `SUBTASK_review_security_rbac` · **Subject**: PR #20 (`Nousix-LLC/nswe-demo`,
`work/infra-bootstrap`→`main`, head `016bd44`, Closes #10) — `deploy/bootstrap/` (6 bash scripts + 4 READMEs +
`versions.txt`, +912/−0). **Mode**: review-only; no repo/branch/checkout modification performed.
**Owned concerns** (contract `ownership.concerns`): `security_secrets_posture`, `least_privilege_rbac_cluster_posture`.

---

## 1. Lens summary

Through the security/least-privilege lens this is a **strong, security-conscious deliverable** with no
block- or major-severity defect. Secrets posture is genuinely clean: an independent pattern scan over the staged
tree **and** the committed diff finds **zero** hard-value credentials; every `secret`/`password`/`token`/`kubeconfig`
occurrence is a prereq note, a "NO SECRETS" assertion, or a documented **runtime-retrieval** command (ArgoCD admin
password + kubeconfig fetched at runtime, never staged) — independently corroborating the code DAG's I2, not merely
citing it. The ArgoCD install isolates into a dedicated `argocd` namespace, exposes nothing externally by default
(stock ClusterIP), and ships the stock seven default NetworkPolicies; the `gitops/README.md` RBAC section is
exemplary — it discloses the single broadest grant verbatim and names the hardening levers rather than hiding them.

The findings are all **minor/nit hardening observations**, not defects in what was built: (a) the native-mode
k3s kubeconfig is written world-readable (`0644`); (b) the stock ArgoCD `application-controller` carries a
cluster-admin-equivalent (`*/*/*`) ClusterRole — inherent to stock upstream ArgoCD, transparently documented, and
appropriately deferred to the first-`Application` milestone (#13); (c) the two remote installers
(`curl … | sh` for k3s, `kubectl apply -f <raw.githubusercontent URL>` for ArgoCD) are HTTPS + **version-pinned**
but not digest-/checksum-pinned and are not signature-verified at install. Each is a defensible choice for a
stock-upstream control-plane bring-up; each is recorded below so the gate/overseer can track the hardening before
production exposure. **Net security read: APPROVE-worthy on this lens** — no open block, no open major.

---

## 2. Concern-by-concern assessment

### Concern 4 — Security & secrets posture → **CLEAN (3 minor/nit hardening notes)**

**No committed secret (independent corroboration of I2).** I ran my own secret scan rather than trusting the code
DAG's gate:

- Hard-value patterns — `BEGIN … PRIVATE KEY`, kubeconfig data blobs (`client-key-data` / `client-certificate-data`
  / `certificate-authority-data`), a full `apiVersion: v1 … kind: Config` kubeconfig, inline
  `password=`/`token=` literals, `bearer <token>`, `AKIA…` AWS keys, `eyJ…` JWTs — over the staged tree:
  **zero matches**.
- Same hard-value scan over the committed diff (`gh pr diff 20`): **zero matches**.
- Every `secret`/`password`/`token`/`kubeconfig`/`key` string that does appear is one of: a prerequisite note, an
  explicit "NO SECRETS" header assertion, or a **runtime retrieval** command — e.g.
  `kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d`
  (`gitops/README.md:86`) and `k3d kubeconfig merge nswe …` (`cluster/README.md:37`). These read credentials from
  the cluster at runtime into the operator's terminal; nothing is written into a repo file.

The ArgoCD admin-credential handling is better than merely "not committed": `gitops/README.md:89-96` instructs the
operator to **rotate the admin password and delete the bootstrap `argocd-initial-admin-secret`** after first login,
and to move to SSO via the bundled dex broker rather than sharing `admin` — a correct, least-standing-credential
posture. The no-secrets claim is therefore an **asserted, evidenced conclusion**, not silence.

**Secret-at-rest permission (minor — SEC-1).** `cluster/install-k3s.sh:65` invokes the native k3s installer with
`--write-kubeconfig-mode 0644`, making the cluster-admin kubeconfig at `/etc/rancher/k3s/k3s.yaml` readable by
**every local user** on the host. This is the one place the deliverable *loosens* a credential's at-rest posture.
It is native-mode-only (not the k3d path actually exercised on the sandbox), and both the script comment
(`:62` "adjust to taste") and `cluster/README.md:49` ("tighten for shared hosts") flag it — so it is a documented,
operator-overridable convenience, not a hidden weakening. Minor; see SEC-1 (rises toward major on a shared/
multi-tenant production host).

**Remote-installer provenance / pinning (minor — SEC-3).** Two "fetch-and-run" surfaces, both HTTPS and both
version-pinned, neither digest-/checksum-pinned nor signature-verified at install:
`curl -sfL https://get.k3s.io | … sh -s - server` with `INSTALL_K3S_VERSION=v1.35.5+k3s1`
(`cluster/install-k3s.sh:63-65`), and
`kubectl apply --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/v3.5.4/manifests/install.yaml`
(`gitops/install-argocd.sh:41,62`). Provenance is trustworthy (official k3s domain; the argoproj repo pinned to a
release **tag**) and these are the upstream-recommended install paths, so this is not an over-broad/opaque
fetch-and-run — but per the supply-chain discipline (bind trust to an immutable digest, not a mutable tag/ref;
verify at admission) the k3s install *script* is mutable, the ArgoCD manifest is pinned to a movable git **tag**
rather than a commit SHA, and the images it references are `quay.io/argoproj/argocd:v3.5.4` by **tag, not digest**,
with no cosign verification. Minor supply-chain hardening; see SEC-3. (This is a #13-era hardening, consistent with
the methodology's "start with signature+identity, add digest-pinning/verification as the program matures".)

### Concern 5 — Least-privilege RBAC / cluster posture → **CLEAN (1 minor + 1 nit)**

**Namespace isolation — good.** `install-argocd.sh:58-62` creates and installs strictly into a dedicated `argocd`
namespace (idempotent apply-of-dry-run namespace + `-n "${ARGOCD_NAMESPACE}"` on the manifest apply). Exposure is
closed-by-default: `gitops/README.md:59-77` keeps `argocd-server` as the stock **ClusterIP** (no NodePort, no LB,
no Ingress) reached only via port-forward, "intentionally not configured here, to keep the control plane closed by
default." The stock install also ships **seven default NetworkPolicies** (one per component) — sane out-of-the-box
pod-to-pod isolation. This matches the stated infra-only scope: only ArgoCD's own install workloads land, nothing
cluster-wide or surprising beyond stock ArgoCD.

**Broadest grant — stock `application-controller` ClusterRole is `*/*/*` (minor — SEC-2).** Per
`gitops/README.md:107-118`, the stock upstream ArgoCD install grants `argocd-application-controller` a
cluster-admin-equivalent ClusterRole (`*/*/*`), with `argocd-server` and `argocd-applicationset-controller` also
cluster-scoped, while the three namespace-only components (`repo-server` — the highest-risk templating component —
`redis`, `dex`, `notifications`) deliberately get **zero** cluster permissions. `install-argocd.sh` applies this
stock manifest **unmodified** — it adds no grant of its own. Against the RBAC least-privilege rubric a standing
`*/*/*` ClusterRole is the "cluster-admin as convenient default"/wildcard anti-pattern; here it is **mitigated to
minor** because (i) it is inherent to stock upstream ArgoCD (the script introduces nothing extra), (ii) at
control-plane bring-up there are **zero `Application`s**, so nothing is being reconciled cluster-wide yet,
(iii) it is isolated to the `argocd` namespace's own identity, and (iv) the README already treats it as a recorded
decision with named change-conditions (scope the ClusterRole to needed apiGroups/resources, constrain targets with
AppProjects, or adopt the upstream `namespace-install.yaml`), explicitly deferred to when the first `Application`
is introduced (#13). It should not block an infra-only bring-up, but it must be tracked and hardened **before** the
first `Application` lands. See SEC-2.

**Re-run can revert out-of-band hardening (nit — SEC-4).** `install-argocd.sh:62` uses
`kubectl apply --server-side --force-conflicts`. `--force-conflicts` is the correct, upstream-recommended path for
ArgoCD's oversized CRDs (and is well justified in the script header), but it also means a re-run **forcibly
reclaims field ownership** — so if an operator later narrows the `application-controller` ClusterRole out-of-band
(the SEC-2 hardening), a subsequent `install-argocd.sh` re-run silently reverts it back to stock `*/*/*`. Nit /
operational caution tied to SEC-2's remediation; see SEC-4.

**Security consequence of the k3d substitution (nit — SEC-5, cross-referenced).** The k3d fallback
(`install-k3s.sh:48,69-88`) requires a usable Docker daemon; membership in the `docker` group is **root-equivalent**
on the host, so k3d mode presumes a host where the operator already holds host-root-equivalent access. I record this
only as the *security consequence* of the substitution — whether the k3d-vs-native substitution is an acceptable
environment is **owned by `SUBTASK_review_honesty_scope_ops`** and is not adjudicated here. Nit; see SEC-5.

---

## 3. Findings

- [SEC-1] severity=minor concern=security_secrets_posture lens=security
  location=`cluster/install-k3s.sh:62,65` (and `cluster/README.md:41-49`)
  acceptance_criteria_touched=[AC1_cluster, AC2_gitops]
  statement: Native-mode k3s install writes the cluster-admin kubeconfig to `/etc/rancher/k3s/k3s.yaml` with
    `--write-kubeconfig-mode 0644`, making an admin credential world-readable by every local user on the host.
    Native-mode-only and documented ("adjust to taste" / "tighten for shared hosts"); it is the single place a
    credential's at-rest posture is loosened. Would rise to major on a shared/multi-tenant production host.
  evidence: `install-k3s.sh:65` `$sh_pfx sh -s - server --write-kubeconfig-mode 0644`; comment `:62`
    "lets a non-root client read /etc/rancher/k3s/k3s.yaml; adjust to taste"; `README.md:48-49`
    "uses `--write-kubeconfig-mode 0644` so a non-root client can read it; tighten for shared hosts."
  remediation: Default to `0600` (or omit the flag → k3s default `0600`) and have clients copy the kubeconfig to
    `~/.kube/config` with `chmod 600`; gate `0644` behind an explicit opt-in env var documented as single-user-host
    only.

- [SEC-2] severity=minor concern=least_privilege_rbac_cluster_posture lens=security
  location=`gitops/install-argocd.sh:62` (applies stock manifest) + `gitops/README.md:107-128` (RBAC posture)
  acceptance_criteria_touched=[AC2_gitops]
  statement: The stock upstream ArgoCD install grants `argocd-application-controller` a cluster-admin-equivalent
    (`*/*/*`) ClusterRole. `install-argocd.sh` applies the stock manifest unmodified (adds no extra grant). For a
    control-plane bring-up with zero `Application`s this is the documented upstream default and is namespace-isolated,
    but a standing `*/*/*` ClusterRole is a least-privilege over-grant that must be hardened before workloads are
    reconciled cluster-wide.
  evidence: `install-argocd.sh:62`
    `kubectl apply -n "${ARGOCD_NAMESPACE}" --server-side --force-conflicts -f "${MANIFEST_URL}"`;
    `README.md:109` "`argocd-application-controller` | Yes — ClusterRole (currently `*/*/*`, cluster-admin-equivalent)";
    `README.md:120-128` names the hardening levers and defers them to #13.
  remediation: Before #13's first `Application`, scope the `application-controller` ClusterRole from `*/*/*` to the
    specific apiGroups/resources the managed workloads need and/or constrain targets with AppProjects
    (per-team source/destination/namespace allow-lists); for a single-namespace footprint, adopt the upstream
    namespace-scoped install (`namespace-install.yaml`). Track as a follow-up hardening issue now.

- [SEC-3] severity=minor concern=security_secrets_posture lens=security
  location=`cluster/install-k3s.sh:63-65`; `gitops/install-argocd.sh:41,62`
  acceptance_criteria_touched=[AC1_cluster, AC2_gitops]
  statement: Both remote installers are HTTPS and version-pinned but not digest-/checksum-pinned and not
    signature-verified at install. k3s: `curl -sfL https://get.k3s.io | sh` runs a mutable install script (the k3s
    binary is version-pinned + upstream-checksum-verified internally). ArgoCD: the manifest is fetched from a movable
    git **tag** (`…/argo-cd/v3.5.4/manifests/install.yaml`) rather than a commit SHA, and the images it references
    are pinned by **tag** (`quay.io/argoproj/argocd:v3.5.4`), not digest, with no cosign verification. Upstream-
    recommended paths, so low risk — but tag/ref trust is weaker than digest trust.
  evidence: `install-k3s.sh:63-65` `curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION="$K3S_VERSION" $sh_pfx sh …`;
    `install-argocd.sh:41` `MANIFEST_URL="https://raw.githubusercontent.com/argoproj/argo-cd/${ARGOCD_VERSION}/manifests/install.yaml"`;
    `:62` server-side apply of that URL; no `cosign verify`/digest pin present anywhere in the tree.
  remediation: Optional supply-chain hardening (defer to the #13 Application era is acceptable): pin the ArgoCD
    manifest by commit SHA and images by `@sha256:` digest (or mirror into an internal registry); vendor/checksum the
    k3s install script; longer-term, verify image signatures at admission (cosign keyless, identity-pinned) once a
    policy engine is in the cluster.

- [SEC-4] severity=nit concern=least_privilege_rbac_cluster_posture lens=security
  location=`gitops/install-argocd.sh:62`
  acceptance_criteria_touched=[AC2_gitops]
  statement: `kubectl apply --server-side --force-conflicts` is correct for ArgoCD's oversized CRDs, but
    `--force-conflicts` forcibly reclaims field ownership, so a re-run silently reverts any out-of-band narrowing of
    the `application-controller` ClusterRole (the SEC-2 hardening) back to stock `*/*/*`.
  evidence: `install-argocd.sh:62` `--server-side --force-conflicts`; header `:23-27` justifies server-side apply for
    the >262144-byte applicationsets CRD (justification is sound).
  remediation: When SEC-2 hardening is applied, express it as GitOps-managed overlay/config the install path does not
    overwrite (or re-apply the narrowed ClusterRole after install), and note in the runbook that a stock re-run
    reverts manual RBAC narrowing. (Keep `--force-conflicts` — it is the right call for the CRDs.)

- [SEC-5] severity=nit concern=least_privilege_rbac_cluster_posture lens=security
  location=`cluster/install-k3s.sh:48,69-88`
  acceptance_criteria_touched=[AC1_cluster]
  statement: Security consequence only (acceptability of the substitution is owned by SUBTASK_review_honesty_scope_ops):
    k3d mode requires Docker daemon access, and `docker`-group membership is root-equivalent on the host, so k3d mode
    presupposes an operator already holding host-root-equivalent privilege.
  evidence: `install-k3s.sh:48` `can_k3d() { have k3d && have docker && docker info …; }`;
    `cluster/README.md:11-12` "K3D … a usable Docker daemon (membership in the `docker` group suffices)."
  remediation: None required from this lens — informational, for the gate's awareness; defer substitution-acceptability
    judgment to `SUBTASK_review_honesty_scope_ops`.

---

## 4. Acceptance-criteria bearing

| Criterion | This lens's bearing |
|---|---|
| **AC2_gitops** ("…kubeconfig + ArgoCD access documented, retrieved at runtime and never staged"; namespace isolation) | **Supports pass.** ArgoCD isolated in its own `argocd` namespace, closed-by-default ClusterIP, stock NetworkPolicies; admin credential + kubeconfig runtime-retrieved, never staged (independent scan clean); rotate-and-delete-bootstrap-secret documented. Open hardening notes: SEC-2 (application-controller `*/*/*`), SEC-3 (ArgoCD manifest/image pinning), SEC-4 (re-run reverts RBAC narrowing). None block. |
| **AC4_runbook** ("…commit no secrets" clause) | **Supports pass (clean).** Independent hard-value secret scan over the staged tree **and** the diff = zero matches; only runtime-retrieval commands documented. No finding raised against the no-secrets clause. |
| **AC1_cluster** (kubeconfig at-rest; installer provenance) | Secondary bearing: SEC-1 (native kubeconfig `0644`), SEC-3 (k3s installer pinning), SEC-5 (k3d root-equivalence consequence). None block. |
| **AC3_wasm** | Not in this lens's scope; no security finding. (Note for completeness: the wasm path uses `cargo install … --version <pinned> --locked` — pinned + lockfile-locked, good supply-chain hygiene.) |

**Lens disposition: no open `block`, no open `major`.** All five findings are `minor`/`nit` hardening observations;
the gate should carry SEC-2 and SEC-3 as pre-#13 hardening follow-ups. Secrets posture (concern 4) and RBAC/cluster
posture (concern 5) are both **clean** at the control-plane bring-up grain this PR targets.
