# _FORK.md — ferric-http review DAG (authored by NSWE overseer swe-lead, iteration I12)

## Fork context
owner_id: overseer/I12
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/review-ferric-http/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8, methodology: code-review+rust+core }

## Notes (non-schema context)
The human-requested review step of the ferric-http (issue #6) work-item turn: review PR #15 (already machine-gated PASS — see /home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-http/SYNTHESIS.md) against issue #6's acceptance criteria + the code-review/rust/core methodologies, post a `gh pr review` (approve / request-changes), and write the APPROVE/REQUEST-CHANGES verdict to the observation_seam above. The overseer wrote no code and does not review inline — review is dispatched to this DAG per the user's "code review is a DAG" request (P1 held). The overseer's successor (overseer/I13) depends on this DAG folding: on APPROVE + green machine verdict it LANDS PR #15 (squash-merge into main, closes #6, --delete-branch); on REQUEST-CHANGES it remediates (fresh code-writing DAG carrying the findings), budget 2 then escalate. Note: `gh` reviews post as COMMENTED not APPROVED (self-review platform block — author==gh account); the authoritative verdict is the APPROVE/REQUEST-CHANGES in this DAG's SYNTHESIS.md body. Scratch compute: reaped whole once the work-item lands.
