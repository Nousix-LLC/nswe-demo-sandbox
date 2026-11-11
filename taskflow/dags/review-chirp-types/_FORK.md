# _FORK.md — chirp-types review DAG (authored by NSWE overseer swe-lead, iteration I14)

## Fork context
owner_id: overseer/I14
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/review-chirp-types/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8, methodology: code-review+rust+architecture }

## Notes (non-schema context)
The human-requested review step of the chirp-types (issue #7) work-item turn: review PR #17 (already machine-gated PASS — see /home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-types/SYNTHESIS.md) against issue #7's acceptance criteria + the code-review/rust/architecture methodologies, post a `gh pr review` (approve / request-changes), and write the APPROVE/REQUEST-CHANGES verdict to the observation_seam above. `architecture` is named deliberately: chirp-types is the SHARED CONTRACT crate consumed by chirp-server (#8) and chirp-frontend (#9), so its public API surface, serde wire stability (field naming, versioning posture), and dependency-light boundary are the load-bearing review concerns. The overseer wrote no code and does not review inline — review is dispatched to this DAG per the user's "code review is a DAG" request (P1 held). The overseer's successor depends on this DAG folding: on APPROVE + green machine verdict it LANDS PR #17 (squash-merge into main, closes #7, --delete-branch) — subject to PR #17 being OPEN/MERGEABLE/CLEAN at land time (a sibling landing may restale its Cargo.lock, requiring a relock remediation DAG first); on REQUEST-CHANGES it remediates (fresh code-writing DAG carrying the findings), budget 2 then escalate. Note: `gh` reviews post as COMMENTED not APPROVED (self-review platform block — author==gh account); the authoritative verdict is the APPROVE/REQUEST-CHANGES in this DAG's SYNTHESIS.md body. Scratch compute: reaped whole once the work-item lands.
