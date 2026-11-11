# SUSPENSION — SUBTASK_release_bar (NeedsDecompose)

## Decision
`decompose_evaluation = NeedsDecompose`. This task consolidates five large area designs (≈395 requirements
total: PROD 42, DOM 81, UX 119, ID 78, OPS 75; experience-design.md alone is 4,671 lines) into a testable
release bar plus MVP-vs-releasable scoping plus a completeness/gap review. The Token, Scope-Based, and
Output-Size triggers all fire; faithful atomic execution would far exceed the 5–15 tool-call atomic envelope.
The only arguments for `Atomic` were "a release bar is one coherent judgment best held whole" — which the
standing contract and the Task Generation Invariant disqualify as grounds for Atomic. The by-area fan-out is the
sound cut and mirrors the sibling `SUBTASK_operational_readiness` pattern.

## Subtree materialized
Subtree hub `_GLOBAL.md` and the sub-contract (`contracts/_MANIFEST.yaml`, `contracts/bar_partition.yaml`,
extending `../contracts/` additively with the BAR number-space partition) are authored at this workspace. Six
children were materialized via `engine_amend_plan { add_task }`:

| Child | Task Kind | Depends on | Owns | Output |
|-------|-----------|-----------|------|--------|
| `SUBTASK_bar_prod` | standard | none | `BAR-001..099` (from release-gating `REQ-PROD-*`) | `SUBTASK_bar_prod/outputs/bar-prod.md` |
| `SUBTASK_bar_dom` | standard | none | `BAR-100..199` (from release-gating `REQ-DOM-*`) | `SUBTASK_bar_dom/outputs/bar-dom.md` |
| `SUBTASK_bar_ux` | standard | none | `BAR-200..299` (from release-gating `REQ-UX-*`) | `SUBTASK_bar_ux/outputs/bar-ux.md` |
| `SUBTASK_bar_id` | standard | none | `BAR-300..399` (from release-gating `REQ-ID-*`) | `SUBTASK_bar_id/outputs/bar-id.md` |
| `SUBTASK_bar_ops` | standard | none | `BAR-400..499` (from release-gating `REQ-OPS-*`) | `SUBTASK_bar_ops/outputs/bar-ops.md` |
| `SUBTASK_bar_synthesis` | synthesis | all five above | `BAR-900..999` cross-cutting, assembled bar, fold | `outputs/release-bar.md`, `SYNTHESIS.md` |

## Contract (the frozen seam)
`contracts/` extends the ancestor `../contracts/` additively: it partitions the one flat `BAR-*` number space
across the five area spokes (no collisions) + a synthesis cross-cutting range, fixes the bar-fragment field set
(from the inherited schema — `id`, `statement`, `references`, `verification_method`, `proposed_stage`), fixes
the proposed→final staging split (spokes propose a stage; the synthesis hub owns the one coherent cross-cutting
MVP line), and declares the eight identities the synthesis gate asserts (range respected; no collision; every
release-gating `REQ-*` covered; every `BAR-*` testable; every `BAR-*` staged; each expected surface judged
in/out of scope; three sections present; hygiene).

## Resumption condition
All children reach terminal state. `SUBTASK_bar_synthesis` folds the subtree: it assembles
`outputs/release-bar.md` (the three required sections, the parent's declared output), authors `SYNTHESIS.md` at
this workspace (the fold location), and resumes this task via `engine_resume_suspended`, which flips it
SUSPENDED → COMPLETED with `outputs/release-bar.md` as its declared output — unblocking the dependents
`SUBTASK_design_pr`, `SUBTASK_delivery_backlog`, and `SUBTASK_synthesis`.

## Environment note
The Phase-B `design` methodology loader is unavailable here (`agent_domain_unset`, run-wide; sibling synthesis
gates hit the same and proceeded). Methodology bundle IDs are relayed to each child in its brief; children apply
the product-design persona and that relayed guidance rather than blocking. This note is taskflow-internal and is
kept out of the repository-bound deliverable.
