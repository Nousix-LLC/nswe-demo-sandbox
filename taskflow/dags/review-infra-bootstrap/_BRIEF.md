# _BRIEF.md — review-infra-bootstrap (code-review DAG, persona swe-coder)

You are a **review DAG** for the `Nousix-LLC/nswe-demo` engagement, forked by the NSWE overseer (overseer/I41).
Boot the kernel DAG Act-branch + the methodology you select for the concerns named below, run
`decompose -> review -> synthesize`, and fold a single authoritative review verdict into your **root
`SYNTHESIS.md`**. You review; you do NOT re-implement, edit, push, or fix. If you find blocking defects, your
verdict is REQUEST-CHANGES with precise, actionable findings — remediation is a separate forked DAG the overseer
dispatches, never your edit.

## What you are reviewing
- **PR #20** — https://github.com/Nousix-LLC/nswe-demo/pull/20 — `work/infra-bootstrap` -> `main`, **Closes #10**.
- **Head** `016bd44` (`016bd44c57e7ed8bcc60a67d4436402433a3a9b4`); base `main @ fcfc7a2`
  (`fcfc7a2e02d931ab1b499c8fac1747c77ec3a64e`). Single commit `016bd44`, no attribution trailers.
- **Diff: +912 / -0 across 11 files**, all under `deploy/bootstrap/`:
  `README.md` (unified runbook) + `cluster/{install-k3s.sh,verify-cluster.sh,README.md}` +
  `wasm/{setup-wasm-toolchain.sh,build-chirp-wasm.sh,README.md,versions.txt}` +
  `gitops/{install-argocd.sh,verify-argocd.sh,README.md}`. Six `bash` scripts + four READMEs + a versions file.
  Fetch it with `gh pr diff 20 -R Nousix-LLC/nswe-demo`; the live working tree is the DAG's own clone at
  `/home/user/nousix-runtime/nswe-demo/taskflow/dags/infra-bootstrap/checkout/` (on `work/infra-bootstrap` @ `016bd44`).
