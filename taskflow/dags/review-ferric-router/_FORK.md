# _FORK.md — ferric-router review DAG (authored by NSWE overseer swe-lead, iteration I11)

## Fork context
owner_id: overseer/I11
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/review-ferric-router/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8, methodology: code-review+rust+core }

## Notes (non-schema context)
The human-requested review step of the ferric-router (issue #5) work-item turn: review PR #16 (already machine-gated PASS — see /home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-router/SYNTHESIS.md) against issue #5's acceptance criteria + the code-review/rust/core methodologies, post a `gh pr review` (approve / request-changes), and write the APPROVE/REQUEST-CHANGES verdict to the observation_seam above. The overseer wrote no code and does not review inline — review is dispatched to this DAG per the user's "code review is a DAG" request. The overseer's successor (overseer/I12) depends on this DAG folding: on APPROVE + green machine verdict it LANDS PR #16 (squash-merge into main, closes #5, --delete-branch); on REQUEST-CHANGES it remediates (fresh code-writing DAG carrying the findings), budget 2 then escalate. Note: `gh` reviews post as COMMENTED not APPROVED (self-review platform block — author==gh account); the authoritative verdict is the APPROVE/REQUEST-CHANGES in this DAG's SYNTHESIS.md body. Scratch compute: reaped whole once the work-item lands.
