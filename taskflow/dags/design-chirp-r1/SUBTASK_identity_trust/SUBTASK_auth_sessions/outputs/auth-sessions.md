# Authentication and Sessions

Chirp today lets a person sign in by typing a handle: the server opens a session for whoever
presents it. There is no secret, no proof of ownership, and no verification — anyone who knows a
handle can sign in as that account. That breaks the premise the whole product rests on, that a chirp
attributed to a person was posted by that person. The session the server issues has no expiry, no
server-side invalidation, and no sign-out; the app can forget its copy of the token, but the session
stays usable. On a shared device that leaves the account open to the next person.

This section specifies what real authentication and a session safe to expose on the public internet
must guarantee for chirp, from the user's and the attacker's side. It states requirements, not
mechanisms: it does not choose a password-hashing algorithm, a token format, or a session store.
Where a requirement implies an engineering "how" — hashing, transport configuration, the durable
store that holds session state, the enforcement of guess-rate limits — the requirement names the
property that must hold and leaves the build to the code and operational-readiness areas, which it
points to by name.

Two decisions set the boundary of this area. Chirp is a single public product of individual
accounts, not a tenant platform, so it carries no enterprise single-sign-on obligation. And the
account object, its sign-up, and its recovery flow are the `accounts_and_lifecycle` area's to own;
this area owns the **mechanism requirements** — what proving identity and holding a safe session must
guarantee — and references that sibling where sign-up or recovery establishes or resets the secret.

The credential a person proves with is referred to here as their **secret**. The requirements do not
mandate a password specifically; they mandate a secret only the owner holds, and the properties any
such secret and its session must satisfy.

## Requirements (REQ-ID-*)

### REQ-ID-030 — Sign-up establishes a secret, not a handle alone
- **statement**: Creating an account establishes a secret that only the account owner holds and that is required to sign in afterward; a handle by itself never stands in for that secret. (The sign-up flow that collects and confirms the secret is owned by the `accounts_and_lifecycle` area; this requirement fixes what that flow must result in.)
- **acceptance_criteria**: After an account is created, signing in requires presenting the secret set at sign-up. Knowing only the handle, with no secret, does not produce a session.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-008, REQ-PROD-010

### REQ-ID-031 — Sign-in only the account owner can pass
- **statement**: A session is granted only on presentation of the account's correct secret; presenting a known handle without the matching secret grants nothing.
- **acceptance_criteria**: Attempt to sign in to another account using only its handle (public information) and no secret, or a wrong secret; no session is granted and no authenticated action can be taken as that account. The legitimate owner, presenting the correct secret, is signed in.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-010

### REQ-ID-032 — The secret is the sole gate to a session
- **statement**: There is no path to an authenticated session that bypasses verification of the account's secret — no debug route, no handle-only fallback, no default or shared secret.
- **acceptance_criteria**: Inspection of the sign-in surface and any alternate entry points finds no route that issues a session without verifying the presented secret against the account.
- **release_gating**: true
- **verification_method**: inspection
- **traces_to**: REQ-PROD-010

### REQ-ID-033 — Not-found and failed-secret are distinguishable without leaking who exists
- **statement**: A person can tell "no such account" from "that secret did not match," enough to distinguish a mistyped handle from a wrong secret, without the product revealing which accounts exist beyond what it already makes public. (Chirp profiles and handles are public, so confirming that a handle resolves to an account discloses nothing not already public; the signal must not go further — for example by revealing a private contact or whether a contact is registered.)
- **acceptance_criteria**: Sign in with an unknown handle; the result lets you conclude the account does not exist, so you can proceed to sign-up. Sign in with a known handle and a wrong secret; the result is a failed sign-in you can retry or recover from. Neither path exposes a private attribute (such as a recovery contact) of any account.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-011

### REQ-ID-034 — The secret meets a stated strength expectation
- **statement**: The product requires a secret strong enough that it cannot be guessed by trying a handful of common values, and states that expectation to the person setting it. (The specific policy — minimum length, disallowed common values — is tuned by the experience and accounts areas; this requirement fixes that a stated, enforced minimum exists.)
- **acceptance_criteria**: Attempt to set a trivially weak secret (for example a short or well-known common value); it is rejected with guidance. A secret meeting the stated policy is accepted.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-008, REQ-PROD-010

