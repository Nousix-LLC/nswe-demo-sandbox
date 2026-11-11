# SUSPENSION — SUBTASK_synthesis (NeedsDecompose)

**Task**: `SUBTASK_synthesis` — the deploy-argocd subtree's verification gate (NSWE #13).
**Status**: SUSPENDED / NeedsDecompose. **Date**: 2026-10-08.

## Why this node suspended (decompose evaluation)

At dispatch the gate's brief enumerated **four distinct kinds of work** drawing on distinct methodology
bundles: (1) a read-only static four-check (contract identities + wiring + duplication + review); (2) a
live-cluster deploy + reachability proof; (3) a git commit + PR into `main`; (4) authoring the root
`SYNTHESIS.md` fold record. The Single-Responsibility conjunction test and the Scope/Distinct-Concerns
trigger both fire (verify **and** deploy **and** prove **and** open PR **and** author fold record), and
the realistic tool-call envelope (live deploy + pull/probe debugging + HTTP proof + git/gh + fold) far
exceeds the atomic floor. Per Trigger Precedence the single-file `SYNTHESIS.md` output does not override a
fired scope/responsibility trigger. Verdict: **NeedsDecompose** (published before any substantive work).

## Chosen cut (serial verification pipeline, disjoint side-effect ownership)

A fully serialized pipeline by *kind of work and side-effect domain* — every cross-sibling edge is a
declared dependency reading the producer's real COMPLETED output (no frozen interface seam/mock):

| Child | Side-effect domain | Depends on | Output |
|-------|--------------------|------------|--------|
| `SUBTASK_static_gate` | none (read-only) | — | `SUBTASK_static_gate/outputs/static_gate_report.md` |
| `SUBTASK_deploy_reach` | cluster only | `SUBTASK_static_gate` | `SUBTASK_deploy_reach/outputs/reachability_evidence.md` |
| `SUBTASK_land_pr` | git only | `SUBTASK_static_gate`, `SUBTASK_deploy_reach` | `SUBTASK_land_pr/outputs/pr_record.md` |
| `SUBTASK_fold` | authors root `SYNTHESIS.md` + folds | all three | `../SYNTHESIS.md` (deploy-argocd root) |

Disjoint write-sets (hard ownership gate satisfied); the sibling manifests `deploy/chirp/*` + `deploy/argocd/*`
are read-only shared input; all edges unidirectional → declared dependencies. Rationale recorded in `_GLOBAL.md`.

## Named state authored before this suspension

- `_GLOBAL.md` — sub-subtree hub (chosen-cut rationale, posture, task structure).
- `contracts/_MANIFEST.yaml` + `contracts/synthesis_gate_contract.yaml` — per-child ownership, the
  identity-coverage map over the parent identities, the output-artifact seam, and the fold obligation.
- `SUBTASK_static_gate/_BRIEF.md`, `SUBTASK_deploy_reach/_BRIEF.md`, `SUBTASK_land_pr/_BRIEF.md`,
  `SUBTASK_fold/_BRIEF.md` — the four child briefs (each materialized via `engine_amend_plan { add_task }`).

## Fold / resumption

Resumption condition: all four child tasks reach terminal state. `SUBTASK_fold` authors the root
`SYNTHESIS.md` (this node's owed deliverable + the deploy-argocd root fold record) and resumes both this
`SUBTASK_synthesis` node and the `deploy-argocd` root from SUSPENDED → COMPLETED via `engine_resume_suspended`,
with `SYNTHESIS.md` as the seam. Any gate FAIL is remediated by injected fix-tasks + re-verification, never
by silent edits to the sibling manifests.
