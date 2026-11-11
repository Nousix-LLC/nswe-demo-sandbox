# COMPLETE — SUBTASK_durability_proof

## What this task did
Reviewed PR #113 @ `09fa453` through the durability-proof lens only: whether the tests and the durability
drill actually prove the acceptance criteria of #65/#66/#67 and the failure paths (restart/redeploy/reschedule,
concurrency, non-durable write / fail-closed), with the tests read as closely as the code, plus drill
repeatability and `postgres` feature gating. Read-only on the repository; no GitHub writes.

## Output produced
- `SUBTASK_durability_proof/outputs/findings.md` — conforms to `../contracts/finding_schema.md` (prefix `DUR`);
  every finding pinned to `file:line @ 09fa453`, with severity, explicit `blocks_landing`, and
  "what would satisfy me"; includes "What I checked", "What I found clean", and the concern sub-verdict.

## Evidence surface read (at the pinned commit)
- `crates/chirp-server/tests/concurrency_invariants.rs`, `crates/chirp-server/tests/api.rs`
- `crates/chirp-server/src/repository/postgres.rs` (substrate/capacity/live test modules), `…/mod.rs`,
  `…/in_memory.rs`, `…/main.rs`, `Cargo.toml`
- `deploy/chirp/drill/durability-drill.sh`, `deploy/chirp/drill/PROCEDURE.md`
- `.github/workflows/ci.yml`
- Acceptance criteria read from source issues #65, #66, #67

## Sub-verdict
NON-BLOCKING-ONLY. Four findings: DUR-01 (major, non-blocking) no required CI check runs any durable-store
proof; DUR-02 (major, non-blocking) the drill's default store-only run checksums a synthetic table yet the
summary claims user data survived; DUR-03 (nit) reschedule degrades to same-node rebind on node-local storage
(disclosed); DUR-04 (minor) fail-closed-on-write proven at the substrate, not end-to-end through the HTTP
surface. No blocker in this concern; the failing required `doc` check is the CI-diagnosis concern's to record.

## How this composes with the subtree
One of seven concern spokes feeding `SUBTASK_synthesis`. All four findings are non-blocking (backlog); the
synthesis gate folds them with the other concerns to render the APPROVE/REQUEST-CHANGES verdict and gates
landing on the required `doc` check going green and the PR being mergeable and clean.
