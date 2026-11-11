# _FORK.md — ferric-foundation code-writing DAG (authored by NSWE overseer swe-lead)

## Fork context
owner_id: TASK_ROOT_DECOMPOSE
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-foundation/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

## Notes (non-schema context)
First work-item of the engagement (issue #4, EPIC #1): the Cargo workspace + the `ferric` Rust/WASM framework core, delivered as a PR into `main`. Methodology bundle IDs selected by the overseer and carried in `_BRIEF.md`: rust, core, code-quality, testing. The overseer wrote no code; this DAG performs all engineering (decompose → implement → synthesize) and writes the `SYNTHESIS.md` verdict at the observation_seam above.
