# _FORK.md — ferric-http code-writing DAG (authored by NSWE overseer swe-lead, iteration I2)

## Fork context
owner_id: overseer/I2
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-http/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8, methodology: rust+core+code-quality+testing }

## Notes (non-schema context)
Work-item of the engagement (issue #6, EPIC #1): the `ferric-http` fetch-based HTTP/JSON client, built ON TOP of the now-landed `ferric` foundation (PR #14 merged to `main`, squash `3c8d264`, issue #4 closed). Delivered as a PR into `main`. Methodology bundle IDs selected by the overseer and carried here + in `_BRIEF.md`: rust, core, code-quality, testing. The overseer wrote no code; this DAG performs all engineering (decompose → implement → synthesize) and writes the `SYNTHESIS.md` verdict at the observation_seam above.
