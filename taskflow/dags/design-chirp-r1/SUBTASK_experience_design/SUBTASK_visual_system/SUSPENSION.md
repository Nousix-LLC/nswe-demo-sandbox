# SUSPENSION.md — SUBTASK_visual_system (NeedsDecompose)

## Why this node suspended

`SUBTASK_visual_system` evaluated its brief against the decomposition triggers and declared
`NeedsDecompose`. It authored its subtree (hub `_GLOBAL.md`, the internal `contracts/`, and one `_BRIEF.md`
per child), materialized the three children via `engine_amend_plan { add_task }`, and now suspends pending
their resolution. It executed none of the children's work.

## Evaluation that produced NeedsDecompose

Triggers applied to the actual brief and inputs:

- **Token (input)** — CLEARED. Inputs (screen inventory, product requirements, contracts) are well under 50%
  of context.
- **Output Size** — FIRED. A full visual language across seven sub-areas + a named design-token set + a
  ~14-component library each with its states + up to twenty testable `REQ-UX` entries is a ~600-line
  deliverable, over the 400-line MUST-decompose line.
- **Scope / Enumerated-concerns** — FIRED. The brief enumerates distinct concerns (visual language; component
  library; design tokens/consistency rules), and the component library composes against the visual language
  across a real token seam the parent contract already treats as a distinct shared vocabulary.
- **Distinct Concerns / Single-Responsibility** — the visual-language-and-tokens foundation and the component
  vocabulary built on it are two responsibilities joined by a serial seam (components are instantiations of
  the tokens), not one.

Per the disjunction rule and the asymmetric bias (a fired trigger means not atomic; over-decomposition is
penalty-free), the verdict is `NeedsDecompose`. The professional instinct that "a design system is one
coherent picture held in one head" carries no weight at the evaluation point and was not used as grounds for
atomicity.

## Children materialized (recursive-depth placement = this task)

| Child (task id) | Depends on | Owns | Output |
|---|---|---|---|
| `SUBTASK_visual_language` | none | `visual_language_and_design_system` section body + design-token vocabulary + consistency rules + `REQ-UX-020..032` | `SUBTASK_visual_language/outputs/visual-language.md` |
| `SUBTASK_component_library` | `SUBTASK_visual_language` | "Component library" heading content + component vocabulary + `REQ-UX-033..039` | `SUBTASK_component_library/outputs/component-library.md` |
| `SUBTASK_visual_system/SUBTASK_synthesis` | both content children | assembled `outputs/visual-system.md` + consolidated `REQ-UX-020..039` + `SYNTHESIS.md`; folds this node | `outputs/visual-system.md`, `SYNTHESIS.md` |

Contract frozen before any child runs: `contracts/_MANIFEST.yaml` + `contracts/visual_system_seam.yaml`
(section split, `REQ-UX-020..039` sub-ranges, the design-token seam, the component coverage rule, and the
eight identities the synthesis gate asserts).

## Resumption condition

All child tasks reach a terminal lifecycle state. `SUBTASK_visual_system/SUBTASK_synthesis` then assembles
`outputs/visual-system.md`, asserts the identities, authors `SYNTHESIS.md`, and folds `SUBTASK_visual_system`
`SUSPENDED → COMPLETED`.

## Note on environment

The design-domain methodology loader is unavailable in the current reconstructed environment (the loader
syscall reports the agent domain unset). The children design from the Experience Design bundle intent and
product-design competence and record the limitation; this did not block the decomposition.
