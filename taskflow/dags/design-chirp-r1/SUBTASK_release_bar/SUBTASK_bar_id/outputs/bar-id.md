# Release bar — identity, security & trust (BAR-300..399)

This fragment turns the **release-gating** `REQ-ID-*` from the identity & security design
(`design/identity-security.md`) into concrete, testable release conditions. Each `BAR-*` is a release
condition someone who was not in the room can check against the live product, not a restatement of the
requirement it enforces. One `BAR-*` may enforce several related `REQ-ID-*`; it is owned here when the
identity/trust area most centrally holds the gating requirement.

The bar proves a plain thing for a stranger's account: they can only get in with a secret they own, a
session that is safe to expose on the public internet carries them, they see and change only what is
theirs, they can recover access and leave with their data, and when they delete the account it is gone.

**Range**: `BAR-300 .. BAR-399` (this spoke's assigned partition). **Fields per block**: `id`,
`statement`, `references` (≥1 `REQ-ID-*`), `verification_method` (one of `manual_user_check`,
`automated_test`, `inspection`, `operational_check`), `proposed_stage` (`usable_early` | `releasable`).

**On `proposed_stage`**: the stage is this spoke's proposal from the identity/trust view. `usable_early`
is the irreducible floor the moment real accounts exist at all — real authentication, a safe session, the
authority boundary, transport and private-field confidentiality; without it the product is not safely
usable even in a closed early build. `releasable` is what a public launch requires on top — the full
account lifecycle rights (recovery, export, deletion), the operator and reporting surface, and the
anti-abuse depth. The one coherent cross-cutting MVP-vs-releasable line is the synthesis hub's to finalize;
it may move a `BAR-*` between stages for cross-area coherence, and the stage recorded in `release-bar.md`
is authoritative.

---

## Real authentication — no handle-only access

#### BAR-300 — A secret only the owner holds is required to sign in
- **statement**: Signing in to any account requires presenting the secret established at sign-up; knowing only a handle (public information) grants no session and no authenticated action on any product surface. There is no debug route, handle-only fallback, or default/shared secret that issues a session without verifying the presented secret against the account.
- **references**: REQ-ID-002, REQ-ID-030, REQ-ID-031, REQ-ID-032
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-301 — A secret cannot be set weak, and guessing is slowed and silent
- **statement**: A trivially weak secret (a short or well-known value) is rejected with guidance and a secret meeting the stated policy is accepted; repeated failed sign-in attempts against one account or from one source are throttled, delayed, or capped rather than answered at full speed indefinitely, and the throttled response does not distinguish "almost right" from "wrong."
- **references**: REQ-ID-034, REQ-ID-035
- **verification_method**: automated_test
- **proposed_stage**: usable_early

#### BAR-302 — No surface ever returns an account's secret
- **statement**: No product surface — API response, data export, settings screen, or operator tool — returns any account's secret or holds it in a form from which the original value can be read back; the only supported way back in after losing a secret is to set a new one through recovery.
- **references**: REQ-ID-036
- **verification_method**: inspection
- **proposed_stage**: usable_early

#### BAR-303 — Handle format and uniqueness are enforced with field-level feedback
- **statement**: Sign-up accepts a handle only if it is well-formed (up to 15 letters, digits, or underscores) and not already taken; a taken or ill-formed handle is reported as a field-level error on the handle so the person can correct it, and a valid unused handle is accepted.
- **references**: REQ-ID-003
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-304 — Sign-in signals "no such account" vs "wrong secret" without leaking private attributes
- **statement**: A sign-in with an unknown handle lets the person conclude the account does not exist (so they can proceed to sign-up); a sign-in with a known handle and a wrong secret is a retryable, recoverable failure; and neither path exposes a private attribute of any account (such as a recovery contact) beyond what the product already makes public.
- **references**: REQ-ID-033
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

---

## Sessions safe to expose on the public internet

#### BAR-305 — The session is distinct from the secret, server-authoritative, and unforgeable
- **statement**: A successful sign-in issues a session credential separate from the account secret, so routine authenticated requests never carry the secret; whether a session is valid and until when is decided server-side, and tampering with the presented session credential — altering its contents, substituting another account's identifier, or extending an encoded expiry — yields no valid or longer-lived session for any account.
- **references**: REQ-ID-037, REQ-ID-040
- **verification_method**: automated_test
- **proposed_stage**: usable_early

#### BAR-306 — Sessions expire and invalid sessions are rejected consistently
- **statement**: Every session has a bounded, defined maximum lifetime after which it is rejected and the person is returned to sign-in; an expired, signed-out, or unrecognized session credential is each rejected the same way (treated as unauthenticated, with no partial or half-authenticated state); and a session accepted before a server restart behaves consistently with the expiry and invalidation rules after one.
- **references**: REQ-ID-038, REQ-ID-044
- **verification_method**: operational_check
- **proposed_stage**: usable_early

#### BAR-307 — Sign-out ends the session on the server
- **statement**: A person can sign out, and sign-out invalidates the session server-side so the prior session credential can no longer act as the account — verified by replaying the prior request, which is rejected — and the next person at that device is not signed in as the previous one.
- **references**: REQ-ID-039
- **verification_method**: operational_check
- **proposed_stage**: usable_early

#### BAR-308 — Sessions are individually identifiable and independently revocable
- **statement**: A person's sessions are distinguishable from one another, so that ending one device's session rejects it on its next use while the others keep working, and the set of a person's active sessions can be listed for the account-settings surface to present.
- **references**: REQ-ID-045
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-309 — A fresh session identity is established at sign-in (fixation resistance)
- **statement**: Signing in establishes a new session identity; a session identifier carried before authentication does not become an authenticated session and carries no authenticated privileges after sign-in.
- **references**: REQ-ID-043
- **verification_method**: automated_test
- **proposed_stage**: usable_early

#### BAR-310 — The session credential is confidential in transit and never exposed where it can be stolen
- **statement**: The session credential is exchanged only over an encrypted transport — a request carrying it over an unencrypted channel is refused or redirected, never served — and it never appears in URLs, server or client logs, or storage readable by page scripts, so a network observer or an injected script cannot capture and replay it as the owner.
- **references**: REQ-ID-041, REQ-ID-042
- **verification_method**: inspection
- **proposed_stage**: usable_early

#### BAR-311 — Every private field is encrypted in transit, product-wide
- **statement**: Every private field the product exchanges with a person — the account secret at sign-up, sign-in, and recovery; the session credential; the verified contact; and the data-export payload — crosses the network only over an encrypted transport, and any request that would carry such a field in the clear is refused or redirected rather than served.
- **references**: REQ-ID-100
- **verification_method**: inspection
- **proposed_stage**: usable_early

---

## Authorization — who may see and change what

#### BAR-312 — A valid session is the sole basis of action authority (default-deny)
- **statement**: Every action that creates, changes, or removes data, and every read restricted to an owner, requires a valid authenticated session and is refused without one; any action not explicitly permitted by the authority model is refused rather than allowed by default.
- **references**: REQ-ID-060
- **verification_method**: automated_test
- **proposed_stage**: usable_early

#### BAR-313 — The read boundary holds: public, owner-only, owner-scoped
- **statement**: An account's public fields (handle, display name, bio, follower/following counts, public chirps with their reply and like counts) are readable by any viewer; its owner-only fields (verified contact, credential, active session/device list, notification preferences, settings, and any export payload) and its owner-scoped views (home timeline, account-management views) are returned only to the authenticated owner and never to another account or an unauthenticated viewer.
- **references**: REQ-ID-001, REQ-ID-061, REQ-ID-062, REQ-ID-063
- **verification_method**: automated_test
- **proposed_stage**: usable_early

#### BAR-314 — A person acts only as themselves, and attribution cannot be forged
- **statement**: Posting, replying, liking and unliking, and following and unfollowing are authorized for and performed as the signed-in actor and cannot be directed to take effect under another account's identity; the author recorded on any chirp, reply, like, or follow is set by the product from the authenticated session, not from actor-supplied input, and no surface lets an actor create or alter content attributed to another account.
- **references**: REQ-ID-064, REQ-ID-065, REQ-ID-068
- **verification_method**: automated_test
- **proposed_stage**: usable_early

#### BAR-315 — Change and removal authority is limited to the actor's own account and content
- **statement**: A signed-in person can change only their own profile, contact, notification preferences, and account settings, and can delete only their own chirps and their own account; every attempt to change or delete another account or its content through any surface is refused and leaves the other account unchanged.
- **references**: REQ-ID-066, REQ-ID-067
- **verification_method**: automated_test
- **proposed_stage**: usable_early

#### BAR-316 — A refused action discloses no owner-only data or private existence
- **statement**: When the authority model refuses a read or action, the response carries no owner-only field of the target account and reveals nothing about it beyond its already-public profile, and the refusal is consistent whether or not the target account exists, beyond what public lookup already discloses.
- **references**: REQ-ID-069
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

---

## Managing the account: profile, settings, contact

#### BAR-317 — A person can edit their display name and bio
- **statement**: A signed-in person can change their display name and bio under the same format rules as at sign-up; a valid change persists and shows on their public profile, and an invalid value is reported as a field-level error and not saved.
- **references**: REQ-ID-007
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-318 — One account-settings surface gathers the account-level choices
- **statement**: A signed-in person has one settings surface, reachable from the product's navigation, that presents in one place the verified contact, the active sessions/devices, and — where notifications exist — notification preferences.
- **references**: REQ-ID-008
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

#### BAR-319 — The verified contact can be viewed and changed, with the change confirmed before it takes over
- **statement**: From settings a person can view their current verified contact and enter a new one; the new contact becomes the recovery/notification basis only after its confirmation step is completed, and until then the prior confirmed contact remains in force.
- **references**: REQ-ID-009
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

#### BAR-320 — Active sessions can be viewed and ended from settings
- **statement**: From settings a person can see the sessions/devices currently signed in to their account and end any of them; an ended session can no longer act as the account.
- **references**: REQ-ID-010
- **verification_method**: operational_check
- **proposed_stage**: releasable

---

## Getting back in: verified contact and recovery

#### BAR-321 — A point of contact is captured at sign-up and confirmed before it is relied on
- **statement**: Sign-up captures one point of contact, stores it as a private field never shown to other users, and the product confirms the person controls it before using it for recovery or notifications; an unconfirmed contact is not accepted as a basis for regaining access.
- **references**: REQ-ID-004, REQ-ID-005
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

#### BAR-322 — Recovery is self-service and gated on proven control of the verified contact
- **statement**: A person who lost their credential can regain access themselves by proving control of the verified contact, is then prompted to set a new credential, and afterward signs in with it; the credential-reset step cannot be reached without proving contact control, and someone who does not control the contact cannot complete recovery.
- **references**: REQ-ID-013, REQ-ID-014
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

#### BAR-323 — Recovery does not enumerate accounts
- **statement**: The recovery surface does not reveal whether a given handle or contact has an account beyond what the product already makes public; submitting a handle or contact with no account does not disclose account existence in a way that enumerates accounts.
- **references**: REQ-ID-015
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

#### BAR-324 — Recovery and credential reset end the sessions that predate them
- **statement**: Completing recovery and setting a new credential ends the account's sessions that predate the reset (or offers the owner the option to end them), and the old secret no longer signs in, so a recovery prompted by a possible compromise can eject an attacker.
- **references**: REQ-ID-016, REQ-ID-046
- **verification_method**: operational_check
- **proposed_stage**: releasable

---

## Leaving: export and deletion

#### BAR-325 — A person can export their own data, self-service and portable, scoped to their account
- **statement**: A signed-in person can obtain their own data — their chirps, profile, and follow list — through the product without contacting an operator, in a form they can open outside chirp without special tooling; the export contains only the requesting account's data and no other account's records.
- **references**: REQ-ID-017, REQ-ID-018
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

#### BAR-326 — An export excludes secrets and other people's private data
- **statement**: A data export never includes the account's credential or session data, and never includes another person's private contact.
- **references**: REQ-ID-019
- **verification_method**: inspection
- **proposed_stage**: releasable

#### BAR-327 — Account deletion is self-service, confirmed, and reversible up to confirmation
- **statement**: A signed-in person can delete their own account after a confirmation that explains what will and will not survive and points to export as their chance to keep a copy; cancelling at the confirmation leaves the account and all content intact, and after deletion the account can no longer sign in.
- **references**: REQ-ID-020, REQ-ID-022
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

#### BAR-328 — Deletion applies the stated outcome for content and handle
- **statement**: Deletion applies the product's stated outcome: the person's chirps leave public view; a reply that pointed at a now-deleted chirp shows a "chirp unavailable" placeholder with like/reply counts adjusted rather than breaking the conversation; and the freed handle is retired — not immediately re-registerable — so a departed account cannot be impersonated by someone claiming its handle.
- **references**: REQ-ID-021
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

#### BAR-329 — Deletion erases private data and ends every session
- **statement**: Deleting an account erases its private data — verified contact, credential, and session records — so none remains on any product surface or in an export, and immediately ends all of the account's active sessions so none can continue to act as the deleted account.
- **references**: REQ-ID-023, REQ-ID-024, REQ-ID-088
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-330 — The data-rights baseline is stated and satisfied through the account's own surfaces
- **statement**: The product states, where a person can find it, a data-rights baseline — access and a portable copy of their own data, and erasure by deleting their account — and every part of it is satisfied through the account's own surfaces, with no step requiring the person to contact an operator by hand.
- **references**: REQ-ID-090
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

---

## Operator authority (the supported admin surface)

#### BAR-331 — Operator authority is a separate, provisioned, least-privilege role
- **statement**: The authority to perform the supported administrative actions — assist recovery, remove content, action an abusive account — is provisioned outside the ordinary sign-up/sign-in path and is carried by no ordinary session; an ordinary account attempting any operator action is refused, and the operator surface exposes no authority beyond the supported set.
- **references**: REQ-ID-070, REQ-ID-071
- **verification_method**: inspection
- **proposed_stage**: releasable

#### BAR-332 — Operators cannot impersonate users or read credentials
- **statement**: No operator action posts, replies, likes, or follows as a user, and no operator action returns any account's credential; assisting a recovery routes the user through their own verified contact rather than exposing or resetting the credential to the operator.
- **references**: REQ-ID-072
- **verification_method**: inspection
- **proposed_stage**: releasable

#### BAR-333 — Operator actions are attributable, auditable, and have a defined recorded outcome
- **statement**: Each operator action on an account or on content records which operator performed it, what was done, the target, and when, in a retained record not editable through the ordinary product surfaces; and operator content removal and account actioning apply the product's defined outcome (consistent with the account-deletion outcome), with the applied outcome recorded.
- **references**: REQ-ID-073, REQ-ID-074
- **verification_method**: operational_check
- **proposed_stage**: releasable

---

## Abuse resistance and the privacy floor

#### BAR-334 — A person can report a chirp or account against stated, in-product rules
- **statement**: A signed-in person can report a chirp or an account, receives an acknowledgement that the report was received, and can point the report at a specific rule; the rules that say what is and is not allowed are reachable from within the product without an external link.
- **references**: REQ-ID-080, REQ-ID-081
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

#### BAR-335 — Reports are captured and routed to the operator surface with enough context to act
- **statement**: A filed report is recorded and made available to the authorized operator/support surface with what was reported, by whom, against whom, and which rule — enough to act on — rather than merely acknowledged to the reporter and discarded.
- **references**: REQ-ID-082
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-336 — Rate and volume limits are a first line against flooding
- **statement**: The product throttles or rejects writes and requests from one account or client that exceed a reasonable rate rather than serving them without limit, while a legitimate user at a normal rate is not blocked.
- **references**: REQ-ID-085
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-337 — Automated account creation and mass abuse are resisted
- **statement**: The product slows, challenges, or rejects automated mass account creation at the public sign-up surface and resists automated high-volume writes from many fresh accounts, while a legitimate person signing up once is not blocked.
- **references**: REQ-ID-101
- **verification_method**: operational_check
- **proposed_stage**: releasable

#### BAR-338 — Private fields never reach another user or a public, report, or block/mute flow
- **statement**: Through every surface available to another user, to an unauthenticated visitor, and through the report/block/mute flows, only an account's public fields appear; its verified contact, credential, and session data are never returned to anyone else, and the credential is never returned to anyone in readable form.
- **references**: REQ-ID-087
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

#### BAR-339 — The product collects only the data an account needs
- **statement**: Every field that sign-up and the account surfaces collect and store maps to a stated account function — identity, authentication, recovery/contact, or profile — and no field is collected that no function needs.
- **references**: REQ-ID-086
- **verification_method**: inspection
- **proposed_stage**: releasable

---

## Coverage note — every release-gating `REQ-ID-*` and the `BAR-*` that covers it

This spoke's area has **63** release-gating `REQ-ID-*` (every `REQ-ID-*` with `release_gating: true` in
`design/identity-security.md`). Each is referenced by at least one `BAR-*` above. The synthesis gate can
assert `GATING_REQ_COVERAGE` for the identity area directly from this table without re-deriving the gating
set.

