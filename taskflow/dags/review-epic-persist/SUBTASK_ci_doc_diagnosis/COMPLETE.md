# COMPLETE — SUBTASK_ci_doc_diagnosis

**Task**: Diagnose the failing required `doc` CI job for PR #113 @ `09fa453`, name the change that greens it,
record it as a blocker to landing. Read-only; findings document only.

## What was done

- Confirmed the live CI rollup on PR #113 at the pinned head `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`:
  `clippy`/`fmt`/`test`/`wasm` PASS, `image` skipping, `doc` FAIL, merge state `UNSTABLE`.
- Read the failing `doc` job log and isolated the failing step: `cargo doc --workspace --no-deps --locked` under
  `RUSTDOCFLAGS: -D warnings`, exit code 101.
- Root cause (verified against source at the pinned commit): a public doc comment on `export_user_data`
  (`crates/chirp-server/src/repository/in_memory.rs:787`) carries a rustdoc intra-doc link to
  `super::export::ExportDocument`, which is `pub(crate)` inside the private module `mod export;`. The
  `rustdoc::private_intra_doc_links` lint, promoted to a hard error by `-D warnings`, fails the `chirp-server`
  crate's documentation.
- Named the narrowest green-ing change (remove the public→private intra-doc link at `in_memory.rs:787`) and noted
  weaker alternatives. Confirmed `in_memory.rs:827` is a code statement, not a doc comment, so line 787 is the
  sole offending link.
- Recorded it as finding `CI-01`, severity `blocker`, `blocks_landing: true`, and stated the landing gate: the
  PR is not clean to land until `doc` is green AND the PR is mergeable and clean, regardless of the other concerns.

## Output

- `SUBTASK_ci_doc_diagnosis/outputs/findings.md` — conforms to `../contracts/finding_schema.md` (prefix `CI`),
  one blocker finding, sub-verdict **HAS-BLOCKERS**, what-checked / what-found-clean both stated.

## Composition note

This spoke performed no GitHub writes and did not modify the repository. Its `findings.md` is consumed by
`SUBTASK_synthesis`, which folds the `doc` blocker into the verdict and owns all posting. The remediation (the
actual source fix) is out of scope for this task.

## Constraint adherence

Read-only on the repo; no GitHub writes. Failure described by content (job command + quoted rustdoc error +
repo-relative `file:line`); no host paths, runner internals, or pipeline internals in the findings. Plain voice;
avoid-ai-writing finishing pass run.
