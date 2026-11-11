# Release bar — Domain & application area (`BAR-100..199`)

This fragment holds the release-bar criteria for the domain & application design
(`design/domain-application-design.md`, `REQ-DOM-*`). Each `BAR-*` is a checkable release
condition — something a person who was not in the room can test against the live product (or,
where the condition is structural, inspect in the repository `Nousix-LLC/nswe-demo @ c805525`).
A `BAR-*` enforces the requirements it references; it does not restate them, and it does not say
how to build anything. One `BAR-*` may enforce several related `REQ-DOM-*`.

- **Range owned:** `BAR-100 .. BAR-199` (domain area). 60 criteria minted: `BAR-100..120`,
  `BAR-130..148`, `BAR-160..179`.
- **Verification methods** are drawn from the frozen vocabulary: `manual_user_check`,
  `automated_test`, `inspection`, `operational_check`.
- **`proposed_stage`** is this spoke's proposal from the domain view (`usable_early` |
  `releasable`). The synthesis hub owns the one cross-cutting MVP line and may move a criterion
  between stages for whole-design coherence; the stage recorded in `release-bar.md` is
  authoritative.
- **The headline release blocker** this area carries is durable persistence: the store at
  `c805525` is in-memory and loses everything on restart. `BAR-130` and `BAR-143`/`BAR-144`
  are the criteria that close it.

---

## Release bar criteria

### Accounts, handles, and profile

#### BAR-100 — A registered person has exactly one account with the public profile fields
- **statement**: Registering a person yields exactly one account carrying an opaque id, a handle, a display name, an optional bio (absent and empty-string are distinguishable), a creation time, and follower/following counts; no second "profile" entity exists, and that single entity is both the public profile others see and the account its holder manages.
- **references**: REQ-DOM-001, REQ-DOM-004, REQ-DOM-005
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-101 — Handles are well-formed and unique
- **statement**: A handle of 1–15 characters, each an ASCII letter, digit, or underscore, is accepted; an empty, over-length, or otherwise invalid handle is refused against the handle field; and registering a handle already in use is refused as a conflict, so at most one account holds any handle.
- **references**: REQ-DOM-002, REQ-DOM-003
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-102 — Entity ids are opaque and server-assigned
- **statement**: Account ids and chirp ids are assigned by the product and are opaque to clients; no create surface accepts a client-supplied id, and a client only echoes back an id the product issued.
- **references**: REQ-DOM-006
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-103 — An assigned id is never reused
- **statement**: Once assigned to an entity, an account id or chirp id is never later observed on a different entity, including after the original entity is deleted.
- **references**: REQ-DOM-007
- **verification_method**: automated_test
- **proposed_stage**: usable_early

#### BAR-104 — Creation times are UTC, immutable, and totally ordered
- **statement**: Every account and chirp carries a creation time in UTC epoch-milliseconds that does not change after creation, and two entities created in sequence carry times whose order matches the order they were created, so timestamps are directly comparable for ordering such as the newest-first timeline.
- **references**: REQ-DOM-008, REQ-DOM-039
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-105 — Profile edits apply; id and creation time do not change
- **statement**: A signed-in holder can change their display name and bio and see the change on the next view, and no product surface ever changes an account's id or creation time.
- **references**: REQ-DOM-009
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### Chirps, authorship, and replies

#### BAR-106 — A chirp is a bounded post with one existing author, immutable once posted
- **statement**: Posting a chirp of 1–280 characters (counted by Unicode scalar value) attributed to the signed-in account yields a chirp carrying an id, that author, the body as written, a creation time, a like count of zero, and no reply target; an empty or over-length body is refused and no chirp is created; and after posting, the chirp's body and author never change.
- **references**: REQ-DOM-011, REQ-DOM-012, REQ-DOM-013, REQ-DOM-014
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-107 — A reply records an existing target chirp
- **statement**: A reply records the id of exactly one chirp that exists at reply time; replying to a chirp id that does not exist or has been removed is refused as not-found, and no reply is created with a dangling target.
- **references**: REQ-DOM-015
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### The social graph (follow)

