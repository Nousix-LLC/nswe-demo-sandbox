# _FORK.md — chirp-server code-writing DAG (authored by NSWE overseer swe-lead, iteration I16)

## Fork context
owner_id: overseer/I16
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8, methodology: rust+core+architecture+testing }

## Notes (non-schema context)
Work-item of the engagement (issue #8, EPIC #2): `crates/chirp-server` — the axum REST API + persistence + static SPA serving backend for the chirp Twitter-style app. Newly unblocked: its only dependency, `chirp-types` (#7), LANDED to `main` at I16 (squash commit `2e32aed`, PR #17). This DAG consumes `crates/chirp-types` as the shared contract (it is on `main`). Delivered as a PR into `main` on branch `work/chirp-server`, `Closes #8`. Methodology bundle IDs selected by the overseer and carried here + in `_BRIEF.md`: rust, core, architecture, testing (testing added for API integration tests). The overseer wrote no code (P1); this DAG performs all engineering (decompose → implement → synthesize) and writes the `SYNTHESIS.md` verdict at the observation_seam above. Scratch: reaped whole once #8 lands (after its own review DAG folds APPROVE and the overseer gates it).
