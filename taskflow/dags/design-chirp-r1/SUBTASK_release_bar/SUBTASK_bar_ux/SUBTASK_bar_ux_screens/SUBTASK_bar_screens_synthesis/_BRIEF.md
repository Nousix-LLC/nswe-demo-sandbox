# Task: Assemble, verify, and fold the screens release-bar fragment (synthesis gate)

## Task Specification
**Slug**: SUBTASK_bar_screens_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_bar_screens_entry_auth, SUBTASK_bar_screens_core_loop, SUBTASK_bar_screens_social_profiles, SUBTASK_bar_screens_account_lifecycle, SUBTASK_bar_screens_safety_states
**Status**: Pending

### Objective
Assemble the five chapter sub-fragments into the single screens release-bar fragment
`SUBTASK_bar_ux_screens/outputs/bar-ux-screens.md`, finalize the within-screens per-`BAR-*` staging into one
coherent set, assert the subtree's identities with recorded evidence, mint the cross-cutting `BAR-264` only if the
assembled view needs a condition no single chapter owns, build the whole-slice coverage note, author `SYNTHESIS.md`,
and fold `SUBTASK_bar_ux_screens` (resume the suspended parent with the assembled fragment as its declared output).

### Context
This is the synthesis/verification gate of the `SUBTASK_bar_ux_screens` subtree. Read `../_GLOBAL.md` for shared
context and the frozen seams (`../contracts/`, `../../contracts/`, `../../../contracts/`, `../../../../contracts/`).
It runs after all five chapter spokes are COMPLETED and reads their outputs. The verification is mechanical: assert
the contract's identities against the combined outputs with recorded evidence; a failing identity is reported and
remediated (request an amendment), never silently plugged. **Dependents**: this fold resumes `SUBTASK_bar_ux_screens`,
whose output `outputs/bar-ux-screens.md` is then consumed by the parent `SUBTASK_bar_ux_synthesis`.

### The concern you own
Assemble the five chapter sub-fragments into one consolidated `BAR-230..264` register and reconcile them into one
coherent whole:
- Assemble every `BAR-*` block from the five sub-fragments into one register, in id order, each carrying the
  inherited field set (`id`, `statement`, `references`, `verification_method`, `stage`).
- Finalize the within-screens staging: reconcile the spokes' `proposed_stage` values into one coherent
  `usable_early` vs `releasable` line for the screens slice (one stage per `BAR-*`, no criterion staged two ways).
  Record this as the screens-view proposal; the parent `SUBTASK_bar_ux_synthesis` and the whole-bar synthesis own
  the wider cross-area line and may still move a `BAR-*`.
- Build the whole-slice coverage note mapping every release-gating `REQ-UX-*` in 040..089 (the 43 with
  `release_gating: true`) to the `BAR-*`(s) covering it, so the parent UX synthesis gate asserts screens-area
  gating coverage without re-deriving the set.
- Mint the cross-cutting `BAR-264` ONLY if the assembled view needs a release condition that no single chapter's
  gating requirements already cover; record the finding that motivated it. If none is needed, `BAR-264` is unused.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, identities to assert, ownership, methodology posture |
| This subtree contract | `../contracts/` (read-only) | The `BAR-230..264` sub-partition, per-chapter gating sets, the identities, the fragment + coverage-note layout |
| UX / release-bar / DAG-root contracts | `../../contracts/`, `../../../contracts/`, `../../../../contracts/` (read-only) | Inherited scheme, vocab, stages, and the parent fragment target |
| Entry-auth sub-fragment | `../SUBTASK_bar_screens_entry_auth/outputs/bar-screens-entry-auth.md` | `BAR-230..237` + its coverage note |
| Core-loop sub-fragment | `../SUBTASK_bar_screens_core_loop/outputs/bar-screens-core-loop.md` | `BAR-238..242` + its coverage note |
| Social-&-profiles sub-fragment | `../SUBTASK_bar_screens_social_profiles/outputs/bar-screens-social-profiles.md` | `BAR-243..247` + its coverage note |
| Account-lifecycle sub-fragment | `../SUBTASK_bar_screens_account_lifecycle/outputs/bar-screens-account-lifecycle.md` | `BAR-248..255` + its coverage note |
| Safety-&-states sub-fragment | `../SUBTASK_bar_screens_safety_states/outputs/bar-screens-safety-states.md` | `BAR-256..263` + its coverage note |
| Experience design | `../../../../SUBTASK_experience_design/outputs/experience-design.md` | The authoritative gating set to check coverage against |

### Output
- `SUBTASK_bar_ux_screens/outputs/bar-ux-screens.md` — the single assembled screens bar fragment: the consolidated
  `BAR-230..264` register (one block per `BAR-*`, inherited field set, one finalized stage each) + the whole-slice
  coverage note (every release-gating `REQ-UX-*` in 040..089 → the `BAR-*` covering it). Repository-ready: no
  host/system/taskflow detail, no attribution trailer.
- `SUBTASK_bar_ux_screens/SYNTHESIS.md` — the fold record: the identities asserted with recorded evidence (no
  silent plugs), any cross-cutting `BAR-264` finding, and the methodology-posture note. Taskflow-internal.

### Success criteria (identities asserted with recorded evidence)
- [ ] **SCREENS_BAR_RANGE_RESPECTED** — every `BAR-NNN` within its owning spoke's sub-range; all within `BAR-230..264`.
- [ ] **SCREENS_NO_BAR_COLLISION** — all `BAR-NNN` ids across the five sub-fragments + the cross-cutting bar are distinct.
- [ ] **SCREENS_GATING_REQ_COVERAGE** — every release-gating `REQ-UX-*` in 040..089 (43) referenced by ≥1 `BAR-*`.
- [ ] **SCREENS_BAR_TESTABLE** — every `BAR-*` names a `verification_method` from the frozen vocabulary and references ≥1 `REQ-*`.
- [ ] **SCREENS_BAR_STAGED** — every `BAR-*` carries exactly one stage ∈ {`usable_early`, `releasable`}.
- [ ] **SCREENS_NONGATING_EXCLUDED** — no `BAR-*` justified solely by a non-gating `REQ-UX-*` (057, 064, 071, 072, 078, 080, 081).
- [ ] **SCREENS_COVERAGE_NOTE_PRESENT** — `bar-ux-screens.md` carries the whole-slice coverage note.
- [ ] **SCREENS_HYGIENE** — `bar-ux-screens.md` carries no host/system/taskflow detail and no attribution trailer.

### Constraints
- Do not re-author `BAR-*` content the spokes own; assemble and reconcile. You MAY mint `BAR-264` only for a
  cross-cutting finding no chapter owns, and MAY adjust staging for within-screens coherence (recording the move).
- A failing identity is reported (and an amendment requested), never silently plugged.
- Reference `REQ-*`; do not re-author requirements.
- Methodology bundles (relayed; loader unavailable, apply the product-design persona + the hub guidance): Release
  Definition (primary); Experience Design, Product Strategy (support).