#### BAR-108 — Following is directed, self-free, idempotent, and reversible
- **statement**: A follow is recorded in one direction from one existing account to another; following one's own account is refused; following an account already followed changes nothing and does not duplicate the edge or double a count; and unfollowing removes the edge so the followee's chirps no longer enter the follower's timeline (unfollowing an account not followed changes nothing).
- **references**: REQ-DOM-017, REQ-DOM-018, REQ-DOM-019, REQ-DOM-020
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-109 — Follower and following counts equal the edges
- **statement**: An account's follower count equals the number of accounts currently following it and its following count equals the number it currently follows; one follow raises the count by exactly one and an unfollow returns it.
- **references**: REQ-DOM-021
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### Engagement (like)

#### BAR-110 — A like is at most one per account and chirp, and the like count equals the likes
- **statement**: Liking a chirp records one like from the account to that existing chirp; liking a chirp already liked changes nothing and does not add a second like; unliking removes it; and the chirp's like count equals the number of distinct accounts that currently like it, moving by exactly one on a like or unlike.
- **references**: REQ-DOM-022, REQ-DOM-023, REQ-DOM-024
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### The timeline

#### BAR-111 — The home timeline is the derived, newest-first, paged view of self plus followed accounts
- **statement**: A viewer's home timeline contains the viewer's own chirps and the chirps of every account the viewer currently follows and no others; it is ordered newest-first; it is returned a bounded page at a time with an opaque continuation cursor when more remain (a client cannot force every chirp into one response); and because it is derived, following or unfollowing an account changes what the next read returns with no stale materialized timeline.
- **references**: REQ-DOM-025, REQ-DOM-026, REQ-DOM-027, REQ-DOM-028
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### Sessions

#### BAR-112 — A session authenticates as exactly one account and is carried as an opaque token
- **statement**: A session authenticates requests as exactly one account, and every action taken under it is attributed to that account and no other; the session is presented as an opaque bearer token whose internal structure no client surface interprets.
- **references**: REQ-DOM-029, REQ-DOM-032
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-113 — A session can be ended and does not live forever
- **statement**: A signed-in person can end their session (sign out) after which a request carrying that session's token is refused, and a session presented after its bounded lifetime has elapsed is refused and the person is returned to sign-in. Sign-out that invalidates the session is a release surface the product does not provide at `c805525`.
- **references**: REQ-DOM-030, REQ-DOM-031
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### Account-associated identity data

#### BAR-114 — An account has an authentication credential distinct from its handle
- **statement**: Each account has an associated authentication credential the holder proves themselves with, distinct from the handle, so that knowing only an account's handle never establishes a session for it; the credential value is never returned in any profile or public response.
- **references**: REQ-DOM-033
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-115 — An account has a verified point of contact for recovery
- **statement**: Each account has an associated point of contact the product treats as verified before relying on it for account recovery; that contact value is never returned to another account or in a public response. A verified contact and the recovery it supports are a release surface the product does not provide at `c805525`.
- **references**: REQ-DOM-034
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

#### BAR-116 — Private account data is never exposed to others
- **statement**: An account's credential, verified contact, and session data never appear in any public response or in another account's view; a profile fetched with no session or with a different account's session returns only the handle, display name, bio, follower/following counts, and public chirps.
- **references**: REQ-DOM-035
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### Integrity, deletion, and a person's own data

#### BAR-117 — Every reference resolves; no dangling reference is observable
- **statement**: Through every product surface that creates a relationship, a chirp's author, a reply's target, a follow's two endpoints, and a like's account and chirp all name entities that exist or the action is refused; no surface produces a chirp, follow, reply, or like that names a nonexistent entity.
- **references**: REQ-DOM-036
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-118 — Account deletion has a single defined, applied outcome with no dangling reference
- **statement**: The product states a single deletion outcome — what becomes of the account's chirps (including those others replied to or liked), its follow edges, and its likes, and whether its freed handle may be re-registered — and deleting an account applies exactly that outcome: the account can no longer sign in, the product's state matches the stated outcome, and no remaining entity references the deleted account in a way the outcome did not define. Account deletion is a release surface the product does not provide at `c805525`.
- **references**: REQ-DOM-037
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

