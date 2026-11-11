# SUSPENSION.md — review-ci-actions-r2 (NeedsDecompose)

**Task**: `review-ci-actions-r2` (root of the re-fork r2 review DAG for PR #21)
**Terminal state**: SUSPENDED / `decompose_evaluation = NeedsDecompose`
**Resumption condition**: all child tasks reach terminal lifecycle state; the subtree resolves via
the synthesis fold (`SUBTASK_synthesis` authors the root `SYNTHESIS.md` and folds this parent
`SUSPENDED → COMPLETED`).

## Decompose evaluation (auditable)

Applied the decomposition triggers to this task's actual brief (review PR #21 across six enumerated
concerns, producing one landing verdict):

| Trigger / test | Outcome | Basis |
|---|---|---|
| Token-based | cleared | Input modest (ci.yml ~194 lines; diff +286/−92; well under 50% context). |
| Output-size | (weakest; non-dominant) | One `SYNTHESIS.md` verdict — MUST NOT override a fired scope trigger. |
| Scope-based (enumerated-concerns rule) | **FIRED** | Brief enumerates **six distinct concerns** (CI correctness; reproducibility/pinning; supply-chain security; image-job-vs-Dockerfile; folded doc minors; acceptance mapping). |
| Distinct Concerns Test | **FIRED** | CI/workflow, supply-chain-security, container, and code-review specialists could work in parallel. |
| Single-Responsibility Test | **FIRED** | Bundles distinct kinds of analysis + a verdict synthesis. |

Precedence: fired scope/concern triggers win over cleared size signals → **NeedsDecompose**. (A
principal-engineer instinct that "one reviewer could read it all and write one verdict" is explicitly
overridden by the kernel's enumerated-concerns rule.)

## Cut chosen

Candidate A (one spoke per concern = 6+1) vs **Candidate B (chosen)**: group the two tightly-coupled
workflow concerns (1+2) into one spoke; keep security (3), image-job (4), and folded-minors (5) as
distinct-specialty spokes; fold acceptance-mapping (6) into the synthesis gate (integrative; the
verdict is gated on it). B minimizes cross-sibling edges and duplicated `ci.yml`/caching findings,
gives disjoint output ownership, and keeps each child in the S/M band.

**4 parallel review spokes (group 0) + 1 synthesis verification gate (group 1):**

| Task id | Depends on | Output |
|---|---|---|
| `SUBTASK_workflow_correctness` | none | `SUBTASK_workflow_correctness/findings.md` (concerns 1+2) |
| `SUBTASK_supply_chain_security` | none | `SUBTASK_supply_chain_security/findings.md` (concern 3) |
| `SUBTASK_image_job` | none | `SUBTASK_image_job/findings.md` (concern 4) |
| `SUBTASK_folded_minors` | none | `SUBTASK_folded_minors/findings.md` (concern 5) |
| `SUBTASK_synthesis` | all four spokes | `SYNTHESIS.md` at DAG root (concern 6 + fold + verdict) |

## Contract (frozen seam)

`contracts/` — kind `taxonomy`: `findings_schema.md` (severity enum block/major/minor/nit, per-finding
record, per-spoke id prefixes, verdict rule) + `_MANIFEST.yaml` (ownership + identities). The seam is
the findings format so the gate aggregates counts and applies the verdict rule mechanically.

## Authored before this terminal call

- `_GLOBAL.md` (subtree hub), `contracts/_MANIFEST.yaml`, `contracts/findings_schema.md`
- `SUBTASK_workflow_correctness/_BRIEF.md`, `SUBTASK_supply_chain_security/_BRIEF.md`,
  `SUBTASK_image_job/_BRIEF.md`, `SUBTASK_folded_minors/_BRIEF.md`, `SUBTASK_synthesis/_BRIEF.md`
- Five `engine_amend_plan { add_task }` calls (all applied).

The authoritative landing verdict (`APPROVE` / `REQUEST-CHANGES`) will be the body of the root
`SYNTHESIS.md` produced by `SUBTASK_synthesis` — the overseer's observation seam.
