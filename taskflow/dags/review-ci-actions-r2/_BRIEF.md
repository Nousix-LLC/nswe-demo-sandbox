# _BRIEF.md — review DAG: ci-actions (#11, PR #21) — re-fork r2 (persona swe-coder)

You are a **code-review DAG** for the `Nousix-LLC/nswe-demo` engagement. Review the open pull request **PR #21**
(`CI: GitHub Actions for the Rust/WASM workspace (#11)`) and produce an authoritative landing verdict. You review
and report; you do **not** change code, push, or merge. Select and load your own review methodology (the
code-review methodology is your spine; add CI/CD, supply-chain/security, and Rust-idiom methodology as the diff
warrants — decide fresh from what the diff touches).

## Why this is a re-fork (r2)
The original review DAG (`taskflow/dags/review-ci-actions/`) was force-marked COMPLETE by a resume-time
subtree-resolution fixpoint during a whole-OS reconstruction **without producing any verdict** — no root
`SYNTHESIS.md`, no posted review. Its decomposition artifacts were lost. Nothing of its analysis survives, so this
is a clean fresh review, not a continuation. PR #21 has **zero** reviews posted and has **not** been reviewed.

## Objective
Judge whether PR #21 is fit to land on `main`, held to issue #11's acceptance criteria, and emit APPROVE or
REQUEST-CHANGES with findings. Nothing lands unreviewed; your `SYNTHESIS.md` verdict is the authoritative landing
signal for the overseer (the `gh` self-review approval path is blocked because the PR author and the reviewer are
the same account, so post what you can as a review comment, but the authoritative verdict lives in your root
`SYNTHESIS.md` body).

## The change under review
- **PR #21** — head `c8123376ca1794c0b0466f41a1204bf3c3301b16`, base `main` (currently `61f924afa`), state
  OPEN / MERGEABLE / CLEAN. `Closes #11`.
- **Primary deliverable:** `.github/workflows/ci.yml` (+194 lines). Six jobs:
  - `fmt` — `cargo fmt --all --check`
  - `clippy` — `cargo clippy --workspace --all-targets --locked -- -D warnings`
  - `test` — `cargo test --workspace --locked`
  - `wasm` — `chirp-frontend` `wasm32-unknown-unknown` build + `wasm-bindgen --target web` (produces the `pkg/`
    the SPA's `index.html` imports)
  - `doc` — `cargo doc --workspace --no-deps` under `RUSTDOCFLAGS=-D warnings`
  - `image` — **`main`-push only** — builds & pushes `ghcr.io/nousix-llc/chirp-server` via the built-in
    `GITHUB_TOKEN`.
  - Pinning claims to verify: toolchain `dtolnay/rust-toolchain@1.97`, `Swatinem/rust-cache@v2`,
    `wasm-bindgen-cli` pinned to the locked `0.2.129`, `--locked` cargo throughout.
  - Permissions claims to verify: top-level `permissions: contents: read`; only `image` adds `packages: write`;
    no secrets beyond `GITHUB_TOKEN`.
- **Folded #8-review minors** (in the same PR):
  - CRQ-02 / F2 — rustdoc intra-doc-link fixes across the workspace (doc-comment-only edits in
    `crates/chirp-frontend/*`, `crates/chirp-server/*`, `crates/ferric/*`, `crates/ferric-router/*`,
    `crates/ferric-http/*`) so the new `doc` gate is green without weakening it. Claimed: no behavior change.
  - CRQ-01 — `crates/chirp-server/README.md` validation-error status corrected to **400** (`VALIDATION_ERROR`).

## IMPORTANT ordering fact (changed since the PR was written)
When PR #21 was authored, #12 (containerize) had **not** landed, so the PR documents the `image` job as
"skips cleanly when `./Dockerfile` is missing." **#12 has since LANDED** — the multi-stage `Dockerfile` is now on
`main` (`61f924afa`). Therefore the `image` job's skip-clean path is no longer the active path on a `main` push:
the next `main` push (i.e. when #11 lands) will trigger a **real** GHCR build-and-push. Review the `image` job
against a **present** `Dockerfile`: build context, image tag/ref, GHCR auth via `GITHUB_TOKEN` + `packages: write`,
and whether a real push on land is correct and intended — not merely the skip path.

## Acceptance criteria (issue #11)
On PR/push: `cargo fmt --check`, `cargo clippy -D warnings`, `cargo test`, build the wasm frontend, and (on main)
build & push the chirp-server container image to GHCR; cache cargo/target; required-check friendly; PR into `main`.
Confirm each is genuinely met by the workflow as written (not merely claimed in the PR body).

## Concerns to cover (named as distinct concerns; you choose depth and methodology)
- **CI correctness** — triggers (PR + push to `main`), job definitions actually run the claimed commands, the
  cache keys are correct and safe (no poisoning across lockfile/rustc changes), `--locked` is honored, toolchain
  and `wasm-bindgen-cli` pins resolve, job names are stable/required-check-friendly, and the full matrix actually
  gates a PR (a job that silently passes on failure is a blocker).
- **The `image` job specifically** — correctness and safety of the GHCR build+push against the now-present
  `Dockerfile`: tag/ref correctness, `main`-only gating, `GITHUB_TOKEN` + `packages: write` least-privilege, no
  credential leakage, and behavior on the first real land.
- **Supply-chain / security / trust boundary** — third-party action pinning (tag vs commit-SHA pinning is a
  supply-chain exposure worth a finding), `permissions:` least privilege (top-level read, image-only
  `packages: write`), secret handling, and any token over-grant. CI holds push credentials, so treat this as a
  trust boundary.
- **Testing depth** — does CI exercise the full suite (workspace `cargo test --locked`, doctests, the wasm build,
  the `doc -D warnings` gate), and are all crates covered? Note any gap (e.g. no integration/e2e, no wasm test
  run) as a finding at appropriate severity.
- **Workflow quality / maintainability** — YAML structure, duplication across jobs, matrix usage, readability.
- **The folded minors** — confirm the rustdoc link fixes are genuinely doc-comment-only with no behavior change,
  and that the README 400/`VALIDATION_ERROR` correction is accurate. Folding unrelated #8-review minors into a CI
  PR is a scope question — note it.
- **Rust/GitHub-Actions idiom** — one concern among the above, not the only one.

## Declared output
- A root **`SYNTHESIS.md`** at this DAG's workspace root
  (`/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-ci-actions-r2/SYNTHESIS.md`) whose body carries: the
  **verdict (APPROVE or REQUEST-CHANGES)**, a gate summary (block / major / minor / nit counts), the acceptance-
  criteria pass/fail table, and every finding with severity and location. This body — not a side-effect — is the
  authoritative landing verdict.
- A posted review on PR #21 where the platform permits (comment if approval is blocked by self-review).
- Non-blocking findings (minor/nit/suggestion) **filed as backlog issues** on the project board (epic #3), linked
  to PR #21 / issue #11, so they survive this DAG being reaped. Group related findings; do not file anything the
  board already holds.

## Constraints
- Scope: `Nousix-LLC/nswe-demo` only. Review-only: **do not** modify code, push, rebase, relock, or merge. Do not
  re-run or trust nothing — you may run read-only checks (e.g. `actionlint`, inspecting the workflow) to verify
  correctness, but you author no change to the tree. No force-push. Add no attribution trailers to anything you
  post.
- Decide your own decomposition (Atomic vs NeedsDecompose) and your own methodology bundles; do not carry a prior
  DAG's selection forward.
