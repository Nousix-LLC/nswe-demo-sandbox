# Task: Release-bar criteria for the identity, security & trust area (BAR-300..399)

## Task Specification
**Slug**: SUBTASK_bar_id
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Author the `BAR-*` release-bar criteria (in the range `BAR-300..399`) that enforce every **release-gating**
`REQ-ID-*` from the identity & security design — the account lifecycle (sign-up/in/recovery, deletion, data
export), real authentication and safe sessions, authorization (what each user may see/change), and the
abuse/privacy basics — so each release-gating identity/trust requirement is held to a concrete, testable release
condition.

### Context
Part of the `SUBTASK_release_bar` subtree (see `../_GLOBAL.md` and the frozen seam `../contracts/`). You own the
identity-area slice of the release bar: the `BAR-300..399` range and the fragment file below. Sibling spokes own
the other areas; `SUBTASK_bar_synthesis` assembles all fragments, finalizes cross-cutting staging, and runs the
whole-design gap review — you propose a stage per `BAR-*` from the identity/trust view and cover your area's
gating set.
**Dependents**: `SUBTASK_bar_synthesis`.

## The concern you own
Turn the identity/trust area's release-gating requirements into bar criteria that prove a stranger's account and
data are safe on the live product — they can get in, only see and change what they may, recover access, delete
the account, and take their data out. A `BAR-*` is the checkable release condition, not a restatement of the
`REQ-*`; one `BAR-*` may enforce several related `REQ-ID-*`. Reference what it enforces; mint `BAR-*` only in
your range.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, identities, methodology posture |
| Inherited contract | `../../contracts/` (read-only) | `BAR-<NNN>` scheme, closed `verification_methods` vocab, stages |
| Subtree sub-contract | `../contracts/` (read-only) | Your `BAR-300..399` range; the bar-fragment field set; the proposed_stage convention |
| Identity & security design | `../../SUBTASK_identity_trust/outputs/identity-security.md` | The authoritative `REQ-ID-*` set and which are release-gating (per-REQ `release_gating` field) |

## Output
- `SUBTASK_bar_id/outputs/bar-id.md` — one block per `BAR-*` carrying the fields fixed in
  `../contracts/bar_partition.yaml` (`id`, `statement`, `references` ≥1 `REQ-ID-*`, `verification_method`,
  `proposed_stage`), plus the coverage note listing every release-gating `REQ-ID-*` and the `BAR-*` that covers
  it. Repository-ready content (no host/system/taskflow detail, no attribution trailers).

## Success criteria
- [ ] Composes against `../contracts/` and `../../contracts/`; `BAR-*` only within `BAR-300..399`; schema not redefined.
- [ ] Every release-gating `REQ-ID-*` in the identity design is referenced by ≥1 `BAR-*`.
- [ ] Every `BAR-*` names a verification method from the frozen vocabulary, references ≥1 `REQ-*`, and carries a `proposed_stage`.
- [ ] The coverage note lets the synthesis gate assert gating coverage without re-deriving the gating set.

## Constraints
- A bar, not an aspiration — each criterion checkable by someone who was not in the room (e.g. "a deleted account's
  data is gone, verified by …", not "data is handled securely").
- Reference `REQ-*`; do not re-author requirements, and do not specify implementation ("how" — protocols, libraries).
- Methodology bundles (relayed; loader unavailable, apply the product-design persona + this guidance): Release
  Definition (primary); Identity and Trust, Product Strategy (support).
