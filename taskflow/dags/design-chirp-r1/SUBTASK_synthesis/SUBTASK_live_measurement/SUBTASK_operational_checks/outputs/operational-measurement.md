# operational_check measurement — chirp @ `c805525`

Verdicts for every `BAR-*` in the release bar whose declared `verification_method` is `operational_check`
(68 criteria), judged by observing a property of the running `Nousix-LLC/nswe-demo` chirp service at commit
`c805525` and, where a code or manifest artifact determines whether the running property can exist at all,
the source at `c805525`. One row per `BAR-*`, keyed by `bar_id`; `live_status` ∈ `{met, partial, missing,
not_applicable}`.

## Access note

The running chirp deployment (the ArgoCD `chirp` application) was observed read-only, and its serving
container image digest matched the image pinned in `deploy/chirp/10-deployment.yaml` at `c805525`, so the
running service is the `c805525` build. Observation was confined to the project's own namespace and
application. The only mutation was a throwaway test account's own actions (register / sign in / post) and one
rollout restart of the project's own serving Deployment, performed to observe restart-survival; both are
within the normal effect a user or operator has on the project's own service. Where a running observation was
not exposed by the product (a capability that has no endpoint or signal), the determining source or manifest
property at `c805525` was read and the criterion judged conservatively. No result is assumed or invented.

## Shared observations (each verdict below cites the ones it rests on)

- **[RESTART]** — On the running deployment, an account (id 3) created beforehand with a chirp (id 2) and an
  active session (`tok-5-3`) was present before a rollout restart of the serving Deployment (profile 200; the
  authenticated timeline returned the chirp). After the restart every account was absent — including an
  account (id 0) created ~19 days earlier — `GET /api/users/3` → 404, `GET /api/users/0` → 404, re-login →
  `NOT_FOUND`, and the pre-restart session token → 401; `/healthz` returned 200 throughout. State does not
  survive a restart, redeploy, or process replacement.
- **[STORE]** — Authoritative state is the in-process `InMemoryRepository` (`std::sync::Mutex<Store>`) at
  `crates/chirp-server/src/repository/in_memory.rs`; `deploy/chirp/10-deployment.yaml` runs `replicas: 1` with
  no database, PVC, or StatefulSet. No durable store exists separate from the serving process (the named
  `c805525` blocker).
