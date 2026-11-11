# Authorization

Authorization is the question of **what each actor may see and change**, once authentication has
established *who the actor is*. Proving identity — passwords, sessions, recovery — is the sibling
authentication-and-sessions concern; this section takes a proven identity as given and specifies what
that identity is permitted to do, and what every viewer (including one with no identity at all) is
permitted to read.

chirp's authority model rests on one premise the whole product depends on: **a person acts only as
themselves**. A chirp carries the weight of *this person said this* only if no one else could have
posted, edited, or deleted it as them, and only if the private details behind an account stay with its
owner. The model has three parts, and they are one model seen from three sides:

- **The read boundary** — which fields any viewer may read without an account, which require a session,
  and which belong to the account owner alone.
- **Actor-scoped action authority** — a signed-in person may create, change, and remove only their own
  account and their own content, always attributed to themselves, never acting as another account.
- **Operator authority** — the separate, least-privilege, auditable authority the supported
  administrative surface needs to assist a user, remove content, and action an abusive account, held by
  provisioned operators rather than by any ordinary account.

Two framing rules run through all three parts. First, the model is **default-deny**: an action or a
read that is not explicitly permitted below is refused, so a surface added later does not silently
inherit authority no one granted it. Second, this section owns the **authority boundary** of the
public-versus-private field split — *who* may read or write each field — while the data-protection rules
for those same private fields (what is collected, how long it is kept, how it is erased on deletion)
belong to the abuse-and-privacy concern. The two are coordinated by naming the same field set, not by
restating each other's requirements.

### The field model this section authorizes against

The requirements below refer to a single field model, stated once here so each requirement can name it
without redefining it:

- **Public fields** (readable by any viewer, with or without a session): a user's handle, display name,
  bio, follower count and following count, and that user's public chirps with their reply and like
  counts. This is the set `REQ-PROD-007` and `REQ-PROD-024` name as public.
- **Owner-only fields** (readable and changeable only by the authenticated account owner): the verified
  contact, the authentication credential, the list of active sessions and devices, notification
  preferences, account settings, and any data-export payload.
- **Owner-scoped views** (composed for, and served to, one authenticated owner): the home timeline of
  the owner's own and followed accounts' chirps, and the account-management views.

Any field not listed as public is non-public by default. The *why* and the *lifecycle* of the owner-only
fields — minimization, retention, erasure on account deletion — are the abuse-and-privacy concern's to
state; this section fixes only who may read and write them.

### State today (grounded in `Nousix-LLC/nswe-demo` @ `c805525`)

A session identifies an actor, and actions run as that actor; a user's public profile is served without
a session. There is no model for what an actor may *not* do beyond its own account, no stated
public-versus-owner-only field boundary, and no operator authority at all — no separation between an
ordinary account and whoever administers the service, and no supported administrative action. The
requirements below specify the model the product is missing; the enforcement mechanism (how a session is
checked, how a field is withheld, how an operator is provisioned) is deferred to the `chirp-server` code
work in the `software` domain.

## Requirements (REQ-ID-*)

### REQ-ID-060 — Authenticated session is the sole basis of action authority (default-deny)
- **statement**: Every action that creates, changes, or removes data is authorized only for an actor with a valid authenticated session, and is refused otherwise; any action not explicitly permitted by this authority model is refused rather than allowed by default.
- **acceptance_criteria**: With no session, attempt each state-changing action the product exposes (post, reply, like, follow, edit profile, change a setting, delete content, delete account); each is refused. A read restricted to an owner (for example the account-settings view) is likewise refused without a session.
- **release_gating**: true
- **verification_method**: automated_test
- **traces_to**: REQ-PROD-023, REQ-PROD-010

### REQ-ID-061 — Unauthenticated read scope is limited to the public fields
- **statement**: A viewer with no session may read only the public fields — a user's handle, display name, bio, follower and following counts, and that user's public chirps with their reply and like counts — and nothing else.
- **acceptance_criteria**: With no session, open a user's profile and their chirps: the public fields are shown. Through the same unauthenticated surfaces, no owner-only field (contact, credential, session list, settings, notification preferences) is returned for that user or any other.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-007, REQ-PROD-024

### REQ-ID-062 — Owner-only fields are readable only by the account owner
- **statement**: The owner-only fields of an account — verified contact, authentication credential, active session and device list, notification preferences, account settings, and any data-export payload — are readable only by the authenticated owner of that account, and are never returned to another user or included in any public response.
- **acceptance_criteria**: Signed in as one account, attempt through every product surface to read another account's contact, session list, settings, or notification preferences; none is returned. Signed in as the owner, the same fields are readable for your own account only.
- **release_gating**: true
- **verification_method**: automated_test
- **traces_to**: REQ-PROD-024

### REQ-ID-063 — Owner-scoped views are served only to their owner
- **statement**: A view composed for one account — the home timeline of the owner's own and followed accounts' chirps, and the account-management views — is served only to the authenticated owner of that account, not to other accounts or to unauthenticated viewers.
- **acceptance_criteria**: Signed in as account A, request account A's home timeline and account views; they are served. Attempt to obtain account B's home timeline or account views while signed in as A, or with no session; neither is served.
- **release_gating**: true
- **verification_method**: automated_test
- **traces_to**: REQ-PROD-002, REQ-PROD-024

