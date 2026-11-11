# _BRIEF.md — review-security-persist-r1 (swe-reviewer DAG)

**Goal**: Review PR #182 (`work/security-persist-r1` → `main`, repository `Nousix-LLC/nswe-demo`).
This PR closes issue #120 (persistence security hardening: argon2id KDF credential storage + CronJob TLS).

---

## Target

- **PR**: #182 (`work/security-persist-r1` → `main`)
- **Issue closed**: #120 — Persistence security hardening
- **Code DAG SYNTHESIS.md**: `taskflow/dags/security-persist-r1/SYNTHESIS.md` (gate verdict: PASS, all
  four checks clear, no blocking findings)
- **Commits on branch**:
  - `282707f43cc898dffa1e19db613899e5dc8f3cd9` — credential hashing with argon2id, constant-time verify
  - `d5e865bd0e6a` — PGSSLMODE: require in CronJob manifest

## Issue #120 acceptance criteria

The PR is held to every criterion below:

1. Passwords/credentials hashed with argon2id: per-credential fresh salt via `SaltString::generate`
   (with `OsRng`); `PasswordHasher::hash_password` for storage; `PasswordVerifier::verify_password` for
   constant-time comparison — no direct `==` on stored vs. supplied credential.
2. All credential-verify paths use `PasswordVerifier::verify_password` (not `==`). Applies to both
   `crates/chirp-server/src/repository/postgres.rs` and `crates/chirp-server/src/repository/in_memory.rs`,
   and to every code path that checks a credential: sign-in, account recovery, and any other.
3. CronJob `deploy/chirp/50-transient-sweep-cronjob.yaml` sets `PGSSLMODE: require` (TLS enforced on
   the database connection).
4. No secrets or plaintext credentials in the diff.
5. All existing tests pass; any new tests cover the hash/verify round-trip.

## Review concerns

Each concern must be covered as a distinct concern with its own findings and verdict.

### 1. Correctness

Argon2id implementation correct end-to-end:
- Fresh salt per credential on every hash operation (`SaltString::generate(&mut OsRng)` at call site, not
  a static or reused salt).
- `PasswordHasher::hash_password` used for storage; result stored as a PHC-format string.
- `PasswordVerifier::verify_password` used for all comparisons — no raw `==`, no `!=` comparison of stored
  and supplied values.
- `complete_account_recovery` updated in both `postgres.rs` and `in_memory.rs` (both repository
  implementations must use the KDF path).
- All acceptance criteria above are met.
- Edge cases: empty passwords, wrong password behavior, repository error propagation.

### 2. Security

Trust-boundary review:
- Argon2id used everywhere a credential is stored or verified; no plaintext fallback remains.
- No hardcoded salts; no reuse of a salt across credentials.
- `PGSSLMODE: require` correctly enforced in the CronJob manifest — no other manifest in `deploy/` sets
  TLS off or leaves it unset where it matters.
- No secrets, tokens, or plaintext credentials in the diff.
- No host paths, Tailscale IPs, internal addresses, or internal taskflow directory paths committed to the
  repository (check PR description, code comments, and all changed files).
- The diff introduces no new trust-boundary exposure: no new unauthenticated surface, no bypassed auth
  path, no skipped verify call.

### 3. Code quality and design

- Responsibilities clear: hashing and verifying are in the right layer; no leakage across abstraction
  boundaries.
- No duplication introduced between `postgres.rs` and `in_memory.rs`; implementations are symmetric.
- Naming and error-handling appropriate; errors propagate correctly.
- Migration script (`0003_invalidate_plaintext_credentials.sql`) correct and idempotent-safe (safe to
  re-apply; does not break if run twice).
- The change leaves the code simpler to extend, not harder.

### 4. Test coverage

- Existing tests exercise the hash/verify round-trip (sign-in, recovery, or relevant integration tests
  pass with the new KDF path).
- No regressions in the 22 tests that passed locally.
- Any new tests cover both the happy path (correct credential verifies) and the error path (wrong
  credential rejected).

### 5. Rust idiom

- Argon2 crate (`argon2 = { version = "0.5", features = ["std"] }`) usage idiomatic: correct trait
  imports, correct generic type parameters, no deprecated methods.
- Error handling pattern fits the project's existing style (e.g., `?` propagation, custom error types or
  `anyhow`).
- No unnecessary `unwrap`/`expect` on crypto operations.

---

## Declared output

1. **A posted review comment on PR #182** with the verdict (APPROVE or REQUEST-CHANGES) and the
   findings per concern: what was checked, what was found clean, and any finding with its severity and
   whether it blocks. Post as a comment if the platform does not allow a formal approval from this account.
2. **`SYNTHESIS.md` at the review DAG root** (`taskflow/dags/review-security-persist-r1/SYNTHESIS.md`)
   with the APPROVE or REQUEST-CHANGES verdict, concern-by-concern findings, and the non-blocking items
   to file.
3. **Non-blocking findings filed as backlog issues** on the `Nousix-LLC/nswe-demo` repository — grouped,
   de-duplicated, linked to PR #182 and issue #120.

---

## Config and landing authority

- **Repository**: `Nousix-LLC/nswe-demo`
- **Landing authority**: delegated (`landing_authority: delegated`, `auto_land: true`, `headless: true`)
- **On APPROVE + machine PASS**: Land PR #182 automatically — squash-merge `work/security-persist-r1`
  into `main`, delete the branch, close #120, schedule a deployment check.
- **On REQUEST-CHANGES**: Report blockers in `SYNTHESIS.md`; the overseer will launch a remediation DAG.
- **No attribution trailers** on anything posted to GitHub (no "Co-Authored-By" lines in PR comments or
  review text).
- Do not name host paths, Tailscale addresses, or taskflow internals in any GitHub post.
