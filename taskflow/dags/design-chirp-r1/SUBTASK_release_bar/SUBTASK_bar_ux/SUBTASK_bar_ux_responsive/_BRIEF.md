# Task: Release-bar criteria for the responsive-layout area (BAR-265..274)

## Task Specification
**Slug**: SUBTASK_bar_ux_responsive
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Author the `BAR-*` release-bar criteria in the range `BAR-265..274` that enforce every **release-gating**
`REQ-UX-*` in the responsive-layout area (`REQ-UX-090..099`): the whole core loop usable on a phone; one
reading column reflowed not rescaled across viewports; the signed-in navigation shell adapting while keeping
every destination reachable; the signed-out shell never dead-ending at any viewport; feed/list screens adapting
without losing their controls or scroll place; form screens usable with the on-screen keyboard; profile and
settings screens stacking with a way back; overlays as full-height surfaces on a phone with reachable actions;
touch targets large enough and within thumb reach; and no auto-zoom / no horizontal scroll in portrait and
landscape. Each release-gating requirement in this band must be held to a concrete, testable release condition.

### Context
Part of the `SUBTASK_bar_ux` subtree (see `../_GLOBAL.md` and the frozen seams `../contracts/`, `../../contracts/`,
`../../../contracts/`). You own the responsive-area slice: the `BAR-265..274` sub-range and the fragment file
below. Sibling spokes own the other experience areas; `SUBTASK_bar_ux_synthesis` assembles all sub-fragments,
finalizes the within-UX staging, and asserts coverage — you propose a stage per `BAR-*` from the responsive view
and cover your area's gating set.
**Dependents**: `SUBTASK_bar_ux_synthesis`.

## The concern you own
Turn the responsive area's release-gating requirements into bar criteria that prove the product holds its layout
and remains fully usable across viewports on the live product — the core loop completes on a phone, content
reflows to one column without horizontal scroll or pinch-zoom in portrait and landscape, every navigation
destination and control stays reachable and tappable, and forms work with the on-screen keyboard. A `BAR-*` is
the checkable release condition, not a restatement of the `REQ-*`; name the concrete viewport check (e.g. at a
360×640 CSS-px portrait viewport, no horizontal page scroll; touch targets ≥ the stated minimum), not
"responsive" or "mobile-friendly". One `BAR-*` may enforce several related `REQ-UX-*`. Reference what it
enforces; mint `BAR-*` only in your range.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, identities, methodology posture |
| This subtree contract | `../contracts/` (read-only) | Your `BAR-265..274` sub-range; the per-area gating set; the bar-fragment field set; the proposed_stage convention |
| Parent BAR partition | `../../contracts/` (read-only) | The `SUBTASK_release_bar` partition (this subtree owns `BAR-200..299`) |
| DAG-root schema | `../../../contracts/` (read-only) | `BAR-<NNN>` scheme, closed `verification_methods` vocab, stages |
| Experience design | `../../../SUBTASK_experience_design/outputs/experience-design.md` | The authoritative `REQ-UX-090..099` set and the per-REQ `release_gating` flag |

Your area's release-gating set (read the `release_gating` field in the design for the authoritative list):
`REQ-UX-090..099` (all 10 gating). Non-gating in this band: none.

## Output
- `SUBTASK_bar_ux_responsive/outputs/bar-ux-responsive.md` — one block per `BAR-*` carrying the fields fixed in
  `../contracts/bar_ux_partition.yaml` (`id`, `statement`, `references` ≥1 `REQ-UX-*`, `verification_method`,
  `proposed_stage`), plus a coverage note listing every release-gating `REQ-UX-*` in your band and the `BAR-*`
  that covers it. Repository-ready content (no host/system/taskflow detail, no attribution trailers).

## Success criteria
- [ ] Composes against `../contracts/`, `../../contracts/`, `../../../contracts/`; `BAR-*` only within `BAR-265..274`; no inherited schema redefined.
- [ ] Every release-gating `REQ-UX-*` in your band (090..099) is referenced by ≥1 `BAR-*`.
- [ ] Every `BAR-*` names a verification method from the frozen vocabulary, references ≥1 `REQ-*`, and carries a `proposed_stage`.
- [ ] The coverage note lets the synthesis gate assert responsive-area gating coverage without re-deriving the gating set.

## Constraints
- A bar, not an aspiration — each criterion checkable by someone who was not in the room, with the concrete
  viewport/target measurement named. State release conditions as checkable facts, not implementations.
- Reference `REQ-*`; do not re-author requirements.
- Methodology bundles (relayed; loader unavailable, apply the product-design persona + this guidance): Release
  Definition (primary); Experience Design, Product Strategy (support).
- Evaluate your own scope against the decomposition triggers at dispatch; the atomic-vs-decompose decision is
  yours to make on your actual brief and inputs.
