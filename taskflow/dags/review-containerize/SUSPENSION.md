# SUSPENSION — review-containerize (NeedsDecompose)

**Status**: SUSPENDED · `decompose_evaluation = NeedsDecompose`
**Task**: review-containerize (root of the review DAG for PR #22 / work-item #12 `containerize`)
**Date**: 2026-10-07

## Why suspended

This review node decomposed. The brief enumerates **eight distinct concerns** to evaluate explicitly,
spanning different specialist lenses and methodology bundles (Containerization, Security, Operations,
Rust/Core, Code Review, Testing). Applying the Task Decomposition Framework at the evaluation point:

- **Scope-Based trigger — FIRED** by the Enumerated-Concerns rule (≥2 distinct analyses named in the brief).
- **Distinct Concerns Test — FIRED** (several concerns could be evaluated in parallel by different specialists).
- Token and output-size triggers cleared, but per **Trigger Precedence** a fired scope/concern signal
  wins over a single declared output file and a low token estimate. Verdict: **NeedsDecompose**.

## Subtree materialized

Hub-and-spoke: five parallel analysis spokes (Group 0) + one synthesis/verification gate (Group 1).
A `taxonomy` contract (`contracts/_MANIFEST.yaml` + `contracts/findings_schema.md`) fixes the shared
findings vocabulary, the concern→spoke ownership partition (every concern owned exactly once), the
severity rubric, and identities I1–I6 the gate asserts.

| Task id | Depends on | Concerns | Output |
|---|---|---|---|
| `SUBTASK_dockerfile_build` | none | 1, 2 (layer/size), 6 (Dockerfile idiom) | `SUBTASK_dockerfile_build/findings.md` |
| `SUBTASK_security_supplychain` | none | 3, 2 (secret-leakage face) | `SUBTASK_security_supplychain/findings.md` |
| `SUBTASK_operability_docs` | none | 4, 6 (docs) | `SUBTASK_operability_docs/findings.md` |
| `SUBTASK_rustcode_sigterm` | none | 5, 6 (Rust idiom) | `SUBTASK_rustcode_sigterm/findings.md` |
| `SUBTASK_scope_verification` | none | 7, 8 | `SUBTASK_scope_verification/findings.md` |
| `SUBTASK_verdict_synthesis` | all five spokes | integration/gate | `SYNTHESIS.md` (DAG root) + posted PR #22 review |

All six children were authored (`_GLOBAL.md`, `contracts/`, six `_BRIEF.md`) and materialized via
`engine_amend_plan { add_task }` before this suspension.

## Resumption condition

All child tasks reach terminal state. The synthesis gate writes the root `SYNTHESIS.md` at this
workspace (the fold location / observation seam named in `_FORK.md`) and folds this parent
`SUSPENDED → COMPLETED` via `engine_resume_suspended`. That `SYNTHESIS.md` carries the one
authoritative APPROVE / REQUEST-CHANGES verdict.
