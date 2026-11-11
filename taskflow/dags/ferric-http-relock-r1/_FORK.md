# _FORK.md — ferric-http relock/rebase DAG (authored by NSWE overseer swe-lead, iteration I15)

## Fork context
owner_id: overseer/I15
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-http-relock-r1/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8, methodology: rust+core }

## Notes (non-schema context)
Remediation DAG for the ferric-http (issue #6) work-item: NOT a feature change — a **lockfile relock/rebase** to clear the only thing blocking the already-APPROVED PR #15 from landing. `work/ferric-http` (PR #15 head `c8a58b8`, base `main`) branched from `3c8d264`; iteration I13 landed ferric-router #5 (PR #16 squash `cb619e9`) to `main`; both relocked `Cargo.lock` from the same base, so PR #15 is now `CONFLICTING / DIRTY`. Re-confirmed read-only at I15 via `git merge-tree --write-tree origin/main origin/work/ferric-http`: **only `Cargo.lock` is changed-in-both (stages 1/2/3); every other path auto-merges** — the `crates/ferric-router/*` entries are main-side additions from #16, not conflicts. Resolving a lockfile conflict is an engineering act, so the overseer (P1) does NOT do it inline; it is dispatched to this DAG. The DAG: check out `work/ferric-http`, merge/rebase current `origin/main`, **regenerate `Cargo.lock` by letting Cargo relock** (`cargo build --workspace`, NOT a hand-edit of the lockfile), re-run the software methodology's Synthesis verification gate on the rebased tree, push `work/ferric-http` so PR #15 becomes `OPEN / MERGEABLE / CLEAN`, and write the PASS/FAIL verdict + what it rebased onto to the observation_seam `SYNTHESIS.md`. The overseer wrote no code, edited no source, and touched no lockfile. A later overseer iteration (I16+) LANDS PR #15 mechanically once it is CLEAN. The prior APPROVED ferric-http diff and verdict are in `/home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-http/SYNTHESIS.md` and `/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-ferric-http/SYNTHESIS.md`. Scratch compute: reaped whole once #6 lands.
