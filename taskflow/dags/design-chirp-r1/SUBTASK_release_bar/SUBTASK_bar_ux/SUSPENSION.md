# SUSPENSION.md — SUBTASK_bar_ux (decomposition)

**Status**: SUSPENDED — `decompose_evaluation = NeedsDecompose`.

## Why this task decomposed

My brief owns the experience-area slice of the whole-product release bar: `BAR-200..299` enforcing every
release-gating `REQ-UX-*`. Applying the decomposition triggers to my actual brief and the fully-read input
(experience-design.md, 4,671 lines, 119 `REQ-UX-*`, **106 release-gating**):

- **Output-Size trigger FIRED** — a comprehensive UX bar fragment (one block per `BAR-*` across ~106 gating
  requirements) plus a ~106-row coverage note is an estimated ~450–650 lines, over the 400-line MUST-decompose
  line.
- **Scope** — the brief enumerates five distinct experience areas (IA & interaction, visual/component system,
  screens & flows, responsive layout, accessibility); screens & flows alone carries ~43 gating requirements.
- Token and single-responsibility signals cleared; but a trigger fired and the evaluation was genuinely
  uncertain, so the normative asymmetric bias (uncertain ⇒ decompose; over-decomposing carries no penalty) and
  the standing design contract (I may not declare `Atomic` on the "a flat BAR range is best held in one head /
  splitting fragments the clusters" instinct) resolve to **NeedsDecompose**. This recursively mirrors the
  parent `SUBTASK_release_bar` by-area fan-out.

## What was authored (the subtree)

- `_GLOBAL.md` — subtree hub (objective, scope, constraints, Task Summary, contract, identities).
- `contracts/_MANIFEST.yaml` + `contracts/bar_ux_partition.yaml` — the sub-contract: sub-partition of
  `BAR-200..299` across five area spokes + a synthesis cross-cutting range, the per-area release-gating
  `REQ-UX-*` sets, the fragment layout, and the subtree identities. Extends the inherited `../contracts/` and
  `../../contracts/` additively; redefines nothing.
- Six child briefs (materialized via `add_task`):

| Child | Sub-range | Covers (release-gating REQ-UX-*) | Depends on |
|-------|-----------|----------------------------------|------------|
| `SUBTASK_bar_ux_ia` | BAR-200..214 | 001..014, 016, 017, 018 (17) | none |
| `SUBTASK_bar_ux_visual` | BAR-215..229 | 020, 021, 022, 025..029, 031..039 (17) | none |
| `SUBTASK_bar_ux_screens` | BAR-230..264 | 040..056, 058..063, 065..070, 073..077, 079, 082..089 (43) | none |
| `SUBTASK_bar_ux_responsive` | BAR-265..274 | 090..099 (10) | none |
| `SUBTASK_bar_ux_a11y` | BAR-275..294 | 100..104, 106..119 (19) | none |
| `SUBTASK_bar_ux_synthesis` | BAR-295..299 (cross-cutting) | assemble + gate + fold | the five spokes |

Non-gating `REQ-UX-*` excluded from coverage: 015, 019, 023, 024, 030, 057, 064, 071, 072, 078, 080, 081, 105.

## Resumption condition

All child tasks reach terminal lifecycle state. `SUBTASK_bar_ux_synthesis` assembles the five sub-fragments
into `SUBTASK_bar_ux/outputs/bar-ux.md` (this task's declared output), asserts the subtree identities with
recorded evidence, authors `SUBTASK_bar_ux/SYNTHESIS.md`, and folds this task (`SUSPENDED → COMPLETED`) via the
synthesis fold.

## Methodology posture

The Phase-B `design` methodology loader is unavailable in this environment (`agent_domain_unset`, run-wide);
the product-designer persona's release-definition judgment and the relayed bundle guidance (Release Definition
primary; Experience Design, Product Strategy supporting) are applied instead. Recorded internally only; kept
out of the repository-bound `bar-ux.md`.
