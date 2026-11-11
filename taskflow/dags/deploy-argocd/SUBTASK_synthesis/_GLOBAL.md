# _GLOBAL.md — SUBTASK_synthesis sub-subtree hub (deploy-argocd verification gate, NSWE #13)

## Project Context

**Status**: Active (sub-decomposition of the deploy-argocd synthesis verification gate).

This hub governs the sub-subtree rooted at `SUBTASK_synthesis`. The parent deploy-argocd subtree
(`../_GLOBAL.md`, `../contracts/`) decomposed its work into a serialized `discovery` precursor, two
disjoint authoring spokes (`../SUBTASK_app_manifests` → `deploy/chirp/*`, `../SUBTASK_argocd_gitops`
→ `deploy/argocd/*`, both COMPLETED), and this synthesis **verification gate**. This node's whole-task
spec is `./_BRIEF.md`; at dispatch it evaluated `NeedsDecompose` because the gate spans four distinct
kinds of work (a static contract/wiring/dedup/review check; a live-cluster deploy + reachability proof;
a git commit + PR into `main`; and authoring the root `SYNTHESIS.md` fold record) drawing on distinct
methodology bundles — the Single-Responsibility/Distinct-Concerns triggers fire, and the single-file
`SYNTHESIS.md` output does not override them (Trigger Precedence).

### Objective (of this sub-subtree)

Produce the deploy-argocd subtree's PASS/FAIL verification verdict **with evidence** and land the work:
statically assert the contract identities, deploy onto the live k3d `nswe` cluster and **demonstrate the
app is reachable**, open a PR into `main` that `Closes #13` (no attribution trailers, not merged), and
author the root `SYNTHESIS.md` fold record that folds the deploy-argocd subtree to COMPLETED.

### Success Criteria (sub-subtree)

- [ ] Every parent contract identity (`../contracts/_MANIFEST.yaml`) asserted with a recorded PASS/FAIL —
      static ones by `SUBTASK_static_gate`, runtime ones by `SUBTASK_deploy_reach` — no silent plug.
- [ ] The app is demonstrably reachable on the live cluster, HTTP evidence captured (not asserted);
      pod not in ImagePullBackOff; probes reflect real readiness.
- [ ] A PR into `main` on `work/deploy-argocd` `Closes #13`, accurate body, CI green, **no attribution
      trailers**; PR NOT merged and `main` NOT pushed.
- [ ] `SYNTHESIS.md` at the deploy-argocd subtree root (`../SYNTHESIS.md`) carries the verdict, per-identity
      results, reachability evidence, decision record, and PR link; the deploy-argocd subtree is folded COMPLETED.
- [ ] Any gate FAIL handled by injected remediation fix-tasks (`engine_amend_plan { add_task }`) +
      re-verification, never inline plugs or silent edits to the sibling manifests.

---

## Constraints and Requirements (inherited — bind every child of this hub)

- **Repo**: `Nousix-LLC/nswe-demo`; checkout at `/home/user/nswe-demo`. Base `origin/main @ ada3aa9`
  (ground_truth §1: the local `main` is stale at `25e90c0`, 5 behind, and lacks the #11 `Dockerfile`/`deploy/`
  baseline; the branch `work/deploy-argocd` does not exist yet). All landing is on `work/deploy-argocd`
  based at `ada3aa9`; PR into `main`. Never merge the PR, never push/force-push `main`, never rewrite merged history.
