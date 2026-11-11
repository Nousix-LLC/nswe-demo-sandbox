# Task: Credential Hashing — argon2id KDF + Constant-Time Verify

## Task Specification

**Slug**: SUBTASK_credential_hashing  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

Replace the plaintext credential storage and non-constant-time comparison in
`chirp-server`'s durable (PostgreSQL) and in-memory repositories with a salted argon2id KDF
on write and a `PasswordVerifier::verify_password` constant-time check on read. Create and push
the `work/security-persist-r1` branch with these changes committed and CI-clean.

### Context

This is spoke 1 of 3 in the `security-persist-r1` subtree (see parent `_GLOBAL.md`). Issue #120
(PR #113 review follow-up) documents this as a pre-production blocker: the durable store persists
`credentials.secret` verbatim, and `verify_credential` uses `stored == secret` — a plaintext-at-rest
risk and a timing side channel. This spoke owns all credential-hashing changes in the Rust codebase.

**Dependencies**: none (first spoke; creates the branch)  
**Dependents**: `SUBTASK_ssl_manifest`, `SUBTASK_synthesis`

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Repository facts, constraints, branch name |
| postgres.rs | `crates/chirp-server/src/repository/postgres.rs` | Location of `set_credential` (~842), `verify_credential` (~900), `complete_account_recovery` (~1060) |
| in_memory.rs | `crates/chirp-server/src/repository/in_memory.rs` | Location of `set_credential` (~535), `verify_credential` (~552) |
| chirp-server Cargo.toml | `crates/chirp-server/Cargo.toml` | Where to add argon2 dependency |
| Workspace Cargo.toml | `Cargo.toml` | Workspace context |
| Migrations dir | `crates/chirp-server/migrations/` | Whether a new migration is needed |
| Issue #120 | GitHub issue | Exact fix description and acceptance criteria |

All inputs are on the build server at `~/nswe-demo`. Access via:
```bash
ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 'bash -lc "..."'
```

---

## Process

This task's scope and how to approach it:

1. **Create branch** `work/security-persist-r1` from `origin/main` on the build server
2. **Add `argon2` dependency** to `crates/chirp-server/Cargo.toml`:
   `argon2 = { version = "0.5", features = ["std"] }`  
   No workspace-level dep needed (argon2 is only used by chirp-server).
3. **Update `set_credential`** in `postgres.rs` and `in_memory.rs`: hash the secret with argon2id before storage. The `credentials.secret` column is `TEXT NOT NULL` (unconstrained) — no schema migration needed for the column itself.
4. **Update `verify_credential`** in both files: replace `stored == secret` with `argon2::PasswordVerifier::verify_password(secret.as_bytes(), &PasswordHash::new(&stored)?)` which is constant-time.
5. **Update `complete_account_recovery`** in `postgres.rs`: it calls the same credential upsert verbatim — must hash `new_secret` before binding it.
6. **Migration strategy**: The `credentials` table may hold plaintext rows from prior testing. Clean approach: add a new migration `0003_invalidate_plaintext_credentials.sql` with `DELETE FROM credentials;` so no plaintext row survives to confuse the hash verifier. Alternatively, simply document that credentials must be re-set. Child agent owns the judgment — prefer the migration if it keeps the system self-consistent.
7. **Update tests**: Existing unit tests in both files that set and verify credentials with literal strings will still pass with argon2 (hash+verify round-trips correctly). If any test does a raw string equality on the stored value (e.g. `assert_eq!(stored_secret, "password")`), update it to verify via the repo API instead. Integration tests that go through the HTTP API are unaffected.
8. **Commit** with message `fix(security): hash credentials with argon2id; constant-time verify (#120)` (or close variant)
9. **Push** the branch to `origin`

### Quality criteria

- `stored == secret` must not appear in any credential path after this change
- `verify_password` or equivalent constant-time check must be used
- All five CI checks must be green (run `cargo fmt --check`, `cargo clippy`, `cargo test --features postgres` locally where possible to pre-validate)
- Commit message references `#120`

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| File | `COMPLETE.md` |
| Location | `SUBTASK_credential_hashing/` |

### COMPLETE.md contents

Record:
- What was changed (files, lines), what was added (dependency, migration if any)
- Any judgment calls made (e.g. migration strategy chosen)
- Git commit SHA pushed to `origin/work/security-persist-r1`
- Whether CI was pre-checked locally

---

## Success Criteria

- [ ] Branch `work/security-persist-r1` exists on `origin`
- [ ] `argon2` in `crates/chirp-server/Cargo.toml`
- [ ] `set_credential` in `postgres.rs` hashes before storing
- [ ] `verify_credential` in `postgres.rs` uses constant-time verify
- [ ] `complete_account_recovery` in `postgres.rs` hashes before storing
- [ ] `set_credential` + `verify_credential` in `in_memory.rs` updated (for consistency)
- [ ] `stored == secret` is absent from all credential paths
- [ ] Existing tests pass with the new hashing round-trip
- [ ] `COMPLETE.md` authored at this task's workspace

---

## Suggested Methodology Files

**Task type match**: "Writing Rust code" → primary: `rust`, supporting: `core`, `code-quality`; "Security review" → primary: `security`, supporting: `code-review`

**Specific files to load**:
- `security/Security_Secure_Coding_Methodology.md` — credential hashing, constant-time compare, password storage patterns. **Rationale**: direct match — this methodology covers KDF selection (argon2id vs bcrypt), PHC string format, and the timing side-channel that makes `==` dangerous for secrets.
- `core/BestPractices_Error_Handling_Methodology.md` — argon2 error propagation into `ServerError::Internal`. **Rationale**: the hash and verify functions return `Result`; mapping them cleanly through the error boundary matters.
- `core/BestPractices_Coding_Standards_Methodology.md` — comment / doc conventions, since the credential doc blocks reference `REQ-ID-*` ownership statements that need updating. **Rationale**: existing docs say "secret is stored verbatim" which will be false after this change.

*These are the parent's flagged methodologies based on the task type. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.*

## Inherited Constraints

- Use `argon2 = { version = "0.5", features = ["std"] }`. Do not use `bcrypt`.
- Do NOT commit secrets or the out-of-band DB credential.
- The `credentials.secret` column is `TEXT NOT NULL` with no length constraint — no ALTER TABLE migration needed.
- Branch name is exactly `work/security-persist-r1`.
- Commit message convention: `fix(security): ...` prefix; reference `#120`.
- Never force-push to `main`.
