## Information architecture and interaction model

This section defines the structure of chirp — the set of screens it is made of, how they are grouped,
and how a person moves between them — and the product-wide interaction conventions every screen obeys.
It is the foundation the visual system, the per-screen flows, the responsive layout, and the
accessibility work build on. Where it names a screen, it does so by the name in the **Screen inventory**
below; the rest of the experience design refers to screens by those names.

chirp today presents three screens above a persistent navigation bar: the home timeline at `/`, a
combined compose-and-sign-in view at `/compose`, and a public profile at `/user/:id`. That is a working
skeleton of the core loop, not the structure of a product a stranger can sign up for, trust, and leave.
The architecture here keeps the core loop at the centre and adds the account lifecycle, the settings and
safety surfaces, onboarding, notifications, and the signed-out entry a first-time visitor meets — each as
a named screen with a route and an archetype, so no required surface is missing and every surface has one
clear place to live.

The routes below are the user-facing address scheme the design calls for, stated from the user's side;
how they are served is a build decision for later code work. Handles are how people are known on chirp,
so a profile is addressed by its handle (`/@:handle`) rather than an internal id.

### Screen archetypes

Every screen is classified as one of seven archetypes. The archetype fixes what a person can expect of
the screen before they read a word of it, and lets the visual system and the responsive and accessibility
work design once per archetype instead of once per screen.

- **feed/list** — a paginated, newest-first (or ranked) list of items a person scans and acts on in place
  (timeline, notifications, a conversation, a followers list, search results).
- **form** — a screen whose job is to collect and submit input (sign-up, sign-in, recovery, edit profile).
- **profile** — a person's public identity surface (handle, display name, bio, counts, their chirps).
- **settings** — a grouped surface of account-level choices, each independently addressable.
- **modal/dialog** — a focused task layered over the current screen without leaving it (compose, report).
- **confirmation** — a dialog whose only job is to confirm a consequential or destructive action.
- **empty/landing** — a screen that is mostly explanation and a next step: the signed-out landing, the
  first-run onboarding, the rules and help pages, and the not-found screen.

### Screen inventory

The canonical set of screens a releasable chirp needs. Every screen names its user-facing route, its
archetype, the auth state(s) in which it is reachable (**signed-out**, **signed-in**, or **both**), and
its purpose. Sibling design areas refer to these screens by the names in the first column.

**Signed-out and public surfaces**

| Screen | Route | Archetype | Auth | Purpose |
|---|---|---|---|---|
| Landing | `/` (no session) | empty/landing | signed-out | Explain what chirp is to a first-time visitor and lead to sign-up or sign-in without requiring an account; show public content where a sample is available. |
| Sign up | `/signup` | form | signed-out | Create an account: handle, display name, optional bio, the credential, and the verified contact the account requires. |
| Sign in | `/signin` | form | signed-out | Return to an existing account by proving ownership. |
| Recover access | `/recover` | form | signed-out | Start self-service recovery for a person who has lost their credential, via the verified contact. |
| Set new credential | `/recover/confirm` | form | signed-out | Complete recovery: prove control of the contact and set a new credential. |
| Public profile | `/@:handle` | profile | both | A user's public profile — handle, display name, bio, follower/following counts, their chirps. |
| Chirp / conversation | `/@:handle/chirp/:id` | feed/list | both | A single chirp shown with the chirp it replies to and its replies — the conversation in context. |
| Followers | `/@:handle/followers` | feed/list | both | The accounts that follow this user. |
| Following | `/@:handle/following` | feed/list | both | The accounts this user follows. |
| Rules & terms | `/rules` | empty/landing | both | The stated rules and terms a report references. |
| Help & support | `/help` | empty/landing | both | How to get help; the user-facing entry to recovery, reporting, and contacting the operator. |
| Not found | any unresolved path | empty/landing | both | Explain that a resource is missing or removed and route the person back to a known place. |

**Signed-in surfaces**

