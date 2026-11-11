<!--
This file is the `domain_model` section of design/domain-application-design.md.
SUBTASK_synthesis assembles it, with the sibling parts, into the consolidated design file and folds
every REQ-DOM-* below into that file's requirements_and_acceptance_criteria register.
Owns: the `domain_model` section, the canonical entity vocabulary, and REQ-DOM-001..049.
Held to the chirp-types crate shapes and the current chirp-server domain at Nousix-LLC/nswe-demo @ c805525.
-->

# Domain model

## What this section fixes

This section states *what is true of chirp's domain* — the entities a reader and poster deals with,
how they relate, and the invariants that must hold — as requirements something can be built and
tested against. It says nothing about *how* the data is stored or served: persistence is the sibling
`persistence_requirement` section (`REQ-DOM-100..149`), and the division of the running system into
parts is the `modules_and_responsibilities` / `interfaces_and_entry_points` sections
(`REQ-DOM-200..249`). Where an engineering decision is tempting here — a schema, an index, a session
format — it is stated as a requirement on the model and the decision is left to the `software` domain's
later code work.

The model is held to what already exists in the repository at commit `c805525`: the shared
`crates/chirp-types` crate (the single source of truth for the types that cross the wire) and the
`crates/chirp-server` domain (the `ChirpRepository` seam and its in-memory backing). Every entity below
names the `chirp-types` type that already carries it, so the model refines the running product rather
than inventing a parallel one. Where the model requires something the product does not yet have (a
session a person can end, a defined outcome when an account is deleted), that is called out as a gap the
requirement closes, traced to the product requirement (`REQ-PROD-*`) it serves.

### Scope of this section

- **In this section**: the core social domain — accounts and their public profile, the handle, the
  chirp and its authorship, replies, the follow graph, likes, the timeline a reader sees, and the
  session that identifies a signed-in person — with their relationships and invariants.
- **Referenced, owned elsewhere**: the authentication *credential* and how a session is proven
  (identity/security design, `REQ-ID-*`); the *verified point of contact* mechanism and verification
  (identity/privacy, `REQ-ID-*`); safety entities — *report*, *block*, *mute* — and moderation
  (identity/abuse, `REQ-ID-*`); *notifications* (experience and product, `REQ-UX-*` / `REQ-PROD-029`);
  durability, backups, and limits (operational readiness, `REQ-OPS-*`). These are named in the entity
  vocabulary where the core model must reference them, so the picture is complete and persistence knows
  what account data exists, but their internals are not modelled here.
- **Not in the product** (recorded so the absence is a decision, not an oversight): **mentions** and
  mention-based notification. The product requirements settle rich social features beyond the core loop
  as out of scope (`product-requirements.md`, Part 5); replies (`REQ-PROD-003`) are the only
  chirp-to-chirp relationship the product carries, so the model defines replies and does **not**
  introduce a mention entity or a mention edge. If a later phase adopts mentions, it extends this
  vocabulary; it is absent today by decision.

---

## Entity vocabulary (canonical)

The rest of the design references entities **only** by the canonical names below — the persistence
requirement, the module and interface design, and the consolidated requirements all draw on this one
vocabulary. Anything that needs an entity this vocabulary does not name has found a gap to report, not
a licence to coin a new name.

