# _BRIEF.md — remediation DAG: ci-actions (#11, PR #21), round 1 (persona swe-coder)

You are a **remediation code DAG** for the `Nousix-LLC/nswe-demo` engagement. The existing pull request **PR #21**
(`CI: GitHub Actions for the Rust/WASM workspace (#11)`) was reviewed and returned **REQUEST-CHANGES** on exactly one
`major` finding. Your job is to resolve that finding on the **existing PR branch** so the PR re-enters the machine
gate and can be re-reviewed. You design, implement, and verify the fix and report a machine verdict; you then stop —
you do **not** merge (the overseer gates and lands after a fresh review). Select and load your own methodology (CI/CD
+ Docker/containerization + Rust-toolchain concerns as the fix warrants — decide fresh from what you touch; do not
inherit any prior DAG's selection).

## Why you exist (round 1 of a 2-round remediation budget)
The review DAG for PR #21 folded **REQUEST-CHANGES** (round 1). All nine of issue #11's acceptance criteria were
judged **MET**; the verdict is driven **solely** by one robustness `major`, **IMG-1**, on the durability of the
image-publish path. Close IMG-1 and the gate flips to APPROVE. The authoritative review body lives at:
`/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-ci-actions-r2/SYNTHESIS.md` (read it).

## The change you are remediating (prior diff)
- **PR #21** — branch **`work/ci-actions`**, head `c8123376ca1794c0b0466f41a1204bf3c3301b16`, base `main`
  (currently `61f924afa`), state OPEN / MERGEABLE / CLEAN, `Closes #11`. Primary file:
  `.github/workflows/ci.yml`. Work on **this existing branch** and push to it so PR #21 updates in place — do **not**
  open a new PR and do **not** change the issue linkage.

## The blocking finding to resolve (IMG-1, major)
**Finding**: the image is built with **Rust 1.88** (pinned in `Dockerfile:FROM rust:1.88-slim-bookworm`, which
landed on `main` via #12), decoupled from and older than CI's validated `RUST_TOOLCHAIN: "1.97"` in `ci.yml`. The
`image` job is gated `if: push && ref==main`, so the container build **never runs on a PR** and is absent from the
machine gate. The one build that exercises the Dockerfile runs only post-merge on `main`, on a toolchain no CI check
validates — so a future `Cargo.lock` bump that raises the rustc floor above 1.88 would keep PR CI green (1.97) while
the post-merge image publish breaks (1.88), discovered only after landing.

**Required change (the review's own words — you choose how, and may combine):** remove the toolchain decoupling by
driving the Dockerfile's Rust version from a **single source of truth** shared with `RUST_TOOLCHAIN` (e.g. a
build-arg the workflow passes to `docker/build-push-action`, or raise the Dockerfile `FROM` to match 1.97),
**and/or** run the image build on PRs with `push: false` (a build-only check) so the Dockerfile build is gated
**before** merge rather than first exercised on `main`.

## Scope judgment (yours to make)
- The cleanest fix may be localizable to `ci.yml` (the PR's own file) — e.g. a PR-time build-only `image` check with
  `push: false` — which closes the "green-on-PR / broken-post-merge" window without touching files owned by other
  issues. If instead you change `Dockerfile` (which is on `main` from #12), make the branch coherent with `main`'s
  current `Dockerfile` and keep the single-source-of-truth property. Decide the approach you can best defend; either
  satisfies IMG-1.
- **Do not regress** any of the nine met acceptance criteria, and do not weaken an existing gate (no job that
  passes-on-failure; `--locked` preserved; pins still resolve).

## Advisory findings (optional — fold only if cheap and clearly correct; none block)
From the review, 5 minor + 4 nit, advisory only: WF-1 (pin exact `1.97.0`/`rust-toolchain.toml`), WF-2 (MSRV
reconcile), **IMG-2** (now-dead Dockerfile-detection skip branch — a cheap, related cleanup if you touch the `image`
job), DOC-1 (name the folded doc-debt in the PR description), IMG-3/IMG-4 (manual-republish note / surface pushed
digest), DOC-2 (`crates/chirp-server/README.md` should reference `ServerError::InvalidBody`). **Supply-chain items
SEC-1 and SEC-2 are already tracked under issue #24 — do NOT address or duplicate them here.** Folding advisories is
optional; IMG-1 is the only thing that must change.

## Acceptance criteria (this remediation)
1. IMG-1 is resolved — the Dockerfile build toolchain is no longer silently decoupled from CI's validated
   toolchain, by one or both of the sanctioned approaches above.
2. All nine of issue #11's original acceptance criteria remain met (`fmt --check`, `clippy -D warnings`, `test`,
   wasm build, on-`main` GHCR build+push, cargo/target cache, required-check-friendly job names, PR into `main`).
3. The fix is pushed to branch `work/ci-actions` so PR #21 updates in place and stays MERGEABLE against `main`.
4. The machine gate is green on the updated head (the checks CI can run; verify by read-only inspection /
   `actionlint` and whatever you can run, and by running the workspace's own `fmt`/`clippy`/`test` as applicable).

## Declared output
- A root **`SYNTHESIS.md`** at this DAG's workspace root
  (`/home/user/nousix-runtime/nswe-demo/taskflow/dags/remediate-ci-actions/SYNTHESIS.md`) whose body is the
  authoritative **machine verdict** (PASS / FAIL) for this remediation: what changed and why, the four-check gate
  result, how IMG-1 was closed, confirmation the nine criteria still hold, and the updated PR #21 head SHA. This
  body — not a side-effect — is what the overseer reads.
- The updated `work/ci-actions` branch pushed to PR #21 (do not merge; do not touch `main`).

## Constraints
- Scope: `Nousix-LLC/nswe-demo` only. You MAY modify code and push to `work/ci-actions`; you MUST NOT merge, MUST
  NOT force-push or rewrite `main`, and MUST NOT rewrite merged history. Changes stay on the PR branch. Add no
  attribution trailers to commits or the PR. File any genuinely new, out-of-scope defect you discover as a backlog
  issue (epic #3) rather than expanding this fix.
- Decide your own decomposition (Atomic vs NeedsDecompose) and your own methodology bundles; do not carry a prior
  DAG's selection forward. This remediation re-enters the machine gate; after it folds machine-PASS the overseer
  launches a fresh review DAG before anything lands (nothing lands unreviewed).
