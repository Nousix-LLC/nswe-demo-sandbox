# Task: Release-bar criteria for the domain & application area (BAR-100..199)

## Task Specification
**Slug**: SUBTASK_bar_dom
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Author the `BAR-*` release-bar criteria (in the range `BAR-100..199`) that enforce every **release-gating**
`REQ-DOM-*` from the domain & application design — including the **durable-persistence requirement** (the
in-memory store is a release blocker) — so each release-gating domain requirement is held to a concrete,
testable release condition.

### Context
Part of the `SUBTASK_release_bar` subtree (see `../_GLOBAL.md` and the frozen seam `../contracts/`). You own the
domain-area slice of the release bar: the `BAR-100..199` range and the fragment file below. Sibling spokes own
the other areas; `SUBTASK_bar_synthesis` assembles all fragments, finalizes cross-cutting staging, and runs the
whole-design gap review — you propose a stage per `BAR-*` from the domain view and cover your area's gating set.
**Dependents**: `SUBTASK_bar_synthesis`.

## The concern you own
Turn the domain area's release-gating requirements into bar criteria that prove the product's data and
structure actually hold on the live product — durability across restart/redeploy being the headline condition.
A `BAR-*` is the checkable release condition, not a restatement of the `REQ-*`; one `BAR-*` may enforce several
related `REQ-DOM-*`. Reference what it enforces; mint `BAR-*` only in your range.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, identities, methodology posture |
| Inherited contract | `../../contracts/` (read-only) | `BAR-<NNN>` scheme, closed `verification_methods` vocab, stages |
| Subtree sub-contract | `../contracts/` (read-only) | Your `BAR-100..199` range; the bar-fragment field set; the proposed_stage convention |
| Domain & application design | `../../SUBTASK_domain_app_design/outputs/domain-application-design.md` | The authoritative `REQ-DOM-*` set and which are release-gating (per-REQ `release_gating` field) |

## Output
- `SUBTASK_bar_dom/outputs/bar-dom.md` — one block per `BAR-*` carrying the fields fixed in
  `../contracts/bar_partition.yaml` (`id`, `statement`, `references` ≥1 `REQ-DOM-*`, `verification_method`,
  `proposed_stage`), plus the coverage note listing every release-gating `REQ-DOM-*` and the `BAR-*` that covers
  it. Repository-ready content (no host/system/taskflow detail, no attribution trailers).

## Success criteria
- [ ] Composes against `../contracts/` and `../../contracts/`; `BAR-*` only within `BAR-100..199`; schema not redefined.
- [ ] Every release-gating `REQ-DOM-*` in the domain design is referenced by ≥1 `BAR-*` (the durable-persistence blocker included).
- [ ] Every `BAR-*` names a verification method from the frozen vocabulary, references ≥1 `REQ-*`, and carries a `proposed_stage`.
- [ ] The coverage note lets the synthesis gate assert gating coverage without re-deriving the gating set.

## Constraints
- A bar, not an aspiration — each criterion checkable by someone who was not in the room.
- Reference `REQ-*`; do not re-author requirements, and do not specify implementation ("how"). State release conditions as checkable facts.
- Methodology bundles (relayed; loader unavailable, apply the product-design persona + this guidance): Release
  Definition (primary); Product Strategy, Release Readiness (support).