- **NO attribution trailers** on any commit or the PR body (#27/HYG-1) — this overrides any default
  "Generated with / Co-Authored-By" footer. Keep the PR body accurate to what shipped.
- **Target cluster only**: k3d cluster `nswe` (k3s v1.35.5+k3s1), ArgoCD ns `argocd` (v3.5.4). Serverlb maps
  `localhost:8081 -> 80` / `8444 -> 443` via Traefik. Do not touch sibling apps/clusters/namespaces.
- **Supply chain / RBAC**: image pinned by immutable `@sha256:` digest; least-privilege AppProject (no `*/*/*`),
  GitOps-managed. These are already satisfied in the sibling manifests; the gate ASSERTS them, it does not re-author.
- **No secrets committed**: GHCR package is private (ground_truth §6) → the imagePullSecret path is handled
  out-of-band (or the package made public) and documented in `SYNTHESIS.md`; nothing secret enters the tree.
- **Reachability shown with evidence, not asserted.** Target k3d-hosted k3s only (#23 HSO-1); note any
  native-cluster divergence, do not take #23 on.
- **Remediation, not silent repair**: route any gate FAIL through injected fix-tasks (`engine_amend_plan`),
  not inline edits of the sibling manifests.

---

## Methodology

### Subtree Methodology Posture

- **Dominant task types**: a `synthesis`/verification gate that also spans *Kubernetes networking & service
  connectivity* + *GitOps reconciliation/drift* (deploy + reachability) and *PR creation and management via
  gh CLI* (landing). The fold leaf is a `synthesis` task.
- **Primary bundles**: `synthesis` (the gate posture), `kubernetes` + `gitops` (deploy + reachability),
  `operations` + `code-review` (commit + PR). Supporting: `kubernetes-security` (confirm the RBAC/supply-chain
  posture holds), `core`.
- **Cross-cutting bindings** (bind every leaf): the no-attribution/branch/no-merge-main git posture; the
  evidence-not-assertion reachability rule; least-privilege + digest-pinning asserted (not re-authored);
  remediation-as-decomposition on FAIL.
- **Suggestion, not prescription**: each child loads the bundle IDs its brief names plus whatever its own
  reading reveals; it is the final judge of what it loads, and of its own atomic-vs-decompose evaluation.

### Chosen cut (serial verification pipeline, disjoint side-effect ownership)

Candidate cuts considered: **(A)** keep atomic — rejected at the kernel evaluation (four distinct
responsibilities + a tool-call envelope far past the atomic floor). **(B)** split by contract-identity —
rejected: shards one verification responsibility across the deploy boundary and every shard needs the
cluster, maximizing shared-state coupling. **(C) chosen** — a serial pipeline by *kind of work and
side-effect domain*: a read-only **static gate**, then a **cluster-only deploy+reachability**, then a
**git-only land+PR**, then a **fold** sub-synthesis. Each child owns a disjoint write-set (a report file /
the cluster + an evidence file / the git branch+PR + a record file / `SYNTHESIS.md`); the sibling manifests
are read-only shared input; every cross-sibling edge is unidirectional → a declared dependency. This cut has
disjoint ownership (hard gate satisfied), minimal cross edges, and independently reviewable children. Because
every edge is serialized, the sub-subtree's `contracts/` is a thin ownership + identity-coverage manifest
(no frozen interface seam is needed — see `contracts/`).

---

## Task Structure

```
SUBTASK_synthesis/
├── _GLOBAL.md                          (this hub)
├── contracts/
│   ├── _MANIFEST.yaml                  (per-child ownership + identity-coverage map + fold obligation)
│   └── synthesis_gate_contract.yaml    (output-artifact locations/schemas the fold composes)
├── SUBTASK_static_gate/_BRIEF.md       (Group 0 — read-only static four-check; writes static_gate_report.md)
├── SUBTASK_deploy_reach/_BRIEF.md      (Group 1 — deps static_gate; cluster deploy + reachability evidence)
├── SUBTASK_land_pr/_BRIEF.md           (Group 2 — deps static_gate, deploy_reach; git commit + PR into main)
└── SUBTASK_fold/_BRIEF.md              (Group 3 — deps all; author ../SYNTHESIS.md + fold the subtree)
```

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_static_gate` | (none intra-subtree) | Read-only four-check over the combined `deploy/chirp/*` + `deploy/argocd/*` manifests and the parent contract identities: assert every statically-checkable identity (digest-pinned; Service selector/targetPort; Ingress wiring+class; requests/limits + liveness/readiness; Application wired to `deploy/chirp`+AppProject; AppProject least-privilege no `*/*/*`; namespace isolation; no committed secrets), plus wiring (no dead manifest), duplication (disjoint producers), and a focused k3s/ArgoCD + security review. Go/no-go before any cluster touch. | `outputs/static_gate_report.md` |
| `SUBTASK_deploy_reach` | `SUBTASK_static_gate` | Deploy onto the live k3d `nswe` cluster (apply AppProject+Application and/or let ArgoCD sync), handle the private-GHCR imagePullSecret out-of-band, watch the rollout to Synced/Healthy, resolve ImagePullBackOff/probe failures (remediation-as-decomposition if a manifest is wrong), then issue a real HTTP request via the k3d ingress path (`localhost:8081`, recorded Host/path) and capture the response. Assert the runtime identities (endpoints non-empty, Synced/Healthy, HTTP served, no ImagePullBackOff). Reachability shown with evidence. | `outputs/reachability_evidence.md` |
| `SUBTASK_land_pr` | `SUBTASK_static_gate`, `SUBTASK_deploy_reach` | Land the work: create `work/deploy-argocd` from `ada3aa9`, bring `deploy/chirp/` + `deploy/argocd/` onto it cleanly, commit (no attribution trailers), push, open a PR into `main` that `Closes #13` with an accurate body (no trailers), confirm CI is green. Do NOT merge the PR or push `main`. | `outputs/pr_record.md` |
| `SUBTASK_fold` | `SUBTASK_static_gate`, `SUBTASK_deploy_reach`, `SUBTASK_land_pr` | Sub-synthesis / fold: read the three upstream outputs, confirm the full parent contract-identity set is covered (static + runtime) with no silent plug, assemble the decision record, and author `../SYNTHESIS.md` at the deploy-argocd subtree root (PASS/FAIL verdict, per-identity results, reachability evidence, decision record, PR link). Then fold the deploy-argocd subtree to COMPLETED (resume this `SUBTASK_synthesis` node and the `deploy-argocd` root). | `../SYNTHESIS.md` (deploy-argocd subtree root) |

### Dependency Graph

```
SUBTASK_static_gate ──> SUBTASK_deploy_reach ──> SUBTASK_land_pr ──> SUBTASK_fold
        └───────────────────────────────────────────────────────────┘ (fold also deps static_gate)
```

---

## Contract

**Location**: `contracts/` (read-only to every child). **Kind**: `yaml_schema` (output-artifact ownership +
identity-coverage manifest). No frozen interface seam is required — the cut is a fully serialized pipeline,
so every cross-sibling edge is a declared dependency reading the producer's real COMPLETED output, not a
contract-mediated parallel seam. `contracts/_MANIFEST.yaml` records per-child ownership, the identity-coverage
map (which child asserts which parent identity), and the fold obligation; `synthesis_gate_contract.yaml`
fixes the output-artifact locations/schemas the fold composes. The parent identities to assert live in
`../contracts/_MANIFEST.yaml` and are referenced, not duplicated.