| Canonical name | What it is | `chirp-types` type (at `c805525`) |
|---|---|---|
| **Account** (a.k.a. **User**) | A registered person: their identity, their public profile, and the account-level data an account-based product carries. "User" and "Account" name the same entity — *User* is the public/profile face, *Account* the owned-and-managed face. | `chirp_types::domain::User` |
| **Handle** | The unique, human-chosen identifier others know an account by and follow. | `chirp_types::domain::Username` |
| **Display name** | The free-form, non-unique name an account shows under. | `User::display_name` (field) |
| **Bio** | An optional short free-form profile description. | `User::bio` (field, `Option`) |
| **Chirp** | A single short public post, attributed to one authoring account. | `chirp_types::domain::Chirp` |
| **Chirp text** | The validated body of a chirp. | `chirp_types::domain::ChirpText` |
| **Reply** | A chirp that answers another chirp; the relationship, not a separate entity — a chirp whose *reply target* is set. | `Chirp::reply_to` (field, `Option<ChirpId>`) |
| **Follow** | A directed "follows" relationship from one account (the follower) to another (the followee). | `chirp_types::domain::Follow` |
| **Like** | A relationship recording that an account likes a chirp. | `chirp_types::domain::Like` |
| **Timeline** | The reverse-chronological run of chirps a viewer sees: their own chirps and those of the accounts they follow. A derived view, not stored state. | `chirp_types::domain::Timeline`, paged as `chirp_types::api::Page<Chirp>` |
| **Session** | A proof that a request is acting as a particular account, carried as an opaque bearer token. | `chirp_types::api::SessionToken`, issued in `AuthResponse` |
| **Account id / Chirp id** | Opaque, server-assigned identifiers for an account and a chirp. | `chirp_types::ids::UserId`, `chirp_types::ids::ChirpId` |
| **Timestamp** | A point in time on an entity (created-at), UTC. | `chirp_types::ids::Timestamp` |
| **Credential** *(referenced; owned by `REQ-ID-*`)* | The secret an account proves itself with at sign-in. Named so the model and persistence know account-secret data exists and must be protected; its structure and handling are the identity/security design's. | — (not in `chirp-types` at `c805525`) |
| **Verified contact** *(referenced; owned by `REQ-ID-*`)* | A confirmed point of contact for an account, the basis for recovery and important notifications. Named so persistence carries it as part of the account record; what contact is collected and how it is verified is the identity/privacy design's. | — (not in `chirp-types` at `c805525`) |

**Relationships at a glance.** An Account **authors** Chirps (one author per chirp; many chirps per
account). A Chirp **replies to** at most one other Chirp. An Account **follows** other Accounts (the
social graph: a set of directed Follow edges). An Account **likes** Chirps (a set of Like edges). A
Timeline is **derived** for a viewing Account from its own chirps plus the chirps of the accounts it
follows. A Session **belongs to** exactly one Account.

---

## The entities and their invariants

The requirements below (`REQ-DOM-001..049`) carry the detail; this prose states the model's spine so a
reader has the shape before the register.

**Accounts and identity.** An account is identified two ways: by an **opaque, server-assigned id**
that never changes and is never reused, and by a **handle** the person chooses, which is unique across
the product and well-formed (1–15 characters of ASCII letters, digits, or underscore — the
`Username` rule already enforced at `c805525`). An account carries a mutable display name and optional
bio, an immutable creation time, and server-maintained follower/following counts that clients read but
do not set. The account record also carries identity-area data — a credential and a verified contact —
whose internals the identity design owns but which the model acknowledges so they are persisted and
protected as part of the account.

**Chirps, authorship, and replies.** A chirp is a short public post with a validated body of 1–280
characters (the `ChirpText` rule at `c805525`), attributed to exactly one authoring account that must
exist. A chirp may be a **reply**, in which case it records the id of the chirp it answers, and that
target must exist when the reply is posted; a chirp that is not a reply records no target. The parent
linkage is what lets a reply be read in the context of its conversation. A posted chirp's body and
authorship are immutable; only its server-maintained like count and the existence of replies to it
change over time.

**The social graph.** Following is a set of directed edges: *follower → followee*. A person cannot
follow themselves, there is at most one edge per ordered pair (following is idempotent), and unfollowing
removes the edge idempotently. The follower/following counts on an account always equal the number of
edges into and out of it.

**Engagement.** A like is an edge *account → chirp*. There is at most one like per (account, chirp)
pair; liking is idempotent and unliking removes the like idempotently. A chirp's like count always
equals the number of distinct accounts that currently like it.

