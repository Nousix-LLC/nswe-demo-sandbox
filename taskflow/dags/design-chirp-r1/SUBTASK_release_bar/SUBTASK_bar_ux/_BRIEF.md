# Task: Release-bar criteria for the experience area (BAR-200..299)

## Task Specification
**Slug**: SUBTASK_bar_ux
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Author the `BAR-*` release-bar criteria (in the range `BAR-200..299`) that enforce every **release-gating**
`REQ-UX-*` from the experience design — the screens and flows (sign-up/in, the posting/timeline loops,
onboarding, settings), the empty/error/loading states, the visual system, responsive layout, and accessibility —
so each release-gating experience requirement is held to a concrete, testable release condition.

### Context
Part of the `SUBTASK_release_bar` subtree (see `../_GLOBAL.md` and the frozen seam `../contracts/`). You own the
experience-area slice of the release bar: the `BAR-200..299` range and the fragment file below. Sibling spokes
own the other areas; `SUBTASK_bar_synthesis` assembles all fragments, finalizes cross-cutting staging, and runs
the whole-design gap review — you propose a stage per `BAR-*` from the experience view and cover your area's
gating set. Note: the experience design is large (≈4,671 lines, ~119 `REQ-UX-*`); evaluate your own scope
honestly against the decomposition triggers at dispatch and decompose if warranted — the atomic-vs-decompose
decision is yours to make on your actual brief and inputs.
**Dependents**: `SUBTASK_bar_synthesis`.

## The concern you own
Turn the experience area's release-gating requirements into bar criteria that prove the product looks and
behaves as designed on the live product — a person can complete the core flows, the states render, the layout
holds on a phone, and the accessibility floor is met. A `BAR-*` is the checkable release condition, not a
restatement of the `REQ-*`; one `BAR-*` may enforce several related `REQ-UX-*`. Reference what it enforces; mint
`BAR-*` only in your range.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, identities, methodology posture |
| Inherited contract | `../../contracts/` (read-only) | `BAR-<NNN>` scheme, closed `verification_methods` vocab, stages |
| Subtree sub-contract | `../contracts/` (read-only) | Your `BAR-200..299` range; the bar-fragment field set; the proposed_stage convention |
| Experience design | `../../SUBTASK_experience_design/outputs/experience-design.md` | The authoritative `REQ-UX-*` set and which are release-gating (per-REQ `release_gating` field) |

## Output
- `SUBTASK_bar_ux/outputs/bar-ux.md` — one block per `BAR-*` carrying the fields fixed in
  `../contracts/bar_partition.yaml` (`id`, `statement`, `references` ≥1 `REQ-UX-*`, `verification_method`,
  `proposed_stage`), plus the coverage note listing every release-gating `REQ-UX-*` and the `BAR-*` that covers
  it. Repository-ready content (no host/system/taskflow detail, no attribution trailers).

## Success criteria
- [ ] Composes against `../contracts/` and `../../contracts/`; `BAR-*` only within `BAR-200..299`; schema not redefined.
- [ ] Every release-gating `REQ-UX-*` in the experience design is referenced by ≥1 `BAR-*`.
- [ ] Every `BAR-*` names a verification method from the frozen vocabulary, references ≥1 `REQ-*`, and carries a `proposed_stage`.
- [ ] The coverage note lets the synthesis gate assert gating coverage without re-deriving the gating set.

## Constraints
- A bar, not an aspiration — each criterion checkable by someone who was not in the room. Accessibility criteria
  name the concrete check (e.g. a stated conformance level verified by inspection), not "accessible".
- Reference `REQ-*`; do not re-author requirements. State release conditions as checkable facts, not implementations.
- Methodology bundles (relayed; loader unavailable, apply the product-design persona + this guidance): Release
  Definition (primary); Experience Design, Product Strategy (support).
