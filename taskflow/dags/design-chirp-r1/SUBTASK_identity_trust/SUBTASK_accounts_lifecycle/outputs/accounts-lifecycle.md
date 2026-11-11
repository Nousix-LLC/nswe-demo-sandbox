# Accounts and lifecycle

This section designs chirp's **account object** and the full life of an account — how a person
creates one, manages it, and ends it, and how they and their data leave. It states what must be
true from the account holder's side, to the bar of a releasable, publicly-exposed, account-based
consumer product. It is requirements, not implementation: where a "how" is tempting (how a
credential is hashed, how a session token is minted, how an export file is packaged), the design
names the area that owns it and stops there.

Two boundaries matter throughout. First, the **account depends on authentication but does not own
it.** Sign-up establishes a credential, recovery re-establishes one, and both end sessions — but
the credential, session, and sign-out *mechanisms* are the sibling `authentication_and_sessions`
area's requirements (`REQ-ID-030..059`). This section states the lifecycle events from the
account's side and names that area for the mechanism. Second, the account's **public/private field
boundary** is defined here as part of the account object, but who is *allowed* to read or change
each field is the `authorization` area's to enforce (`REQ-ID-060..079`); the retention and erasure
baseline deletion relies on is the `abuse_and_privacy_basics` area's (`REQ-ID-080..099`). Those
seams are recorded in the notes for synthesis.

The account lifecycle today is almost entirely absent. At `Nousix-LLC/nswe-demo@c805525`, signing
in is typing a handle, there is no credential, no verified contact, no recovery, no settings, no
profile edit, no export, and no deletion. Each requirement below closes one part of that gap and
says how a stranger would check it on the live product.

## The account object

An **account** is the thing a person owns and acts through. It comprises:

- a **handle** — the unique public identifier, up to 15 letters, digits, or underscores, that
  others follow, reply to, and see on every chirp;
- a **display name** and an optional **bio** — public, person-chosen presentation;
- a **verified point of contact** — private, used only for recovery and notifications;
- a **credential** — private, owned by the `authentication_and_sessions` area, that proves the
  account is the person's own;
- the person's **content and graph** — their chirps, who they follow, and what they liked — which
  the domain design (`REQ-DOM-*`) persists and this lifecycle governs on export and deletion.

The split between public fields (handle, display name, bio, public chirps, follower/following
counts) and private fields (contact, credential, session data) is the account's structural
privacy boundary. Defining the boundary is this section's job; enforcing who may read or write
across it is the `authorization` area's.

## Sign-up: establishing a real account

A releasable product cannot let one person claim another by typing a name. Sign-up must create an
account whose owner holds a secret, collect only what the account needs, and capture a contact the
product has confirmed the person controls — the basis for ever letting them back in.

## Managing the account: profile, settings, handle

Once in, a person expects to change how they appear and to reach the handful of account-level
choices the lifecycle implies — their contact, their active sessions, their notification
preferences — from one place. The handle is the exception: because others follow and address an
account by its handle, whether it can change is a stated product decision, not an open surface.

## Recovery: getting back in

A person who loses their credential must be able to return without another person acting for them,
and only through the contact the product verified at sign-up. Recovery is the account-side event;
the credential it re-establishes and the sessions it ends belong to the
`authentication_and_sessions` area.

## Leaving: export and deletion

The end of the relationship is part of the product. A person must be able to take their own data
out in a form they can open elsewhere, and to delete their account with a defined, confirmed
outcome for their content and their handle. A product a person cannot leave cleanly is one they do
not fully trust in the first place.

## Requirements (REQ-ID-*)

### REQ-ID-001 — The account object and its public/private field boundary
- **statement**: An account comprises a public identity (handle, display name, optional bio) and private account data (verified contact, credential, session data), plus the person's content and follow graph. Public fields are readable by any viewer; private fields are never part of any other user's view of the account.
- **acceptance_criteria**: View any account's public profile with no session: handle, display name, bio, and follower/following counts appear. Inspect every product surface that returns another account to a viewer: none returns that account's contact, credential, or session data.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-007, REQ-PROD-024

### REQ-ID-002 — Sign-up establishes a real credential
- **statement**: Creating an account establishes a secret the owner will later use to prove the account is theirs; a handle alone is never sufficient to act as the account. The credential mechanism is the `authentication_and_sessions` area's; from the account's side, an account does not exist in a usable state until such a credential is set.
- **acceptance_criteria**: Complete sign-up for a fresh handle; the account is created only once a credential is set. Then, knowing only the handle (not the credential), attempt to sign in as that account through any product surface: no session is granted.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-008

