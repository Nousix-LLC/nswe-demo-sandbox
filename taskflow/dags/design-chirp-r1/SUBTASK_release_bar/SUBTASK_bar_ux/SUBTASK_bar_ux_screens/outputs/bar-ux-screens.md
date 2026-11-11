# Release bar — screens & flows (BAR-230..263)

Assembled release conditions for the screens and flows band of the UX release bar. The 34 criteria
below (`BAR-230..263`) hold every release-gating `REQ-UX-040..089` in this band to a checkable
release condition — stated as something a person who was not in the room can confirm against the
live product. Each criterion references the requirement(s) it enforces; it does not restate them. The
authoritative requirements are in `design/experience-design.md`.

Fields per block: `id`, `statement`, `references` (the `REQ-*` it enforces), `verification_method`
(one of `manual_user_check`, `automated_test`, `inspection`, `operational_check`), `stage`
(`usable_early` | `releasable` — the finalized screens-view stage; the parent UX hub and the
whole-bar synthesis own the wider line and may still move any criterion).

---

## Entry & auth (BAR-230..237)

### BAR-230
- **statement**: With no session, opening the site root reaches a Landing that says what chirp is
  and shows both a Sign up and a Sign in action, each reachable without first signing in. Where a
  public sample is served it shows real public chirps; where none is served the Landing still
  explains chirp and offers both actions rather than a blank area.
- **references**: REQ-UX-040 (REQ-PROD-030, REQ-PROD-031)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-231
- **statement**: The Sign up screen collects a handle, a display name, an optional bio marked
  optional, a credential, and a point of contact — and no fields beyond these — and on submit with
  valid values creates the account and signs the person in. The contact is shown as pending
  verification and is not treated as confirmed until it is verified.
- **references**: REQ-UX-041, REQ-UX-043 (REQ-PROD-008, REQ-PROD-012, REQ-PROD-031)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-232
- **statement**: On the Sign up screen a handle that is already taken, or that breaks the rule (more
  than 15 characters, or anything other than letters, numbers, or underscores), is reported inline
  against the handle field so the person can fix it before submitting, and a valid unused handle
  resolves to accepted. The check does not disclose which other handles exist beyond the conflict it
  reports.
- **references**: REQ-UX-042 (REQ-PROD-009)
- **verification_method**: automated_test
- **stage**: usable_early

### BAR-233
- **statement**: Signing in requires the credential set at sign-up or recovery — a known handle
  alone never grants a session. A handle that matches no account returns a not-found result with a
  path to Sign up; a real handle with a wrong credential returns a failed sign-in the person can
  retry or recover from, with a path to Recover access. Neither result reveals account existence
  beyond what a public profile already shows, and neither shows a system code.
- **references**: REQ-UX-044, REQ-UX-045 (REQ-PROD-010, REQ-PROD-011)
- **verification_method**: automated_test
- **stage**: usable_early

### BAR-234
- **statement**: A person who cannot sign in can start recovery themselves from a Recover access
  screen that runs through the account's verified contact. Submitting a contact returns the same
  neutral acknowledgement whether or not it matches an account, so the response discloses no account
  existence. Following a valid recovery step opens a Set new credential screen, and after setting a
  new credential the person is routed to Sign in and can sign in with it. An expired or already-used
  recovery link is explained with a path back to Recover access rather than a dead end.
- **references**: REQ-UX-046, REQ-UX-047 (REQ-PROD-013, REQ-PROD-012)
- **verification_method**: automated_test
- **stage**: releasable

### BAR-235
- **statement**: Signing out is confirmed before it proceeds; the confirmation names the consequence
  and offers both a cancel and an option to end sessions on all other devices. Confirming ends the
  current session on the server — the prior session can no longer be used — and lands the person on
  the signed-out Landing. Cancelling changes nothing. A sign-out that fails is reported and leaves
  the person signed in rather than appearing to succeed.
- **references**: REQ-UX-048 (REQ-PROD-014)
- **verification_method**: automated_test
- **stage**: usable_early

### BAR-236
- **statement**: Each of the Landing, Sign up, Sign in, Recover access, Set new credential, and Sign
  out surfaces presents a designed state for empty, loading, and error — a field-level message, a
  busy control, a skeleton, or an explained error with a next step — rather than a blank area, a
  hang, or a silent failure. Where a state does not apply to a surface, that is stated rather than
  left undesigned.
