# _BRIEF.md — Remediation of PR #113 (durable PostgreSQL persistence), round 1

This is a code-remediation goal for the repository `Nousix-LLC/nswe-demo`. A prior change delivered durable
PostgreSQL persistence on branch `work/epic-persist` as PR #113 (epic #56: issues #65, #66, #67; #64 stays
open). A review returned **REQUEST-CHANGES** with a single landing blocker: the required `doc` CI check is red.
The implementation underneath is sound and must not be re-architected — this goal clears the documentation /
feature-gating blocker and its connected hazards so the PR can land clean, without regressing the durability
work.

## Objective

Make PR #113 landable: the required `doc` CI check passes green and the PR stays mergeable and clean, with no
regression of the durability guarantees #65/#66/#67 deliver. Update PR #113 in place by committing to its
existing branch `work/epic-persist` (the PR tracks that branch). Do not open a second PR unless the branch
state makes updating #113 impossible, in which case open one PR into `main` that closes #65, #66, #67 with one
`Closes #N` keyword per issue as plain text in the description.

## Acceptance criteria

The result is held to these, each named with where it is judged:

- **CI-01 (the blocker).** The `doc` CI job fails because a public doc comment links into a private module
  under `-D warnings`. Specifically, `export_user_data` at `crates/chirp-server/src/repository/in_memory.rs`
  (around line 787) carries an intra-doc link `` [`ExportDocument`](super::export::ExportDocument) `` to a
  `pub(crate)` item in the private `export` module; `RUSTDOCFLAGS: -D warnings` turns
  `rustdoc::private_intra_doc_links` into a hard error, so the crate fails to document and the check is red.
  **Acceptance:** drop or rework that public→private link (a plain code span `` `ExportDocument` ``, or a
  reword that no longer links into the private module), and `cargo doc --workspace --no-deps --locked` run with
  `-D warnings` is clean. Because rustdoc reports only the first crate that fails, re-run `doc` after the fix
  and confirm no further `-D warnings` error surfaces behind it.

- **Connected doc-link / feature-gating hazards (issue #118).** Clear these in the SAME remediation so the
  `doc` re-run is clean and does not fail on the next link:
  - `crates/chirp-server/src/repository/export.rs` (around line 7): an always-compiled reference that links
    into the `postgres`-feature-gated module — an ungated→gated doc link that can error under `-D warnings`
    once CI-01 is fixed. Make the reference gating-correct (gate the doc, or make it a plain code span).
  - The stale "scaffold stub" / "placeholder" rustdoc on the persistence layer: public doc comments describe
    methods that are now fully implemented as unimplemented stubs/placeholders, and internal build-breakdown
    vocabulary remains in shipped comments. Bring the persistence-layer docs in line with what the code
    actually does, so the documentation is accurate and carries no internal workstream vocabulary.
  - **Acceptance:** issue #118's criteria are met — persistence-layer public docs are accurate (no
    implemented-as-stub descriptions, no internal build vocabulary), and all public→private / ungated→gated
    intra-doc links in the changed crate are resolved, verified by a clean `cargo doc --workspace --no-deps
    --locked` under `-D warnings`.

- **No regression.** The durable store, the `ChirpRepository` seam, versioned migrations, fail-closed
  behavior, retention/transient lifetimes, and the durability proofs that #65/#66/#67 were accepted on must
  remain intact. The change is to documentation text, doc-links, and feature-gating of docs only — not to the
  store's logic, schema, or wiring.

## Inputs (what to build on — all named as repository identities)

- The branch under remediation: `Nousix-LLC/nswe-demo` `work/epic-persist`, PR #113, pinned head commit
  `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`. This is the prior diff you are correcting.
- The review verdict that produced this remediation: the posted **REQUEST-CHANGES** review on PR #113 and its
  **CI-01** finding (the private intra-doc link at `in_memory.rs:787`), plus the review's note that
  `export.rs:7` and the stale scaffold rustdoc are the two further `doc` hazards that can surface next.
- Issue **#118** ("stale scaffold documentation & feature-gating hygiene"), which groups the connected
  doc-link and feature-gating findings and carries their acceptance criteria.
- The original acceptance criteria of issues **#65, #66, #67** (the durability bars the change must still
  meet), and the persistence design that epic **#56** traces to (the design of record in the repository).

## What to evaluate (distinct concerns, each with the bar it is held to)

- **Documentation-link correctness.** Every public doc comment in the changed crate resolves its intra-doc
  links under `-D warnings`: no public item links into a `pub(crate)`/private item, no always-compiled doc
  links into a feature-gated item. Bar: `cargo doc --workspace --no-deps --locked` is green with `-D warnings`,
  confirmed by a fresh run (not inferred from fixing the first error).
- **Documentation accuracy.** Public docs on the persistence layer describe the behavior the code actually
  has, carry no "scaffold stub"/"placeholder" language for implemented methods, and carry no internal
  build-breakdown vocabulary. Bar: a reader of the published docs is not misled about what is implemented.
- **Feature-gating hygiene.** `postgres`-gated items and always-compiled items are documented consistently so
  the crate documents cleanly whether or not the `postgres` feature is enabled. Bar: `doc` is green in the
  CI configuration that runs it.
- **Non-regression of durability.** The store logic, seam, migrations, and proofs are untouched except where a
  doc comment sits; the existing test/proof suite still builds and the other CI checks (`clippy`, `fmt`,
  `test`, `wasm`) stay green. Bar: the only behavioral change is to documentation; all previously-green checks
  remain green.

The DAG selects and loads its own methodology for these concerns; this brief describes the work, it does not
name bundles or prescribe a decomposition or a method.

## Declared output

- Commits on `work/epic-persist` that update PR #113 (or, only if the branch state requires it, a fresh PR into
  `main` that closes #65, #66, #67), with the required `doc` check green and the PR mergeable and clean. The
  DAG never merges its own PR and never pushes to `main`.
- The PR description and commit messages are written for the repository's readers: what changed and why, how it
  was verified (a green `doc` run under `-D warnings`), and the issues it closes — with no host paths, no
  cluster/SSH details, and no taskflow internals.
- A root `SYNTHESIS.md` verdict that accounts for CI-01 (fixed, with the verification) and each item grouped
  under #118 (fixed, or not and why), and confirms no durability regression.

## Constraints

- **Scope: documentation and feature-gating of docs only.** Do not re-architect or modify the durable store,
  its schema, its migrations, or its wiring — the review found the implementation sound. Touch source only
  where a doc comment or a doc-link/feature-gate attribute must change.
- Branch `work/epic-persist`; **never force-push `main`**; never rewrite merged history.
- **No attribution trailers** on commits.
- **Nothing posted to GitHub carries host or system details** — no absolute/host paths, no cluster, SSH, or
  credential details, no taskflow/agent/run identifiers. Name everything by its repository identity
  (`owner/repo`, issue/PR numbers, commit SHAs, repo-relative paths).
