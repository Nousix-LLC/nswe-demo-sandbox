# _BRIEF.md — review-ci-actions-r3 (persona swe-coder, forked by overseer/I46)

## Objective
Perform a **fresh, independent code review** of **PR #21** — "CI: GitHub Actions for the Rust/WASM workspace (#11)" —
in `Nousix-LLC/nswe-demo`, at its **remediated head `716817bcac7d669169a4339b0d15005a1eca7e15`** (branch
`work/ci-actions`, base `main @ 61f924afa2a31d4d92c214c89b48e0ee6fc4e394`). This is review **round 2** for issue #11:
a prior review (`review-ci-actions-r2`) returned **REQUEST-CHANGES** on a single robustness major (**IMG-1**), and a
remediation (`remediate-ci-actions`) has since reshaped the `image` job. Your job is to decide, independently, whether
the PR is now fit to land. Render your verdict — **APPROVE** or **REQUEST-CHANGES** — in your root `SYNTHESIS.md`
body; that body is the authoritative verdict the overseer gates on (not a posted GitHub review, not a side-effect).

This is a review DAG: **read-only against the repository** (P1). You may read the diff, the tree, CI run results,
and PR metadata via `gh`/`git`; you MUST NOT push to the branch, merge, modify `main`, or edit source. If you post
anything to GitHub, post at most a non-authoritative review comment; the real verdict lives in `SYNTHESIS.md`.

## What landing-readiness means here (decide these, as distinct concerns)
Select and load your own review/CI/Rust methodologies; the concerns below are *what to evaluate*, not how.

1. **IMG-1 closure (the verdict-forcing concern from round 1).** Round 1's sole major: the `image` job built the
   `./Dockerfile` (pinned `rust:1.88`) only post-merge on `main`, decoupled from CI's validated Rust `1.97`, so a
   future `Cargo.lock` floor bump could keep PR CI green while breaking the post-merge image publish — a
   green-on-PR / broken-post-merge **drift window**, discovered only on `main`. The remediation claims to close it by
   running the `image` job **build-only on pull requests** (`push: false`) against the PR **merge ref** (which
   carries `main`'s Dockerfile), so the Dockerfile build becomes a **pre-merge gate**, publishing to GHCR only on
   `main`. **Independently verify** this actually closes the drift window: that the PR-time image build exercises the
   real Dockerfile, fails loudly (not silently skips) on a missing/broken Dockerfile, and that a toolchain-floor
   drift would now fail the PR gate. Confirm the live CI run on head `716817b` shows the `image` job green with
   `push: false` on the PR path.
2. **CI workflow correctness overall.** The `on:` triggers (PR + push to `main` + dispatch), the fmt / clippy /
   test / wasm / doc / image jobs, `--locked` on compiling/build steps, `RUSTDOCFLAGS=-D warnings` on doc, the wasm
   target build, cargo/target caching, and required-check-friendly stable job names (branch-protection contexts).
   Whether any job can pass-on-failure or mask a real failure.
3. **Least privilege / trust boundary on the publish path.** `packages: write` exercised only on the `main` publish
   path and inert on PR builds; GHCR login + digest summary guarded to the publish condition. **Supply-chain items
   SEC-1 (action SHA-pinning) and SEC-2 (provenance/attestation) are owned by issue #24 and are OUT OF SCOPE here —
   do not duplicate them as blocking findings**; note them as already-tracked if relevant.
4. **Testing / verification depth** appropriate to a CI workflow change: is the change self-evidencing (a green
   run on the remediated head), and are the acceptance criteria demonstrably exercised by the workflow?
5. **Workflow / YAML quality and idiom** (GitHub Actions and Rust-toolchain idiom); `actionlint` cleanliness.
6. **Advisory disposition sanity.** The remediation reports folding IMG-2 (dead "Detect Dockerfile" skip branch
   removed → loud failure) and IMG-4 (published digest surfaced), folding DOC-1 into the PR description, and
   deferring WF-1 (pin exact `1.97.0`/`rust-toolchain.toml`), WF-2 (MSRV reconcile), IMG-3 (manual-republish path),
   DOC-2 (README cosmetic, #19-owned). Judge whether these dispositions are reasonable or whether any deferral
   should actually block.
7. **Scope & cleanliness.** The remediation changed exactly one file (`.github/workflows/ci.yml`, ~+38/−30); `main`
   and the `./Dockerfile` untouched so PR #21 stays **MERGEABLE/CLEAN**; `Closes #11` linkage intact; no attribution
   trailers on the commit or PR. Confirm these hold on the live head.

## Issue #11 acceptance criteria (confirm each is MET on head `716817b`)
1. Runs on PR + push to `main`. 2. `cargo fmt --check`. 3. `cargo clippy -D warnings`. 4. `cargo test`.
5. Build the WASM frontend. 6. On `main`, build + push the chirp-server image to GHCR. 7. Cache cargo/target.
8. Required-check-friendly job names. 9. Delivered as a PR into `main`.
Round 1 judged all nine MET; the remediation claims no regression. Verify independently; a verdict of
REQUEST-CHANGES should rest on a genuine blocking/major concern, not a durability nit.

## Inputs / context (read-only)
- Live PR #21 @ head `716817b` (diff, tree, PR metadata, CI run **37720238038**) via `gh`/`git`.
- Prior round context (for continuity, not to re-litigate settled MET criteria):
  - `/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-ci-actions-r2/SYNTHESIS.md` — round-1 REQUEST-CHANGES
    (IMG-1 + advisory minors/nits).
  - `/home/user/nousix-runtime/nswe-demo/taskflow/dags/remediate-ci-actions/SYNTHESIS.md` — the remediation's
    machine-PASS record and IMG-1 closure claim.
- Repo clone / worktree: use a read-only checkout of head `716817b`; do not push.

## Output (the fold)
A root `SYNTHESIS.md` at this DAG's workspace root whose body carries: the **verdict** (APPROVE / REQUEST-CHANGES),
severity-classified findings (block / major / minor / nit), the reviewed head (must equal the live PR head), a
per-criterion acceptance table, and an explicit **IMG-1 closed? (yes/no)** determination. If APPROVE and PR #21 is
OPEN/MERGEABLE/CLEAN, the overseer will land #11. If REQUEST-CHANGES, name the specific required change(s) so a
bounded remediation (this would be the last of the 2-budget) can address them.

## Guardrails
Scope limited to reviewing PR #21 in `Nousix-LLC/nswe-demo`. Read-only on the repo (P1): no push, no merge, no
`main` change, no source edit, no force-push, no history rewrite, no attribution trailers. The authoritative verdict
is your root `SYNTHESIS.md` body (gotcha g/i), not a posted review or any side-effect.
