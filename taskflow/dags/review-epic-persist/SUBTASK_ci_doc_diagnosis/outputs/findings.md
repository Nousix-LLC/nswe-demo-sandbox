# Findings — CI `doc` check diagnosis — PR #113 @ 09fa453

## What I checked

- The live CI rollup on PR #113 (`gh pr checks 113`): `clippy` PASS, `fmt` PASS, `test` PASS, `wasm` PASS,
  `image` skipping, **`doc` FAIL** → merge state `UNSTABLE`. PR head commit confirmed as the pinned
  `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`; state OPEN, not draft, `MERGEABLE`.
- The failing `doc` job's log, down to the step that exited non-zero: the job runs
  `cargo doc --workspace --no-deps --locked` with `RUSTDOCFLAGS: -D warnings`, and the step exited with code 101.
- The single rustdoc error the step emitted, read by content (quoted below), and the crate it failed to document
  (`chirp-server`).
- Correlation to the PR #113 diff: whether the file and the doc comment the error points at are part of this
  change, and the visibility of the item the doc comment links to, at the pinned commit.
- Whether any second public-doc link into the same private module would still fail after the first is fixed.

## What I found clean

- Every other check on the PR passes at the pinned commit: `clippy`, `fmt`, `test`, and `wasm` are green, and
  `image` is skipping (not failing). The failure is isolated to `doc`.
- The failure is one localized rustdoc lint error, not a broad documentation breakage: `cargo doc` documented
  `ferric`, `ferric-http`, `ferric-router`, `chirp-frontend`, and `chirp-types` without complaint, and failed
  only while documenting `chirp-server` on a single intra-doc link.
- The error is deterministic and reproducible from the change itself — a doc-comment link, not a flaky or
  environment-dependent failure — so a targeted source change will green the check.
- The PR is otherwise `MERGEABLE` with no reported merge conflict; the only thing holding merge state at
  `UNSTABLE` is this required check.

## Findings

### CI-01 — required `doc` check fails: public docs link to a private item under `-D warnings`

- **severity**: blocker
- **blocks_landing**: true
- **location**: `crates/chirp-server/src/repository/in_memory.rs:787` @ 09fa453 — the doc comment on
  `export_user_data`. The linked item is declared at `crates/chirp-server/src/repository/export.rs:33`
  (`pub(crate) struct ExportDocument`) inside the module declared `mod export;` (private) at
  `crates/chirp-server/src/repository/mod.rs:110`. Both the offending doc comment and the linked `export` module
  are introduced by PR #113.
- **acceptance-criterion / design ref**: n/a as a code criterion — this is the required CI `doc` gate itself. (The
  doc comment in question describes the shared export path that #66's seam relies on, but the finding is the
  failing required check, not a #66 defect.)
- **principle**: a required CI check must pass before the PR is clean to land; and, concretely, public-item
  documentation must not carry a rustdoc intra-doc link that resolves to a private item when the `doc` job runs
  rustdoc with `-D warnings`.
- **why it matters here**: the `doc` job sets `RUSTDOCFLAGS: -D warnings`, which promotes the
  `rustdoc::private_intra_doc_links` lint from a warning to a hard error. The public method `export_user_data`
  (in `pub mod in_memory`) documents itself with the intra-doc link
  `` [`ExportDocument`](super::export::ExportDocument) ``, but `ExportDocument` is `pub(crate)` inside a private
  module, so rustdoc cannot resolve a public→private documentation link and fails the crate. The log shows this
  exactly:

  ```
  error: public documentation for `export_user_data` links to private item `super::export::ExportDocument`
     --> crates/chirp-server/src/repository/in_memory.rs:787:58
      = note: `-D rustdoc::private-intra-doc-links` implied by `-D warnings`
  error: could not document `chirp-server`
  ##[error]Process completed with exit code 101.
  ```

  While this fails, `doc` is red and the PR's merge state stays `UNSTABLE`; the change is not clean to land.
- **confidence**: verified — reproduced from the job log and confirmed against the source at the pinned commit:
  the offending doc link is at `in_memory.rs:787`, and the link target is `pub(crate)` within a private module.
  The other reference to `super::export::ExportDocument` in that file, at `in_memory.rs:827`, is a code statement
  (not a doc comment) and is not flagged; line 787 is the only public-doc link into the private module, so
  clearing it clears the sole error.
- **what would satisfy me**: the `doc` job passing (`cargo doc --workspace --no-deps --locked` green with
  `-D warnings`). The narrowest source change that achieves it is to stop the public doc comment from linking to
  the private item at `in_memory.rs:787` — e.g. replace the intra-doc link
  `` [`ExportDocument`](super::export::ExportDocument) `` with a plain code span `` `ExportDocument` `` (no link
  target), or otherwise reword so public docs no longer link into the private `export` module. Alternatives exist
  but are weaker: making `ExportDocument`/`mod export` public widens the crate's public API beyond what this doc
  link needs, and `#[allow(rustdoc::private_intra_doc_links)]` only suppresses the lint the job deliberately
  denies. The fix itself belongs to separate remediation work, not to this review. (One caveat for the
  remediator: after removing the link, re-run the `doc` job — rustdoc reports the first crate that fails to
  document, so confirm no further `-D warnings` error surfaces behind this one.)

## Concern sub-verdict

- **HAS-BLOCKERS**
- The required `doc` check fails at the pinned commit on a reproducible rustdoc error, so the PR is not clean to
  land. Landing is gated on `doc` going green **and** the PR remaining mergeable and clean — this holds even if
  every code concern in the review is otherwise clean.
