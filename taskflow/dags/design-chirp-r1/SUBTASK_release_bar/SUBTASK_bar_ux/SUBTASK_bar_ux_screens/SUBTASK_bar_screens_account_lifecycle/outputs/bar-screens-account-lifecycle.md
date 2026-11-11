# Release bar — screens & flows: account management & lifecycle (`BAR-248..255`)

This fragment holds the release-gating account-lifecycle requirements of the screens band
(`REQ-UX-065..077` gating subset) to concrete, testable release conditions. Each `BAR-*` states what a
person who was not in the room can observe on the live product; it references the `REQ-UX-*` it enforces
(and the `REQ-PROD-*` those flows serve) and does not restate them. Requirements are defined in
`design/experience-design.md`.

Scope of this chapter: a signed-in person setting up, managing, and ending their own account — onboarding,
editing a profile, the settings hub, contact control and verification, sessions and sign-out, data export,
and account deletion. The id budget is tight by design (8 ids for 11 gating requirements), so related
requirements are clustered into one checkable condition rather than restated one-to-one.

Non-gating requirements in this band (`REQ-UX-071` handle-change position, `REQ-UX-072` notification
preferences) are out of coverage and are not the basis of any criterion here.

---

### BAR-248 — Onboarding explains the empty start and always offers a way off it, across every state
- **statement**: After a fresh sign-up, a brand-new account lands on the onboarding screen and sees, in
  plain language, why its timeline is empty and at least one working control that opens compose to write a
  first chirp (and, wherever discovery is present, a control to find people to follow). The explanation and
  the compose route appear immediately and stay usable while any suggestions preview is still loading — shown
  as placeholders, not a blank region — and after that preview fails or comes back empty. The screen is never
  a blank page and never leaves the person without a next step.
- **references**: REQ-UX-065, REQ-UX-066, REQ-PROD-032, REQ-PROD-033
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-249 — Editing a profile saves and shows the new values, validates at the field, and never loses typed input
- **statement**: A signed-in person can reach edit profile from the settings hub and from the edit action on
  their own profile, change their display name and bio, and save; the saved values then show on their
  profile. An empty required display name or a rejected value is reported against the field in plain words and
  no save is made; a save that fails is reported at the form with the person's edited values still present so
  they can retry; a save that succeeds is confirmed. The screen never reports success or failure silently and
  never shows a raw system or error code.
- **references**: REQ-UX-067, REQ-UX-068, REQ-PROD-016, REQ-PROD-033, REQ-PROD-034
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-250 — The settings hub lists every account section, each reachable by row and by URL with a way back, and treats delete as destructive
- **statement**: A signed-in person opening settings sees a labelled row for every account section in the
  release — edit profile, account & contact, sessions & devices, blocked & muted, export your data, and
  delete account (the notification-preferences row appears only where notifications are in the release). Each
  row opens its section both by selection and by entering the section's own URL directly in a fresh tab, and
  each section offers a labelled way back to the hub that works alongside the browser back control. The
  delete-account row is shown as destructive and opens a confirmation rather than deleting when selected. If
  the account summary fails to load, every section row is still reachable.
- **references**: REQ-UX-069, REQ-PROD-017
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-251 — A person can see, change, and prove control of their contact, and an unverified contact is treated as a caution, never as verified
- **statement**: On the account & contact screen a signed-in person sees their current point of contact with
  a status of either "Verified" or "Not verified yet". They can change the contact and save; the change is
  confirmed, the new contact shows as not-yet-verified, and the screen offers a step that confirms the person
  controls it before it is used for account recovery. An unverified contact is presented as a caution, not an
  error, and is not treated as verified until that step is completed. A failed save is shown against the
  contact field with the typed value preserved for retry.
- **references**: REQ-UX-070, REQ-PROD-012, REQ-PROD-017
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-252 — A person can see where the account is signed in and end another device's session, and that session stops working
- **statement**: A signed-in person opening sessions & devices sees every place the account is currently
  signed in, each with enough to recognise it — device and browser, approximate location, last-active time —
  and the current session marked. Ending another session goes through a confirmation that names the effect;
  after confirming, that session leaves the list and the next action attempted from the ended session on its
  own device is refused and requires a fresh sign-in.
- **references**: REQ-UX-073, REQ-PROD-017, REQ-PROD-014
- **verification_method**: operational_check
- **proposed_stage**: releasable

