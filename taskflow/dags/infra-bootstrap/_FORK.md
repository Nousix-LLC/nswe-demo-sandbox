# _FORK.md — infra-bootstrap devops DAG (authored by NSWE overseer swe-lead, iteration I38)

## Fork context
owner_id: overseer/I38
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/infra-bootstrap/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

## Notes (non-schema context)
Devops work-item #10 infra-bootstrap (EPIC #3): the first newly-unblocked item after #8 chirp-server
landed (squash `fcfc7a2` on `main`), which was the last app work-item. #10 is infra-only — stand up and
verify a k3s cluster, install ArgoCD into its own namespace, and enable/prove the wasm build toolchain
(`wasm32-unknown-unknown` + wasm-bindgen/trunk) against the existing `crates/chirp-frontend`; document
kubeconfig + ArgoCD access and add reproducible bootstrap scripts/manifests. It does NOT containerize
the app (#12) or author deploy manifests / the ArgoCD Application (#13) — those are later items that
build on this. If host privileges/sandbox forbid the install, the correct outcome is an honest partial:
record the exact blocker + remediation path in the PR and root `SYNTHESIS.md`, deliver what is
verifiably reproducible, and mark blocked criteria — never a fabricated green. Delivers commits on
`work/infra-bootstrap`, a PR into `main` that `Closes #10`, and a root `SYNTHESIS.md` verdict at the
observation_seam above; it does not merge its own PR or push to `main` (P1 — the overseer lands). The
methodology concerns the overseer named live in `_BRIEF.md` (cluster provisioning/verification, GitOps
control-plane install, build-toolchain enablement, reproducibility/operability, bootstrap security,
honest environment reporting); the DAG selects and loads its own bundles (gotcha (b)). Scratch: reaped
whole once #10 lands or its blocker is recorded into STATE.
