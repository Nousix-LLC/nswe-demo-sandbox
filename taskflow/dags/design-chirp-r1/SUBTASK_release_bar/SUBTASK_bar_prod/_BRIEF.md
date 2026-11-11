# Task: Release-bar criteria for the product area (BAR-001..099)

## Task Specification
**Slug**: SUBTASK_bar_prod
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Author the `BAR-*` release-bar criteria (in the range `BAR-001..099`) that enforce every **release-gating**
`REQ-PROD-*` from the product-requirements design, so that each release-gating product requirement is held to a
concrete, testable release condition.

### Context
Part of the `SUBTASK_release_bar` subtree (see `../_GLOBAL.md` and the frozen seam `../contracts/`). You own the
product-area slice of the release bar: the `BAR-001..099` range and the fragment file below. A sibling spoke
owns each other area; the `SUBTASK_bar_synthesis` hub assembles all five fragments into the one
`release-bar.md`, finalizes the cross-cutting MVP-vs-releasable staging, and runs the whole-design gap review —
so you do **not** own staging coherence across areas or the gap review; you propose a stage per `BAR-*` from the
product view and cover your area's gating requirements.
**Dependents**: `SUBTASK_bar_synthesis`.

## The concern you own
Turn the product area's release-gating requirements into bar criteria. A `BAR-*` is not a restatement of a
`REQ-*`: it is the checkable release condition that proves the requirement holds on the live product. One
`BAR-*` may enforce several related `REQ-PROD-*`; reference all it enforces. If a product release condition is
genuinely enforced jointly with another area, you may reference that area's `REQ-*` too, but mint the `BAR-*`
only within your own range.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, identities, methodology posture |
| Inherited contract | `../../contracts/` (read-only) | `BAR-<NNN>` scheme, closed `verification_methods` vocab, stages |
| Subtree sub-contract | `../contracts/` (read-only) | Your `BAR-001..099` range; the bar-fragment field set; the proposed_stage convention |
| Product requirements design | `../../SUBTASK_product_requirements/outputs/product-requirements.md` | The authoritative `REQ-PROD-*` set and which are release-gating (per-REQ `release_gating` field) |

## Output
- `SUBTASK_bar_prod/outputs/bar-prod.md` — one block per `BAR-*` carrying the fields fixed in
  `../contracts/bar_partition.yaml` (`id`, `statement`, `references` ≥1 `REQ-PROD-*`, `verification_method` from
  the vocabulary, `proposed_stage`), plus the coverage note listing every release-gating `REQ-PROD-*` and the
  `BAR-*` that covers it. Repository-ready content (no host/system/taskflow detail, no attribution trailers).

## Success criteria
- [ ] Composes against `../contracts/` and `../../contracts/`; `BAR-*` only within `BAR-001..099`; schema not redefined.
- [ ] Every release-gating `REQ-PROD-*` in the product design is referenced by ≥1 `BAR-*`.
- [ ] Every `BAR-*` names a verification method from the frozen vocabulary, references ≥1 `REQ-*`, and carries a `proposed_stage`.
- [ ] The coverage note lets the synthesis gate assert gating coverage without re-deriving the gating set.

## Constraints
- A bar, not an aspiration — each criterion checkable by someone who was not in the room.
- Reference `REQ-*`; do not re-author requirements. State release conditions as checkable facts, not implementations.
- Methodology bundles (relayed; loader unavailable, apply the product-design persona + this guidance): Release
  Definition (primary); Product Strategy, Release Readiness (support).
