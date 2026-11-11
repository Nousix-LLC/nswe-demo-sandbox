# COMPLETE — SUBTASK_security — PR #113 @ 09fa453

## What was done

Reviewed PR #113 (`Nousix-LLC/nswe-demo#113`, head `09fa453`) through the security / trust-boundary
lens, read-only, and wrote one findings document conforming to `../contracts/finding_schema.md`
(prefix `SEC`). All five mandated areas assessed:

1. **Credential handling for `CHIRP_DATABASE_URL`** — sourced only from the out-of-band
   `chirp-db-credentials` Secret via `secretKeyRef`; nothing committed; never logged (verified in
   `main.rs`, `postgres.rs`, the manifests); AppProject excludes `Secret` from both whitelists.
   Clean.
2. **SQL / injection at the store boundary** — all 78 `sqlx::query*` sites parameterized (`$N` +
   `.bind`), no dynamic SQL / `QueryBuilder` / `raw_sql` / `unsafe`; `export.rs` is pure
   serialization. Clean.
3. **Migration safety** — `0001`/`0002` idempotent `IF NOT EXISTS` DDL, forward-only, non-destructive,
   version-tracked, applied before serving; `replicas: 1` avoids a migrator race. Clean.
4. **Pod Security `restricted` admission** — StatefulSet, Deployment, and sweep CronJob all satisfy
   restricted (`readOnlyRootFilesystem` correctly omitted on Postgres with accurate justification).
   Clean.
5. **Dependency / feature pull-ins** — 147 added `Cargo.lock` crates, all registry-sourced +
   checksummed (no git/path sources), the expected `sqlx 0.8` + `rustls` tree; `postgres` feature off
   by default; Dockerfile `--locked`, distroless non-root, no build-time credential. Clean.

## Findings (both non-blocking)

- **SEC-01** (major, blocks_landing=false): durable store persists the login secret verbatim and
  verifies with non-constant-time `==`. Live via `POST /api/sessions`, but faithfully mirrors the
  pre-existing in-memory seam (#66 parity) and the hashing protocol is deferred to `REQ-ID-*` by
  design — not a regression, not grounds to block a persistence PR. Backlog follow-up.
- **SEC-02** (minor, blocks_landing=false): DB credential crosses the in-cluster network unencrypted
  (sweep CronJob `PGSSLMODE: disable`; server TLS unverifiable from the tree). Documented hardening
  follow-up. Backlog.

## Sub-verdict

**NON-BLOCKING-ONLY.** No security-blocking finding: no exposure, no committed or loggable secret,
no injection surface, non-destructive migrations, restricted admission satisfied.

## Output

- `SUBTASK_security/outputs/findings.md`

## Constraints honored

Read-only on the repo; no GitHub writes. No host/cluster/SSH/credential details, no DAG internals,
and no secret values in the findings. Plain-voice finishing pass run (removed the moral-adjective
"real" tells).
