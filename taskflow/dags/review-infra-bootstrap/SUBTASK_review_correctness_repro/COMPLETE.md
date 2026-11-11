# COMPLETE — SUBTASK_review_correctness_repro

**Task:** Review PR #20 (`deploy/bootstrap/`) through the correctness / reproducibility / idiom lens.
**Outcome:** completed (Atomic). Review-only — no repo/branch/checkout modification performed.

## What was done

Read all six bootstrap scripts, the four READMEs, `versions.txt`, the PR #20 diff/body, and the code
DAG's folded `SYNTHESIS.md` (as INPUT context, not authority). Validated the wasm build path against the
live crate (`examples/chirp.rs`, `index.html` default import of `./pkg/chirp.js`, `Cargo.lock`
wasm-bindgen `0.2.129`), and empirically probed two suspected defects (`k3d v5.9.0 cluster list -o json`
serialization; sudo `env_reset` forwarding). Judged all three owned concerns individually with evidence
and emitted findings in the contract schema.

## Result (one artifact)

- `review_correctness.md` — lens summary; per-subsystem genuine-vs-trivially-true-green verdict
  (cluster / gitops / wasm all **genuine**); concern-by-concern assessment; 7 findings
  (1 major, 3 minor, 3 nit) + evidenced clean observations; AC-bearing table for the gate's R2.

## Finding headline

- No `block` finding. One **major**: CORR-1 — NATIVE-mode k3s version pin silently dropped under `sudo`
  (`env_reset`), a latent reproducibility defect on the unexercised production path; remediation given.
- Minors: version printed-not-asserted in verify scripts (CORR-2); brittle JSON-via-grep idempotency
  probe (CORR-3, works on pinned k3d, verified). Nits: wrong-token bundle-check grep (CORR-4), curl `-S`
  (CORR-5), vacuous `--all` node wait backstopped by CoreDNS (CORR-6), log stdout/stderr inconsistency
  (CORR-7).

## Scope boundaries honored

k3d-vs-native *acceptability* adjudication, security/secrets, RBAC, scope conformance, and operability
were left to their owning spokes; only correctness-scoped observations relevant to them were flagged for
the gate, not owned.

## Success criteria

- [x] All three owned concerns assessed individually with evidence.
- [x] Every finding well-formed per `finding_schema.md`; the major carries actionable remediation.
- [x] Explicit genuine-vs-trivially-true verdict for each of the three subsystems.
- [x] `review_correctness.md` written; no repo/branch/checkout modification performed.

## Dependents

`SUBTASK_synthesis_gate` consumes `review_correctness.md`.
