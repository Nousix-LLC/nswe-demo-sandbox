### Screens and flows — getting in

This section covers the screens a stranger meets before
they have a session, and the moment they cross from signed-out to signed-in and back. It covers the
first-visit **Landing**, **Sign up**, **Sign in**, the two-screen recovery (**Recover access** and
**Set new credential**), and the **Sign out** confirmation. Each is designed as an arrangement of
named components realising a named screen-inventory screen, with its layout, its content, its one
primary action, and its empty, error, and loading states, not a bare route.

These screens carry more weight than their size suggests. They are where a person decides whether
chirp is a product they will trust with an account, and they are the signed-out↔signed-in boundary,
so they are designed to the identity requirements the product sets: an account only its owner can
enter, a recovery path that runs through a verified contact and no one else, and a sign-out that ends
the session on the server rather than only forgetting it in the browser. Where a transition or a
convention is already fixed by the information architecture (auth-gated return-to, session-expiry
interception, the sign-up/sign-in/sign-out boundary), these screens compose against it and refer to
it; they do not restate it.

All six render inside the **NavShell** signed-out shell (the Sign out confirmation is the one
exception: it is a **Dialog** layered over the signed-in shell). The shell carries the chirp
wordmark to the Landing, a Sign in and a prominent Sign up entry, and footer access to Rules & terms
and Help & support on every signed-out screen, so no one ever dead-ends at an authentication wall.

---

#### Landing — `/` (no session), empty/landing archetype

**Layout.** The signed-out **NavShell** frames a single centred reading column at `space.measure`
(600px). Inside it, an **EmptyState** hero: a calm flat illustration in one or two brand hues, a
`type.display` headline, and a `type.body` `color.text.secondary` paragraph that says what chirp is
in plain words. Directly below the hero, the action pair, a prominent **PrimaryButton** "Sign up"
and a quieter **SecondaryButton** "Sign in". Below that, where a public sample is available, a bounded
**ListView** of public **ChirpCard**s (read-only, each still linking to its public profile and
conversation) so a first-time visitor sees real content, not just a pitch. Generous vertical rhythm
(`space.10`/`space.12`) keeps the screen unhurried. The footer (Rules & terms, Help & support) comes
from the shell.

**Content.** A one-line explanation of chirp ("Short public posts from the people you follow"), the
two entry actions, and, when a sample is served, a handful of public chirps. Nothing on this screen
requires an account to read.

**Primary action.** **Sign up** → opens **Sign up** (`/signup`). The secondary action, **Sign in**,
opens **Sign in** (`/signin`). Both are always present; the Landing never requires signing in to be
understood.

**States.**
- **Empty**: no public sample is available (none is served, or it is withheld). The hero explanation
  and both entry actions stand on their own; the sample region carries a short **EmptyState**
  explanatory line ("Sign up to see what people are posting") rather than a blank gap. The Landing
  still explains chirp and leads to sign-up.
- **Error**: the public-sample fetch fails. The sample region shows the **EmptyState** error variant
  ("We couldn't load a sample right now — you can still join") with a retry. The explanation and the
  Sign up / Sign in actions stay fully usable; a sample failure never blocks joining.
- **Loading**: on first paint the shell and the explanatory hero render immediately (the native
  `type.family.sans` stack means no blank flash while a font loads). The sample region shows
  **LoadingState** skeleton **ChirpCard**s at their real dimensions while it resolves, so the column
  does not jump when content arrives.

---

#### Sign up — `/signup`, form archetype

**Layout.** The signed-out shell around a single 600px form column, `type.title` heading "Create your
account". A stack of **TextField**s with `space.4` between them, then a **PrimaryButton** "Create
account" at the foot. Below the button, interlinks: "Already have an account? Sign in" and "Can't get
in? Recover access". The form asks for no more than the account needs.

**Content.** Five fields, each a labelled **TextField** with a plain hint:
- **Handle**: "@handle", hint "Up to 15 letters, numbers, or underscores". Checked for format and
  uniqueness as the person types (see loading / error states).