**The timeline.** A viewer's timeline is **derived**, not stored: it is the reverse-chronological
(newest-first) run of the viewer's own chirps and the chirps of the accounts the viewer currently
follows, returned a bounded page at a time behind an opaque cursor. Because it is derived from the
current follow graph and chirp set, it reflects follows and unfollows without any separate
materialized state the model must keep consistent.

**Sessions.** A session identifies the account a request acts as. From the person's side the model
requires three things of a session regardless of how authentication is built: it authenticates exactly
one account; it can be **ended** so it can no longer be used (sign-out, which the product does not
support at `c805525`); and it does not live forever. How a session is established and proven — the
credential exchange and the token's internals — is the identity/security design's (`REQ-ID-*`); the
`SessionToken` type already treats the token as opaque.

**Integrity across the model.** Every reference resolves: a chirp's author, a reply's target, a
follow's two endpoints, and a like's account and chirp all name entities that exist. This referential
integrity is what makes **account deletion** a domain question and not only a privacy one: the model
must define a consistent outcome for a deleted account's chirps, follows, likes, and whether its freed
handle may be registered again. The model fixes that a defined, applied outcome is required and that no
dangling reference may result; the specific policy (what is retained, whether the handle returns to the
pool) is settled with the identity/privacy design against `REQ-PROD-021`.

---

## Requirements and acceptance criteria (`REQ-DOM-001..049`)

Each requirement carries an `id`, a `statement` (what must be true), `acceptance_criteria` a person who
never met the author can check against the live product or the shared contract, a `release_gating` flag
(`true` when a releasable product depends on it), and `traces_to` the product requirement it refines
where one applies. Acceptance criteria that read "inspect `crates/chirp-types` …" are checkable by
inspection of the shared contract; the rest are checkable against the running product.

### Accounts, handles, and profile

#### REQ-DOM-001 — The account is the one entity for a registered person
- **statement**: A registered person is represented by exactly one account entity carrying an opaque id, a handle, a display name, an optional bio, a creation time, and follower/following counts; the same entity is the account's public profile (what others see) and the owned account (what its holder manages).
- **acceptance_criteria**: Register an account and fetch it; a single profile is returned carrying a handle, a display name, a bio field (possibly empty), a creation time, and follower/following counts. Inspect `crates/chirp-types/src/domain.rs`; `User` carries exactly these fields and no second "profile" type exists.
- **release_gating**: true
- **traces_to**: REQ-PROD-008

#### REQ-DOM-002 — Handles are well-formed
- **statement**: A handle is 1 to 15 characters, each an ASCII letter, digit, or underscore; anything else is rejected against the handle field.
- **acceptance_criteria**: Create an account with handle `alice_01`; it is accepted. Attempt handles that are empty, 16 characters, contain a space, or contain `!`; each is rejected with a field-level validation error naming the handle. Inspect `chirp_types::domain::Username`; `USERNAME_MAX_CHARS` is 15 and the rule matches.
- **release_gating**: true
- **traces_to**: REQ-PROD-009

#### REQ-DOM-003 — Handles are unique
- **statement**: At most one account exists for a given handle; registering a handle already in use is refused as a conflict.
- **acceptance_criteria**: Register handle `bob`; register `bob` again — the second attempt is refused as a conflict naming the handle, and only one account holds `bob`.
- **release_gating**: true
- **traces_to**: REQ-PROD-009

#### REQ-DOM-004 — An account has a display name
- **statement**: An account carries a free-form display name that need not be unique and is shown wherever the account is presented.
- **acceptance_criteria**: Register two accounts with the same display name and different handles; both are created, and each profile shows the display name given.
- **release_gating**: true

#### REQ-DOM-005 — Bio is optional
- **statement**: An account's bio is optional; an account with no bio is well-formed and its bio is explicitly absent, not an empty-string stand-in that cannot be told from "unset".
- **acceptance_criteria**: Register an account without a bio and fetch it; the bio is absent (null), distinguishable from an account whose bio is the empty string. Inspect `User::bio`; it is an `Option`.
- **release_gating**: true