### REQ-ID-035 — Repeated sign-in guessing is slowed and does not leak progress
- **statement**: Repeated failed sign-in attempts against an account or from a source are slowed, limited, or otherwise made to cost the attacker, so a secret cannot be found by high-volume guessing; the responses to guesses do not tell an attacker they are getting closer. The enforcement mechanics (counters, lockout windows, source limits) are owned by the operational-readiness limits requirements — this area states the anti-guessing property and names `REQ-OPS-*` for the enforcement detail, and does not mint `REQ-OPS-*`.
- **acceptance_criteria**: Drive many failed sign-in attempts against one account; attempts are throttled, delayed, or capped rather than answered at full speed indefinitely, and the throttled response does not distinguish "almost right" from "wrong."
- **release_gating**: true
- **verification_method**: automated_test
- **traces_to**: REQ-PROD-010, REQ-PROD-011

### REQ-ID-036 — The secret is never stored or returned in a recoverable form
- **statement**: The product cannot reveal any account's secret to anyone, including the account owner and operators: the secret is never returned by any surface and is never held in a form from which the original value can be read back. Recovery restores access by setting a new secret, not by retrieving the old one. (How the secret is protected at rest — hashing and its parameters — is the code area's "how"; this requirement fixes the externally observable property.)
- **acceptance_criteria**: No product surface (API response, export, settings screen, operator tool) returns an account's secret. The only supported way back in after losing a secret is to set a new one through recovery.
- **release_gating**: true
- **verification_method**: inspection
- **traces_to**: REQ-PROD-008, REQ-PROD-010

### REQ-ID-037 — A successful sign-in issues a session distinct from the secret
- **statement**: Authentication issues a session credential that the app then carries on the person's behalf for subsequent actions; this session credential is separate from the account secret, so routine requests never carry the secret itself.
- **acceptance_criteria**: Sign in; subsequent authenticated actions succeed while carrying only the issued session credential, not the account secret. The account secret is not present on requests after sign-in.
- **release_gating**: true
- **verification_method**: inspection
- **traces_to**: REQ-PROD-010

### REQ-ID-038 — Sessions have a bounded lifetime and expire
- **statement**: Every session has a bounded maximum lifetime after which it is no longer accepted; a session does not remain valid forever.
- **acceptance_criteria**: A session that has passed its maximum lifetime is rejected, and the person is returned to sign-in. The bound is a defined value, not open-ended.
- **release_gating**: true
- **verification_method**: operational_check
- **traces_to**: REQ-PROD-014, REQ-PROD-015

### REQ-ID-039 — Sign-out ends the session server-side
- **statement**: A person can sign out, and sign-out invalidates the session on the server so it can no longer be used — not merely dropping the app's local copy.
- **acceptance_criteria**: Sign out; then present the session that was in use (for example, replay the prior request). It is rejected. The next person at that device is not signed in as you.
- **release_gating**: true
- **verification_method**: operational_check
- **traces_to**: REQ-PROD-014