### BAR-253 — Signing out ends the session on the server and leaves nothing reachable by going back
- **statement**: A signed-in person can sign out from sessions & devices through a confirmation that, where
  the account is signed in elsewhere, offers to end those other sessions too. After sign-out the person is on
  the signed-out landing; the browser back control does not re-expose any protected screen; and replaying the
  signed-out session's request is refused, so the next person at that device is not signed in as them.
- **references**: REQ-UX-074, REQ-PROD-014
- **verification_method**: operational_check
- **proposed_stage**: usable_early

### BAR-254 — A person can request their data and obtain their chirps, profile, and follows in a form they can open elsewhere
- **statement**: From the export screen a signed-in person sees what the export contains and a single request
  action. After requesting, the screen shows a preparing state rather than freezing or blanking, and when
  ready offers a way to download the file; the downloaded file opens outside chirp and contains the person's
  chirps, their profile, and who they follow. A preparation that fails is explained in plain words with a
  retry, and no broken file is offered.
- **references**: REQ-UX-075, REQ-PROD-019
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-255 — Deletion states its consequence and runs only on explicit confirmation; cancelling changes nothing, and a completed deletion signs the person out with no way back
- **statement**: The delete-account confirmation, shown before anything is deleted, states plainly that the
  account and its chirps are removed and cannot be recovered, shows what is and is not retained and what
  happens to the handle (matching the product's stated deletion outcome), and points the person to export
  their data first. The delete action stays unavailable until the person gives the explicit confirmation it
  asks for. Cancelling at any point returns to settings with the account and its content unchanged and still
  able to sign in. Giving the confirmation and deleting signs the person out to the signed-out landing, after
  which the account can no longer sign in and the browser back control does not re-expose the deleted
  account's screens.
- **references**: REQ-UX-076, REQ-UX-077, REQ-PROD-020, REQ-PROD-021, REQ-PROD-022
- **verification_method**: operational_check
- **proposed_stage**: releasable

---

## Coverage note — account-lifecycle release-gating `REQ-UX-*` → `BAR-*`

Every release-gating requirement in this chapter is covered by at least one criterion above. This lets the
screens synthesis gate assert account-lifecycle gating coverage without re-deriving the set.

| Release-gating REQ-UX | Surface | Covered by |
|---|---|---|
| REQ-UX-065 | Onboarding — explains the empty timeline, offers a way off it | BAR-248 |
| REQ-UX-066 | Onboarding — never blanks or dead-ends across its states | BAR-248 |
| REQ-UX-067 | Edit profile — changes display name and bio and persists them | BAR-249 |
| REQ-UX-068 | Edit profile — validates in place, reports failures, keeps input | BAR-249 |
| REQ-UX-069 | Settings hub — lists every section, addressable, returns to hub | BAR-250 |
| REQ-UX-070 | Account & contact — view, update, confirm control of the contact | BAR-251 |
| REQ-UX-073 | Sessions & devices — see active sessions, end another's session | BAR-252 |
| REQ-UX-074 | Sign out — ends the session server-side, no back-leak | BAR-253 |
| REQ-UX-075 | Data export — request and obtain own data in a portable form | BAR-254 |
| REQ-UX-076 | Deletion — confirmation names consequence, retention, export-first | BAR-255 |
| REQ-UX-077 | Deletion — explicit confirmation only; cancel leaves intact | BAR-255 |

Coverage count: 11 of 11 release-gating `REQ-UX-*` in the account-lifecycle chapter, across `BAR-248..255`
(8 ids; three same-screen pairs clustered — onboarding `065+066`, edit profile `067+068`, deletion
`076+077`).

Not covered (non-gating, out of this chapter's gating set): REQ-UX-071 (handle-change position), REQ-UX-072
(notification preferences). Neither is the sole basis of any `BAR-*` here.

## Staging note (proposal; the screens synthesis gate finalizes within the screens view)

- **usable_early**: BAR-248 (a new account that dead-ends on an empty timeline cannot get started — this is
  part of the first-run path), BAR-253 (a sign-out that does not truly end the session, or that leaks
  protected screens via back on a shared device, is a trust breach that should not ship even in an early
  usable version).
- **releasable**: BAR-249, BAR-250, BAR-251, BAR-252, BAR-254, BAR-255 — full account management, session
  listing, data export, and self-serve deletion are expected at release but are not on the minimum path to
  using the core loop.

These are this chapter's proposals from the account-lifecycle view; `SUBTASK_bar_screens_synthesis` reconciles
them into one coherent per-`BAR-*` stage across the screens slice, and the UX and whole-bar synthesis may move
a criterion for wider coherence.
