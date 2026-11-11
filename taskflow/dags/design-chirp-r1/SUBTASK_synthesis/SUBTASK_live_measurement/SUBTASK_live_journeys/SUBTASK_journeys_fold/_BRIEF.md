# Task: Synthesis — union the nine journey-cluster verdicts into the manual_user_check measurement and fold

## Task Specification
**Slug**: SUBTASK_journeys_fold
**Task Kind**: synthesis
**Depends on**: SUBTASK_getin_identity, SUBTASK_core_loop, SUBTASK_account_lifecycle, SUBTASK_resilience_states, SUBTASK_safety_trust_support, SUBTASK_visual_craft_nav, SUBTASK_responsive_phone, SUBTASK_accessibility, SUBTASK_web_delivery_api
**Status**: Pending

### Objective
Union the nine journey-cluster verdict tables into one `bar_id`-keyed verdict table over all 139 `manual_user_check`
`BAR-*`, assert the partition is disjoint and total and the vocabulary conforms, write this subtree's declared output
`../outputs/live-journeys-measurement.md`, and fold `SUBTASK_live_journeys` to COMPLETED.

### Context
This is the synthesis/verification gate for the `manual_user_check` measurement subtree (see `../_GLOBAL.md` and
`../contracts/_MANIFEST.yaml`). The nine cluster children are COMPLETED; read their outputs directly (do not poll, do
not re-verify completion, do not re-measure). The fold is mechanical: union and check, never re-judge a verdict and
never silently reconcile a gap.

**Dependencies**: all nine cluster measurement children. **Dependents**: the parent `SUBTASK_measurement_fold`
consumes `../outputs/live-journeys-measurement.md` as the `manual_user_check` partition.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene |
| Sub-contract | `../contracts/_MANIFEST.yaml` | The cluster partition + per-cluster `BAR-*` assignment, the verdict-row schema, ownership, the totality identities to assert |
| id/traceability schema | `../../../../contracts/id_and_traceability_schema.yaml` | `live_status` + `verification_method` vocab (authoritative) |
| Release bar | `../../../../SUBTASK_release_bar/outputs/release-bar.md` | The authoritative set of `manual_user_check` `BAR-*` (filter to confirm the union is exactly these 139) |
| getin_identity verdicts | `../SUBTASK_getin_identity/outputs/getin-identity-measurement.md` | Cluster partition (22) |
| core_loop verdicts | `../SUBTASK_core_loop/outputs/core-loop-measurement.md` | Cluster partition (24) |
| account_lifecycle verdicts | `../SUBTASK_account_lifecycle/outputs/account-lifecycle-measurement.md` | Cluster partition (20) |
| resilience_states verdicts | `../SUBTASK_resilience_states/outputs/resilience-states-measurement.md` | Cluster partition (12) |
| safety_trust_support verdicts | `../SUBTASK_safety_trust_support/outputs/safety-trust-support-measurement.md` | Cluster partition (8) |
| visual_craft_nav verdicts | `../SUBTASK_visual_craft_nav/outputs/visual-craft-nav-measurement.md` | Cluster partition (16) |
| responsive_phone verdicts | `../SUBTASK_responsive_phone/outputs/responsive-phone-measurement.md` | Cluster partition (9) |
| accessibility verdicts | `../SUBTASK_accessibility/outputs/accessibility-measurement.md` | Cluster partition (18) |
| web_delivery_api verdicts | `../SUBTASK_web_delivery_api/outputs/web-delivery-api-measurement.md` | Cluster partition (10) |

### Process (approach, not a runbook)
Union the nine cluster tables into one `bar_id`-keyed table conforming to the inherited `verdict_row_schema` (columns
`bar_id, live_status, observation`). Then assert the sub-contract identities:
- `CLUSTER_DISJOINT_TOTAL` — the nine partitions are pairwise disjoint and union to exactly the 139 `manual_user_check`
  `BAR-*` in the release bar, each under exactly the cluster the partition table assigns it. A mismatch (a missing
  `BAR-*`, a duplicate, a cluster count off its `expected_counts`) is a **reported gap**, named explicitly, never
  silently reconciled.
- `MANUAL_STATUS_TOTAL` — every `BAR-*` carries exactly one `live_status` and a non-empty observation.
- `VOCAB_CONFORMS` — every `live_status` is from the inherited vocab; every `bar_id` is verbatim.
- `OBSERVATION_GROUNDED`, `OUTPUT_HYGIENE` — carry each cluster's grounded observations through verbatim; confirm no
  host/system/taskflow detail leaked into any observation or the preamble.

### Output
- `../outputs/live-journeys-measurement.md` — the unioned `bar_id`-keyed verdict table over all 139
  `manual_user_check` `BAR-*` (this subtree's declared output), with a short preamble recording only *that* the live
  product was reached (or why not), by repository/commit identity, and a one-line note of the `design` loader
  limitation. Repository identity only — no host/system/taskflow detail.
- `../SYNTHESIS.md` (at the `SUBTASK_live_journeys/` root — the fold location) — the fold record: how the nine
  partitions were unioned, the identity-assertion results (pass, or the named gaps), and the per-cluster/total counts.

### Fold
Author `../SYNTHESIS.md` at the subtree root, report terminal `status="completed"` with `artifact_path` pointing at it
and `outputs` listing `../outputs/live-journeys-measurement.md`, and resolve `SUBTASK_live_journeys`
`SUSPENDED → COMPLETED` with `../SYNTHESIS.md` as the fold seam, per the kernel fold contract.

### Success criteria
- [ ] `../outputs/live-journeys-measurement.md` holds exactly one row per `manual_user_check` `BAR-*`, all 139, each
      once, each with one `live_status` from the vocab and a non-empty grounded observation.
- [ ] The partition is confirmed disjoint and total against the release bar and the sub-contract's `expected_counts`;
      any discrepancy is reported in `../SYNTHESIS.md`, not reconciled away.
- [ ] No host/system/taskflow detail anywhere in the output or the fold record; repository identity only.

### Constraints
- Mechanical union and verification only; do not re-judge or alter a cluster's verdicts, and do not re-measure the
  product.
- Read-only on the live product; no product code.
