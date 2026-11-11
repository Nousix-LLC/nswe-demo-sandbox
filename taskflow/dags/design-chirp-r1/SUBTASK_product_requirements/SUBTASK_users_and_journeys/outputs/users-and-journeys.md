<!--
Section sources for design/product-requirements.md:
  - users_personas
  - user_journeys
Needs are expressed in prose and `need:` handles only; REQ-PROD-* ids are minted by the
requirements fragment, not here. Where a journey touches a surface another design area owns
(detailed screens, authentication internals, durability, operations) the need is stated from the
user's side and the formal requirement is left to that area.
-->

# Users & end-to-end journeys — chirp

chirp is a Twitter-style social product: people post short messages ("chirps"), read a timeline of
the people they follow, and follow, reply to, and like each other. This document describes **who the
product serves** and **what each of them is trying to get done, from first visit to the day they
leave**, so that the requirements that follow are grounded in people doing real things rather than in
a feature list.

The journeys are walked against the product as it exists today (the `chirp-server` REST API and the
`chirp-frontend` single-page app). Where the walk reaches a point the product does not yet support —
a step a releasable product of this kind is expected to have — that gap is named as a **need**, because
a journey that dead-ends is itself a finding. Needs carry lowercase `need:` handles so the
requirements fragment can adopt them and make them testable.

A note on product kind, which the product-definition fragment settles: chirp is treated here as a
**consumer web application** first — a stranger can reach it, sign up, and use it from a browser. It
also ships as a single self-contained server image, which makes **running an instance** a real
activity and gives the operator (and, depending on the product kind chosen, a self-hoster) a place in
this document. Personas and journeys that depend on the product-kind decision are marked so.

---

## Users & personas (`users_personas`)

Each persona is a distinct kind of person with a distinct goal, not a demographic. A single real
human may move between them (a visitor becomes a chirper; a chirper also operates their own instance).
What separates them is what they are trying to accomplish and what they assume the product owes them.

### P1 — The unregistered visitor

**Who:** someone who has arrived at chirp with no account — from a shared link, a search, or
curiosity — and has not decided whether to join.

**Goal:** understand what chirp is and whether it is worth an account, with as little commitment as
possible, and then either join or leave.

**Context & assumptions:** a first-time visitor to a consumer web product expects to see *something*
before being asked to sign up — at minimum an explanation of what the product is, and ideally a taste
of real content (a public profile, a sample of posts). They assume signing up is quick and reversible,
and that they are not being asked for more than the product needs. They judge the whole product in the
first minute, mostly on the landing experience and the sign-up step.

**What they need from chirp:** a way in that explains itself and does not dead-end. Today the home
timeline requires authentication and there is no public discovery surface, so a visitor who is not
handed a link to a specific profile has little to look at before committing. `need: a first-visit
experience that lets an unregistered visitor understand chirp and reach sign-up without an account`.

### P2 — The everyday chirper (reader & poster)

**Who:** the core user — a registered person who reads and posts. "Reader-leaning" and "poster-leaning"
are the same persona at different moments; most people do both, and the product does not meaningfully
separate them (there is one account type, one home timeline, one compose action).

**Goal:** keep up with the people they follow and share short posts of their own, in short visits
through the day, without friction and without losing what they have posted or who they follow.

**Context & assumptions:** this persona assumes the ordinary contract of an account-based social
product: that signing in is theirs alone and cannot be done by someone who merely knows their handle;
that their posts, follows, and profile **persist** and are still there on the next visit; that they can
end a session, especially on a shared device; that they can change their mind — edit their profile,
leave, take their content with them. They expect the daily loop (open, read the timeline, post, reply,
like, follow) to be fast and to behave sensibly when there is nothing new, when they are brand new with
an empty timeline, and when something goes wrong.

**What they need from chirp:** the full participatory loop plus the account-lifecycle surfaces that
make the account feel like theirs. Several of these are the "unglamorous" surfaces the product does not
yet have; they are surfaced in the journeys below (sign-in that proves identity, session end, durable
data, account management, leaving with their data).

### P3 — The returning user after a break

**Who:** a registered chirper who has been away long enough that their session has ended and they are
no longer sure what they missed. This is P2 at a specific, high-friction moment, called out separately
because the return journey exposes needs the daily loop does not.

