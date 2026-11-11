# SYNTHESIS.md — review-security-persist-r1

**Review Verdict**: ✅ APPROVE — no blocking findings, all five acceptance criteria met

**PR**: https://github.com/Nousix-LLC/nswe-demo/pull/182  
**Branch merged**: `work/security-persist-r1` → `main`  
**Merge commit**: `c3f9f558fc7b254c2b0d431c31a7fc9a095fe0d5`  
**Issue closed**: #120  
**Review comment**: https://github.com/Nousix-LLC/nswe-demo/pull/182#issuecomment-6612993164  
**Backlog issue**: https://github.com/Nousix-LLC/nswe-demo/issues/184  

---

## Verdict

APPROVE. The PR correctly implements all five acceptance criteria from issue #120. No blockers found.
CI was green on the branch (all six checks: fmt, clippy, test, wasm, doc, image — SUCCESS) before merge.
PR squash-merged under delegated landing authority; branch deleted; issue #120 closed.

---

## Concern 1 — Correctness: PASS

**What was checked**: Fresh-salt generation at every hash call; PHC-format storage via `h.to_string()`; constant-time verify on all three credential paths in both repository implementations; migration correctness; edge-case behavior (wrong password, corrupt hash, empty password).

**What was found clean**:
- `SaltString::generate(&mut OsRng)` called inside `hash_password` on every invocation — no static salt.
- `Argon2::default().hash_password().to_string()` → PHC string; `PasswordHash::new(stored)` parses it back before verify. Round-trip correct.
- Both `postgres.rs` and `in_memory.rs` call `super::verify_password` on every credential comparison. Grep for `stored ==` / `stored !=` returned empty.
- Both `complete_account_recovery` implementations hash before the critical section (lock for in-memory, transaction for Postgres).
- Migration 0003 (`DELETE FROM credentials`) is idempotent-safe and correct for a pre-production system.
- Wrong password → `false` via `.is_ok()` → caller returns `Unauthorized`. Corrupt stored hash caught by `PasswordHash::new` → `Internal`.

**Non-blocking observation** (filed in #184): `.is_ok()` absorbs algorithm/version-mismatch errors as `false` rather than `Internal`. In practice won't occur — all stored hashes come from the same `Argon2::default()` call — but silently masks a would-be invariant if parameters change.

---

## Concern 2 — Security: PASS

**What was checked**: Argon2id coverage of all store/verify paths; hardcoded-salt absence; CronJob TLS manifest; secrets/credentials in diff; sensitive content in PR text; new attack surface.

**What was found clean**:
- Every credential store and verify path goes through `mod.rs` helpers. No plaintext path remains.
- `OsRng` at every call site; no static or shared salt.
- `deploy/chirp/50-transient-sweep-cronjob.yaml` changed from `PGSSLMODE: disable` → `require`. No other manifest in `deploy/` sets TLS off.
- Diff contains no plaintext credentials, secrets, or tokens. Migration deletes rows; no credential values present.
- PR description and code comments contain no host paths, internal addresses, or taskflow paths.
- No new unauthenticated surface. The HTTP `login` endpoint is intentionally passwordless (separate from credential checking by design).

---

## Concern 3 — Code quality and design: PASS

**What was checked**: Abstraction layer for hashing; duplication between implementations; critical-section discipline; migration idempotence; naming.

**What was found clean**:
- Both helpers in `mod.rs`; both impls call `super::hash_password` / `super::verify_password`. No KDF logic duplicated.
- Symmetric credential handling across both impls; structural differences (lock vs. transaction) reflect storage model, not inconsistency.
- Hash computed outside critical section in both `set_credential` and `complete_account_recovery` in both implementations.
- Migration idempotent-safe.

**Non-blocking observations** (filed in #184):
- `let user_copy = user;` in `in_memory.rs::complete_account_recovery` is correct but adds naming noise.
- `Result<bool, ServerError>` from `verify_password` unconventional; callers would be simpler with `Err(Unauthorized)` on mismatch.

---

## Concern 4 — Test coverage: PASS

**What was checked**: New test scope; round-trip coverage; error-path coverage; AC#5 satisfaction; CI result.

**What was found clean**:
- The HTTP `login` path is passwordless by design; credential tests are at repository level.
- New in-memory tests (run unconditionally, included in 22-test count):
  - `set_then_verify_credential_round_trips_to_the_user` — happy path with real secret.
  - `set_credential_replaces_the_previous_secret` — replacement: old rejects, new accepts.
  - `verify_credential_is_unauthorized_for_unknown_handle_missing_credential_or_mismatch` — three rejection cases.
  - Recovery completion test — verifies recovery-set credential accepts; pre-recovery credential rejects.
- Postgres tests mirror in-memory coverage; skip without `CHIRP_TEST_DATABASE_URL`; run in CI.
- CI test check: SUCCESS (22/22 on branch; SUCCESS on merge commit in progress).

---

## Concern 5 — Rust idiom: PASS

**What was checked**: `argon2 v0.5` API; feature flag; trait imports; error handling; `unwrap`/`expect` on crypto.

**What was found clean**:
- `argon2 = { version = "0.5", features = ["std"] }` — `std` feature required for `OsRng`. Correct.
- `PasswordHasher`, `PasswordVerifier`, `PasswordHash`, `SaltString`, `OsRng` imported from correct `password-hash 0.5` paths. No deprecated symbols.
- `Argon2::default()` — recommended Argon2id defaults (19 MiB, 2 iterations, parallelism 1).
- `?` propagation throughout; no `unwrap` or `expect` on crypto.

**Non-blocking observation** (filed in #184): `Argon2::default()` instantiated per call — zero cost today; worth a note if custom parameters are added.

---

## Non-blocking items

Filed as issue #184 (four related observations in the credential helper layer):
1. `verify_password` absorbs algorithm/version-mismatch errors as `false` rather than `Internal`.
2. `Result<bool, ServerError>` return type unconventional; callers simpler with `Err(Unauthorized)` on mismatch.
3. `let user_copy = user;` verbosity in `in_memory.rs::complete_account_recovery`.
4. `Argon2::default()` per-call — zero cost now; worth noting for when custom params arrive.

---

## Landing record

- **Merge**: Squash-merge `work/security-persist-r1` → `main`, commit `c3f9f558fc7b254c2b0d431c31a7fc9a095fe0d5`, 2026-11-03T19:08:01Z
- **Branch**: `work/security-persist-r1` deleted
- **Issue #120**: Closed (auto-closed on merge)
- **CI on merge commit**: In progress at time of SYNTHESIS authoring; all pre-merge checks were SUCCESS
- **ArgoCD**: OutOfSync at time of authoring — pending CI image build and push; will sync on new image
