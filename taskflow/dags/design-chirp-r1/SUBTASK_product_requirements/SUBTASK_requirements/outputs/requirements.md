<!--
Section sources for design/product-requirements.md:
  - requirements_and_acceptance_criteria  (the REQ-PROD-* register)
  - in_scope_out_of_scope                  (consolidated)
Owner: SUBTASK_requirements. Sole minter of REQ-PROD-* ids. Composes against the read-only
subtree and parent contracts; uses the inherited REQ-PROD-NNN format and each_requirement_has
fields (id, statement, acceptance_criteria, release_gating) without redefining them.
Expresses what the product must do from the user's/operator's side — never how it is built.
Grounded in Nousix-LLC/nswe-demo @ c805525.
-->

# Requirements, acceptance criteria & scope — chirp

This part of the product-requirements design turns the needs surfaced by the product
definition and the user journeys into a register of testable product requirements, and states
what a releasable chirp of this kind includes and leaves out. It mints every `REQ-PROD-*` id
(it is the sole minter) and states each requirement as *what must be true from the user's or
operator's side*, with an acceptance criterion a person who never met the author can check
against the live product. The implementation "how" is left to later code work; where the
detailed requirement belongs to another design area, the product-level requirement is stated
here from the user's side and the area that carries the detail is named, without minting that
area's ids.

**How to read a requirement.** Each carries an `id`, a `statement` (the condition that must
hold), an `acceptance_criteria` a stranger can exercise on the live product, and a
`release_gating` flag — `true` when a releasable product of this kind depends on it, `false`
when it is in scope and expected but a first release could ship without it. A `false` flag is
never "won't build"; it is "the release bar need not block v1 on it," and each carries its
reason. The final MVP-vs-releasable staging of the `false` items is the release-bar design's
to settle (`BAR-*`); this register gives it the requirements and the release-gating flags to stage.

chirp is held to the bar of a **releasable consumer web application**, not a prototype: absent
an explicit reduction by the engagement, "it deploys and the core loop runs" is not the bar.
That standard is what the `release_gating: true` flags below encode.

---

## requirements_and_acceptance_criteria

### The core loop — what chirp is for

#### REQ-PROD-001 — Post a chirp
- **statement**: A signed-in person can publish a short public message (a *chirp*) up to the published length limit of 280 characters, attributed to them; an empty or over-limit message is rejected and nothing is posted.
- **acceptance_criteria**: Signed in, compose a message of 280 characters or fewer and publish it; it appears attributed to your handle. Compose a message over 280 characters, or an empty one, and submit; the product reports the problem against the compose field and no chirp is created.
- **release_gating**: true

#### REQ-PROD-002 — Read the home timeline
- **statement**: A signed-in person can read a timeline of their own chirps and those of the people they follow, newest first, in bounded pages rather than all at once.
- **acceptance_criteria**: Signed in and following at least one person who has posted, open the timeline: recent chirps appear newest-first. Request the next page and older chirps load; the product returns pages (it does not attempt to return every chirp in one response).
- **release_gating**: true

#### REQ-PROD-003 — Reply to a chirp
- **statement**: A person can reply to an existing chirp, and the reply records the chirp it answers; replying to a chirp that no longer exists is reported, not silently dropped.
- **acceptance_criteria**: Reply to a visible chirp; the reply is published and identifies its parent. Attempt to reply to a deleted or nonexistent chirp; the product reports not-found rather than appearing to succeed.
- **release_gating**: true

#### REQ-PROD-004 — Read a reply in the conversation it belongs to
- **statement**: A person can move from a reply to the chirp it answers and see the conversation it belongs to.
- **acceptance_criteria**: Given a reply, navigate to its parent chirp and see the two in relation (the reply presented as answering that parent).
- **release_gating**: false — the parent reference is already recorded (REQ-PROD-003); reading replies as a navigable conversation is an enhancement a first release can omit. Richer multi-level threading is out of scope (see below). The release bar decides whether v1 includes conversation reading.