#### REQ-DOM-006 — Account and chirp ids are opaque and server-assigned
- **statement**: Account ids and chirp ids are assigned by the product, are opaque to clients, and a client never supplies one on creation; a client only echoes back an id the product issued.
- **acceptance_criteria**: Register an account and post a chirp without supplying any id; the product assigns both ids. Inspect `chirp_types::ids`; `UserId`/`ChirpId` are server-minted newtypes and the create-request types (`CreateUserRequest`, `CreateChirpRequest`) carry no id field.
- **release_gating**: true

#### REQ-DOM-007 — Ids are never reused
- **statement**: Once assigned, an account id or chirp id is never reassigned to a different entity, including after the original entity is deleted.
- **acceptance_criteria**: Record an account's id; delete the account (per REQ-DOM-039); over the product's lifetime no other account is ever observed carrying that id.
- **release_gating**: true
- **traces_to**: REQ-PROD-020

#### REQ-DOM-008 — Creation time is recorded and immutable
- **statement**: Each account and each chirp records the UTC time it was created, and that time does not change after creation.
- **acceptance_criteria**: Fetch an account and a chirp; each carries a creation timestamp. Re-fetch later; the timestamp is unchanged. Inspect `chirp_types::ids::Timestamp`; it is epoch-milliseconds UTC.
- **release_gating**: true

#### REQ-DOM-009 — Display name and bio are editable; id and creation time are not
- **statement**: An account holder can change their display name and bio after sign-up; an account's id and creation time are immutable.
- **acceptance_criteria**: Signed in, change your display name and bio; the change shows on your profile on the next view. No product surface changes an account's id or creation time.
- **release_gating**: true
- **traces_to**: REQ-PROD-016

#### REQ-DOM-010 — Handle mutability follows the product's stated policy
- **statement**: Whether a handle may change after sign-up is governed by a single stated policy, and the model behaves consistently with it; if handles are fixed, no path changes one, and if a handle change is offered, the uniqueness and format invariants (REQ-DOM-002, REQ-DOM-003) continue to hold after the change and following relationships remain attached to the account, not to the old handle string.
- **acceptance_criteria**: Find the product's stated handle-change position. If fixed, confirm no surface changes a handle. If changes are offered, change a followed account's handle and confirm its followers still follow the account and the new handle is validated and unique.
- **release_gating**: false
- **traces_to**: REQ-PROD-018

### Chirps, authorship, and replies

#### REQ-DOM-011 — A chirp is a short post with one author
- **statement**: A chirp is a single public post carrying an opaque id, the id of exactly one authoring account that exists, a validated body, a creation time, a like count, and an optional reply target.
- **acceptance_criteria**: Post a chirp; it is returned with an id, your account as author, the body you wrote, a creation time, a like count of zero, and no reply target. Inspect `chirp_types::domain::Chirp`; it carries exactly these fields.
- **release_gating**: true
- **traces_to**: REQ-PROD-001

#### REQ-DOM-012 — Chirp body length is bounded
- **statement**: A chirp body is 1 to 280 characters, counted by Unicode scalar value (not bytes); an empty or over-length body is rejected and no chirp is created.
- **acceptance_criteria**: Post a 280-character body (including one of 280 multi-byte emoji); it is accepted. Post a 281-character or empty body; it is rejected against the body field and no chirp appears. Inspect `chirp_types::domain::ChirpText`; `CHIRP_TEXT_MAX_CHARS` is 280 and length is by character.
- **release_gating**: true
- **traces_to**: REQ-PROD-001

#### REQ-DOM-013 — Every chirp is attributed to an existing author
- **statement**: A chirp is always attributed to one account that exists at post time; a chirp with no author or an author that does not exist cannot be created.
- **acceptance_criteria**: Post a chirp while signed in; it is attributed to your account. There is no product path to post a chirp attributed to a nonexistent account.
- **release_gating**: true
- **traces_to**: REQ-PROD-001

