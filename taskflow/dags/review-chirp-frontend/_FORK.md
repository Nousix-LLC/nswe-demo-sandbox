# _FORK.md — review-chirp-frontend review DAG (authored by NSWE overseer swe-lead, iteration I29)

## Fork context
owner_id: overseer/I29
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/review-chirp-frontend/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8, methodology: code-review+rust+architecture }

## Notes (non-schema context)
Review DAG for PR #18 (chirp-frontend, issue #9, EPIC #2): `work/chirp-frontend` -> `main`, `Closes #9`, head `b5f7e62`, base `main @ 25e90c0`. The code-writing DAG `chirp-frontend` FOLDED machine-PASS round 1 (root SYNTHESIS.md + COMPLETE.md: 4/4 checks, 7/7 contract identities, 41/41 native tests, 2 non-blocking minors). This review DAG renders the authoritative human-landing APPROVE / REQUEST-CHANGES verdict in its own root SYNTHESIS.md — the overseer gates the land on THAT folded root record, not on the gh review state (self-review platform block posts COMMENTED) and not on the code DAG's machine gate alone. The overseer wrote no code and performed no review itself (P1); this DAG performs the review (decompose -> review -> synthesize) and writes the SYNTHESIS.md verdict at the observation_seam above. Methodology bundle IDs selected by the overseer and carried here + in `_BRIEF.md`: code-review, rust, architecture. Scratch: reaped whole once #9 lands (after this review DAG folds APPROVE and the overseer gates PR #18 OPEN/MERGEABLE/CLEAN).
