# SYNTHESIS — SUBTASK_live_journeys (manual_user_check union, totality assertion, fold)

Fold record for the `SUBTASK_live_journeys` subtree. This is the synthesis gate's terminal record and the
record the fold consumes to flip `SUBTASK_live_journeys` SUSPENDED → COMPLETED. Taskflow-internal (not
repository content).

## What this task did

Unioned the nine journey-cluster verdict tables into one `bar_id`-keyed table over all 139
`manual_user_check` `BAR-*` and wrote this subtree's declared output
`outputs/live-journeys-measurement.md` (columns `bar_id, live_status, observation`, one row per criterion,
ordered by `bar_id`, with the access and standing preamble). The fold is mechanical: verdicts and
observations are carried through from the clusters verbatim — no criterion was re-judged, no gap was
silently reconciled. The nine cluster outputs were COMPLETED dependencies and were read directly.

This node ran as a reconstructed taskflow invocation. The declared output existed from a prior invocation;
this invocation read all nine cluster files independently and re-verified every identity assertion below
before reporting COMPLETED and calling the fold.

## Fragments merged (owning cluster → count, confirmed by reading each cluster's verdict table)

| Cluster | Partition (manual_user_check) | Rows emitted | expected_counts |
|---------|-------------------------------|-------------:|----------------:|
| `SUBTASK_getin_identity` | get-in & identity journeys | 22 | 22 |
| `SUBTASK_core_loop` | account model, compose/post, reply, like, follow, timeline, profiles | 24 | 24 |
| `SUBTASK_account_lifecycle` | settings, edit profile, contact, sessions/devices, export, deletion, data rights | 20 | 20 |
| `SUBTASK_resilience_states` | empty/loading/error/not-found states, onboarding, session-expiry, feedback | 12 | 12 |
| `SUBTASK_safety_trust_support` | reporting, rules/terms, help & support, operator surface, status | 8 | 8 |
| `SUBTASK_visual_craft_nav` | navigation shell, consistency, layout, typography, contrast, motion, copy | 16 | 16 |
| `SUBTASK_responsive_phone` | typical-phone / responsive experience | 9 | 9 |
| `SUBTASK_accessibility` | keyboard & screen-reader path, WCAG checks | 18 | 18 |
| `SUBTASK_web_delivery_api` | one-address web delivery, SPA routing, typed API, health endpoint | 10 | 10 |
| **Union** | all `manual_user_check` `BAR-*` | **139** | **139** |

Each cluster's emitted `bar_id` set was checked for exact equality with the `contracts/_MANIFEST.yaml`
assignment for that cluster (no criterion judged that the contract did not assign; none assigned that the
cluster did not judge), and its row count against `expected_counts`. All nine match.

## Identity verdicts (evidence recorded; no silent plugs)

All five identities in `contracts/_MANIFEST.yaml` hold.

1. **CLUSTER_DISJOINT_TOTAL — PASS.** The nine clusters' `bar_id` sets are pairwise disjoint (0
   cross-cluster duplicates over the 139 rows) and union to exactly the 139 `manual_user_check` `BAR-*`.
   The union set equals the contract partition's 139 assignments (139 distinct, no duplicate assignment).
   Missing from the union: 0. Extra in the union: 0. Each criterion appears under exactly one cluster,
   matching the partition table in `contracts/_MANIFEST.yaml`.

2. **MANUAL_STATUS_TOTAL — PASS.** Every one of the 139 criteria carries exactly one `live_status` and a
   non-empty observation. Rows with no verdict or empty observation: 0.

3. **OBSERVATION_GROUNDED — PASS (carried through).** Each cluster grounded its observations in an actual
   read-only exercise of the live product at `c805525` or an actual SPA/API source artifact at `c805525`,
   and judged conservatively (`missing`/`partial`/`not_applicable`) with the reason stated where a surface
   could not be reached; this fold carried those observations through verbatim and did not weaken or
   optimize any verdict. The one `not_applicable` (BAR-485) is recorded conservatively with its reason by
   its owning cluster.

4. **VOCAB_CONFORMS — PASS.** Every `live_status` is from the inherited vocab {met, partial, missing,
   not_applicable}; every `bar_id` is a verbatim release-bar id of the form `BAR-NNN`. Out-of-vocab or
   malformed values: 0.

5. **OUTPUT_HYGIENE — PASS.** The deliverable `outputs/live-journeys-measurement.md` names things only by
   repository identity (`Nousix-LLC/nswe-demo`, commit `c805525`, repo-relative paths such as `crates/…`
   and product paths such as `/api/…`, `/healthz`) and `BAR-*`/`REQ-*` ids. No host/cluster addresses, no
   SSH detail, no filesystem/taskflow paths, no agent/DAG/run ids appear. Its preamble records only that
   the live product was reached, by repository/commit identity.

## Standing against the bar (this partition)

Of the 139 `manual_user_check` criteria: **met 27, partial 46, missing 65, not_applicable 1**.

| Cluster | met | partial | missing | n/a | total |
|---------|----:|--------:|--------:|----:|------:|
| getin_identity | 2 | 4 | 16 | 0 | 22 |
| core_loop | 12 | 6 | 6 | 0 | 24 |
| account_lifecycle | 0 | 0 | 20 | 0 | 20 |
| resilience_states | 0 | 8 | 4 | 0 | 12 |
| safety_trust_support | 0 | 0 | 7 | 1 | 8 |
| visual_craft_nav | 0 | 9 | 7 | 0 | 16 |
| responsive_phone | 1 | 5 | 3 | 0 | 9 |
| accessibility | 4 | 12 | 2 | 0 | 18 |
| web_delivery_api | 8 | 2 | 0 | 0 | 10 |
| **Total** | **27** | **46** | **65** | **1** | **139** |

The backend core loop (`SUBTASK_core_loop`: 12 met of 24) and the one-address web/API delivery
(`SUBTASK_web_delivery_api`: 8 met of 10) are largely present; the get-in and identity surfaces (16 of 22
missing), the whole account-management and lifecycle surface (20 of 20 missing), and the
safety/trust/support surfaces (7 missing, 1 n/a of 8) are where the product falls short of the bar, along
with the designed visual, resilience, and accessibility treatments (mostly `partial`, reflecting a working
skeleton without the designed depth).

## Methodology posture

The Phase-B `design` methodology loader was unavailable run-wide (`agent_domain_unset`), as recorded in
`_GLOBAL.md`; every cluster applied the principal-product-designer persona and the relayed release-bar
guidance, recorded the limitation, and proceeded. This fold applied the same posture and performed only the
mechanical union and verification. This note is internal; it is not in the repository-bound deliverable.

## Derived artifact

`manual_user_check_table` — the unioned `bar_id`-keyed verdict table — is `outputs/live-journeys-measurement.md`,
produced by this task and consumed by the parent `SUBTASK_measurement_fold`, which unions it with the
`automated_test`, `inspection`, and `operational_check` partitions into `outputs/live-measurement.md`.

## Fold

`outputs/live-journeys-measurement.md` exists and is verified (this subtree's declared output). After this
record is reported completed, the parent `SUBTASK_live_journeys` is resumed — fold: target
`SUBTASK_live_journeys`, synthesized `SUBTASK_journeys_fold`, seam this file — flipping it
SUSPENDED → COMPLETED with `outputs/live-journeys-measurement.md` as its result.
