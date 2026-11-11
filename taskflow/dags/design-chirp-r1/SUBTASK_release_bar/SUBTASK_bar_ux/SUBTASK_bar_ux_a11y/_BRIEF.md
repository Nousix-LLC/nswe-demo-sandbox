# Task: Release-bar criteria for the accessibility area (BAR-275..294)

## Task Specification
**Slug**: SUBTASK_bar_ux_a11y
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Author the `BAR-*` release-bar criteria in the range `BAR-275..294` that enforce every **release-gating**
`REQ-UX-*` in the accessibility area (`REQ-UX-100..119`): the named, versioned standard (WCAG 2.1 AA) and the
gated conformance set; keyboard operability of every action; logical, always-visible focus order; no keyboard
trap with escapable modal focus; a skip-to-content bypass; name/role/state on every control; landmark regions;
one nested top-level heading per screen; lists/feeds exposed as navigable lists; icon-only controls with text
labels and active state; AA contrast in every shipped theme; text resize/reflow to 200% and 320px without loss;
no-colour-alone and no-flash; honoured reduced motion; status changes announced without stealing focus; errors
announced and tied to their field; empty/loading/expired-session states reaching assistive technology; the
three-way conformance verification over the gated set; and accessibility gating the release (failures are fixes,
not waivers). Each release-gating requirement in this band must be held to a concrete, testable release
condition.

### Context
Part of the `SUBTASK_bar_ux` subtree (see `../_GLOBAL.md` and the frozen seams `../contracts/`, `../../contracts/`,
`../../../contracts/`). You own the accessibility-area slice: the `BAR-275..294` sub-range and the fragment file
below. Sibling spokes own the other experience areas; `SUBTASK_bar_ux_synthesis` assembles all sub-fragments,
finalizes the within-UX staging, and asserts coverage — you propose a stage per `BAR-*` from the accessibility
view and cover your area's gating set.
**Dependents**: `SUBTASK_bar_ux_synthesis`.

## The concern you own
Turn the accessibility area's release-gating requirements into bar criteria that prove the product meets its
committed WCAG 2.1 AA floor on the live product — verified, not asserted. Each `BAR-*` names the concrete check:
the specific WCAG success criterion and how it is verified (an automated scan per shipped theme, a keyboard-only
pass, a screen-reader pass over the stated support matrix, or inspection of a declared property) over the gated
conformance set (the core loop and the get-in screens with their empty/loading/error states). A `BAR-*` is the
checkable release condition, never "accessible" in the abstract; one `BAR-*` may enforce several related
`REQ-UX-*`. Reference what it enforces; mint `BAR-*` only in your range.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, identities, methodology posture |
| This subtree contract | `../contracts/` (read-only) | Your `BAR-275..294` sub-range; the per-area gating set; the bar-fragment field set; the proposed_stage convention |
| Parent BAR partition | `../../contracts/` (read-only) | The `SUBTASK_release_bar` partition (this subtree owns `BAR-200..299`) |
| DAG-root schema | `../../../contracts/` (read-only) | `BAR-<NNN>` scheme, closed `verification_methods` vocab, stages |
| Experience design | `../../../SUBTASK_experience_design/outputs/experience-design.md` | The authoritative `REQ-UX-100..119` set and the per-REQ `release_gating` flag |

Your area's release-gating set (read the `release_gating` field in the design for the authoritative list):
`REQ-UX-100..104, 106..119` (19 gating). Non-gating in this band: `REQ-UX-105` (WCAG 2.2 target size, staged
ahead of the committed 2.1 AA floor) — not covered.

## Output
- `SUBTASK_bar_ux_a11y/outputs/bar-ux-a11y.md` — one block per `BAR-*` carrying the fields fixed in
  `../contracts/bar_ux_partition.yaml` (`id`, `statement`, `references` ≥1 `REQ-UX-*`, `verification_method`,
  `proposed_stage`), plus a coverage note listing every release-gating `REQ-UX-*` in your band and the `BAR-*`
  that covers it. Repository-ready content (no host/system/taskflow detail, no attribution trailers).

## Success criteria
- [ ] Composes against `../contracts/`, `../../contracts/`, `../../../contracts/`; `BAR-*` only within `BAR-275..294`; no inherited schema redefined.
- [ ] Every release-gating `REQ-UX-*` in your band (100..104, 106..119) is referenced by ≥1 `BAR-*`.
- [ ] Every `BAR-*` names a verification method from the frozen vocabulary, references ≥1 `REQ-*`, and carries a `proposed_stage`.
- [ ] No `BAR-*` is justified solely by the non-gating `REQ-UX-105`.
- [ ] The coverage note lets the synthesis gate assert accessibility-area gating coverage without re-deriving the gating set.

## Constraints
- A bar, not an aspiration — each criterion checkable by someone who was not in the room. Accessibility criteria
  name the concrete check (the WCAG success criterion and the verification method), never the abstract word
  "accessible". State release conditions as checkable facts, not implementations.
- Reference `REQ-*`; do not re-author requirements.
- Methodology bundles (relayed; loader unavailable, apply the product-design persona + this guidance): Release
  Definition (primary); Experience Design, Product Strategy (support).
- Evaluate your own scope against the decomposition triggers at dispatch; the atomic-vs-decompose decision is
  yours to make on your actual brief and inputs.
