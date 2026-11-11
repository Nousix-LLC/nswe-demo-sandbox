# Account management & lifecycle — live measurement (`manual_user_check`)

**Cluster**: `SUBTASK_account_lifecycle` (20 `BAR-*`, `verification_method: manual_user_check`)
**Product under test**: `Nousix-LLC/nswe-demo`, commit `c805525` — the running deployment and the
checked-out SPA/API source at the same commit.

## Access note

The live product was reached and exercised read-only for this measurement: a single throwaway account was
registered (`POST /api/users`), authenticated (`POST /api/sessions`), and used to probe the account-management
surfaces. Where the running UI is a compiled WASM single-page app whose rendered screens cannot be driven
headlessly in this environment, presence or absence of a surface was settled against the SPA/API source at
`c805525` — the server route table (`crates/chirp-server/src/api/router.rs`), the handler set
(`crates/chirp-server/src/api/handlers.rs`), the wire contract (`crates/chirp-types/src/api.rs`), and the
frontend route table and modules (`crates/chirp-frontend/src/app.rs` and `src/`). The two agree.

## What the product provides at `c805525` (shared finding)

The entire account surface at `c805525` is: register (`POST /api/users`), read a public profile
(`GET /api/users/{id}`), log in (`POST /api/sessions`, handle-only — no password or contact), post/reply
(`POST /api/chirps`), home timeline (`GET /api/timeline`), follow/unfollow, like/unlike, and `GET /healthz`.
The SPA renders three client routes — `/` (timeline), `/compose`, `/user/:id` (read-only profile) — behind a
two-item nav ("Timeline", "Compose"); every other path falls back to the index shell and the client router
renders "Not found". The `User` record is `id, username, displayName, bio, createdAt, followerCount,
followingCount` — there is no contact/email field and no verification status. There is **no** settings hub, **no**
edit-profile or any profile-update endpoint (`PUT`/`PATCH /api/users/{id}` return 405), **no** account-&-contact
screen, **no** sessions/devices management (`GET`/`DELETE /api/sessions` return 405; the login token is a trivial
opaque string with no server-side session registry to list or revoke), **no** data export (`/api/export`,
`/api/users/{id}/export` fall through to the SPA shell), **no** account deletion (`DELETE /api/users/{id}` returns
405), and **no** stated data-rights baseline. The only destructive-looking actions are the idempotent
unfollow/unlike toggles; there is no delete-chirp, block, mute, end-session, or delete-account action, and so no
confirmation surface for any of them.

Each surface this cluster measures is in the release scope (the release bar lists Settings, Data export, Account
deletion, Sessions & devices, and the data-rights posture as in-scope/releasable), so its absence is a grounded
`missing` — not `not_applicable`. None is judged `partial`, because none of the required behaviour is present.

## Verdict table

