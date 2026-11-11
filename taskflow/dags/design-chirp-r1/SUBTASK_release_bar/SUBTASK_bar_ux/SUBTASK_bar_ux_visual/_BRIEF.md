# Task: Release-bar criteria for the visual language & component area (BAR-215..229)

## Task Specification
**Slug**: SUBTASK_bar_ux_visual
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Author the `BAR-*` release-bar criteria in the range `BAR-215..229` that enforce every **release-gating**
`REQ-UX-*` in the visual-language & component-system area (`REQ-UX-020..039`): one product read from one token
set, legible text and clear hierarchy, WCAG 2.1 AA colour contrast, visible focus indicators, consistent
spacing/grid/measure, consistent elevation/layering, consistent iconography that never carries meaning by
colour alone, bounded and reduced-motion-respecting motion, designed empty/loading/error visual treatments, a
consistent voice with plain actionable errors, screens built from the named component vocabulary and published
tokens, and the chirp-card / compose-box / list / form / confirmation / feedback component behaviours. Each
release-gating requirement in this band must be held to a concrete, testable release condition.

### Context
Part of the `SUBTASK_bar_ux` subtree (see `../_GLOBAL.md` and the frozen seams `../contracts/`, `../../contracts/`,
`../../../contracts/`). You own the visual/component-area slice: the `BAR-215..229` sub-range and the fragment
file below. Sibling spokes own the other experience areas; `SUBTASK_bar_ux_synthesis` assembles all sub-fragments,
finalizes the within-UX staging, and asserts coverage — you propose a stage per `BAR-*` from the visual view and
cover your area's gating set.
**Dependents**: `SUBTASK_bar_ux_synthesis`.

## The concern you own
Turn the visual/component area's release-gating requirements into bar criteria that prove the product looks and
reads as one designed product on the live product — consistent type/colour/spacing from the token set, AA
contrast and visible focus, a named component vocabulary rather than one-off controls, the core-loop components
(chirp card, compose box, list, form, confirmation dialog, feedback) behaving to contract, and empty/loading/
error states carrying a designed treatment. A `BAR-*` is the checkable release condition, not a restatement of
the `REQ-*`; one `BAR-*` may enforce several related `REQ-UX-*`. Contrast criteria name the concrete measured
check (e.g. ≥4.5:1 normal text sampled with a contrast tool), not "accessible" or "good contrast". Reference
what it enforces; mint `BAR-*` only in your range.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, identities, methodology posture |
| This subtree contract | `../contracts/` (read-only) | Your `BAR-215..229` sub-range; the per-area gating set; the bar-fragment field set; the proposed_stage convention |
| Parent BAR partition | `../../contracts/` (read-only) | The `SUBTASK_release_bar` partition (this subtree owns `BAR-200..299`) |
| DAG-root schema | `../../../contracts/` (read-only) | `BAR-<NNN>` scheme, closed `verification_methods` vocab, stages |
| Experience design | `../../../SUBTASK_experience_design/outputs/experience-design.md` | The authoritative `REQ-UX-020..039` set and the per-REQ `release_gating` flag |

Your area's release-gating set (read the `release_gating` field in the design for the authoritative list):
`REQ-UX-020, 021, 022, 025, 026, 027, 028, 029, 031, 032, 033, 034, 035, 036, 037, 038, 039` (17 gating).
Non-gating in this band: `REQ-UX-023`, `024`, `030` — not covered.

## Output
- `SUBTASK_bar_ux_visual/outputs/bar-ux-visual.md` — one block per `BAR-*` carrying the fields fixed in
  `../contracts/bar_ux_partition.yaml` (`id`, `statement`, `references` ≥1 `REQ-UX-*`, `verification_method`,
  `proposed_stage`), plus a coverage note listing every release-gating `REQ-UX-*` in your band and the `BAR-*`
  that covers it. Repository-ready content (no host/system/taskflow detail, no attribution trailers).

## Success criteria
- [ ] Composes against `../contracts/`, `../../contracts/`, `../../../contracts/`; `BAR-*` only within `BAR-215..229`; no inherited schema redefined.
- [ ] Every release-gating `REQ-UX-*` in your band (020, 021, 022, 025..029, 031..039) is referenced by ≥1 `BAR-*`.
- [ ] Every `BAR-*` names a verification method from the frozen vocabulary, references ≥1 `REQ-*`, and carries a `proposed_stage`.
- [ ] No `BAR-*` is justified solely by a non-gating `REQ-UX-*` (023, 024, 030).
- [ ] The coverage note lets the synthesis gate assert visual-area gating coverage without re-deriving the gating set.

## Constraints
- A bar, not an aspiration — each criterion checkable by someone who was not in the room. Contrast and visual
  criteria name the concrete measurable check, not an abstract quality word. State release conditions as
  checkable facts, not implementations.
- Reference `REQ-*`; do not re-author requirements.
- Methodology bundles (relayed; loader unavailable, apply the product-design persona + this guidance): Release
  Definition (primary); Experience Design, Product Strategy (support).
- Evaluate your own scope against the decomposition triggers at dispatch; the atomic-vs-decompose decision is
  yours to make on your actual brief and inputs.