- **Display name**: the name shown on your chirps.
- **Bio**: optional, multi-line, marked optional so it reads as skippable.
- **Credential**: the secret you will use to prove the account is yours; obscured input. (What the
  credential is and how it is stored is the identity design's; this screen states only that one is set
  here, so a handle alone can never sign in, J2/REQ-PROD-008.)
- **Contact**: a point of contact chirp can verify, used for account recovery and important
  notifications; a one-line note says why it is asked for and that it is kept minimal. The form
  triggers a verification step and shows a pending-verification affordance; whether verification
  completes inline or just after the account is created is the identity design's call.

**Primary action.** **Create account**: disabled until the required fields are valid. On success it
establishes the session and lands the person on **Onboarding** (`/welcome`); they are not asked to
sign in again, and they do not land on a blank timeline. This routing composes against REQ-UX-014 and
is not redefined here.

**States.**
- **Empty**: a fresh form: labels and placeholders, no values, **Create account** disabled. A
  required-but-empty field is not shown as an error until the person has had a chance to fill it
  (**TextField** empty state).
- **Error**: field-level and plain: a taken or ill-formed handle shows an **InlineError** against the
  handle field ("That handle's already taken — try another" / "Handles can use letters, numbers, and
  underscores, up to 15"). A failed submit shows an **InlineError** at the point of the problem with
  every entered value preserved, so the person fixes one thing and retries. No message carries a system
  or error code.
- **Loading**: the handle uniqueness/format check runs as a quiet **TextField** pending affordance
  that resolves to accepted or a field error. On submit, **Create account** shows its busy state and
  the form locks briefly so the account is not created twice.

---

#### Sign in — `/signin`, form archetype

**Layout.** The signed-out shell around a 600px form column, `type.title` heading "Sign in". Two
**TextField**s, handle and credential, then a **PrimaryButton** "Sign in". Below it, interlinks:
"New to chirp? Sign up" and a "Can't get in?" link to **Recover access**.

**Content.** The handle you signed up with and your credential. The "Can't get in?" link is the
in-flow route to recovery for someone who has lost their credential.

**Primary action.** **Sign in**: disabled until both fields hold input. On success the person lands
in the signed-in shell, or on the screen they originally asked for when they were routed here by
auth-gating (the return-to behaviour is fixed by REQ-UX-007 and composed against, not redefined). When
this screen is the destination of a mid-use session expiry, it states the reason and preserves the
person's in-progress work, composing against REQ-UX-008 and the expired-session pattern in the states section; it does not restate that pattern.

**States.**
- **Empty**: labelled fields, no values, **Sign in** disabled.
- **Error**: two distinct signals, so a person can tell a typo from a wrong secret (REQ-PROD-011). An
  unknown handle resolves to "We couldn't find an account with that handle" with a path to **Sign up**.
  A known handle with a wrong credential resolves to "That didn't match — try again or recover access"
  with a path to **Recover access**. Both are **InlineError** at the point of action, worded so they do
  not disclose which accounts exist beyond what the product already makes public, and never a system
  code.
- **Loading**: on submit, **Sign in** shows its busy state and the fields lock briefly so a double
  submit cannot open two sessions.

---

#### Recover access — `/recover`, form archetype

**Layout.** The signed-out shell around a 600px column, `type.title` heading "Can't get in?". A
`type.body` paragraph explains what will happen, chirp sends a recovery step to the contact verified
on the account, and no one else can start this for you. One **TextField** (the verified contact, or
the handle, depending on what the identity design keys recovery to), then a **PrimaryButton** "Send
recovery link". A link back to **Sign in** closes the interlink loop.

**Content.** The contact field and the plain explanation. The screen sets the expectation that
recovery runs end to end through the verified contact (J3a / REQ-PROD-012, 013).

**Primary action.** **Send recovery link**: on success the screen confirms, in wording that does not
reveal whether a given contact has an account, that if the contact matches an account a recovery step
has been sent ("If that contact is on an account, we've sent a recovery link to it"). Following that
step opens **Set new credential**.

**States.**
- **Empty**: labelled field, no value, the action disabled.
- **Error**: a malformed contact shows an **InlineError** against the field ("That doesn't look like
  a contact we can reach"). A send failure shows an **InlineError** with a retry. A valid but unknown
  contact is answered with the same neutral, non-disclosing acknowledgement as a match, not an error,
  so the screen never reveals who has an account.
- **Loading**: on send, **Send recovery link** shows its busy state until the request resolves.

---

#### Set new credential — `/recover/confirm`, form archetype

**Layout.** The signed-out shell around a 600px column, `type.title` heading "Set a new way to get
in". A `type.body` line explains this finishes recovery. The recovery token is carried by the link the
person followed and is not asked of them; where a recovery code must be read or typed exactly it is
shown in `type.family.mono`. A **TextField** for the new credential and a second to confirm it, then a
**PrimaryButton** "Set new credential".

**Content.** The new-credential field and its confirm, with the same plain validation voice as the
rest of the forms. On success the person is sent to **Sign in** to enter with the new credential,
completing the IA path signed-out → Recover access → Set new credential → Sign in.

**Primary action.** **Set new credential**: disabled until the new credential is valid and confirmed.
On success it routes to **Sign in** (composing against REQ-UX-015).

**States.**
- **Empty**: labelled field(s), no value, the action disabled.
- **Error**: an expired or already-used recovery link shows an **EmptyState** error variant that
  explains the link is no longer valid and offers a path to start again at **Recover access**, rather
  than a dead end. A new credential that does not meet the stated rule, or a mismatch between the field
  and its confirm, shows an **InlineError** against the field. A submit failure shows an **InlineError**
  with a retry.
- **Loading**: validating the recovery link when the screen opens shows a **LoadingState** that
  resolves either to the form or to the expired-link error. On submit, **Set new credential** shows its
  busy state.

---

#### Sign out — the account-menu confirmation, confirmation archetype (**Dialog**)

**Layout.** A **Dialog** (confirmation variant) rises over the current signed-in screen on the
`color.bg.scrim`, at `elevation.3`. A `type.heading` title "Sign out?", a `type.body` line, a
**Toggle** labelled "Also sign out on all other devices", and the action pair, a **PrimaryButton**
"Sign out" with a **SecondaryButton** "Cancel". The Dialog traps focus while open and returns focus to
the account-menu control that opened it on close.

**Content.** A plain confirmation that this ends the current session, with the option to end sessions
on every other device too. This is the only entry/auth surface reached from the signed-in shell (the
account menu), because signing out is the move back across the boundary.

**Primary action.** **Sign out**: ends the session on the server (and, when the toggle is on, the
other sessions too), then lands the person on the signed-out **Landing**. After sign-out the browser
back control does not re-expose a protected screen's content; that no-leak behaviour is fixed by
REQ-UX-016 and composed against here, not redefined.

**States.**
- **Empty**: does not apply: a **Dialog** always opens with its content. Recorded, not omitted.
- **Error**: the sign-out request fails. An **InlineError** appears inside the panel ("We couldn't
  sign you out — try again") and the Dialog stays open so the person can retry. The browser session is
  not treated as ended while the server still holds it, so the control never claims a sign-out that did
  not happen.
- **Loading**: on confirm, the **Sign out** button shows its busy state and the Dialog does not close
  until the server confirms the session has ended.

---

#### The transitions between these screens

These screens are stitched together so no one is stranded at the boundary, composing against the IA
interaction model (REQ-UX-007, 008, 014, 015, 016) rather than restating it:

- **Sign up → Onboarding.** A completed sign-up establishes the session and lands on **Onboarding**,
  not on a sign-in prompt and not on a blank timeline.
- **Interlinks.** Sign up, Sign in, and Recover access each link to the others, so a returning person
  who opened Sign up, a new person who opened Sign in, or someone who cannot get in, can correct course
  without leaving the flow. Recover access also stays reachable from Help & support.
- **Auth-gated return-to.** When a person is routed to **Sign in** from a signed-in-only screen they
  asked for, a successful sign-in returns them there rather than to a default screen.
- **Session expiry mid-use.** An action on an expired session routes to **Sign in** with the reason
  stated and the person's in-progress work preserved; the keep-the-draft pattern is set out in the states section and composed against here.
- **Sign out → signed-out Landing.** Signing out ends the session and returns to the Landing, with no
  back-leak into protected content.

---

### Requirements and acceptance criteria — REQ-UX-040..050

Each requirement is testable by someone who never met the author, exercisable on the live product.
Each carries a `release_gating` flag (a `false` flag names its reason) and references the product
requirement(s) it serves. Where a referenced product requirement is itself non-gating, these entries
honour that staging.

#### REQ-UX-040 — A first-visit Landing that explains chirp without an account
- **statement**: A person with no session reaches a Landing that explains what chirp is and offers a
  clear path to sign up and to sign in, without being required to sign in first, and that shows a
  sample of public content where one is available.
- **acceptance_criteria**: With no session, open the site root. You see an explanation of what chirp
  is and both a Sign up and a Sign in action, reachable without signing in. Where a public sample is
  served, real public chirps appear; where none is served, the Landing still explains chirp and offers
  both actions rather than a blank area.
- **release_gating**: true
- **references**: REQ-PROD-030, REQ-PROD-031

#### REQ-UX-041 — Sign-up creates an account from only what it needs
- **statement**: The Sign up screen collects a handle, a display name, an optional bio, the credential,
  and the contact the account requires, and nothing extraneous, and creates the account on submit.
- **acceptance_criteria**: Open Sign up. The form requests a handle, a display name, an optional bio
  (marked optional), a credential, and a contact, and no fields beyond these. Complete it with valid
  values and submit; an account is created and you are signed in.
- **release_gating**: true
- **references**: REQ-PROD-008, REQ-PROD-031

#### REQ-UX-042 — Handle format and uniqueness are reported against the field
- **statement**: Sign-up checks the handle for format (up to 15 letters, numbers, or underscores) and
  uniqueness, and reports a taken or ill-formed handle against the handle field so the person can fix
  it before submitting.
- **acceptance_criteria**: Enter a handle already in use; an inline message against the field names the
  conflict. Enter a handle with a space, a disallowed character, or more than 15 characters; an inline
  field-level message explains the rule. Enter a valid, unused handle; the field resolves to accepted.
- **release_gating**: true
- **references**: REQ-PROD-009

#### REQ-UX-043 — Sign-up captures a contact to be verified
- **statement**: Sign-up captures a point of contact and makes clear it will be verified before the
  product relies on it for recovery or notifications, showing the person a pending-verification state.
- **acceptance_criteria**: During sign-up, provide a contact; the screen states the contact must be
  confirmed and shows that verification is pending (or prompts the verification step), rather than
  treating an unverified contact as confirmed.
- **release_gating**: true
- **references**: REQ-PROD-012

#### REQ-UX-044 — Sign-in proves the account is the person's own
- **statement**: Signing in requires the credential set at sign-up or recovery; presenting a known
  handle alone does not grant a session.
- **acceptance_criteria**: Enter another account's handle with no credential (or a wrong one); no
  session is granted. Enter your own handle with the correct credential; you are signed in.
- **release_gating**: true
- **references**: REQ-PROD-010

#### REQ-UX-045 — Sign-in distinguishes no-such-account from wrong-credential
- **statement**: Sign-in lets a person tell "no account with that handle" from "the credential did not
  match", enough to distinguish a typo from a wrong secret, without disclosing which accounts exist
  beyond what the product already makes public.
- **acceptance_criteria**: Sign in with a handle that does not exist; the result tells you the account
  was not found and offers a path to Sign up. Sign in with a real handle and a wrong credential; the
  result is a failed sign-in you can retry or recover from, offering a path to Recover access. Neither
  message reveals account existence beyond what a public profile already shows, and neither shows a
  system code.
- **release_gating**: true
- **references**: REQ-PROD-011

#### REQ-UX-046 — Recover access starts self-service recovery through the verified contact
- **statement**: A person who cannot sign in can start recovery themselves from a Recover access
  screen that runs through the account's verified contact, and the screen's response does not reveal
  whether a given contact is on an account.
- **acceptance_criteria**: Open Recover access and submit the verified contact; the screen confirms, in
  wording that does not disclose account existence, that a recovery step has been sent if the contact
  matches an account. Submit a contact not on any account; the response is the same neutral
  acknowledgement, not a "not found" error.
- **release_gating**: true
- **references**: REQ-PROD-013, REQ-PROD-012

#### REQ-UX-047 — Set new credential completes recovery and returns to sign-in
- **statement**: Following the recovery step opens a Set new credential screen that lets the person set
  a new credential and then sign in with it; an expired or used recovery link is explained with a way
  to start recovery again rather than a dead end.
- **acceptance_criteria**: Follow a valid recovery link; set a new credential; you are routed to Sign
  in and can sign in with it. Follow an expired or already-used recovery link; the screen explains the
  link is no longer valid and offers a path back to Recover access.
- **release_gating**: true
- **references**: REQ-PROD-013

#### REQ-UX-048 — Sign-out confirmation ends the session, optionally on all devices
- **statement**: Signing out is confirmed before it proceeds, ends the current session on the server,
  and offers to end sessions on all other devices; a failed sign-out is reported and leaves the session
  intact rather than appearing to succeed.
- **acceptance_criteria**: From the account menu, choose sign out; a confirmation names the consequence
  and offers a cancel and an option to end other devices' sessions. Confirm; you land on the signed-out
  Landing and the prior session can no longer be used. Cancel; nothing changes. Force the sign-out to
  fail; the confirmation reports the failure and you remain signed in.
- **release_gating**: true
- **references**: REQ-PROD-014

#### REQ-UX-049 — Each entry/auth screen has designed empty, error, and loading states
- **statement**: The Landing, Sign up, Sign in, Recover access, Set new credential, and Sign out
  surfaces each present a designed state for empty, loading, and error, explained rather than shown as
  a blank, a hang, or a silent failure, using the component library's own named states.
- **acceptance_criteria**: On each of the six surfaces, reach its empty or initial state, a loading
  state (submit or fetch in flight), and a failure (an invalid submission, a failed request, or an
  expired recovery link). Each presents something the person can read and act on, a field-level
  message, a busy control, a skeleton, or an explained error with a next step, not a blank area or an
  unexplained failure. Where a state does not apply (the Sign out Dialog has no empty state), that is
  stated.
- **release_gating**: true
- **references**: REQ-PROD-033, REQ-PROD-034

#### REQ-UX-050 — The entry/auth screens land the person on the right place and do not leak back
- **statement**: A completed sign-up lands the person on onboarding; sign-in returns a person routed
  from a gated screen to that screen; signing out returns to the signed-out Landing with no back-leak
  into protected content; and Sign up, Sign in, and Recover access each link to the others.
- **acceptance_criteria**: Complete a fresh sign-up; you land on the onboarding screen, not a sign-in
  prompt or a blank page. With no session, open a signed-in-only screen, get routed to Sign in, and
  sign in; you land on the screen you asked for. Sign out and press back; you do not see the protected
  screen's content. On Sign in, Sign up, and Recover access, find and follow a link to each of the
  others.
- **release_gating**: true; the sign-up→onboarding landing and the sign-out no-leak are release-gating
  (REQ-PROD-032, REQ-PROD-014); the three-way interlinks ride the non-gating REQ-UX-015 and a first
  release may omit them provided Recover access stays reachable from Help & support.
- **references**: REQ-PROD-032, REQ-PROD-014, REQ-PROD-034
