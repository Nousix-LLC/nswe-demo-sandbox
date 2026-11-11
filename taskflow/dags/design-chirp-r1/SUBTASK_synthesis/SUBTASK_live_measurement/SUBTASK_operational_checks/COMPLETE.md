# COMPLETE — SUBTASK_operational_checks

## What was done

Judged every `BAR-*` in the release bar whose declared `verification_method` is `operational_check` (68
criteria, the exact unique set tagged `operational_check` in `SUBTASK_release_bar/outputs/release-bar.md`)
against the running `Nousix-LLC/nswe-demo` chirp service at commit `c805525`, each with one `live_status` ∈
`{met, partial, missing, not_applicable}` and a grounded observation. Output conforms to `verdict_row_schema`
in `../contracts/_MANIFEST.yaml` (columns `bar_id, live_status, observation`), keyed by `bar_id`.

## How it was grounded

The running deployment was reached read-only and its serving image digest matched the `c805525` manifest, so
the live service is the `c805525` build. The headline fact — whether state survives a restart — was observed
directly: a throwaway account, chirp, and session were created on the running service, the serving Deployment
was rolled-restarted (a redeploy of the project's own process), and afterward every account (including a
~19-day-old one), chirp, and session was gone while `/healthz` stayed 200. This one observation settles the
whole durable-persistence band and confirms readiness is process-liveness only. Further live observations
grounded the remaining bands: request bursts (no rate limiting), endpoint probes (no logout / sessions-list /
account-delete / report / admin / metrics surfaces), the timeline page-size clamp and the 2 MB body cap, and
the typed error taxonomy. Where a property has no running surface, the determining source/manifest at
`c805525` (the in-memory `ChirpRepository`, the deployment manifest, the router, the error enum) was read and
the criterion judged conservatively. No result was assumed or invented.

## Result

0 met, 3 partial (BAR-034, BAR-461, BAR-464), 65 missing, 0 not_applicable. The posture turns on the
in-memory store losing all state on restart/redeploy, compounded by the absence of backups, rate limiting,
session lifecycle, operator/admin and audit surfaces, metrics, and status/availability apparatus.

## Output

- `outputs/operational-measurement.md` — access-note header + the 68-row `bar_id`-keyed verdict table.

## Conformance

- Every `operational_check` `BAR-*` present exactly once; none omitted; no criterion of another method
  included (verified: symmetric diff against the release-bar `operational_check` set is empty).
- `live_status` values from the inherited vocab; `bar_id`s verbatim.
- Read-only on the live product; only the project's own namespace/application touched; the one mutation was a
  throwaway test account's own actions plus one rollout restart of the project's own Deployment.
- Output carries no host/system/taskflow detail — repository identity, commit SHA, repo-relative paths, and
  `BAR-*`/`REQ-*` ids only (verified by hygiene scan).

## Note

The Phase-B `design`-domain methodology loader was unreachable in this reconstructed node
(`agent_domain_unset`), as recorded in `../_GLOBAL.md`; the principal-product-designer persona and the relayed
ReleaseBar guidance, with `_BRIEF.md`, `../_GLOBAL.md`, and `../contracts/`, fully specified the work.