| Screen | Route | Archetype | Auth | Purpose |
|---|---|---|---|---|
| Home timeline | `/` (session) | feed/list | signed-in | The home: the person's own chirps and those of the people they follow, newest-first, in bounded pages. |
| Compose | `/compose` and an overlay dialog | modal/dialog | signed-in | Write and publish a chirp, or a reply to a named chirp. |
| Explore / find people | `/explore` | feed/list | signed-in | Search for and discover people and content to follow, beyond already holding a profile link. |
| Notifications | `/notifications` | feed/list | signed-in | Activity directed at the person — replies, follows, and likes. |
| Own profile | `/@:handle` (own) | profile | signed-in | The person's own public face, with the entry to edit it. |
| Onboarding | `/welcome` | empty/landing | signed-in | First run: explain the empty timeline and offer at least one way to a non-empty one (find people, first post). |
| Settings | `/settings` | settings | signed-in | The hub for account-level choices, linking to each sub-section below. |
| Edit profile | `/settings/profile` | form | signed-in | Change display name and bio. |
| Account & contact | `/settings/account` | settings | signed-in | View and update the verified contact; the stated handle-change policy. |
| Notification preferences | `/settings/notifications` | settings | signed-in | Choose which activity categories send a notification. |
| Sessions & devices | `/settings/sessions` | settings | signed-in | View active sessions/devices, end a session, and sign out. |
| Blocked & muted | `/settings/blocks` | settings | signed-in | Manage the accounts the person has blocked or muted. |
| Export your data | `/settings/export` | settings | signed-in | Request and obtain the person's own data — chirps, profile, follows — in a portable form. |
| Delete account | `/settings/delete` | confirmation | signed-in | Delete the account with a confirmed, explained outcome. |

**Dialogs (layered over the current screen; no address of their own)**

| Screen | Trigger | Archetype | Auth | Purpose |
|---|---|---|---|---|
| Report | report action on a chirp or profile | modal/dialog | signed-in | Report a chirp or account that breaks the rules; acknowledge receipt. |
| Block / mute | block-or-mute action on a profile | confirmation | signed-in | Confirm blocking or muting an account and state the effect. |
| Delete chirp | delete action on the person's own chirp | confirmation | signed-in | Confirm removing a chirp the person posted. |
| Sign out | sign-out action in the account menu | confirmation | signed-in | End the current session; confirm when ending sessions on other devices too. |

Two surfaces in this inventory serve product requirements the release bar does not gate, and they are
marked so the staging is explicit: **Notifications** (and the notification-related settings) ride
REQ-PROD-029, and **Explore / find people** rides REQ-PROD-042 — both `release_gating: false` in the
product requirements. They are in scope and have a designed place in the architecture; the release bar
decides whether a first release includes them. Every other screen above serves a release-gating product
requirement.

### Navigation and wayfinding

chirp has two navigation shells — one a person meets before they have an account, one they live in after
signing in. The transition between them is the sign-up / sign-in / sign-out boundary.

#### The signed-out shell

A person with no session sees a light shell built to answer one question — "what is this, and do I want
an account?" — and to never dead-end at an authentication wall. It carries:

- the chirp wordmark, linking to the Landing screen;
- a clear **Sign in** and a prominent **Sign up** entry, present on every signed-out screen;
- a footer reaching **Rules & terms** and **Help & support**.

Public surfaces — a profile, a chirp's conversation, the rules, and help — render inside this shell when
reached without a session, so a visitor who arrives on a shared link lands on real content with a visible
path to joining rather than a blank gate.

#### The signed-in shell

After signing in, a person lives in a persistent shell that exposes every primary destination from every
screen, so they always know where they are and can reach anything in one step:

- **Home** — the home timeline;
- **Explore** — find people and content to follow;
- **Notifications** — activity directed at them, with an unseen-activity indicator;
- **Profile** — their own profile;
- an always-available **Compose** affordance;
- an **account menu** reaching **Settings**, **Help & support**, **Rules & terms**, and **Sign out**.

The shell is the same set of destinations on every signed-in screen; the responsive design decides how it
presents on a phone versus a wider viewport, and the accessibility work decides how it is operated and
announced. Settings is itself a small secondary navigation: a hub listing its sub-sections (edit profile,
account & contact, notification preferences, sessions & devices, blocked & muted, export, delete), each a
screen a person can open directly and return from to the hub.

#### Wayfinding

A person can always tell where they are and how they got there:

- the active primary-nav destination is visibly marked in the shell;
- the browser document title and the main heading name the current screen;
- a screen reached by drilling in (a conversation from the timeline, a sub-section from Settings, a
  followers list from a profile) offers a labelled way back to where the person came from, and the browser
  back control does the same thing.

#### Paths between account states

The architecture has three account states — **no session** (signed-out shell), **a brand-new session**
(onboarding), and **an established session** (signed-in shell) — and the moves between them are designed,
not incidental:

- signed-out → **Sign up** → a created session that lands on **Onboarding**, then into the signed-in shell;
- signed-out → **Sign in** → the signed-in shell (or the screen the person originally asked for);
- signed-out → **Recover access** → **Set new credential** → **Sign in** → the signed-in shell;
- signed-in → **Sign out** → the signed-out Landing, with protected screens no longer reachable.

