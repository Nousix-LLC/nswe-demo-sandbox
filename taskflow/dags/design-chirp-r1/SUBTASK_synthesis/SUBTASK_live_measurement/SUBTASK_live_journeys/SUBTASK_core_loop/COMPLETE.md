# COMPLETE — SUBTASK_core_loop

**Task:** Measure the core value loop (`manual_user_check` cluster, 24 `BAR-*`) against the deployed `chirp` product at `Nousix-LLC/nswe-demo` commit `c805525`.

## What was done
Exercised the live product end to end and judged each of the 24 owned `BAR-*` to a grounded observation, producing the declared verdict table.

- **Reached the live product:** the single-page app, `/healthz`, and the `/api/*` REST surface all answered; the built WASM bundle is served, so the frontend runs.
- **Data behaviors** (account model, handle rules, opaque ids, timestamps, compose/post, reply targeting, follow, like, counts, derived paginated newest-first timeline, referential integrity, server-enforced invariants) were exercised directly against the API with two throwaway test accounts — read-only beyond those accounts' own ordinary actions. No product code was written and no repo/namespace outside the project's own was touched.
- **UI-presentation behaviors** (compose placements, like/follow controls, profile, timeline affordances, reply/conversation) were judged against the `c805525` frontend source compiled into the served bundle and the server routing, where the running SPA's screen inventory can be read off a code artifact (the WASM SPA cannot be driven headlessly here).

## Result
- **met (12):** BAR-100, 101, 102, 104, 106, 107, 108, 109, 110, 111, 117, 163.
- **partial (6):** BAR-209, 211, 212, 238, 245, 246.
- **missing (6):** BAR-105, 239, 242, 243, 244, 247.
- **not_applicable (0).**

The backend core loop is present and correct; the gaps are in the walking-skeleton frontend (no profile editing, no conversation/catch-up, a single bare composer with no reply path or character counter, no genuine per-chirp like control, no followers/following lists) and in the account-edit surface (no profile-edit endpoint).

## Output
- `outputs/core-loop-measurement.md` — verdict table conforming to the inherited `verdict_row_schema` (`bar_id, live_status, observation`), one row per owned `BAR-*`, keyed by `bar_id`, with an access-note preamble recording reachability by repository/commit identity only.

## Verification against success criteria
- Every owned `BAR-*` carries exactly one `live_status` and a grounded observation; none omitted; no `BAR-*` outside this cluster included (24 rows, matching the `contracts/_MANIFEST.yaml` `SUBTASK_core_loop` partition and its expected count of 24).
- Each observation is grounded in an actual exercise of the live product or an actual `c805525` source artifact; unobservable-in-UI criteria judged against the deployed source, never confabulated.
- `live_status` values are from the inherited vocab; `bar_id`s are verbatim.
- Read-only on the live product; output touches only `Nousix-LLC/nswe-demo` and the project's own deployment; no host/system/taskflow detail in the output.

## Methodology note
The Phase-B `design` methodology loader was unavailable run-wide (`agent_domain_unset`); this node applied the principal-product-designer persona and the relayed ReleaseBar guidance and proceeded, recording the limitation.