- **references**: REQ-UX-049 (REQ-PROD-033, REQ-PROD-034)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-237
- **statement**: A completed sign-up lands the person on the onboarding screen, not a sign-in prompt
  or a blank page. A person routed from a signed-in-only screen to Sign in lands back on the screen
  they asked for after signing in. After signing out, pressing back does not show the protected
  screen's content. (The three-way links among Sign in, Sign up, and Recover access ride the
  non-gating REQ-UX-015 and are not part of this release condition; a first release may omit them
  provided Recover access stays reachable from Help & support.)
- **references**: REQ-UX-050 (REQ-PROD-032, REQ-PROD-014)
- **verification_method**: automated_test
- **stage**: releasable

---

## Home timeline & compose (BAR-238..242)

### BAR-238
- **statement**: A signed-in person who opens the home destination sees a timeline carrying their own
  chirps and the chirps of the accounts they follow, ordered newest first, and the signed-in shell
  marks Home as the current destination. The timeline arrives as a bounded first page with a visible
  control to load older chirps; using that control brings in a further bounded page, and at no point
  does the product load the entire timeline in one request. Following at least one account that has
  posted, the person sees those chirps interleaved with their own in newest-first order.
- **references**: REQ-UX-051 (REQ-PROD-002)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-239
- **statement**: When chirps have been posted since the person last viewed the timeline, a catch-up
  control at the top of the list states how many new chirps are waiting and, when used, brings them
  in as a single bounded step that returns the reader to the newest chirps — not an open-ended scroll
  back through everything missed. Opening a chirp's conversation and returning to the timeline leaves
  the reader at the position they left, not reset to the top of the list.
- **references**: REQ-UX-052 (REQ-PROD-002)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-240
- **statement**: The home timeline shows a designed state for empty, for failure, and for loading in
  place of a blank region or an indefinite spinner. An account that follows no one and has posted
  nothing sees an empty state that explains why the timeline is empty and offers a route to Explore
  and to composing a first chirp. A failed first page shows a plain-language message with a retry in
  place of the list, visibly distinct from the empty state; a failed load-older or failed catch-up is
  shown at the boundary while the chirps already on screen stay loaded. A first load shows skeleton
  rows at the size of real chirp cards while the signed-in shell stays visible, and no region of the
  timeline continues to spin without resolving.
- **references**: REQ-UX-053 (REQ-PROD-002)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-241
- **statement**: The compose surface shows a remaining-character count that warns as the 280-character
  limit nears and marks the draft as over the limit once it is exceeded. The post action is not
  activatable while the draft is empty or over the limit, and an empty or over-limit submission
  reached by any path creates no chirp. While a publish is in flight the post action shows a busy
  state and the same draft cannot be submitted a second time; on success the chirp is published, the
  field clears, and a brief non-blocking confirmation is shown; on failure the draft text is kept
  exactly as written with an inline error and a retry, so the person can post again without retyping.
  No successful post is duplicated and no failed post loses its draft.
- **references**: REQ-UX-054, REQ-UX-055 (REQ-PROD-001)
- **verification_method**: automated_test
- **stage**: usable_early

