# COMPLETE — SUBTASK_safety_trust_support

## What was done
Judged the 8 `manual_user_check` `BAR-*` owned by the safety/trust/support cluster against the deployed
chirp product at `Nousix-LLC/nswe-demo@c805525`, exercising the live product read-only and confirming
presence/absence of each surface in the `c805525` SPA/API source where the running (WebAssembly) UI is
client-rendered. One throwaway account was created and signed in to exercise the signed-in surface; no
other mutation was made.

## Output produced
- `outputs/safety-trust-support-measurement.md` — a verdict table conforming to the inherited
  `verdict_row_schema` (columns `bar_id, live_status, observation`), one row per owned `BAR-*`, keyed by
  `bar_id`, plus an access-note header (repository/commit identity only).

## Verdicts
- missing ×7: BAR-023, BAR-025, BAR-256, BAR-257, BAR-258, BAR-334, BAR-482
- not_applicable ×1: BAR-485
- No `BAR-*` outside this cluster included.

## Grounding
- API surface read from `crates/chirp-server/src/api/router.rs` at `c805525` and confirmed by live probes
  (real routes return JSON; report/rules/help/admin/status paths return the SPA shell on GET and 405 on
  POST — no such endpoint, authenticated or not).
- SPA surface read from `crates/chirp-frontend/src/app.rs` at `c805525` (routes: timeline, compose,
  profile; nav: "Timeline · Compose") — no report action, rules/terms, help/support, account menu,
  operator, or status screen.
- Store confirmed in-memory only (`InMemoryRepository`; `deploy/README.md` states no external database;
  no database/StatefulSet/PVC in deploy manifests), grounding BAR-485 not_applicable.
- Running image's `crates/` tree verified byte-identical to `c805525` (diff of `crates/` between `c805525`
  and the synced deploy revision `276138f`), so live observations are of the `c805525` application.

## Success criteria
- [x] Every owned `BAR-*` carries exactly one `live_status` and a grounded observation; none omitted;
      no out-of-cluster `BAR-*` included.
- [x] Each observation grounded in an actual exercise of the live product or an actual `c805525` source
      artifact; nothing assumed or confabulated; unobservable/inapplicable cases judged conservatively.
- [x] `live_status` values from the inherited vocab; `bar_id`s verbatim.
- [x] Read-only on the live product; output touches only `Nousix-LLC/nswe-demo` and the project
      deployment; no host/system/taskflow detail (scanned clean).

## Note
The Phase-B `design` methodology loader was unavailable run-wide (`agent_domain_unset`); measured on the
principal-product-designer persona and the relayed ReleaseBar guidance per the brief, limitation recorded
in the output. This node was (re)dispatched with only its `_BRIEF.md` present and no prior output; it
produced the measurement fresh.