### REQ-ID-003 — Handle format and uniqueness with field-level feedback
- **statement**: Sign-up accepts a handle only if it is well-formed (up to 15 letters, digits, or underscores) and not already taken, reporting a taken or ill-formed handle against the handle field so the person can correct it.
- **acceptance_criteria**: Submit a handle already in use; sign-up reports a conflict naming the handle. Submit a handle with a space, a disallowed character, or more than 15 characters; sign-up reports a field-level error on the handle. Submit a valid, unused handle; it is accepted.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-009

### REQ-ID-004 — A verified point of contact captured at sign-up
- **statement**: Sign-up captures one point of contact for the account and records it as a private field, so recovery and important notifications have a basis. What kind of contact is collected and how it is protected in storage is a privacy/identity decision carried with `abuse_and_privacy_basics`.
- **acceptance_criteria**: During sign-up, provide a contact; after sign-up the account holds that contact as a private field (never shown to other users), and recovery (REQ-ID-013) and notifications can reference it.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-012

### REQ-ID-005 — The contact is confirmed before it is relied on
- **statement**: The product confirms the person controls the captured contact before using it for recovery or notifications; an unconfirmed contact is not a basis for regaining access.
- **acceptance_criteria**: Provide a contact at sign-up and do not complete its confirmation step; attempt recovery (REQ-ID-013) through that contact — it is not accepted as a recovery basis. Complete the confirmation step; the contact is then usable for recovery.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-012

### REQ-ID-006 — Sign-up collects only what the account needs
- **statement**: Sign-up asks for a handle, a display name, an optional bio, the credential, and one point of contact — and nothing beyond what the account requires.
- **acceptance_criteria**: Inspect the sign-up surface: the only fields requested are handle, display name, optional bio, credential, and one contact. No additional personal data is required to create an account.
- **release_gating**: false — the specific gated collection requirements are REQ-ID-002/003/004; "nothing extraneous" is a data-minimization expectation stated here for the sign-up surface and coordinated with `abuse_and_privacy_basics`, which owns the product-wide minimization baseline.
- **verification_method**: inspection
- **traces_to**: REQ-PROD-012, REQ-PROD-031

### REQ-ID-007 — Edit display name and bio after sign-up
- **statement**: A signed-in person can change their display name and bio after sign-up, under the same format rules as at sign-up, and the change persists and shows on their public profile.
- **acceptance_criteria**: Signed in, change your display name and bio and save; reload your public profile — the new values show. Submit an invalid display name or bio; the product reports a field-level error and does not save it.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-016

### REQ-ID-008 — An account settings surface
- **statement**: A signed-in person has one settings surface for their account-level choices — at minimum their verified contact, their active sessions/devices, and their notification preferences where notifications exist.
- **acceptance_criteria**: Signed in, open settings from the product's navigation; it presents, in one place, the verified contact, the active sessions/devices, and (where notifications exist) notification preferences.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-017

### REQ-ID-009 — View and update the verified contact in settings
- **statement**: From settings, a person can see their current verified contact and change it; a changed contact is confirmed (REQ-ID-005) before it replaces the old one as the recovery/notification basis.
- **acceptance_criteria**: In settings, view the current contact. Enter a new contact; until its confirmation step is completed, recovery and notifications still use the prior confirmed contact. Complete confirmation; the new contact takes over.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-017, REQ-PROD-012

### REQ-ID-010 — View and end active sessions/devices in settings
- **statement**: From settings, a person can see the sessions/devices currently signed in to their account and end any of them. Ending a session invalidates it; the invalidation mechanism is the `authentication_and_sessions` area's.
- **acceptance_criteria**: Signed in on two devices, open settings on one and view the active sessions; end the other session; the ended session can no longer act as the account (verify by attempting an action from it).
- **release_gating**: true
- **verification_method**: operational_check
- **traces_to**: REQ-PROD-017, REQ-PROD-014

### REQ-ID-011 — Notification preferences in settings
- **statement**: Where activity notifications exist, a person can set which categories they are notified about from the settings surface. The notification capability itself is carried by the notifications/abuse-privacy areas; this requirement places its preferences in account settings.
- **acceptance_criteria**: In settings, find notification preferences; turn one category off and confirm; notifications of that category stop. If notifications are not in the release, settings states that no preferences apply yet rather than showing an empty control.
- **release_gating**: false — activity notifications are a non-gating product requirement (REQ-PROD-029); the preference controls gate only when notifications ship. Recorded so the settings surface accounts for them rather than omitting the seam.
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-017, REQ-PROD-029

