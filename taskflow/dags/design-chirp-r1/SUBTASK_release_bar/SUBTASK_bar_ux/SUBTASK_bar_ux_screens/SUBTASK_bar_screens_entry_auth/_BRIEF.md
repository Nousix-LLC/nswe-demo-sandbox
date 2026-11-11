# Task: Release-bar criteria for the entry & auth chapter (BAR-230..237)

## Task Specification
**Slug**: SUBTASK_bar_screens_entry_auth
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Author the `BAR-*` release-bar criteria in `BAR-230..237` that enforce every **release-gating** `REQ-UX-*` in the
entry & auth chapter (`REQ-UX-040..050`) — the surfaces a person meets before and during getting into the product.

### Context
Part of the `SUBTASK_bar_ux_screens` subtree (the screens & flows slice of the UX release bar). Read `../_GLOBAL.md`
for shared context and the frozen seams (`../contracts/`, `../../contracts/`, `../../../contracts/`,
`../../../../contracts/`). You own the entry-&-auth chapter: the `BAR-230..237` sub-range and the fragment file
below. Sibling spokes own the other chapters; `SUBTASK_bar_screens_synthesis` assembles all sub-fragments,
finalizes the within-screens staging, and asserts coverage. Evaluate your own scope against the decomposition
triggers at dispatch; the atomic-vs-decompose decision is yours to make on your actual brief and inputs.
**Dependents**: `SUBTASK_bar_screens_synthesis`.

### The concern you own
Turn the entry & auth gating requirements into checkable release conditions proving that a stranger with no session
can understand what chirp is and reach both sign-up and sign-in; that sign-up creates an account from only what it
needs, reports handle format/uniqueness against the field, and captures a contact marked to-be-verified; that
sign-in proves the account is the person's own and distinguishes no-such-account from wrong-credential without
leaking account existence; that a person can self-start recovery through the verified contact (neutral, no-leak
acknowledgement) and set a new credential; that sign-out is confirmed, ends the session, and offers all-devices;
that each of these screens renders a designed empty/error/loading state; and that completing sign-up lands on
onboarding, a routed sign-in returns to the asked-for screen, and sign-out does not leak protected content via
back. One `BAR-*` may enforce several related `REQ-UX-*`; the id budget is tight by design, so cluster related
gating requirements into one condition. A `BAR-*` is the checkable release condition, not a restatement of the
`REQ-*`; reference what it enforces (and the `REQ-PROD-*` a flow serves) and mint `BAR-*` only in your range.

Note on `REQ-UX-050`: its gating basis is the sign-up→onboarding landing and the sign-out no-leak
(`REQ-PROD-032`, `REQ-PROD-014`); its three-way interlinks ride the non-gating `REQ-UX-015` and are not the
gating basis.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, identities, methodology posture |
| This subtree contract | `../contracts/` (read-only) | Your `BAR-230..237` sub-range; the entry-auth gating set; the per-BAR field set; the sub-fragment layout; the proposed_stage convention |
| UX partition contract | `../../contracts/` (read-only) | The screens slice owns `BAR-230..264` |
| Release-bar partition | `../../../contracts/` (read-only) | UX owns `BAR-200..299` |
| DAG-root schema | `../../../../contracts/` (read-only) | `BAR-<NNN>` scheme, closed `verification_methods` vocab, stages |
| Experience design | `../../../../SUBTASK_experience_design/outputs/experience-design.md` | The authoritative `REQ-UX-040..050` set and the per-REQ `release_gating` flag |

Your chapter's release-gating set (read the `release_gating` field in the design for the authoritative list):
`REQ-UX-040, 041, 042, 043, 044, 045, 046, 047, 048, 049, 050` (11 gating). No non-gating `REQ-UX-*` fall in
040..050.

### Output
- `SUBTASK_bar_screens_entry_auth/outputs/bar-screens-entry-auth.md` — one block per `BAR-*` carrying the fields
  fixed in `../contracts/bar_screens_partition.yaml` (`id`, `statement`, `references` ≥1 `REQ-UX-*`,
  `verification_method`, `proposed_stage`), plus a coverage note listing every release-gating `REQ-UX-*` in
  040..050 and the `BAR-*` that covers it. Repository-ready content (no host/system/taskflow detail, no
  attribution trailers). If you decompose, this remains the single assembled output your sub-synthesis produces.

### Success criteria
- [ ] Composes against the inherited contracts; `BAR-*` only within `BAR-230..237`; no inherited schema redefined.
- [ ] Every release-gating `REQ-UX-040..050` is referenced by ≥1 `BAR-*`.
- [ ] Every `BAR-*` names a verification method from the frozen vocabulary, references ≥1 `REQ-*`, and carries a `proposed_stage`.
- [ ] The coverage note lets the synthesis gate assert entry-auth gating coverage without re-deriving the set.

### Constraints
- A bar, not an aspiration — each criterion checkable by someone who was not in the room. State release conditions
  as checkable facts in the user's terms, not implementations.
- Reference `REQ-*`; do not re-author requirements. No `BAR-*` justified solely by a non-gating `REQ-UX-*`.
- Methodology bundles (relayed; loader unavailable, apply the product-design persona + the hub guidance): Release
  Definition (primary); Experience Design, Product Strategy (support).
