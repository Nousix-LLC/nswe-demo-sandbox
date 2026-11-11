# Task: Release-bar criteria for the screens & flows area (BAR-230..264)

## Task Specification
**Slug**: SUBTASK_bar_ux_screens
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Author the `BAR-*` release-bar criteria in the range `BAR-230..264` that enforce every **release-gating**
`REQ-UX-*` in the screens & flows area (`REQ-UX-040..089`). This band spans several distinct screen groups, each
its own body of gating requirements:
- **Entry & auth** (`REQ-UX-040..050`): Landing, sign-up (fields, handle format/uniqueness, contact to be
  verified), sign-in (credential proof, no-such-account vs wrong-credential), recover access, set new
  credential, sign-out confirmation, each screen's empty/error/loading states, and the land-right / no-leak /
  interlink behaviours.
- **Home timeline & compose core loop** (`REQ-UX-051..056`): the own+followed newest-first bounded timeline,
  the catch-up affordance, timeline empty/error/loading states, the 280-char limit enforced while composing,
  publish lock/confirm/keep-draft, and the one compose surface in three placements.
- **Conversation, like, follow** (`REQ-UX-058..060`): reply from the conversation (and reply-to-gone reported),
  the in-place idempotent like toggle with accurate count, the in-place idempotent follow control that cannot
  self-follow.
- **Profiles & discovery lists** (`REQ-UX-061..063`): the public profile, the owner's profile with edit entry,
  the addressable paginated followers/following lists.
- **Onboarding & profile edit** (`REQ-UX-065..068`): onboarding that explains the empty timeline and never
  blanks/dead-ends, edit-profile persistence and in-place validation.
- **Settings & account lifecycle** (`REQ-UX-069, 070, 073, 074, 075, 076, 077`): the settings hub, account &
  contact control/verification, sessions & devices, server-side sign-out no-leak, data export, and the
  delete-account confirmation/consequence/retention/export-pointer and explicit-confirmation flow.
- **Safety, help, rules, not-found** (`REQ-UX-079, 082, 083, 084`): report acknowledged as received, help &
  support from both shells, stated rules a report points to, the not-found screen.
- **Cross-screen state patterns** (`REQ-UX-085, 086, 087, 088, 089`): the per-surface considered states, empty
  explained not blank, loading that shows shape and never runs forever, failures at the point of action, and
  expired-session / transient-error recovery without losing work.
Each release-gating requirement in this band must be held to a concrete, testable release condition.

### Context
Part of the `SUBTASK_bar_ux` subtree (see `../_GLOBAL.md` and the frozen seams `../contracts/`, `../../contracts/`,
`../../../contracts/`). You own the screens-&-flows slice: the `BAR-230..264` sub-range and the fragment file
below. This is the largest UX sub-area (43 gating requirements across the distinct screen groups named above);
evaluate your own scope honestly against the decomposition triggers at dispatch and decompose if warranted — the
atomic-vs-decompose decision is yours to make on your actual brief and inputs. Sibling spokes own the other
experience areas; `SUBTASK_bar_ux_synthesis` assembles all sub-fragments, finalizes the within-UX staging, and
asserts coverage — you propose a stage per `BAR-*` from the screens view and cover your area's gating set.
**Dependents**: `SUBTASK_bar_ux_synthesis`.

## The concern you own
Turn the screens & flows area's release-gating requirements into bar criteria that prove a stranger can get into
the product, complete the core posting/timeline/reply/like/follow loop, reach and use their profile and
settings, manage their account's contact, sessions, export and deletion, get help and report, and meet a
not-found or failure without a dead end — all on the live product, with the designed empty/error/loading and
session-recovery states rendering. A `BAR-*` is the checkable release condition, not a restatement of the
`REQ-*`; one `BAR-*` may enforce several related `REQ-UX-*` (and may reference the `REQ-PROD-*` a flow serves).
Reference what it enforces; mint `BAR-*` only in your range.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, identities, methodology posture |
| This subtree contract | `../contracts/` (read-only) | Your `BAR-230..264` sub-range; the per-area gating set; the bar-fragment field set; the proposed_stage convention |
| Parent BAR partition | `../../contracts/` (read-only) | The `SUBTASK_release_bar` partition (this subtree owns `BAR-200..299`) |
| DAG-root schema | `../../../contracts/` (read-only) | `BAR-<NNN>` scheme, closed `verification_methods` vocab, stages |
| Experience design | `../../../SUBTASK_experience_design/outputs/experience-design.md` | The authoritative `REQ-UX-040..089` set and the per-REQ `release_gating` flag |

Your area's release-gating set (read the `release_gating` field in the design for the authoritative list):
`REQ-UX-040..056, 058..063, 065..070, 073..077, 079, 082..089` (43 gating). Non-gating in this band:
`REQ-UX-057, 064, 071, 072, 078, 080, 081` — not covered.

## Output
- `SUBTASK_bar_ux_screens/outputs/bar-ux-screens.md` — one block per `BAR-*` carrying the fields fixed in
  `../contracts/bar_ux_partition.yaml` (`id`, `statement`, `references` ≥1 `REQ-UX-*`, `verification_method`,
  `proposed_stage`), plus a coverage note listing every release-gating `REQ-UX-*` in your band and the `BAR-*`
  that covers it. Repository-ready content (no host/system/taskflow detail, no attribution trailers).
  If you decompose, this remains the single assembled output your sub-synthesis produces.

## Success criteria
- [ ] Composes against `../contracts/`, `../../contracts/`, `../../../contracts/`; `BAR-*` only within `BAR-230..264`; no inherited schema redefined.
- [ ] Every release-gating `REQ-UX-*` in your band is referenced by ≥1 `BAR-*`.
- [ ] Every `BAR-*` names a verification method from the frozen vocabulary, references ≥1 `REQ-*`, and carries a `proposed_stage`.
- [ ] No `BAR-*` is justified solely by a non-gating `REQ-UX-*` (057, 064, 071, 072, 078, 080, 081).
- [ ] The coverage note lets the synthesis gate assert screens-area gating coverage without re-deriving the gating set.

## Constraints
- A bar, not an aspiration — each criterion checkable by someone who was not in the room. State release
  conditions as checkable facts, not implementations.
- Reference `REQ-*`; do not re-author requirements.
- Methodology bundles (relayed; loader unavailable, apply the product-design persona + this guidance): Release
  Definition (primary); Experience Design, Product Strategy (support).
