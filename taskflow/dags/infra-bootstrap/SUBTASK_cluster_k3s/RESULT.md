# RESULT — Cluster provisioning & verification (k3s) (issue #10)

## Spoke
- subtask: SUBTASK_cluster_k3s
- owns-criteria: [cluster]

## Versions
- k3s: v1.35.5+k3s1                       # node osImage "K3s v1.35.5+k3s1"; k3d image docker.io/rancher/k3s:v1.35.5-k3s1
- k3d: v5.9.0                             # runs real k3s in Docker (rootless-via-docker install path)
- kubectl (client): v1.37.1
- docker (server): 29.5.2                 # cgroup v2, systemd cgroup driver

## Criteria
### cluster  — verdict: PASS
- what: k3s cluster installed/verified reachable; `kubectl get nodes` shows a Ready node; kubeconfig access documented as a retrieval command/path.
- evidence:
  - command: `./verify-cluster.sh`   # KUBE_CONTEXT=k3d-nswe
    observed: |
      [verify-cluster] waiting up to 120s for all nodes to be Ready ...
      NAME                STATUS   ROLES           AGE    VERSION        OS-IMAGE           CONTAINER-RUNTIME
      k3d-nswe-agent-0    Ready    <none>          129m   v1.35.5+k3s1   K3s v1.35.5+k3s1   containerd://2.2.3-k3s1
      k3d-nswe-server-0   Ready    control-plane   129m   v1.35.5+k3s1   K3s v1.35.5+k3s1   containerd://2.2.3-k3s1
      k3s server version (node osImage): K3s v1.35.5+k3s1
      kube-system: coredns Running(1/1), local-path-provisioner Running(1/1), metrics-server Running(1/1),
                   traefik Running(1/1), svclb-traefik Running(2/2 x2), helm-install-traefik* Completed
      [verify-cluster] PASS: cluster is Ready and core system workloads are healthy.  (exit 0)
  - command: `./install-k3s.sh`   # idempotency proof — cluster already present
    observed: |
      [install-k3s] K3D mode: cluster 'nswe' already exists -> idempotent no-op (merging kubeconfig)
      [install-k3s] install complete (mode=k3d).  (exit 0)
- notes: |
    This is a genuine k3s cluster (two Ready nodes, control-plane + agent, k3s v1.35.5+k3s1), stood up
    in K3D mode (real k3s running inside Docker). It was NOT fabricated. The method matters for honesty:
    the canonical NATIVE install `curl -sfL https://get.k3s.io | sh -` (systemd unit + binary into
    /usr/local/bin) cannot run on THIS build host — it is a rootless sandbox (see the honest sub-blocker
    below). The staged install-k3s.sh carries BOTH paths and auto-selects; on a privileged production
    host it performs the NATIVE systemd install of the same pinned k3s version. Kubeconfig access is
    documented as a RETRIEVAL command in README.md (`k3d kubeconfig get/merge nswe`, or
    /etc/rancher/k3s/k3s.yaml for native); no credential value is staged.
- native-install sub-blocker (transparency; does NOT block the PASS above, which used k3d):
    command: `curl -sfL https://get.k3s.io | sh -`
    error: |
      requires root to write /usr/local/bin/k3s and /etc/systemd/system/k3s.service; both are
      NOT writable as uid=1001, and `sudo -n true` returns "a password is required" (no
      non-interactive root). Egress to get.k3s.io is fine (HTTP 200); cgroup v2 and systemd are present.
    env_fact: "rootless sandbox: uid=1001, non-interactive sudo unavailable, /usr/local/bin & /etc/systemd/system not writable"
    remediation: |
      On a production host with root (or passwordless sudo) + systemd + cgroup v2, run
      `K3S_INSTALL_MODE=native ./install-k3s.sh` then
      `KUBE_CONTEXT=default KUBECONFIG=/etc/rancher/k3s/k3s.yaml ./verify-cluster.sh`.

## Staged files
- deploy/bootstrap/cluster/install-k3s.sh: reproducible k3s stand-up; auto-selects NATIVE (root/systemd via get.k3s.io) or K3D (rootless-via-docker); pinned k3s v1.35.5+k3s1; idempotent (native re-runnable; k3d create-if-missing, K3S_FORCE_RECREATE=1 to recreate).
- deploy/bootstrap/cluster/verify-cluster.sh: real readiness proof — `kubectl wait --for=condition=Ready nodes --all` + CoreDNS Running check + version print; read-only, re-runnable; exits non-zero if not ready.
- deploy/bootstrap/cluster/README.md: cluster runbook fragment — prereqs, run order, kubeconfig RETRIEVAL (no secrets), verification meaning, and the native-install blocker + remediation.

## Secrets check
- confirmed-no-secrets: true   # no kubeconfig with live credentials, no token, no password, no private key staged or committed
- notes: Kubeconfig is obtained at runtime via `k3d kubeconfig get/merge nswe` (K3D) or /etc/rancher/k3s/k3s.yaml (native); only the retrieval commands are documented, never credential values.
