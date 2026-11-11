# SUSPENSION.md — design-chirp-r1 (NeedsDecompose)

## Disposition
`suspended` / `decompose_evaluation = NeedsDecompose`. This root design task decomposed the chirp first product
design into a hub-and-spoke subtree and suspends pending the subtree's resolution. Resumption condition
(implicit): all child tasks reach terminal lifecycle state; the subtree folds through `SUBTASK_synthesis`,
which authors `SYNTHESIS.md` at this workspace root and resumes this parent.

## Why decomposition (trigger application)
The brief enumerates **six distinct design concerns**, each mapping to a different design-methodology bundle,
plus three distinct serial responsibilities (design → plan/backlog → measure the live product). The
Scope-Based trigger (enumerated concerns), the Distinct Concerns Test (parallel specialists), the
Single-Responsibility Test (serial pipeline of distinct verbs), and the Output-Size trigger all fire.
Mechanically `NeedsDecompose`.

## Subtree authored (named state)
- `_GLOBAL.md` — subtree hub (context, constraints, task tree, contract).
- `contracts/_MANIFEST.yaml`, `contracts/design_artifact_map.yaml`, `contracts/id_and_traceability_schema.yaml`
  — the frozen seam: design-doc file ownership, the `REQ-<AREA>-NNN` / `BAR-NNN` / epic-issue id scheme, the
  traceability matrix, and the coverage/trace identities the synthesis gate asserts.
- Nine child `_BRIEF.md` files (one per `SUBTASK_*`).

## Children (9), by execution group
0. `SUBTASK_product_requirements` — foundation; REQ-PROD-*. (deps: none)
1. `SUBTASK_domain_app_design`, `SUBTASK_experience_design`, `SUBTASK_identity_trust` — concern designs. (deps: product_requirements)
2. `SUBTASK_operational_readiness` — ops readiness. (deps: product_requirements, domain_app_design)
3. `SUBTASK_release_bar` — MVP/release scoping, BAR-*, completeness/gap review. (deps: all 5 concerns)
4. `SUBTASK_design_pr` — assemble design/ tree + open PR into main. (deps: all concerns + release_bar)
5. `SUBTASK_delivery_backlog` — epics/issues traceable to design, de-duplicated, ordered. (deps: design_pr, release_bar)
6. `SUBTASK_synthesis` — verification gate: assert identities, measure live product at c805525 vs the bar,
   author root `SYNTHESIS.md`, fold the parent. Task Kind: synthesis. (deps: design_pr, delivery_backlog,
   release_bar, all concerns)

## Fold
`SUBTASK_synthesis` writes `SYNTHESIS.md` at this subtree root (the DAG's observation seam) and resumes this
parent via the synthesis fold. That `SYNTHESIS.md` is the DAG's verdict: the release bar, the issue index by
epic, and the measured standing of the live product against the bar.