| bar_id | live_status | observation |
|--------|-------------|-------------|
| BAR-018 | missing | No settings surface exists. The signed-in product offers no screen to view or update a contact (the `User` model has no contact field) and none to view or end sessions/devices (`GET`/`DELETE /api/sessions` → 405; no session registry in `crates/chirp-server/src/api`). Client route `/settings` falls back to the index shell → "Not found". |
| BAR-019 | missing | No self-service data export. `GET /api/export` and `GET /api/users/{id}/export` fall through to the SPA shell (no handler); no export route or module in the frontend (`crates/chirp-frontend/src/`). A signed-in person cannot obtain their chirps/profile/follow list in a portable form through the product. |
| BAR-022 | missing | No account-deletion surface exists, so no deletion confirmation — and therefore no confirmation that explains what survives, points to export, or treats cancel as a no-op. `DELETE /api/users/{id}` → 405; `/delete` client route → index shell → "Not found". |
| BAR-118 | missing | The product states no deletion outcome and provides no deletion. `DELETE /api/users/{id}` → 405; there is no delete handler in `handlers.rs` and no deletion type in `chirp-types/src/api.rs`. Deletion behaviour (sign-in blocked, dangling references) cannot occur because the surface is absent — consistent with the release-bar note that deletion is not provided at `c805525`. |
| BAR-119 | missing | No self-service export, confirmed live (`/api/users/{id}/export` → SPA shell) and in source (no export handler/DTO). The data may be enumerable internally, but no surface lets a signed-in person obtain their profile, full chirps, and full follow set. |
| BAR-210 | missing | No destructive action presents a consequence-naming confirmation with cancel, because none of the enumerated destructive actions exists: no delete-account, delete-chirp, block/mute, or end-session (verified live by 405s and by the absence of any such handler/route). The only "confirm" in the frontend is a post-success toast in `compose.rs`, not a pre-action confirmation; unfollow/unlike are idempotent toggles, not confirmed destructive actions. |
| BAR-214 | missing | No single settings area with labelled sub-sections (edit profile, account & contact, notification preferences, sessions & devices, blocked & muted, export, delete) and no per-section URLs — the SPA has only `/`, `/compose`, `/user/:id`. No rules/terms entry and no help & support entry are reachable from either the signed-out or signed-in shell (nav is "Timeline"/"Compose" only; no such routes in `app.rs`). |
| BAR-228 | missing | Delete-a-chirp, block-an-account, and delete-account do not exist at `c805525`, so none presents the required confirmation (consequence named, plain cancel, nothing changes on cancel; deletion additionally stating retention and pointing to export). No delete-chirp/block/delete-account handler or route in source; nothing to exercise live. |
| BAR-249 | missing | No edit-profile surface. It cannot be reached from a settings hub (none exists) or from the profile view (`profile.rs` renders a read-only public profile with no edit action), and there is no update endpoint — `PUT`/`PATCH /api/users/{id}` → 405. Display name and bio are set only at registration (`CreateUserRequest`) and cannot be changed afterward, so the field-level validation / failed-save-preserves / success-confirmation behaviour has no screen to occur on. |
| BAR-250 | missing | No settings screen with labelled section rows exists; `/settings` → index shell → "Not found". None of the named sections (edit profile, account & contact, sessions & devices, blocked & muted, export, delete) is present, so there are no rows, no per-section URLs, no destructive delete row opening a confirmation, and no account-summary fallback behaviour to observe. |
| BAR-251 | missing | No account-&-contact screen. The `User` record carries no contact and no "Verified"/"Not verified yet" status, and there is no endpoint to view or change a contact (`/api/users/{id}/contact` → SPA shell). The change-and-confirm flow, the unverified-as-caution treatment, and the failed-save-preserves-value behaviour have no surface. |
| BAR-254 | missing | No export screen. There is no route presenting export contents and a request action, no preparing state, and no download — `/api/export` and the `/settings/export` client route resolve to the index shell. A signed-in person cannot request or download an export of their data. |
| BAR-317 | missing | A signed-in person cannot change their display name or bio: there is no edit UI and no update endpoint (`PUT`/`PATCH /api/users/{id}` → 405). Values are fixed at registration; the persist-and-show-on-profile and invalid-value-field-error behaviours cannot be exercised because the change capability is absent. |
| BAR-318 | missing | There is no single settings surface reachable from the product's navigation. The nav exposes only "Timeline" and "Compose"; `/settings` → index shell → "Not found". Nothing presents the verified contact, active sessions/devices, or notification preferences (none of which exist in the product). |
| BAR-319 | missing | No settings surface and no contact model, so a person cannot view a current verified contact or enter a new one, and there is no confirmation step governing when a new contact becomes the recovery/notification basis. Verified live (`/api/users/{id}/contact` → SPA shell) and in source (no contact field/endpoint). |
| BAR-325 | missing | No self-service data-access/export surface. A signed-in person cannot obtain their own chirps, profile, and follow list in a portable form without an operator, because the export surface does not exist (`/api/export`, `/api/users/{id}/export` → SPA shell; no export handler/DTO/route). The "only the requester's data" constraint has no export to apply to. |
| BAR-327 | missing | No account self-deletion. `DELETE /api/users/{id}` → 405 and no delete route in the SPA, so there is no confirmation explaining what survives and pointing to export, no cancel-leaves-intact behaviour, and no post-deletion sign-in-blocked state to observe. (The throwaway test account could not be removed afterward for this reason — itself confirming the absence.) |
| BAR-328 | missing | Deletion does not exist, so its stated outcome cannot be applied or observed: no chirps-leave-public-view, no "chirp unavailable" placeholder for replies to a deleted chirp with adjusted counts, and no handle-retirement behaviour. No deletion handler/route in source; `DELETE /api/users/{id}` → 405 live. |
| BAR-330 | missing | The product states no data-rights baseline anywhere a person can find it, and the two mechanisms it would be satisfied through — a portable copy (export) and erasure (account deletion) — are both absent (export → SPA shell; delete → 405). No part of access/portability/erasure is satisfied through the account's own surfaces. |
| BAR-411 | missing | There is no self-service export, so the "retained data equals exported data" equality has no export side to compare: a signed-in account's profile, complete chirps, and complete followed accounts cannot be exported at all (`/api/users/{id}/export` → SPA shell; no export handler/DTO). The retained categories are therefore entirely absent from what a person can export. |
