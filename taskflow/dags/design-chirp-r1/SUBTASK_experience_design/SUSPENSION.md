# SUSPENSION.md — SUBTASK_experience_design (NeedsDecompose)

## Outcome
Decomposed. This node evaluated its brief against the decomposition triggers and found it spans five
distinct design disciplines plus a large, cross-referencing deliverable; it therefore decomposes into a
hub-and-spoke subtree and suspends pending the subtree's resolution. No experience-design content is
authored at this node — the children produce it and the synthesis gate folds it.

## Why NeedsDecompose (triggers applied at the evaluation point)
- **Scope / enumerated-concerns** — the brief enumerates five distinct concerns (IA & interaction;
  screens & flows; visual language & design system; responsive layout; accessibility). The Scope trigger
  fires by that enumeration alone. FIRES.
- **Distinct Concerns Test** — IA/interaction, visual/design-system, and accessibility are genuinely
  separable specialties. FIRES.
- **Single-Responsibility / conjunction** — the faithful task description joins distinct deliverables
  with "and"; multiple kinds of output. FIRES.
- **Output Size** — the full experience design (every journey's screens with empty/error/loading states,
  a design system, responsive rules, accessibility, and a complete REQ-UX register) far exceeds 400
  lines. FIRES (MUST decompose).
- Per Trigger Precedence, the single declared output file does not override the fired scope signals; the
  persona instinct to hold the experience whole carries no weight at the evaluation point.

## Subtree materialized (children added under this node via engine_amend_plan)
| Child id | Depends on | Owns | Output |
|---|---|---|---|
| `SUBTASK_ia_interaction` | — | IA & interaction section; screen inventory; `REQ-UX-001..019` | `SUBTASK_ia_interaction/outputs/ia-interaction.md` |
| `SUBTASK_visual_system` | ia_interaction | Visual system section; component library; `REQ-UX-020..039` | `SUBTASK_visual_system/outputs/visual-system.md` |
| `SUBTASK_screens_flows` | ia_interaction, visual_system | Screens & flows + empty/error/loading sections; `REQ-UX-040..089` | `SUBTASK_screens_flows/outputs/screens-flows.md` |
| `SUBTASK_responsive` | ia_interaction, visual_system | Responsive section; `REQ-UX-090..099` | `SUBTASK_responsive/outputs/responsive.md` |
| `SUBTASK_accessibility` | ia_interaction, visual_system | Accessibility section; `REQ-UX-100..119` | `SUBTASK_accessibility/outputs/accessibility.md` |
| `SUBTASK_experience_synthesis` (Task Kind: synthesis) | all five | Assembled deliverable + consolidated REQ-UX register; identity assertions; fold | `outputs/experience-design.md` + `SYNTHESIS.md` |

(The synthesis child's id is `SUBTASK_experience_synthesis` to avoid collision with the parent subtree's
top-level `SUBTASK_synthesis`; its workspace is `SUBTASK_synthesis/`.)

## Named state authored before this suspension
- `_GLOBAL.md` — this subtree's hub (task tree + contract).
- `contracts/_MANIFEST.yaml`, `contracts/ux_section_and_id_map.yaml` — the internal seam (section
  ownership, REQ-UX id-range partition, shared vocabularies, trace rule, eight identities). Extends the
  parent `../contracts/` additively; does not override it.
- `SUBTASK_*/_BRIEF.md` — one brief per child (six).

## Deliverable on fold
`SUBTASK_experience_design/outputs/experience-design.md` — the one experience-design document with all
required sections (per `../contracts/design_artifact_map.yaml`) and the full `REQ-UX-*` register, produced
by the synthesis child, which folds this node SUSPENDED → COMPLETED via its `SYNTHESIS.md`.

## Environment note
The Phase-B methodology-loader syscall reports the agent domain unset in this reconstructed node, so
design-bundle bodies were not resolvable here. The decomposition proceeded from the bundle intent named
in the brief (Experience Design primary; Product Strategy, Identity and Trust supporting) and
product-design competence; each child brief propagates the bundle IDs and records the same fallback.

## Resumption condition
All children reach terminal lifecycle state and `SUBTASK_experience_synthesis` folds this node to
COMPLETED (implicit for the NeedsDecompose case).
