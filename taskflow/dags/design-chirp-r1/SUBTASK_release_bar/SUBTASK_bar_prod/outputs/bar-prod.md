# Release bar — product area (BAR-001..099)

This fragment holds the product-area slice of chirp's release bar: the `BAR-*` criteria that enforce
every **release-gating** `REQ-PROD-*` from `design/product-requirements.md`. Each `BAR-*` is a release
condition someone who was not in the room can check against the live product — not a restatement of a
requirement. One criterion may enforce several related requirements; it names every `REQ-PROD-*` it
enforces. The `proposed_stage` on each is the product view of when the condition must hold; the release-bar
synthesis owns the final cross-cutting MVP-vs-releasable line.

Staging convention (proposed): `usable_early` is the first version a real person could actually use — the
core loop works, what they create persists, and their identity is real and safe. `releasable` is the full
public bar layered on top: the rest of the account lifecycle, leaving with and deleting their data, safety
and operator support, the finished-feeling experience, and operational readiness. Every `BAR-*` below is
release-gating; `usable_early` ones must hold by the earlier milestone, `releasable` ones by release.

The gating set this fragment covers is the 35 `REQ-PROD-*` flagged `release_gating: true`. The seven
non-gating requirements (REQ-PROD-004, 015, 018, 027, 029, 031, 042) are in scope and expected but need
not block a first release; they are staged by the product register itself and carry no `BAR-*` here.

---

## The core loop — what chirp is for

### BAR-001
- **statement**: A signed-in person can publish a chirp of 280 characters or fewer, attributed to their handle; an empty or over-limit message is refused and no chirp is created.
- **references**: REQ-PROD-001
- **verification_method**: automated_test
- **proposed_stage**: usable_early

### BAR-002
- **statement**: A signed-in person's home timeline returns their own chirps and those of the people they follow, newest first, in bounded pages reached by a cursor — never the entire history in one response.
- **references**: REQ-PROD-002
- **verification_method**: automated_test
- **proposed_stage**: usable_early

### BAR-003
- **statement**: A reply records the chirp it answers; a reply to a chirp that no longer exists is reported as not-found rather than accepted as though it succeeded.
- **references**: REQ-PROD-003
- **verification_method**: automated_test
- **proposed_stage**: usable_early

### BAR-004
- **statement**: Liking a chirp increases its like count by one; liking it again does not increase the count further; unliking returns the count — the like is idempotent and the displayed count matches the result.
- **references**: REQ-PROD-005
- **verification_method**: automated_test
- **proposed_stage**: usable_early

### BAR-005
- **statement**: Following a user brings that user's new chirps into the follower's timeline and is idempotent; unfollowing removes them; a person cannot follow their own account.
- **references**: REQ-PROD-006
- **verification_method**: automated_test
- **proposed_stage**: usable_early

### BAR-006
- **statement**: A user's public profile — handle, display name, bio, and follower/following counts — is viewable with no session.
- **references**: REQ-PROD-007
- **verification_method**: automated_test
- **proposed_stage**: usable_early

---

## Real accounts and owner-only identity

### BAR-007
- **statement**: Sign-up establishes a secret the person later uses to prove the account is theirs; an account created at sign-up cannot be entered by knowledge of its handle alone.
- **references**: REQ-PROD-008
- **verification_method**: automated_test
- **proposed_stage**: usable_early

### BAR-008
- **statement**: Sign-up enforces handle format (up to 15 letters, digits, or underscores) and uniqueness, reporting a taken handle as a conflict naming it and an ill-formed handle as a field-level error; a valid, unused handle is accepted.
- **references**: REQ-PROD-009
- **verification_method**: automated_test
- **proposed_stage**: usable_early

### BAR-009
- **statement**: Presenting only another account's handle, without its credential, grants no session; the legitimate owner presenting the credential set at sign-up or recovery is signed in.
- **references**: REQ-PROD-010
- **verification_method**: automated_test
- **proposed_stage**: usable_early

### BAR-010
- **statement**: A sign-in attempt lets the person tell "no such account" from "credential did not match" — enough to distinguish a typo from a wrong secret — without revealing which accounts exist beyond what the product already makes public.
- **references**: REQ-PROD-011
- **verification_method**: automated_test
- **proposed_stage**: releasable

### BAR-011
- **statement**: Signed in as one account, every attempt through the product's surfaces to act as another account — post, reply, like, or follow as them, edit their profile or settings, or delete their content — is refused.
- **references**: REQ-PROD-023
- **verification_method**: automated_test
- **proposed_stage**: usable_early

### BAR-012
- **statement**: A person's contact, credential, and session data are never returned to another user or in any public response; only the public fields (handle, display name, bio, public chirps, counts) are exposed.
- **references**: REQ-PROD-024
- **verification_method**: automated_test
- **proposed_stage**: usable_early