### Interaction conventions

These are the product-wide patterns every screen obeys, so a person learns them once. The per-screen
flows apply them; they are not redesigned per screen.

#### Addressable screens and deep-linking

Public profiles and individual chirps have stable, shareable URLs that open the right screen directly: a
link to `/@:handle` opens that profile, and a link to `/@:handle/chirp/:id` opens that chirp in its
conversation. A settings sub-section and a followers/following list are addressable too, so a person can
bookmark or link to the exact place. Opening an addressable screen directly, with or without a session,
lands the person on that screen (subject to auth-gating below), not on a generic home.

#### Auth-gated routing and return-to

Signed-in-only screens are gated. A person who opens a signed-in-only URL without a session is routed to
**Sign in**, and on success is returned to the screen they originally asked for rather than dropped on the
home timeline. A public screen opened without a session renders in the signed-out shell.

#### Session expiry mid-use

When an action is attempted with an expired or invalid session, the product routes the person to
**Sign in** with the reason stated, preserves any in-progress input (such as a drafted chirp), and returns
them to where they were after they sign back in. Expiry is never a silent failure or a lost draft.

#### Browser back and forward

Back and forward behave the way a person expects in a web product: back returns to the previous screen
without re-submitting the previous action and without losing the person's place in a timeline they had
scrolled; opening a dialog (compose, report, a confirmation) is a step the back control dismisses, closing
the dialog rather than leaving the underlying screen.

#### Pagination and catch-up

Every list — the timeline, a conversation's replies, notifications, search results, followers and
following — loads in bounded pages, never as a single unbounded load. A list offers an explicit way to
load older items, and the timeline offers a way to pull in chirps posted since the person last looked, so
a long absence is a bounded catch-up rather than an endless scroll.

#### Confirming destructive actions

Every irreversible or destructive action is confirmed before it proceeds, through a **confirmation**
dialog that names what will happen and offers a plain way to cancel. This convention governs deleting an
account, deleting a chirp, blocking or muting an account, ending a session on another device, and signing
out of all sessions. The confirmation for deleting an account additionally states what is and is not
retained and points to data export first.

#### Transient feedback

The result of an action is always shown. A completed action (a chirp published, a follow, a like, a saved
setting, a received report) is confirmed with brief, non-blocking feedback that does not interrupt what
the person is doing. A failure is shown where the action was taken — against the field for a form, against
the control for an in-place action — with enough to understand and retry, never a silent no-op.

#### The sign-up, sign-in, and sign-out transitions

The boundary between the two shells is designed so no one is stranded:

- **Sign up → signed in.** A completed sign-up establishes the session and lands the person on
  **Onboarding** — they are not asked to sign in again immediately after creating the account, and they do
  not land on a blank timeline.
- **Sign in / sign up / recovery are interlinked.** Each of these screens links to the others, so a person
  who arrived at the wrong one (a returning user on Sign up, a new user on Sign in, someone who cannot get
  in) can correct course without leaving the flow.
- **Sign out → signed out.** Signing out ends the session and returns to the signed-out Landing; after
  sign-out the back control does not re-expose a protected screen's content.

### Requirements and acceptance criteria

The IA and interaction requirements chirp must meet. Each is testable by someone who never met the author,
against the live product; each carries a `release_gating` flag and references the product requirement(s)
it serves. Per-screen content and the full account flows are specified by the screens-and-flows area
(REQ-UX-040+); these requirements govern the structure, navigation, and the conventions above.

#### REQ-UX-001 — A signed-out shell that explains chirp and never dead-ends
- **statement**: A person with no session sees a signed-out shell carrying the chirp wordmark, a Sign in
  entry, a prominent Sign up entry, and footer access to the rules and to help, on every signed-out screen.
- **acceptance_criteria**: With no session, open the landing and a public profile link; on each, Sign up,
  Sign in, Rules & terms, and Help & support are all reachable without first signing in.
- **release_gating**: true
- **references**: REQ-PROD-030, REQ-PROD-031

#### REQ-UX-002 — A signed-in shell exposing every primary destination
- **statement**: After signing in, a persistent shell exposes Home, Explore, Notifications, Profile,
  Settings, and a Compose affordance, present and reachable from every signed-in screen.
- **acceptance_criteria**: Signed in, from the timeline, a profile, a conversation, and a settings
  sub-section, confirm each of Home, Explore, Notifications, Profile, Settings, and Compose is reachable
  from the shell without using the browser back control.