#### REQ-PROD-005 — Like and unlike
- **statement**: A person can like and unlike a chirp; liking is idempotent and the like count reflects the result.
- **acceptance_criteria**: Like a chirp; the count increases by one. Like it again; the count does not increase again. Unlike it; the count returns.
- **release_gating**: true

#### REQ-PROD-006 — Follow and unfollow
- **statement**: A person can follow and unfollow another user to shape their timeline; following is idempotent and a person cannot follow themselves.
- **acceptance_criteria**: Follow another user; that user's new chirps appear in your timeline. Follow again; nothing is duplicated. Unfollow; their chirps leave your timeline. Attempt to follow your own account; it is rejected.
- **release_gating**: true

#### REQ-PROD-007 — View a user's public profile
- **statement**: Anyone can view a user's public profile — handle, display name, bio, and follower/following counts — without signing in.
- **acceptance_criteria**: Open a user's profile with no session; it shows the handle, display name, bio, and follower/following counts.
- **release_gating**: true

### Accounts and the identity lifecycle
*(Product-level requirements. The credential, session, and authentication mechanisms are the identity/security design's detail — `REQ-ID-*` — not minted here.)*

#### REQ-PROD-008 — Real sign-up that establishes a credential
- **statement**: A new person can create an account with a unique, well-formed handle and a display name (bio optional), and sign-up establishes a secret the person will later use to prove the account is theirs — not a handle alone.
- **acceptance_criteria**: Sign up with a fresh, well-formed handle; the account is created. Verify, via REQ-PROD-010, that knowing the handle alone does not let someone else sign in as the account — i.e. sign-up established a credential beyond the handle.
- **release_gating**: true

#### REQ-PROD-009 — Handle validation and uniqueness feedback at sign-up
- **statement**: Sign-up enforces handle format (up to 15 letters, digits, or underscores) and uniqueness, reporting a taken or ill-formed handle against the field so the person can fix it.
- **acceptance_criteria**: Submit a handle already in use; the product reports a conflict naming the handle. Submit a handle with a space, a disallowed character, or more than 15 characters; the product reports a field-level validation error. Submit a valid, unused handle; it is accepted.
- **release_gating**: true

#### REQ-PROD-010 — Sign-in only the account owner can pass
- **statement**: Signing in requires proving the account is the person's own; presenting a known handle alone must not grant a session.
- **acceptance_criteria**: Knowing only another account's handle (not its credential), attempt to sign in as it; no session is granted. The legitimate owner, presenting the credential set at sign-up or recovery, is signed in.
- **release_gating**: true

#### REQ-PROD-011 — Clear not-found vs. failed-credential signal at sign-in
- **statement**: Sign-in lets a person tell "no such account" from "credential did not match," enough to distinguish a typo from a wrong secret, without exposing which accounts exist beyond what the product already makes public.
- **acceptance_criteria**: Sign in with an unknown handle; the result lets you tell the account does not exist so you can proceed to sign-up. Sign in with a known handle and a wrong credential; the result is a failed sign-in you can retry or recover from.
- **release_gating**: true

#### REQ-PROD-012 — A verified point of contact for recovery and notifications
- **statement**: The product captures and verifies a point of contact for an account, kept minimal and privacy-respecting, so recovery and important notifications have a basis.
- **acceptance_criteria**: During sign-up or in settings, provide a contact; the product confirms you control it (a verification step) before relying on it for recovery.
- **release_gating**: true — account recovery (REQ-PROD-013) depends on it. What contact is collected and how it is protected is the identity/privacy design's detail.

#### REQ-PROD-013 — Self-service account recovery
- **statement**: A person who has lost their credential can regain access themselves, through the verified contact, without another person acting on their behalf.
- **acceptance_criteria**: Having lost your credential, use a "can't get in?" path, prove control of the verified contact, and regain access. Someone without that verified contact cannot recover the account.
- **release_gating**: true

#### REQ-PROD-014 — Sign-out that ends the session server-side
- **statement**: A person can end their session so it can no longer be used — important on a shared or public device.
- **acceptance_criteria**: Sign out; then present the session that was in use (e.g. replay the prior request) — it is rejected. The next person at that device is not signed in as you.
- **release_gating**: true

#### REQ-PROD-015 — Stay signed in across ordinary visits on a trusted device
- **statement**: On a device a person chooses to trust, they remain signed in across ordinary visits, subject to session expiry and to sign-out.
- **acceptance_criteria**: Sign in, close and reopen the app on the same device within the session's validity; you are still signed in. After expiry or sign-out, you are returned to sign-in.
- **release_gating**: false — a releasable product may require sign-in each visit; staying signed in is an expected convenience the experience/identity design tunes. Recorded so the choice is explicit rather than assumed.

### Managing the account

#### REQ-PROD-016 — Edit profile after sign-up
- **statement**: A person can change their display name and bio after sign-up.
- **acceptance_criteria**: Signed in, change your display name and bio; the change persists and shows on your profile on the next view.
- **release_gating**: true

#### REQ-PROD-017 — An account settings surface
- **statement**: A person has a settings surface for account-level choices — at minimum their verified contact and their active sessions/devices, plus notification preferences where notifications exist.
- **acceptance_criteria**: Signed in, open settings; view and update your verified contact, and view and end your active sessions. Where activity notifications exist (REQ-PROD-029), set their preferences here.
- **release_gating**: true — the surface the recovery-contact and sign-out requirements imply must exist. The exact settings are shared with the identity and experience designs.

#### REQ-PROD-018 — A stated handle-change policy
- **statement**: The product states whether and how a handle can change after sign-up, and behaves consistently with that stated policy.
- **acceptance_criteria**: Find the product's stated position on handle changes; the product's behavior matches it — either a handle change is offered and works, or the handle is stated as fixed and no path changes it.
- **release_gating**: false — this is a decision-and-consistency requirement (handles are the identifier others follow by); the product-definition/identity designs make the call. A first release may ship with handles fixed, provided that position is stated in the product.

### Leaving — export and deletion

#### REQ-PROD-019 — Self-service data export
- **statement**: A person can obtain their own data — their chirps, profile, and who they follow — themselves, in a portable form.
- **acceptance_criteria**: Signed in, request your data; you receive your posts, profile, and follow list in an openable, portable form (a file or download you can read outside chirp).
- **release_gating**: true

#### REQ-PROD-020 — Self-service account deletion
- **statement**: A person can delete their own account and have their content removed.
- **acceptance_criteria**: Signed in, delete your account; afterward the account can no longer sign in, and your content is removed per the stated deletion outcome (REQ-PROD-021).
- **release_gating**: true

#### REQ-PROD-021 — A defined deletion outcome for content and handle
- **statement**: The product defines, and applies, what deletion does to the person's chirps that others have replied to or liked, and whether the handle becomes available again.
- **acceptance_criteria**: Find the stated deletion outcome. After a deletion, the product's behavior matches it — what remains (or not) of replied-to/liked chirps, and whether the freed handle can be re-registered, is as stated.
- **release_gating**: true — deletion is not releasable without a defined outcome. The privacy and identity designs own the specifics.

#### REQ-PROD-022 — Deletion is confirmed and explained
- **statement**: Account deletion is confirmed before it happens and tells the person what will and will not survive, including that export is their chance to keep a copy.
- **acceptance_criteria**: Initiate deletion; a confirmation explains the consequences and points to export, and deletion proceeds only after explicit confirmation. Cancel at the confirmation; nothing is deleted.
- **release_gating**: true

### Authorization and privacy
*(Product-level. The detailed authorization model and threat analysis are the identity/security design's — `REQ-ID-*`.)*

#### REQ-PROD-023 — A clear authorization boundary
- **statement**: A person can act only as themselves and can change only their own account and content; there is a clear boundary on who may act as an account and who may change what.
- **acceptance_criteria**: Signed in as one account, attempt through the product's surfaces to post/reply/like/follow as another account, to edit another's profile or settings, or to delete another's content; each is refused.
- **release_gating**: true

#### REQ-PROD-024 — Privacy basics
- **statement**: Private account details — a person's contact, credential, and session data — are never exposed to other users or in public responses; only intended public fields (handle, display name, bio, public chirps, counts) are public.
- **acceptance_criteria**: View another user's profile and any public responses; only public fields appear. A person's contact, credential, and session data are never returned to another user.
- **release_gating**: true

### Safety, moderation, and support
*(Product-level. The abuse model and operator tooling detail are shared with the identity/security and operational-readiness designs — `REQ-ID-*` / `REQ-OPS-*`.)*

#### REQ-PROD-025 — Report abusive content or accounts
- **statement**: A person can report a chirp or an account that breaks the rules, and sees that the report was received.
- **acceptance_criteria**: Signed in, submit a report against a chirp and against an account; each submission is acknowledged as received.
- **release_gating**: true — a public space where strangers post at each other is not releasable with no way to report a problem.

#### REQ-PROD-026 — Stated rules a report can reference
- **statement**: The product states the rules — what is and is not allowed — that a report references.
- **acceptance_criteria**: Find the rules/terms within the product; a report can point to them.
- **release_gating**: true

#### REQ-PROD-027 — Controls to stop unwanted interaction (block/mute)
- **statement**: A person can stop unwanted interaction from another account — at minimum block or mute.
- **acceptance_criteria**: Signed in, block or mute another account; afterward that account's interaction with you, or its visibility to you, is suppressed per the control's stated effect.
- **release_gating**: false — expected, but a first release may ship with reporting (REQ-PROD-025) and operator action (REQ-PROD-028) as the safety floor and add block/mute as a fast follow. The release bar decides which unwanted-interaction controls gate v1; at least one safety control (reporting) is gated above.

#### REQ-PROD-028 — A supported administrative/support surface
- **statement**: The operator has a minimal, supported way to act on accounts and content — assist a user (e.g. recovery), remove content, and action an abusive account — without hand-editing the datastore.
- **acceptance_criteria**: As the operator, through a supported interface, assist a user's recovery, remove a named chirp, and disable or action an abusive account; none of these requires editing stored data by hand.
- **release_gating**: true

### Notifications

#### REQ-PROD-029 — Activity notifications with preferences
- **statement**: A person is notified of relevant activity — replies, follows, and likes directed at them — and can set which of these they are notified about.
- **acceptance_criteria**: Have another account reply to, follow, or like you; you see a notification of it. In settings, turn one category off; notifications of that category stop.
- **release_gating**: false — a baseline notifications story is in scope and expected, but a first release can ship without it. The release bar decides whether v1 gates on notifications.

### Experience quality
*(Product-level. The screens, visual system, and the exact accessibility standard are the experience design's — `REQ-UX-*`.)*

#### REQ-PROD-030 — A public first-visit experience
- **statement**: An unregistered visitor can understand what chirp is and reach sign-up without an account, rather than meeting an authentication wall.
- **acceptance_criteria**: Arrive with no account and no session; you see an explanation of what chirp is and a clear path to sign up, without being required to sign in first.
- **release_gating**: true — a consumer product that dead-ends unregistered visitors at a sign-in wall is not releasable.

#### REQ-PROD-031 — A low-commitment path from first visit to sign-up
- **statement**: The path from first visit to a created account is short and asks for no more than the account needs.
- **acceptance_criteria**: From the landing experience, reach a created account through a sign-up that requests only a handle, a display name, an optional bio, and the credential and contact the account requires — nothing extraneous.
- **release_gating**: false — the gated sign-up behavior is REQ-PROD-008/009; the brevity of the path is a quality expectation the experience design tunes.

#### REQ-PROD-032 — First-run onboarding off the empty state
- **statement**: A brand-new account is helped off its empty timeline — the product explains the empty state and offers at least one way to reach a non-empty timeline (find people to follow, prompt a first post) rather than showing a blank page.
- **acceptance_criteria**: Immediately after sign-up, with no follows and no posts, you see guidance explaining the empty state and at least one actionable way toward a non-empty timeline, not a blank screen.
- **release_gating**: true — a releasable consumer product does not drop every new account onto a blank page.

#### REQ-PROD-033 — Considered empty, loading, and error states
- **statement**: Empty, loading, and error states across the product are explained rather than shown as blanks or silent failures.
- **acceptance_criteria**: Reach an empty list, a loading list, and a failed action; each presents a state you can understand and act on, rather than a blank area or an unexplained failure.
- **release_gating**: true

#### REQ-PROD-034 — Graceful expired-session and transient-error recovery
- **statement**: An expired or invalid session returns the person to sign-in with their place explained; a transient error is recoverable by retry without losing in-progress work such as a drafted chirp.
- **acceptance_criteria**: With an expired session, take an action; you are routed to sign-in with an explanation, not a silent failure. On a transient server error while posting, retry without losing the drafted text.
- **release_gating**: true

#### REQ-PROD-035 — Works on a phone
- **statement**: The core loop works in a phone browser at a phone-sized viewport.
- **acceptance_criteria**: On a typical phone viewport, read the timeline, compose and post, reply, like, follow, and view a profile, with no broken layout or unreachable controls.
- **release_gating**: true

#### REQ-PROD-036 — An accessibility baseline
- **statement**: The core loop is usable with assistive technology — operable by keyboard, with accessible names and roles for its controls — to a baseline the experience design sets.
- **acceptance_criteria**: Using keyboard navigation and a screen reader, complete the core loop (read the timeline, compose/post, reply, like, follow, view a profile); controls expose accessible names and roles.
- **release_gating**: true — a releasable consumer product meets an accessibility baseline; the exact standard (e.g. a WCAG level) is the experience design's to fix.

### Durability and operational readiness
*(Product-level, stated from the user's and operator's side. The persistence model is the domain design's — `REQ-DOM-*`; backups, limits, observability, and availability targets are the operational-readiness design's — `REQ-OPS-*`.)*

#### REQ-PROD-037 — Durable user data across restart and redeploy
- **statement**: Accounts, chirps, follows, likes, and sessions survive the service being restarted, updated, and redeployed — a person's account and content are still there on the next visit. This requirement holds for any deployment of chirp.
- **acceptance_criteria**: Create an account and some chirps, follows, and likes; have the service restarted or redeployed; sign in again — the account still exists and its chirps, follows, and likes are still present.
- **release_gating**: true — the in-memory store at `c805525`, which loses everything on restart, is a release blocker, not a style choice.

#### REQ-PROD-038 — Backup and recovery of durable data
- **statement**: The durable user data can be backed up and restored, so it can be recovered after a failure.
- **acceptance_criteria**: Operating the service, produce a backup of user data, then restore from it; accounts, chirps, and follows are brought back.
- **release_gating**: true

#### REQ-PROD-039 — A trustworthy health/readiness signal
- **statement**: The product exposes a health/readiness signal an operator can trust to mean "serving users," not merely "the process is running."
- **acceptance_criteria**: Query the signal while the product cannot actually serve users (e.g. its durable store is unavailable); it reports not-ready. Query it while the product can serve users; it reports ready.
- **release_gating**: true — the `/healthz` liveness probe at `c805525` reports process liveness only; a readiness meaning is required.

#### REQ-PROD-040 — Reachable and reasonably available
- **statement**: The product is reachable on the web and reasonably available when people return.
- **acceptance_criteria**: Over a sustained period, the product responds at its address with the core loop working; unavailability is the exception, not the norm (the availability target is the operational-readiness design's).
- **release_gating**: true

#### REQ-PROD-041 — Limits and quotas as a first line against abuse
- **statement**: The product enforces basic rate and volume limits so one actor cannot trivially overwhelm the service or flood others.
- **acceptance_criteria**: Exceed a reasonable rate of posting or requests; the product throttles or rejects the excess rather than serving it without limit.
- **release_gating**: true — a public write surface with no limits is a releasability concern for an internet-facing product.

### Finding people

#### REQ-PROD-042 — A way to find people and content to follow
- **statement**: The product offers some way to discover and find other users to follow, beyond already holding a link to a profile.
- **acceptance_criteria**: Signed in and holding no external link, find at least one other user to follow through the product itself (for example a search or a discovery/suggestion surface).
- **release_gating**: false — a first release can ship with follow-by-profile and follow-from-a-reply and add discovery as a near-term follow-up. This is the main social-completeness gap; the release bar should decide explicitly what minimum discovery v1 includes rather than leaving it absent by default.

---

## Traceability — needs and journeys to REQ-PROD

This maps the upstream fragments' needs and journeys to the ids above, so the coverage and
journey-to-requirement identities are checkable. The product kind's implications and every
end-to-end journey resolve to at least one `REQ-PROD-*` or to a recorded out-of-scope position.

### Product-kind implications → requirement or out-of-scope

| Kind implication (need handle) | Resolution |
|---|---|
| `need: real-account-signup-signin` | REQ-PROD-008, 010 |
| `need: account-recovery` | REQ-PROD-013 (via 012) |
| `need: authenticated-identity` | REQ-PROD-010 |
| `need: durable-account-data` | REQ-PROD-037 |
| `need: account-settings` | REQ-PROD-016, 017 |
| `need: account-deletion` | REQ-PROD-020, 021, 022 |
| `need: data-export` | REQ-PROD-019 |
| `need: authorization-boundary` | REQ-PROD-023 |
| `need: privacy-basics` | REQ-PROD-024 |
| `need: considered-states` | REQ-PROD-033, 034 |
| `need: works-on-mobile` | REQ-PROD-035 |
| `need: reachable-and-available` | REQ-PROD-040 |
| `need: help-and-abuse-reporting` | REQ-PROD-025, 026, 028 |
| `need: no-tenancy-or-billing` | Out of scope — tenancy/billing (reason below) |
| `need: releasable-bar-not-prototype` | The `release_gating: true` flags throughout; stated in scope below |

### Journeys → REQ-PROD (JOURNEY_TO_REQ)

| Journey | REQ-PROD |
|---|---|
| J1 First visit | 030, 031, 007 |
| J2 Sign-up | 008, 009, 012, 031 |
| J3 Sign-in | 010, 011 |
| J3a Recovery | 013, 012 |
| J3b Sign-out | 014 |
| J4 Core loop (post/read/reply/like/follow/profile) | 001, 002, 003, 004, 005, 006, 007, 042 |
| J5 Daily & returning use | 015, 032, 033, 034 |
| J6 Managing the account | 016, 017, 018 |
| J7 Safety & notifications | 025, 026, 027, 029 |
| J8 Leaving (export & deletion) | 019, 020, 021, 022 |
| J9 Operating the service | 037, 038, 039, 040, 028, 041 |
| J10 Self-hosting *(product-kind-dependent)* | REQ-PROD-037 holds for any deployment, so an instance someone runs inherits durability and the account-lifecycle requirements; chirp as a *supported self-hosting product* is out of scope (reason below). |

Two findings from the journeys break a basic releasable-product assumption and are gated
accordingly: handle-only authentication (REQ-PROD-010) — an account must be enterable only by
its owner — and the in-memory store (REQ-PROD-037) — what a person creates must still be there
next time.

---

## in_scope_out_of_scope

This consolidates the product-definition fragment's product-kind scope draft with what the
requirements above settle. chirp's one applicable product kind is a **hosted, public,
account-based consumer web application**; three other kinds (multi-tenant SaaS, commercial
off-the-shelf, open-source product) do not apply, and each shapes what is correctly left out.

### In scope — what a releasable chirp of this kind includes

- **The core loop, intact**: post a chirp including replies, read a paginated home timeline,
  view profiles, follow/unfollow, like/unlike (REQ-PROD-001–007). This exists at `c805525` and
  is the product's reason to exist.
- **Real accounts and the full account lifecycle**: sign-up that establishes a credential,
  owner-only sign-in, a verified recovery contact, self-service recovery, server-side sign-out,
  profile editing, a settings surface, data export, and account deletion with a defined,
  confirmed outcome (REQ-PROD-008–022). The authentication, session, and credential mechanisms
  are the identity/security design's detail.
- **An authorization boundary and privacy basics** (REQ-PROD-023–024): a person acts only as
  themselves, and private details stay private.
- **Safety, moderation, and operator support** (REQ-PROD-025–028): reporting and stated rules
  as the safety floor, a supported operator surface to assist users and action abuse, and
  controls to stop unwanted interaction (block/mute) as an expected near-term addition.
- **A baseline notifications story** (REQ-PROD-029): told when replied to, followed, or liked,
  with preferences.
- **A finished-feeling experience** (REQ-PROD-030–036): a public first-visit experience, a
  short path to sign-up, first-run onboarding off the empty state, considered empty/loading/
  error states, graceful session-expiry and transient-error recovery, a responsive layout that
  works on a phone, and an accessibility baseline. The screens, visual system, and exact a11y
  standard are the experience design's.
- **Durability and operational readiness to be a live service** (REQ-PROD-037–041): durable
  user data across restart and redeploy, a backup and recovery path, a trustworthy
  health/readiness signal, reachability and reasonable availability, and basic limits/quotas.
  The persistence model is the domain design's; backups, observability, limits, and
  availability targets are the operational-readiness design's.
- **A way to find people to follow** (REQ-PROD-042), at least minimally.

Requirements flagged `release_gating: false` above (REQ-PROD-004, 015, 018, 027, 029, 031, 042)
are **in scope and expected** but need not block a first release; the release-bar design stages
them across usable-early vs. releasable. Their being non-gating is a deliberate, reasoned call,
not an omission.

The detailed requirements and acceptance criteria owned by the sibling design areas —
`REQ-DOM-*` (domain & persistence), `REQ-UX-*` (experience), `REQ-ID-*` (identity/security),
`REQ-OPS-*` (operational readiness) — and the consolidated release bar (`BAR-*`) are out of
*this fragment's* scope but in scope for the design overall. This fragment states the
product-level requirement from the user's side and names the area that carries the detail; it
mints no other area's ids.

### Out of scope — with reasons

- **Tenancy, organizations, team management, and billing.** chirp is a single public product of
  individual accounts, and no money changes hands; the multi-tenant SaaS kind does not apply, so
  the tenancy, seat/team management, org-admin, and billing surfaces a SaaS buyer would assume
  are out of scope (`need: no-tenancy-or-billing`, as an explicit non-goal).
- **Customer-side install, licensing, and upgrade tooling.** chirp is operated as a hosted
  service, not distributed for customers to run in their own environment; the COTS kind does not
  apply.
- **Open-source community infrastructure** — a contribution guide, public issue/PR intake, and a
  self-host support commitment. The repository is a closed demonstration that does not accept
  contributions, so the OSS product kind does not apply. The container is self-hostable in
  principle and REQ-PROD-037 and the account-lifecycle requirements are written to hold for any
  deployment, so an instance someone runs inherits them; but chirp is not productized as a
  supported self-hosting product, so supporting self-hosters as a user base (persona P5, journey
  J10) is out of scope.
- **Native mobile applications.** chirp is a responsive web app (REQ-PROD-035); native iOS/
  Android clients are a separate product surface beyond the stated aim.
- **Rich social features beyond the core loop** — direct messages, full-text search beyond basic
  discovery, media and image uploads, trending/discovery feeds, verified badges, and multi-level
  threaded conversations beyond simple replies and reading a reply in context. These are
  candidates for later scope, not v1 commitments; a releasable chirp can ship without them.
  Basic discovery (REQ-PROD-042) and recording a reply's parent (REQ-PROD-003) are in scope; the
  richer forms are not. The release-bar design decides explicitly which, if any, a first release
  includes, rather than treating their absence as a defect.
- **The implementation "how"** — the persistence engine, the authentication protocol internals,
  framework internals, and every other build decision — is out of scope for the design and
  deferred to later code work. Each is stated here, where it belongs, as a requirement with a
  testable bar.
