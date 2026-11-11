# Task: Release-bar criteria for social interactions & profiles (BAR-243..247)

## Task Specification
**Slug**: SUBTASK_bar_screens_social_profiles
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Author the `BAR-*` release-bar criteria in `BAR-243..247` that enforce every **release-gating** `REQ-UX-*` in the
social-interactions & profiles chapter (`REQ-UX-058..063`). This chapter holds two related bodies of gating
requirements: the in-place social actions (reply, like, follow) and the profile & discovery-list surfaces they act
on.

### Context
Part of the `SUBTASK_bar_ux_screens` subtree (the screens & flows slice of the UX release bar). Read `../_GLOBAL.md`
for shared context and the frozen seams (`../contracts/`, `../../contracts/`, `../../../contracts/`,
`../../../../contracts/`). You own the social-&-profiles chapter: the `BAR-243..247` sub-range and the fragment
file below. Sibling spokes own the other chapters; `SUBTASK_bar_screens_synthesis` assembles all sub-fragments,
finalizes the within-screens staging, and asserts coverage. Evaluate your own scope against the decomposition
triggers at dispatch; the atomic-vs-decompose decision is yours to make on your actual brief and inputs.
**Dependents**: `SUBTASK_bar_screens_synthesis`.

### The concern you own
Turn this chapter's gating requirements into checkable release conditions across its two related bodies:

- **Social interactions** — a signed-in person writes and publishes a reply from the conversation's reply slot
  using the shared compose control (the reply records the chirp it answers and appears in the conversation; a
  reply to a gone chirp is reported not-found with the draft kept; a signed-out visitor sees a path to sign
  in/up in place of the reply control); the like control is an in-place idempotent toggle whose liked state is
  shown by more than colour, with an accurate count that reverts on failure; the follow control is an in-place
  idempotent control that cannot start a self-follow (own identity shows "Edit profile", not "Follow") and
  reverts on failure.
- **Profiles & discovery lists** — a public profile shows identity and chirps with or without a session; the
  owner's profile is their public face with an edit entry in place of the follow control; and followers/following
  are addressable, paginated lists with a follow control per row (signed in) and a way back to the profile.

One `BAR-*` may enforce several related `REQ-UX-*` (for example the public and owner profile views); the id budget
is tight, so cluster related gating requirements. A `BAR-*` is the checkable release condition, not a restatement
of the `REQ-*`; reference what it enforces (and the `REQ-PROD-*` a flow serves) and mint `BAR-*` only in your
range.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, identities, methodology posture |
| This subtree contract | `../contracts/` (read-only) | Your `BAR-243..247` sub-range; the social-&-profiles gating set; the per-BAR field set; the sub-fragment layout; the proposed_stage convention |
| UX partition contract | `../../contracts/` (read-only) | The screens slice owns `BAR-230..264` |
| Release-bar partition | `../../../contracts/` (read-only) | UX owns `BAR-200..299` |
| DAG-root schema | `../../../../contracts/` (read-only) | `BAR-<NNN>` scheme, closed `verification_methods` vocab, stages |
| Experience design | `../../../../SUBTASK_experience_design/outputs/experience-design.md` | The authoritative `REQ-UX-058..063` set and the per-REQ `release_gating` flag |

Your chapter's release-gating set (read the `release_gating` field in the design for the authoritative list):
`REQ-UX-058, 059, 060, 061, 062, 063` (6 gating). Non-gating in the adjacent band: `REQ-UX-064` (a way to find
people to follow / Explore) — not covered.

### Output
- `SUBTASK_bar_screens_social_profiles/outputs/bar-screens-social-profiles.md` — one block per `BAR-*` carrying
  the fields fixed in `../contracts/bar_screens_partition.yaml` (`id`, `statement`, `references` ≥1 `REQ-UX-*`,
  `verification_method`, `proposed_stage`), plus a coverage note listing every release-gating `REQ-UX-*` in
  058..063 and the `BAR-*` that covers it. Repository-ready content. If you decompose, this remains the single
  assembled output your sub-synthesis produces.

### Success criteria
- [ ] Composes against the inherited contracts; `BAR-*` only within `BAR-243..247`; no inherited schema redefined.
- [ ] Every release-gating `REQ-UX-058..063` is referenced by ≥1 `BAR-*`.
- [ ] Every `BAR-*` names a verification method from the frozen vocabulary, references ≥1 `REQ-*`, and carries a `proposed_stage`.
- [ ] No `BAR-*` is justified solely by the non-gating `REQ-UX-064`.
- [ ] The coverage note lets the synthesis gate assert social-&-profiles gating coverage without re-deriving the set.

### Constraints
- A bar, not an aspiration — each criterion checkable by someone who was not in the room. State release conditions
  as checkable facts in the user's terms, not implementations.
- Reference `REQ-*`; do not re-author requirements.
- Methodology bundles (relayed; loader unavailable, apply the product-design persona + the hub guidance): Release
  Definition (primary); Experience Design, Product Strategy (support).
