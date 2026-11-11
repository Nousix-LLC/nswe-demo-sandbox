# _BRIEF.md — sweep-seam-r1 (swe-coder DAG)

## Objective

Close issue #117: resolve the transient sweep CronJob's second source of truth — the CronJob
currently duplicates the sweep logic as raw SQL in a manifest rather than invoking the Rust
repository seam, creating a drift risk and violating REQ-DOM-014 ("all durable state crosses
the one seam").

Repository: `Nousix-LLC/nswe-demo`
Branch: `work/sweep-seam-r1` (create from `main` at `9a24c281f1380644801e246b79b85f13a11cb33d`)
PR: open against `main` when complete, referencing issue #117.

## Background

`sweep_expired_transient_state` is a `ChirpRepository` method with a full durable Postgres
implementation (`crates/chirp-server/src/repository/postgres.rs:1618-1659`), but the deployed
sweep CronJob (`deploy/chirp/50-transient-sweep-cronjob.yaml`) re-expresses the three `DELETE`s
as raw `psql` statements. The server's Rust method and the CronJob SQL cover the same predicate
sets today (verified), but they are independent paths: a future change to the Rust sweep (e.g.
a new transient table, an altered predicate) would silently diverge from the CronJob. Tests that
exercise the Rust method cover a path that does not run in production; the SQL that actually runs
in production has no test. This also conflicts with REQ-DOM-014.

The current CronJob jobs have been failing (chirp-transient-sweep-29895480: failed: 4, succeeded: 0
as of 2026-11-03T18:00:00Z). The root cause of those failures is not confirmed, but could be
related to: DB connectivity (PGSSLMODE or credentials), the sessions table not being present, or
other reasons. Diagnose and confirm the sweep is working correctly as part of this goal.

## Acceptance criteria (from issue #117)

1. The sweep CronJob no longer duplicates the DELETE predicates as raw SQL. Either:
   - **Option A (preferred)**: introduce a `chirp-server sweep` subcommand that calls
     `sweep_expired_transient_state` on the repository and exits; update the CronJob to invoke
     it (`./chirp-server sweep` or equivalent) against the running image, removing the inline psql
     statements. The subcommand must be tested.
   - **Option B (if Option A is not feasible given the current architecture)**: keep the raw-SQL
     path but add a test that runs the CronJob's exact SQL against the real schema and asserts it
     reclaims the same rows the Rust sweep does. Add a comment in the manifest noting that
     REQ-DOM-014 is consciously scoped to exclude this ops job.
2. Whichever option is chosen, the CronJob must succeed in the cluster (verify against a running
   instance or with a dry-run that proves connectivity).
3. If the current CronJob failures have a root cause that is fixable (e.g. wrong `PGSSLMODE`,
   missing env, connectivity), fix it. Note: `PGSSLMODE: disable` → `require` is addressed in a
   separate in-flight PR (`work/security-persist-r1`); if that change conflicts or the CronJob
   needs SSL configuration, coordinate or note the dependency.
4. `sessions.expires_at` nullability: if the schema permits NULL expiry for sessions and this is
   inconsistent with the table's semantics, either make `sessions.expires_at NOT NULL` in a new
   migration, or add a comment stating the invariant and a test asserting the app never writes a
   NULL expiry. (This item is from #117 and the related #121 context.)
5. All existing tests pass. New tests added for the sweep subcommand or the SQL equivalence check.
6. PR passes CI on the branch.
7. Root `SYNTHESIS.md` accounts for each criterion (met, or not and why) and provides a pass/fail
   verdict.

## Scope

**In scope:**
- `crates/chirp-server/` — add a `sweep` subcommand to the binary; update `Cargo.toml` if needed.
- `deploy/chirp/50-transient-sweep-cronjob.yaml` — update the CronJob to use the new subcommand
  (or note the REQ-DOM-014 scope-out if Option B is chosen).
- New migration (`0003_*.sql` or later) if fixing `sessions.expires_at` nullability.
- Tests: unit/integration tests for the sweep subcommand or SQL equivalence.
- Diagnosis and fix of current CronJob failure cause if root cause is in-tree.

**Out of scope:**
- Changes to `CHIRP_DATABASE_URL` server-leg SSL configuration.
- The `PGSSLMODE` change (`disable` → `require`) — that belongs to the parallel `security-persist-r1`
  DAG on `work/security-persist-r1`. Do not merge from that branch; commit independently.
- Identity/trust or other security items beyond sweep and sessions table.
- Broader Ferric 1.0 feature work.

## Inputs

- Repository: `Nousix-LLC/nswe-demo`, main at `9a24c281f1380644801e246b79b85f13a11cb33d`
- Issue: #117 (the full issue text)
- Related issue: #121 (minor correctness — `sessions.expires_at` nullability item)
- Existing sweep CronJob: `deploy/chirp/50-transient-sweep-cronjob.yaml`
- Rust sweep method: `crates/chirp-server/src/repository/postgres.rs:1618-1659`
- In-flight parallel PR: `work/security-persist-r1` (KDF credential hashing + `PGSSLMODE: require`)

## Declared output

- Commits on `work/sweep-seam-r1`.
- PR against `main` referencing issue #117 (and #121 if the sessions.expires_at item is addressed).
- Root `SYNTHESIS.md` with a pass/fail verdict and an accounting for each acceptance criterion.

## Constraints

- Do not force-push `main`.
- Do not merge from `work/security-persist-r1`; commit independently to `work/sweep-seam-r1`.
- No attribution trailers in PR descriptions, issue comments, or commit messages.
- Stay within the scope of `Nousix-LLC/nswe-demo` repository.
