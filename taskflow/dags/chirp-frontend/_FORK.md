# _FORK.md — chirp-frontend code-writing DAG (authored by NSWE overseer swe-lead, iteration I17)

## Fork context
owner_id: overseer/I17
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-frontend/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8, methodology: rust+core+architecture+testing }

## Notes (non-schema context)
Work-item of the engagement (issue #9, EPIC #2): `crates/chirp-frontend` — the chirp Twitter-style client SPA, a client-side WASM app built on the landed `ferric` framework and composing the landed `chirp-types` REST contract. Newly unblocked: its dependencies ferric-router #5 (`cb619e9`), ferric-http #6 (squash `25e90c0`, PR #15, landed by overseer/I17), and chirp-types #7 (`2e32aed`) are all on `main`. This DAG consumes `crates/ferric`, `crates/ferric-router`, `crates/ferric-http`, and `crates/chirp-types` as path-deps / the wire contract (all on `main`). Delivered as a PR into `main` on branch `work/chirp-frontend`, `Closes #9`. Methodology bundle IDs selected by the overseer and carried here + in `_BRIEF.md`: rust, core, architecture, testing. The overseer wrote no code (P1); this DAG performs all engineering (decompose → implement → synthesize) and writes the `SYNTHESIS.md` verdict at the observation_seam above. chirp-server #8 is a parallel in-flight work-item; chirp-frontend does NOT build-depend on it (it calls the REST API at runtime via the chirp-types contract). Scratch: reaped whole once #9 lands (after its own review DAG folds APPROVE and the overseer gates it).