### REQ-ID-040 — Session validity is decided server-side and cannot be forged or extended by the client
- **statement**: Whether a session is valid, and until when, is determined by the server; a client cannot mint a session, extend its own session's lifetime, or alter whose session it is by changing what it presents. (The durable store that holds authoritative session state so it survives a server restart is a domain/operational concern — this requirement fixes that validity is server-authoritative and names `REQ-DOM-*`/`REQ-OPS-*` for the durable-store "how"; it does not mint them.)
- **acceptance_criteria**: Tampering with the presented session credential (altering its contents, substituting another account's identifier, or extending an expiry it encodes) does not yield a valid session for a different account or a longer life. A session accepted before a server restart behaves consistently with the invalidation and expiry rules after one.
- **release_gating**: true
- **verification_method**: automated_test
- **traces_to**: REQ-PROD-010, REQ-PROD-014

### REQ-ID-041 — The session credential is protected in transit
- **statement**: The session credential is exchanged only over an encrypted transport, so a network observer between the person and the product cannot read or capture it. (The transport configuration is the operational area's "how"; this requirement fixes that the session credential is never sent in the clear.)
- **acceptance_criteria**: The session credential is transmitted only over an encrypted channel; a request carrying it over an unencrypted channel is refused or redirected rather than served. Inspection confirms no path exchanges the session credential in cleartext.
- **release_gating**: true
- **verification_method**: inspection
- **traces_to**: REQ-PROD-010, REQ-PROD-014

### REQ-ID-042 — The session credential is not exposed where it can be stolen
- **statement**: The session credential is not placed where it leaks — not in URLs, not in logs, and not readable by page scripts that a cross-site attack could run — so that a stolen copy cannot be replayed as the owner.
- **acceptance_criteria**: Inspection of URLs, server and client logs, and the surfaces available to page scripts finds the session credential in none of them. A captured request intended to exfiltrate the credential through those channels yields nothing usable.
- **release_gating**: true
- **verification_method**: inspection
- **traces_to**: REQ-PROD-010, REQ-PROD-014

### REQ-ID-043 — A fresh session identity is established at sign-in (fixation resistance)
- **statement**: Signing in establishes a new session identity; a session identifier a person carried before authenticating cannot become an authenticated session. This prevents an attacker from fixing a known session identifier on a victim and inheriting it once the victim signs in.
- **acceptance_criteria**: Capture a pre-sign-in session identifier, then sign in; the identifier in force after sign-in differs from the pre-authentication one, and the old identifier does not carry authenticated privileges.
- **release_gating**: true
- **verification_method**: automated_test
- **traces_to**: REQ-PROD-010

### REQ-ID-044 — An expired, signed-out, or unknown session is rejected consistently
- **statement**: A session credential that is expired, has been signed out, or is not recognized is rejected the same way — treated as unauthenticated — and the person is returned to sign-in rather than shown a silent failure or a partial, half-authenticated state.
- **acceptance_criteria**: Present an expired session, a signed-out session, and a made-up session credential; each is rejected and routed to sign-in. None grants any authenticated action.
- **release_gating**: true
- **verification_method**: operational_check
- **traces_to**: REQ-PROD-014, REQ-PROD-015

### REQ-ID-045 — Each session is individually identifiable and independently revocable
- **statement**: A person's sessions are distinguishable from one another, so that one session (one device) can be ended without ending the others, and so the account-settings surface can list active sessions and end any of them. (The settings screen that lists and ends sessions is owned by `accounts_and_lifecycle` and the experience area under REQ-PROD-017; this requirement fixes the mechanism that makes per-session revocation possible.)
- **acceptance_criteria**: With two active sessions on two devices, end one; that one is rejected on its next use while the other keeps working. The set of a person's active sessions can be listed for the account-settings surface to present.
- **release_gating**: true
- **verification_method**: operational_check
- **traces_to**: REQ-PROD-014

### REQ-ID-046 — Recovery re-establishes the secret and does not reopen old sessions
- **statement**: When a person recovers access by setting a new secret (recovery itself is owned by `accounts_and_lifecycle`, REQ-PROD-013), the new secret takes effect for future sign-in and sessions that predate the reset are not silently left valid — a recovery triggered because the account may be compromised must be able to end the attacker's sessions.
- **acceptance_criteria**: Complete a recovery that sets a new secret; the old secret no longer signs in, and sessions established before the reset are ended (or the person is given the option to end them) rather than remaining usable.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-010, REQ-PROD-014

### REQ-ID-047 — Stay-signed-in on a trusted device is an explicit, opt-in choice
- **statement**: Remaining signed in across ordinary visits on a device is offered only as a choice the person makes for a device they treat as trusted, not a default applied to every device. On a device not marked trusted, the ordinary bounded session applies.
- **acceptance_criteria**: Sign in without choosing to be remembered; the ordinary session lifetime applies. Choose to stay signed in on a trusted device; you remain signed in across close-and-reopen within the allowed period.
- **release_gating**: false — staying signed in is a convenience, not a condition of a releasable product; a releasable chirp may require sign-in each visit (this mirrors REQ-PROD-015). Recorded so the choice is explicit rather than assumed.
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-015

### REQ-ID-048 — A remembered session is itself bounded and revocable
- **statement**: Where the stay-signed-in convenience of REQ-ID-047 is offered, the remembered session still has a bounded maximum lifetime and is subject to sign-out and server-side invalidation like any other session; "stay signed in" does not mean "forever" and does not create a session that cannot be ended.
- **acceptance_criteria**: With stay-signed-in chosen, confirm the remembered session expires at its stated maximum and that sign-out and a remote end-this-session action both invalidate it.
- **release_gating**: false — this requirement binds only if the optional convenience in REQ-ID-047 is offered; when it is offered, these bounds are mandatory and gate that feature.
- **verification_method**: operational_check
- **traces_to**: REQ-PROD-015, REQ-PROD-014

### REQ-ID-050 — Multi-factor authentication is out of scope for the release bar
- **statement**: A second authentication factor (MFA) is not required for chirp's release bar. The reason: chirp is a single public product of individual accounts with no enterprise or regulatory obligation that compels a second factor, and a well-formed single secret plus the session and anti-guessing requirements above meets the bar of "real auth, not a stub." The credential and session design must not foreclose adding MFA later as an opt-in protection.
- **acceptance_criteria**: The release does not depend on an MFA feature. Review of the credential and session design confirms no decision taken here would have to be undone to add an optional second factor later.
- **release_gating**: false — recorded as a deliberate scope decision with its reason, not an omission.
- **verification_method**: inspection
- **traces_to**: REQ-PROD-010

### REQ-ID-051 — Third-party / social sign-in is out of scope for the release bar
- **statement**: Signing in through a third-party or social identity provider is not required for chirp's release bar. The reason: chirp issues and holds its own account secret for individual accounts and has no enterprise single-sign-on obligation; adding a social provider brings its own account-linking, privacy, and provider-dependency surface that is not needed to reach a releasable product. The design must not foreclose adding a third-party sign-in option later.
- **acceptance_criteria**: The release does not depend on any third-party sign-in. Review of the sign-in and account-secret design confirms an external provider could be added later without reworking the owner-only sign-in guarantees above.
- **release_gating**: false — recorded as a deliberate scope decision with its reason, not an omission.
- **verification_method**: inspection
- **traces_to**: REQ-PROD-008, REQ-PROD-010

## Notes for synthesis

**Cross-area seams (handoffs this area depends on or feeds):**

- **Sign-up and recovery establish/reset the secret — owned by `accounts_and_lifecycle`.** REQ-ID-030 fixes what sign-up must result in (a real secret), and REQ-ID-046 fixes what a recovery-driven reset must do to old sessions, but the sign-up and "can't get in?" flows themselves are that sibling's (REQ-PROD-008, REQ-PROD-012, REQ-PROD-013). The seam: this area owns the guarantees, that area owns the flows that produce them.
- **The active-sessions settings surface — shared with `accounts_and_lifecycle` / experience.** REQ-ID-045 provides the mechanism (per-session identity and independent revocation); the screen that lists sessions and lets a person end them is REQ-PROD-017, owned by the accounts and experience areas. No duplication intended — one mechanism requirement here, the surface there.
- **Anti-guessing limits coordinate with `REQ-OPS-*`.** REQ-ID-035 states the property (repeated guessing is slowed and leaks no progress); the enforcement mechanics (counters, lockout windows, per-source limits) belong to the operational-readiness limits area. This area does not mint `REQ-OPS-*`; it names OPS for the enforcement "how" so the two do not diverge.
- **Durable session store — `REQ-DOM-*` / `REQ-OPS-*`.** REQ-ID-040 and REQ-ID-044 require that session validity, expiry, and invalidation are server-authoritative and behave consistently across a restart. Today's in-memory store loses sessions on restart; making session state durable is the domain/operational "how." Flagged so the operational-readiness durable-data requirement covers it.
- **Transport confidentiality — possible generalization by the threat-model synthesis.** REQ-ID-041 claims encrypted transport specifically for the session credential. If the synthesis prefers one product-wide transport-confidentiality requirement covering all private fields (not only the session credential), it may generalize this in the `REQ-ID-100..119` range; this area has scoped it to the session credential to keep the auth/session bar self-contained.

**Threat-to-requirement hints for the STRIDE threat model (synthesis owns the threat_model section):**

- **Spoofing an identity** (signing in as someone else): answered by REQ-ID-030–034, REQ-ID-036 (real secret, owner-only sign-in, no bypass, anti-guessing, no secret retrieval). This is the direct close of the critical handle-only gap.
- **Tampering / forged attribution** (acting as another account via a crafted session): answered by REQ-ID-040, REQ-ID-043 (server-authoritative validity, fresh session identity at sign-in).
- **Repudiation** (denying an action): partially answered here by per-session identity (REQ-ID-045); admin-action auditing belongs to the `authorization` area, flag for the threat model.
- **Information disclosure** (secret or session theft): answered by REQ-ID-036, REQ-ID-041, REQ-ID-042 (no recoverable secret, protected in transit, not placed where it leaks).
- **Denial of service** (credential-guessing or session-flooding load): the anti-guessing property is REQ-ID-035; the load/rate enforcement is `REQ-OPS-*` — the threat model should name the residual and point to OPS.
- **Elevation of privilege** (one session acting beyond its account): bounded here by server-authoritative sessions (REQ-ID-040); acting only as oneself is the `authorization` area's requirement.
- **Residual risk accepted for the bar:** with MFA out of scope (REQ-ID-050), a phished or guessed single secret remains a path to an account; the anti-guessing (REQ-ID-035), bounded/revocable sessions (REQ-ID-038, REQ-ID-039, REQ-ID-045), and recovery-ends-old-sessions (REQ-ID-046) requirements bound the damage and the recovery path. The threat model should record this as a known, accepted residual for the release bar, revisited if the account's sensitivity grows.

**Range use:** this area minted REQ-ID-030 through REQ-ID-051 (with 049 intentionally unused) within its allotted REQ-ID-030..059; ids 052–059 are left free for later additions in this concern.
</content>
</invoke>
