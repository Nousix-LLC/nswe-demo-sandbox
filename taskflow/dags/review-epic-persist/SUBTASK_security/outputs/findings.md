# Findings — Security and trust boundaries — PR #113 @ 09fa453

## What I checked

- **Credential handling for `CHIRP_DATABASE_URL`** — the whole supply path and every place it
  could leak:
  - `crates/chirp-server/src/main.rs:97-105` (`durable_database_url`) — how the URL is read from the
    environment, and `:68-95` / `:40-53` — whether the value is ever logged.
  - `crates/chirp-server/src/repository/postgres.rs:80-96` (`connect`) — the URL only flows into
    `PgPoolOptions::connect(database_url)`; grepped the whole file for any `tracing::*` /
    `format!` that stringifies the URL or a password (none outside tests).
  - `deploy/chirp/10-deployment.yaml:68-79` — the pod sources `CHIRP_DATABASE_URL` from a
    `secretKeyRef`, not an inline value.
  - `deploy/chirp/40-postgres-statefulset.yaml:83-102` and `deploy/chirp/50-transient-sweep-cronjob.yaml:93-121`
    — DB name/user/password come from the same out-of-band `secretKeyRef`s.
  - `deploy/argocd/appproject.yaml:51-94` — whether `Secret` is syncable through GitOps.
  - Scanned the whole diff for any committed credential literal in source or manifests.
- **SQL / injection & input handling at the store boundary** — every query-construction site in
  `crates/chirp-server/src/repository/postgres.rs` (78 `sqlx::query*` call sites): literal SQL vs
  string-built SQL, `.bind()` parameterization, `QueryBuilder` / `raw_sql` / `format!`-into-SQL,
  dynamic identifiers, `unsafe`. Read `verify_credential` (`:905-935`) and the credential writes
  (`:842-887`, `:1065-1125`) specifically. Read `crates/chirp-server/src/repository/export.rs`
  (export-document assembly) for an injection/path surface.
- **Migration safety** — `crates/chirp-server/migrations/0001_baseline.sql`,
  `0002_domain_schema.sql`, and the runner at `postgres.rs:45-96` (`sqlx::migrate!()` +
  `MIGRATOR.run`): forward-only, idempotent, version-tracked, destructive statements, when they run
  relative to serving, and concurrent-migrator races against the deployment's replica count.
- **Pod Security `restricted` admission** — the pod/container `securityContext` of all three
  workloads against the restricted profile's controls: `deploy/chirp/40-postgres-statefulset.yaml:57-148`,
  `deploy/chirp/10-deployment.yaml:41-124`, `deploy/chirp/50-transient-sweep-cronjob.yaml:61-141`.
- **Dependency / feature pull-ins** — the `Cargo.lock` delta (147 added crates): the source of each
  (registry vs git/path), integrity checksums, the shape of the `sqlx 0.8` + TLS tree, and whether
  the `postgres` feature stays off by default (`crates/chirp-server/Cargo.toml:26-75`). Read the
  `Dockerfile` delta for build-time credential/root surface. Read `crates/chirp-server/src/error.rs`
  for server-detail leakage to HTTP clients.
