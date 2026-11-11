# _BRIEF.md — review-sweep-seam-r1

## Objective

Review PR #183 (`work/sweep-seam-r1`) against `Nousix-LLC/nswe-demo`, branch rebased onto `main` at commit `c3f9f558`, head commit `5dcb72f`.

**PR title**: "fix(#117): replace psql sweep CronJob with chirp-server sweep subcommand"
**Issue closed**: #117 — "Replace psql-based sweep CronJob with Rust-implemented sweep endpoint/subcommand"

The code DAG (`sweep-seam-r1`) returned a PASS verdict with all 6 functional acceptance criteria met. A subsequent remediation DAG (`sweep-seam-r1-r1`) fixed a `cargo fmt` failure and a rebase conflict (from a sibling security commit that landed on main), and all CI checks now pass: fmt ✓, clippy ✓, test ✓, wasm ✓, doc ✓, image ✓. The branch is MERGEABLE / CLEAN.

---

## Issue #117 — Acceptance Criteria

The PR is held to these criteria:

1. **AC #1 — No duplicate DELETE predicates as raw SQL in the CronJob.** The sweep CronJob no longer duplicates the `DELETE … WHERE expires_at …` predicates as raw SQL executed by psql. The sweep logic lives exactly once: in the Rust repository layer.

2. **AC #2 — CronJob succeeds in the cluster.** The updated CronJob manifest runs correctly in the cluster (or the reason it cannot yet run—a post-merge image digest update—is explained and the path to resolution is clear).

3. **AC #3 — Root cause of the prior CronJob failures diagnosed and fixed.** The start-order race condition (`sessions` table not yet created when the CronJob ran) is diagnosed and the new implementation is immune to it.

4. **AC #4 — `sessions.expires_at` nullability.** The nullable semantics of `sessions.expires_at` are documented and an appropriate invariant test is in place (or an explanation of why it is not needed).

5. **AC #5 — All existing tests pass; new tests cover the sweep path.** The test suite passes. New tests cover the sweep correctness.

6. **AC #6 — PR passes CI on the branch.** All CI jobs pass (fmt, clippy, test, wasm, doc, image).

---

## Code DAG `SYNTHESIS.md` summary (sweep-seam-r1)

- **AC #1**: CronJob rewritten to invoke `/usr/local/bin/chirp-server sweep` (Option A). `run_sweep()` added to `crates/chirp-server/src/main.rs`; dispatches on first CLI argument (`sweep` → `ChirpRepository::sweep_expired_transient_state()`; no arg → existing serve mode). Feature-gated on `#[cfg(feature = "postgres")]`; stub returns error on other builds.
- **AC #2**: Connectivity verified by dry-run against the live database. CronJob manifest uses a placeholder image digest (pre-merge); manifest must be updated post-merge to the new digest that includes the `sweep` subcommand.
- **AC #3**: Start-order race confirmed; `sweep` subcommand is self-migrating (calls `PostgresRepository::connect()` first), eliminating the race.
- **AC #4**: `sessions.expires_at` nullable by design (documented); column comment added; new test `login_always_stamps_a_bounded_session_expiry` asserts the application always writes a bounded `Some(expires_at)`.
- **AC #5**: 56 tests pass (chirp-server); all sweep tests pass; new test added.
- **AC #6**: All CI jobs pass (after remediation fmt fix).

---

## Review concerns

Review this PR as a whole, held issue #117 by issue #117 to its acceptance criteria. Decide the concerns fresh from what the diff touches.

### 1. Correctness
Does the implementation do what AC #1–#5 say? Specifically:
- Does `run_sweep()` correctly invoke `ChirpRepository::sweep_expired_transient_state()` and exit with the right code on success and failure?
- Is the feature-gate (`#[cfg(feature = "postgres")]`) correct — does it compile and behave correctly in both configurations?
- Is the CLI dispatch correct — does `None` (no args) preserve the existing serve path without regression?
- Is the self-migrating guarantee accurate: does `PostgresRepository::connect()` actually apply migrations before returning, so the sweep subcommand is safe to run before the server pod starts?
- Does the CronJob manifest correctly use `CHIRP_DATABASE_URL` from `chirp-db-credentials`, matching how the Deployment accesses it?
- Is the post-merge image-digest update correctly described and unambiguous?