#### REQ-DOM-014 — A posted chirp's body and author are immutable
- **statement**: After a chirp is posted, its body text and author do not change; only its server-maintained like count and whether other chirps reply to it change over time.
- **acceptance_criteria**: Post a chirp and re-fetch it over time; its body and author are unchanged. No product surface edits a chirp's text or reassigns its author.
- **release_gating**: true

#### REQ-DOM-015 — A reply records the chirp it answers, and that chirp must exist
- **statement**: A chirp may be a reply, in which case it records the id of exactly one existing chirp it answers; replying to a chirp that does not exist is refused as not-found rather than posted with a dangling target.
- **acceptance_criteria**: Reply to a visible chirp; the reply carries that chirp's id as its reply target. Attempt to reply to a nonexistent or removed chirp id; it is refused as not-found and no reply is created. Inspect `Chirp::reply_to`; it is `Option<ChirpId>`.
- **release_gating**: true
- **traces_to**: REQ-PROD-003

#### REQ-DOM-016 — The reply linkage supports reading a conversation
- **statement**: The reply target linkage is sufficient to move from a reply to the chirp it answers, so a conversation can be reconstructed from the model without any separate thread entity.
- **acceptance_criteria**: Given a reply, use its recorded reply target to fetch the parent chirp and present the two in relation. No entity beyond `Chirp` and its `reply_to` linkage is required to do so.
- **release_gating**: false
- **traces_to**: REQ-PROD-004

### The social graph (follow)

#### REQ-DOM-017 — Following is a directed relationship between two accounts
- **statement**: A follow is a directed relationship from a follower account to a followee account, both of which exist, recording when it was created.
- **acceptance_criteria**: Follow another account; the relationship is recorded from you to them. Inspect `chirp_types::domain::Follow`; it carries `follower_id`, `followee_id`, and a creation time.
- **release_gating**: true
- **traces_to**: REQ-PROD-006

#### REQ-DOM-018 — No account follows itself
- **statement**: An account cannot follow itself; a self-follow is refused.
- **acceptance_criteria**: Attempt to follow your own account; it is refused and no self-edge exists.
- **release_gating**: true
- **traces_to**: REQ-PROD-006

#### REQ-DOM-019 — Following is idempotent
- **statement**: At most one follow edge exists per ordered (follower, followee) pair; following an account already followed succeeds and changes nothing, and unfollowing an account not followed succeeds and changes nothing.
- **acceptance_criteria**: Follow an account twice; the second call succeeds and the follow is not duplicated and counts do not double. Unfollow an account you do not follow; it succeeds and nothing changes.
- **release_gating**: true
- **traces_to**: REQ-PROD-006

#### REQ-DOM-020 — Unfollowing removes the relationship
- **statement**: Unfollowing an account removes the follow edge so the followee's chirps no longer enter the follower's timeline.
- **acceptance_criteria**: Follow an account and see their chirps in your timeline; unfollow them; their chirps no longer appear in your timeline.
- **release_gating**: true
- **traces_to**: REQ-PROD-006

#### REQ-DOM-021 — Follower and following counts match the edges
- **statement**: An account's follower count equals the number of accounts currently following it, and its following count equals the number it currently follows; the counts are maintained by the product and are read-only to clients.
- **acceptance_criteria**: Note an account's follower count; have one account follow it; the follower count increases by exactly one. Unfollow; it returns. A client cannot set these counts directly (they are not inputs to any create/update request).
- **release_gating**: true

### Engagement (like)

#### REQ-DOM-022 — A like relates an account to a chirp
- **statement**: A like records that one account likes one chirp, both of which exist, and when the like was recorded.
- **acceptance_criteria**: Like a chirp; the like is recorded from your account to that chirp. Inspect `chirp_types::domain::Like`; it carries `user_id`, `chirp_id`, and a creation time.
- **release_gating**: true
- **traces_to**: REQ-PROD-005