#### BAR-119 — A person can obtain their own data in a portable form
- **statement**: A signed-in person can obtain their own data — their profile, the full set of their chirps, and the full set of accounts they follow — because that data is enumerable per account. A self-service export is a release surface the product does not provide at `c805525`.
- **references**: REQ-DOM-038
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

#### BAR-120 — Server-maintained counts are never accepted as client input
- **statement**: An account's follower and following counts and a chirp's like count are maintained by the product and are never honored as client input; a create or update request carrying such a count has no effect on the stored value.
- **references**: REQ-DOM-040
- **verification_method**: inspection
- **proposed_stage**: usable_early

### Persistence — what must survive a restart (the durability gate)

#### BAR-130 — The product's user state survives restart, update, and redeploy
- **statement**: On a running deployment, an account created with chirps, follows, and likes is still present and unchanged — account, chirps, follows, likes, and active session — after the serving process is restarted and, separately, after it is redeployed; a person's content is intact on their next visit. This closes the `c805525` release blocker: the in-memory store loses everything on restart.
- **references**: REQ-DOM-100
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-131 — Accounts persist in full across a restart
- **statement**: After a restart, an account reads back with the same id, handle, display name, bio (preserved as given, absent or present), and creation time, and its follower/following counts are unchanged; an account registered with no bio still reads back with its bio absent rather than an empty string.
- **references**: REQ-DOM-101
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-132 — Account private identity data persists durably and stays non-public across a restart
- **statement**: An account's credential and verified contact persist across a restart so the holder can still sign in and still recover their account afterward, and that data never appears in any public response before or after the restart.
- **references**: REQ-DOM-102
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-133 — Chirps persist in full across a restart
- **statement**: After a restart, each chirp reads back with the same id, author, body text, and creation time; a reply still records the id of the chirp it answers; and like counts are unchanged.
- **references**: REQ-DOM-103
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-134 — The follow graph persists across a restart
- **statement**: After a restart, every follow edge is still recorded in the same direction, the followee's chirps still enter the follower's timeline, and both accounts' follower/following counts are unchanged.
- **references**: REQ-DOM-104
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-135 — Likes persist across a restart
- **statement**: After a restart, each like is still recorded from the same account to the same chirp and the chirp's like count is unchanged.
- **references**: REQ-DOM-105
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-136 — Active sessions survive a restart; ended sessions stay ended
- **statement**: A session obtained before a restart is still accepted afterward and still acts as the same account, so a redeploy does not silently sign a person out; a session that was ended (signed out) or has passed its lifetime is refused after a restart and is never revived by one.
- **references**: REQ-DOM-106
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-137 — Server-maintained counts are correct after a restart
- **statement**: After a restart, each account's follower and following counts equal its current follow edges and each chirp's like count equals the distinct accounts that currently like it; a follow or like added or removed after the restart moves the relevant count by exactly one.
- **references**: REQ-DOM-107
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-138 — The timeline is reconstructable from durable data after a restart
- **statement**: A timeline noted before a restart returns the same chirps in the same newest-first order after the restart with no further writes, reconstructed from the durable chirps and the durable follow graph; no separately stored timeline is required.
- **references**: REQ-DOM-108
- **verification_method**: operational_check
- **proposed_stage**: releasable

### Persistence — durability as a correctness property

#### BAR-139 — An acknowledged write is durable before it is acknowledged
- **statement**: A write the product confirms to a person — posting a chirp, following or unfollowing, liking or unliking, editing a profile, deleting an account — is present after a restart that occurs immediately after the acknowledgement, with no further action in between.
- **references**: REQ-DOM-109
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-140 — Referential integrity holds across restart and restore
- **statement**: After a restart and, separately, after a restore from backup, traversing chirps, replies, follows, and likes resolves every referenced account and chirp; no stopping, restarting, or recovering of the product introduces a reference to an entity that is absent.
- **references**: REQ-DOM-110
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-141 — Ids stay unique and are never reused across a restart
- **statement**: After a restart, ids already issued are never reassigned to a different entity and id generation does not reset to a point that collides with existing ids; accounts and chirps created after the restart carry ids that collide with none recorded before it, and no existing entity's id has changed.
- **references**: REQ-DOM-111
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-142 — An applied account deletion is durable and never half-applied
- **statement**: Once applied, an account deletion's stated outcome survives a restart (the account still cannot sign in, the stated outcome still holds, the freed-handle policy still holds), and a restart during a deletion leaves the product with the deletion either fully applied or not applied — never a partially deleted account with dangling references.
- **references**: REQ-DOM-112
- **verification_method**: operational_check
- **proposed_stage**: releasable

