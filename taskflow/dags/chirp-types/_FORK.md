# _FORK.md — chirp-types code-writing DAG (authored by NSWE overseer swe-lead, iteration I2)

## Fork context
owner_id: overseer/I2
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-types/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8, methodology: rust+core+architecture }

## Notes (non-schema context)
Work-item of the engagement (issue #7, EPIC #2): the `chirp-types` shared domain model + client<->server API contract crate. Independent of the ferric framework crates (depends only on serde), so it fans out in parallel with ferric-router/#5 and ferric-http/#6. Delivered as a PR into `main`. Methodology bundle IDs selected by the overseer and carried here + in `_BRIEF.md`: rust, core, architecture. The overseer wrote no code; this DAG performs all engineering (decompose → implement → synthesize) and writes the `SYNTHESIS.md` verdict at the observation_seam above.
