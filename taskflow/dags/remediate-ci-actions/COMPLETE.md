# COMPLETE — remediate-ci-actions (PR #21, IMG-1, round 1)

**Task**: Resolve the sole blocking review finding **IMG-1** (major) on PR #21 (`CI: GitHub Actions for
the Rust/WASM workspace (#11)`, branch `work/ci-actions`), push to the existing branch so the PR re-enters
the machine gate, and report a machine verdict. Evaluated **Atomic**; executed to completion.

**Outcome**: **machine PASS.** IMG-1 closed by running the `image` job on pull requests as a build-only
check (`push: false`) in `.github/workflows/ci.yml`, so `./Dockerfile` (on `main` from #12, present on the
PR merge ref) is gated **before** merge — closing the 1.88/1.97 toolchain-drift window. Advisories IMG-2
(dead detection branch removed) and IMG-4 (digest surfaced) folded in the same job; DOC-1 folded via the PR
description. SEC-1/SEC-2 left to issue #24. No Dockerfile change → PR stays MERGEABLE.

**Verification**: `actionlint` clean; local fmt/clippy(`-D warnings`)/test/doc(`-D warnings`)/wasm all green
on rustc 1.97.1; merged-tree `docker buildx build --check` clean; **live CI run 37720238038 on head
`716817b` = success, 6/6 jobs (fmt, clippy, test, wasm, doc, image)**. All nine of issue #11's acceptance
criteria remain MET; no gate weakened.

**State changes**:
- Pushed `c812337..716817b` to `work/ci-actions` (one commit; PR #21 updated in place, OPEN/MERGEABLE/CLEAN).
- Updated PR #21 description with a remediation note (DOC-1).
- `main` untouched (`61f924afa…`). No merge, no force-push, no history rewrite, no new PR, no linkage change,
  no attribution trailers.

**Declared output**: `SYNTHESIS.md` at this DAG's workspace root — the authoritative machine verdict the
overseer reads (observation seam). This remediation did not land; the overseer launches a fresh review DAG
before anything merges.

**Remediated PR head SHA**: `716817bcac7d669169a4339b0d15005a1eca7e15`
