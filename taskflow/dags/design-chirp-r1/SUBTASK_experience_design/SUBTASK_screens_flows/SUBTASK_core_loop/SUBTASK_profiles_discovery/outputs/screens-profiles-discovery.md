### Core loop — profiles, followers/following, and discovery

This part of the core loop covers how a chirper meets other people: the profile where someone's
identity and chirps live, the followers and following lists that hang off it, and the Explore screen
where a person looks for someone to follow in the first place. These are the screens a stranger uses to
decide who is worth following and to find their way to those accounts, so each is designed as a real
screen — layout, content, one clear primary action, and the empty, error, and loading states it meets in
ordinary use — not a route with a name.

Every screen here is built from the frozen component library and named in the screen inventory; nothing
below invents a screen or a component outside those vocabularies. Two behaviours that appear on these
screens are owned elsewhere and are composed, not redesigned here: the **follow / unfollow** control (the
`social_actions` part) and **edit profile** (the account-lifecycle part). Where this part shows one of
them, it places the existing control and links to the existing screen.

---

#### Public profile — `/@:handle` (profile archetype; reachable signed-out and signed-in)

A profile is the public face of one account and the thing a person reads before deciding to follow. It is
reachable without a session, because people arrive here from shared links and from replies, and a visitor
on such a link should land on real content with a visible way to join rather than an auth wall.

**Layout.** The reading column at `space.measure`, inside the shell for the current auth state
(`NavShell` signed-out for a visitor, signed-in for a member). Top to bottom:

- **`ProfileHeader`** — `Avatar` at `avatar.xl`, the display name in `type.title`, the `@handle` and bio in
  `type.body` / `color.text.secondary`, and the follower and following counts in
  `type.meta` + `type.numeral.tabular` so a changing count does not shift the layout. Each count is a
  labelled link that opens the Followers or Following list.
- Below it, a **`ListView`** of the account's own chirps as `ChirpCard`s, newest first, in bounded pages
  with the load-older affordance — the same `ListView` and `ChirpCard` the timeline uses, so a chirp reads
  the same here as anywhere.

**Content.** Handle, display name, bio, the two counts, and the person's chirps. Nothing here needs a
session to be shown (REQ-PROD-007).