### 2. Design conformance
Does the change match the stated approach (invoking the Rust sweep subcommand rather than raw psql)?
- Is the old psql-based sweep logic fully removed (no residual raw SQL for the sweep in any manifest or helper)?
- Is the sweep logic living exactly once (the Rust repository layer), as claimed?
- Is the CronJob manifest's connection-string approach consistent with the broader chirp-server deployment's approach (single `CHIRP_DATABASE_URL` env var from the same secret)?

### 3. Security
- Are there credentials or sensitive values committed in manifests or source? The CronJob must pull `CHIRP_DATABASE_URL` from the `chirp-db-credentials` Kubernetes secret, not embed a connection string inline.
- TLS: the security commit (`c3f9f558`, issue #120) required `sslmode=require` in the connection URL for the CronJob. Does the rebase conflict resolution correctly carry that requirement forward? (The remediation noted the env-section comment was updated to document that `sslmode=require` must be embedded in the URL.)
- Does the manifest still pull from a private GHCR package using `imagePullSecrets: [{name: ghcr-pull}]`?
- No host paths, internal infrastructure addresses (Tailscale, LAN IPs), or deployment-internal URLs committed in source or manifests.

### 4. Test coverage and depth
- Do the existing sweep tests (`sweep_reclaims_expired_sessions_and_keeps_live_ones`, `sweep_reclaims_expired_recovery_tokens_and_keeps_valid_ones`, etc.) exercise the sweep path end-to-end?
- Does `login_always_stamps_a_bounded_session_expiry` correctly assert the invariant it claims (login always writes `Some(expires_at)`)? Does it test real behavior or is it vacuous?
- Is there a test or integration path that exercises the new `sweep` CLI argument dispatch?
- Are edge cases covered: what happens if the sweep encounters a DB error?

### 5. Code quality and design
- Is `run_sweep()` clear and well-scoped? Does it handle errors correctly (propagating them in a way the process exit code reflects)?
- Is the CLI argument dispatch in `main.rs` readable and idiomatic?
- Are there abstraction or responsibility concerns — does `main.rs` carry too much logic, or is it appropriately thin?
- Naming and function size.

### 6. Manifest hygiene
- Is `50-transient-sweep-cronjob.yaml` correct after the rewrite? Schedule, `restartPolicy`, `backoffLimit`, resource limits, and namespace.
- Are the removed `PG*` individual env vars cleanly gone with no leftovers?
- Is the `imagePullSecrets` stanza correct?

### 7. Language idiom (Rust)
- Is the new Rust code idiomatic? Error handling style (`.ok_or`, `?`, `Box<dyn Error>`), match style, `cfg` attribute placement.

---

## Declared output

- A review posted on PR #183 (as an approval or as a comment carrying the verdict, depending on what the platform allows).
- A root `SYNTHESIS.md` at the DAG root with:
  - An **APPROVE** or **REQUEST-CHANGES** verdict.
  - Findings per concern, each with its severity and whether it blocks.
  - A per-concern account of what was checked and found clean.
  - Non-blocking findings listed for board follow-up.
- Non-blocking findings filed as grouped, linked backlog issues on `Nousix-LLC/nswe-demo`.

Findings posted on the PR point at files and line numbers in the repository. Nothing in the review names host paths, internal infrastructure addresses, or DAG-internal paths.

---

## Constraints

- Repository: `Nousix-LLC/nswe-demo`, branch `work/sweep-seam-r1`, head commit `5dcb72f`.
- Read and judge; do not author commits or change the branch.
- The review is of the change as a whole, not of individual files in isolation.
- Remediation budget context (for the overseer's use): 1 of 2 remediation attempts used; 1 remaining.