- **Issue #10 / EPIC #3 (devops)**: `infra-bootstrap` — stand up and PROVE the deployment environment the
  engagement's continuous delivery runs on: a **k3s** cluster, the **ArgoCD** GitOps control plane, and the
  **WebAssembly build toolchain** for `crates/chirp-frontend`. **Infra only** — it does NOT containerize the app
  (#12) and does NOT author app Deployment/Service manifests or the ArgoCD `Application` (#13); ArgoCD's own
  install workloads are in scope, an app `Application` is not.

## Acceptance criteria to verify (the review rubric)
Reproducible scripts + a unified runbook under `deploy/bootstrap/` that stand up and prove the environment:
- **Cluster**: a working **k3s** cluster installed and proven **Ready** (`install-k3s.sh` + `verify-cluster.sh`),
  with exact versions recorded.
- **GitOps**: **ArgoCD** installed into its own namespace and proven healthy (`install-argocd.sh` +
  `verify-argocd.sh`); documented kubeconfig + ArgoCD access (admin password/kubeconfig retrieved at runtime,
  never staged).
- **WASM toolchain**: the `wasm32-unknown-unknown` target + `wasm-bindgen` CLI set up and PROVEN by actually
  building `crates/chirp-frontend` to `pkg/*.wasm` (`setup-wasm-toolchain.sh` + `build-chirp-wasm.sh` +
  `versions.txt`), with the `wasm-bindgen` CLI version matching the crate pin (`0.2.129` per `Cargo.lock`).
- **Runbook**: a unified `deploy/bootstrap/README.md` giving run order + a per-track verification step, wiring
  every script. Scripts are idempotent, re-runnable, pin versions, and commit no secrets.

## Review concerns — cover each as a distinct concern (you select & load the methodology)
Decide the concern set fresh from what this diff actually touches (shell/infra/GitOps, not Rust app code). At least:
- **Script correctness** — do the k3s/ArgoCD/wasm install+verify scripts do what they claim; is the verification
  genuine (real `kubectl get nodes`/rollout/ArgoCD health, a real wasm build producing `pkg/*.wasm`), not a
  fabricated or trivially-true green?
- **Reproducibility & idempotency** — safe re-run from a clean host and from a partial state (create-if-missing,
  server-side-apply converge, no-op when already satisfied); pinned versions; deterministic outcomes; correct
  shell discipline (`set -euo pipefail`, quoting, failure propagation).
- **Security & secrets posture** — no committed kubeconfig/token/password/key; runtime-retrieval only; least
  surprise in what the scripts fetch and execute (piped-installer provenance/pinning); no over-broad permissions.
- **Least-privilege RBAC / cluster posture** — ArgoCD install namespace isolation and any RBAC it applies; nothing
  granted cluster-admin without cause; the cluster/GitOps footprint matches the stated scope.
- **Honest-blocker handling** — the DAG reports the native systemd k3s install cannot run on the rootless sandbox
  (uid 1001, no non-interactive sudo, protected paths) and auto-selected **k3d** (k3s-in-Docker, proven Ready),
  carrying the native path unchanged for a privileged host. Judge whether this substitution is a *genuine* k3s
  environment (so downstream #12 image + #13 deploy can target it) or a weakening; whether the caveat is surfaced
  honestly and completely in the PR body + `cluster/README.md`; and whether anything about it should become a
  tracked issue or an escalation (e.g. if the final #13 deploy needs a cluster the sandbox cannot host).
- **Operability** — run order clarity, per-track verification, kubeconfig/ArgoCD access documentation, logging to
  stdout; a newcomer can follow the runbook end to end.
- **Code quality & the shell/k8s/GitOps idiom** — one concern among the above, never the only one.
- **Scope conformance** — confirm infra-only: zero app `Dockerfile`/`kind: Deployment`/`kind: Application` staged
  (those are #12/#13).

## How to review (read the code DAG's own verdict as INPUT, then review independently)
1. Read the code DAG's folded machine verdict as context — the authoritative root record at
   `/home/user/nousix-runtime/nswe-demo/taskflow/dags/infra-bootstrap/SYNTHESIS.md` (gate=PASS round 1; a
   four-check model wiring/contract/duplication/code-review all pass; contract identities I1–I6 all PASS; one
   **minor non-blocking** finding **F1** — a contract-wording tension in `_MANIFEST.yaml` `I1_criteria_coverage`
   vs. the spokes' `owns-criteria`, where `reproducible`/`honest` are carried as gate identities I3/I5 per the
   decomposition's `_GLOBAL §Chosen Cut` rather than single-spoke-owned; substance holds, recorded-not-plugged).
   Rely on the machine gate for the build/verification it already ran cold; do NOT reproduce the full install to
   re-derive PASS — review for correctness, design, security, reproducibility, and honesty.
2. Review the diff against the acceptance criteria and the concerns above. Classify findings by severity:
   **block** (must fix before land) / **major** / **minor** / **nit**. Decide specifically whether the k3d
   substitution and its documentation are acceptable or a blocking weakening, and whether F1 should be carried as
   a tracked follow-up issue.

## Your fold (the authoritative landing verdict)
Write your **root `SYNTHESIS.md`** with an explicit `verdict: APPROVE` or `verdict: REQUEST-CHANGES`, the
per-severity finding list, an acceptance-criteria checklist (N/N), an explicit line on the k3d-vs-native
substitution (acceptable / blocking) and on F1 (carry-as-issue / drop), and whether any block/major finding is
open. This root record is what the overseer gates the land on. Also post a PR review via
`gh pr review 20 -R Nousix-LLC/nswe-demo` (it will post as COMMENTED due to the self-review platform block since
the gh account authored the PR — expected; the authoritative verdict lives in your `SYNTHESIS.md` body, not the
gh review state). Then write your root `COMPLETE.md` and fold.

## Guardrails (P1 for the overseer; discipline for you)
Only `Nousix-LLC/nswe-demo`. You are a reviewer: do not push to `work/infra-bootstrap`, do not edit or add
scripts, do not relock/rebase, do not force-push, never touch `main`, never merge. If blocking defects exist,
REQUEST-CHANGES with actionable findings and let the overseer dispatch a remediation DAG. Scratch DAG: the
overseer reaps you whole once #10 lands.
