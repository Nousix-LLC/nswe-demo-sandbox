# SYNTHESIS — review-ci-actions (overseer/I43)

**Repo**: `Nousix-LLC/nswe-demo` · **Scope**: CI GitHub Actions for the Rust/WASM workspace (work-item #11 / PR #21)
**Synthesized at**: 2026-11-02 (recovered dispatch; original fork overseer/I43)
**DAG**: `review-ci-actions` — retroactive synthesis of the PR #21 review cycle and current CI posture

---

## Summary

The CI Actions work for the `nswe-demo` Rust/WebAssembly workspace completed its full review cycle. PR #21 was
**merged** on 2026-10-08 after two review rounds (r2 → REQUEST-CHANGES on IMG-1; r3 → APPROVE after remediation).
The CI workflow is live and green. One high-priority CI gap remains open (issue #115). Two Ferric 1.0 CI
enhancement items are planned for a future milestone.

---

## Review Cycle Completed

| Round | DAG | Head reviewed | Verdict | Key finding |
|-------|-----|---------------|---------|-------------|
| Implementation | `ci-actions` | `c812337` | PASS | CI workflow built and self-validated |
| Review round 1 | `review-ci-actions-r2` | `c8123376` | REQUEST-CHANGES | IMG-1 (major): image job not gated pre-merge |
| Remediation | `remediate-ci-actions` | — | PASS | IMG-1 closed by commit `716817bc` |
| Review round 2 | `review-ci-actions-r3` | `716817bc` | APPROVE | All criteria MET; IMG-1 independently verified closed |
| **Merge** | — | `ada3aa97` | — | PR #21 merged 2026-10-08 by `mattsmcknight` |

### Round 1 (r2) findings resolved before merge

| id | sev | disposition |
|----|-----|-------------|
| IMG-1 | **major** | **RESOLVED** in `716817bc`: `image` job now runs build-only on every PR, closing the toolchain-drift window |
| IMG-2 | minor | **RESOLVED** folded in `716817bc`: Dockerfile detection / skip guards removed; build runs unconditionally |
| IMG-4 | nit | **RESOLVED** folded in `716817bc`: published image digest surfaced in job summary |
| WF-1 | minor | Deferred: toolchain pinned to series `1.97`, not exact `1.97.0` |
| WF-2 | minor | Deferred: manifest `rust-version = "1.82"` contradicts locked deps requiring `≥1.97` |
| SEC-1 | minor | Deferred to issue #24 (ArgoCD hardening track); action tags not SHA-pinned |
| DOC-1 | minor | Resolved in PR description (appended remediation note; stale top section tracked as DOC-3) |
| DOC-2 | nit | Deferred (#19-owned, cosmetic) |
| SEC-2 | nit | Deferred to #24 |
| IMG-3 | nit | Deferred: `workflow_dispatch` doesn't publish |

### Round 2 (r3) advisories (non-blocking, PR metadata only)

| id | sev | note |
|----|-----|------|
| DOC-3 | minor | PR #21 body top section contradicts shipped workflow; tracked as issue #27 |
| HYG-1 | minor | Pre-existing `🤖 Generated with Claude Code` trailer in PR body; tracked as issue #27 |

---

## Current CI Workflow (landed on `main`)

File: `.github/workflows/ci.yml` — [as of merge commit `ada3aa97`]

| Job | Trigger | Purpose |
|-----|---------|---------|
| `fmt` | PR + `main` | `cargo fmt --all --check` |
| `clippy` | PR + `main` | `cargo clippy --workspace --all-targets --locked -- -D warnings` |
| `test` | PR + `main` | `cargo test --workspace --locked` (no `--features postgres`) |
| `wasm` | PR + `main` | WASM build + `wasm-bindgen`; asserts `pkg/chirp.js` + `pkg/chirp_bg.wasm` |
| `doc` | PR + `main` | `cargo doc --workspace --no-deps --locked` under `RUSTDOCFLAGS=-D warnings` |
| `image` | PR (build-only) + `main` (push to GHCR) | `docker/build-push-action@v6` from `./Dockerfile` |

**All six jobs confirmed running as of most recent observed CI run** (e.g. `work/design-ferric-1_0` on 2026-10-29: 6 jobs, all success).

**Known CI behavior**: The `Renew interaction limit` scheduled workflow (`renew-interaction-limit.yml`) is failing on the scheduled trigger (observed 2026-11-01) — unrelated to the codebase CI pipeline; a platform/credential maintenance item.

---

## Open CI Action Items

### Priority: HIGH — Issue #115

**Title**: PR #113 review: durable-store proofs run in no required CI gate; drill default run overstates coverage
**Severity**: major / non-blocking at landing of #113 (epic-persist)

The required `test` job runs `cargo test --workspace --locked` with **no `--features postgres`** and **no database
service**. The durable-store test suite (`concurrency_invariants.rs`, `repository/postgres.rs`) is feature-gated
on `postgres` and env-gated on `CHIRP_TEST_DATABASE_URL`, so it is **not compiled or run in any required check**.
After merge, CI can stay green while the entire durable write path regresses silently.

**What would satisfy**: A new required job that provisions an ephemeral PostgreSQL via `services:` in the workflow,
sets `CHIRP_TEST_DATABASE_URL`, and runs `cargo test -p chirp-server --features postgres`. This job should fail
CI if the database is unreachable rather than silently skip green.

**Additional**: The durability drill's default run (`durability-drill.sh`) prints `ALL MODES PASS — user data
survived restart` but only proves the store layer (`drill_evidence` table, hand-written rows), not chirp's
migrated schema or the repository layer. The chirp user-data claim requires the optional system layer
(`--image`). The store-layer summary should state what it actually proved.

### Priority: MEDIUM — Planned Ferric 1.0 CI items

| Issue | Title | Stage |
|-------|-------|-------|
| #162 | Ferric 1.0: Semver contract and `cargo semver-checks` CI enforcement | `one_oh` (depends on #161 Publishing readiness) |
| #157 | Ferric 1.0: README, troubleshooting entry, and CI doc sync | `one_oh` |

These are planned, not regressions. They extend CI coverage for the Ferric 1.0 release milestone (epic #136).

### Priority: LOW — Deferred from round 1

| Item | Issue | Status |
|------|-------|--------|
| SHA-pin third-party actions (SEC-1, SEC-2) | No dedicated CI issue (issue #24 is ArgoCD RBAC); `docker/*` actions are the highest-impact | Backlog |
| Toolchain series vs. exact pin (WF-1) | Tracked in r2/r3 SYNTHESISes | Deferred |
| MSRV `1.82` vs locked deps `1.97` (WF-2) | Tracked in r2/r3 SYNTHESISes; comment in `ci.yml` | Deferred |
| PR body hygiene (DOC-3, HYG-1) | Issue #27 | Open (minor) |

---

## Overseer Guidance

1. **PR #21 / issue #11 are closed.** The CI workflow is live, reviewed, and green. No further action required
   on the original CI-actions work-item.

2. **Issue #115 is the highest-priority CI gap** — the durable-store test suite runs outside required CI.
   This should be addressed as part of the epic-persist follow-up work or as a standalone hardening sprint.
   A PostgreSQL `services:` job in `ci.yml` is a bounded, well-understood change.

3. **Ferric 1.0 CI items** (#162, #157) are planned follow-ups for the `one_oh` release milestone and should
   be scheduled with the Ferric 1.0 epic (#136). They do not block current work.

4. **Supply-chain hardening** (action SHA-pinning, image provenance) remains a backlog item. Issue #24 is
   currently scoped to ArgoCD RBAC; a CI-specific SHA-pinning issue may be worth filing separately so the
   item does not get lost in the ArgoCD scope. Priority is lower than #115 but worth tracking under EPIC #3.

5. **No re-review of main CI is warranted** at this time. The workflow is correct, green, and covers all
   nine original acceptance criteria. Issue #115 is a new gap introduced by epic-persist, not a regression
   from the CI work-item.

---

## Disposition

`reap-whole-after-land` — the overseer may reap this thread on receipt of this synthesis.
