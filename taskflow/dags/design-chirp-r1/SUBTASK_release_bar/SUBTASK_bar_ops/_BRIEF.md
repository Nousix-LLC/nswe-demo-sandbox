# Task: Release-bar criteria for the operational-readiness area (BAR-400..499)

## Task Specification
**Slug**: SUBTASK_bar_ops
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Author the `BAR-*` release-bar criteria (in the range `BAR-400..499`) that enforce every **release-gating**
`REQ-OPS-*` from the operational-readiness design — durable data, backups & recovery, limits & quotas,
observability, status & incident — so each release-gating operational requirement is held to a concrete,
testable release condition (the operational-readiness design already marks 59 of its 75 requirements
release-gating).

### Context
Part of the `SUBTASK_release_bar` subtree (see `../_GLOBAL.md` and the frozen seam `../contracts/`). You own the
operations-area slice of the release bar: the `BAR-400..499` range and the fragment file below. Sibling spokes
own the other areas; `SUBTASK_bar_synthesis` assembles all fragments, finalizes cross-cutting staging, and runs
the whole-design gap review — you propose a stage per `BAR-*` from the operations view and cover your area's
gating set.
**Dependents**: `SUBTASK_bar_synthesis`.

## The concern you own
Turn the operations area's release-gating requirements into bar criteria that prove what must be true in
production beyond "it runs" — data survives restart, a backup actually restores, limits are enforced, the
product is observable, and an incident has a path. Many of these are best proven by an `operational_check`
(observe a production property) rather than a user action. A `BAR-*` is the checkable release condition, not a
restatement of the `REQ-*`; one `BAR-*` may enforce several related `REQ-OPS-*`. Reference what it enforces;
mint `BAR-*` only in your range.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, identities, methodology posture |
| Inherited contract | `../../contracts/` (read-only) | `BAR-<NNN>` scheme, closed `verification_methods` vocab, stages |
| Subtree sub-contract | `../contracts/` (read-only) | Your `BAR-400..499` range; the bar-fragment field set; the proposed_stage convention |
| Operational-readiness design | `../../SUBTASK_operational_readiness/SUBTASK_ops_synthesis/outputs/operational-readiness.md` | The authoritative `REQ-OPS-*` set and which are release-gating (per-REQ `release_gating` field) |

## Output
- `SUBTASK_bar_ops/outputs/bar-ops.md` — one block per `BAR-*` carrying the fields fixed in
  `../contracts/bar_partition.yaml` (`id`, `statement`, `references` ≥1 `REQ-OPS-*`, `verification_method`,
  `proposed_stage`), plus the coverage note listing every release-gating `REQ-OPS-*` and the `BAR-*` that covers
  it. Repository-ready content (no host/system/taskflow detail, no attribution trailers).

## Success criteria
- [ ] Composes against `../contracts/` and `../../contracts/`; `BAR-*` only within `BAR-400..499`; schema not redefined.
- [ ] Every release-gating `REQ-OPS-*` in the operational-readiness design is referenced by ≥1 `BAR-*`.
- [ ] Every `BAR-*` names a verification method from the frozen vocabulary, references ≥1 `REQ-*`, and carries a `proposed_stage`.
- [ ] The coverage note lets the synthesis gate assert gating coverage without re-deriving the gating set.

## Constraints
- A bar, not an aspiration — each criterion checkable by someone who was not in the room (e.g. "a backup taken at
  T restores to a working product at T+1, verified by …", not "backups exist").
- Reference `REQ-*`; do not re-author requirements, and do not specify implementation ("how"). Describe production
  properties by product/repository identity only — no host or cluster addresses, no filesystem paths.
- Methodology bundles (relayed; loader unavailable, apply the product-design persona + this guidance): Release
  Definition (primary); Release Readiness, Product Strategy (support).
