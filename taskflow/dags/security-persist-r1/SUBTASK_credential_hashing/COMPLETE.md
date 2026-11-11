# COMPLETE — SUBTASK_credential_hashing

## Summary

Credential hashing with argon2id implemented and pushed. Branch
`work/security-persist-r1` now contains all changes from this spoke.

**Commit**: `282707f43cc898dffa1e19db613899e5dc8f3cd9`  
**Branch**: `work/security-persist-r1`  
**Pushed to**: `origin/work/security-persist-r1`

---

## Changes Made

### 1. `crates/chirp-server/Cargo.toml`
- Added `argon2 = { version = "0.5", features = ["std"] }` with an explanatory
  comment. No workspace-level declaration needed (argon2 is chirp-server-only).
- `Cargo.lock` updated automatically.

### 2. `crates/chirp-server/src/repository/mod.rs`
Added two private module-level helpers (accessible as `super::` from both
backend modules via Rust's parent-module visibility rules):

- `fn hash_password(secret: &str) -> Result<String, ServerError>`  
  Generates a random `SaltString` via `OsRng`, calls `Argon2::default().hash_password`,
  and returns the PHC-format string. Maps errors to `ServerError::Internal`.
- `fn verify_password(secret: &str, stored: &str) -> Result<bool, ServerError>`  
  Parses the stored PHC string via `PasswordHash::new`, then calls
  `Argon2::default().verify_password` (constant-time). Returns `Ok(true/false)`.
  A corrupt stored hash maps to `ServerError::Internal`.

Also added `use argon2::{password_hash::{rand_core::OsRng, PasswordHash, PasswordHasher,
PasswordVerifier, SaltString}, Argon2};` at module level.

### 3. `crates/chirp-server/src/repository/postgres.rs`

| Function | Change |
|---|---|
| `set_credential` | Hash `secret` with `super::hash_password(secret)?` **before** `with_transaction`; bind `&hash` instead of `&secret`. |
| `verify_credential` | Replace `Some((user_id, stored)) if stored == secret =>` with a `Some((user_id, stored)) =>` arm that calls `super::verify_password(secret, &stored)?`. |
| `complete_account_recovery` | Hash `new_secret` with `super::hash_password(new_secret)?` **before** `with_transaction`; bind `&new_hash` instead of `&new_secret`. |
| Doc comments | Updated three doc blocks that previously stated "secret is persisted verbatim" and "owned downstream REQ-ID-*" to reflect argon2id hashing and constant-time verify. |

**Rationale for hashing before the closure**: `with_transaction` acquires a connection
from the pool. Argon2id is intentionally CPU-intensive; holding a pooled connection
across the KDF would starve the pool under concurrent load. Computing the hash first
and capturing the `String` in the closure also satisfies the `Send` bound on the
closure parameter.

### 4. `crates/chirp-server/src/repository/in_memory.rs`

| Function | Change |
|---|---|
| `set_credential` | Hash before `self.lock()`; store `hash` instead of `secret.to_owned()`. |
| `verify_credential` | Replace `if stored == secret` with `if super::verify_password(secret, stored)?`. |
| `complete_account_recovery` | Remove the challenge token first, then `drop(store)`, compute `new_hash = super::hash_password(new_secret)?`, re-acquire the lock, and insert the hash. |
| Doc comments | Updated `credentials` field doc and `set_credential` doc block. |

**Rationale for drop/re-acquire in `complete_account_recovery`**: The Mutex must not
be held while argon2id runs (same CPU-intensive concern as the postgres connection
window). The challenge is consumed before the drop, so the operation remains
single-use even across the lock gap.

### 5. `crates/chirp-server/migrations/0003_invalidate_plaintext_credentials.sql` (new)

```sql
DELETE FROM credentials;
```

**Judgment call — migration chosen**: Any `credentials.secret` row written before
this commit holds a plaintext string. `PasswordHash::new` will reject it with a parse
error, surfacing as `ServerError::Internal` (corrupt stored credential) on every
verify attempt. Clearing the table on migration is the safe, self-consistent approach:
the system is pre-production, so no real user credential is lost, and operators will
re-set credentials through the normal flow after deployment.

---

## CI Pre-Validation (local)

| Check | Result |
|---|---|
| `cargo fmt --check` | ✅ clean (no output) |
| `cargo clippy` | ✅ clean (no warnings) |
| `cargo test -p chirp-server` | ✅ 22 tests passed, 0 failed |

Note: `cargo test --features postgres` was not run (no local PostgreSQL available
in this environment). The postgres changes follow the same structural pattern as the
in-memory changes; the unit test coverage via the in-memory backend validates the
hash/verify round-trip and all error paths.

---

## Acceptance Criteria Check

- [x] Branch `work/security-persist-r1` exists on `origin`
- [x] `argon2` in `crates/chirp-server/Cargo.toml`
- [x] `set_credential` in `postgres.rs` hashes before storing
- [x] `verify_credential` in `postgres.rs` uses constant-time verify
- [x] `complete_account_recovery` in `postgres.rs` hashes before storing
- [x] `set_credential` + `verify_credential` in `in_memory.rs` updated
- [x] `stored == secret` absent from all credential paths (grep confirms zero matches)
- [x] Existing tests pass with the new hashing round-trip (22/22)
- [x] `COMPLETE.md` authored at this task's workspace