### REQ-ID-012 — A stated handle-change policy
- **statement**: The product states whether and how a handle can change after sign-up and behaves consistently with that statement. For the first release, a handle is **fixed for the life of the account**: it cannot be changed from any product surface, and the product states this where a person would look for the option. The reason: the handle is the public identifier others follow and address, so a change path carries redirect, follower-continuity, and impersonation questions a first release states as deferred rather than answers.
- **acceptance_criteria**: Find the product's stated position on handle changes; it says the handle is fixed. Search every account surface for a handle-change action; none exists, matching the stated position.
- **release_gating**: false — this is a decision-and-consistency requirement (per REQ-PROD-018, non-gating); a first release may ship with handles fixed provided that position is stated in the product.
- **verification_method**: inspection
- **traces_to**: REQ-PROD-018

### REQ-ID-013 — Self-service account recovery through the verified contact
- **statement**: A person who has lost their credential can regain access themselves, through the contact verified for the account, without another person acting on their behalf.
- **acceptance_criteria**: Having lost your credential, use a "can't get in?" path, prove control of the verified contact, and regain access to the account. A person who does not control that contact cannot complete recovery.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-013

### REQ-ID-014 — Recovery re-establishes a credential, gated on proven contact control
- **statement**: Recovery lets the owner set a new credential for the account only after they have proven control of the verified contact. Setting the credential is the `authentication_and_sessions` area's mechanism; this requirement binds recovery to re-establishing owner-held access rather than granting a session without a new secret.
- **acceptance_criteria**: Complete the recovery path by proving control of the verified contact; you are prompted to set a new credential, and afterward you sign in with that new credential. Reaching the credential-reset step without proving contact control is not possible.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-013, REQ-PROD-012

### REQ-ID-015 — Recovery resists non-owners and does not leak account existence
- **statement**: Recovery cannot be completed by anyone who does not control the verified contact, and the recovery surface does not reveal whether a given handle or contact has an account beyond what the product already makes public.
- **acceptance_criteria**: Attempt recovery for an account whose contact you do not control; it cannot be completed. Submit a handle or contact with no account to the recovery surface; the response does not disclose account existence differently in a way that enumerates accounts.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-013, REQ-PROD-011

### REQ-ID-016 — Recovery and credential reset end existing sessions
- **statement**: Completing recovery (and any credential reset) ends the account's existing sessions, so a lost or compromised credential does not leave old sessions active. The session-invalidation mechanism is the `authentication_and_sessions` area's.
- **acceptance_criteria**: Sign in, then from another context recover the account and set a new credential; the original session can no longer act as the account.
- **release_gating**: true
- **verification_method**: operational_check
- **traces_to**: REQ-PROD-013, REQ-PROD-014

### REQ-ID-017 — Self-service data export in a portable form
- **statement**: A signed-in person can obtain their own data — their chirps, their profile, and who they follow — themselves, in a form they can open outside chirp. The packaging format is deferred to code; the requirement is that the export is self-service and portable.
- **acceptance_criteria**: Signed in, request your data; you receive your posts, your profile, and your follow list as a file or download you can open outside chirp without special tooling.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-019

### REQ-ID-018 — Export is scoped to the requester's own account
- **statement**: An export contains only the requesting account's own data; it never includes another account's data. The authorization enforcement of "own account only" is the `authorization` area's.
- **acceptance_criteria**: Export your data; inspect the result — it contains your chirps, profile, and follows and no other account's records.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-019, REQ-PROD-024

### REQ-ID-019 — Export excludes secrets
- **statement**: An export never includes the account's credential or session data, and never includes another person's private contact (for example, contacts of accounts the person follows).
- **acceptance_criteria**: Inspect an export: it contains no credential and no session tokens, and no private contact data belonging to other accounts.
- **release_gating**: true
- **verification_method**: inspection
- **traces_to**: REQ-PROD-019, REQ-PROD-024

### REQ-ID-020 — Self-service account deletion
- **statement**: A signed-in person can delete their own account; afterward the account can no longer sign in, and the person's content is handled per the defined deletion outcome (REQ-ID-021).
- **acceptance_criteria**: Signed in, delete your account; afterward, attempting to sign in to that account fails, and the person's content has been handled as REQ-ID-021 states.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-020

### REQ-ID-021 — A defined outcome for a deleted account's content and handle
- **statement**: The product defines, states, and applies what deletion does to the person's content and handle. For the first release the defined outcome is: the person's chirps are removed from public view; a reply by another person that pointed at a now-deleted chirp shows a "chirp unavailable" placeholder rather than breaking the conversation, and like/reply counts adjust accordingly; and the freed handle is **retired, not immediately re-registerable**, so a departed account cannot be impersonated by someone claiming its handle. The retention/erasure timing behind "removed" is coordinated with `abuse_and_privacy_basics`.
- **acceptance_criteria**: Find the stated deletion outcome in the product. Delete an account whose chirps others replied to and liked; its chirps leave public view, replies to them show the unavailable placeholder, counts adjust, and the handle cannot be registered by a new sign-up (matching the stated outcome).
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-021