**Goal:** get back in and re-orient — sign back in (or recover access if they have forgotten how they
get in), and catch up on what happened while they were gone.

**Context & assumptions:** they assume getting back in is possible even if they have lost whatever they
signed in with, and that a device they trusted might remember them. They assume the catch-up is bounded
— they can see what is new without scrolling forever — and that a long absence has not quietly lost
their account or their follows.

**What they need from chirp:** a sign-in that recognizes a returning person, a recovery path when they
cannot sign in, and a timeline that handles "a lot has happened since you were here" gracefully.

### P4 — The operator / administrator

**Who:** the person responsible for running the chirp service for its users — deploying it, keeping it
up, keeping it safe, and helping users when something is wrong. In a small product the operator also
wears the support and trust-&-safety hats.

**Goal:** keep chirp available, protect the data users have entrusted to it, and be able to answer "is
it healthy?", "will the data survive a restart?", and "a user needs help / a user is abusing the
service — what can I do?".

**Context & assumptions:** an operator assumes the product can tell them whether it is healthy
(there is a `/healthz` probe today), that user data is durable across the restarts and redeploys that
operating a service entails, and that there is *some* supported way to act on an abusive account or an
account-holder's request (help a user recover, remove content, respond to a deletion request) without
editing data by hand. They do not assume a rich admin console for a product this size, but they do
assume the absence of any supported operator action is a gap, not a design choice.

