# _BRIEF.md — infra-bootstrap (issue #10, EPIC #3 devops) — swe-coder DAG

You are a `swe-coder` DAG for the `Nousix-LLC/nswe-demo` engagement. Deliver **work-item #10
infra-bootstrap** as commits on a feature branch and a PR into `main`, with a root `SYNTHESIS.md`
verdict. You evaluate your own scope (Atomic vs decompose), choose and load your own methodologies,
and run your own machine gate. This brief is your whole task spec; it describes the objective and the
concerns to cover — it does not prescribe a method or a decomposition.

## Objective
Bootstrap the deployment environment this engagement's continuous delivery will run on, and prove it
is ready: a **k3s** cluster, **ArgoCD** installed into it (own namespace), and the **wasm build
toolchain** (`wasm32-unknown-unknown` target + wasm-bindgen / trunk) available. This is the
infrastructure foundation the later devops items (#11 CI, #12 containerize, #13 deploy-argocd) build
on; it is **infra-only** — it stands up and documents the environment, it does not containerize the
app or author deployment manifests (those are #12 and #13).

Closes issue **#10** (`infra-bootstrap: k3s cluster + ArgoCD + wasm toolchain`).

## Acceptance criteria (testable)
- A **k3s** cluster is installed/verified and reachable; `kubectl get nodes` shows a Ready node, and
  the exact command/path to obtain kubeconfig access is documented.
- **ArgoCD** is installed into its own namespace (e.g. `argocd`) and its core workloads reach Ready;
  how to reach the ArgoCD API/UI and retrieve the initial admin credential is documented (without
  committing any secret to the repo).
- The **wasm toolchain** is present and proven: `rustup target add wasm32-unknown-unknown` is in place
  and a wasm build of the existing `crates/chirp-frontend` (via trunk or wasm-bindgen, as the repo
  already uses) succeeds; the exact toolchain versions are recorded.
- Any **bootstrap scripts / declarative install manifests** you add are reproducible and safe to
  re-run (idempotent where feasible), committed under a sensible path (e.g. `deploy/bootstrap/` or
  `scripts/`), and documented with a short runbook (prerequisites, run order, verification).
- If **host privileges or sandbox constraints block** the k3s/ArgoCD install (no root, no systemd, no
  network to the install endpoints, etc.), do **not** fake success: record the **exact blocker**
  (command, error, environment fact) and a concrete **remediation path** in the PR body and in
  `SYNTHESIS.md`, deliver whatever is verifiably reproducible (the scripts/manifests + the toolchain
  portion that does work), and mark the blocked criteria clearly. A clean, honest partial with a
  precise blocker is the correct outcome when the environment forbids the install — not a fabricated
  green.

## Inputs
- The repo at `main @ fcfc7a2` (full ferric framework + chirp app landed and green: `crates/ferric*`,
  `crates/chirp-types`, `crates/chirp-server`, `crates/chirp-frontend`; workspace builds, tests, fmt,
  clippy all clean as of the #8 land).
- `crates/chirp-frontend` is the existing wasm SPA — use it as the concrete wasm-build proof target;
  do not modify its source for this item.
- The engagement's deploy intent (STATE architecture): chirp-server containerized; k8s manifests under
  `deploy/`; an ArgoCD Application tracking this repo deploys to k3s; the app must end up reachable.
  #10 lays the ground for that; it does not implement the deploy itself.

## Declared output
- Commits on branch **`work/infra-bootstrap`** (create it off `main`).
- A **PR into `main`** that closes #10, with a body summarizing what was installed/verified, the
  kubeconfig + ArgoCD access runbook, toolchain versions, and (if applicable) the exact blocker +
  remediation path.
- A root **`SYNTHESIS.md`** at your DAG root carrying the machine-gate verdict (PASS, or an honest
  PASS-with-documented-blocker), the acceptance-criteria results, and your decision record.
- Do **not** merge your own PR and do **not** push to `main`.

## What to evaluate / concerns to cover (named as distinct concerns)
Decide the methodologies for these yourself through the methodology loader; cover them as separate
concerns, not as one:
- **Cluster provisioning & verification** — a correct, reproducible k3s install and a real readiness
  check, not an assumed one.
- **GitOps control-plane install** — ArgoCD into its own namespace, healthy, with documented access;
  readiness for a later `Application` (#13) without pre-building that Application here.
- **Build-toolchain enablement** — the wasm target + wasm-bindgen/trunk, proven against the real
  frontend crate, with pinned/recorded versions.
- **Reproducibility & operability** — idempotent, re-runnable bootstrap; a clear runbook; sane paths.
- **Security of the bootstrap** — no secrets committed; least-privilege/RBAC posture for ArgoCD; how
  credentials are obtained at runtime rather than stored in the repo.
- **Honest environment reporting** — precise blocker capture + remediation if the host forbids the
  install, versus a verified-green claim.

## Constraints
- Repo scope: **only** `Nousix-LLC/nswe-demo`, and only this project's k3s cluster / namespaces /
  ArgoCD. Touch no sibling repo and no unrelated cluster.
- Branch `work/infra-bootstrap`; PR into `main`. **Never** force-push `main` or rewrite merged history.
- Add **no attribution trailers** to commits.
- Do not commit secrets, kubeconfigs with live credentials, or tokens.