#### REQ-DOM-023 — At most one like per account and chirp
- **statement**: There is at most one like for a given (account, chirp) pair; liking a chirp already liked succeeds and does not add a second like, and unliking a chirp not liked succeeds and changes nothing.
- **acceptance_criteria**: Like a chirp twice; the second call succeeds and the like count does not increase again. Unlike twice; the first returns the count, the second changes nothing.
- **release_gating**: true
- **traces_to**: REQ-PROD-005

#### REQ-DOM-024 — Like count matches the likes
- **statement**: A chirp's like count equals the number of distinct accounts that currently like it; it is maintained by the product and read-only to clients.
- **acceptance_criteria**: Note a chirp's like count; have one account like it; the count increases by exactly one. Unlike; it returns. A client cannot set the count directly.
- **release_gating**: true
- **traces_to**: REQ-PROD-005

### The timeline

#### REQ-DOM-025 — The timeline is derived from the viewer's own chirps and those they follow
- **statement**: A viewer's home timeline is the set of the viewer's own chirps together with the chirps of every account the viewer currently follows; it is a derived view, not stored state the model keeps separately.
- **acceptance_criteria**: Follow one account and post yourself; your timeline contains your chirps and theirs, and contains no chirps from accounts you neither are nor follow.
- **release_gating**: true
- **traces_to**: REQ-PROD-002

#### REQ-DOM-026 — The timeline is newest-first
- **statement**: Chirps in a timeline are ordered reverse-chronologically, newest first.
- **acceptance_criteria**: Post two chirps a moment apart; in the timeline the later one appears before the earlier one. Inspect `chirp_types::domain::Timeline`; its ordering invariant is reverse-chronological.
- **release_gating**: true
- **traces_to**: REQ-PROD-002

#### REQ-DOM-027 — The timeline is returned in bounded pages
- **statement**: A timeline is read a bounded page at a time, each page carrying an opaque continuation cursor when more chirps remain; a reader cannot force the product to return every chirp in one response.
- **acceptance_criteria**: Request a timeline; a bounded page is returned with a continuation cursor when more remain. Pass the cursor; the next, older page is returned. A page carries no more than the product's maximum, independent of any requested size. Inspect `chirp_types::api::Page` and `TimelineQuery`; the page carries `items` and an optional `next_cursor`, and the query's limit is optional.
- **release_gating**: true
- **traces_to**: REQ-PROD-002

#### REQ-DOM-028 — The timeline reflects the current follow graph
- **statement**: Because the timeline is derived, following or unfollowing an account changes what a subsequent timeline read returns, with no separate materialized timeline to reconcile.
- **acceptance_criteria**: Read your timeline; follow a new account that has posted; read again — their chirps now appear. Unfollow; read again — their chirps are gone.
- **release_gating**: true
- **traces_to**: REQ-PROD-002

### Sessions

#### REQ-DOM-029 — A session identifies exactly one account
- **statement**: A session authenticates requests as exactly one account; actions taken under a session are attributed to that account and no other.
- **acceptance_criteria**: Sign in and post, follow, and like; each action is attributed to the signed-in account. Inspect `chirp_types::api::AuthResponse`; a session is issued for one authenticated `User`.
- **release_gating**: true
- **traces_to**: REQ-PROD-010

#### REQ-DOM-030 — A session can be ended
- **statement**: A session can be ended so that it can no longer be used to act as the account — the model supports sign-out that invalidates the session, which the product does not provide at `c805525`.
- **acceptance_criteria**: Sign in, then end the session (sign out); replay a request with the ended session's token — it is refused. The account is no longer acted as under that session.
- **release_gating**: true
- **traces_to**: REQ-PROD-014