- **[HEALTH]** — The only health signal is one unauthenticated `GET /healthz` (`crates/chirp-server/src/api/router.rs`):
  state-free, returns 200 whenever the process is up ("process liveness only; there is no external dependency
  to check in the in-memory configuration"), wired to the startup, liveness, and readiness probes alike. After
  the restart the empty new pod reported 200/ready immediately. There is no store-reflecting readiness and no
  readiness-vs-liveness distinction.
- **[RATE]** — 80 rapid `GET /healthz` and 40 rapid `POST /api/users` requests from one client all succeeded
  (200 / 201); no request was throttled or returned 429. The router applies only a request `TraceLayer`, with
  no rate-limiting middleware.
- **[SURFACE]** — The HTTP surface is exactly 8 API routes plus `/healthz` plus a static/SPA fallback. There is
  no sign-out / session-invalidation endpoint, no sessions-and-devices listing, no account-deletion endpoint,
  no report endpoint, no operator/admin surface, and no metrics endpoint (`DELETE`/`GET /api/sessions` → 405,
  `DELETE /api/users/{id}` → 405, `POST /api/reports` → 405, `/metrics` serves the SPA page). Sessions are
  opaque in-memory tokens with no expiry or lifetime; authentication is handle-only, and the model carries no
  credential or verified-contact field.
- **[NOBACKUP]** — No backup or restore mechanism of any kind (no scheduled job, snapshot, PVC, or restore
  path); with an in-memory store there is nothing to back up or restore.
- **[NOSTATUS]** — No status or availability page, no serving/availability signal beyond `/healthz`, and no
  incident, alerting, or availability-measurement apparatus.
- **[LOG]** — A `tracing` subscriber with a tower-http `TraceLayer` logs request spans and their outcome and
  process start/stop, and logs `INTERNAL` errors at error level; there is no metrics endpoint, no
  store-connectivity event (no external store), and no dedicated authentication-outcome log event.
- **[ERRORS]** — The typed error taxonomy (`crates/chirp-server/src/error.rs`) is
  `VALIDATION_ERROR`/`UNAUTHORIZED`/`FORBIDDEN`/`NOT_FOUND`/`CONFLICT`/`INTERNAL`; observed live:
  `VALIDATION_ERROR` (400), `NOT_FOUND` (404), `UNAUTHORIZED` (401). There is no rate-limit / too-many-requests
  category.
- **[LIMITS+]** — Two bounds do exist: the timeline page size is clamped to 100 (`?limit=1000` → 200, served
  clamped; `MAX_TIMELINE_LIMIT` in `repository/mod.rs`), and an oversized request body is rejected (a 2.2 MB
  body → 400, axum's default 2 MB cap). Neither is a rate/quota limit, and neither returns a typed limit error
  category.

## Verdicts

| bar_id | live_status | observation |
|--------|-------------|-------------|
| BAR-013 | missing | [RESTART] An account created beforehand and its chirps/follows/likes are gone after a restart/redeploy; the in-memory store [STORE] loses everything. Headline `c805525` blocker. |
| BAR-032 | missing | [NOBACKUP] No operator backup/restore exists; [STORE] there is no durable store to back up. Cannot bring back accounts, chirps, follows. |
| BAR-033 | missing | [HEALTH] `/healthz` reports process liveness only and returned 200 from an empty pod after the restart; it never reflects whether the durable store can serve users. |
| BAR-034 | partial | The service responds at its address and the core loop worked live (register, sign in, post, timeline). But [NOSTATUS] there is no availability measurement against a target, and [RESTART] any restart/redeploy wipes user data, so sustained usable availability is not demonstrable. |
| BAR-035 | missing | [RATE] Posting/requesting beyond a reasonable rate is served without limit; bursts were not throttled or rejected. |
| BAR-130 | missing | [RESTART] Account, chirps, follows, likes, and session are all absent after the serving process is restarted; [STORE] in-memory backing. |
| BAR-131 | missing | [RESTART] After a restart the account does not read back at all (404) — id, handle, counts, and bio are gone, not merely altered. |
| BAR-132 | missing | [RESTART] Nothing persists across a restart, so sign-in/recovery data cannot survive it; additionally [SURFACE] the model has no credential or verified-contact field to persist. |
| BAR-133 | missing | [RESTART] Chirps do not read back after a restart (the posted chirp id 2 was lost); [STORE] in-memory. |
| BAR-134 | missing | [RESTART] Follow edges and the counts derived from them do not survive a restart; [STORE] in-memory. |
| BAR-135 | missing | [RESTART] Likes and like counts do not survive a restart; [STORE] in-memory. |
| BAR-136 | missing | [RESTART] A session obtained before the restart is not accepted afterward (prior token → 401 because the whole store was lost, not because it was validly carried); sessions are in-memory with no expiry/sign-out [SURFACE]. |
| BAR-137 | missing | [RESTART] Counts cannot equal edges after a restart because every account, edge, and like is gone; [STORE] in-memory. |
| BAR-138 | missing | [RESTART] The timeline cannot be reconstructed after a restart — its source chirps and follow graph are lost; [STORE] in-memory. |
| BAR-139 | missing | [RESTART] An acknowledged write (the posted chirp) was absent after a restart that followed its acknowledgement; no acknowledged write survives. |
| BAR-140 | missing | [RESTART] After a restart no references resolve because all entities are gone; [NOBACKUP] restore-from-backup does not exist. |
| BAR-141 | missing | [RESTART][STORE] The new pod's id counters reset to zero (`next_user_id`/`next_chirp_id` start at 0), so after a restart ids are reassigned to different entities and collide with pre-restart ids. |
| BAR-142 | missing | [SURFACE] There is no account-deletion feature, and [RESTART] nothing persists across a restart, so a deletion outcome cannot survive one. |
| BAR-143 | missing | [RESTART] Replacing the serving process with a fresh instance lost all accounts, chirps, follows, likes, and sessions — the authoritative state lived in the replaced process [STORE]. |
| BAR-144 | missing | [STORE] The `ChirpRepository` seam is backed by `InMemoryRepository` (process memory), confirmed by [RESTART] the product's state not surviving a restart. The named blocker. |
| BAR-145 | missing | [HEALTH] The product reports ready whenever the process is up, with no durable-store reachability check; an empty post-restart pod reported ready. |
| BAR-146 | missing | [NOBACKUP] No backup can be produced or restored; [STORE] no durable store exists. |
| BAR-147 | missing | `GET /api/users/{id}` returns a profile, but [SURFACE] no endpoint enumerates an account's complete set of chirps or its followed accounts, and [STORE] there is no committed durable state to match — the export enumeration is absent. |
| BAR-148 | missing | [RESTART] Data does not survive a plain restart, so a data-shape-changing upgrade cannot preserve it; no migration path exists. |
| BAR-178 | missing | [HEALTH] An unauthenticated health endpoint exists but reports process liveness only; it does not report not-ready when the store is unavailable, so an orchestrator cannot tell "serving" from "running". |
| BAR-252 | missing | [SURFACE] No sessions-and-devices listing and no session-ending endpoint (`GET`/`DELETE /api/sessions` → 405); a signed-in person cannot see or end other sessions. |
| BAR-253 | missing | [SURFACE] No sign-out endpoint exists; a session is never invalidated server-side (except by whole-process loss), so a prior session's replay is not refused on demand. |
| BAR-255 | missing | [SURFACE] No account-deletion flow or endpoint (`DELETE /api/users/{id}` → 405); the delete-account confirmation and its effects do not exist. |
| BAR-306 | missing | [SURFACE] Sessions are in-memory tokens with no bounded lifetime or expiry; an unrecognized token is rejected (401), but there is no expiry and no sign-out, so the lifetime/invalidation rules the criterion requires are absent. |
| BAR-307 | missing | [SURFACE] There is no sign-out that invalidates a session server-side; the prior token was refused after the restart only because the entire in-memory store was lost [RESTART], not because sign-out ended it. |
| BAR-308 | missing | [SURFACE] Sessions are not individually manageable — no endpoint lists a person's sessions or ends one device's session while others continue. |
| BAR-320 | missing | [SURFACE] No settings surface and no session management; sessions cannot be viewed or individually ended. |
| BAR-324 | missing | [SURFACE] There is no credential or recovery flow and no session-invalidation, so completing a reset cannot end pre-existing sessions or retire an old secret. |
| BAR-329 | missing | [SURFACE] No account deletion and no private-data model (no credential/verified-contact) to erase, and no mechanism to end an account's sessions on deletion. |
| BAR-333 | missing | [SURFACE] No operator/admin surface and no audit record; operator actions and their recording do not exist. |
| BAR-335 | missing | [SURFACE] No report endpoint and no operator/support surface; a filed report is neither recorded nor made available to act on. |
| BAR-336 | missing | [RATE] Writes and requests exceeding a reasonable rate from one client are served without limit; no per-account/per-client throttle exists. |
| BAR-337 | missing | [RATE] Automated mass account creation is not resisted — 40 consecutive sign-ups from one client all returned 201; the public sign-up surface has no challenge or limit. |
| BAR-400 | missing | [STORE] Authoritative state runs in serving-process memory, not a separate persistent component; [RESTART] replacing the process reset the state. The named blocker. |
| BAR-401 | missing | [RESTART] A restart/redeploy/replacement of the serving process lost every Account, Chirp, Follow, and Like, with no recovery. |
| BAR-402 | missing | [RESTART] A create confirmed to the user (the posted chirp) was absent after a restart immediately following its success response. |
| BAR-403 | missing | [RESTART] After a restart the durable data does not satisfy the invariants because it is entirely gone; counts, ids, and references do not survive. |
| BAR-404 | missing | [RESTART][STORE] A process replacement does not leave data consistent — the entire dataset vanishes rather than each write being fully applied or fully absent on a durable store. |
| BAR-405 | missing | [RESTART] A production upgrade changing data shape cannot preserve user data when a plain restart already loses all of it; no migration exists. |
| BAR-407 | missing | [SURFACE] No account-deletion feature and [NOSTATUS] no retention policy or enforcement; the deletion outcome and bounded-retention behavior do not exist. |
| BAR-409 | missing | [RESTART] An active session did not survive the restart (prior token → 401); [STORE] sessions are held in process memory. |
| BAR-410 | missing | [SURFACE] The model has no Credential or Verified-contact field, and [RESTART] nothing is retained durably across a restart; there is no deletion/retention path either. |
| BAR-420 | missing | [NOBACKUP] No scheduled backups are produced or recorded on any cadence. |
| BAR-422 | missing | [NOBACKUP] No backup exists to restore, so invariant-preserving restore cannot be demonstrated. |
| BAR-426 | missing | [NOBACKUP] No retained backup and no restore path; data at a backup point cannot be returned. |
| BAR-427 | missing | [NOBACKUP][NOSTATUS] No restore drill and no stated/measured RTO or RPO. |
| BAR-428 | missing | A deploy can be rolled back as a Kubernetes operation (`revisionHistoryLimit: 5`), but [RESTART] every roll loses the in-memory data, so the no-user-data-loss guarantee fails. |
| BAR-429 | missing | [NOBACKUP] Recovery from a damaging deploy via a pre-deploy backup is impossible — no backup or restore procedure exists. |
| BAR-430 | missing | [NOBACKUP] No recurring restore drill exists; there is nothing to restore or verify. |
| BAR-431 | missing | [NOBACKUP] No backup system exists, so a failed or missed backup cannot be surfaced to operators. |
| BAR-440 | missing | [RATE] No per-client request-rate bound on either the authenticated or unauthenticated surface; unauthenticated bursts were served without limit. |
| BAR-441 | missing | [RATE] State-creating actions have no tighter rate limit than reads — repeated `POST`s were served without throttling. |
| BAR-442 | missing | [RATE] No rolling-window volume bound on content creation; sustained creation is not bounded. |
| BAR-445 | missing | [RATE][ERRORS] No limit is enforced to exceed, and the error taxonomy has no typed limit/too-many-requests category distinct from validation or not-found. |
| BAR-460 | missing | [HEALTH] There is no readiness signal distinct from liveness; `/healthz` is process-only, carries no machine-distinguishable store-reflecting ready/not-ready state, and reported ready from an empty post-restart pod. |
| BAR-461 | partial | [HEALTH] A liveness probe exists and reports the serving process's own health only (`/healthz` → 200 while the process is up), which matches the liveness half; but no distinct readiness signal and no external store exist, so the liveness-alive-while-readiness-not-ready behavior cannot be realized. |
| BAR-464 | partial | [LOG] Request handling and outcome, process start/stop, and internal errors are logged via `tracing`/`TraceLayer`; but there is no store-connectivity event, no dedicated authentication-outcome event, and 4xx outcomes are not emitted as distinct categorized error events — several required event classes are absent. |
| BAR-466 | missing | [SURFACE][LOG] No serving-metrics endpoint exists (`/metrics` serves the SPA page); request/error-rate metrics are not exposed. |
| BAR-467 | missing | [NOSTATUS][HEALTH] No serving/availability signal reflects core-loop degradation; the only signal, `/healthz`, tracks process liveness, not whether users are served. |
| BAR-468 | missing | [SURFACE] No administrative surface and no audit log; administrative actions and their audit entries do not exist. |
| BAR-480 | missing | [NOSTATUS][LOG] No observability signals (serving/availability, request/error rates, saturation, store health) and no alerting; a serving degradation raises no notification. |
| BAR-483 | missing | [NOSTATUS] No status surface exists; the only reachable endpoint is the product itself, which is down when the product is down, so outage information is not independently reachable. |
| BAR-487 | missing | [NOSTATUS] Availability is not computed from any signal over a window; there is no measured availability to compare against a target. |

## Totals

68 `operational_check` criteria: 0 met, 3 partial (BAR-034, BAR-461, BAR-464), 65 missing, 0 not_applicable.
The operational posture at `c805525` turns on one observed fact — the in-memory store loses all state on a
restart or redeploy — which, with the absence of backups, rate limiting, session lifecycle, operator/admin and
audit surfaces, metrics, and any status/availability apparatus, leaves the band almost entirely unmet. The
three partials are the only running-service positives: the service responds with the core loop working at a
point in time (BAR-034), a process-only liveness probe exists (BAR-461), and request/start-stop/internal-error
logging exists (BAR-464).