- **release_gating**: true
- **references**: REQ-PROD-002, REQ-PROD-017

#### REQ-UX-003 — The current location is always indicated
- **statement**: On every screen the product shows where the person is: the active primary-nav destination
  is marked, and the document title and main heading name the current screen.
- **acceptance_criteria**: Navigate to Home, Explore, Notifications, Profile, and a settings sub-section in
  turn; on each, the active destination is visibly marked and the browser tab title reflects that screen.
- **release_gating**: true
- **references**: REQ-PROD-002, REQ-PROD-033

#### REQ-UX-004 — The product is built from the published screen inventory
- **statement**: Every screen chirp presents appears in the screen inventory with a route, exactly one
  archetype, and a declared auth state; no screen exists outside the inventory and no inventory screen is
  missing from the product.
- **acceptance_criteria**: Walk the product signed-out and signed-in; every screen reached matches an
  inventory entry (route, archetype, auth state), and every signed-in-reachable inventory screen can be
  reached.
- **release_gating**: true
- **references**: REQ-PROD-033, REQ-PROD-032

#### REQ-UX-005 — Every required surface is reachable without an external link
- **statement**: From the signed-in shell a person can reach the timeline, compose, their profile,
  notifications, settings, discovery, help, and the rules, each in at most two steps, without holding an
  external link.
- **acceptance_criteria**: Signed in and starting from the home timeline, reach each of compose, own
  profile, notifications, settings, explore, help, and rules in no more than two steps through the product.
- **release_gating**: true
- **references**: REQ-PROD-028, REQ-PROD-042

#### REQ-UX-006 — Profiles and chirps are addressable and shareable
- **statement**: A public profile and an individual chirp each have a stable, shareable URL that opens that
  exact screen directly.
- **acceptance_criteria**: Copy the URL of a profile and of a chirp's conversation, open each in a fresh
  browser context; each lands on that profile / that chirp, not on a generic home.
- **release_gating**: true
- **references**: REQ-PROD-007, REQ-PROD-003

#### REQ-UX-007 — Auth-gated routing returns the person to where they asked to go
- **statement**: Opening a signed-in-only URL without a session routes the person to sign-in, and after a
  successful sign-in returns them to the originally requested screen rather than a default screen.
- **acceptance_criteria**: With no session, open a signed-in-only URL (for example settings); you are
  routed to sign-in; after signing in you land on that settings screen, not on the home timeline.
- **release_gating**: true
- **references**: REQ-PROD-030, REQ-PROD-034

#### REQ-UX-008 — An expired session is intercepted, explained, and recovered from
- **statement**: An action taken with an expired or invalid session routes the person to sign-in with the
  reason stated, preserves in-progress input, and returns them to where they were after they sign back in.
- **acceptance_criteria**: With a session expired, take an action (for example open the timeline or submit
  a drafted chirp); you are routed to sign-in with an explanation, your drafted text is not lost, and after
  signing in you resume where you were.
- **release_gating**: true
- **references**: REQ-PROD-034

#### REQ-UX-009 — Browser back and forward behave predictably
- **statement**: The browser back control returns to the previous screen without re-submitting the prior
  action and without losing the person's place in a scrolled timeline; opening a dialog is a step that back
  dismisses by closing the dialog.
- **acceptance_criteria**: Scroll the timeline, open a chirp, then press back — you return to the timeline
  at your place. Open the compose dialog, then press back — the dialog closes and the underlying screen is
  unchanged. Pressing back after posting does not re-post the chirp.
- **release_gating**: true
- **references**: REQ-PROD-033, REQ-PROD-034

#### REQ-UX-010 — Lists load in bounded pages with a catch-up affordance
- **statement**: Every list loads in bounded pages rather than one unbounded load, offers an explicit way
  to load older items, and the timeline offers a way to pull in chirps posted since the person last looked.
- **acceptance_criteria**: Open a timeline with more items than one page; it loads a bounded page, offers a
  way to load older chirps, and offers a way to load chirps posted since you opened it — it does not attempt
  to load every chirp at once.
- **release_gating**: true
- **references**: REQ-PROD-002

#### REQ-UX-011 — Destructive actions are confirmed before they proceed
- **statement**: Every irreversible or destructive action — delete account, delete a chirp, block or mute,
  end a session, sign out of all sessions — requires an explicit confirmation step that names the
  consequence and offers a cancel before it proceeds.
- **acceptance_criteria**: Initiate account deletion, chirp deletion, a block, and ending a session; each
  presents a confirmation that states what will happen and a cancel. Cancel each; nothing changes. The
  account-deletion confirmation also states what is and is not retained and points to export.