---

## Durability — what a person creates is still there

### BAR-013
- **statement**: After the service is restarted, updated, or redeployed, an account created beforehand still exists and its chirps, follows, and likes are still present on the next sign-in. The in-memory store at `c805525`, which loses everything on restart, does not meet this.
- **references**: REQ-PROD-037
- **verification_method**: operational_check
- **proposed_stage**: usable_early

---

## The rest of the account lifecycle

### BAR-014
- **statement**: An account has a point of contact that the product confirms the person controls (a verification step) before it is relied on for recovery or important notices; the contact is kept minimal.
- **references**: REQ-PROD-012
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-015
- **statement**: A person who has lost their credential can regain access themselves by proving control of the verified contact, with no one acting on their behalf; a person without that verified contact cannot recover the account.
- **references**: REQ-PROD-013
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-016
- **statement**: After a person signs out, the session that was in use can no longer be used — replaying the prior request with it is rejected — so the next person at a shared device is not signed in as them.
- **references**: REQ-PROD-014
- **verification_method**: automated_test
- **proposed_stage**: releasable

### BAR-017
- **statement**: A signed-in person can change their display name and bio, and the change persists and shows on their profile on the next view.
- **references**: REQ-PROD-016
- **verification_method**: automated_test
- **proposed_stage**: releasable

### BAR-018
- **statement**: A signed-in person has a settings surface where they can view and update their verified contact and view and end their active sessions or devices.
- **references**: REQ-PROD-017
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

---

## Leaving — export and deletion

### BAR-019
- **statement**: A signed-in person can obtain their own data — their chirps, profile, and follow list — in a portable form they can open and read outside chirp.
- **references**: REQ-PROD-019
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-020
- **statement**: A signed-in person can delete their own account; afterward the account can no longer sign in and the person's content is removed per the stated deletion outcome.
- **references**: REQ-PROD-020
- **verification_method**: automated_test
- **proposed_stage**: releasable

### BAR-021
- **statement**: The product states a definite outcome for deletion — what becomes of the person's chirps that others replied to or liked, and whether the freed handle can be re-registered — and its behavior after a deletion matches that stated outcome.
- **references**: REQ-PROD-021
- **verification_method**: inspection
- **proposed_stage**: releasable

### BAR-022
- **statement**: Deletion is confirmed before it happens and explains what will and will not survive — including that export is the person's chance to keep a copy; cancelling at the confirmation deletes nothing.
- **references**: REQ-PROD-022
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

---

## Safety, moderation, and operator support

### BAR-023
- **statement**: A signed-in person can report a chirp and report an account, and each submission is acknowledged as received.
- **references**: REQ-PROD-025
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-024
- **statement**: The product states the rules — what is and is not allowed — within the product, and a report can point to them.
- **references**: REQ-PROD-026
- **verification_method**: inspection
- **proposed_stage**: releasable

### BAR-025
- **statement**: Through a supported interface, the operator can assist a user's recovery, remove a named chirp, and disable or action an abusive account, none of which requires editing stored data by hand.
- **references**: REQ-PROD-028
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

---

## A finished-feeling experience

### BAR-026
- **statement**: A visitor arriving with no account and no session sees an explanation of what chirp is and a clear path to sign up, rather than being stopped at a sign-in wall.
- **references**: REQ-PROD-030
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-027
- **statement**: Immediately after sign-up, with no follows and no posts, the person sees guidance explaining the empty state and at least one actionable way toward a non-empty timeline, not a blank page.
- **references**: REQ-PROD-032
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-028
- **statement**: An empty list, a loading list, and a failed action each present a state the person can understand and act on, rather than a blank area or a silent failure.
- **references**: REQ-PROD-033
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-029
- **statement**: An expired or invalid session routes the person to sign-in with their place explained rather than failing silently; a transient server error while posting can be recovered by retry without losing the drafted chirp.
- **references**: REQ-PROD-034
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-030
- **statement**: On a typical phone viewport, a person can read the timeline, compose and post, reply, like, follow, and view a profile with no broken layout or unreachable controls.
- **references**: REQ-PROD-035
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-031
- **statement**: Using keyboard navigation and a screen reader, a person can complete the core loop (read the timeline, compose and post, reply, like, follow, view a profile), and the controls expose accessible names and roles, to the baseline the experience design sets.
- **references**: REQ-PROD-036
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

---

## Operational readiness to be a live service

### BAR-032
- **statement**: An operator can produce a backup of user data and restore from it, bringing back accounts, chirps, and follows.
- **references**: REQ-PROD-038
- **verification_method**: operational_check
- **proposed_stage**: releasable

