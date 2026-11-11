# Web-delivery & API-as-experienced — live measurement (`manual_user_check`)

**Cluster**: `SUBTASK_web_delivery_api` · **Product**: `Nousix-LLC/nswe-demo` @ `c805525` · **Method**: `manual_user_check`
**Owned criteria**: BAR-166, BAR-169, BAR-170, BAR-171, BAR-172, BAR-173, BAR-176, BAR-177, BAR-406, BAR-462 (10)

## Access note

The live product was reached and exercised read-only as a user does — through the single-page app
served at one web address, the client-side routes, and the REST surface under `/api/…` that the app
itself calls. A single throwaway account was used for signed-in operations; no other account or
state was touched, and no product code was changed. Where the running product was ambiguous or a
surface was absent, presence/absence was settled from the product source at `c805525`
(repo-relative paths cited in the observations). The product is referenced only by repository
identity (`Nousix-LLC/nswe-demo`), commit SHA `c805525`, repo-relative paths, and `BAR-*`/`REQ-*`
ids.

The served SPA is the `chirp-frontend` WASM bundle built from `c805525` (per `Dockerfile`, shipped
to `/srv/chirp` and read via `CHIRP_STATIC_DIR`); it is the real app, not the committed
`crates/chirp-server/static/index.html` placeholder, which the deployment overrides.

**Methodology limitation**: the Phase-B `design` methodology loader was unavailable run-wide
(`agent_domain_unset`); this node applied the principal-product-designer persona and the relayed
ReleaseBar guidance, recorded the limitation, and proceeded. It did not block the measurement.

## Verdict table

| bar_id | live_status | observation |
|--------|-------------|-------------|
| BAR-166 | met | One origin serves all three surfaces: the SPA at `/` (HTTP 200, `text/html`), the REST API under `/api/…`, and the health probe at `/healthz` (HTTP 200, JSON). The only deployable is a single-replica `chirp-server` (`deploy/chirp/10-deployment.yaml`: `replicas: 1`, one container); `crates/chirp-server/src/api/router.rs` mounts the API, `/healthz`, and the static/SPA service into one router. No second process or second deployable was needed to serve the app. |
| BAR-169 | met | The REST surface lives under the reserved `/api/…` prefix on the same origin that served the app, so normal operation involves no cross-origin configuration. A path that is not an API path resolves to the SPA: `GET /settings` returned the app entry document (HTTP 200, `text/html`), not an API handler. Confirmed against `crates/chirp-server/src/api/router.rs`, which mounts the explicit `/api/*` routes first and a static-dir + `index.html` fallback for everything else. |
| BAR-170 | met | Every listed operation was served end to end from the running product, each with a defined request/response type in `crates/chirp-types/src/api.rs`: create account (`POST /api/users` → 201, `User`), fetch public profile (`GET /api/users/{id}` → 200), open session (`POST /api/sessions` → 200, `AuthResponse`), post a chirp and a reply (`POST /api/chirps` → 201, `Chirp` with `replyTo` set), read a timeline (`GET /api/timeline` → 200, `Page<Chirp>`), follow and unfollow (`PUT`/`DELETE /api/users/{id}/follow` → 200, `FollowResponse`), like and unlike (`PUT`/`DELETE /api/chirps/{id}/like` → 200, `LikeResponse`). |
| BAR-171 | met | `GET /api/timeline?limit=2` returned a bounded 2-item page with an opaque `nextCursor`; passing that cursor returned the next older page with its own cursor; `GET /api/timeline?limit=500` returned HTTP 200 with the limit clamped to the server maximum (`MAX_TIMELINE_LIMIT = 100` in `crates/chirp-server/src/repository/mod.rs`), so a client cannot pull every chirp in one response. The cursor crosses the contract as an opaque string the client echoes back (`Cursor` in `crates/chirp-types/src/api.rs`). |
| BAR-172 | met | A signed-in request proved itself with an opaque, server-issued bearer token presented as `Authorization: Bearer …`; a missing or invalid token was rejected with 401 (`crates/chirp-server/src/api/auth.rs`). Only public data crossed outward: profile responses carried `id, username, displayName, bio, createdAt, followerCount, followingCount` and nothing else, and chirp responses only public chirp fields. The session token appeared only in the login issuance response, as intended. The `c805525` domain (`crates/chirp-types/src/domain.rs`) has no password or verified-contact field at all (handle-based auth), so no credential or contact value can appear in any response. |
| BAR-173 | met | Every failed request returned a typed `ApiError` `{code, message, details?}` with a machine-readable `SCREAMING_SNAKE_CASE` category the frontend can branch on (`ErrorCode` in `crates/chirp-types/src/api.rs`): a taken handle → `CONFLICT`/409, a malformed handle → `VALIDATION_ERROR`/400 with field `details` — the two are distinguished — a missing/invalid token → `UNAUTHORIZED`/401, an unknown id → `NOT_FOUND`/404, a self-follow → `FORBIDDEN`/403. No ad-hoc string errors were seen. |
| BAR-176 | met | The server serves the frontend as static assets from a configurable root (`CHIRP_STATIC_DIR`, set to `/srv/chirp` in `deploy/chirp/10-deployment.yaml`; `ServeDir` in `crates/chirp-server/src/api/router.rs`). A deep in-app route reached directly (`GET /settings`) loaded the app's entry document (HTTP 200, `text/html`), which the WASM `ferric-router` SPA resolves client-side; an unknown path (`GET /api/does-not-exist`) returned the same `index.html` entry document rather than a server error. |
| BAR-177 | partial | The one-address delivery holds: the running product serves the single-page app at one web address with nothing to install and no second place to go. But the in-app route set does not reach the full release surface set. The SPA's routes are `/` (timeline), `/compose` (handle login + compose), and `/user/:id` (profile), plus a no-match fallback (`crates/chirp-frontend/src/app.rs`); `/compose` offers a sign-**in** (log-in) form only, and there are no recovery, settings, or account-deletion screens (no corresponding frontend modules or routes at `c805525`). So sign-in, timeline, compose/reply, and profile are reachable; sign-up, recovery, settings, and deletion are not. |
| BAR-406 | partial | On the running product an account's data stayed present and complete throughout an uninterrupted operating period: the throwaway account, its chirps (including a reply), a follow, and a like were all created and read back consistently across repeated requests. But the only backing at `c805525` is an in-memory repository (`crates/chirp-server/src/repository/in_memory.rs`; `deploy/chirp/10-deployment.yaml` states the server "uses an in-memory repository (no DB / no PVC)"), so ordinary restarts and redeploys lose all account data and the holder would have to re-create it — the across-restart durability the criterion requires is not met, and the loss is not a stated retention age-out but an unexplained wipe. (Restart/redeploy survival proper is the operational-check partition's method; recorded here from the within-run exercise plus the in-memory backing settled from source.) |
| BAR-462 | met | `GET /healthz` answered with no account or session present (HTTP 200, `application/json`: `{"status":"ok","service":"chirp-server","version":"0.1.0"}`). The body conveys serving status only — no credential, session token, verified-contact value, or secret such as a connection string. Confirmed against `crates/chirp-server/src/api/router.rs`, where the `healthz` handler is unauthenticated and touches no application state. |

## Summary (not part of the schema)

- met: 8 — BAR-166, BAR-169, BAR-170, BAR-171, BAR-172, BAR-173, BAR-176, BAR-462
- partial: 2 — BAR-177 (SPA route set omits sign-up/recovery/settings/deletion), BAR-406 (in-memory backing; no across-restart durability)
- missing: 0 · not_applicable: 0 · total: 10
