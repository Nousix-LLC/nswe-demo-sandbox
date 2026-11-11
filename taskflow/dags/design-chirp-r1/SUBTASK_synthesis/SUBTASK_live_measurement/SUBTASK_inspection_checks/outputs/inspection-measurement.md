# Inspection measurement — `Nousix-LLC/nswe-demo` @ `c805525`

The 35 release-bar criteria whose declared `verification_method` is `inspection`, judged by reading the
declared property from a config, manifest, or code artifact in the repository at commit `c805525`. Each row
carries exactly one `live_status` ∈ {met, partial, missing, not_applicable} and an observation citing the
repo-relative artifact it rests on and the property found there.

## Access note

The product was reached **by repository inspection only**: every artifact was read from `Nousix-LLC/nswe-demo`
at commit `c805525` (read-only; no checkout mutated, no product code written). Verdicts are grounded in what
the artifacts at `c805525` declare, not in the product's runtime behaviour (another method's job) nor in what
the design intends. Two facts set the backdrop for several verdicts and are stated once here:

- **The `design/` tree is empty at `c805525`.** The refreshed design documents land only through the still-open
  PR `#122`; they are not part of the product at this commit. Any criterion that asks whether *the product
  states/publishes a posture* is therefore measured against the product's own shipped artifacts (code, README,
  `deploy/`, in-product content) at `c805525`, where those postures are absent.
- **Authentication at `c805525` is handle-only.** `LoginRequest` carries just a `username`; `crates/chirp-server/src/repository/mod.rs`
  states "there is no password/credential step." There is no account secret, no verified contact, and no
  recovery, deletion, export, settings, reporting, or operator surface in the router
  (`crates/chirp-server/src/api/router.rs` mounts only the core loop + `/healthz`).

A `releasable` surface or posture that is simply not built at `c805525` is judged `missing` (it applies to this
product and is absent), never `not_applicable`. Where a guarantee is only partly realized, the row is `partial`
and names both halves.

## Verdicts