### Persistence — where state lives

#### BAR-143 — Authoritative state lives in a durable store distinct from the serving process
- **statement**: Replacing the serving process entirely — rolling it to a fresh instance with no shared memory — without touching the data store leaves all accounts, chirps, follows, likes, and active sessions intact afterward, demonstrating that the authoritative state did not live in the replaced process.
- **references**: REQ-DOM-113
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-144 — The persistence seam is backed by a durable store, closing the in-memory blocker
- **statement**: The persistence seam the product reads and writes through (the `ChirpRepository` boundary in `chirp-server`, or its equivalent) is backed by a durable store rather than process memory on the released product, confirmed by the product's state surviving a restart. The in-memory backing at `Nousix-LLC/nswe-demo @ c805525` is the named release blocker this closes; the store engine, schema, and migrations are deferred to the code work and are not fixed here.
- **references**: REQ-DOM-114
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-145 — Readiness reflects durable-store availability
- **statement**: The product reports ready to serve only when its durable store is reachable: queried while the store is unreachable to the serving process it reports not-ready, and queried while the store is reachable and the product can serve it reports ready.
- **references**: REQ-DOM-115
- **verification_method**: operational_check
- **proposed_stage**: releasable

### Persistence — backup, recovery, and a person's own copy

#### BAR-146 — Durable data can be backed up and restored intact
- **statement**: A backup produced from a populated deployment can be restored, and on the restored store the accounts, chirps, follows, and likes are present and satisfy every model invariant — references resolve, ids are unchanged, counts equal the edges.
- **references**: REQ-DOM-116
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-147 — Durable data is enumerable per account for export
- **statement**: For a signed-in account, the product can produce that account's profile, its complete set of chirps, and its complete set of followed accounts, matching the committed durable state at the time of the request.
- **references**: REQ-DOM-117
- **verification_method**: operational_check
- **proposed_stage**: releasable

### Persistence — change over time

#### BAR-148 — Upgrading the product preserves existing durable data
- **statement**: After an upgrade that changes the shape of the data (a redeploy with a data-model change), the accounts, chirps, follows, and likes that existed before the upgrade are all present afterward and their references still resolve.
- **references**: REQ-DOM-118
- **verification_method**: operational_check
- **proposed_stage**: releasable

### Modules — the four-crate decomposition

#### BAR-160 — The product is the four-crate, two-layer partition with every responsibility assigned once
- **statement**: The product is exactly a client-side framework layer (`ferric` with `ferric-http` and `ferric-router`) and a product layer of three crates (`chirp-types`, `chirp-server`, `chirp-frontend`), with no fifth product crate silently carrying responsibility, and for every entity its wire shape, its lifecycle and persistence, and its presentation each resolve to exactly one part (no entity owned by two parts, none owned by the frontend).
- **references**: REQ-DOM-200, REQ-DOM-208
- **verification_method**: inspection
- **proposed_stage**: usable_early

#### BAR-161 — `ferric` carries no chirp domain knowledge and the dependency direction is one-way
- **statement**: The `ferric` crates reference no chirp entity (account, chirp, follow, like, timeline, session) and do not depend on `chirp-types`; `chirp-frontend` depends on the `ferric` crates and never the reverse.
- **references**: REQ-DOM-201
- **verification_method**: inspection
- **proposed_stage**: usable_early

#### BAR-162 — `chirp-types` is the single source of truth for everything crossing the wire
- **statement**: Every identifier, domain entity and value object, request/response shape, pagination envelope, session token, and error contract that crosses between frontend and backend is defined once in `chirp-types`; the crate carries no I/O, framework, or async dependency, so both the native backend and the WebAssembly frontend compile against the identical definitions, and no wire shape is defined anywhere else.
- **references**: REQ-DOM-202
- **verification_method**: inspection
- **proposed_stage**: usable_early