### REQ-ID-064 — A person acts only as themselves (no impersonation)
- **statement**: Every create, change, or remove action is authorized for, and carried out as, the authenticated actor of the session; the product provides no way for one account to act as, or on behalf of, another account.
- **acceptance_criteria**: Signed in as account A, attempt through the product's surfaces to post, reply, like, or follow as account B, or to edit account B's profile or settings; each is refused and nothing is recorded as B's action.
- **release_gating**: true
- **verification_method**: automated_test
- **traces_to**: REQ-PROD-023, REQ-PROD-010

### REQ-ID-065 — Social write actions are performed as the signed-in actor
- **statement**: Posting a chirp, replying, liking and unliking, and following and unfollowing are authorized only for the signed-in actor and are performed as that actor; they cannot be directed to take effect under another account's identity.
- **acceptance_criteria**: Signed in, post, reply, like, and follow; each is attributed to your handle. Attempt the same actions carrying another account's identity through any available parameter or surface; the action is refused or applied only to your own account, never to the other.
- **release_gating**: true
- **verification_method**: automated_test
- **traces_to**: REQ-PROD-001, REQ-PROD-003, REQ-PROD-005, REQ-PROD-006, REQ-PROD-023

### REQ-ID-066 — Change authority is limited to the actor's own account
- **statement**: A person may change only their own account — their profile (display name, bio), their contact, their notification preferences, and their account settings — and may not change any field of another account.
- **acceptance_criteria**: Signed in as account A, change A's display name, bio, contact, and settings; the changes take effect for A. Attempt to change any of the same for account B through any surface; each attempt is refused and B is unchanged.
- **release_gating**: true
- **verification_method**: automated_test
- **traces_to**: REQ-PROD-016, REQ-PROD-017, REQ-PROD-023

### REQ-ID-067 — Removal authority is limited to the actor's own content and account
- **statement**: A person may delete only their own chirps and may delete only their own account; they may not delete another account or another account's content.
- **acceptance_criteria**: Signed in as account A, delete a chirp A posted, and delete account A; both succeed. Attempt to delete a chirp authored by account B, or to delete account B, through any surface; each is refused and B's content and account remain.
- **release_gating**: true
- **verification_method**: automated_test
- **traces_to**: REQ-PROD-020, REQ-PROD-023

### REQ-ID-068 — Attribution is bound to the acting account and cannot be forged
- **statement**: The author recorded on a chirp, reply, like, or follow is the authenticated actor that performed it, set by the product from the session rather than from actor-supplied input, so that no actor can create or alter content attributed to another account.
- **acceptance_criteria**: Signed in as account A, create a chirp while supplying account B as the author through any available field; the stored chirp is attributed to A, or the request is refused — never attributed to B. No surface lets an actor change the author of existing content.
- **release_gating**: true
- **verification_method**: automated_test
- **traces_to**: REQ-PROD-023, REQ-PROD-001

### REQ-ID-069 — A refused action does not disclose owner-only data or private existence
- **statement**: When an action or read is refused by this authority model, the response carries no owner-only field and reveals nothing about another account beyond what is already public, so that probing the authority boundary cannot be used to read private data or to learn more than the public surface already shows.
- **acceptance_criteria**: Signed in as account A, attempt a refused cross-account read or change against account B; the refusal response contains no owner-only field of B and no information about B not already readable on B's public profile. The refusal is consistent whether or not B exists, beyond what public lookup already discloses.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-024, REQ-PROD-011

