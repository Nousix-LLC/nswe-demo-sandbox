# Task: Release-bar criteria for safety/help/not-found & cross-screen state patterns (BAR-256..263)

## Task Specification
**Slug**: SUBTASK_bar_screens_safety_states
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Author the `BAR-*` release-bar criteria in `BAR-256..263` that enforce every **release-gating** `REQ-UX-*` in this
chapter (`REQ-UX-079, 082, 083, 084, 085, 086, 087, 088, 089`). It holds two related bodies of gating
requirements: the safety/help/rules/not-found surfaces, and the product-wide cross-screen state patterns (empty,
loading, failure, and session/transient recovery).

### Context
Part of the `SUBTASK_bar_ux_screens` subtree (the screens & flows slice of the UX release bar). Read `../_GLOBAL.md`
for shared context and the frozen seams (`../contracts/`, `../../contracts/`, `../../../contracts/`,
`../../../../contracts/`). You own the safety-&-states chapter: the `BAR-256..263` sub-range and the fragment file
below. Sibling spokes own the other chapters; `SUBTASK_bar_screens_synthesis` assembles all sub-fragments,
finalizes the within-screens staging, and asserts coverage. Evaluate your own scope against the decomposition
triggers at dispatch; the atomic-vs-decompose decision is yours to make on your actual brief and inputs.
**Dependents**: `SUBTASK_bar_screens_synthesis`.

### The concern you own
Turn this chapter's gating requirements into checkable release conditions across its two related bodies:

- **Safety, help, rules, not-found** (`REQ-UX-079, 082, 083, 084`) — a signed-in person can report a chirp or
  account against a stated rule and sees the report acknowledged as received (never silently swallowed, and
  submission is prevented with no reason chosen); a help & support entry is reachable from both the signed-out
  and signed-in shell and reaches recovery and operator contact; the product's rules are stated as named
  categories a report's reasons correspond to, reachable from both shells; and an unresolved or removed resource
  lands on a not-found screen that explains the absence without exposing private detail and routes back to a
  known place.
- **Cross-screen state patterns** (`REQ-UX-085, 086, 087, 088, 089`) — these are the product-wide empty/error/
  loading/recovery conventions every surface composes: each surface presents considered empty, error, and
  loading states (or states where one does not apply); empty surfaces are explained and never blank, and a
  genuinely-empty surface is visibly distinct from one that failed; loading shows the shape of what is coming
  (skeletons at real dimensions, the nav frame never blanks) and never runs forever (an unresolved load becomes
  an error with a way forward); failures appear where the action was taken, in plain words with no system code
  and a way forward; and an expired session routes to sign-in with the reason stated and returns the person with
  in-progress work (a drafted chirp) preserved, while a transient error is retryable in place without losing work.

Because the cross-screen patterns are product-wide, a `BAR-*` here may reference `REQ-UX-*` from other chapters
as the surfaces on which the pattern is checked; it is owned here because the pattern requirement (`085..089`) is
most centrally held in this chapter. One `BAR-*` may enforce several related `REQ-UX-*`; the id budget is tight,
so cluster related gating requirements (the state patterns cluster naturally). A `BAR-*` is the checkable release
condition, not a restatement of the `REQ-*`; reference what it enforces (and the `REQ-PROD-*` it serves) and mint
`BAR-*` only in your range.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, identities, methodology posture |
| This subtree contract | `../contracts/` (read-only) | Your `BAR-256..263` sub-range; the safety-&-states gating set; the per-BAR field set; the sub-fragment layout; the proposed_stage convention |
| UX partition contract | `../../contracts/` (read-only) | The screens slice owns `BAR-230..264` |
| Release-bar partition | `../../../contracts/` (read-only) | UX owns `BAR-200..299` |
| DAG-root schema | `../../../../contracts/` (read-only) | `BAR-<NNN>` scheme, closed `verification_methods` vocab, stages |
| Experience design | `../../../../SUBTASK_experience_design/outputs/experience-design.md` | The authoritative `REQ-UX-079, 082..089` set and the per-REQ `release_gating` flag |

Your chapter's release-gating set (read the `release_gating` field in the design for the authoritative list):
`REQ-UX-079, 082, 083, 084, 085, 086, 087, 088, 089` (9 gating). Non-gating in this band: `REQ-UX-078`
(notifications surface), `REQ-UX-080` (block/mute), `REQ-UX-081` (managing blocked/muted) — not covered.

### Output
- `SUBTASK_bar_screens_safety_states/outputs/bar-screens-safety-states.md` — one block per `BAR-*` carrying the
  fields fixed in `../contracts/bar_screens_partition.yaml` (`id`, `statement`, `references` ≥1 `REQ-UX-*`,
  `verification_method`, `proposed_stage`), plus a coverage note listing every release-gating `REQ-UX-*` in your
  chapter and the `BAR-*` that covers it. Repository-ready content. If you decompose, this remains the single
  assembled output your sub-synthesis produces.

### Success criteria
- [ ] Composes against the inherited contracts; `BAR-*` only within `BAR-256..263`; no inherited schema redefined.
- [ ] Every release-gating `REQ-UX-079, 082..089` is referenced by ≥1 `BAR-*`.
- [ ] Every `BAR-*` names a verification method from the frozen vocabulary, references ≥1 `REQ-*`, and carries a `proposed_stage`.
- [ ] No `BAR-*` is justified solely by a non-gating `REQ-UX-*` (078, 080, 081).
- [ ] The coverage note lets the synthesis gate assert safety-&-states gating coverage without re-deriving the set.

### Constraints
- A bar, not an aspiration — each criterion checkable by someone who was not in the room. State release conditions
  as checkable facts in the user's terms, not implementations. The state-pattern criteria name the concrete check
  (reach the empty/error/loading state on a named surface and observe the designed treatment), never "robust states".
- Reference `REQ-*`; do not re-author requirements. No `BAR-*` justified solely by a non-gating `REQ-UX-*`.
- Methodology bundles (relayed; loader unavailable, apply the product-design persona + the hub guidance): Release
  Definition (primary); Experience Design, Product Strategy (support).