#### BAR-163 — `chirp-server` owns the REST backend and enforces the domain invariants
- **statement**: Against the running product, actions that would violate a domain invariant (following oneself, liking a chirp twice, posting as a nonexistent account) are refused with a categorized error and no violating state is stored; `chirp-server` is the authority that enforces these invariants.
- **references**: REQ-DOM-203
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-164 — Domain rules are enforced on the server, not trusted from the client
- **statement**: Submitting directly to the API, bypassing the frontend, a chirp over the length limit, a self-follow, and a chirp attributed to a nonexistent account is refused by the server regardless of any client-side checking.
- **references**: REQ-DOM-207
- **verification_method**: automated_test
- **proposed_stage**: usable_early

#### BAR-165 — All durable state flows through one replaceable persistence boundary
- **statement**: A single `ChirpRepository` boundary in `chirp-server` mediates every durable operation and enumerates exactly the durable operations the product uses; no handler or frontend code reaches around it to the store, and a durable store added as a second implementation requires no change to any handler.
- **references**: REQ-DOM-204, REQ-DOM-223
- **verification_method**: inspection
- **proposed_stage**: usable_early

#### BAR-166 — One process serves the API, the app, and the health endpoint
- **statement**: From one address, the running service serves the REST API, loads the single-page app, and answers the health endpoint; no second process or second deployable is required to serve the app.
- **references**: REQ-DOM-205
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-167 — The frontend holds only session state and no durable state
- **statement**: The only state `chirp-frontend` owns across views is the current session (the authenticated account and its bearer token); every account, chirp, follow, like, and timeline it shows is fetched from the backend through the typed API client, and reloading the app re-fetches state so no entity data persists only in the client.
- **references**: REQ-DOM-206
- **verification_method**: inspection
- **proposed_stage**: usable_early

### Modules — the REST contract (frontend↔server seam)

#### BAR-168 — There is exactly one typed client↔server contract
- **statement**: The frontend and server build requests and decode responses from the same `chirp-types` definitions, with no second, hand-maintained copy of any wire shape on either side.
- **references**: REQ-DOM-215
- **verification_method**: inspection
- **proposed_stage**: usable_early

#### BAR-169 — The API is namespaced and same-origin with the app
- **statement**: The REST surface lives under a reserved path prefix reached on the same origin that served the app, so no cross-origin configuration is part of normal operation; a path that is not an API path resolves to the single-page app rather than an API handler.
- **references**: REQ-DOM-216
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-170 — The contract covers the core-loop operations the app depends on
- **statement**: Create an account, fetch an account's public profile, open a session, post a chirp (including a reply), read a timeline, follow and unfollow an account, and like and unlike a chirp are each served end to end from the app and each has a defined request and response type in the contract.
- **references**: REQ-DOM-217
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-171 — Timeline reads cross the contract as bounded pages behind an opaque cursor
- **statement**: A timeline read over the API returns a bounded page with an opaque continuation cursor when more chirps remain, passing the cursor returns the next older page, and a requested size above the server's maximum is clamped so a client cannot pull every chirp in one response.
- **references**: REQ-DOM-218
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-172 — Authentication crosses as an opaque bearer token; private data never crosses outward
- **statement**: A signed-in request proves itself by presenting the session as an opaque bearer token the server issued, and only an account's public profile fields and public chirps cross the contract outward — credential, verified contact, and session data never appear in any response.
- **references**: REQ-DOM-219
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-173 — Errors cross the contract as a typed, machine-readable category
- **statement**: A failed request returns a typed error carrying a machine-readable category (for example validation, not-found, conflict, unauthorized, forbidden) the frontend can branch on — distinguishing, for instance, a taken handle from a malformed one — rather than an ad-hoc string.
- **references**: REQ-DOM-220
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-174 — The contract's wire conventions are stable and grow additively
- **statement**: JSON field names are stable regardless of internal renames, opaque identifiers and tokens serialize as their bare value, validated value objects reject invalid input on the way in, and error categories are machine-readable constants; the contract's public surface grows only by addition, and changing or removing an existing wire shape is out of bounds.
- **references**: REQ-DOM-221
- **verification_method**: inspection
- **proposed_stage**: usable_early