- **release_gating**: true
- **references**: REQ-PROD-022, REQ-PROD-020, REQ-PROD-014, REQ-PROD-027

#### REQ-UX-012 — The result of every action is shown
- **statement**: A completed action is confirmed with brief, non-blocking feedback, and a failed action is
  shown where it was taken — against the field for a form, against the control for an in-place action —
  with enough to understand and retry; no action completes or fails silently.
- **acceptance_criteria**: Publish a chirp, follow an account, and save a setting; each shows brief
  confirmation. Force a failure (for example submit an invalid form, or act while offline); the failure is
  shown at the point of action with a way to retry, not as a silent no-op.
- **release_gating**: true
- **references**: REQ-PROD-033, REQ-PROD-001, REQ-PROD-025

#### REQ-UX-013 — Compose is reachable from anywhere, and addressable
- **statement**: A signed-in person can start composing a chirp from any screen through a persistent
  compose affordance, and a dedicated compose URL supports opening compose directly.
- **acceptance_criteria**: Signed in, from the timeline, a profile, and notifications, open compose from
  the shell without navigating away first. Open the compose URL directly; the compose surface opens.
- **release_gating**: true
- **references**: REQ-PROD-001

#### REQ-UX-014 — Sign-up lands a new account in the product, onboarding first
- **statement**: A completed sign-up establishes the session and lands the person on onboarding — they are
  not prompted to sign in again immediately after creating the account, and they do not land on a blank
  timeline.
- **acceptance_criteria**: Complete a fresh sign-up; you are signed in and land on the onboarding screen
  (which explains the empty state and offers a way toward a non-empty timeline), not on a sign-in prompt
  and not on a blank page.
- **release_gating**: true
- **references**: REQ-PROD-032, REQ-PROD-030, REQ-PROD-031

#### REQ-UX-015 — Sign-in, sign-up, and recovery are interlinked
- **statement**: The sign-in, sign-up, and recovery screens each link to the others, so a person who
  reached the wrong one can correct course without leaving the flow.
- **acceptance_criteria**: On sign-in, find a link to sign-up and to recovery; on sign-up, find a link to
  sign-in; on recovery, find a link back to sign-in. Each link opens the named screen.
- **release_gating**: false — the gated behaviors are the flows themselves (REQ-PROD-010/011/013); the
  cross-links are a convenience a first release can omit, provided recovery remains reachable from help.
- **references**: REQ-PROD-011, REQ-PROD-013

#### REQ-UX-016 — Sign-out returns to the signed-out shell and does not leak back
- **statement**: Signing out ends the session and returns the person to the signed-out landing; after
  sign-out, the browser back control does not re-expose a protected screen's content.
- **acceptance_criteria**: Signed in on a screen, sign out; you land on the signed-out landing. Press back;
  you do not see the protected screen's content — you remain in the signed-out shell or are routed to
  sign-in.
- **release_gating**: true
- **references**: REQ-PROD-014

#### REQ-UX-017 — Settings groups account-level choices, each addressable
- **statement**: Account-level choices live under one settings area with labelled sub-sections — edit
  profile, account & contact, notification preferences, sessions & devices, blocked & muted, export, delete
  — each independently addressable and each returning to the settings hub.
- **acceptance_criteria**: Open settings; the sub-sections above are listed. Open each directly by its URL;
  it opens on that sub-section. From a sub-section, return to the settings hub.
- **release_gating**: true
- **references**: REQ-PROD-017, REQ-PROD-012, REQ-PROD-019, REQ-PROD-020

#### REQ-UX-018 — The rules and a help entry are reachable from both shells
- **statement**: The rules/terms and a user-facing help & support entry are reachable from both the
  signed-out shell and the signed-in shell.
- **acceptance_criteria**: With no session, reach Rules & terms and Help & support from the signed-out
  shell. Signed in, reach both from the account menu. Each opens the named screen.
- **release_gating**: true
- **references**: REQ-PROD-026, REQ-PROD-028

#### REQ-UX-019 — A notifications entry with an unseen-activity indicator
- **statement**: The signed-in shell carries a notifications entry that indicates unseen activity and
  leads to the notifications list.
- **acceptance_criteria**: Have another account reply to, follow, or like you; the shell's notifications
  entry shows an unseen indicator. Open it; the notifications list shows the activity and the indicator
  clears.
- **release_gating**: false — notifications ride REQ-PROD-029, which the release bar does not gate; the
  entry and its indicator ship with notifications when notifications ship.
- **references**: REQ-PROD-029
