# _GLOBAL.md — deploy-ghcr-auth-r2 (subtree hub)

## Project Context

**Status**: Active (devops DAG; F1 deploy **attempt #2 of 2**).

### Objective
Verify and, where reachable, **complete** the live reachability of Chirp running on its **committed
digest** for `Nousix-LLC/nswe-demo`, and reconcile the running cluster with the committed GitOps
desired state — held to the acceptance criteria of **issue #32**. Deliverables: a root `SYNTHESIS.md`
recording what is deployed at which commit, the AC1–5 results, **how it was verified live**, and any
external input still required; plus a PR on `work/deploy-ghcr-auth-r2` into `main` for any repository
change the fix needs (carrying `Closes #32` **iff** live reachability is actually achieved and verified).

### What changed since attempt #1 (evaluate on a fresh clock)
- Owner acted directly on `main`: commit **`c805525`** added a **host-less ingress rule** to
  `deploy/chirp/30-ingress.yaml`, so Chirp is reachable by the cluster's external (tailnet) address for any
  Host, alongside the existing `chirp.localhost` host rule. `main` HEAD is now `c805525`. This addresses
  north-south **reachability**; it does **not** by itself resolve the image pull.
- The prior escalation issue was closed; the `read:packages` credential was never supplied through the
  prior ask. The owner may have resolved the pull **out of band** (created a `ghcr-pull` Secret, or flipped
  the GHCR package public) without saying so. **Test the live world first; do not assume it is still blocked.**

### Prior verdict (attempt #1 — `taskflow/dags/deploy-ghcr-auth/SYNTHESIS.md` + `FAILURE.md`) — do NOT re-tread
Confirmed-live last time: the committed-digest pod was in `ImagePullBackOff` (no `ghcr-pull` Secret; the only
local token lacked `read:packages`); a stale `chirp:local` pod masked the outage as the sole Service endpoint;
ArgoCD was Synced@`22d2df6` but Health=Degraded. Ruled out then (do **not** retry blindly): the local `gh`/docker
token cannot pull GHCR (403) and cannot flip package visibility (no `read:packages`); anonymous pull is 403
(private); non-interactive `gh auth refresh` is a device flow; `docker pull` + `k3d image import` is non-durable
and fails the operability bar. PR #30 landed the pull-auth runbook into `deploy/chirp/README.md`.

### Success Criteria (issue #32 — the subtree's bar)
1. `chirp-server` pod runs the **committed digest**, `1/1 Ready`; stale local-image ReplicaSet scaled to `0`.
2. ArgoCD `Application chirp` **Synced and Healthy** at the integration-branch head.
3. `GET /healthz` → `200` served by the **committed-digest** pod (not the stale pod), through the ingress.
4. The fix **survives ArgoCD selfHeal/prune**.
5. Supply-chain / least-privilege posture preserved: digest pin unchanged, no registry secret committed to the
   repo, no broad RBAC, ArgoCD project scope unchanged.

## Constraints and Requirements (inherited by the whole subtree)

- **Scope**: `Nousix-LLC/nswe-demo` plus this project's own k3s cluster/namespaces (`chirp*`) and its own ArgoCD
  Application `chirp`. Do **not** touch other namespaces or other ArgoCD applications.
- **Change through the repo where GitOps owns desired state; repository changes land as reviewed PRs.** The
  overseer reads the live system and lands/merges; this subtree changes the cluster and opens the PR.
- **Host/cluster access** (SSH to the build server for `kubectl`/`helm`/`k3d`, the k3d LB serving port, context
  `k3d-nswe`, namespace `chirp`, ArgoCD ns `argocd`) is in the **repo checkout's `CLAUDE.md`** — read and follow it.
  The repo checkout is a **separate directory** from this taskflow workspace (prior attempt used `~/nswe-demo`);
  each executing child establishes its own checkout per `CLAUDE.md`.
- **Never** commit a secret or registry credential to the repo. **Never** force-push `main` or rewrite merged
  history. **No attribution trailers** on commits or PR bodies.
- **GitHub output carries no host/system facts** — no server address, SSH key path, user name, host paths, or
  taskflow internals in any issue, PR, commit, or comment. Translate host facts to repository identities before
  anything goes on GitHub. (Taskflow state files here stay in the working environment and may carry working facts.)

## Methodology

This subtree boots into the `software` methodology bundle. Per-child bundle IDs are propagated in each
`_BRIEF.md`; see the posture below.

### Subtree Methodology Posture
- **Dominant task type**: GitOps deployment reconcile-and-verify (a deploy-fix-and-verify / incident-repair shape).
  Rough split: one live-diagnosis task (GitOps + Kubernetes reads), one remediation task (GitOps secrets +
  Kubernetes-security + reconciliation + PR), one verification/synthesis gate.
- **Primary bundles the subtree draws on**: `gitops`, `kubernetes`, `kubernetes-security`, `operations`,
  `security`, and `synthesis` (for the gate). Children SHOULD assume these are in scope for their task type
  without re-justifying.
- **Cross-cutting bindings (every leaf)**: supply-chain / least-privilege posture (AC5) and the
  "change through the repo, host facts never reach GitHub" constraints bind every descendant.
- Suggestion, not prescription: each child is the final judge of what it actually loads.

## Task Structure

### Overview
```
_GLOBAL.md (this hub)                         narrative: why, scope, chosen-cut rationale
├── contracts/_MANIFEST.yaml                  deployment-identity constants + diagnosis schema + AC/posture identities (READ-ONLY)
├── SUBTASK_diagnose/_BRIEF.md                observe & diagnose the fresh live world → diagnosis.md
├── SUBTASK_remediate/_BRIEF.md               the change only: reconcile to desired state (+ PR if a repo change is needed)
└── SUBTASK_verify_synthesis/_BRIEF.md        verification gate + root SYNTHESIS.md (the fold record)
```

### Chosen-cut rationale
Candidate cuts considered: **(A) by concern** — four parallel spokes (reachability / image-pull / gitops-drift /
ops). **Rejected**: fails ownership-disjointness (all four operate on one mutable live cluster and the same
manifests), the concerns are causally chained (reachability depends on the digest pod pulling; selfHeal-survival
is the mechanism, not a separate work item), and none is input-complete without first reading fresh live state.
**(B) serial pipeline** diagnose → remediate → verify/synthesize (the bugfix/verification shape's
precursor → transform → synthesis/verify). **Chosen**: each child discharges one responsibility (observe / change /
judge), owns a disjoint output, and the serial edges are genuine dataflow. The four named concerns are
cross-cutting threads woven through all three stages, verified at the gate — not separable parallel tasks.

**Verdict placement — Shape B (gate-concentrated).** Single remediation child; the AC1–5 live verdict is NOT
produced inside the remediate task (change/verify split). It folds into `SUBTASK_verify_synthesis`, the hub gate,
which runs the executable checks and authors the root `SYNTHESIS.md`. Rationale recorded here per the bugfix-shape
methodology: one fix child + the verdict already needs the gate's `SYNTHESIS.md` deliverable → concentrate.

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_diagnose` | none | Read the fresh live cluster + repo state; diagnose the gap and pick the decision branch (already-working / create-Secret / blocked) | `SUBTASK_diagnose/diagnosis.md` |
| `SUBTASK_remediate` | `SUBTASK_diagnose` | The change only: bring the live deployment to the committed desired state through the repo/GitOps (create least-privilege `ghcr-pull` Secret iff a credential is now reachable; reconcile drift; ensure stale RS → 0); open a PR on `work/deploy-ghcr-auth-r2` iff a repo change is needed (without `Closes #32`) | `SUBTASK_remediate/remediation.md` (+ optional PR) |
| `SUBTASK_verify_synthesis` | `SUBTASK_diagnose`, `SUBTASK_remediate` | **Verification gate**: confirm live reachability at both ingress routes and AC1–5 with executed checks; confirm selfHeal survival; finalize the PR's `Closes #32` wording iff verified; author the root `SYNTHESIS.md` fold record | `SYNTHESIS.md` (at this subtree root — the fold location) |

### Dependency Graph
```
SUBTASK_diagnose ──▶ SUBTASK_remediate ──▶ SUBTASK_verify_synthesis
         └───────────────────────────────▶ (also an input to the gate)
```

## Contract

**Location**: `contracts/` (read-only for every descendant). **Kind**: `yaml_schema`.
The children are a serial pipeline (each edge is a cross-group dependency, serialized by structure — each
consumer reads its producer's real output), so no seam needed freezing for parallelism. The contract is the
required thin seam: it freezes the **shared deployment-identity constants** (forced, stable, referenced
identically by all three children), the **`diagnosis.md` schema** the remediate and gate children consume, and
the **AC / supply-chain identities** the synthesis gate enumerates and runs. Prose rationale lives here; the
machine-readable structure lives in `contracts/_MANIFEST.yaml`. Full contract-layer semantics: the Contract Layer
module. Identities are additive at the gate; the synthesis child attaches the contract-verification methodology
because at least the identity set is frozen.

## Output Specifications

| Deliverable | Owner | Location | Description |
|-------------|-------|----------|-------------|
| `diagnosis.md` | `SUBTASK_diagnose` | `SUBTASK_diagnose/` | Fresh live-state snapshot + gap diagnosis + decision branch |
| `remediation.md` (+ optional PR) | `SUBTASK_remediate` | `SUBTASK_remediate/` | What was changed (or why no change / why blocked); PR link if any |
| `SYNTHESIS.md` | `SUBTASK_verify_synthesis` | this subtree root | AC1–5 verdict, live-verification evidence, external input still required; the fold record |