### REQ-ID-070 — Operator authority is a separate, provisioned role, not an ordinary account's
- **statement**: The authority to perform the supported administrative actions is held by provisioned operators and is distinct from ordinary-user authority; no account gains operator authority through ordinary sign-up or sign-in, and an ordinary session carries none of it.
- **acceptance_criteria**: Inspect how operator authority is granted; it is provisioned outside the ordinary sign-up/sign-in path. Signed in as an ordinary account, attempt each operator action (assist recovery, remove another's content, action an account); each is refused.
- **release_gating**: true
- **verification_method**: inspection
- **traces_to**: REQ-PROD-028

### REQ-ID-071 — Operators are authorized only for the supported, least-privilege action set
- **statement**: An operator is authorized to do only the supported administrative actions — assist a user's account recovery, remove content, and action (for example disable or suspend) an abusive account — and nothing beyond that set.
- **acceptance_criteria**: As a provisioned operator, perform each supported action and confirm it succeeds. Confirm, by inspecting the operator surface, that it exposes no authority beyond the supported set (for example it offers no way to read a credential or to post as a user).
- **release_gating**: true
- **verification_method**: inspection
- **traces_to**: REQ-PROD-028, REQ-PROD-025

### REQ-ID-072 — Operators cannot impersonate users or read authentication credentials
- **statement**: Operator authority does not allow posting or acting as a user, and does not allow reading any account's authentication credential; an operator's access to an owner-only field is limited to what a supported action requires (for example initiating a recovery the owner completes through their verified contact).
- **acceptance_criteria**: As an operator, confirm there is no action that posts, replies, likes, or follows as a user. Confirm no operator action returns an account's credential. Confirm that assisting recovery routes the user through their own verified contact rather than exposing or resetting the credential to the operator.
- **release_gating**: true
- **verification_method**: inspection
- **traces_to**: REQ-PROD-028, REQ-PROD-024

### REQ-ID-073 — Operator actions are attributable and auditable
- **statement**: Each operator action on an account or on content records which operator performed it, what was done, and when, and that record is retained so administrative actions can be reviewed and attributed after the fact.
- **acceptance_criteria**: As an operator, remove a chirp and action an account; afterward a retained record shows the operator identity, the action, the target, and the time for each. The record is available to review and is not editable through the ordinary product surfaces.
- **release_gating**: true
- **verification_method**: operational_check
- **traces_to**: REQ-PROD-028

### REQ-ID-074 — Operator removal and account actioning have a defined, recorded outcome
- **statement**: When an operator removes content or actions an account, the effect on that content and account is the product's defined outcome — consistent with the account-deletion outcome the accounts-and-lifecycle concern defines — and the applied outcome is recorded.
- **acceptance_criteria**: As an operator, remove a chirp and action an account; the resulting state of that content and account matches the product's stated outcome for each, and the applied outcome is recorded against the action.
- **release_gating**: true
- **verification_method**: inspection
- **traces_to**: REQ-PROD-028, REQ-PROD-021

## Notes for synthesis

**Cross-area seams (coordinated, not duplicated):**

- **Public-vs-private field split.** This section owns the *authority* boundary over the field model
  defined above (who may read/write each field: `REQ-ID-061`, `REQ-ID-062`, `REQ-ID-063`). The
  abuse-and-privacy concern owns the *data-protection* rules over the same owner-only field set
  (minimization, retention, erasure on deletion). The two name the same fields; neither restates the
  other. If the two sections describe the public set differently, reconcile to the set named here and in
  `REQ-PROD-007` / `REQ-PROD-024`.
- **Not-found vs failed-credential signalling.** `REQ-ID-069` (a refusal leaks nothing beyond the public
  surface) is the authorization side of the sign-in signalling the authentication-and-sessions concern
  owns (`REQ-PROD-011`). Keep the two consistent: neither authentication failures nor authorization
  refusals should disclose private existence.
- **Block/mute is not here.** The authority to suppress one account's interaction with or visibility to
  another (block/mute, `REQ-PROD-027`) is an interaction-control owned by the abuse-and-privacy concern;
  it is deliberately not minted in the `REQ-ID-060..079` range. If synthesis finds it unowned, it
  belongs to that sibling, not to this section.
- **Session invalidation / sign-out** (`REQ-PROD-014`) is the authentication-and-sessions concern's;
  `REQ-ID-060` depends on a valid session but does not define how a session is ended.
- **Recovery mechanism** referenced by `REQ-ID-072` (operator-assisted recovery routes through the
  owner's verified contact) is defined by accounts-and-lifecycle / authentication; this section fixes
  only that the operator cannot read or reset the credential directly.
- **Deletion outcome** referenced by `REQ-ID-074` is defined by accounts-and-lifecycle
  (`REQ-PROD-021`); this section fixes only that operator removal applies that same defined outcome.

**REQ-PROD coverage this section carries:** `REQ-PROD-023` (authorization boundary — `REQ-ID-060`,
`064`–`068`), `REQ-PROD-024` (privacy field boundary, authority side — `REQ-ID-061`, `062`, `063`,
`069`, `072`), `REQ-PROD-007` (unauthenticated public read — `REQ-ID-061`), `REQ-PROD-028` (supported
admin surface, authority side — `REQ-ID-070`–`074`). The admin *surface's* existence and shape are a
product/operational concern; this section specifies only the authority behind it.

**Threats each requirement answers (hints for the STRIDE threat model):**

- **Spoofing / elevation beyond one's own account** — `REQ-ID-060` (default-deny), `REQ-ID-064` (act as
  yourself), `REQ-ID-065` (social actions as the actor), `REQ-ID-070`–`072` (operator separation and
  least privilege, no impersonation).
- **Tampering with content or attribution** — `REQ-ID-066`, `REQ-ID-067` (change/remove only your own),
  `REQ-ID-068` (attribution bound to the actor, non-forgeable), `REQ-ID-074` (defined removal outcome).
- **Repudiation** — `REQ-ID-073` (operator actions attributable and auditable).
- **Information disclosure of private fields** — `REQ-ID-061`, `REQ-ID-062`, `REQ-ID-063` (read
  boundary), `REQ-ID-069` (refusals leak nothing), `REQ-ID-072` (no credential read by operators).

A cross-cutting transport/confidentiality requirement (private fields and session tokens protected in
transit) and an anti-automation requirement are candidates for the synthesis's own `REQ-ID-100..119`
range; they are noted here as not covered by this section so they are not assumed owned.