| Release-gating `REQ-ID-*` | Covered by |
|---|---|
| REQ-ID-001 | BAR-313 |
| REQ-ID-002 | BAR-300 |
| REQ-ID-003 | BAR-303 |
| REQ-ID-004 | BAR-321 |
| REQ-ID-005 | BAR-321 |
| REQ-ID-007 | BAR-317 |
| REQ-ID-008 | BAR-318 |
| REQ-ID-009 | BAR-319 |
| REQ-ID-010 | BAR-320 |
| REQ-ID-013 | BAR-322 |
| REQ-ID-014 | BAR-322 |
| REQ-ID-015 | BAR-323 |
| REQ-ID-016 | BAR-324 |
| REQ-ID-017 | BAR-325 |
| REQ-ID-018 | BAR-325 |
| REQ-ID-019 | BAR-326 |
| REQ-ID-020 | BAR-327 |
| REQ-ID-021 | BAR-328 |
| REQ-ID-022 | BAR-327 |
| REQ-ID-023 | BAR-329 |
| REQ-ID-024 | BAR-329 |
| REQ-ID-030 | BAR-300 |
| REQ-ID-031 | BAR-300 |
| REQ-ID-032 | BAR-300 |
| REQ-ID-033 | BAR-304 |
| REQ-ID-034 | BAR-301 |
| REQ-ID-035 | BAR-301 |
| REQ-ID-036 | BAR-302 |
| REQ-ID-037 | BAR-305 |
| REQ-ID-038 | BAR-306 |
| REQ-ID-039 | BAR-307 |
| REQ-ID-040 | BAR-305 |
| REQ-ID-041 | BAR-310 |
| REQ-ID-042 | BAR-310 |
| REQ-ID-043 | BAR-309 |
| REQ-ID-044 | BAR-306 |
| REQ-ID-045 | BAR-308 |
| REQ-ID-046 | BAR-324 |
| REQ-ID-060 | BAR-312 |
| REQ-ID-061 | BAR-313 |
| REQ-ID-062 | BAR-313 |
| REQ-ID-063 | BAR-313 |
| REQ-ID-064 | BAR-314 |
| REQ-ID-065 | BAR-314 |
| REQ-ID-066 | BAR-315 |
| REQ-ID-067 | BAR-315 |
| REQ-ID-068 | BAR-314 |
| REQ-ID-069 | BAR-316 |
| REQ-ID-070 | BAR-331 |
| REQ-ID-071 | BAR-331 |
| REQ-ID-072 | BAR-332 |
| REQ-ID-073 | BAR-333 |
| REQ-ID-074 | BAR-333 |
| REQ-ID-080 | BAR-334 |
| REQ-ID-081 | BAR-334 |
| REQ-ID-082 | BAR-335 |
| REQ-ID-085 | BAR-336 |
| REQ-ID-086 | BAR-339 |
| REQ-ID-087 | BAR-338 |
| REQ-ID-088 | BAR-329 |
| REQ-ID-090 | BAR-330 |
| REQ-ID-100 | BAR-311 |
| REQ-ID-101 | BAR-337 |

