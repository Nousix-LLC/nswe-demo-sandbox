# security-persist-r1 — Persistence Security Follow-Ups

## Project Context

**Status**: Active  
**Branch**: `work/security-persist-r1`  
**Refs**: Issue #120, PR #113, epic #56

### Objective

Close two security concerns surfaced during the PR #113 review of the durable PostgreSQL persistence
layer, before any production credential is accepted:

1. **Credential at rest**: The durable store persists `credentials.secret` as plaintext and verifies
   it with a non-constant-time equality (`stored == secret`). Fix: route credential storage through a
   salted password-hashing KDF (argon2id) and use a constant-time verify.

2. **In-cluster DB traffic**: The sweep CronJob sets `PGSSLMODE: disable`, transmitting the DB
   password in plaintext on the pod network. Fix: set `PGSSLMODE: require`.

### Scope

**In scope:**
- Introduce `argon2` crate; update `set_credential` and `verify_credential` in
  `crates/chirp-server/src/repository/postgres.rs` and `in_memory.rs`; also update the
  `complete_account_recovery` path in `postgres.rs` which calls the same credential upsert verbatim
- Change `PGSSLMODE: disable` → `PGSSLMODE: require` in
  `deploy/chirp/50-transient-sweep-cronjob.yaml`; update the stale comment
- A new forward migration (`0003_*.sql`) to invalidate existing plaintext credentials if needed
- Update existing unit/integration tests that compare passwords to use the new hash round-trip
- Create PR for `work/security-persist-r1` → `main` referencing issue #120

**Out of scope:**
- Changes to `CHIRP_DATABASE_URL` server-leg SSL (out-of-band, not in-tree)
- Identity/trust epic (REQ-ID-*) changes beyond the KDF replacement
- Broader security hardening beyond the two explicit follow-up items

### Success Criteria

- [ ] All stored credential writes (`set_credential`, `complete_account_recovery`) hash via argon2id
- [ ] `verify_credential` uses `argon2::verify_password` (constant-time)
- [ ] `PGSSLMODE: disable` is gone from the CronJob manifest
- [ ] All CI checks (`doc`, `clippy`, `fmt`, `test`, `wasm`) are green on the security branch
- [ ] PR opened referencing issue #120, with a clear description of both fixes

---

## Repository Facts (for child tasks)

| Fact | Value |
|------|-------|
| Repo | `Nousix-LLC/nswe-demo` |
| Base branch | `main` (at commit `9a24c28` after PR #113 merge) |
| New branch | `work/security-persist-r1` (to be created from `origin/main`) |
| Server repo path (on build server) | `~/nswe-demo` |
| Workspace Cargo.toml | `Cargo.toml` (workspace root) |
| chirp-server Cargo.toml | `crates/chirp-server/Cargo.toml` |
| postgres repository | `crates/chirp-server/src/repository/postgres.rs` |
| in_memory repository | `crates/chirp-server/src/repository/in_memory.rs` |
| Migrations dir | `crates/chirp-server/migrations/` |
| CronJob manifest | `deploy/chirp/50-transient-sweep-cronjob.yaml` |
| `credentials` table | `TEXT NOT NULL secret` — no size limit; argon2 hashes (~97 chars) fit without a schema migration |
| Plaintext-vs-hash migration | A `DELETE FROM credentials` migration (new migration file) is the cleanest pre-production path; child task owns the judgment |

---

## Task Structure

### Subtree

```
_GLOBAL.md (this document)
├── contracts/
│   └── _MANIFEST.yaml
├── SUBTASK_credential_hashing/
│   └── _BRIEF.md
├── SUBTASK_ssl_manifest/
│   └── _BRIEF.md
└── SUBTASK_synthesis/
    └── _BRIEF.md
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_credential_hashing` | none | Add argon2 dep; replace plaintext store + non-CT compare with salted KDF + constant-time verify; update tests; create and push branch | `COMPLETE.md` |
| `SUBTASK_ssl_manifest` | `SUBTASK_credential_hashing` | Change PGSSLMODE from disable to require; commit to the existing branch | `COMPLETE.md` |
| `SUBTASK_synthesis` | `SUBTASK_ssl_manifest` | Verify combined changes; open the PR; write SYNTHESIS.md fold record | `SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_credential_hashing
        │
        ▼
SUBTASK_ssl_manifest
        │
        ▼
SUBTASK_synthesis
```

---

## Subtree Methodology Posture

**Dominant task types**: Writing Rust code (spoke 1) + Kubernetes CronJob manifest hardening (spoke 2)

**Primary bundles**:
- `security` — `Security_Secure_Coding_Methodology.md` (credential hashing, constant-time compare)
- `core` — `BestPractices_Coding_Standards_Methodology.md`, `BestPractices_Error_Handling_Methodology.md`
- `kubernetes` — `K8s_Configuration_Management_Methodology.md` (manifest spoke)
- `synthesis` — `Synthesis_Overview_Methodology.md` (synthesis gate)

**Cross-cutting constraints**:
- Branch all work on `work/security-persist-r1` (create from `origin/main`)
- All five CI checks (`doc`, `clippy`, `fmt`, `test`, `wasm`) must pass
- Never commit secrets; DB credential supplied out-of-band
- Follow existing commit-message conventions (`fix(security): ...`)
- Use `argon2` crate at `0.5`; feature `std`; DO NOT use `bcrypt` (argon2id is the documented choice)

---

## Subtree-Wide Constraints

1. **argon2 only**: The brief specifies argon2. Use `argon2 = { version = "0.5", features = ["std"] }`.
2. **No production credentials**: The DB is pre-production; existing plaintext credential rows must be invalidated (migration or by design choice) before any real user re-sets their password.
3. **Constant-time requirement**: `argon2::PasswordVerifier::verify_password` is inherently constant-time. Do NOT use `==` for any credential comparison after this fix.
4. **No schema change needed**: The `credentials.secret` column is `TEXT NOT NULL` (unconstrained length). Argon2 PHC strings are ~97 chars and fit without a schema migration.
5. **Git sequencing**: `SUBTASK_ssl_manifest` depends on `SUBTASK_credential_hashing` purely for git ordering so both write to the same branch serially without conflict.
6. **Commit messages**: `fix(security): ...` prefix, consistent with project history.