#### REQ-DOM-031 — A session does not live forever
- **statement**: A session has a bounded lifetime after which it no longer authenticates; the specific duration and renewal behavior are the identity/security design's to set.
- **acceptance_criteria**: A session presented after its lifetime has elapsed is refused and the person is returned to sign-in. (The exact lifetime is defined by `REQ-ID-*`; this requirement is that a lifetime exists and is enforced.)
- **release_gating**: true
- **traces_to**: REQ-PROD-015

#### REQ-DOM-032 — The session token is opaque
- **statement**: A session is carried as an opaque bearer token; its internal structure is not part of the domain contract and clients treat it as an opaque string to present, not to interpret.
- **acceptance_criteria**: Inspect `chirp_types::api::SessionToken`; it is a transparent string wrapper with no interpreted structure, and no client surface parses its contents. (How the token is formed and proven is the identity/security design's, `REQ-ID-*`.)
- **release_gating**: true

### Account-associated data owned by the identity area

#### REQ-DOM-033 — An account carries an authentication credential
- **statement**: An account has an associated authentication credential — a secret the holder proves themselves with — distinct from the handle, so that knowing a handle alone does not establish a session. The credential's structure and handling are the identity/security design's; the model requires that such data exists on the account and is never part of any public profile.
- **acceptance_criteria**: Knowing only another account's handle, attempt to obtain a session for it; it is refused (the handle is not the credential). A credential value is never returned in any profile or public response. (The credential mechanism is `REQ-ID-*`.)
- **release_gating**: true
- **traces_to**: REQ-PROD-008, REQ-PROD-010

#### REQ-DOM-034 — An account carries a verified point of contact
- **statement**: An account has an associated, confirmed point of contact that is the basis for account recovery and important notifications; the model requires it as part of the account record and as non-public data. What contact is collected and how it is verified is the identity/privacy design's.
- **acceptance_criteria**: An account has a contact value that the product treats as verified before relying on it for recovery, and that value is never returned to another account or in a public response. (The contact and verification mechanism is `REQ-ID-*`.)
- **release_gating**: true
- **traces_to**: REQ-PROD-012

#### REQ-DOM-035 — Private account data is never public
- **statement**: An account's credential, verified contact, and session data are never exposed to other accounts or in public responses; only the public profile fields — handle, display name, bio, follower/following counts, and public chirps — are visible to others.
- **acceptance_criteria**: Fetch another account's profile and any public response with no session and with a different account's session; only handle, display name, bio, and counts appear. Credential, contact, and session data never appear.
- **release_gating**: true
- **traces_to**: REQ-PROD-024

### Integrity, deletion, and derivable facts

#### REQ-DOM-036 — Every reference resolves
- **statement**: Every reference between entities resolves to an entity that exists: a chirp's author, a reply's target (when set), a follow's follower and followee, and a like's account and chirp all name existing entities; no dangling reference is observable.
- **acceptance_criteria**: Through every product surface that creates a relationship, the referenced entities must exist or the action is refused (REQ-DOM-013, REQ-DOM-015, REQ-DOM-017, REQ-DOM-022). No surface produces a chirp, follow, or like naming an entity that does not exist.
- **release_gating**: true

#### REQ-DOM-037 — Account deletion has a defined, applied outcome
- **statement**: Deleting an account produces a single defined outcome that the product applies and states: what becomes of the account's chirps (including those others have replied to or liked), its follow edges, and its likes, and whether its freed handle may be registered again — with no dangling reference left behind (REQ-DOM-036 continues to hold after a deletion).
- **acceptance_criteria**: Find the stated deletion outcome. Delete an account that has chirps (some replied-to and liked), follows, and likes; afterward the account cannot sign in, the product's state matches the stated outcome, and no remaining chirp, follow, or like references the deleted account in a way the outcome did not define. Whether the handle can be re-registered matches the stated policy.
- **release_gating**: true
- **traces_to**: REQ-PROD-020, REQ-PROD-021

#### REQ-DOM-038 — A person's own data is enumerable for export
- **statement**: The data belonging to an account — its profile, its chirps, and the set of accounts it follows — is enumerable from the model so the holder can obtain their own data in a portable form.
- **acceptance_criteria**: For a signed-in account, the model yields that account's profile, the full set of its chirps, and the full set of accounts it follows — the data a data-export surface returns. (The export surface and format are the experience/identity designs'; this requirement is that the data is enumerable per account.)
- **release_gating**: true
- **traces_to**: REQ-PROD-019

