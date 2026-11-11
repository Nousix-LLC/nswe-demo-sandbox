# COMPLETE — SUBTASK_cluster_k3s (k3s cluster provisioning & verification)

## What was done
Stood up and **proved** the engagement's k3s deployment cluster, and produced a reproducible,
idempotent script set + runbook fragment + honest evidence record. `decompose_evaluation = Atomic`
(one component, one methodology, one install/prove/document cycle — all decomposition triggers
cleared and both concern tests passed).

## Outcome (honest)
- **cluster criterion: PASS** — real cluster, not fabricated. Two Ready nodes
  (`k3d-nswe-server-0` control-plane + `k3d-nswe-agent-0`) at **k3s v1.35.5+k3s1**; CoreDNS,
  local-path-provisioner, metrics-server, and traefik healthy. Proven by `./verify-cluster.sh`
  (exit 0) and install idempotency by a re-run no-op of `./install-k3s.sh` (exit 0).
- Cluster was stood up in **K3D mode** (real k3s in Docker) because this build host is a rootless
  sandbox where the canonical NATIVE `get.k3s.io` systemd install cannot run (uid 1001, no
  non-interactive sudo, `/usr/local/bin` + `/etc/systemd/system` not writable). This native-install
  sub-blocker + remediation is recorded transparently in `RESULT.md` and the runbook; the staged
  installer carries BOTH paths and auto-selects (native on a privileged production host).

## Outputs
- `staged/deploy/bootstrap/cluster/install-k3s.sh` — reproducible, idempotent, env-adaptive k3s install (pinned v1.35.5+k3s1).
- `staged/deploy/bootstrap/cluster/verify-cluster.sh` — real readiness proof (nodes Ready + CoreDNS), gating exit code.
- `staged/deploy/bootstrap/cluster/README.md` — cluster runbook fragment (prereqs, run order, kubeconfig retrieval, verification, blocker+remediation).
- `RESULT.md` — evidence record per `contracts/result_record.schema.md`, owns-criteria `[cluster]`.

## Contract compliance
- Composed against `../contracts/` literally (ownership `staged/deploy/bootstrap/cluster/**` +
  `RESULT.md`; `result_record.schema.md` shape followed). No contract modified; no amendment needed.
- **I2 no-secrets**: PASS — secret-pattern scan found zero live values; `confirmed-no-secrets: true`.
  Kubeconfig documented as retrieval-only.
- **I6 infra-only**: PASS — no app Deployment/Service, no ArgoCD `Application`, no Dockerfile/app image.
- Staged files only; ran no git and touched no repo checkout (synthesis gate owns git).
- Scope honored: no ArgoCD, no app workloads, no container images.

## Handoff to dependents
`SUBTASK_gitops_argocd` installs ArgoCD INTO this cluster: use context **`k3d-nswe`** (merged into
the default kubeconfig by `install-k3s.sh`), cluster is Ready now. `SUBTASK_synthesis_gate` reads
this `RESULT.md` and the staged tree; the `cluster` criterion is owned here with a PASS verdict and
reproducible evidence.
