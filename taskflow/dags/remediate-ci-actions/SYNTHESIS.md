# SYNTHESIS — remediation of PR #21 "CI: GitHub Actions for the Rust/WASM workspace (#11)", round 1

**Repo**: `Nousix-LLC/nswe-demo` · **PR**: #21 · **Branch**: `work/ci-actions`
**Base**: `main` @ `61f924afa2a31d4d92c214c89b48e0ee6fc4e394` (untouched)
**Reviewed head (before)**: `c8123376ca1794c0b0466f41a1204bf3c3301b16`
**Remediated head (after, pushed)**: `716817bcac7d669169a4339b0d15005a1eca7e15`
**Remediation DAG**: `remediate-ci-actions` (persona swe-coder) · evaluated **Atomic**

---

## Verdict

```
gate:    PASS
round:   1 of 2
basis:   IMG-1 (the sole verdict-forcing major) is CLOSED. The machine gate is green on the
         remediated head: CI run 37720238038 = success, 6/6 jobs (fmt, clippy, test, wasm, doc,
         image). PR #21 is OPEN / MERGEABLE / CLEAN against main@61f924a. Base main untouched;
         no merge performed; issue linkage (Closes #11) intact.
```

> **This `SYNTHESIS.md` body is the authoritative machine verdict the overseer reads.** It reports a
> machine PASS for the remediation only — it is **not** an approval to land. Per the brief, after this
> folds machine-PASS the overseer launches a **fresh review DAG** before anything merges (nothing lands
> unreviewed). This remediation did **not** merge, did **not** touch `main`, and added **no** attribution
> trailers to the commit or PR.

---

## What changed, and why