**What they need from chirp:** operational visibility and durable data (the detailed requirements
belong to the operational-readiness and identity design areas; the operator journey below states the
need from the operator's side), and at least a minimal, supported way to administer accounts and
content.

### P5 — The self-hoster *(product-kind-dependent)*

**Who:** a technically capable person who runs their own copy of chirp from the published image, for
themselves or a small group, rather than using a service someone else operates.

**Goal:** stand up their own instance, understand how to configure and run it, and trust it with their
small community's data.

**Context & assumptions:** whether this persona is in scope depends on the product-kind decision the
product-definition fragment makes. chirp already ships as a single self-contained, documented container
image, which makes self-hosting technically real today. A self-hoster assumes they can run it from
documentation alone, configure the handful of things an instance needs, and that running their own copy
does not cost them the durability and account-management surfaces a hosted user would get. If the
product kind is settled as a closed hosted demonstration, this persona is recorded out of scope with
that reason rather than designed for.

**What they need from chirp:** a runnable, documented image (present today) and the same durability and
account-lifecycle guarantees as any other deployment — so self-hosting is not a second-class experience.

---

## End-to-end journeys (`user_journeys`)

Each journey is walked from the user's side, step by step, including the empty, error, and
second-visit states where they shape the experience. A step marked **gap** is one the product does not
support today but a releasable product of this kind is expected to; each gap carries a `need:` handle.
Detailed screen design belongs to the experience-design area, authentication and session internals to
the identity area, durability and operations to the domain and operational-readiness areas; the
journeys here describe what the user is trying to do and what they need, and leave each area its formal
requirement.

### J1 — First visit (unregistered visitor → decision) — P1

1. The visitor arrives at chirp's address with no account and no session.
2. They look for an answer to "what is this and should I join?" A consumer web product is expected to
   present a landing experience — what chirp is, and ideally a sample of real content — before asking
   for a commitment.
   - **gap / empty state:** the home timeline requires authentication and there is no public discovery
     or landing content, so a visitor who did not arrive on a specific public profile link has little
     to evaluate. `need: a public landing/first-visit experience that explains chirp and leads to
     sign-up without requiring an account`.
3. If the visitor arrived on a link to a specific profile, they can view that public profile (the
   product serves a user's public profile without authentication). From there they understand the shape
   of the product — a person, their posts' existence — but cannot browse further without an account.
4. The visitor decides to join and proceeds to sign-up (J2), or leaves. If they leave, nothing is
   created; this is a clean exit and the expected outcome for many first visits.

**Needs surfaced:** `need: a public first-visit experience`; `need: a clear, low-commitment path from
first visit to sign-up`.

### J2 — Sign-up (create an account) — P1 → P2

1. The visitor chooses to create an account and provides a **handle** (the unique username, up to 15
   letters, digits, or underscores), a **display name**, and optionally a short **bio**.
2. The product checks the handle is well-formed and not already taken; a taken handle is reported as a
   conflict the person can resolve by choosing another. An ill-formed handle (a space, a disallowed
   character, too long) is reported against the offending field so the person can fix it. These
   validation and conflict behaviors exist today and are the expected, correct shape.
3. The account is created and the person is now a chirper (P2).
   - **gap:** sign-up collects a handle and profile only — it establishes **no secret or credential**
     the person will later use to prove they are them. Anyone who later knows the handle can sign in as
     this account (see J3). A releasable account-based product is expected to establish a real
     credential at sign-up. `need: sign-up establishes a real authentication credential, not a handle
     alone` (the credential mechanism itself is the identity area's requirement).
   - **gap:** there is no confirmation that the person controls any contact address, so there is no
     basis for later account recovery (J3a) or important notifications. `need: a verified point of
     contact captured at sign-up to support recovery and notifications` (kept minimal and
     privacy-respecting; what contact is collected is an identity/privacy decision).
4. Immediately after sign-up the person lands in the product for the first time with **nothing yet** —
   no posts, no follows, an empty home timeline (J5 covers the empty state and onboarding).

**Needs surfaced:** `need: handle uniqueness and validation feedback at sign-up` (present today);
`need: a real credential at sign-up`; `need: a verified contact for recovery/notifications`;
`need: a first-run / onboarding experience that gets a brand-new account to a non-empty timeline`.

### J3 — Sign-in (returning to an existing account) — P2 / P3

1. The person provides the handle they signed up with.
2. The product authenticates them and issues a **session token** the app then carries on their behalf;
   subsequent actions (posting, following, reading the home timeline) are performed as that
   authenticated person. The session-token mechanism exists today.
   - **gap (critical, from the user's side):** authentication today is **handle-only** — presenting a
     known handle is sufficient to receive a session for that account. From the user's perspective this
     means *anyone who knows your handle can sign in as you*, which breaks the most basic assumption a
     person has about their account. `need: sign-in proves the person is the account owner, not merely
     that they know the handle` (the authentication design is the identity area's requirement; the
     journey states the user-side need: an account only its owner can enter).
3. An unknown handle is reported as "no such account" so the person can tell a typo from a
   not-yet-created account and proceed to sign-up.
4. The authenticated person continues into their daily use (J5).

**Needs surfaced:** `need: authenticated sign-in that only the account owner can pass`;
`need: a clear not-found vs. wrong-credential distinction on sign-in`.

#### J3a — Account recovery (forgotten access) — P3

1. A returning person cannot sign in — they have forgotten or lost whatever they sign in with.
2. They look for a "can't get in?" path that re-establishes access through the verified contact
   captured at sign-up, without needing anyone to act on their behalf.
   - **gap:** there is no recovery path today. With handle-only sign-in the question is moot; once a
     real credential exists (J2/J3), a person who loses it has no supported way back in. `need: a
     self-service account-recovery path for a person who has lost their credential`.
3. On success the person is back in and continues as P2.

**Needs surfaced:** `need: self-service recovery through a verified contact`.

#### J3b — Ending a session (sign-out) — P2

1. The person wants to stop being signed in — especially on a shared or public device.
2. They look for a sign-out action that ends the current session so the next person at that device is
   not them.
   - **gap:** there is no way to end a session today — the app can drop its copy of the token, but
     there is no supported sign-out that invalidates the session server-side. On a shared device this
     leaves the account exposed. `need: a sign-out that reliably ends the session, including
     server-side invalidation`.

**Needs surfaced:** `need: sign-out that ends the session`.

### J4 — The core loop: post, read, reply, like, follow — P2

This is the activity the product exists for; it is walked as the connected loop a chirper actually
performs, not as isolated features.

1. **Read the home timeline.** The chirper opens chirp and sees their home timeline — their own posts
   and those of everyone they follow, newest first, in bounded pages (the product paginates with an
   opaque cursor and returns pages rather than everything at once). This is the default thing to do on
   opening the app.
   - **empty state:** a chirper who follows no one and has posted nothing sees an empty timeline; the
     product should explain what to do about it rather than show a blank (J5 onboarding).
   - **second-visit / catch-up state:** a chirper returning after activity sees new posts since last
     time; paging lets them catch up without loading everything. `need: a timeline that handles a large
     backlog of unseen posts gracefully (bounded catch-up, not infinite load)`.
2. **Compose and post a chirp.** The chirper writes a message up to 280 characters and posts it; it is
   attributed to them and appears in their timeline and in the timelines of their followers. The
   length limit and validation exist today.
   - **error state:** an over-long or empty message is rejected against the text field with a message
     the composer can act on (present today). The compose experience should show the limit *before*
     submission (a detail owned by the experience-design area). `need: compose shows remaining
     characters and prevents an over-limit post before submission`.
3. **Reply.** The chirper replies to a chirp; the reply records what it is replying to, enabling a
   threaded conversation. Replying to a chirp that no longer exists is reported as not-found rather than
   silently dropped. Reading a conversation as a thread (following a reply to its parent and back) is a
   need the journey implies. `need: read a reply in the context of the conversation it belongs to`.
4. **Like / unlike.** The chirper likes a chirp (and can unlike it); liking is idempotent — liking
   twice does not double-count — and the like count they see reflects the result. This behavior exists
   today.
5. **Follow / unfollow.** The chirper follows another user to bring that user's posts into their home
   timeline (and unfollows to remove them); following is idempotent and a person cannot follow
   themselves. This exists today. Finding *who* to follow is the open question:
   - **gap:** there is no search or discovery surface — a chirper can only follow someone whose profile
     they already reached (e.g. via an external link or a reply). A social product is expected to offer
     some way to find people. `need: a way to discover and find other users and content to follow`.
6. **View a profile.** The chirper views a user's profile — their display name, bio, and follower and
   following counts — to decide whether to follow, or to see their own public face. Public profiles are
   served today.

**Needs surfaced:** `need: home timeline (own + followed, newest-first, paged)` (present today);
`need: post a chirp within a published length limit` (present today);
`need: reply and read conversations in context`;
`need: like/unlike, idempotent, with an accurate count` (present today);
`need: follow/unfollow to shape the timeline` (present today);
`need: discover/search for people and content to follow` (gap);
`need: view a user's public profile` (present today).

### J5 — Daily & returning use (empty / error / second-visit states) — P2 / P3

1. **Brand-new account (first run).** Straight after sign-up the chirper has an empty timeline. The
   product should onboard them — explain the empty state and help them reach a non-empty timeline
   (suggest or help them find people to follow, prompt a first post) rather than present a blank page.
   `need: a first-run onboarding that moves a new account off the empty state`.
2. **Ordinary daily visit.** The chirper opens chirp, reads what is new, posts or replies, and leaves —
   often in under a minute. The loop must be fast and must not make them re-authenticate every visit on
   a device they trust (bounded by the session/sign-out needs in J3/J3b). `need: a trusted device keeps
   the chirper signed in across ordinary visits, subject to session expiry and sign-out`.
3. **Error states the chirper meets.** An expired or invalid session should return the chirper to
   sign-in with their place explained, not fail silently (the product returns an unauthorized signal
   today; presenting it well is the experience area's job). A transient server error should be
   recoverable by retrying without losing a drafted chirp. `need: expired-session and transient-error
   states that recover without losing the person's in-progress work`.
4. **Returning after a break.** A lapsed chirper (P3) signs back in (J3) or recovers access (J3a), then
   meets the catch-up state of J4.1.

**Needs surfaced:** `need: onboarding off the empty state`; `need: fast, low-friction daily re-entry`;
`need: graceful expired-session and error recovery`.

### J6 — Managing the account (profile, settings) — P2

1. The chirper wants to change how they appear — update their display name or bio — or manage the
   handful of settings an account-based product carries (their contact for recovery/notifications,
   notification preferences, session/device management).
   - **gap:** there is no way to edit a profile or change any account setting today — a profile is set
     at sign-up and fixed thereafter. A person's display name and bio are exactly the things they
     expect to be able to change. `need: edit profile (display name, bio) after sign-up`.
   - **gap:** there is no settings surface for the account-level choices the lifecycle implies (contact,
     notifications, sessions). `need: an account settings surface for contact, notifications, and
     session/device management` (the specific settings are shared with the identity and experience
     areas; the journey establishes that the surface must exist).
2. Whether a handle can be changed after sign-up is an open product question (handles are unique
   identifiers others follow by). The journey raises it; the decision is the product-definition/identity
   areas'. `need: a decision on whether and how a handle can change after sign-up`.

**Needs surfaced:** `need: edit profile after sign-up`; `need: an account-settings surface`;
`need: a handle-change decision`.

### J7 — Safety: being bothered by others — P2

1. A chirper is replied to, followed, or targeted by an account they do not want to interact with.
2. They look for the controls a social product is expected to have — block or mute an account, and
   report content or an account that violates the rules.
   - **gap:** there are no block, mute, or report controls today, and no stated rules. For a product
     that lets strangers post at each other, the absence of any safety control is a releasability
     concern, not a nice-to-have. `need: block and mute controls so a chirper can stop unwanted
     interaction`; `need: a way to report abusive content or accounts`; `need: stated rules/terms a
     report can reference`.
3. Notifications are the other side of this loop: a chirper expects to know when they are replied to,
   followed, or liked.
   - **gap:** there is no notification surface today. `need: notify a chirper of relevant activity
     (replies, follows, likes), with preferences`.

**Needs surfaced:** `need: block/mute`; `need: report abuse`; `need: stated rules`; `need: activity
notifications with preferences`.

### J8 — Leaving: deletion and taking your data out — P2

The end of the relationship is part of the product. A person who cannot leave cleanly, or cannot take
their content with them, does not fully trust the product with their data in the first place.

1. **Export my data.** The departing (or merely cautious) chirper wants to take their content with them
   — their posts, their profile, who they follow.
   - **gap:** there is no data export today. A releasable consumer product is expected to let a person
     obtain their own data. `need: a person can export their own data (posts, profile, follows) in a
     portable form`.
2. **Delete my account.** The person decides to leave and wants their account and content removed.
   - **gap:** there is no account deletion today — once created, an account cannot be removed by its
     owner. `need: a person can delete their account and have their content removed`.
   - The journey raises, for the identity/privacy areas to decide: what deletion does to the person's
     chirps that others have replied to or liked, and whether the handle becomes available again.
     `need: a defined outcome for a deleted account's content and handle`.
3. **Confirmation and finality.** Deletion is destructive and should be confirmed, and the person should
   be told what will and will not survive (e.g. that export is their chance to keep a copy). `need:
   deletion is confirmed and explains what is and is not retained`.

**Needs surfaced:** `need: self-service data export`; `need: self-service account deletion`;
`need: a defined deletion outcome for content and handle`; `need: confirmed, explained deletion`.

### J9 — Operating the service (keep it running for users) — P4

1. **Is it healthy?** The operator checks whether the service is up; chirp answers a health probe
   today, which reports process liveness. The operator needs enough signal to know the service is
   serving users, not merely running. `need: a health/readiness signal the operator can
   trust to mean "serving users"` (the detailed observability requirement is the operational-readiness
   area's).
2. **Will the data survive?** The operator deploys, restarts, and redeploys as a normal part of running
   a service. They need the users' accounts, chirps, and follows to persist across those events.
   - **gap (critical, from the operator's and every user's side):** chirp stores its data **in memory**
     with no external database, so a restart or redeploy loses every account, chirp, follow, and
     session. For a product held to a releasable bar this is a blocker: it breaks the P2 assumption
     that "my account and posts are still there next time." `need: user data (accounts, chirps,
     follows, sessions) is durable across restart and redeploy` (the persistence design is the domain
     and operational-readiness areas' requirement; the journey states that no user journey above holds
     without it).
3. **Help a user / act on abuse.** A user asks for help (cannot get in, wants their account removed) or
   an account is reported for abuse. The operator needs a supported way to act — assist recovery,
   remove content, action an account — without hand-editing data.
   - **gap:** there is no administrative or support surface today. `need: a minimal, supported
     administrative surface for the operator to act on accounts and content (assist, remove, action
     abuse)`.
4. **Back up and recover.** The operator needs to be able to recover user data after a failure.
   - **gap:** with no durable store there is nothing to back up; once data is durable, a backup/restore
     path is expected. `need: a backup and recovery path for durable user data` (owned by the
     operational-readiness area; raised here because the operator's journey requires it).

**Needs surfaced:** `need: trustworthy health/readiness`; `need: durable user data across
restart/redeploy` (blocker); `need: a supported administrative/support surface`; `need: backup and
recovery`.

### J10 — Self-hosting an instance — P5 *(product-kind-dependent)*

1. A self-hoster runs chirp from the published container image for their own small community.
2. They configure the instance from documentation, start it, and confirm it is serving. The
   self-contained, documented image makes this real today.
3. They expect their instance to give their users the same durability and account-lifecycle guarantees
   as any other deployment — the same durable-data and account-management needs from J8 and J9 apply to
   a self-hosted instance. `need: a self-hosted instance offers the same durability and
   account-lifecycle guarantees as a hosted one`.
4. If the product kind is settled as a closed hosted demonstration, this journey is recorded out of
   scope with that reason rather than designed for; the product-definition fragment makes that call.

**Needs surfaced:** `need: a runnable, documented self-host image` (present today); `need: parity of
durability and account-lifecycle guarantees for self-hosted instances` (conditional on product kind).

---

## Journey → need summary (for the requirements fragment)

The requirements fragment is the sole minter of `REQ-PROD-*` ids; this table hands it the
journey-derived needs so every journey traces to at least one requirement. "Status" records whether the
product supports the need today, from the walks above.

| Journey | Need handle | Status today |
|---|---|---|
| J1 | `need: a public first-visit experience` | gap |
| J1/J2 | `need: a low-commitment path from first visit to sign-up` | gap |
| J2 | `need: handle uniqueness and validation feedback at sign-up` | present |
| J2/J3 | `need: a real authentication credential (not handle alone)` | gap (critical) |
| J2/J3a | `need: a verified contact for recovery/notifications` | gap |
| J2/J5 | `need: first-run onboarding off the empty state` | gap |
| J3 | `need: sign-in only the account owner can pass` | gap (critical) |
| J3 | `need: clear not-found vs wrong-credential on sign-in` | partial |
| J3a | `need: self-service account recovery` | gap |
| J3b | `need: sign-out that ends the session (server-side)` | gap |
| J4 | `need: home timeline (own + followed, newest-first, paged)` | present |
| J4 | `need: post a chirp within a published length limit` | present |
| J4 | `need: reply and read conversations in context` | partial |
| J4 | `need: like/unlike, idempotent, accurate count` | present |
| J4 | `need: follow/unfollow to shape the timeline` | present |
| J4 | `need: discover/search for people and content to follow` | gap |
| J4 | `need: view a user's public profile` | present |
| J5 | `need: fast, low-friction daily re-entry` | partial |
| J5 | `need: graceful expired-session and transient-error recovery` | gap |
| J6 | `need: edit profile (display name, bio) after sign-up` | gap |
| J6 | `need: an account-settings surface (contact, notifications, sessions)` | gap |
| J6 | `need: a handle-change decision` | open question |
| J7 | `need: block and mute controls` | gap |
| J7 | `need: report abusive content or accounts` | gap |
| J7 | `need: stated rules/terms` | gap |
| J7 | `need: activity notifications with preferences` | gap |
| J8 | `need: self-service data export` | gap |
| J8 | `need: self-service account deletion` | gap |
| J8 | `need: a defined deletion outcome for content and handle` | gap |
| J8 | `need: confirmed, explained deletion` | gap |
| J9 | `need: trustworthy health/readiness signal` | partial |
| J9 | `need: durable user data across restart/redeploy` | gap (blocker) |
| J9 | `need: a supported administrative/support surface` | gap |
| J9 | `need: backup and recovery for durable data` | gap |
| J10 | `need: a runnable, documented self-host image` | present |
| J10 | `need: durability/account-lifecycle parity for self-hosted instances` | gap (conditional) |

The handles marked **critical** (handle-only authentication) and **blocker** (in-memory storage) are
the two findings that most directly break a releasable-product assumption: that an account is enterable
only by its owner, and that what a person creates is still there next time. Every other gap is a
surface a releasable product of this kind is expected to have; where the product kind makes one
out of scope, the requirements and product-definition fragments record it out of scope with a reason
rather than leaving it silently absent.