### BAR-033
- **statement**: The health/readiness signal reports not-ready when the product cannot actually serve users (for example its durable store is unavailable) and ready when it can — it means "serving users," not merely "the process is running."
- **references**: REQ-PROD-039
- **verification_method**: operational_check
- **proposed_stage**: releasable

### BAR-034
- **statement**: Over a sustained period the product responds at its address with the core loop working; unavailability is the exception, measured against the availability target the operational-readiness design sets.
- **references**: REQ-PROD-040
- **verification_method**: operational_check
- **proposed_stage**: releasable

### BAR-035
- **statement**: Posting or requesting beyond a reasonable rate is throttled or rejected rather than served without limit, so one actor cannot trivially overwhelm the service or flood others.
- **references**: REQ-PROD-041
- **verification_method**: operational_check
- **proposed_stage**: releasable

---

## Coverage note — release-gating REQ-PROD-* → BAR-*

Every `REQ-PROD-*` flagged `release_gating: true` in `design/product-requirements.md` and the `BAR-*`
that covers it. This lets the release-bar synthesis assert GATING_REQ_COVERAGE for the product area
without re-deriving the gating set.

| Release-gating REQ-PROD-* | Covered by |
|---|---|
| REQ-PROD-001 (post a chirp) | BAR-001 |
| REQ-PROD-002 (home timeline) | BAR-002 |
| REQ-PROD-003 (reply records parent) | BAR-003 |
| REQ-PROD-005 (like/unlike idempotent) | BAR-004 |
| REQ-PROD-006 (follow/unfollow) | BAR-005 |
| REQ-PROD-007 (public profile) | BAR-006 |
| REQ-PROD-008 (real credential at sign-up) | BAR-007 |
| REQ-PROD-009 (handle validation/uniqueness) | BAR-008 |
| REQ-PROD-010 (owner-only sign-in) | BAR-009 |
| REQ-PROD-011 (not-found vs failed-credential signal) | BAR-010 |
| REQ-PROD-012 (verified point of contact) | BAR-014 |
| REQ-PROD-013 (self-service recovery) | BAR-015 |
| REQ-PROD-014 (sign-out ends session server-side) | BAR-016 |
| REQ-PROD-016 (edit profile) | BAR-017 |
| REQ-PROD-017 (account settings surface) | BAR-018 |
| REQ-PROD-019 (data export) | BAR-019 |
| REQ-PROD-020 (account deletion) | BAR-020 |
| REQ-PROD-021 (defined deletion outcome) | BAR-021 |
| REQ-PROD-022 (confirmed, explained deletion) | BAR-022 |
| REQ-PROD-023 (authorization boundary) | BAR-011 |
| REQ-PROD-024 (privacy basics) | BAR-012 |
| REQ-PROD-025 (report abuse) | BAR-023 |
| REQ-PROD-026 (stated rules) | BAR-024 |
| REQ-PROD-028 (operator/support surface) | BAR-025 |
| REQ-PROD-030 (public first-visit experience) | BAR-026 |
| REQ-PROD-032 (first-run onboarding) | BAR-027 |
| REQ-PROD-033 (considered empty/loading/error states) | BAR-028 |
| REQ-PROD-034 (graceful session-expiry/error recovery) | BAR-029 |
| REQ-PROD-035 (works on a phone) | BAR-030 |
| REQ-PROD-036 (accessibility baseline) | BAR-031 |
| REQ-PROD-037 (durable data across restart/redeploy) | BAR-013 |
| REQ-PROD-038 (backup and recovery) | BAR-032 |
| REQ-PROD-039 (trustworthy readiness signal) | BAR-033 |
| REQ-PROD-040 (reachable and available) | BAR-034 |
| REQ-PROD-041 (limits and quotas) | BAR-035 |

**Gating count**: 35 release-gating `REQ-PROD-*`, each referenced by at least one `BAR-*`.
**Non-gating (no BAR here, staged by the product register)**: REQ-PROD-004, 015, 018, 027, 029, 031, 042.
**Range used**: BAR-001..BAR-035, within the product-area range BAR-001..099. No id outside the range; no gaps that hide a dropped requirement.

### Proposed staging summary
- **usable_early** (12): BAR-001, BAR-002, BAR-003, BAR-004, BAR-005, BAR-006, BAR-007, BAR-008, BAR-009, BAR-011, BAR-012, BAR-013 — the core loop, owner-only real identity, the authorization/privacy boundary that real accounts require, and durable data.
- **releasable** (23): BAR-010, BAR-014 through BAR-035 — the clear sign-in signal, the rest of the account lifecycle, leaving (export and deletion), safety and operator support, the finished-feeling experience, and operational readiness.

The synthesis hub may move a criterion between stages for cross-area coherence; the final per-`BAR-*`
stage recorded in `release-bar.md` is authoritative.
