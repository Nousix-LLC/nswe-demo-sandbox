# RESULT — GitOps control-plane install (ArgoCD) (issue #10)

## Spoke
- subtask: SUBTASK_gitops_argocd
- owns-criteria: [argocd]

## Versions
- ArgoCD: v3.5.4                          # pinned; running image quay.io/argoproj/argocd:v3.5.4; `argocd version` -> v3.5.4
- manifest: argoproj/argo-cd@v3.5.4 manifests/install.yaml   # https://raw.githubusercontent.com/argoproj/argo-cd/v3.5.4/manifests/install.yaml
- namespace: argocd (dedicated)
- target cluster: k3s v1.35.5+k3s1 (context k3d-nswe, from SUBTASK_cluster_k3s)   # kubectl client v1.37.1
- install mechanism: kubectl server-side apply (--server-side --force-conflicts)

## Criteria
### argocd  — verdict: PASS
- what: ArgoCD installed into its own namespace from a pinned declarative manifest; core workloads reach Ready; API/UI access + initial-admin-credential RETRIEVAL documented (no secret committed); least-privilege RBAC posture noted; ArgoCD version recorded.
- evidence:
  - command: `kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/v3.5.4/manifests/install.yaml`
    observed: |
      All objects applied with exit 0 (CRDs applications/applicationsets/appprojects.argoproj.io,
      7 Deployments/StatefulSet, Services, ConfigMaps, 3 ClusterRoleBindings + 7 RoleBindings,
      7 NetworkPolicies). NOTE: the first attempt with plain client-side `kubectl apply` failed on
      `applicationsets.argoproj.io` with `metadata.annotations: Too long: may not be more than 262144
      bytes` (the known large-CRD client-side-apply limit); re-running with `--server-side` succeeded
      cleanly. The staged install-argocd.sh uses server-side apply for exactly this reason.
  - command: `./verify-argocd.sh`   # staged read-only readiness proof, ARGOCD_NAMESPACE=argocd
    observed: |
      [verify-argocd] checking ArgoCD CRDs are registered ...
      deployment "argocd-redis" successfully rolled out
      deployment "argocd-repo-server" successfully rolled out
      deployment "argocd-dex-server" successfully rolled out
      deployment "argocd-applicationset-controller" successfully rolled out
      deployment "argocd-notifications-controller" successfully rolled out
      deployment "argocd-server" successfully rolled out
      partitioned roll out complete: 1 new pods have been updated...   # argocd-application-controller StatefulSet
      NAME                                                READY   STATUS    RESTARTS   AGE
      argocd-application-controller-0                     1/1     Running   0          2m34s
      argocd-applicationset-controller-5c66f59556-t6c4q   1/1     Running   0          2m34s
      argocd-dex-server-64cc54b998-tvlrk                  1/1     Running   0          2m34s
      argocd-notifications-controller-68d59788b7-bgx6v    1/1     Running   0          2m34s
      argocd-redis-7f877d46b7-zvqtw                       1/1     Running   0          2m34s
      argocd-repo-server-7bc46c4ddf-qhfjg                 1/1     Running   0          2m34s
      argocd-server-57bf79bfcc-h9qjl                      1/1     Running   0          2m34s
      [verify-argocd] installed argocd-server image: quay.io/argoproj/argocd:v3.5.4
      [verify-argocd] PASS: ArgoCD control plane is installed and all core workloads are Ready in 'argocd'.  (exit 0)
  - command: `SKIP_WAIT=1 ./install-argocd.sh`   # idempotency proof — re-run converges, no error
    observed: |
      [install-argocd] applying pinned ArgoCD manifest via server-side apply (idempotent; converges to desired state) ...
      (all objects report serverside-applied/unchanged)  exit 0
  - command: `kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.metadata.name}{" type="}{.type}'`
    observed: |
      argocd-initial-admin-secret  type=Opaque
      # Secret EXISTS (decoded admin password is 16 chars); value deliberately NOT read into any file.
      # Documented retrieval command (runtime only):
      #   kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d
- notes: |
    Genuine install against the live k3d-nswe k3s cluster (NOT fabricated): 7/7 core ArgoCD workloads
    Running 1/1, server image pinned to v3.5.4. Control plane only — NO ArgoCD `Application`, app
    manifests, or images were created (those are #13/#12). Access is via `kubectl -n argocd
    port-forward svc/argocd-server 8080:443` (stock ClusterIP service; no external exposure configured,
    closed-by-default). RBAC/least-privilege posture (full detail in the staged README):
      - application-controller / applicationset-controller / argocd-server hold ClusterRoles (need
        cross-namespace reconcile); application-controller's is the stock `*/*/*` (cluster-admin-equiv)
        — flagged as the primary hardening lever (scope via AppProjects / narrowed ClusterRole /
        namespace-install) for when the first Application is introduced.
      - repo-server (highest-risk: renders arbitrary repo content), redis, dex, notifications hold
        namespace-scoped Roles ONLY — zero cluster permissions (least privilege).
      - 7 default NetworkPolicies (one per component) ship with the install for in-namespace isolation.
    Credential hardening documented: change admin password then delete argocd-initial-admin-secret;
    prefer SSO via the bundled dex server over the bootstrap admin account.

## Staged files        # repo-relative paths staged under SUBTASK_gitops_argocd/staged/<path>
- deploy/bootstrap/gitops/install-argocd.sh: pinned (v3.5.4), idempotent ArgoCD install into the dedicated `argocd` namespace via server-side apply + readiness wait; prereq/re-run header; env-overridable (ARGOCD_VERSION / ARGOCD_NAMESPACE / SKIP_WAIT). Safe to re-run (converges to desired state).
- deploy/bootstrap/gitops/verify-argocd.sh: read-only readiness proof — rollout status of all 6 core Deployments + the application-controller StatefulSet, CRD presence, all-pods-Running assertion, prints installed image; exits non-zero if not Ready. Side-effect-free; re-runnable.
- deploy/bootstrap/gitops/README.md: access runbook fragment — prereqs, run order, API/UI access (port-forward), runtime admin-credential RETRIEVAL (no value) + rotation/delete hardening, full RBAC/least-privilege posture table, NetworkPolicy note, security notes, pinned versions.

## Secrets check
- confirmed-no-secrets: true   # secret-pattern scan over the staged tree returned zero embedded-value matches; no kubeconfig/token/password/key staged
- notes: |
    The ArgoCD initial admin credential is generated by ArgoCD inside the cluster and is RETRIEVED at
    runtime via a documented `kubectl get secret ... | base64 -d` command; its value is never staged or
    committed. The only references to `argocd-initial-admin-secret` in staged files are the retrieval
    command, the delete-after-rotation command, and explanatory prose. No kubeconfig with live
    credentials is staged (cluster access is retrieved per the cluster spoke's README).
