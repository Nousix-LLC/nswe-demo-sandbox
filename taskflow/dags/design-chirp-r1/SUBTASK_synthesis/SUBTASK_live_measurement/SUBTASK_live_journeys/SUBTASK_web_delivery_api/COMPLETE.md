# COMPLETE — SUBTASK_web_delivery_api

**Task**: Measure the 10 `manual_user_check` `BAR-*` of the web-delivery & API-as-experienced
cluster against the live `Nousix-LLC/nswe-demo` product at `c805525`.

**Decompose evaluation**: Atomic — one coherent surface (web delivery + API as experienced),
measured by one read-only exercise of the running product; one kind of output (a `bar_id`-keyed
verdict table). Every decomposition trigger cleared and both concern tests passed.

## What was done

Exercised the live product read-only as a user: the SPA served at one web address, its client-side
routes, and the REST surface under `/api/…` the app calls. Created one throwaway account (and a
second to exercise follow), opened a session, posted a chirp and a reply, read the timeline with
pagination, followed/unfollowed, liked/unliked, and probed the typed-error, routing, and health
surfaces. Where the running product was ambiguous or a surface was absent, settled presence/absence
from the product source at `c805525` (router, handlers, types, repository, frontend app, Dockerfile,
and deploy manifests). No product code changed; no state touched beyond the throwaway account's own
actions.

## Result

`outputs/web-delivery-api-measurement.md` — a verdict table conforming to the inherited
`verdict_row_schema` (`bar_id, live_status, observation`), one row per owned `BAR-*`, with a short
access note recording only that the product was reached, by repository/commit identity.

- met: 8 — BAR-166, BAR-169, BAR-170, BAR-171, BAR-172, BAR-173, BAR-176, BAR-462
- partial: 2 — BAR-177 (SPA route set omits sign-up/recovery/settings/deletion), BAR-406
  (in-memory backing at `c805525`; no across-restart durability)
- missing: 0 · not_applicable: 0 · total: 10

## Success criteria

- [x] Every owned `BAR-*` carries exactly one `live_status` and a grounded observation; none
      omitted; no `BAR-*` outside the cluster included.
- [x] Each observation grounded in an actual exercise of the running product, or an actual
      `c805525` source artifact where a surface was absent/ambiguous — never assumed.
- [x] `live_status` values from the inherited vocab; `bar_id`s verbatim.
- [x] Read-only on the live product (beyond the throwaway account's own actions); output touches
      only `Nousix-LLC/nswe-demo` and references no host/system/taskflow detail.

## Notes

- Phase-B `design` methodology loader unavailable run-wide (`agent_domain_unset`); applied the
  principal-product-designer persona and relayed ReleaseBar guidance, recorded the limitation,
  proceeded. Did not block the measurement.
- The live deployment serves the real `chirp-frontend` WASM SPA built from `c805525` (via
  `CHIRP_STATIC_DIR`), not the committed server-side placeholder `index.html` — reconciled before
  judging the delivery/routing criteria.
