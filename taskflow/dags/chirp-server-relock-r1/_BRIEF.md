# _BRIEF.md — chirp-server-relock-r1 (clear PR #19's Cargo.lock conflict so the approved change can land)

## Objective
PR [#19](https://github.com/Nousix-LLC/nswe-demo/pull/19) (`work/chirp-server` → `main`, `Closes #8`, head
`714d50f6075416cf8c5f43c8611dcd88c8352ebd`) is **APPROVED to land** — the code DAG folded machine-PASS (round 1
re-verification) and the review DAG `review-chirp-server` folded an authoritative **APPROVE** (0 block, 0 major).
The only thing blocking the merge is a **mechanical `Cargo.lock` conflict**: the branch was cut on `main @ 25e90c0`
and `main` is now `92661d8` (the `chirp-frontend` #9 land restaled the workspace `Cargo.lock`). GitHub reports PR #19
`OPEN / CONFLICTING / DIRTY`.

Your job is to **resolve that lockfile conflict and nothing else**, re-verify that the tree still builds and passes
cold, and push `work/chirp-server` so PR #19 becomes `OPEN / MERGEABLE / CLEAN`. This is a lockfile relock/rebase,
**not** a feature change. The feature source was already reviewed and approved at head `714d50f`; it must not change.

## Acceptance criteria (testable)
1. `work/chirp-server` is merged/rebased onto `origin/main @ 92661d8` with the conflict resolved, so that a PR into
   `main` is mergeable and clean (no remaining conflict markers; `git` reports a clean merge base).
2. The `Cargo.lock` conflict is resolved by **regenerating the lockfile from Cargo** — take `main`'s `Cargo.lock`
   and run `cargo build --workspace` (or `cargo generate-lockfile` + `cargo build --workspace`) so Cargo authors the
   merged lockfile. **Never hand-edit `Cargo.lock`.**
3. The **feature diff is unchanged** from the approved head `714d50f`: the only content difference introduced by this
   work versus `714d50f` is in `Cargo.lock`. No `crates/chirp-server/**` source, test, README, or manifest change.
   Confirm and report the diff of the pushed head against `714d50f` is empty outside `Cargo.lock`.
4. The full machine gate **re-passes cold on the rebased tree**: workspace build, `cargo test -p chirp-server`
   (expect the 44 tests — 24 unit + 20 integration, no DB), `cargo fmt --check`, `cargo clippy -D warnings`. Report
   the exact results.
5. The rebased/relocked `work/chirp-server` is **pushed** to the remote so PR #19 updates. Do **not** merge PR #19
   yourself and do **not** push to `main` — the overseer lands the PR after confirming it is clean.

## Inputs (what you build on)
- PR #19 and its branch `work/chirp-server` at approved head `714d50f`.
- `origin/main @ 92661d8` (the current integration branch; includes the landed `ferric` framework #4/#5/#6,
  `chirp-types` #7, and `chirp-frontend` #9).
- The approved verdict: `taskflow/dags/review-chirp-server/SYNTHESIS.md` (APPROVE) — context only; do not re-review.
- The machine verdict: `taskflow/dags/chirp-server/SYNTHESIS.md` (PASS round 1) — the gate you must reproduce green
  on the rebased tree.
- Precedent: `ferric-http-relock-r1` (overseer I15→I17) cleared an identical `Cargo.lock` restale this same way
  (merge `origin/main`, Cargo relock, re-PASS the gate on the rebased tree, push) and landed with a byte-identical
  feature diff.

## Declared output
- Commits on `work/chirp-server` (the merge/rebase + regenerated `Cargo.lock`), pushed to the remote so PR #19
  reflects them.
- A root `SYNTHESIS.md` at this DAG's root recording: the merge base reached, the lockfile-regeneration method, the
  cold re-verification results (build/test/fmt/clippy), confirmation the feature diff vs `714d50f` is empty outside
  `Cargo.lock`, and the final pushed head SHA. State plainly whether the relock PASSED (tree green, conflict cleared,
  feature unchanged) or FAILED (and why).

## What to evaluate / concerns to cover (named as distinct concerns; you select & load your own methodologies)
- **Rust / Cargo workspace lockfile correctness** — the merged `Cargo.lock` is Cargo-authored, resolves the whole
  virtual workspace, and reflects `main`'s dependency set plus `chirp-server`'s nodes with no spurious version churn.
- **Rebased-tree re-verification** — the workspace builds and `chirp-server`'s full test suite + fmt + clippy pass
  cold on the merged tree, matching the approved machine gate.
- **Diff-fidelity** — the feature code is byte-identical to the approved head `714d50f`; only `Cargo.lock` differs.

## Constraints
- Repo scope: only `Nousix-LLC/nswe-demo`, only branch `work/chirp-server`.
- Never force-push `main`, never rewrite merged history, never merge the PR yourself, add no attribution trailers.
- Never hand-edit `Cargo.lock`; let Cargo regenerate it. This is a relock, not a feature or behavior change.