### BAR-242
- **statement**: The compose surface is reachable inline at the top of the home timeline, as the
  Compose dialog (opened from the signed-in shell's compose affordance and directly at `/compose`),
  and in the reply position of a chirp's conversation screen, and it behaves the same way in each.
  In every placement an untouched field shows a placeholder prompt, a remaining-character count at
  the full 280 budget, and a disabled primary action; the action is labelled for its placement —
  "Post" when writing a chirp, "Reply" when answering one. Dismissing the Compose dialog with text
  still in the field and reopening it does not lose the draft.
- **references**: REQ-UX-056 (REQ-PROD-001, REQ-PROD-003)
- **verification_method**: manual_user_check
- **stage**: releasable

---

## Social interactions & profiles (BAR-243..247)

### BAR-243
- **statement**: Signed in on a chirp's conversation, a person can write a reply within the character
  limit and publish it from the conversation's reply control; the published reply then appears in that
  conversation shown as answering the chirp, and its publication is confirmed. Attempting to reply to
  a chirp that no longer exists reports not-found at the reply control and keeps the typed draft,
  rather than appearing to send. Opened without a session, the conversation presents a visible way to
  sign in or sign up in place of the reply control, not a dead or silent one.
- **references**: REQ-UX-058 (REQ-PROD-003)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-244
- **statement**: A chirp's like control toggles between not-liked and liked, with the liked state
  distinguished by more than colour (a filled heart and a "Liked" label). Liking an already-liked
  chirp, or reloading the screen, does not raise the count a second time; unliking returns the count
  to its earlier value. When a like or unlike cannot be completed, the control returns to its prior
  state, the count is left unchanged (it never shows a like that did not take), and the failure is
  reported at the control with a way to retry. The control looks and behaves the same wherever the
  chirp is shown — in the timeline, in its conversation, and on a profile.
- **references**: REQ-UX-059 (REQ-PROD-005)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-245
- **statement**: On another person's profile header or in a person row, the follow control toggles
  between "Follow" and "Following"; following the same account again, or reloading, leaves exactly
  one follow in place with the control reading "Following", and unfollowing returns it to "Follow". A
  person's own identity never presents a Follow control — the own-identity action is "Edit profile"
  — so a self-follow cannot be started, and any attempt is refused and shown at the control. When a
  follow or unfollow cannot be completed, the control returns to its prior label, any follower count
  is unchanged, and the failure is reported at the control with a way to retry. The control looks and
  behaves the same wherever it appears (profile header and person rows).
- **references**: REQ-UX-060 (REQ-PROD-006)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-246
- **statement**: A person's profile at its handle URL shows their avatar, display name, handle, bio,
  and follower and following counts, above that person's own chirps in newest-first bounded pages
  with a way to load older ones, and loads both without a session and with one; signed in, the header
  also carries the follow control. When the signed-in owner opens their own profile, they see the
  same public face a visitor sees, with an "Edit profile" entry in place of the follow control that
  opens the edit-profile screen, and no follow control is shown on their own profile.
- **references**: REQ-UX-061, REQ-UX-062 (REQ-PROD-007)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-247
- **statement**: A profile's follower and following counts open the followers list and the following
  list, each at its own URL. Each list shows one person per row with enough to recognise the account
  (avatar, display name, handle, bio) in a bounded page with a way to load more, a labelled way back
  to the profile, and — for a signed-in viewer — a follow control on each row. Each list's URL,
  opened directly, lands on that list.
- **references**: REQ-UX-063 (REQ-PROD-007, REQ-PROD-006)
- **verification_method**: manual_user_check
- **stage**: releasable

---

## Account management & lifecycle (BAR-248..255)

### BAR-248
- **statement**: After a fresh sign-up, a brand-new account lands on the onboarding screen and sees,
  in plain language, why its timeline is empty and at least one working control that opens compose to
  write a first chirp (and, wherever discovery is present, a control to find people to follow). The
  explanation and the compose route appear immediately and stay usable while any suggestions preview
  is still loading — shown as placeholders, not a blank region — and after that preview fails or
  comes back empty. The screen is never a blank page and never leaves the person without a next step.
- **references**: REQ-UX-065, REQ-UX-066 (REQ-PROD-032, REQ-PROD-033)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-249
- **statement**: A signed-in person can reach edit profile from the settings hub and from the edit
  action on their own profile, change their display name and bio, and save; the saved values then
  show on their profile. An empty required display name or a rejected value is reported against the
  field in plain words and no save is made; a save that fails is reported at the form with the
  person's edited values still present so they can retry; a save that succeeds is confirmed. The
  screen never reports success or failure silently and never shows a raw system or error code.
- **references**: REQ-UX-067, REQ-UX-068 (REQ-PROD-016, REQ-PROD-033, REQ-PROD-034)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-250
- **statement**: A signed-in person opening settings sees a labelled row for every account section in
  the release — edit profile, account & contact, sessions & devices, blocked & muted, export your
  data, and delete account (the notification-preferences row appears only where notifications are in
  the release). Each row opens its section both by selection and by entering the section's own URL
  directly in a fresh tab, and each section offers a labelled way back to the hub that works
  alongside the browser back control. The delete-account row is shown as destructive and opens a
  confirmation rather than deleting when selected. If the account summary fails to load, every
  section row is still reachable.
- **references**: REQ-UX-069 (REQ-PROD-017)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-251
- **statement**: On the account & contact screen a signed-in person sees their current point of
  contact with a status of either "Verified" or "Not verified yet". They can change the contact and
  save; the change is confirmed, the new contact shows as not-yet-verified, and the screen offers a
  step that confirms the person controls it before it is used for account recovery. An unverified
  contact is presented as a caution, not an error, and is not treated as verified until that step is
  completed. A failed save is shown against the contact field with the typed value preserved for
  retry.
- **references**: REQ-UX-070 (REQ-PROD-012, REQ-PROD-017)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-252
- **statement**: A signed-in person opening sessions & devices sees every place the account is
  currently signed in, each with enough to recognise it — device and browser, approximate location,
  last-active time — and the current session marked. Ending another session goes through a
  confirmation that names the effect; after confirming, that session leaves the list and the next
  action attempted from the ended session on its own device is refused and requires a fresh sign-in.
- **references**: REQ-UX-073 (REQ-PROD-017, REQ-PROD-014)
- **verification_method**: operational_check
- **stage**: releasable

### BAR-253
- **statement**: A signed-in person can sign out from sessions & devices through a confirmation that,
  where the account is signed in elsewhere, offers to end those other sessions too. After sign-out
  the person is on the signed-out landing; the browser back control does not re-expose any protected
  screen; and replaying the signed-out session's request is refused, so the next person at that
  device is not signed in as them.
- **references**: REQ-UX-074 (REQ-PROD-014)
- **verification_method**: operational_check
- **stage**: usable_early

### BAR-254
- **statement**: From the export screen a signed-in person sees what the export contains and a single
  request action. After requesting, the screen shows a preparing state rather than freezing or
  blanking, and when ready offers a way to download the file; the downloaded file opens outside chirp
  and contains the person's chirps, their profile, and who they follow. A preparation that fails is
  explained in plain words with a retry, and no broken file is offered.
- **references**: REQ-UX-075 (REQ-PROD-019)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-255
- **statement**: The delete-account confirmation, shown before anything is deleted, states plainly
  that the account and its chirps are removed and cannot be recovered, shows what is and is not
  retained and what happens to the handle (matching the product's stated deletion outcome), and
  points the person to export their data first. The delete action stays unavailable until the person
  gives the explicit confirmation it asks for. Cancelling at any point returns to settings with the
  account and its content unchanged and still able to sign in. Giving the confirmation and deleting
  signs the person out to the signed-out landing, after which the account can no longer sign in and
  the browser back control does not re-expose the deleted account's screens.
- **references**: REQ-UX-076, REQ-UX-077 (REQ-PROD-020, REQ-PROD-021, REQ-PROD-022)
- **verification_method**: operational_check
- **stage**: releasable

---

## Safety, help, rules, not-found & cross-screen state patterns (BAR-256..263)

### BAR-256
- **statement**: Signed in, a person can open the report action from both a chirp's and an account's
  more-actions menu, choose a reason, add optional detail, and submit, and sees an in-product
  confirmation that the report was received; and when no reason is chosen the submit control does not
  send the report. No report path ends in a silent no-op.
- **references**: REQ-UX-079 (REQ-PROD-025, REQ-PROD-026)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-257
- **statement**: From both the signed-out and the signed-in shell, a person can reach a Rules & terms
  screen that lists the product's rules as named categories; and the reasons offered in the report
  action correspond to those same named categories, so a submitted report points at a stated rule
  rather than an unlabelled choice.
- **references**: REQ-UX-083 (REQ-PROD-026)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-258
- **statement**: A Help & support entry is reachable with no session from the signed-out shell and,
  signed in, from the account menu; from it a person can reach the recover-access path ("Can't get
  in?") and a way to contact the operator ("Contact support") for what self-service does not cover.
- **references**: REQ-UX-082 (REQ-PROD-028, REQ-PROD-013)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-259
- **statement**: Opening an address that does not resolve — a mistyped path, a deleted chirp, an
  unavailable account — shows a not-found screen that states the resource is missing (consistent with
  the in-place tombstone used elsewhere), reveals no private detail about a removed or restricted
  resource, and offers a route to a known place (the home timeline when signed in, the landing when
  signed out) rather than a broken page.
- **references**: REQ-UX-084 (REQ-PROD-033)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-260
- **statement**: On each surface in this area a person can force an empty result, a failed load, and
  a first load and sees, respectively, an explained empty treatment carrying at least one next step
  (never a blank region), a distinct "couldn't load — try again" treatment with a retry, and a
  loading treatment — with the empty treatment and the failed treatment visibly different from each
  other; a surface to which one of these states does not apply says so rather than showing nothing.
  Checked across, for example, Notifications, the report and block/mute dialogs on a failed submit
  (the dialog stays open with its input preserved and an inline error), the blocked & muted screen
  when empty, a brand-new home timeline, and an empty followers list.
- **references**: REQ-UX-085, REQ-UX-086 (REQ-PROD-033, REQ-PROD-034)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-261
- **statement**: On a slow connection a first load of a content surface shows skeletons sized to the
  real content — not a spinner on a blank page — while the persistent navigation frame stays visible;
  an incremental load, such as loading older items, shows a bounded indicator at the point of the
  action while the already-loaded content stays on screen; and a load that cannot resolve stops and
  becomes an error with a retry rather than spinning without end.
- **references**: REQ-UX-087 (REQ-PROD-033)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-262
- **statement**: A person who triggers a field error (for example a taken handle at sign-up), a
  failed in-place action (for example a like or follow that fails), and a failed list page sees in
  each case a plain-language message at the point of the problem — no system or error code, never a
  silent no-op and never a blank — with a way to retry or correct and their input preserved; an
  optimistic in-place action that fails reverts to its prior state rather than showing a result that
  did not happen.
- **references**: REQ-UX-088 (REQ-PROD-033)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-263
- **statement**: With a session expired, a person who drafts a chirp and tries to post is routed to
  sign-in with the reason stated — not a silent failure — and, after signing in, is returned to where
  they were with the drafted text intact; and a transient server error during the same post can be
  retried in place and succeeds without re-typing the draft. This observes, and does not redefine,
  the information architecture's session-expiry (REQ-UX-008) and auth-gated-return (REQ-UX-007)
  conventions.
- **references**: REQ-UX-089 (REQ-PROD-034)
- **verification_method**: manual_user_check
- **stage**: releasable

---

## Coverage note — every release-gating `REQ-UX-040..089` → the `BAR-*` that covers it

Every release-gating requirement in the screens band (43 of the 50 in `REQ-UX-040..089`; the other
seven are `release_gating: false` in `design/experience-design.md`) is covered by at least one
criterion above. Non-gating requirements are listed in parentheses for completeness.

| REQ-UX | Gating | Covered by | Topic |
|--------|--------|------------|-------|
| REQ-UX-040 | yes | BAR-230 | Landing explains chirp, reachable with no session |
| REQ-UX-041 | yes | BAR-231 | Sign-up creates account from only what it needs |
| REQ-UX-042 | yes | BAR-232 | Handle format and uniqueness reported against the field |
| REQ-UX-043 | yes | BAR-231 | Sign-up captures a contact marked to-be-verified |
| REQ-UX-044 | yes | BAR-233 | Sign-in requires the person's own credential |
| REQ-UX-045 | yes | BAR-233 | Sign-in distinguishes no-account from wrong-credential, no existence leak |
| REQ-UX-046 | yes | BAR-234 | Self-service recovery through the verified contact, neutral no-leak |
| REQ-UX-047 | yes | BAR-234 | Set new credential completes recovery, returns to sign-in, no dead end |
| REQ-UX-048 | yes | BAR-235 | Sign-out confirmed, ends the session, offers all devices |
| REQ-UX-049 | yes | BAR-236 | Each entry/auth surface has designed empty/error/loading states |
| REQ-UX-050 | yes | BAR-237 | Land on the right place; no back-leak (gating basis only) |
| REQ-UX-051 | yes | BAR-238 | Home timeline: own + followed, newest first, bounded pages, Home current |
| REQ-UX-052 | yes | BAR-239 | Catch-up as a bounded step; keep reading position on return from a conversation |
| REQ-UX-053 | yes | BAR-240 | Home timeline designed empty, error, and loading states |
| REQ-UX-054 | yes | BAR-241 | 280-character limit enforced while composing, before submission |
| REQ-UX-055 | yes | BAR-241 | Publish locks against double-posting, confirms on success, keeps draft on failure |
| REQ-UX-056 | yes | BAR-242 | One compose surface in three placements, context-labelled action, empty state |
| (REQ-UX-057) | no | — | Navigable conversation read — non-gating; not covered |
| REQ-UX-058 | yes | BAR-243 | Reply from conversation; reply-to-gone reports not-found with draft kept |
| REQ-UX-059 | yes | BAR-244 | Like is an idempotent toggle; count reflects only what took |
| REQ-UX-060 | yes | BAR-245 | Follow is idempotent; no self-follow; own identity shows Edit profile |
| REQ-UX-061 | yes | BAR-246 | Public profile shows identity + chirps with or without a session |
| REQ-UX-062 | yes | BAR-246 | Owner's own profile shows Edit profile in place of follow control |
| REQ-UX-063 | yes | BAR-247 | Followers/following are addressable, paginated lists with per-row follow control |
| (REQ-UX-064) | no | — | Explore/discovery — non-gating; not covered |
| REQ-UX-065 | yes | BAR-248 | Onboarding explains the empty timeline, offers a way off it |
| REQ-UX-066 | yes | BAR-248 | Onboarding never blanks or dead-ends across its states |
| REQ-UX-067 | yes | BAR-249 | Edit profile saves and shows display name and bio changes |
| REQ-UX-068 | yes | BAR-249 | Edit profile validates in place, reports failures, keeps input |
| REQ-UX-069 | yes | BAR-250 | Settings hub lists every section; each addressable; returns to hub |
| REQ-UX-070 | yes | BAR-251 | Account & contact: view, update, confirm control of the contact |
| (REQ-UX-071) | no | — | Handle-change position — non-gating; not covered |
| (REQ-UX-072) | no | — | Notification preferences — non-gating; not covered |
| REQ-UX-073 | yes | BAR-252 | Sessions & devices: see active sessions, end another device's session |
| REQ-UX-074 | yes | BAR-253 | Sign out ends the session server-side; no back-leak |
| REQ-UX-075 | yes | BAR-254 | Data export: request and obtain own data in a portable form |
| REQ-UX-076 | yes | BAR-255 | Deletion confirmation names consequence, retention, and export-first |
| REQ-UX-077 | yes | BAR-255 | Deletion requires explicit confirmation; cancel leaves account intact |
| (REQ-UX-078) | no | — | Notifications surface — non-gating; not covered |
| REQ-UX-079 | yes | BAR-256 | Report acknowledged as received; reasonless submit prevented |
| (REQ-UX-080) | no | — | Block/mute — non-gating; not covered |
| (REQ-UX-081) | no | — | Managing blocked/muted — non-gating; not covered |
| REQ-UX-082 | yes | BAR-258 | Help & support reachable from both shells |
| REQ-UX-083 | yes | BAR-257 | Rules stated as named categories; report reasons correspond to them |
| REQ-UX-084 | yes | BAR-259 | Not-found screen explains and routes to a known place; no private leak |
| REQ-UX-085 | yes | BAR-260 | Considered empty/error/loading per surface (or stated N/A) |
| REQ-UX-086 | yes | BAR-260 | Empty explained, never blank; empty visibly distinct from failed |
| REQ-UX-087 | yes | BAR-261 | Loading shows shape of content; nav frame persists; unresolved → error with retry |
| REQ-UX-088 | yes | BAR-262 | Failures at the point of action; plain words; input preserved; optimistic reverts |
| REQ-UX-089 | yes | BAR-263 | Expired session and transient error both recover with in-progress work preserved |

**Gating coverage**: 43 of 43 release-gating `REQ-UX-*` in the screens band are covered.
Non-gating (7): REQ-UX-057, 064, 071, 072, 078, 080, 081 — each `release_gating: false` in
`design/experience-design.md`; none is the sole basis of any criterion above.
