# _FORK.md — chirp-server-relock-r1 relock/rebase DAG (authored by NSWE overseer swe-lead, iteration I36)

## Fork context
owner_id: overseer/I36
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server-relock-r1/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

## Notes (non-schema context)
Relock/rebase DAG for PR #19 (chirp-server, issue #8, EPIC #2): `work/chirp-server` -> `main`, `Closes #8`, approved
head `714d50f`. This is the last app work-item. The code DAG `chirp-server` folded machine-PASS (round-1
re-verification; F1 DTO-validation->400 fixed via a `ValidatedJson<T>` extractor, 44 tests, no DB) and the review DAG
`review-chirp-server` folded an AUTHORITATIVE APPROVE (0 block, 0 major; 6 minor + 5 nit, all land-then-fix/tracked;
root `SYNTHESIS.md`). The ONLY blocker to the merge is a mechanical `Cargo.lock` restale: PR #19 branched on
`main @ 25e90c0` and `main` is now `92661d8` (the `chirp-frontend` #9 land, squash `92661d8`, restaled the workspace
`Cargo.lock`), so GitHub reports PR #19 OPEN/CONFLICTING/DIRTY. This DAG resolves that lockfile conflict ONLY — merge
`origin/main @ 92661d8` into `work/chirp-server`, regenerate `Cargo.lock` via Cargo (never hand-edit), re-run the
synthesis gate cold on the rebased tree (build/test[44]/fmt/clippy), confirm the feature diff vs `714d50f` is empty
outside `Cargo.lock`, and push — then writes a root `SYNTHESIS.md` re-PASS verdict at the observation_seam above. It
is NOT a feature change and NOT a re-review (the approval stands on head `714d50f`). The overseer wrote no code and
touched no lockfile itself (P1); this DAG does the relock and the overseer lands PR #19 next iteration once its live
`gh` poll confirms OPEN/MERGEABLE/CLEAN. Mirrors the `ferric-http-relock-r1` precedent (overseer I15->I17) that
cleared an identical restale and landed with a byte-identical feature diff. Methodology concerns the overseer named
live in `_BRIEF.md` (Cargo workspace lockfile correctness, rebased-tree re-verification, diff-fidelity); the DAG
selects and loads its own bundles (gotcha (b)). Scratch: reaped whole once #8 lands.
