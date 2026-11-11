# Task: Synthesis verification gate — deploy, prove reachability, open the PR, author SYNTHESIS.md

## Task Specification

**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective

Act as the deploy-argocd subtree's **verification gate** (NOT a prose summary): verify the combined
manifests compose and satisfy the contract identities, deploy/sync them onto the live k3d cluster and
**demonstrate the app is actually reachable**, then land the work — commit on `work/deploy-argocd`,
open a PR into `main` that `Closes #13`, and author the root `SYNTHESIS.md` fold record carrying the
PASS/FAIL verdict, the decision record, and the reachability evidence.

### Context

Part of the deploy-argocd subtree (NSWE #13) — see `../_GLOBAL.md` and `../contracts/`. You read the
outputs of all three prior tasks; you do not re-author their manifests (except via remediation
fix-tasks). This is the fold point: your `SYNTHESIS.md` at the subtree root is both your terminal
record and what folds the parent `SUSPENDED → COMPLETED`.

**Dependencies**: `SUBTASK_discovery`, `SUBTASK_app_manifests`, `SUBTASK_argocd_gitops`.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Scope, acceptance criteria, constraints |
| Contract | `../contracts/_MANIFEST.yaml`, `../contracts/deploy_contract.yaml` | The identities to assert (the gate's assertion set) |
| Ground-truth facts | `../SUBTASK_discovery/outputs/ground_truth.md` | Digest, ports, ingress class, repo path, host/path to reach |
| App manifests | `deploy/chirp/*` (produced by `SUBTASK_app_manifests`) | Workload to verify + deploy |
| GitOps config | `deploy/argocd/*` (produced by `SUBTASK_argocd_gitops`) | Application + AppProject to verify + apply |

---

## Process Specification (verification-gate posture)

This gate spans several distinct kinds of work; run them in order and decide for yourself whether any
warrant further decomposition (remediation especially is decomposition-as-fix):

1. **Four-check gate over the combined output** — before touching the cluster:
   - *Contract/identities*: enumerate every identity in `../contracts/_MANIFEST.yaml` and assert each
     against the combined manifests (digest pinned; Service selector/targetPort; Ingress wiring +
     class; requests/limits + liveness/readiness; Application wired to `deploy/chirp` + the AppProject;
     AppProject least-privilege, no `*/*/*`; namespace isolation; no committed secrets).
   - *Wiring / no dead manifest*: every object is referenced/mounted (Service→pods, Ingress→Service,
     Application→path+project).
   - *Duplication*: exactly one producer per owned path; `deploy/chirp` and `deploy/argocd` disjoint.
   - *Review*: a focused review of the combined manifests for k3s/ArgoCD idiom and the security posture.
2. **Deploy + demonstrate reachability** on the live k3d `nswe` cluster: apply the AppProject +
   Application (and/or let ArgoCD sync), watch the rollout to Healthy/Synced, resolve any
   ImagePullBackOff or probe failures, then issue a real HTTP request through the k3d ingress path
   (`localhost:8081`, with the recorded Host/path) and capture the response proving the SPA or API
   health surface is served. A justified NodePort/port-forward is an acceptable fallback. Reachability
   must be **shown with evidence**, not asserted.
3. **Remediation (if the gate FAILs)**: schedule fix-tasks via `engine_amend_plan { add_task }`
   (Inject) for violations and re-verify — do not silently patch around a failure.
4. **Land the work**: commit the manifests on branch `work/deploy-argocd`, push, and open a PR into
   `main` that `Closes #13` with an accurate body and **no attribution trailers** (#27/HYG-1); confirm
   CI is green. Do NOT merge the PR or push to `main`.
5. **Author `SYNTHESIS.md`** at the subtree root (`../SYNTHESIS.md` relative to this task, i.e. the
   deploy-argocd workspace root) with: the machine-gate **PASS/FAIL** verdict, the per-identity
   results, the **reachability evidence** (the request issued + the response), the decision record
   (key choices: ingress mechanism, AppProject scoping, imagePullSecret handling, native-cluster
   divergences noted for #23), and the PR link.

### Methodology
Apply the suggested bundles below; run the gate mechanically-then-review per the synthesis bundle.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `SYNTHESIS.md` |
| Location | The deploy-argocd subtree root (the fold location) |

`SYNTHESIS.md` is both your terminal record and the fold seam. Also produce: commits on
`work/deploy-argocd` and the PR into `main` (the DAG's declared side-effect output).

---

## Success Criteria

- [ ] Every contract identity asserted with a recorded PASS/FAIL result (no silent plug).
- [ ] The app is demonstrably reachable on the live cluster, with the HTTP evidence captured in
      `SYNTHESIS.md`; the pod is not in ImagePullBackOff and probes reflect real readiness.
- [ ] A PR into `main` on `work/deploy-argocd` `Closes #13`, body accurate, CI green, **no attribution
      trailers**; the PR is NOT merged and `main` is NOT pushed.
- [ ] `SYNTHESIS.md` present at the subtree root with the PASS/FAIL verdict, per-identity results,
      reachability evidence, decision record, and PR link.
- [ ] Any gate FAIL was handled by injected remediation fix-tasks + re-verification, not inline plugs.

---

## Suggested Methodology Files

This child is a **verification gate** (deployment obligation). Load `synthesis` first, then the sibling
check/remediation files your reading of the subtree reveals you need. SUGGESTIONS — you judge coverage
depth.

- Task-type rows: *"Synthesizing / verifying a hub-and-spoke decomposition (contract + wiring + dedup +
  review gate)"* (primary `synthesis`; supporting `code-review`, `code-quality`); *"PR creation and
  management via gh CLI"* (`operations`); *"Kubernetes networking & service connectivity"*
  (`kubernetes`, for the reachability path); *"GitOps reconciliation / drift"* (`gitops`).
- Bundle IDs: `synthesis` (`Synthesis_Overview_Methodology.md` — anchor, always first;
  `Synthesis_Contract_Verification_Methodology.md` — the gate-time inverse of the contract we froze;
  `Synthesis_Wiring_Verification_Methodology.md`; `Synthesis_Duplication_Detection_Methodology.md`;
  `Synthesis_Code_Review_Methodology.md`; `Synthesis_Remediation_Methodology.md`), `operations`
  (`GitWorkflow_PR_Lifecycle_Methodology.md`, `CodeReview_PR_Authoring` via `code-review`), `kubernetes`
  + `gitops` (deploy + reachability), `kubernetes-security` (confirm the RBAC/supply-chain posture).
- Rationale: the synthesis bundle makes this a contract-enforcing gate (not a summary); operations
  covers the PR via gh CLI; kubernetes/gitops cover the live deploy + reachability proof.
- Load `Synthesis_Overview_Methodology.md` first (always); the contract/wiring/dedup files apply
  because this subtree composes against a `contracts/` manifest; remediation applies if violations
  are plausible. Synthesis never loads `decomposition/` content.

## Inherited Constraints

- Branch `work/deploy-argocd`; PR into `main` that `Closes #13`. A DAG never merges its own PR and
  never pushes `main`; never force-push `main` or rewrite merged history.
- **NO attribution trailers** on commits or the PR body (#27/HYG-1). Keep the PR body accurate.
- Only this project's k3d `nswe` cluster/namespaces and its ArgoCD; do not touch sibling apps/clusters.
- Reachability must be demonstrated with evidence, not asserted (acceptance criterion #4).
- Target k3d-hosted k3s only (#23 HSO-1); note any native-cluster divergence, do not take #23 on.

## Out-of-Scope Methodologies

- `decomposition/` content — a synthesis gate is the reassembly, not the split. (You MAY still inject
  remediation fix-tasks via `engine_amend_plan`; that is gate-driven correction, not re-cutting.)
- Re-authoring the sibling manifests in place to "fix" them — route failures through remediation
  fix-tasks, not silent edits.
