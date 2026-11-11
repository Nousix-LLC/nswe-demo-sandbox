# Task: Assemble and gate the experience-area release-bar fragment (bar-ux.md) + fold

## Task Specification
**Slug**: SUBTASK_bar_ux_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_bar_ux_ia, SUBTASK_bar_ux_visual, SUBTASK_bar_ux_screens, SUBTASK_bar_ux_responsive, SUBTASK_bar_ux_a11y
**Status**: Pending

### Objective
Assemble the five experience-area sub-fragments into the single `SUBTASK_bar_ux/outputs/bar-ux.md` — the
`SUBTASK_bar_ux` task's declared output — verify the subtree identities with recorded evidence (no silent
plugs), reconcile the five sub-areas' proposed per-`BAR-*` stages into one coherent experience-area view, build
the whole coverage note (every release-gating `REQ-UX-*` → the `BAR-*`(s) covering it), mint any cross-cutting
`BAR-295..299` the assembled UX view needs that no single sub-area already covers, author the fold record, and
fold `SUBTASK_bar_ux`.

### Context
The verification gate and fold of the `SUBTASK_bar_ux` subtree (see `../_GLOBAL.md` and the frozen seams
`../contracts/`, `../../contracts/`, `../../../contracts/`). You read the five sibling sub-fragments once they
are COMPLETED and consolidate them; you do not re-author their `BAR-*`. You own only the assembled `bar-ux.md`,
the cross-cutting `BAR-295..299` range (used sparingly), and the fold record.
**Dependents**: folds the parent `SUBTASK_bar_ux` (resumes it SUSPENDED → COMPLETED).

## The concern you own
Produce the one experience-area bar fragment the parent `SUBTASK_bar_synthesis` consumes, and prove it is
complete and coherent. Assemble; do not re-decide the sub-areas' criteria except to resolve genuine conflicts
and to set one stage per `BAR-*`. Assert each identity as a check with its evidence recorded; a failing identity
is reported and remediated (request an amendment / re-run the owning spoke), never silently plugged.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, identities, methodology posture, ownership |
| This subtree contract | `../contracts/` (read-only) | The sub-partition, the per-area gating sets, the sub-identities, the fragment/coverage-note layout |
| Parent BAR partition | `../../contracts/` (read-only) | The `SUBTASK_release_bar` partition + fragment/coverage-note + proposed_stage convention |
| DAG-root schema | `../../../contracts/` (read-only) | `BAR-<NNN>` scheme, closed `verification_methods` vocab, stages |
| IA sub-fragment | `../SUBTASK_bar_ux_ia/outputs/bar-ux-ia.md` | `BAR-200..214` |
| Visual sub-fragment | `../SUBTASK_bar_ux_visual/outputs/bar-ux-visual.md` | `BAR-215..229` |
| Screens sub-fragment | `../SUBTASK_bar_ux_screens/outputs/bar-ux-screens.md` | `BAR-230..264` |
| Responsive sub-fragment | `../SUBTASK_bar_ux_responsive/outputs/bar-ux-responsive.md` | `BAR-265..274` |
| Accessibility sub-fragment | `../SUBTASK_bar_ux_a11y/outputs/bar-ux-a11y.md` | `BAR-275..294` |
| Experience design | `../../../SUBTASK_experience_design/outputs/experience-design.md` | The authoritative gating set (the 106 release-gating `REQ-UX-*`) to assert coverage against |

## Output
- `SUBTASK_bar_ux/outputs/bar-ux.md` — the assembled experience-area fragment: the consolidated `BAR-200..299`
  register (one block per `BAR-*` with the inherited field set, one stage each) followed by the coverage note
  mapping every release-gating `REQ-UX-*` to the `BAR-*`(s) that cover it. Repository-ready (no host/system/
  taskflow detail, no attribution trailers).
- `SUBTASK_bar_ux/SYNTHESIS.md` — the fold record at the fold location (the SUSPENDED `SUBTASK_bar_ux`
  workspace): each subtree identity asserted with its evidence, any cross-cutting `BAR-295..299` minted with the
  finding that motivated it, and the methodology-posture note. Taskflow-internal.

Then fold `SUBTASK_bar_ux` (resume it with this `SYNTHESIS.md` as the seam).

## Success criteria
- [ ] `bar-ux.md` contains every `BAR-*` from the five sub-fragments, ids distinct, each within its owner's sub-range (UX_BAR_RANGE_RESPECTED, UX_NO_BAR_COLLISION).
- [ ] Every release-gating `REQ-UX-*` (the 106) is referenced by ≥1 `BAR-*`; the coverage note records the mapping (UX_GATING_REQ_COVERAGE, UX_COVERAGE_NOTE_PRESENT).
- [ ] Every `BAR-*` names a verification method from the frozen vocabulary, references ≥1 `REQ-*`, and carries exactly one stage ∈ {`usable_early`, `releasable`} (UX_BAR_TESTABLE, UX_BAR_STAGED).
- [ ] No `BAR-*` is justified solely by a non-gating `REQ-UX-*` (UX_NONGATING_EXCLUDED).
- [ ] `bar-ux.md` carries no host/system/taskflow detail and no attribution trailer (UX_HYGIENE).
- [ ] Any cross-cutting `BAR-295..299` is within range and records its motivating finding; the fold record asserts every identity with evidence and performs no silent plug.

## Constraints
- Assemble and verify; do not silently re-author or drop a sub-fragment's `BAR-*`. A conflict or a failed
  identity is reported and remediated through an amendment, not papered over.
- Stage reconciliation is the UX-area view; the parent `SUBTASK_bar_synthesis` owns the final whole-product
  MVP-vs-releasable line and may still move a `BAR-*`.
- Methodology bundles (relayed; loader unavailable, apply the product-design persona + this guidance): Release
  Definition (primary); Experience Design, Product Strategy (support).
- Evaluate your own scope against the decomposition triggers at dispatch; the atomic-vs-decompose decision is
  yours to make on your actual brief and inputs.