#### BAR-175 — New release surfaces extend the one contract, not a second API
- **statement**: Each new surface the release adopts — among them ending a session, editing a profile, account settings, recovery, data export, account deletion, reporting and blocking/muting, notifications, an operator/administrative surface, and a way to find accounts to follow — has its request/response types defined in `chirp-types` and its operations mounted under the one namespaced API alongside the existing ones, not in a separate contract or service.
- **references**: REQ-DOM-222
- **verification_method**: inspection
- **proposed_stage**: releasable

### Modules — delivery and entry points

#### BAR-176 — The app is served as static assets with a single-page fallback and owns its routing
- **statement**: `chirp-server` serves the frontend as static assets from a configurable root, a request to an in-app route reached directly loads the app and resolves that route client-side, and a request for an unknown path returns the app's entry document rather than a server error.
- **references**: REQ-DOM-224
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-177 — The product has one user entry point: a single web address
- **statement**: A person reaches the product at one web address that serves the single-page app, with nothing to install and no second place to go, and the in-app route set reaches the release's surfaces (sign-up, sign-in, recovery, settings, deletion, and the rest) rather than adding a separate app.
- **references**: REQ-DOM-225
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-178 — The health/readiness entry point reports readiness, not just liveness
- **statement**: An operator can query an unauthenticated health endpoint with no session; with the durable store made unavailable it reports not-ready, and with the service able to serve users it reports ready, so an orchestrator can tell "serving" from "merely running."
- **references**: REQ-DOM-226
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-179 — The service is configured from the environment and ships as one artifact
- **statement**: The service's network bind address and static-asset root are read from the environment with sensible defaults rather than hard-coded, and the product ships as one self-contained artifact serving both the API and the app that deploys to a fresh environment by setting configuration only, without editing source.
- **references**: REQ-DOM-227
- **verification_method**: inspection
- **proposed_stage**: usable_early

---

## Coverage note — every release-gating `REQ-DOM-*` and the `BAR-*` that covers it

The domain design marks 79 of its 81 `REQ-DOM-*` as `release_gating: true`. Every one is listed
below with the `BAR-*` that enforces it, so the synthesis gate can assert `GATING_REQ_COVERAGE`
for the domain area without re-deriving the gating set. The two non-gating requirements are
recorded at the end with the design's stated reason, so the whole set is accounted for.

### Domain model (`REQ-DOM-001..040`)

| Release-gating REQ-DOM | Covered by |
|------------------------|------------|
| REQ-DOM-001 | BAR-100 |
| REQ-DOM-002 | BAR-101 |
| REQ-DOM-003 | BAR-101 |
| REQ-DOM-004 | BAR-100 |
| REQ-DOM-005 | BAR-100 |
| REQ-DOM-006 | BAR-102 |
| REQ-DOM-007 | BAR-103 |
| REQ-DOM-008 | BAR-104 |
| REQ-DOM-009 | BAR-105 |
| REQ-DOM-011 | BAR-106 |
| REQ-DOM-012 | BAR-106 |
| REQ-DOM-013 | BAR-106 |
| REQ-DOM-014 | BAR-106 |
| REQ-DOM-015 | BAR-107 |
| REQ-DOM-017 | BAR-108 |
| REQ-DOM-018 | BAR-108 |
| REQ-DOM-019 | BAR-108 |
| REQ-DOM-020 | BAR-108 |
| REQ-DOM-021 | BAR-109 |
| REQ-DOM-022 | BAR-110 |
| REQ-DOM-023 | BAR-110 |
| REQ-DOM-024 | BAR-110 |
| REQ-DOM-025 | BAR-111 |
| REQ-DOM-026 | BAR-111 |
| REQ-DOM-027 | BAR-111 |
| REQ-DOM-028 | BAR-111 |
| REQ-DOM-029 | BAR-112 |
| REQ-DOM-030 | BAR-113 |
| REQ-DOM-031 | BAR-113 |
| REQ-DOM-032 | BAR-112 |
| REQ-DOM-033 | BAR-114 |
| REQ-DOM-034 | BAR-115 |
| REQ-DOM-035 | BAR-116 |
| REQ-DOM-036 | BAR-117 |
| REQ-DOM-037 | BAR-118 |
| REQ-DOM-038 | BAR-119 |
| REQ-DOM-039 | BAR-104 |
| REQ-DOM-040 | BAR-120 |

