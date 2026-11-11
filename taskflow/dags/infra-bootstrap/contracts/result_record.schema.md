# contracts/result_record.schema.md — the per-spoke RESULT.md evidence record (FROZEN seam)

READ-ONLY. Each build spoke (`SUBTASK_cluster_k3s`, `SUBTASK_wasm_toolchain`,
`SUBTASK_gitops_argocd`) writes exactly one `RESULT.md` at its own task-workspace root, following
this schema. The synthesis gate enumerates these three records to evaluate the contract identities
(see `_MANIFEST.yaml`) and to assemble the PR body + root `SYNTHESIS.md`. Import this shape
literally; do not invent a different evidence format.

A spoke records **only the criteria it owns** (see the ownership split in `_GLOBAL.md`). Honesty
rule: a criterion is `PASS` only with reproducible evidence (command + observed output); otherwise
it is `BLOCKED` with an exact blocker and a concrete remediation. Never a fabricated green.

## Required structure

```markdown
# RESULT — <spoke human name> (issue #10)

## Spoke
- subtask: SUBTASK_<slug>
- owns-criteria: [<criterion-id>, ...]   # subset of {cluster, argocd, wasm, reproducible, honest}

## Versions            # component/toolchain versions this spoke installed or proved
- <name>: <exact version>                # e.g. k3s: v1.xx.x+k3s1 | rustc: 1.xx.x | wasm-bindgen: 0.2.xx
  # (wasm spoke MUST include rustc, cargo, wasm-bindgen, and the wasm32-unknown-unknown target line)

## Criteria            # one block per owned criterion
### <criterion-id>  — verdict: PASS | BLOCKED
- what: <one line: what this criterion requires>
- evidence:           # REQUIRED when PASS (command actually run + what was observed)
  - command: `<cmd>`
    observed: |
      <verbatim or faithfully-summarized output proving the criterion, e.g. `kubectl get nodes`
       showing a Ready node, ArgoCD pods Ready, or a successful wasm build producing pkg/*.wasm>
- blocker:            # REQUIRED when BLOCKED (omit when PASS)
    command: `<the exact command that failed>`
    error: |
      <verbatim error / observed failure>
    env_fact: <the environment fact that caused it — e.g. "no root/systemd in sandbox",
               "no egress to get.k3s.io", "cgroup v2 unavailable">
- remediation:        # REQUIRED when BLOCKED — a concrete path to make it pass
    <ordered, specific steps a privileged operator would run to satisfy this criterion>

## Staged files        # repo-relative paths this spoke staged under SUBTASK_<slug>/staged/<path>
- <repo-relative path>: <one-line description; note idempotency / re-run behavior>

## Secrets check
- confirmed-no-secrets: <true|false>   # true = this spoke committed no live kubeconfig/token/password/key
- notes: <how runtime credentials are obtained instead, if applicable>
```

## Notes binding all spokes
- **Staging, not committing.** Spokes write repo-destined files under `SUBTASK_<slug>/staged/`
  mirroring the intended repo path (e.g. `staged/deploy/bootstrap/cluster/install-k3s.sh`). Spokes do
  NOT run git and do NOT touch the repo checkout — the synthesis gate owns all git.
- **Prove, do not assume.** "Readiness" means a real check was executed (e.g. `kubectl get nodes`,
  ArgoCD workloads Ready, a wasm artifact actually produced), and its output is in `evidence.observed`.
- **No secrets.** Document how to RETRIEVE a credential at runtime; never record a credential value.
