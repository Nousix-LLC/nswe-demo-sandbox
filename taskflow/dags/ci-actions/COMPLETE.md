# COMPLETE — ci-actions (#11)

**Status: completed (Atomic).** GitHub Actions CI is stood up for `Nousix-LLC/nswe-demo` and the two
deferred #8-review minors are folded in. Full verdict, evidence, and follow-ups in `SYNTHESIS.md`
(the observation seam the overseer gates on).

## Produced
- `checkout/.github/workflows/ci.yml` — CI workflow (jobs: `fmt`, `clippy`, `test`, `wasm`, `doc`;
  `main`-only `image` job wired for GHCR, gated to skip cleanly until #12's Dockerfile lands).
- CRQ-02: 79 rustdoc intra-doc-link errors resolved across 20 source files (doc comments only).
- CRQ-01: `crates/chirp-server/README.md` validation-error status corrected to 400.
- Commits on `work/ci-actions` (`c2a60d2`, `763b0e4`, `c812337`).
- **PR #21** into `main` (`Closes #11`): https://github.com/Nousix-LLC/nswe-demo/pull/21
- `SYNTHESIS.md` — PASS verdict + decision record.

## Evidence
All five PR checks pass at head `c812337` both locally and in the real GitHub Actions runner
(run `37581289276`): fmt ✅ clippy ✅ test ✅ (14 suites) doc ✅ wasm ✅; `actionlint` clean. The
workflow self-validated on its own PR.

## Composition with parent / handoff
The overseer lands PR #21 after a review DAG (P1) — this item did NOT merge or push to `main`.
Repo-admin follow-ups for the overseer (see `SYNTHESIS.md`): adopt the five jobs as required status
checks on `main`; set GHCR package visibility after the first post-#12 `main` build; the `image` job
activates automatically once work-item #12 adds `./Dockerfile`. Pre-existing MSRV-vs-locked-deps
mismatch flagged (CI pins 1.97, not the declared 1.82).

## Not done (by design)
No containerization (#12), no deploy manifests / ArgoCD Application (#13), no application-behavior
change beyond the two documentation minors.
