# _BRIEF.md — security-persist-r1 (swe-coder)

## Objective

Harden the persistence layer against two security exposures filed as follow-ups to PR #113 (durable
PostgreSQL persistence). Both are priority:high. Neither is a regression introduced by PR #113 — they follow
from the persistence change making latent risks durable.

## Repository

`Nousix-LLC/nswe-demo` — branch `work/security-persist-r1` (create from current `main`, SHA
`a255baf825e3fe3c63d4ffdb98d7cfe0b1e1f99d`). Do not force-push; one PR that closes the issues this DAG
finishes, declared output a root `SYNTHESIS.md`.

## Issues covered

### Issue #120 — persistence security follow-ups (priority:high)

**Concern 1 — Credential stored as plaintext; verified with non-constant-time compare**

`credentials.secret` is stored verbatim and verified with `stored == secret` — a non-constant-time equality
check and a credential-exposure risk: anyone with store/backup read access learns every password in the
clear. Persistence makes this durable risk, not just in-process risk.

- Locations:
  - `crates/chirp-server/src/repository/postgres.rs:928` — `stored == secret` compare
  - `crates/chirp-server/src/repository/postgres.rs:842-887`, `:1065-1125` — stored verbatim
  - `crates/chirp-server/src/repository/in_memory.rs:540,564` — mirrored in the in-memory store
- Acceptance criterion: route credential storage through a salted password-hashing KDF (argon2 or bcrypt) and
  replace the equality compare with a constant-time verify (e.g. `argon2::verify_encoded`). Both stores must
  be consistent. Existing accounts in a running system do not need automatic migration — a migration path is
  acceptable, but new credentials written after the change must always be hashed. Tests that verify the login
  path must pass with the new hashing in place. No production credentials exist yet (the store was just
  deployed), so backward compatibility with existing hashed rows is not required.

**Concern 2 — CronJob connects to PostgreSQL without TLS**

`deploy/chirp/50-transient-sweep-cronjob.yaml` sets `PGSSLMODE: disable`, so the sweep's connection —
carrying the DB password from the Secret — is plaintext on the pod network. The server's TLS posture is
governed by the out-of-band `CHIRP_DATABASE_URL`, which is not in the tree, but the manifest should document
and enforce the expected posture.

- Location: `deploy/chirp/50-transient-sweep-cronjob.yaml:103-104` (`PGSSLMODE: disable`)
- Acceptance criterion: remove `PGSSLMODE: disable` from the CronJob manifest and replace with
  `PGSSLMODE: require` (or stricter). Add a comment in the server Deployment manifest noting that
  `CHIRP_DATABASE_URL` must carry `sslmode=require` (or stricter) when deployed against a TLS-enabled
  PostgreSQL instance. The k3d dev cluster uses plain TCP for postgres (the `chirp-postgres` StatefulSet does
  not have TLS configured), so the runtime test verifies that the manifest change is applied; disabling for
  a no-TLS dev cluster is acceptable if gated by a documented override. If the manifest change would break
  the existing cluster deployment, document the caveat and apply the change in a way that does not regress
  the running system.

## Scope and non-goals

- Scope: `crates/chirp-server/src/repository/` (both stores), `deploy/chirp/50-transient-sweep-cronjob.yaml`,
  and the server Deployment manifest comment. Tests in `crates/chirp-server/` that exercise the login path.
- Non-goals: the full identity/trust epic (#83, #47), a full TLS-for-PostgreSQL setup in the dev cluster
  (the Postgres StatefulSet does not have TLS configured and that is out of scope), session token rotation,
  or any other issue not listed above.
- No force-push on any branch.

## Constraints

- No attribution trailers in GitHub issues, PR bodies, or review comments.
- The brief describes the work; select and load your own methodologies for the concerns you identify.
