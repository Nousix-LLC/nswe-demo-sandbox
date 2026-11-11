# _FORK.md — review-chirp-server review DAG (authored by NSWE overseer swe-lead, iteration I33)

## Fork context
owner_id: overseer/I33
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/review-chirp-server/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8, methodology: code-review+rust+architecture+testing }

## Notes (non-schema context)
Review DAG for PR #19 (chirp-server, issue #8, EPIC #2): `work/chirp-server` -> `main`, `Closes #8`, head `714d50f`. The code-writing DAG `chirp-server` folded machine-PASS at round 1 of re-verification: its `SUBTASK_reverify_gate` overwrote the interim round-0 FAIL and wrote the AUTHORITATIVE root `SYNTHESIS.md` (gate=PASS; the single round-0 blocker F1 — DTO-validation surfacing as 422 plain-text instead of the contract's 400 `ApiError{VALIDATION_ERROR,details}` — was fixed by `SUBTASK_fix_validation_error_mapping` [commit `714d50f`/`714d50f6`] via a `ValidatedJson<T>` custom extractor, re-verified cold: build/test[44]/fmt/clippy/wiring/contract/duplication/code-review all pass, no DB). This review DAG renders the authoritative human-landing APPROVE / REQUEST-CHANGES verdict in its own root `SYNTHESIS.md` — the overseer gates the land on THAT folded root record, not on the gh review state (self-review platform block posts COMMENTED) and not on the code DAG's machine gate alone. The overseer wrote no code and performed no review itself (P1); this DAG performs the review (decompose -> review -> synthesize) and writes the `SYNTHESIS.md` verdict at the observation_seam above. Methodology concerns the overseer named (carried in `_BRIEF.md`; the DAG selects/loads its own bundles): code review quality, Rust idiom/soundness, architecture + layering + frozen-contract conformance, and test adequacy. NOTE for the overseer (not the reviewer's concern): PR #19 is currently CONFLICTING/DIRTY because it branched on `main @ 25e90c0` and `main` is now `92661d8` (the #9 land restaled its `Cargo.lock`); that is a mechanical lock restale the overseer clears with a forked relock DAG before landing (after APPROVE), NOT a code defect. Scratch: reaped whole once #8 lands (after this review DAG folds APPROVE, a relock clears the conflict, and the overseer gates PR #19 OPEN/MERGEABLE/CLEAN).
