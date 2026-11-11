# _FORK.md — ferric-foundation review DAG (authored by NSWE overseer swe-lead, iteration I1)

## Fork context
owner_id: overseer/I1
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/review-ferric-foundation/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8, methodology: code-review+rust+core }

## Notes (non-schema context)
The human-requested review step of the ferric-foundation (issue #4) work-item turn: review PR #14 (already machine-gated PASS) against issue #4's acceptance criteria + the code-review/rust/core methodologies, post a `gh pr review` (approve / request-changes), and write the APPROVE/REQUEST-CHANGES verdict to the observation_seam above. The overseer wrote no code and does not review inline — review is dispatched to this DAG per the user's "code review is a DAG" request. The overseer's successor (overseer/I2) depends on this DAG folding: on APPROVE + green machine verdict it LANDS PR #14 (squash-merge into main, closes #4); on REQUEST-CHANGES it remediates (fresh code-writing DAG carrying the findings). Scratch compute: reaped whole once the work-item lands.
