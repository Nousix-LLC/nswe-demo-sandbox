# SYNTHESIS.md — review-sweep-seam-r1

## Verdict: APPROVE

PR #183 (`work/sweep-seam-r1 → main`) meets all six acceptance criteria from issue #117. No finding blocks.

---

## Per-concern findings

### 1. Correctness — PASS, no findings

**Checked:**
- `run_sweep()` (`main.rs:66`) chains URL lookup → `PostgresRepository::connect()` → `sweep_expired_transient_state()` → structured log → `Ok(())`. `?` propagates errors; `main()` returning `Err` exits non-zero. Exit code reflects outcome.
- Self-migrating guarantee: `PostgresRepository::connect()` (`postgres.rs:73`) calls `MIGRATOR.run(&pool)` at line 82 before returning. Migrations run before any sweep SQL executes, regardless of server pod start order. Start-order race eliminated.
- Fail-loud stub (`main.rs:90–98`) returns an explicit error on non-postgres builds rather than silently doing nothing.
- CLI dispatch (`main.rs:42–61`) is complete: `Some("sweep")`, `None`, and `Some(other)` are all handled. The serve path is unchanged.
- CronJob `CHIRP_DATABASE_URL` sourced from `secretKeyRef: chirp-db-credentials / CHIRP_DATABASE_URL`. Matches the Deployment's pattern.
- Post-merge image-digest situation is documented in the manifest comment. CronJob fails loudly with the old binary (exit non-zero), which is the correct behavior. The update path is unambiguous.

### 2. Design conformance — PASS, no findings

**Checked:**
- The `psql` command and all six `-c` SQL arguments are removed. No other manifest in `deploy/chirp/` carries sweep SQL.
- `sweep_expired_transient_state()` in `postgres.rs` holds the three DELETE predicates exactly once. The CronJob delegates to it via the `sweep` subcommand with no domain knowledge of its own.
- Both the Deployment and CronJob use `CHIRP_DATABASE_URL` from `chirp-db-credentials`. Consistent.

### 3. Security — PASS, no findings (one informational note filed)

**Checked:**
- No connection string, password, or credential is committed. `CHIRP_DATABASE_URL` is sourced from a Kubernetes Secret at runtime.
- `imagePullSecrets: [{name: ghcr-pull}]` present for the private GHCR image.
- No host addresses or internal infrastructure references in source or manifests.
- The manifest comment documents that the secret's URL must include `sslmode=require`, consistent with #120. The binary does not validate this at startup — noted as a non-blocking backlog item (issue #185).

### 4. Test coverage and depth — PASS, one non-blocking finding (issue #186)

**Checked:**
- In-memory sweep tests (`in_memory.rs:2137, 2164`): `sweep_reclaims_expired_sessions_and_keeps_live_ones`, `sweep_reclaims_expired_recovery_tokens_and_keeps_valid_ones`, `sweep_never_removes_live_user_content` — full path coverage including idempotency and content-safety.
- Durable postgres-gated sweep tests (gated on `CHIRP_TEST_DATABASE_URL`): same logic against a real PostgreSQL backing with direct row-level assertions.
- `login_always_stamps_a_bounded_session_expiry` (`in_memory.rs:2218`): inspects the internal store directly and asserts `session.expires_at.is_some()`. Would fail if `login()` wrote `None`. Tests the right invariant.

**Finding #1 (non-blocking, severity: low):** No automated test for the CLI dispatch in `main()` (`main.rs:42–61`). The three arms are correct on inspection; the gap is in test coverage, not behavior. Filed as issue #186.

### 5. Code quality and design — PASS, no findings

**Checked:**
- `run_sweep()` is 20 lines with no business logic. Appropriate for a binary entrypoint.
- `build_app_state()` extraction is a sensible cleanup of state-construction logic.
- Doc comments on `run_sweep()`, the stub, and the module-level doc are accurate.

### 6. Manifest hygiene — PASS, no findings

**Checked:**
- Schedule `0 * * * *`, `concurrencyPolicy: Forbid`, `restartPolicy: Never`, `backoffLimit: 3`, `activeDeadlineSeconds: 120`, `ttlSecondsAfterFinished: 3600`, resource limits (10m/100m cpu, 32Mi/64Mi memory) — all correct.
- PSA-restricted security context: `runAsNonRoot`, `runAsUser: 65532`, `seccompProfile: RuntimeDefault`, `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`, `capabilities.drop: [ALL]` — all present.
- `automountServiceAccountToken: false`. `timeZone: "Etc/UTC"`. Label schema consistent.
- All `PG*` env vars removed with no leftovers. `tmp` emptyDir mount correct with `readOnlyRootFilesystem: true`.

### 7. Rust idiom — PASS, no findings

**Checked:**
- `.ok_or("message")?` for `Option → Result` coercion — idiomatic.
- `match subcommand.as_deref()` for `&str` matching on `Option<String>` — idiomatic.
- `use chirp_server::ChirpRepository` scoped inside the cfg-gated function body — avoids dead-code warnings in non-postgres builds.
- `#[cfg(feature = "postgres")]` on the function definition (not inside it) — correct placement.

---

## Non-blocking findings for board follow-up

| # | Finding | File | Severity | Issue |
|---|---------|------|----------|-------|
| 1 | CLI dispatch in `main()` has no automated test | `crates/chirp-server/src/main.rs:42–61` | Low | #186 |
| 2 | `sslmode=require` relies on operator convention; no startup validation | `deploy/chirp/50-transient-sweep-cronjob.yaml` (env section) | Low | #185 |

---

## Post-merge action required

After the CI image build completes following merge, update the image digest in `deploy/chirp/50-transient-sweep-cronjob.yaml` to the digest that includes the `sweep` subcommand. Until then the CronJob will fail loudly on each scheduled run (the old binary does not implement `sweep`). Fail-loud is the correct interim behavior.

---

## CI status at review time

All six checks passed at head commit `5dcb72f`: fmt ✓, clippy ✓, test ✓, wasm ✓, doc ✓, image ✓.
