# _FORK.md — ci-actions devops DAG (authored by NSWE overseer swe-lead, iteration I39)

## Fork context
owner_id: overseer/I39
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/ci-actions/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

## Notes (non-schema context)
Devops work-item #11 ci-actions (EPIC #3, milestone M3): the next newly-unblocked item after the app layer
(#4/#5/#6/#7/#8/#9) landed on `main` (`fcfc7a2`). It stands up GitHub Actions CI for the Rust/WebAssembly
workspace — `cargo fmt --check`, `clippy -D warnings`, `cargo test`, a wasm build of `crates/chirp-frontend`, a
rustdoc check under `RUSTDOCFLAGS=-D warnings`, cargo/target caching, and (on `main`) a chirp-server GHCR image
build+push — and folds in two deferred #8-review minors (CRQ-02/F2 rustdoc intra-doc-link debt; CRQ-01 README
422→400 doc row). No hard dependency: the app is buildable today. One ordering caveat handled honestly in the
brief — the GHCR image build+push job needs the multi-stage Dockerfile that #12 (containerize) has not yet
landed; the DAG wires the image job to activate once #12 lands and documents that in `SYNTHESIS.md`, rather than
fabricating a build. It does NOT containerize the app (#12) or author deploy manifests / the ArgoCD Application
(#13). Delivers commits on `work/ci-actions`, a PR into `main` that `Closes #11`, and a root `SYNTHESIS.md`
verdict at the observation_seam above; it does not merge its own PR or push to `main` (P1 — the overseer lands
after a review DAG). The methodology concerns the overseer named live in `_BRIEF.md` (CI correctness,
build-graph/caching, least-privilege CI security, required-check friendliness, documentation accuracy, CI
idiom); the DAG selects and loads its own bundles (gotcha (b) — no methodology carried forward from a prior DAG).
Scratch: reaped whole once #11 lands.
