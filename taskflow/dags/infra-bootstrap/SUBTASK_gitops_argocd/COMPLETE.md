# COMPLETE — SUBTASK_gitops_argocd (issue #10, infra-bootstrap)

## What was done
Installed the **ArgoCD GitOps control plane v3.5.4** into a dedicated `argocd` namespace on the live
k3s cluster (`k3d-nswe`, from `SUBTASK_cluster_k3s`), proved its core workloads reach Ready with a
real read-only check, and staged a reproducible, idempotent install + verification + access runbook —
delivered with an honest evidence record. The `argocd` criterion is **PASS** against the real cluster.

## Outcome (argocd criterion: PASS)
- ArgoCD **v3.5.4** pinned (image `quay.io/argoproj/argocd:v3.5.4`), applied from the upstream
  `manifests/install.yaml` at tag `v3.5.4` via **server-side apply** (the client-side path fails on the
  oversized `applicationsets.argoproj.io` CRD — captured honestly in `RESULT.md`).
- **7/7 core workloads Running 1/1**: application-controller (StatefulSet), server, repo-server, redis,
  dex, applicationset-controller, notifications-controller. Proven by the staged `verify-argocd.sh`
  (exit 0, PASS) — not assumed.
- Idempotency proven: re-running `install-argocd.sh` converges (server-side apply, exit 0).

## Deliverables (all under this task's owned paths)
- `staged/deploy/bootstrap/gitops/install-argocd.sh` — pinned, idempotent install + readiness wait.
- `staged/deploy/bootstrap/gitops/verify-argocd.sh` — read-only readiness proof.
- `staged/deploy/bootstrap/gitops/README.md` — access (port-forward), runtime credential retrieval
  (no value), RBAC/least-privilege posture, NetworkPolicy + security notes.
- `RESULT.md` — evidence record per `contracts/result_record.schema.md`; `owns-criteria: [argocd]`.

## Contract & scope compliance
- Wrote ONLY under owned paths (`staged/deploy/bootstrap/gitops/**`, `RESULT.md@SUBTASK_gitops_argocd`);
  touched no git, no repo checkout, no sibling output, no unified runbook (the synthesis gate owns those).
- `RESULT.md` follows the frozen schema literally.
- **Infra-only honored**: no ArgoCD `Application`, no app Deployment/Service manifests, no container
  builds (#13/#12 untouched). Only ArgoCD's own install workloads were created.
- **No secrets committed** (`confirmed-no-secrets: true`): the admin credential is retrieved at runtime
  via a documented command; a secret-pattern scan over the staged tree returned zero value matches.

## Notes for the synthesis gate
- The `argocd` criterion verdict + evidence + versions are in `RESULT.md` for enumeration (identity I1,
  I4, I5). The staged scripts carry prereq/re-run headers (I3); the README documents run order +
  verification. I2 (no secrets) and I6 (infra-only scope) hold for this spoke's outputs.
- Hardening lever flagged honestly: the stock `argocd-application-controller` ClusterRole is `*/*/*`
  (cluster-admin-equivalent); scoping it (AppProjects / narrowed ClusterRole / namespace-install) is a
  follow-on decision for when the first `Application` lands (#13), out of scope here.