### Non-gating `REQ-ID-*` (in scope, not bar-gating — recorded, not covered by a `BAR-*`)

The design marks these `release_gating: false`, each with its stated reason; they are deliberately not held
by a `BAR-*` and are listed so the synthesis gate sees the omission is intentional, not a gap:
REQ-ID-006 (sign-up data-minimization expectation, covered product-wide by the gated REQ-ID-086/BAR-339),
REQ-ID-011 (notification preferences — gate only when notifications ship), REQ-ID-012 (handle-change
policy — fixed-handle decision), REQ-ID-047 and REQ-ID-048 (stay-signed-in convenience and its bounds),
REQ-ID-050 (MFA out of scope), REQ-ID-051 (third-party sign-in out of scope), REQ-ID-083 and REQ-ID-084
(block and mute — fast-follow; the synthesis hub decides whether v1 gates one, with the reporting floor at
BAR-334/335 gated regardless), and REQ-ID-089 (stated retention posture — minimum left to the bar).

### Notes on sibling-area dependencies (for the synthesis gate; no cross-area `BAR-*` minted here)

Several identity bars state a user- or operator-observable property whose enforcement depth is owned by a
sibling area; the design names this and does not mint sibling requirements, and neither does this spoke:

- **Durable storage.** BAR-305/306/307/308/320/324/329 (session validity, expiry, server-side sign-out,
  per-session revocation, deletion ending sessions) assume authoritative session and account state that
  survives a server restart — the domain and operational-readiness areas' durable-store concern. The
  identity bars fix the observable property; the durability that makes it hold across restart is checked by
  those areas' bars.
- **Limits and anti-automation depth.** BAR-301 (anti-guessing), BAR-336 (rate/volume limits), and BAR-337
  (anti-automation) state the first line; the thresholds, lockout windows, and tuning are the
  operational-readiness limits-and-quotas surface's to set and enforce.

No `BAR-*` outside `BAR-300..399` is authored here, and none of the inherited schema is redefined.
