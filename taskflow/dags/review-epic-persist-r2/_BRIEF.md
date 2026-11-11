# Review brief — review-epic-persist-r2

**Repository**: `Nousix-LLC/nswe-demo`
**PR**: #113 — "Durable PostgreSQL persistence for chirp: provision, wire, and prove durability"
**Branch**: `work/epic-persist` → `main`
**Head at review**: `a129e2b87d8e32aa84d37e9806128ee523949bf1`
**Closes**: #65, #66, #67 (children of epic #56); #64 stays open.

## Context: what changed since the prior review

The prior review (`review-epic-persist`) delivered verdict REQUEST-CHANGES with one blocker:

> **CI-01** — the required `doc` check failed: the public doc comment on `export_user_data`
> (`crates/chirp-server/src/repository/in_memory.rs:787`) carried an intra-doc link
> `` [`ExportDocument`](super::export::ExportDocument) `` to a `pub(crate)` item in a private module,
> turning into a hard error under `RUSTDOCFLAGS: -D warnings`.

Two documentation-only commits were pushed to resolve it:

- **db1a5d6** — corrected 13 doc-comment inaccuracies: stale scaffold vocabulary, incorrect implementation
  claims, and the public→private intra-doc link that was the CI-01 blocker. Files touched: `in_memory.rs`,
  `postgres.rs`, `export.rs`, `mod.rs`, `lib.rs`, `error.rs` (documentation only).
- **a129e2b** — dropped four unresolvable explicit link paths to the feature-gated `PostgresRepository` that
  `db1a5d6` introduced; replaced with plain code spans conveying the same information without requiring the
  type to be in scope. Strictly documentation; no logic, schema, migration, `ChirpRepository` seam, or wiring
  was touched.

All CI checks are now green on `a129e2b`: fmt, clippy, test, wasm, doc, image — all SUCCESS.
`mergeStateStatus: CLEAN`.

The prior review found every code concern non-blocking. Only the doc check blocked landing.

## What this re-review must do

This re-review has a focused, bounded scope: confirm the blocker is resolved and that the fix did not
introduce new problems.

### Concern 1 — Doc-fix correctness and completeness

**Goal**: confirm that the two fix commits (db1a5d6, a129e2b) resolve CI-01 cleanly and fully.

**Bar**:
- The `doc` check passes at `a129e2b` because the private intra-doc link and the subsequent unresolvable
  feature-gated link paths are gone. Verify this is the actual state (the CI run for a129e2b has the `doc`
  job as SUCCESS).
- The prior review named two further links that could surface after the first fix: `export.rs:7`'s
  ungated→gated link and the stale scaffold rustdoc links. Confirm whether these were also addressed.
- The two commits touched only documentation. Confirm no logic, schema, API surface, migration, or
  `ChirpRepository` seam was changed.
- No new doc-lint warning was introduced by the fix commits.

A clean finding here: CI-01 is resolved, the fix is documentation-only, and no new lint issue landed.
A blocking finding: the doc check still fails at `a129e2b`, or the fix commits changed non-documentation
code in a way that introduces a new concern.

### Concern 2 — No new issues introduced

**Goal**: confirm the fix commits did not introduce any new finding that would block landing.

**Bar**:
- The changed doc comments accurately describe what the code does (the stale "scaffold stub" and
  "placeholder" language was an identified non-blocking finding, COR-20/CQ-01; confirm whether it was
  addressed and whether any newly introduced doc language is accurate or introduces a new inaccuracy).
- No security-relevant content was introduced (no host path, internal address, credential, or
  infrastructure detail committed in a doc comment).
- The plain-voice standard is met: no moral adjectives, no narrated candor, no inflated claims.
- No change to logic, schema, or API surface.

A clean finding here: the doc changes are accurate, the plain-voice standard is met, and no new concern
was introduced.

### Non-blocking findings from the prior review — not re-reviewed

The prior review's non-blocking findings (filed as backlog issues #115–#121) were evaluated in full and
all were judged non-blocking at the time. This re-review does **not** re-examine those issues. The
re-review scope is the fix commits and whether they resolve the blocker.

## Declared output

1. **Review verdict** posted as a comment on PR #113: APPROVE if both concerns are clean, REQUEST-CHANGES
   if a new blocker is found. The comment names the verdict explicitly, states what was checked, and for
   APPROVE confirms that CI-01 is resolved and no new blocker was found. For REQUEST-CHANGES, names each
   new blocker with the file, line, and required change.
2. **Root SYNTHESIS.md** at this DAG's workspace root, with:
   - the verdict (APPROVE or REQUEST-CHANGES)
   - per-concern findings (what was checked, what was found clean, any blocking finding)
   - a statement of whether the prior blocker (CI-01) is resolved
   - any new non-blocking findings, if any, with their severity and whether they should be filed as
     backlog issues (they do not hold this landing)
3. Any new non-blocking findings from the fix commits are filed as backlog issues on
   `Nousix-LLC/nswe-demo` linked to PR #113, epic #56, and the originating issue where applicable.

## Constraints

- Review scope is `work/epic-persist` at head `a129e2b` vs `main`.
- Do not re-review the non-blocking findings from the prior review (issues #115–#121). Focus on the
  fix commits.
- Findings posted to GitHub point at repository-relative file paths and line numbers. No host paths,
  cluster/SSH/credential details, or review-process internals in anything posted to the repository.
- No force-push. No changes to the codebase.
