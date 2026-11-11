# _BRIEF.md — remediate-epic-persist-r1b (code remediation, PR #113) — swe-coder

## Objective
Clear the single landing blocker on PR **`Nousix-LLC/nswe-demo#113`** ("Durable PostgreSQL persistence for
chirp", `work/epic-persist` → `main`) — the failing required **`doc`** CI check — together with the connected
documentation-integrity and feature-gating doc hazards grouped in issue **#118**, on the goal's existing branch
**`work/epic-persist`** (do not branch anew). The durable store underneath is sound per the PR review; this is a
documentation / intra-doc-link remediation, **not** a re-architecting of the persistence layer. Keep PR #113 the
live PR and keep it mergeable and clean.

## Inputs (what you build on)
- **The PR under remediation**: `Nousix-LLC/nswe-demo#113`, branch `work/epic-persist`, pinned head
  `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`, into `main`. Closes #65, #66, #67 (children of epic #56); #64 stays
  open and is **not** in scope to close here.
- **The review verdict** on PR #113: **REQUEST-CHANGES**, one landing blocker **CI-01** — `cargo doc --workspace
  --no-deps --locked` runs with `RUSTDOCFLAGS=-D warnings`; the public doc comment on `export_user_data`
  (`crates/chirp-server/src/repository/in_memory.rs:787`) carries an intra-doc link
  `` [`ExportDocument`](super::export::ExportDocument) `` to a `pub(crate)` item in a private module, which
  `rustdoc::private_intra_doc_links` turns into a hard error, so the crate fails to document and the required
  `doc` check is red. Merge state is UNSTABLE solely because of this required check. rustdoc reports only the
  first crate that fails, so a further `-D warnings` doc error can surface behind this one once it is fixed.
- **The connected backlog issue `#118`** (documentation integrity + feature-gating doc hygiene for the
  persistence layer): names the blocker link plus (a) false "scaffold stub" / "placeholder" prose in
  `crates/chirp-server/src/repository/postgres.rs` and `in_memory.rs` describing fully-implemented methods as
  unimplemented, (b) internal work-breakdown / subtask vocabulary in shipped comments, and (c) further
  feature-gating doc links from always-compiled modules (e.g. `export.rs`) to cfg-gated items. Clear this group
  in the same change so a `doc` re-run is clean.
- **The bar the result is still held to**: the epic #56 acceptance criteria of **#65 / #66 / #67** — the durable
  store behind the `ChirpRepository` seam, versioned migrations, fail-closed retention, and non-vacuous,
  stranger-runnable durability proofs. These must remain met; the fix must not weaken them.

## Acceptance criteria (the checklist the result is held to)
1. The required **`doc`** check goes green: `cargo doc --workspace --no-deps --locked` under `-D warnings`
   documents cleanly. Because rustdoc stops at the first failing crate, confirm by re-running that **no further
   `-D warnings` doc error surfaces behind the first** — clear the #118 hazards that could surface in the same
   change.
2. The **#118** documentation-integrity and feature-gating hazards are resolved: prose describes the code as it
   actually stands (no false stub/placeholder/scaffold narrative, no internal subtask vocabulary), and
   feature-gating doc links are correct under the feature combinations the `doc` check builds.
3. **No behavioural regression**: #65/#66/#67 remain met — the change stays documentation/link-level and does
   not alter the durable store, its migrations, its retention/fail-closed behaviour, or its durability proofs.
4. **No regression of the currently-green checks**: `clippy`, `fmt`, `test`, `wasm` stay green (they all pass at
   `09fa453`).
5. #64 stays **open** (durability activates only post-merge + image digest-pin + out-of-band credential Secret);
   do not close it.

## What to evaluate / concerns to cover (distinct concerns, each with its bar)
- **Documentation-link correctness** — every public item's rustdoc links resolve with no
  `rustdoc::private_intra_doc_links` (or other `-D warnings`) error. Bar: a green `doc` run, re-run to confirm
  nothing surfaces behind the first fix.
- **Documentation accuracy** — shipped prose matches the implemented code; #66's full capability set is not
  misdescribed as unbuilt. Bar: no stale-build narrative, no dangling internal identifiers.
- **Feature-gating doc hygiene** — intra-doc links from unconditionally-compiled modules to cfg-gated items are
  correct across the feature sets `doc` builds. Bar: clean under each.
- **Non-regression of the durable store** — the persistence behaviour and proofs for #65/#66/#67 are unchanged.
  Bar: the diff is documentation/link-level; `clippy`/`fmt`/`test`/`wasm` stay green.

Evaluate your own scope and decomposition and select your own methodology; this brief names the concerns and the
bar, not the method.

## Declared output
- Commits on **`work/epic-persist`** (the goal's branch; never `main`, no force-push).
- **PR #113 stays the live PR**, updated in place — do not open a new PR, do not merge your own PR, do not push
  to `main`.
- A root **`SYNTHESIS.md`** that accounts for the blocker (cleared, with the green `doc` run demonstrated) and
  for each of #65/#66/#67 (still met, or not and why) — the verdict the overseer reads at the machine gate.
- Everything that reaches GitHub (PR description, commit messages, any comment) is written for the repository's
  readers: the outcome and what changed and how it was verified, with **no host paths, no cluster/SSH details,
  and no taskflow internals**.

## Constraints
Only `Nousix-LLC/nswe-demo`. Branch `work/epic-persist` only; no force-push; a DAG never merges its own PR and
never pushes the integration branch. No attribution trailers on commits. Nothing posted to GitHub carries
host/system details. Do not prescribe your own Atomic/NeedsDecompose verdict to this brief — evaluate it.
