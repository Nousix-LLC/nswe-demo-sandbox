# Safety, trust & support — live-product measurement (`manual_user_check`)

Cluster: safety, trust & support. Eight `manual_user_check` `BAR-*` judged against the deployed
chirp product at `Nousix-LLC/nswe-demo@c805525`. Each row carries one `live_status` ∈ {met, partial,
missing, not_applicable} and an observation grounded in what was exercised or read.

## Access note

The deployed product was reached and exercised read-only. Its running server image's `crates/` tree is
byte-identical to `Nousix-LLC/nswe-demo` at commit `c805525` (confirmed by diffing `crates/` between
`c805525` and the synced deploy revision `276138f`, of which `c805525` is an ancestor), so these
observations are of the `c805525` application. A single throwaway account was created and signed in to
exercise the signed-in surface; no other mutation was made. Where the running UI is client-rendered
WebAssembly (not scrapable over HTTP), presence or absence of a surface was settled from the `c805525`
SPA/API source, which is authoritative for what the client renders.

Context observed once, relied on by several rows below:
- **API surface** (`crates/chirp-server/src/api/router.rs`): the only routes are `POST /api/users`,
  `GET /api/users/{id}`, `POST /api/sessions`, `POST /api/chirps`, `GET /api/timeline`,
  `PUT|DELETE /api/users/{id}/follow`, `PUT|DELETE /api/chirps/{id}/like`, and `GET /healthz`; every
  other path falls through to the SPA's `index.html`. Live probes agree: `GET /api/timeline` returns
  JSON (`401` without a token, `200` with one), while `/api/reports`, `/api/report`, `/api/rules`,
  `/api/moderation`, `/api/admin`, `/api/status` return the HTML SPA shell on `GET` and `405` on `POST`
  — there is no such endpoint, authenticated or not.
- **SPA surface** (`crates/chirp-frontend/src/app.rs`): the route table is `/` (timeline), `/compose`,
  `/user/:id` (profile), plus a not-found fallback; the persistent nav renders only "Timeline · Compose".
  There is no account menu, more-actions menu, or settings entry.
- **Store**: `crates/chirp-server/src/repository/` has one backing, `InMemoryRepository`; `deploy/README.md`
  states no external database is required, and the deploy manifests define no database, StatefulSet, or
  persistent volume for chirp. There is no durable store separable from the serving process.

## Verdicts

| bar_id | live_status | observation |
|--------|-------------|-------------|
| BAR-023 | missing | No report action exists for a chirp or an account. The API has no reporting route (`POST /api/reports` and related paths return `405` with a signed-in token; `GET` returns the SPA shell), and the SPA source exposes no report control on any screen. A signed-in person cannot report, so nothing is acknowledged. Grounded in the live API probes and the `c805525` router/SPA source. |
| BAR-025 | missing | There is no operator/support surface of any kind. `crates/` contains no admin, operator, or moderation module; the API router mounts no admin/operator route; grep of the `c805525` source for admin/operator/moderation finds only unrelated code (e.g. the `?` operator). The provisioned least-privilege operator path a user cannot reach is confirmed absent from the SPA/API source, so assisting recovery, removing a named chirp, and actioning an abusive account are not available through any supported interface — only by editing in-memory state in process, which is the opposite of what the criterion requires. |
| BAR-256 | missing | No report action is reachable from a chirp's or an account's more-actions menu — the SPA renders no more-actions menu and no report control (`app.rs` route/nav table), and the API has no report endpoint. With no report flow present there is no reason picker, no optional-detail field, no in-product confirmation, and no disabled-submit-until-reason behavior to exercise. The absence is total rather than a silent no-op. Grounded in the `c805525` SPA source and live API probes. |
| BAR-257 | missing | There is no Rules & terms screen from either shell. The SPA route table (`/`, `/compose`, `/user/:id`) has no rules/terms route, and the nav offers no such link; the `c805525` source contains no rules or terms content (grep finds only an unrelated "emptiness rule" and the `macro_rules!` token). Because no report action exists either, there are no report reasons to correspond to named rule categories. Grounded in the `c805525` SPA source and live probes of `/rules` and `/terms` (both return the SPA shell, not a rules screen). |
| BAR-258 | missing | No Help & support entry exists in either shell. Signed out, the served page's nav is only "Timeline · Compose"; signed in, there is no account menu (the SPA renders none), so no help entry hangs off one. The SPA source has no help/support route or view, and consequently no "Can't get in?" recover-access path and no "Contact support" path. Live probes of `/help` and `/support` return the SPA shell, not a help screen. Grounded in the `c805525` SPA source and live probes. |
| BAR-334 | missing | Same surfaces as BAR-023 and BAR-257, judged against the identity/trust requirement: a signed-in person cannot report a chirp or an account (no report endpoint; `POST` to report paths returns `405`), receives no acknowledgement, and cannot point a report at a rule because no in-product rules screen exists. Nothing here is reachable within the product. Grounded in the live API probes and the `c805525` SPA/API source. |
| BAR-482 | missing | There is no user-facing status or incident surface. The SPA has no status route or in-product status notice, and the only health-related endpoint is `GET /healthz` — a machine liveness probe that returns `{"service":"chirp-server","status":"ok","version":"0.1.0"}`. By its own source it touches no state and has no dependency to check, so it always reports "ok" while the process is up and cannot express a degraded state; it is also not surfaced to a person as a status page. A person hitting an unavailable or degraded product is left to infer it from a failed request or a non-loading page, which is what the criterion says must not happen. Grounded in the live `/healthz` response and the `c805525` router/SPA source. |
| BAR-485 | not_applicable | The stated fault — the durable store made unreachable while the serving process stays up — cannot be constructed at `c805525`: the product has a single in-memory backing (`InMemoryRepository`) and no separable durable store (`deploy/README.md`: no external database; no database/StatefulSet/PVC in the deploy manifests), so state shares the process's lifetime and cannot fail independently of it. The specific resilience scenario therefore does not apply to this architecture. Recorded conservatively, not as a pass: the SPA does map transport/API failures to a coherent `AppError` UI state without panicking (`crates/chirp-frontend/src/error.rs`), but there is no explained backend-outage/degraded experience or status surface, and because the SPA is served by the same process, a true backend outage would stop the page loading rather than present an explained degraded experience. The adjacent per-request error/empty/expired-session experiences are owned by the resilience-states cluster, not measured here. |

## Loader limitation

The Phase-B `design` methodology loader was unavailable run-wide (`agent_domain_unset`). This cluster was
measured on the principal-product-designer persona and the relayed ReleaseBar guidance, as the brief and
subtree hub direct; the limitation is recorded and did not block the measurement.

## Totals

Eight owned `BAR-*`, each with exactly one `live_status`: missing ×7 (BAR-023, BAR-025, BAR-256, BAR-257,
BAR-258, BAR-334, BAR-482), not_applicable ×1 (BAR-485). No `BAR-*` outside this cluster included.