### REQ-ID-022 — Deletion is confirmed and explains what survives
- **statement**: Account deletion is confirmed before it happens and tells the person what will and will not survive, including that export (REQ-ID-017) is their chance to keep a copy; a person can cancel at the confirmation and nothing is deleted.
- **acceptance_criteria**: Initiate deletion; a confirmation explains the consequences and points to export, and deletion proceeds only after explicit confirmation. Cancel at the confirmation; the account and all content remain intact.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-022

### REQ-ID-023 — Deletion erases the account's private data
- **statement**: Deletion removes the account's private data — its verified contact, credential, and session records — so no private account data remains after deletion. The retention baseline and any legally required erasure window are coordinated with `abuse_and_privacy_basics`.
- **acceptance_criteria**: Delete an account; afterward the account's contact, credential, and session records are no longer present on any product surface or in an export, consistent with the stated retention baseline.
- **release_gating**: true
- **verification_method**: operational_check
- **traces_to**: REQ-PROD-020, REQ-PROD-024

### REQ-ID-024 — Deletion ends all active sessions
- **statement**: Deleting an account immediately ends all of that account's active sessions, so no session can continue to act as a deleted account. The session-invalidation mechanism is the `authentication_and_sessions` area's.
- **acceptance_criteria**: Signed in on two devices, delete the account from one; the other device's session can no longer act as the account.
- **release_gating**: true
- **verification_method**: operational_check
- **traces_to**: REQ-PROD-020, REQ-PROD-014

## Notes for synthesis

**Cross-area seams this section hands off (for the threat model and the consolidated register):**

- **Authentication/session mechanism (`authentication_and_sessions`, REQ-ID-030..059).** Four
  lifecycle events depend on it and name it rather than specify it: credential establishment at
  sign-up (REQ-ID-002), credential reset on recovery (REQ-ID-014), and session invalidation on
  recovery and on deletion (REQ-ID-016, REQ-ID-024, and the session-ending in REQ-ID-010). The
  threat model should pair these with that area's session-invalidation and credential-strength
  requirements; the account side asserts the event must happen, the auth side asserts how.
- **Authorization enforcement (`authorization`, REQ-ID-060..079).** The account object defines the
  public/private field boundary (REQ-ID-001) and that export/deletion act only on the requester's
  own account (REQ-ID-018, REQ-ID-020); the enforcement that a person may read/change only their
  own account is that area's. Flag any gap where the boundary is defined here but not enforced
  there.
- **Privacy, retention, erasure (`abuse_and_privacy_basics`, REQ-ID-080..099).** Deletion's "removed"
  and "erased" outcomes (REQ-ID-021, REQ-ID-023) rest on a retention/erasure baseline owned there,
  as does the product-wide data-minimization principle REQ-ID-006 states for the sign-up surface.
  The handle-retirement decision (REQ-ID-021) is an identity call made here; its interaction with
  any retention window should be reconciled at synthesis.
- **Notifications.** REQ-ID-011 places notification preferences in settings but does not create the
  notification capability (REQ-PROD-029, non-gating); if notifications are out of the release,
  REQ-ID-008/011 degrade cleanly (settings states no preferences apply yet).
- **Durability (`REQ-DOM-*` / `REQ-OPS-*`).** Every lifecycle requirement assumes the account and
  its content persist across restart and redeploy (REQ-PROD-037). That durability is the domain and
  operational-readiness areas'; none of the requirements here hold if data is not durable. Not
  minted here; noted so the parent synthesis records the dependency.

**REQ-PROD identity needs this section answers in full:** 008 (→002), 009 (→003), 012 (→004,005,009),
013 (→013,014,015,016), 016 (→007), 017 (→008,009,010,011), 018 (→012), 019 (→017,018,019),
020 (→020,023,024), 021 (→021,023), 022 (→022). REQ-PROD-014 (sign-out) and REQ-PROD-024 (privacy
basics) are *referenced* from the account side but owned by the auth and authorization/abuse-privacy
areas respectively — flagged so synthesis does not double-count ownership.

**Threats each cluster is meant to answer (hints for the STRIDE-style threat model):** sign-up +
credential (REQ-ID-002) answers *spoofing* an identity; the public/private boundary and export/erase
scoping (REQ-ID-001, 018, 019, 023) answer *information disclosure* of private fields; recovery
hardening (REQ-ID-015) answers *spoofing via the recovery path* and account enumeration; session
termination on recovery and deletion (REQ-ID-016, 024) answers *stale-session elevation*; the
handle-retirement outcome (REQ-ID-021) answers *post-deletion impersonation*.