- **Live reachability** — `crates/chirp-server/src/api/router.rs:64-79` to see which of these paths
  is wired to a serving route, and `crates/chirp-server/src/repository/in_memory.rs:550-571` to
  compare the durable credential semantics against the pre-existing in-memory seam (#66 parity).

## What I found clean

- **No committed or logged database credential.** `CHIRP_DATABASE_URL` is sourced only from the
  out-of-band `chirp-db-credentials` Secret via `secretKeyRef` (`10-deployment.yaml:75-79`); no value
  is in the tree. `main.rs` selects and connects the durable backing without ever logging the URL
  (`main.rs:72-78`, `postgres.rs:80-96`), and `postgres.rs` never stringifies the URL or a password
  anywhere outside tests. The ArgoCD AppProject **excludes `Secret` from both whitelists**
  (`appproject.yaml:51-94`) — defense in depth: even an accidentally committed Secret could not
  be synced by this project.
- **No injection surface at the store boundary.** All 78 `sqlx::query*` sites use literal SQL with
  `$N` placeholders and `.bind()`; there is no `QueryBuilder`, `raw_sql`, string-concatenated SQL, or
  `format!`-into-SQL, and no `unsafe`. `verify_credential` binds the handle as a parameter in its
  JOIN (`postgres.rs:911-916`). `export.rs` is pure `serde_json` serialization with a deterministic
  order — no filesystem, path, or shell surface.
- **Migrations are safe to apply unattended.** `0001`/`0002` are entirely `CREATE … IF NOT EXISTS`
  (tables, indexes, sequences) plus `INSERT … ON CONFLICT DO NOTHING` — idempotent, forward-only,
  and carrying **no** `DROP` / `TRUNCATE` / `DELETE` / destructive `ALTER`. The runner applies the
  compile-time-embedded set before the repository is handed to the transport layer
  (`postgres.rs:67-96`), and a migration failure is surfaced as a failed startup, never swallowed.
  The app tier is `replicas: 1` (`10-deployment.yaml:20`), so there is no concurrent-migrator race
  this release.
- **All three workloads satisfy `restricted`.** Postgres StatefulSet: `runAsNonRoot`, `runAsUser 70`,
  `drop: [ALL]`, `allowPrivilegeEscalation: false`, `seccompProfile: RuntimeDefault`,
  `automountServiceAccountToken: false` (`40-postgres-statefulset.yaml:57-145`). The decision to
  leave `readOnlyRootFilesystem` unset is correct and accurately justified — restricted does not
  require it (it is an extra NSA/CISA hardening control), and the official postgres entrypoint writes
  outside the data volume. chirp-server Deployment and the sweep CronJob go further with
  `readOnlyRootFilesystem: true` plus the same non-root/drop-all/no-priv-esc/RuntimeDefault/no-SA-token
  posture (`10-deployment.yaml:47-121`, `50-transient-sweep-cronjob.yaml:61-138`).
- **No server-side detail leaks to clients.** `error.rs:216-240` logs the detailed message of
  `Internal` / `Unavailable` (which stringify a `sqlx` error) at `error` level server-side, but
  returns a deliberately generic body (`"an internal server error occurred"`) to the HTTP caller.
- **Dependency pull-ins are the expected, verified `sqlx` tree.** All 147 added `Cargo.lock` crates
  are registry-sourced (`registry+https://github.com/rust-lang/crates.io-index`) with integrity
  checksums — there is **no git or path source** introduced (no supply-chain side-door). The tree is
  the standard `sqlx 0.8` + `rustls` stack (`rustls`, `rustls-webpki`, `ring`, `webpki-roots`;
  `hmac`/`sha2`/`md-5` for the Postgres SCRAM/MD5 auth handshake); TLS is `tls-rustls` with
  `default-features = false` (no OpenSSL/system-TLS surface, `Cargo.toml:69-75`). The `postgres`
  feature is **off by default**, so the default build and the test suite compile none of it. The
  `Dockerfile` builds `--locked` (no silent dependency drift), targets a distroless non-root runtime,
  bakes in no secret, and needs no database or credential at build time (migrations are embedded from
  local `.sql`; queries are runtime, not compile-time macros).

## Findings

### SEC-01 — Durable store persists the login secret verbatim and verifies it with a non-constant-time equality
- **severity**: major
- **blocks_landing**: false
- **location**: `crates/chirp-server/src/repository/postgres.rs:928` (`stored == secret`),
  `:842-887` and `:1065-1125` (secret bound and stored verbatim) @ 09fa453; mirrored at
  `crates/chirp-server/src/repository/in_memory.rs:540,564` @ 09fa453
- **acceptance-criterion / design ref**: n/a to #65/#66/#67 — the credential/verification protocol is
  explicitly owned by the identity & trust work (`REQ-ID-*`), per the method and schema docs
  (`postgres.rs:833-835,896-900`; `migrations/0002_domain_schema.sql:69-77`)
- **principle**: an at-rest authentication secret should be stored as a salted one-way hash and
  verified with a constant-time comparison; plaintext storage plus `==` is both a credential-exposure
  risk (anyone with store/backup read access learns every password) and a timing side channel.
- **why it matters here**: the path is live — `POST /api/sessions` → `handlers::login`
  (`router.rs:72`) reaches `verify_credential`, so user-supplied secrets are compared this way. The
  durable store did not *weaken* anything: it faithfully mirrors the pre-existing in-memory seam
  (`in_memory.rs:564`), which is exactly the #66 "no capability weakened" parity requirement, and the
  hashing protocol is deferred to `REQ-ID-*` by design. It is therefore **not a regression this PR
  introduces, and not grounds to block a persistence PR** — but persistence makes the plaintext
  secret durable (it now survives in a backup-able store, not just process memory), so the latent
  risk is worth a tracked follow-up that must close before production credentials flow.
- **confidence**: verified
- **what would satisfy me**: a backlog item, linked to the identity/trust epic, to route credential
  storage through a salted password hash (e.g. argon2/bcrypt) and a constant-time verify before any
  production credential is accepted; no change required in this PR.

### SEC-02 — DB credential crosses the in-cluster network unencrypted
- **severity**: minor
- **blocks_landing**: false
- **location**: `deploy/chirp/50-transient-sweep-cronjob.yaml:103-104` (`PGSSLMODE: disable`) @
  09fa453; server-side connection TLS is governed by the `sslmode` of the out-of-band
  `CHIRP_DATABASE_URL`, which is not in the tree
- **acceptance-criterion / design ref**: n/a — the manifests note TLS-in-transit as a documented
  hardening follow-up (`50-transient-sweep-cronjob.yaml:96-98`)
- **principle**: the database password and all row data should not traverse the pod network in
  cleartext; a shared or multi-tenant cluster network can observe it.
- **why it matters here**: the sweep CronJob explicitly disables TLS (`PGSSLMODE: disable`), so its
  connection — carrying `PGPASSWORD` from the Secret — is plaintext on the wire. For a
  single-namespace k3d demo the blast radius is small, but the posture is worth recording so it is
  not forgotten when the store moves to a shared cluster.
- **confidence**: verified for the CronJob; suspected for the chirp-server connection — I cannot see
  the `sslmode` of the out-of-band connection string, so I cannot confirm whether the server itself
  requires TLS. The question that settles it: does the `CHIRP_DATABASE_URL` in `chirp-db-credentials`
  carry `sslmode=require` (or stricter)?
- **what would satisfy me**: a backlog item to require TLS in transit for both the server and the
  sweep connections (`sslmode=require`/`verify-full` and dropping `PGSSLMODE: disable`) as the
  documented follow-up lands; no change required in this PR.

## Concern sub-verdict
- **NON-BLOCKING-ONLY**
- The security-blocking bar — an exposure, or a committed/loggable secret — is not met: the DB
  credential is out-of-band, uncommitted, unlogged, and the AppProject cannot sync a Secret; the
  store boundary has no injection surface; migrations are non-destructive; and all three workloads
  satisfy `restricted`. The two findings (verbatim/`==` credential handling, deferred to `REQ-ID-*`
  and pre-existing; plaintext DB traffic in-cluster, a documented follow-up) are trust-boundary
  items for the backlog, neither introduced nor worsened by this persistence change.
