# _FORK.md — review-epic-persist review DAG (authored by NSWE overseer swe-lead, iteration I58)

## Fork context
owner_id: overseer/I58
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/review-epic-persist/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-reviewer
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

## Notes (non-schema context)
Review DAG for PR #113 ("Durable PostgreSQL persistence for chirp", `work/epic-persist` -> `main`, author
`mattsmcknight`, `Closes #65`/`#66`/`#67`, epic #56; #64 stays open). This PR is OWNER-AUTHORED, not produced
by a code DAG, so there is NO code-DAG `SYNTHESIS.md`; the machine signal is the live CI rollup on the PR:
clippy/fmt/test/wasm PASS, `image` skipping, and `doc` FAILING => mergeState UNSTABLE. The PR is MERGEABLE but
NOT clean to land while the required `doc` check fails. This review DAG renders the authoritative human-landing
APPROVE / REQUEST-CHANGES verdict in its own root `SYNTHESIS.md` at the observation_seam above — the overseer
gates on THAT folded root record. Because reviewer and author share the org/account, `gh pr review --approve`
is rejected; the review posts as a PR comment (carrying the verdict) plus inline comments. The whole of the
review work and the concerns to cover live in `_BRIEF.md`; the DAG selects and loads its own methodologies.
The overseer wrote no code and performed no review itself (P1). Reaped whole once PR #113 lands and the
review's findings are on the board.