| bar_id | live_status | observation |
|--------|-------------|-------------|
| BAR-021 | missing | Deletion outcome. No account-deletion surface exists and no artifact states a deletion outcome: `crates/chirp-server/src/api/router.rs` mounts no delete-account route, and `design/` is empty at `c805525`. The stated-outcome property has no subject and no behaviour to match. |
| BAR-024 | missing | In-product rules. No rules/terms content ships at `c805525`: no rules artifact in the repo, no rules route in `crates/chirp-server/src/api/router.rs`, and `design/` is empty. A report cannot point to rules that are not stated. |
| BAR-120 | met | Server-maintained counts. `crates/chirp-types/src/api.rs` `CreateUserRequest` (username, displayName, bio) and `CreateChirpRequest` (text, replyTo) carry **no** count fields, so a create/update request cannot set a count; `crates/chirp-types/src/domain.rs` documents `User::followerCount/followingCount` and `Chirp::likeCount` as "denormalized, read-only to clients"; `crates/chirp-server/src/repository/mod.rs` `create_user` assigns "zeroed follower/following counts". Counts are never honored as client input. |
| BAR-160 | met | Crate partition. Workspace `Cargo.toml` `members = ["crates/*"]` resolves to exactly six crates: the framework layer `ferric`, `ferric-http`, `ferric-router` and the product layer `chirp-types`, `chirp-server`, `chirp-frontend` — no fifth product crate. Each entity's three concerns resolve to one part: wire shape in `chirp-types` (`src/domain.rs` + `src/api.rs`), lifecycle/persistence in `chirp-server` (the `ChirpRepository` seam), presentation in `chirp-frontend`; the frontend owns no entity shape. |
| BAR-161 | met | Framework isolation. `crates/ferric/Cargo.toml`, `crates/ferric-http/Cargo.toml`, and `crates/ferric-router/Cargo.toml` declare **no** dependency on `chirp-types`; a scan of those crates' `src/` finds no chirp entity name (Account/Chirp/Follow/Like/Timeline/Session/UserId/ChirpId). `crates/chirp-frontend/Cargo.toml` path-depends on `ferric`/`ferric-router`/`ferric-http` (and `chirp-types`); the dependency never runs the other way. |
| BAR-162 | met | Single contract source. `crates/chirp-types/Cargo.toml` has one runtime dependency, `serde` (plus a `serde_json` dev-dependency for round-trip tests); `src/lib.rs` states the crate is "pure data and validation — no I/O, no framework, no async," which is what lets both the native server and the wasm frontend import it unchanged. Entities, value objects, DTOs, the `Page` envelope, `SessionToken`, and `ApiError`/`ErrorCode` are all defined here. |
| BAR-165 | met | One repository boundary. `crates/chirp-server/src/repository/mod.rs` defines the `ChirpRepository` trait as the single seam ("Everything the server does to durable state goes through `ChirpRepository`") and enumerates exactly the durable operations used (create_user, get_user, login, resolve_token, create_chirp, timeline, follow/unfollow, like/unlike); `src/api/state.rs` holds it as `Arc<dyn ChirpRepository>`; every handler in `src/api/handlers.rs` delegates via `state.repo.<op>()` with no direct store access in handler bodies. A second implementor (the default is `InMemoryRepository`) needs no handler change. |
| BAR-167 | met | Frontend owns only the session. `crates/chirp-frontend/src/app.rs` `AppContext` holds `base_url` and a reactive `session: Signal<Option<Session>>`, where `Session` is the authenticated `User` + bearer `SessionToken`; the signal starts `None` on load (reload re-fetches). Every account/chirp/follow/like/timeline is fetched through the typed `ApiClient` in `src/api.rs`; no entity data is held client-side across views. |
| BAR-168 | met | Shared wire types. `crates/chirp-frontend/src/api.rs` uses `use chirp_types::prelude::*` and (de)serializes the DTOs directly; `crates/chirp-server` imports the same `chirp-types` ("never re-declared", per `src/lib.rs`). No second, hand-maintained copy of any wire shape exists on either side. |
| BAR-174 | met | Wire-shape stability. `crates/chirp-types/src/lib.rs` + `src/domain.rs` pin JSON keys via `#[serde(rename_all = "camelCase")]` ("deliberate and load-bearing" — a Rust rename does not change the wire); ids/`Cursor`/`SessionToken` use `#[serde(transparent)]` (serialize as the bare value, `src/ids.rs`); `Username`/`ChirpText` use `#[serde(try_from = "String")]` (reject invalid input on the way in); `ErrorCode` is a `SCREAMING_SNAKE_CASE` machine-readable enum (`src/api.rs`); the crate root states growth is "additive-only". |
| BAR-175 | missing | Release-surface placement. The new surfaces this criterion enumerates (end-session, edit-profile, settings, recovery, export, deletion, reporting/blocking/muting, notifications, operator/admin, find-accounts) are absent at `c805525`: `crates/chirp-types/src/api.rs` defines only the core-loop DTOs and `crates/chirp-server/src/api/router.rs` mounts only the core routes + `/healthz`. The enabling structure is in place (one `chirp-types` contract, one `/api` namespace, additive-only growth per BAR-174), but the surfaces the criterion checks are not built. |
| BAR-179 | met | Config from environment, one artifact. `crates/chirp-server/src/main.rs` reads `CHIRP_BIND_ADDR` (default `127.0.0.1:3000`) and `src/api/router.rs` reads `CHIRP_STATIC_DIR` (default crate-local `static/`) from the environment with defaults — nothing hard-coded. `README.md` + `deploy/README.md` + `Dockerfile` ship one self-contained image that serves the REST API under `/api/…` and the SPA at `/` from the in-memory default, reconfigured to a fresh environment by env vars only (image default `CHIRP_BIND_ADDR=0.0.0.0:8080`). |
| BAR-203 | missing | Screen inventory. No published screen-inventory artifact exists at `c805525`: `design/` is empty and `crates/chirp-frontend` carries no inventory (its `src/app.rs` wires a nav plus timeline/compose/profile views and a fallback, with no route/archetype/auth-state register to match screens against). |
| BAR-275 | missing | Accessibility standard. No accessibility statement ships at `c805525` — `design/` is empty and no artifact names WCAG 2.1 Level AA or enumerates a gated conformance set. A reviewer cannot find the stated standard or gated set. |
| BAR-293 | missing | Accessibility checks on file. No recorded accessibility checks (automated scan, keyboard walk, screen-reader walk) or support matrix exist at `c805525`; `design/` is empty and the repository holds no such records. |
| BAR-294 | missing | Accessibility release record. No release record of a cleared gated conformance set (no open A/AA failures) exists at `c805525`; there is no accessibility record in the repository. |
| BAR-302 | missing | Secret handling. The product has no account secret at `c805525`: `crates/chirp-types/src/api.rs` `LoginRequest { username }` carries no credential and `crates/chirp-server/src/repository/mod.rs` states there is "no password/credential step"; there is also no recovery flow (`src/api/router.rs`). The guarantee this criterion states — no surface returns/reversibly-stores a secret, recovery the only way back — cannot be realized because the credential mechanism it presumes is absent. |
| BAR-310 | partial | Session-credential transport + hygiene. Hygiene clause holds by inspection: the token travels as `Authorization: Bearer` (not in URLs) — `crates/chirp-frontend/src/api.rs` — is held only in the in-memory `session` signal (not `localStorage`/cookies) — `src/app.rs` — and is not written to logs (the `tower-http` `TraceLayer` in `crates/chirp-server/src/api/router.rs` does not log headers). Transport clause fails: `deploy/chirp/30-ingress.yaml` states "TLS: omitted deliberately" and serves plain HTTP with no HTTPS redirect, so the credential is not confined to an encrypted transport. |
| BAR-311 | missing | Private fields over encrypted transport. `deploy/chirp/30-ingress.yaml` omits TLS deliberately (plain HTTP, no redirect), so the one private field that exists at `c805525` — the session token — can cross the network in the clear; a clear-text request is served, not refused or redirected. (Account secret, verified contact, and export payload do not exist at this commit.) |
| BAR-326 | missing | Export excludes secrets. No data-export surface exists at `c805525` (`crates/chirp-server/src/api/router.rs` mounts no export route), so the stated exclusion (no credential, session data, or another person's contact in an export) cannot be verified against a real export. |
| BAR-331 | missing | Operator authority. No operator/administrative surface exists at `c805525`: `crates/chirp-server/src/api/router.rs` mounts only the ordinary user API, and `crates/chirp-server/src/api/auth.rs` resolves only ordinary bearer sessions. There is no provisioned-outside-sign-in administrative authority to inspect. |
| BAR-332 | missing | Operator action limits. No operator actions exist at `c805525` (no admin surface in `crates/chirp-server/src/api/router.rs`) and no recovery flow exists, so the guarantees (no operator action posts as a user or returns a credential; assisted recovery runs through the user's own contact) have no subject to inspect. |
| BAR-339 | partial | Data minimization. By inspection the collected set is minimal: `crates/chirp-types/src/api.rs` `CreateUserRequest` collects only `username`, `displayName`, and optional `bio`, each mapping to a legitimate function (identity, profile) with no superfluous field, and `src/domain.rs` `User` stores only these plus system-maintained id/timestamp/counts. But the product publishes no data-use/field-function statement at `c805525` (`design/` empty), and the authentication/recovery-contact functions the design names collect no field yet, so the "maps to a stated function" framing is satisfied only by reading the field semantics, not a stated mapping. |
| BAR-408 | missing | Backup-retention bound. No backups exist at `c805525` (the store is in-memory; `deploy/chirp/10-deployment.yaml` runs one replica with no DB/PVC) and no artifact states a maximum backup-retention bound. |
| BAR-412 | missing | Retention/deletion posture published. No data-retention-and-deletion posture is published at `c805525`: `design/` is empty and no README/`deploy/` artifact names live-account retention, deleted-account retention, a backup bound, or session/private-data handling. |
| BAR-421 | missing | Backup retention period. No backups and no stated bounded retention period exist at `c805525` (in-memory store, no DB/PVC per `deploy/chirp/10-deployment.yaml`); there is no backup to be within or beyond a period. |
| BAR-423 | missing | Backup fault isolation. No backups exist at `c805525` and the only durable state is process memory (`deploy/chirp/10-deployment.yaml`, in-memory repository), so there is no retained backup held apart from a primary store to inspect. |
| BAR-424 | missing | RPO/RTO. No recovery-point or recovery-time objective is stated anywhere at `c805525` (`design/` empty; no operational-posture artifact names a bounded figure). |
| BAR-425 | missing | Restore procedure. No written restore procedure exists at `c805525`; `deploy/` documents container build/run and k3d reachability only, and names no restore-from-backup steps. |
| BAR-432 | missing | Backup-and-recovery posture published. No backup-and-recovery posture (cadence, retention, RPO/RTO, restore/rollback) is published at `c805525`; `design/` is empty and no `deploy/` artifact states it. |
| BAR-463 | partial | Structured logs. `crates/chirp-server/src/main.rs` installs `tracing-subscriber` with an `EnvFilter`, and `src/api/router.rs` adds a `tower-http` `TraceLayer`, so operational events are structured `tracing` events carrying named fields, level (severity), and target (category) — not free-form prose. But the installed subscriber is the default human-readable text `fmt()` (logfmt-style), not a declared machine format such as `.json()`, so machine parsing relies on text rather than a structured serialization. |
| BAR-465 | partial | No secrets in logs. By inspection no credential or session token is written to logs: `crates/chirp-server/src/error.rs` logs only a message for an internal error (never a token), and the `tower-http` `TraceLayer` (`src/api/router.rs`) does not log the `Authorization` header. No credential or verified contact exists to leak. But there is no audit trail at `c805525`, and the recovery and administrative exercises the criterion names do not exist, so the full guarantee across those surfaces is only partially demonstrable. |
| BAR-481 | missing | Incident ownership. No artifact at `c805525` states a role accountable for acknowledging and acting on an incident; `design/` is empty and no operational/incident document exists in the repository. |
| BAR-484 | missing | Status-surface content. No status surface, in-product outage notice, or maintenance-announcement mechanism exists at `c805525`, so there is no published status content to inspect for the absence of private data. |
| BAR-486 | missing | Availability target. No availability target (a specific figure over a stated window) is stated anywhere at `c805525`; `design/` is empty and no README/`deploy/` artifact names one. |

## Summary

35 `inspection` criteria measured, each once, against `Nousix-LLC/nswe-demo @ c805525`:

- **met (9)** — the module/contract structure and its declared properties: BAR-120, BAR-160, BAR-161, BAR-162,
  BAR-165, BAR-167, BAR-168, BAR-174, BAR-179. The four-crate product partition over the `ferric` framework
  layer, the single `chirp-types` wire contract, the one `ChirpRepository` persistence seam, server-authoritative
  counts, env-driven config, and one self-contained serving artifact are all present and declared in code/manifests.
- **partial (4)** — a property half-realized: BAR-310 (token hygiene met; transport encryption omitted),
  BAR-339 (fields minimal; no stated mapping), BAR-463 (structured `tracing` events; default text format, not
  JSON), BAR-465 (no secrets in logs by inspection; no audit trail / admin & recovery surfaces to complete the check).
- **missing (22)** — release-stage surfaces and stated/published postures absent at this commit: BAR-021, BAR-024,
  BAR-175, BAR-203, BAR-275, BAR-293, BAR-294, BAR-302, BAR-311, BAR-326, BAR-331, BAR-332, BAR-408, BAR-412,
  BAR-421, BAR-423, BAR-424, BAR-425, BAR-432, BAR-481, BAR-484, BAR-486. These cover deletion/rules/export/operator/
  recovery surfaces, the accessibility statement and records, the backup/retention/RPO-RTO/restore posture, the
  incident/status/availability apparatus, and transport encryption — none stated or built at `c805525`.
- **not_applicable (0)**.

The verdicts are grounded in artifacts at `c805525` and reference the product only by repository identity, commit
SHA, and repo-relative paths.