#### REQ-DOM-039 — Timestamps are UTC and totally ordered
- **statement**: Every creation timestamp is milliseconds since the Unix epoch in UTC, so timestamps across accounts and chirps are directly and unambiguously comparable for ordering (for example, the newest-first timeline of REQ-DOM-026).
- **acceptance_criteria**: Inspect `chirp_types::ids::Timestamp`; it is epoch-milliseconds UTC and ordered. Two chirps posted in sequence carry timestamps whose order matches the order they were posted.
- **release_gating**: true

#### REQ-DOM-040 — Server-maintained counts are read-only to clients
- **statement**: The denormalized counts in the model — an account's follower and following counts and a chirp's like count — are maintained by the product and are never accepted as client input; a client that sends a count on a create or update has it ignored, not honored.
- **acceptance_criteria**: Inspect the create/update request types in `chirp_types::api`; none carries a follower, following, or like count. Any attempt to set a count directly has no effect on the stored value.
- **release_gating**: true

<!--
Range note: this part owns REQ-DOM-001..049 and uses 001..040. The unused 041..049 are reserved,
not padding; a later amendment to the domain model takes ids from there without disturbing the
persistence (100..149) or module (200..249) ranges.
-->

---

## Traceability

Every `REQ-DOM-*` above that refines a product requirement cites it in `traces_to`. The map below is
the checkable summary, folded into the consolidated traceability matrix.

| REQ-DOM | Traces to REQ-PROD | release_gating |
|---|---|---|
| 001 | 008 | true |
| 002 | 009 | true |
| 003 | 009 | true |
| 004 | — | true |
| 005 | — | true |
| 006 | — | true |
| 007 | 020 | true |
| 008 | — | true |
| 009 | 016 | true |
| 010 | 018 | false |
| 011 | 001 | true |
| 012 | 001 | true |
| 013 | 001 | true |
| 014 | — | true |
| 015 | 003 | true |
| 016 | 004 | false |
| 017 | 006 | true |
| 018 | 006 | true |
| 019 | 006 | true |
| 020 | 006 | true |
| 021 | — | true |
| 022 | 005 | true |
| 023 | 005 | true |
| 024 | 005 | true |
| 025 | 002 | true |
| 026 | 002 | true |
| 027 | 002 | true |
| 028 | 002 | true |
| 029 | 010 | true |
| 030 | 014 | true |
| 031 | 015 | true |
| 032 | — | true |
| 033 | 008, 010 | true |
| 034 | 012 | true |
| 035 | 024 | true |
| 036 | — | true |
| 037 | 020, 021 | true |
| 038 | 019 | true |
| 039 | — | true |
| 040 | — | true |

**How the rest of the design builds on this model.** The persistence requirement (`REQ-DOM-100`–`149`)
determines what of this model is durable and where its state lives; the product requires accounts,
chirps, follows, likes, and sessions to survive a restart (`REQ-PROD-037`) — all five are entities
named in the vocabulary above, together with the account-associated credential and verified contact
(`REQ-DOM-033`, `REQ-DOM-034`). The modules-and-responsibilities and interfaces-and-entry-points
material (`REQ-DOM-200`–`249`) assigns ownership of each entity and the seams between parts, held to
the `crates/chirp-types` types named above and the `ChirpRepository` seam in `crates/chirp-server`.
Each references entities only by the canonical names in the vocabulary.