**One file changed: `.github/workflows/ci.yml`** (the PR's own file). The branch `work/ci-actions` was cut
*before* work-item #12 landed the Dockerfile, so it carries no Dockerfile and its `image` job still had the
"await #12 / detect-and-skip" scaffolding. `main` (from #12) now owns `./Dockerfile`
(`FROM rust:1.88-slim-bookworm@sha256:…`).

The `image` job was reshaped from *"publish only on push to `main`, skip if no Dockerfile"* to *"build on
**every PR and every `main` push**; publish to GHCR only on `main`"*:

- Removed the job-level `if: push && ref==main` gate so the job runs on pull requests too.
- Added a single derived flag `PUBLISH = (event==push && ref==refs/heads/main)`; the build step passes
  `push: ${{ env.PUBLISH == 'true' }}` (so **`push: false` on PRs — build-only**, `push: true` on `main`),
  and GHCR login + the digest summary are guarded to `PUBLISH` only. Least privilege preserved: `packages:
  write` is exercised only on the `main` publish path, inert on PR builds.
- Deleted the now-dead **"Detect Dockerfile"** step and its `present=='true'` guards — the build now runs
  unconditionally, so a missing/broken Dockerfile fails **loudly** instead of silently skipping (folds
  advisory **IMG-2** and removes its silent-skip hazard).
- Added a step that writes the published image **digest** to the job summary on the publish path (folds
  advisory **IMG-4**).
- Updated the header comment to describe the new behavior.

**Why this closes IMG-1 (the mechanism).** On a `pull_request` event `actions/checkout@v4` builds the
**merge ref** (PR head merged onto base `main`), which *includes `main`'s `./Dockerfile`*. The PR-time
build-only job therefore exercises the exact Dockerfile that would publish post-merge — the **pre-merge
build gates the post-merge publish**. The drift window the review flagged ("a future `Cargo.lock` floor
bump above the Dockerfile's rustc keeps PR CI green on 1.97 while the post-merge image publish breaks on
1.88, discovered only on `main`") is closed: such a bump now fails the **PR** `image` gate, before merge,
not silently after. This is the review's sanctioned approach #2 ("run the image build on PRs with
`push: false`"), and it makes the decoupling **no longer silent** — satisfying acceptance criterion 1.

**Why not the single-source-of-truth build-arg / `FROM`-bump approach.** That sanctioned alternative would
require modifying `./Dockerfile`, which lives on `main` (owned by #12). Because `work/ci-actions` branched
before #12, adding/modifying a Dockerfile on the branch produces an **add/add merge conflict** with `main`'s
Dockerfile — the PR would stop being MERGEABLE, violating acceptance criterion 3. The ci.yml-only, build-on-PR
approach is the brief's explicitly-named "cleanest fix localizable to `ci.yml`": it closes the drift window,
touches no file owned by another issue, and keeps the PR mergeable. (Approaches are an `and/or`; one suffices.)

---

## Four-check gate (remediation)

| Check | Result | Evidence |
|-------|--------|----------|
| 1. Conformance / scope | **pass** | Exactly one file changed (`.github/workflows/ci.yml`, +38/−30). `Dockerfile` and all of `main` untouched → PR stays MERGEABLE/CLEAN. `actionlint 1.7.12` on the workflow: **clean (exit 0)**. No commit attribution trailer; no new PR; `Closes #11` preserved. |
| 2. Coverage | **pass** | The sole blocking finding **IMG-1** is resolved. Cheap, clearly-correct advisories in the same job folded: **IMG-2** (dead detection branch removed), **IMG-4** (digest surfaced). **DOC-1** folded via a PR-description remediation note. |
| 3. Duplication / boundaries | **pass** | No duplication of the #24-owned supply-chain items: **SEC-1/SEC-2 deliberately NOT touched** (action SHA-pinning / provenance remain #24's). WF-1/WF-2/IMG-3/DOC-2 left as advisory (out of scope of IMG-1; none block). |
| 4. Machine gate / verdict | **pass** | CI run **37720238038** on head `716817b` = **success**; per-job: fmt ✓ clippy ✓ test ✓ wasm ✓ doc ✓ **image ✓**. Image job log confirms `push: false` on the PR (build-only, nothing published). PR #21 OPEN / MERGEABLE / **CLEAN**. |

---

## IMG-1 closure assertion

- **Before**: `image` job gated `if: push && ref==main` → container build **never ran on a PR**; the single
  build that exercised the Dockerfile (rust 1.88) ran only post-merge on `main`, validated by no CI check.
- **After**: `image` job runs on PRs as a build-only check (`push: false`) against the merge ref (which
  carries `main`'s Dockerfile), and publishes on `main` only. The Dockerfile build is now a **pre-merge gate**.
- **Live confirmation**: the PR-time `image` job built `./Dockerfile` and **succeeded** on head `716817b`
  with `push: false` (CI run 37720238038) — the gate is real and green, and the drift is now caught before
  merge rather than after.

---

## Nine acceptance criteria of issue #11 — still MET (no regression)

Verified locally with the pinned toolchain (`rustc 1.97.1`, matching `RUST_TOOLCHAIN: "1.97"`) and confirmed
live on CI run 37720238038:

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Runs on PR + push to `main` | **MET** | `on:` block unchanged (`pull_request→[main]`, `push→[main]`, `workflow_dispatch`); CI ran on this PR. |
| 2 | `cargo fmt --check` | **MET** | Local `cargo fmt --all --check` exit 0; CI `fmt` ✓. |
| 3 | `cargo clippy -D warnings` | **MET** | Local `cargo clippy --workspace --all-targets --locked -- -D warnings` exit 0; CI `clippy` ✓. |
| 4 | `cargo test` | **MET** | Local `cargo test --workspace --locked` exit 0; CI `test` ✓. |
| 5 | Build the WASM frontend | **MET** | Local wasm32 build of `chirp-frontend` + `chirp` example exit 0; CI `wasm` ✓. |
| 6 | On `main`, build + push chirp-server image to GHCR | **MET (and hardened)** | Publish path preserved: on `main` push the job still builds and `push: true` to `ghcr.io/nousix-llc/chirp-server`. IMG-1 caveat on this path's durability is now resolved by the pre-merge gate. |
| 7 | Cache cargo/target | **MET** | `Swatinem/rust-cache@v2` on the compiling jobs, unchanged. |
| 8 | Required-check-friendly job names | **MET** | Each job keeps explicit `name:`==id (stable branch-protection contexts). `image` now additionally runs on PRs as intended by the remediation (gating the Dockerfile) — not a regression; its name is unchanged. |
| 9 | Delivered as a PR into `main` | **MET** | PR #21 OPEN/MERGEABLE/CLEAN, base `main`, same PR updated in place. |

No gate was weakened: no job passes-on-failure (the silent-skip branch was *removed*), `--locked` preserved
on every compiling/build step, all action/toolchain pins still resolve (CI green), and the `image` publish
path on `main` is unchanged except for the added digest summary.

---

## Advisory findings disposition

| Finding | Severity | Disposition |
|---------|----------|-------------|
| IMG-1 | major | **Resolved** (build-on-PR, `push: false`). |
| IMG-2 | minor | **Folded** — dead "Detect Dockerfile" skip branch removed; build fails loudly on a missing Dockerfile. |
| IMG-4 | nit | **Folded** — pushed image digest surfaced in the job summary. |
| DOC-1 | minor | **Folded** — PR description now names this remediation and the pre-existing folded doc-debt (CRQ-01/CRQ-02). |
| WF-1 (pin exact `1.97.0`/`rust-toolchain.toml`) | minor | **Deferred** — advisory; out of scope of IMG-1; not needed for the gate. |
| WF-2 (MSRV reconcile) | minor | **Deferred** — pre-existing manifest concern, advisory. |
| IMG-3 (manual-republish path) | nit | **Deferred** — noted-for-awareness only. |
| DOC-2 (`README` → `ServerError::InvalidBody`) | nit | **Deferred** — cosmetic; touches a #19-owned README; advisory. |
| SEC-1 / SEC-2 | minor / nit | **NOT addressed here — owned by issue #24** (per the brief). No duplication. |

No genuinely new, out-of-scope defect was discovered during this remediation, so no new backlog issue (epic
#3) was filed.

---

## Mechanical evidence log

- `actionlint 1.7.12` on `.github/workflows/ci.yml`: **clean** (exit 0).
- Local (rustc 1.97.1): `fmt --check` ✓ · `clippy --workspace --all-targets --locked -- -D warnings` ✓ ·
  `test --workspace --locked` ✓ · `cargo doc --workspace --no-deps --locked` with `RUSTDOCFLAGS=-D warnings` ✓ ·
  wasm32 build of `chirp-frontend` lib + `chirp` example ✓.
- Merge-ref validation: `git merge` of `main`@`61f924a` into the remediated head = **clean, no conflicts**;
  `./Dockerfile` present in the merged tree; `docker buildx build --check` on the merged tree = **"Check
  complete, no warnings found"** (exit 0). The validation merge was discarded; only the single commit
  `716817b` was pushed.
- Push: `c812337..716817b  HEAD -> work/ci-actions` (exit 0). Branch is exactly **one** commit ahead of the
  reviewed head.
- Live CI: run **37720238038** (event `pull_request`, head `716817b`) = **success**, jobs fmt/clippy/test/
  wasm/doc/image all ✓; `image` ran with `push: false`.
- PR #21 after push: `state=OPEN`, `mergeable=MERGEABLE`, `mergeStateStatus=CLEAN`, `headRefOid=716817b`,
  `baseRefName=main`. `main` ref still `61f924afa…` (untouched).

## Scope / constraint compliance

- Changes confined to `Nousix-LLC/nswe-demo`, branch `work/ci-actions`. **No merge. No push to `main`. No
  force-push. No history rewrite. No new PR. No issue-linkage change.** No attribution trailers on the
  commit or PR. Supply-chain items (SEC-1/SEC-2) left to issue #24.