### Persistence (`REQ-DOM-100..118`)

| Release-gating REQ-DOM | Covered by |
|------------------------|------------|
| REQ-DOM-100 | BAR-130 |
| REQ-DOM-101 | BAR-131 |
| REQ-DOM-102 | BAR-132 |
| REQ-DOM-103 | BAR-133 |
| REQ-DOM-104 | BAR-134 |
| REQ-DOM-105 | BAR-135 |
| REQ-DOM-106 | BAR-136 |
| REQ-DOM-107 | BAR-137 |
| REQ-DOM-108 | BAR-138 |
| REQ-DOM-109 | BAR-139 |
| REQ-DOM-110 | BAR-140 |
| REQ-DOM-111 | BAR-141 |
| REQ-DOM-112 | BAR-142 |
| REQ-DOM-113 | BAR-143 |
| REQ-DOM-114 | BAR-144 |
| REQ-DOM-115 | BAR-145 |
| REQ-DOM-116 | BAR-146 |
| REQ-DOM-117 | BAR-147 |
| REQ-DOM-118 | BAR-148 |

### Modules and interfaces (`REQ-DOM-200..227`)

| Release-gating REQ-DOM | Covered by |
|------------------------|------------|
| REQ-DOM-200 | BAR-160 |
| REQ-DOM-201 | BAR-161 |
| REQ-DOM-202 | BAR-162 |
| REQ-DOM-203 | BAR-163 |
| REQ-DOM-204 | BAR-165 |
| REQ-DOM-205 | BAR-166 |
| REQ-DOM-206 | BAR-167 |
| REQ-DOM-207 | BAR-164 |
| REQ-DOM-208 | BAR-160 |
| REQ-DOM-215 | BAR-168 |
| REQ-DOM-216 | BAR-169 |
| REQ-DOM-217 | BAR-170 |
| REQ-DOM-218 | BAR-171 |
| REQ-DOM-219 | BAR-172 |
| REQ-DOM-220 | BAR-173 |
| REQ-DOM-221 | BAR-174 |
| REQ-DOM-222 | BAR-175 |
| REQ-DOM-223 | BAR-165 |
| REQ-DOM-224 | BAR-176 |
| REQ-DOM-225 | BAR-177 |
| REQ-DOM-226 | BAR-178 |
| REQ-DOM-227 | BAR-179 |

### Non-gating domain requirements (recorded, not covered by a `BAR-*`)

| REQ-DOM | `release_gating` | Reason it carries no bar criterion |
|---------|------------------|-------------------------------------|
| REQ-DOM-010 | false | Handle-change policy: a stated-policy-and-consistency requirement, not a v1 release blocker (per the design). |
| REQ-DOM-016 | false | Reading a reply in conversation context: an enhancement over the recorded reply linkage, not release-gating (per the design). |

### Coverage summary

- Release-gating `REQ-DOM-*`: **79** — all referenced by ≥1 `BAR-*`.
- `BAR-*` minted (all within `BAR-100..199`): **60** — `BAR-100..120`, `BAR-130..148`, `BAR-160..179`.
- Non-gating `REQ-DOM-*`: 2 (`REQ-DOM-010`, `REQ-DOM-016`) — recorded above, no bar criterion required.
- Every `BAR-*` above names a `verification_method` from the frozen vocabulary, references ≥1 `REQ-DOM-*`, and carries a `proposed_stage`.
- Proposed staging from the domain view: `usable_early` for the core loop and domain correctness (`BAR-100..112`, `BAR-114`, `BAR-116..117`, `BAR-120`) and the structural architecture (`BAR-160..174`, `BAR-176..177`, `BAR-179`); `releasable` for the durability gate (`BAR-130..148`), the account-lifecycle surfaces not present at `c805525` (`BAR-113`, `BAR-115`, `BAR-118..119`), additive contract extension (`BAR-175`), and readiness (`BAR-178`). The synthesis hub owns the final cross-cutting MVP line.
