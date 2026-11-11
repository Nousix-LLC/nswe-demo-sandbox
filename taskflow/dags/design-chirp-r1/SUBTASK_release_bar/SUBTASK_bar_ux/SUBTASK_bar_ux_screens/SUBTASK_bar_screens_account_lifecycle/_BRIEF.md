# Task: Release-bar criteria for onboarding, profile edit, settings & account lifecycle (BAR-248..255)

## Task Specification
**Slug**: SUBTASK_bar_screens_account_lifecycle
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Author the `BAR-*` release-bar criteria in `BAR-248..255` that enforce every **release-gating** `REQ-UX-*` in the
account-management & lifecycle chapter (`REQ-UX-065..077`, gating subset) — everything a signed-in person does to
set up, manage, and end their own account. This chapter spans several distinct account surfaces, named below as
distinct bodies of gating requirements.

### Context
Part of the `SUBTASK_bar_ux_screens` subtree (the screens & flows slice of the UX release bar). Read `../_GLOBAL.md`
for shared context and the frozen seams (`../contracts/`, `../../contracts/`, `../../../contracts/`,
`../../../../contracts/`). You own the account-lifecycle chapter: the `BAR-248..255` sub-range and the fragment
file below. Sibling spokes own the other chapters; `SUBTASK_bar_screens_synthesis` assembles all sub-fragments,
finalizes the within-screens staging, and asserts coverage. This is the broadest chapter of the screens slice
(11 gating requirements across the distinct account surfaces named below); evaluate your own scope honestly
against the decomposition triggers at dispatch and decompose if warranted — the atomic-vs-decompose decision is
yours to make on your actual brief and inputs. **Dependents**: `SUBTASK_bar_screens_synthesis`.

### The concern you own
Turn this chapter's gating requirements into checkable release conditions across its distinct account surfaces:

- **Onboarding** (`REQ-UX-065, 066`) — a brand-new account lands on onboarding that explains the empty timeline
  and always offers a way off it (the compose route is always present, even where discovery is absent), and never
  blanks or dead-ends across its loading and error states.
- **Edit profile** (`REQ-UX-067, 068`) — a person changes display name and bio and the saved values persist and
  show on their profile; the screen validates in place, reports a failed save at the form without discarding
  edited values, confirms success, and never shows a silent success/failure or a system code.
- **Settings hub** (`REQ-UX-069`) — a settings hub lists every account sub-section, each openable from the hub and
  by its own URL with a labelled way back; the delete-account row is destructive and opens a confirmation rather
  than deleting on selection.
- **Account & contact control** (`REQ-UX-070`) — a person views the verified contact with its status, changes it,
  and completes a control-you-own verification step for a new/unverified contact; an unverified contact is a
  caution, not an error, and is never treated as verified.
- **Sessions & server-side sign-out** (`REQ-UX-073, 074`) — a person sees active sessions with enough to
  recognise each and the current one marked, and ends another device's session through a confirmation; signing
  out ends the session server-side so it cannot be used and does not leak protected content via back.
- **Data export** (`REQ-UX-075`) — a person requests and obtains their chirps, profile, and follow list in a
  portable form, with the request, the preparing state, and the obtainable result each shown, and a failure
  explained with retry.
- **Account deletion** (`REQ-UX-076, 077`) — the delete confirmation names the consequence, states the
  retained/not-retained outcome and what happens to the handle, and points to export first — all before any
  deletion; deletion proceeds only on explicit confirmation, cancelling leaves everything intact, and on deletion
  the person is signed out with no back-leak.

One `BAR-*` may enforce several related `REQ-UX-*` (for example the two deletion requirements, or the two
onboarding requirements); the id budget is tight by design, so cluster related gating requirements. A `BAR-*` is
the checkable release condition, not a restatement of the `REQ-*`; reference what it enforces (and the
`REQ-PROD-*` a flow serves) and mint `BAR-*` only in your range.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, identities, methodology posture |
| This subtree contract | `../contracts/` (read-only) | Your `BAR-248..255` sub-range; the account-lifecycle gating set; the per-BAR field set; the sub-fragment layout; the proposed_stage convention |
| UX partition contract | `../../contracts/` (read-only) | The screens slice owns `BAR-230..264` |
| Release-bar partition | `../../../contracts/` (read-only) | UX owns `BAR-200..299` |
| DAG-root schema | `../../../../contracts/` (read-only) | `BAR-<NNN>` scheme, closed `verification_methods` vocab, stages |
| Experience design | `../../../../SUBTASK_experience_design/outputs/experience-design.md` | The authoritative `REQ-UX-065..077` set and the per-REQ `release_gating` flag |

Your chapter's release-gating set (read the `release_gating` field in the design for the authoritative list):
`REQ-UX-065, 066, 067, 068, 069, 070, 073, 074, 075, 076, 077` (11 gating). Non-gating in this band:
`REQ-UX-071` (handle-change position), `REQ-UX-072` (notification preferences) — not covered.

### Output
- `SUBTASK_bar_screens_account_lifecycle/outputs/bar-screens-account-lifecycle.md` — one block per `BAR-*`
  carrying the fields fixed in `../contracts/bar_screens_partition.yaml` (`id`, `statement`, `references` ≥1
  `REQ-UX-*`, `verification_method`, `proposed_stage`), plus a coverage note listing every release-gating
  `REQ-UX-*` in your chapter and the `BAR-*` that covers it. Repository-ready content. If you decompose, this
  remains the single assembled output your sub-synthesis produces.

### Success criteria
- [ ] Composes against the inherited contracts; `BAR-*` only within `BAR-248..255`; no inherited schema redefined.
- [ ] Every release-gating `REQ-UX-*` in your chapter is referenced by ≥1 `BAR-*`.
- [ ] Every `BAR-*` names a verification method from the frozen vocabulary, references ≥1 `REQ-*`, and carries a `proposed_stage`.
- [ ] No `BAR-*` is justified solely by a non-gating `REQ-UX-*` (071, 072).
- [ ] The coverage note lets the synthesis gate assert account-lifecycle gating coverage without re-deriving the set.

### Constraints
- A bar, not an aspiration — each criterion checkable by someone who was not in the room. State release conditions
  as checkable facts in the user's terms, not implementations. (Deletion and sign-out conditions that must hold
  server-side — a session no longer usable, a no-back-leak — are good candidates for an `operational_check`.)
- Reference `REQ-*`; do not re-author requirements. No `BAR-*` justified solely by a non-gating `REQ-UX-*`.
- Methodology bundles (relayed; loader unavailable, apply the product-design persona + the hub guidance): Release
  Definition (primary); Experience Design, Product Strategy (support).
