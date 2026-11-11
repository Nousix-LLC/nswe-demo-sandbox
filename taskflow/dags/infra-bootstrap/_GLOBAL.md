# _GLOBAL.md — infra-bootstrap (#10, EPIC #3 devops) subtree hub

## Project Context

**Status**: Active (decomposed)

### Objective
Stand up and **prove** the deployment environment the engagement's continuous delivery will run
on: a **k3s** cluster, **ArgoCD** installed into its own namespace, and the **wasm build
toolchain** (`wasm32-unknown-unknown` + wasm-bindgen) proven against the existing
`crates/chirp-frontend`. Add **reproducible bootstrap scripts/manifests** + a runbook, deliver
commits on `work/infra-bootstrap`, a **PR into `main` that Closes #10**, and a root `SYNTHESIS.md`
verdict at the observation seam. **Infra-only**: it does NOT containerize the app (#12) or author
app deploy manifests / the ArgoCD Application (#13).

### Scope
**In scope:** k3s install + real readiness check + kubeconfig-access docs; ArgoCD install (own
namespace) + readiness + access/credential-retrieval docs (no secrets committed) + least-privilege
RBAC posture; wasm target + wasm-bindgen + a real `chirp-frontend` wasm build with pinned versions;
idempotent re-runnable bootstrap scripts under `deploy/bootstrap/` + a runbook; honest blocker
reporting if the host/sandbox forbids the install.

**Out of scope:** containerizing chirp-server (#12); authoring app Deployment/Service manifests or
the ArgoCD `Application` (#13); any repo other than `Nousix-LLC/nswe-demo`; merging the PR or pushing
to `main` (the overseer lands — P1).

### Success Criteria
- [ ] k3s cluster installed/verified reachable; `kubectl get nodes` shows a Ready node; kubeconfig-access documented.
- [ ] ArgoCD installed into its own namespace, core workloads Ready; API/UI access + admin-credential RETRIEVAL documented (no secret committed).
- [ ] `wasm32-unknown-unknown` + wasm-bindgen present; a real `chirp-frontend` wasm build succeeds; exact versions recorded.
- [ ] Bootstrap scripts/manifests are reproducible/idempotent, committed under `deploy/bootstrap/`, with a runbook.
- [ ] If blocked by host/sandbox: exact blocker + remediation recorded in PR body and `SYNTHESIS.md`; blocked criteria marked; whatever is reproducible is delivered. No fabricated green.
- [ ] Commits on `work/infra-bootstrap`; PR into `main` Closes #10; root `SYNTHESIS.md` carries the machine-gate verdict. PR not merged; `main` not pushed.

## Chosen Cut & Rationale (decompose-moment record)

The brief enumerates six concerns; three are **distinct system components** (cluster / GitOps
control plane / build toolchain) each binding a **different methodology** (kubernetes / gitops /
rust+frontend), and three are **cross-cutting properties** (reproducibility, security, honest
reporting) that bind every component rather than forming their own tasks.

Candidate cuts considered:
- **(A) by layer** — install-layer / verify-layer / doc-layer. **Rejected:** every layer co-writes
  the same scripts + runbook (ownership-disjointness violation) and maximizes cross-sibling edges.
- **(B) by component + synthesis gate** — k3s / argocd / wasm spokes + one synthesis gate.
  **Chosen:** disjoint path ownership (each spoke owns a subtree under `deploy/bootstrap/`), minimal
  edges (only argocd→k3s, a runtime serialize), each child independently reviewable.
- **(C) merge cluster+gitops into one child** — **Rejected:** bundles two methodologies and two
  distinct verbs (provision-cluster *and* install-control-plane) into one task → single-responsibility
  violation and a larger-than-reviewable diff.

The three cross-cutting concerns are carried as **subtree-wide constraints** (below) + **contract
identities** (`contracts/_MANIFEST.yaml`) the synthesis gate asserts — not as separate parallel
tasks (they are properties, not components).

Sizing (feed-forward): each build spoke forecasts S–M (one install/prove script set + a fragment +
an evidence record); the synthesis gate forecasts M (assemble runbook + git/PR + verdict). Each
child's own dispatch makes the authoritative atomic-vs-decompose call.

## Contract (REQUIRED)

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema`

The spokes are independent except for the runtime argocd→k3s edge (serialized as a dependency, not
frozen). The one frozen seam is **path-ownership + the per-spoke `RESULT.md` evidence schema**, so
the synthesis gate can mechanically enumerate ownership coverage and assert the #10 acceptance
criteria over the combined output. See `contracts/_MANIFEST.yaml` (ownership, identities I1–I6, seam
classification) and `contracts/result_record.schema.md` (the evidence record every spoke emits).
Freeze/serialize rationale is recorded in `_MANIFEST.yaml §seams`. Do NOT embed schema content in
briefs — reference `contracts/` by path.

## Task Structure

```
infra-bootstrap/
├── _GLOBAL.md                      (this hub)
├── contracts/                      (_MANIFEST.yaml + result_record.schema.md — READ-ONLY)
├── SUBTASK_cluster_k3s/_BRIEF.md   (k3s install + readiness + kubeconfig docs)
├── SUBTASK_wasm_toolchain/_BRIEF.md(wasm target + wasm-bindgen + chirp-frontend build proof)
├── SUBTASK_gitops_argocd/_BRIEF.md (ArgoCD install + readiness + access/RBAC docs)
└── SUBTASK_synthesis_gate/_BRIEF.md(verification gate + git branch/commits/PR + root SYNTHESIS.md)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_cluster_k3s` | none | Reproducible k3s install + real readiness check + kubeconfig-access docs | `SUBTASK_cluster_k3s/staged/deploy/bootstrap/cluster/**`, `SUBTASK_cluster_k3s/RESULT.md` |
| `SUBTASK_wasm_toolchain` | none | wasm32 target + wasm-bindgen; real `chirp-frontend` wasm build proof; pinned versions | `SUBTASK_wasm_toolchain/staged/deploy/bootstrap/wasm/**`, `SUBTASK_wasm_toolchain/RESULT.md` |
| `SUBTASK_gitops_argocd` | `SUBTASK_cluster_k3s` | ArgoCD into own namespace, readiness, access/credential-retrieval docs, RBAC posture | `SUBTASK_gitops_argocd/staged/deploy/bootstrap/gitops/**`, `SUBTASK_gitops_argocd/RESULT.md` |
| `SUBTASK_synthesis_gate` | `SUBTASK_cluster_k3s`, `SUBTASK_wasm_toolchain`, `SUBTASK_gitops_argocd` | Verification gate over combined output; assemble unified runbook; branch/commit/PR into main (Closes #10); root verdict | `deploy/bootstrap/README.md`, branch+PR, `SYNTHESIS.md` |

### Dependency Graph
```
SUBTASK_cluster_k3s ──┬──> SUBTASK_gitops_argocd ──┐
                      │                            ├──> SUBTASK_synthesis_gate
SUBTASK_wasm_toolchain ───────────────────────────┘
(cluster_k3s also feeds synthesis directly)
```
Execution groups — G0: `cluster_k3s`, `wasm_toolchain`; G1: `gitops_argocd`; G2: `synthesis_gate`.

## Subtree Methodology Posture

- **Dominant task types**: infra provisioning/verification (Kubernetes), GitOps control-plane
  install (GitOps + Kubernetes Security), and build-toolchain enablement (Rust + Frontend), plus a
  verification-gate synthesis (Synthesis). Rough split: one spoke each + one gate.
- **Primary bundles the subtree draws on**: `kubernetes`, `gitops`, `rust`, `synthesis` — children
  may assume these in scope for their respective areas without re-justifying.
- **Cross-cutting bindings (every leaf)**: `operations` (reproducible scripts, runbook, GitWorkflow
  PR lifecycle), `security` / `kubernetes-security` (no secrets, least-privilege RBAC, runtime
  credential retrieval). Each child selects/loads its own bundles on-demand from the IDs its
  `_BRIEF.md` names.
- Suggestion-not-prescription: each descendant is the final judge of what it loads.

## Subtree-Wide Constraints (inherited by every descendant)

1. **Infra-only**: do NOT containerize the app (#12) or author app deploy manifests / the ArgoCD
   `Application` (#13). ArgoCD's own install workloads are in scope; an app Application is not.
2. **No secrets committed**: no kubeconfig with live credentials, no ArgoCD admin password, no
   tokens/keys in any staged file or commit. Document how to RETRIEVE credentials at runtime.
3. **Reproducibility**: every script declares prereqs + is safe to re-run (idempotent where
   feasible); document run order + a verification step.
4. **Honest environment reporting**: if host privileges/sandbox block an install (no root/systemd,
   no egress, cgroup constraints, etc.), record the **exact** blocker (command + error + env fact) and
   a concrete **remediation**, deliver what is verifiably reproducible, and mark the blocked criteria.
   A clean honest partial beats a fabricated green.
5. **Repo & git discipline**: repo is `Nousix-LLC/nswe-demo` ONLY. Branch `work/infra-bootstrap` off
   `main`. PR into `main` Closes #10. Never force-push/rewrite `main`. **No attribution trailers** on
   commits. Do NOT merge the PR or push to `main` (P1 — the overseer lands). Only the synthesis gate
   performs git operations; spokes stage files only.

## Environment facts (grounding relayed to children)

- Repo remote: `https://github.com/Nousix-LLC/nswe-demo.git`, base `origin/main` (brief baseline
  `fcfc7a2`). Prior work-items operate in a per-DAG `checkout/` worktree; the synthesis gate should
  establish `checkout/` off `origin/main` under this DAG root for its git/PR work.
- Workspace layout: crates live at `crates/{ferric,ferric-http,ferric-router,chirp-types,chirp-frontend,...}`.
- **wasm build tool = wasm-bindgen (NOT trunk)**: `crates/chirp-frontend` has no `Trunk.toml`; its
  `index.html` imports `./pkg/chirp.js` and the README describes generating `pkg/chirp.js` +
  `pkg/chirp_bg.wasm` from the built **example** via `wasm-bindgen` after a `--target wasm32-unknown-unknown`
  build. Prove the toolchain against that path; do not modify `chirp-frontend` source.
- The host may be a sandbox lacking root/systemd/egress — treat the install's feasibility as something
  to VERIFY and honestly report, not assume.
