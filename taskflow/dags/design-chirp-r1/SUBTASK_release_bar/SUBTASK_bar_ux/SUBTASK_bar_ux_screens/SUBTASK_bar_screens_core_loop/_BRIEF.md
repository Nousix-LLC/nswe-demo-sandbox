# Task: Release-bar criteria for the home timeline & compose core loop (BAR-238..242)

## Task Specification
**Slug**: SUBTASK_bar_screens_core_loop
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Author the `BAR-*` release-bar criteria in `BAR-238..242` that enforce every **release-gating** `REQ-UX-*` in the
home-timeline & compose core loop (`REQ-UX-051..056`) — the read-and-post loop that is the product's reason to
return.

### Context
Part of the `SUBTASK_bar_ux_screens` subtree (the screens & flows slice of the UX release bar). Read `../_GLOBAL.md`
for shared context and the frozen seams (`../contracts/`, `../../contracts/`, `../../../contracts/`,
`../../../../contracts/`). You own the core-loop chapter: the `BAR-238..242` sub-range and the fragment file below.
Sibling spokes own the other chapters; `SUBTASK_bar_screens_synthesis` assembles all sub-fragments, finalizes the
within-screens staging, and asserts coverage. Evaluate your own scope against the decomposition triggers at
dispatch; the atomic-vs-decompose decision is yours. **Dependents**: `SUBTASK_bar_screens_synthesis`.

### The concern you own
Turn the core-loop gating requirements into checkable release conditions proving that a signed-in person sees a
home timeline of their own and followed chirps, newest first, loaded in bounded pages (never one unbounded load)
with an explicit load-older control and Home marked current; that a catch-up affordance brings in chirps posted
since the last look as a bounded step and returning from a conversation keeps the reader's place; that the
timeline renders designed empty, error, and loading states (empty explains and points to Explore and composing; a
failed page shows a retry in place without discarding loaded chirps; first load shows skeletons at real card size,
the shell never blanks, nothing spins forever); that the 280-character limit is enforced while composing (live
count, warn near the limit, over-limit marked, the post action disabled while empty or over-limit, and an
empty/over-limit submit rejected by any path); that publishing locks against double-posting, confirms on success,
and keeps the draft on failure with an inline retry; and that the one ComposeBox surface appears in its three
placements (inline timeline, Compose dialog/`/compose`, reply slot) with a context-labelled action and an empty
state. One `BAR-*` may enforce several related `REQ-UX-*`; the id budget is tight, so cluster related gating
requirements. A `BAR-*` is the checkable release condition, not a restatement of the `REQ-*`; reference what it
enforces (and the `REQ-PROD-*` a flow serves) and mint `BAR-*` only in your range.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, identities, methodology posture |
| This subtree contract | `../contracts/` (read-only) | Your `BAR-238..242` sub-range; the core-loop gating set; the per-BAR field set; the sub-fragment layout; the proposed_stage convention |
| UX partition contract | `../../contracts/` (read-only) | The screens slice owns `BAR-230..264` |
| Release-bar partition | `../../../contracts/` (read-only) | UX owns `BAR-200..299` |
| DAG-root schema | `../../../../contracts/` (read-only) | `BAR-<NNN>` scheme, closed `verification_methods` vocab, stages |
| Experience design | `../../../../SUBTASK_experience_design/outputs/experience-design.md` | The authoritative `REQ-UX-051..056` set and the per-REQ `release_gating` flag |

Your chapter's release-gating set (read the `release_gating` field in the design for the authoritative list):
`REQ-UX-051, 052, 053, 054, 055, 056` (6 gating). Non-gating in the adjacent band: `REQ-UX-057` (conversation
read) — not covered.

### Output
- `SUBTASK_bar_screens_core_loop/outputs/bar-screens-core-loop.md` — one block per `BAR-*` carrying the fields
  fixed in `../contracts/bar_screens_partition.yaml` (`id`, `statement`, `references` ≥1 `REQ-UX-*`,
  `verification_method`, `proposed_stage`), plus a coverage note listing every release-gating `REQ-UX-*` in
  051..056 and the `BAR-*` that covers it. Repository-ready content. If you decompose, this remains the single
  assembled output your sub-synthesis produces.

### Success criteria
- [ ] Composes against the inherited contracts; `BAR-*` only within `BAR-238..242`; no inherited schema redefined.
- [ ] Every release-gating `REQ-UX-051..056` is referenced by ≥1 `BAR-*`.
- [ ] Every `BAR-*` names a verification method from the frozen vocabulary, references ≥1 `REQ-*`, and carries a `proposed_stage`.
- [ ] No `BAR-*` is justified solely by the non-gating `REQ-UX-057`.
- [ ] The coverage note lets the synthesis gate assert core-loop gating coverage without re-deriving the set.

### Constraints
- A bar, not an aspiration — each criterion checkable by someone who was not in the room. State release conditions
  as checkable facts in the user's terms, not implementations.
- Reference `REQ-*`; do not re-author requirements.
- Methodology bundles (relayed; loader unavailable, apply the product-design persona + the hub guidance): Release
  Definition (primary); Experience Design, Product Strategy (support).