**Primary action.** The header's context action: for another account, the **follow control** owned by the
`social_actions` part (`PrimaryButton` "Follow" / `SecondaryButton` "Following"), placed in the header and
behaving as that part specifies — this part does not redesign it. A signed-out visitor who presses it is
routed to sign-in and returned to the profile (the IA's auth-gated routing), so follow is never a silent
dead-end for someone without a session.

**States.**
- **Empty** — a sparse profile (no bio, zero followers and following, no chirps yet): the `ProfileHeader`
  *empty* state renders the bio space and the counts as calm, labelled zeros ("0 followers", "0
  following") with a one-line note rather than blank gaps, and the chirp `ListView` shows its `EmptyState`
  ("@handle hasn't chirped yet") instead of an empty column. The header is never shown as broken just
  because it is sparse.
- **Error** — three cases, each distinct from empty so the two are never confused: (1) the profile fails
  to load → the `ProfileHeader` *error* state via an `EmptyState` error variant ("We couldn't load this
  profile — try again") with a retry; (2) the account is blocked, suspended, or does not exist → a plain
  statement of that in place of the header ("This account doesn't exist" / "This account is unavailable"),
  not a half-drawn header and not the generic Not-found screen; (3) a page of chirps fails while the
  header loaded fine → the chirp `ListView` *error* state (`InlineError` with retry) in place of the
  missing page, keeping any chirps already shown.
- **Loading** — the `ProfileHeader` *loading* skeleton (skeleton avatar, name line, bio line, count line)
  above the `ListView` *loading* skeleton rows, both at their real dimensions so the screen does not jump
  when content arrives. A first load shows skeletons, not a spinner on a blank column.

---

#### Own profile — `/@:handle` for the signed-in owner (profile archetype; signed-in)

The same screen a member's own account presents to the world, shown to the owner with the one thing a
visitor does not get: the way in to change it.

**Layout and content.** Identical to the public profile — `ProfileHeader` over a `ListView` of the
owner's own chirps — so a person sees exactly their own public face. The difference is confined to the
header's action and the per-chirp actions.

**Primary action.** In place of Follow, the header shows **"Edit profile"** as a `SecondaryButton` that
opens the Edit profile screen (`/settings/profile`). Edit profile is the account-lifecycle part's surface;
this part places the entry and links to it, and does not design the editing form. On the owner's own
`ChirpCard`s, the more-actions menu exposes **delete** (the confirmation `Dialog` is owned by the
posting/safety parts) — referred to, not redesigned here.

**States.**
- **Empty** — a brand-new owner who has not chirped: the chirp `ListView` *empty* state speaks to the
  owner rather than about a third party ("You haven't chirped yet — write your first one") and offers the
  Compose affordance as the next step; the header shows the owner's real (possibly zero) counts as labelled
  zeros. This complements onboarding (the account-lifecycle part); it does not replace it.
- **Error** — as the public profile (profile fails to load → `EmptyState` error variant with retry; a
  chirp page fails → `ListView` error with retry). The blocked/suspended case does not arise for one's own
  account; a session that has expired routes to sign-in per the IA and returns the owner here.
- **Loading** — as the public profile: header skeleton over `ListView` skeleton rows.

---

#### Followers and Following — `/@:handle/followers` and `/@:handle/following` (feed/list; signed-out and signed-in)

The two lists that hang off a profile: who follows this account, and who this account follows. They are
one designed pattern used at two routes, each addressable so a person can link to or bookmark the exact
list. Both are reachable from the profile's count links and carry a labelled way back to the profile.

**Layout.** The reading column, a `type.title` heading naming the list and whose account it belongs to
("People who follow @handle" / "People @handle follows"), then a **`ListView`** of **person rows**. Each
row is `Avatar` at `avatar.md`, display name in `type.heading`, `@handle` in `type.meta`, a one-line bio
in `type.body` / `color.text.secondary`, and — for a signed-in viewer — the **follow control** (the
`social_actions` part's control) on the trailing edge. The whole row, excluding the follow control, is a
target that opens that person's profile. Loaded in bounded pages with load-older, per the IA's pagination
convention.

**Content.** One row per account, with enough to recognise the person and decide whether to follow them,
and the follow control to act on that decision in place.

**Primary action.** Open a person's profile (the row), or follow/unfollow them from the row's follow
control without leaving the list. A signed-out viewer sees the rows and the counts but is routed to
sign-in if they try to follow.

**States.**
- **Empty** — the `ListView` *empty* state, worded for which list it is: a followers list with no one →
  "@handle doesn't have any followers yet"; a following list with no one → on another account, "@handle
  isn't following anyone yet", and on the owner's own following list, "You're not following anyone yet"
  with Explore offered as the next step, so an empty following list points at the way to fix it.
- **Error** — a page fails to load → the `ListView` *error* state (`InlineError` with retry) in place of
  the missing rows; a failure while loading an older page shows at the load-more boundary and keeps the
  rows already shown.
- **Loading** — the `ListView` *loading* skeleton rows at person-row dimensions on first load; a bounded
  spinner at the boundary when loading older rows.

---

#### Explore / find people — `/explore` (feed/list; signed-in)

Where a chirper finds someone to follow when they do not already hold a link to a profile. Today a person
can only reach an account through an external link or a reply; Explore is the surface that closes that
gap (REQ-PROD-042). It is in scope and fully designed here; the release bar decides whether a first
release ships it (see the gating note on REQ-UX-064).

**Layout.** The signed-in shell with Explore marked as the active destination, then the reading column:

- A **`TextField`** search input at the top (label "Find people", a plain placeholder), the one input on
  the screen.
- Below it, a **`ListView`** of results as person rows (the same row as the followers/following lists —
  `Avatar`, name, handle, bio snippet, and the follow control), in bounded pages.

**Content.** A query field and a list of people who match it, each with enough to recognise them and the
follow control to act. Before any query, the screen shows whatever suggestions the product can offer
(for example, a short list of accounts to follow); if it can offer none, it shows the prompt alone.

**Primary action.** Search for a person, then follow a result from its row (the `social_actions` control)
or open their profile — without leaving Explore.

**States.**
- **Empty** — two distinct cases: (1) no query entered yet → a prompt to search, plus any available
  suggestions; if there are no suggestions, the `EmptyState` prompt stands alone ("Search for people to
  follow") rather than a blank screen; (2) a query that matches no one → the `ListView` *empty* state as a
  "no results" block ("No people found for that search") with a way to refine the query. The
  no-query and no-results states read differently so a person can tell "nothing searched yet" from
  "nothing found".
- **Error** — the search request fails → the `ListView` *error* state (`InlineError` with retry) in place
  of results, the query preserved so the person can retry without retyping.
- **Loading** — `ListView` *loading* skeleton rows while a search resolves; a bounded spinner at the
  boundary when loading further pages of results.

---

#### How these screens compose with the rest of the product

- **Shared vocabulary.** Every screen above is an inventory screen referred to by its name and route, and
  is assembled from library components (`ProfileHeader`, `ListView`, `ChirpCard`, `Avatar`, `TextField`,
  `EmptyState`, `LoadingState`, `InlineError`, and the action buttons). No screen or component outside
  those vocabularies is introduced.
- **Borrowed controls.** The follow/unfollow control (the `social_actions` part) and the Edit profile
  screen (the account-lifecycle part) are placed and linked, not redesigned.
- **States against the global patterns.** Each per-screen empty, error, and loading state above is the
  relevant component's own named state, and each is consistent with the product-wide empty / loading /
  error patterns and the expired-session recovery owned by the considered-states part. These screens
  compose that global treatment; they do not define a competing per-screen pattern.

---

#### Requirements — REQ-UX-061..064

Each requirement is testable by someone who never met its author, exercisable on the live product. Each
carries a `release_gating` flag and references the product requirement(s) it serves.

##### REQ-UX-061 — A public profile shows identity and chirps, with or without a session
- **statement**: A user's profile at `/@:handle` shows their avatar, display name, handle, bio, and
  follower and following counts, above their own chirps in newest-first bounded pages, and is reachable
  both signed-out and signed-in.
- **acceptance_criteria**: With no session, open a profile link; the header shows the handle, display
  name, bio, and the follower and following counts, and the person's chirps load below in a bounded page
  with a way to load older ones. Signed in, open the same profile and see the same content plus the follow
  control in the header.
- **release_gating**: true
- **references**: REQ-PROD-007

##### REQ-UX-062 — The owner's profile is their public face with a way to edit it
- **statement**: When the signed-in owner opens their own profile, they see the same public profile
  anyone else sees, with an "Edit profile" entry in place of the follow control that opens the edit-profile
  screen.
- **acceptance_criteria**: Signed in, open your own profile; it shows your avatar, display name, handle,
  bio, counts, and your chirps as a visitor would see them, and an "Edit profile" control that opens the
  edit-profile screen. The follow control is not shown on your own profile.
- **release_gating**: true
- **references**: REQ-PROD-007

##### REQ-UX-063 — Followers and following are addressable, paginated lists
- **statement**: A profile's follower and following counts open the `/@:handle/followers` and
  `/@:handle/following` lists, each an addressable, paginated list of people showing enough to recognise
  each account, with the follow control on each row for a signed-in viewer and a labelled way back to the
  profile.
- **acceptance_criteria**: From a profile, open the followers list by its count; it shows one row per
  follower (avatar, name, handle, bio) in a bounded page with a way to load more, a way back to the
  profile, and — signed in — a follow control per row. Open the following list the same way with the same
  behaviour. Open each list's URL directly; it lands on that list.
- **release_gating**: true
- **references**: REQ-PROD-007, REQ-PROD-006

##### REQ-UX-064 — A way to find people to follow
- **statement**: A signed-in person can find accounts to follow from within the product at `/explore`, by
  searching for people and following a result in place, without already holding a link to a profile.
- **acceptance_criteria**: Signed in and holding no external link, open Explore, search for a person, and
  follow at least one result from the list without leaving the screen; a search that matches no one shows a
  "no results" state with a way to refine, distinct from the before-you-search prompt.
- **release_gating**: false — Explore implements REQ-PROD-042, which the product requirements do not gate;
  a first release may ship with follow-by-profile and follow-from-a-reply and add discovery as a near-term
  follow-up. The release bar should decide explicitly what minimum discovery v1 includes.
- **references**: REQ-PROD-042

---

*Scope note.* This part designs the view-a-profile surfaces (public profile, own profile, followers,
following) and the discovery/find-people surface (Explore). The follow/unfollow control these screens
carry is designed by the social-actions part; edit profile and account onboarding are the
account-lifecycle part's; the product-wide empty/error/loading patterns and expired-session recovery are
the considered-states part's. All are composed and referenced here, not redesigned.

*Methodology note.* The design methodology loader was unavailable in this environment, so these surfaces
were designed from the intended Experience Design posture (designed screens with their empty/error/loading
states, composed from a shared component vocabulary) and the Product Strategy framing of the identity and
discovery journey, rather than from a loaded methodology bundle. The limitation is recorded; it did not
block the work.
