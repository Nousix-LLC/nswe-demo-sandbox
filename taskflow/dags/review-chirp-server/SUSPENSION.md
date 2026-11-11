# SUSPENSION.md — review-chirp-server review DAG (NeedsDecompose)

**Status**: SUSPENDED (decompose_evaluation = NeedsDecompose)
**Task**: review-chirp-server (root of the PR #19 review DAG)
**Timestamp**: 2026-10-07

## Why suspended
The review task fired the Scope-Based trigger and failed the Distinct Concerns + Single-Responsibility
tests: the brief enumerates four distinct review lenses / methodologies (code-review quality, Rust
idiom/soundness, architecture + layering + frozen-contract conformance, test adequacy), and the
overseer's brief itself specifies a `decompose → review → synthesize` shape. By Trigger Precedence the
single-`SYNTHESIS.md`-output signal does NOT override the fired scope trigger. The task is therefore
decomposed into a hub-and-spoke, not executed in one invocation.

## Subtree materialized (hub-and-spoke; this invocation authored all state below)
Hub: `_GLOBAL.md` · Contract seam: `contracts/_MANIFEST.yaml` + `contracts/findings_schema.md`
(the shared finding-record shape, fixed severity vocabulary `block|major|minor|nit`, the AC1–AC8
coverage map, and the F1_1–F1_4 sub-question checklist).

| Task id | Group | Depends on | Output |
|---------|-------|------------|--------|
| `SUBTASK_rust_soundness_review` | 0 | none | `findings_rust_soundness.md` |
| `SUBTASK_architecture_contract_review` | 0 | none | `findings_architecture_contract.md` |
| `SUBTASK_test_adequacy_review` | 0 | none | `findings_test_adequacy.md` |
| `SUBTASK_code_review_quality_review` | 0 | none | `findings_code_review_quality.md` |
| `SUBTASK_synthesis_verdict` (Task Kind: synthesis — verification gate) | 1 | all four spokes | `../SYNTHESIS.md` (fold record = observation seam) |

## Resumption condition
Implicit: all child tasks reach terminal lifecycle state. The synthesis gate writes the authoritative
`SYNTHESIS.md` at this workspace root (the overseer's observation seam) and folds this root task
`SUSPENDED → COMPLETED` via `engine_resume_suspended`. The root resolves entirely via that fold — no
separate root `COMPLETE.md`.

## Reviewer discipline carried into every child
Review only — no source edits, no push/rebase/relock, never touch `main`; only `Nousix-LLC/nswe-demo`.
The CONFLICTING/DIRTY mergeability is a known `Cargo.lock` restale, not a review finding. Rely on the
code DAG's cold machine gate (`chirp-server/SYNTHESIS.md`, PASS round 1); do not reproduce the full build.
