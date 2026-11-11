# Task: Release-bar criteria for the IA & interaction area (BAR-200..214)

## Task Specification
**Slug**: SUBTASK_bar_ux_ia
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Author the `BAR-*` release-bar criteria in the range `BAR-200..214` that enforce every **release-gating**
`REQ-UX-*` in the information-architecture & interaction-model area (`REQ-UX-001..019`): the signed-out and
signed-in shells, wayfinding and the screen inventory, addressable/shareable URLs, auth-gated routing and
session-expiry recovery, predictable browser navigation, bounded-page list loading with catch-up, destructive-
action confirmation, action feedback, compose reachability, sign-up→onboarding landing, sign-out no-leak, the
settings grouping, and the reachability of rules/help. Each release-gating requirement in this band must be
held to a concrete, testable release condition.

### Context
Part of the `SUBTASK_bar_ux` subtree (see `../_GLOBAL.md` and the frozen seams `../contracts/`, `../../contracts/`,
`../../../contracts/`). You own the IA-area slice: the `BAR-200..214` sub-range and the fragment file below.
Sibling spokes own the other experience areas; `SUBTASK_bar_ux_synthesis` assembles all sub-fragments, finalizes
the within-UX staging, and asserts coverage — you propose a stage per `BAR-*` from the IA view and cover your
area's gating set.
**Dependents**: `SUBTASK_bar_ux_synthesis`.

## The concern you own
Turn the IA area's release-gating requirements into bar criteria that prove the product's navigation, routing,
and wayfinding behave as designed on the live product — a person is never dead-ended, always knows where they
are, can reach every required surface, is returned where they asked to go after auth, recovers from an expired
session without losing work, and has destructive actions confirmed and action results shown. A `BAR-*` is the
checkable release condition, not a restatement of the `REQ-*`; one `BAR-*` may enforce several related
`REQ-UX-*`. Reference what it enforces; mint `BAR-*` only in your range.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, identities, methodology posture |
| This subtree contract | `../contracts/` (read-only) | Your `BAR-200..214` sub-range; the per-area gating set; the bar-fragment field set; the proposed_stage convention |
| Parent BAR partition | `../../contracts/` (read-only) | The `SUBTASK_release_bar` partition (this subtree owns `BAR-200..299`) |
| DAG-root schema | `../../../contracts/` (read-only) | `BAR-<NNN>` scheme, closed `verification_methods` vocab, stages |
| Experience design | `../../../SUBTASK_experience_design/outputs/experience-design.md` | The authoritative `REQ-UX-001..019` set and the per-REQ `release_gating` flag |

Your area's release-gating set (read the `release_gating` field in the design for the authoritative list):
`REQ-UX-001..014, 016, 017, 018` (17 gating). Non-gating in this band: `REQ-UX-015`, `REQ-UX-019` — not covered.

## Output
- `SUBTASK_bar_ux_ia/outputs/bar-ux-ia.md` — one block per `BAR-*` carrying the fields fixed in
  `../contracts/bar_ux_partition.yaml` (`id`, `statement`, `references` ≥1 `REQ-UX-*`, `verification_method`,
  `proposed_stage`), plus a coverage note listing every release-gating `REQ-UX-*` in your band and the `BAR-*`
  that covers it. Repository-ready content (no host/system/taskflow detail, no attribution trailers).

## Success criteria
- [ ] Composes against `../contracts/`, `../../contracts/`, `../../../contracts/`; `BAR-*` only within `BAR-200..214`; no inherited schema redefined.
- [ ] Every release-gating `REQ-UX-*` in your band (001..014, 016, 017, 018) is referenced by ≥1 `BAR-*`.
- [ ] Every `BAR-*` names a verification method from the frozen vocabulary, references ≥1 `REQ-*`, and carries a `proposed_stage`.
- [ ] No `BAR-*` is justified solely by a non-gating `REQ-UX-*` (015, 019).
- [ ] The coverage note lets the synthesis gate assert IA-area gating coverage without re-deriving the gating set.

## Constraints
- A bar, not an aspiration — each criterion checkable by someone who was not in the room. State release
  conditions as checkable facts, not implementations.
- Reference `REQ-*`; do not re-author requirements.
- Methodology bundles (relayed; loader unavailable, apply the product-design persona + this guidance): Release
  Definition (primary); Experience Design, Product Strategy (support).
- Evaluate your own scope against the decomposition triggers at dispatch; the atomic-vs-decompose decision is
  yours to make on your actual brief and inputs.
