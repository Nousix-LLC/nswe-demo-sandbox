# COMPLETE — SUBTASK_versioning_compat

**Task:** Ferric 1.0 versioning & compatibility policy (`REQ-REL-040..059`).
**Status:** completed · **Evaluation:** Atomic.

## What was produced

`versioning-compat.md` — the 1.0 versioning & compatibility policy and the `REQ-REL-040..047` register
(range `REQ-REL-040..059`; `048..059` left unused and available). Eight requirements, each with statement,
rationale (named peer/standard evidence), acceptance criteria using the parent `verification_method`
vocabulary, `stage`, `release_gating`, and read-only references:

- `REQ-REL-040` — 1.0 states a supported MSRV (grounded in the workspace's `rust-version = 1.82`).
- `REQ-REL-041` — how the MSRV may rise within 1.x (minor-only, announced).
- `REQ-REL-042` — the frozen `prelude` surfaces stay usable across 1.x (policy side of REQ-FW-009).
- `REQ-REL-043` — additive-only evolution within 1.x; breaking changes deferred to 2.0.
- `REQ-REL-044` — lockstep cross-crate versioning (`version.workspace = true` kept; release together).
- `REQ-REL-045` — cross-crate compatibility an app author can rely on (ferric-router/ferric-http 1.x work with ferric 1.x).
- `REQ-REL-046` — the compatibility policy is written down and discoverable.
- `REQ-REL-047` — what the 1.x promise does not cover, stated (non-prelude items, unimplemented `todo!()` behaviour, future unstable-flagged APIs).

## How it composes with the parent

Feeds `SUBTASK_rel_synthesis`, which merges this partial with `publishing.md` (`REQ-REL-001..019`) and
`semver-changelog.md` (`REQ-REL-020..039`) into one `release-and-distribution.md` register.

- **J1 (disjoint ranges):** only `REQ-REL-040..047` minted, inside the assigned `040..059` range.
- **J2/J3 (schema + verification):** every requirement carries the parent `requirement_fields`; acceptance
  methods drawn only from {`doc_inspection`, `automated_test`, `example_build`, `publishability`}.
- **J4/J5 (coverage + 1.0 promise):** versioning/compatibility policy covered; MSRV promise (`040`) and
  frozen-`prelude` stability promise (`042`) both present.
- **J6 (peers/standards named):** Leptos, Dioxus, Yew (and Tokio as the independent-versioning counter-example);
  Cargo Book *SemVer Compatibility*, RFC 2495 (`rust-version`), RFC 3537 (MSRV-aware resolver), API Guidelines
  MSRV discussion #231.

## Boundary respected

Owns the compatibility *promise* only. The semver *mechanics* (version-bump signalling, breaking-vs-additive
classification, changelog) are referenced read-only to `REQ-REL-020..039`; publishing mechanics (metadata,
path→version, release order) are referenced read-only to `REQ-REL-001..019`. Sibling outputs were not read
(peers run concurrently and were not COMPLETED); the boundary was taken from the subtree hub and the sibling
briefs.

## Notes / assumptions

- Methodology domain was unset on this reconstructed node (`engine_load_methodology` returned
  `agent_domain_unset`); the versioning/compatibility methodology was therefore unavailable and skipped per the
  brief ("load … if available"). The policy rests on named standards and peer precedent instead.
- Peer MSRV figures are read from published crate metadata as a recency pattern, flagged in the doc as not a
  precise contemporaneous claim.

## Output
- `versioning-compat.md`
