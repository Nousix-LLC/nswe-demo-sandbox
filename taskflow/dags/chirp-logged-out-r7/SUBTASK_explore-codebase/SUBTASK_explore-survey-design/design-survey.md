# Design Survey — Chirp Logged-Out Visitor Experience

Extracted from `design/product-requirements.md`, `design/experience-design.md`, and
`design/release-bar.md` on `main` at `cb1ced3`.

---

## 1. Acceptance Criteria

### AC-1 — Unauthenticated timeline and profile reading

**Requirement IDs:** REQ-PROD-013 / BAR-011

**Verbatim text (product-requirements.md §4.C):**
> "A logged-out visitor can load the home timeline and open a user profile and read their chirps
> without being forced to create an account or sign in first."
> — *release_gating: true; traces to J1, J5*

**Verbatim text (release-bar.md §C, BAR-011):**
> "A logged-out visitor can read the public timeline and the profiles reached from it without
> signing in; the logged-out landing says what chirp is, offers an obvious join route, and handles
> its loading, empty, error, and end-of-list states honestly (no blank or broken screen when there
> is nothing yet)."
> — *verification_method: manual_user_check; stage: usable_early*

**Source sections:** product-requirements.md §4.C (REQ-PROD-013); release-bar.md §C (BAR-011).

**UI implications:**
- The home/public timeline route (`/`) must be accessible without a session cookie or token.
- Opening a chirp author's profile from the timeline must not trigger a sign-in redirect.
- Any existing auth middleware that gates `GET /` or `GET /<handle>` must be removed or made
  optional for the read path; authenticated actions (post, like, follow) remain gated.

---

### AC-2 — Useful empty-state landing

**Requirement IDs:** REQ-PROD-014 / BAR-011

**Verbatim text (product-requirements.md §4.C):**
> "The first screen communicates what chirp is and stays useful even when there is little or no
> content."
>
> Acceptance criteria: "The first screen shows either real content (the public timeline with at
> least one chirp) or a clear statement of what chirp is with a prominent sign-up / sign-in action
> — it never shows a blank page, a spinner with no exit, or an unexplained error message."
> — *release_gating: true; traces to J1*

**Verbatim text (experience-design.md §6, REQ-UX-030):**
> "On arrival a logged-out visitor can tell what chirp is and always sees an obvious way to create
> an account or sign in, whether or not there is any content yet."
>
> Acceptance criteria: "Opening chirp while logged out shows a one-line statement of what chirp is
> together with a visible **Create account** and **Sign in**; when the public timeline has no
> chirps, the screen shows a clear 'what chirp is + be the first' message with a working
> **Create account** action rather than a blank page; neither the statement nor the join controls
> require scrolling past a login wall."
> — *release_gating: true; traces to REQ-PROD-013, 014, 015; J1*

**Source sections:** product-requirements.md §4.C (REQ-PROD-014); experience-design.md §6
(REQ-UX-030).

**UI implications:**
- The landing `empty` state is a distinct designed screen: a one-line "what chirp is" statement
  plus a prominent **Create account** CTA and a **Sign in** link.
- The `empty` state must never be blank — it must render even with zero chirps in the database.
- The statement and CTAs must be above-the-fold (no scrolling required).
- The header/nav (Sign up, Sign in) must remain visible in both the `empty` and `content` states.

---

### AC-3 — Recoverable timeline error state

**Requirement IDs:** REQ-PROD-014 / BAR-011

**Verbatim text (product-requirements.md §4.C, REQ-PROD-014 AC continued):**
> "If the timeline fails to load, the screen shows a plain, honest message and a way to try again
> — not a broken page, a raw error code, or a silent failure."

**Verbatim text (experience-design.md §6, REQ-UX-032):**
> "on a failed load, a plain message with a **Try again** that refetches without reloading the
> whole page"

**Source sections:** product-requirements.md §4.C (REQ-PROD-014); experience-design.md §6
(REQ-UX-032).

**UI implications:**
- The timeline component has an `error` state distinct from `loading` and `empty`.
- The **Try again** action triggers a data refetch of only the timeline component — it must not
  cause a full-page navigation or reload.
- The error message must be in plain language (no raw HTTP status codes or Rust panic output).
- The header chrome (wordmark, Sign up, Sign in) must remain visible during the `error` state.

---

### AC-4 — Visible "create an account" route

**Requirement IDs:** REQ-PROD-015 / BAR-011

**Verbatim text (product-requirements.md §4.C):**
> "A visitor who decides to join always has a visible way to do so."
>
> Acceptance criteria: "A 'Create an account' control is visible on the first screen (the public
> landing) and on the sign-in screen; following it reaches the sign-up screen."
> — *release_gating: true; traces to J1, J2*

**Verbatim text (experience-design.md §6, REQ-UX-002):**
> "On every logged-out surface, a persistent Sign up and Sign in are visible; the landing/home
> timeline and user profiles are readable without signing in; and a 'create an account' control is
> present on the first screen and on the sign-in screen."
> — *release_gating: true; traces to J1; REQ-PROD-013, 014, 015*

**Source sections:** product-requirements.md §4.C (REQ-PROD-015); experience-design.md §6
(REQ-UX-002, REQ-UX-030).

**UI implications:**
- Logged-out navigation chrome must include both **Sign up** and **Sign in** on every logged-out
  surface (landing, profiles, sign-in screen, sign-up screen).
- The sign-in screen (`/signin`) must display a **Create an account** link that navigates to
  `/signup`.
- Following any **Create account** / **Sign up** CTA must reach `SCR-signup` (`/signup`).
- The sign-up and sign-in screens are interlinked: each must have a visible link to the other.

---

### AC-5 — Visually distinct loading / empty / error / end-of-list states

**Requirement IDs:** REQ-UX-002 / REQ-UX-030 / REQ-UX-031 / REQ-UX-032 / BAR-011 /
one-state-model criterion

**Verbatim text (issue #35 / _GLOBAL.md):**
> "The logged-out landing/timeline renders its loading, empty, error, and end-of-list states
> accurately and distinctly — each state is a visually distinct screen, never a blank page or a
> stale view."

**Verbatim text (experience-design.md §6, REQ-UX-032):**
> "A visitor sees shape-matched placeholders on first load (chrome and join route still usable);
> an explained empty state with a next action when there are no chirps; on a failed load, a plain
> message with a **Try again** that refetches without reloading the whole page; and a clear 'you're
> all caught up' marker at the end of the list, visibly different from the empty state."
> — *release_gating: true; traces to REQ-PROD-014, 018; J1. Instantiates state model
> REQ-UX-021..025.*

**Source sections:** experience-design.md §6 (REQ-UX-032); _GLOBAL.md (issue #35 ACs);
release-bar.md §C (BAR-011).

**UI implications:**
- Four states of `SCR-landing_timeline` must be visually distinguishable at a glance:
  `loading` ≠ `empty` ≠ `error` ≠ `end_of_list`.
- `loading`: shape-matched skeleton placeholders — same card geometry as real chirps; header
  chrome (wordmark, Sign up, Sign in) is fully usable during load.
- `empty`: "what chirp is + be the first" copy + working **Create account** action; must look
  intentionally designed, not like a broken list.
- `error`: plain-language message + **Try again** button (in-place refetch, no full reload).
- `end_of_list`: explicit "you're all caught up" (or equivalent) marker after the last chirp;
  must be visually distinct from an empty timeline.
- State vocabulary is **frozen** by the one-state-model: `loading`, `content`, `empty`, `error`,
  `not_found`, `end_of_list`, `session_expired`, `validation`, `busy_submitting`, `success`.
  No new state names may be introduced for this feature.

---

## 2. Screen and State Inventory — Logged-Out Experience

### Screens in scope

| Screen ID | Route | Description |
|---|---|---|
| `SCR-landing_timeline` | `/` | Primary logged-out surface; public timeline; home for all logged-out visitors |
| `SCR-profile` | `/<handle>` (contextual, reached via author links) | Read-only public profile; reachable from timeline chirp cards without sign-in |
| `SCR-signup` | `/signup` | Account creation; reachable from logged-out nav and from `SCR-signin` |
| `SCR-signin` | `/signin` | Credential sign-in; reachable from logged-out nav and from `SCR-signup` |

### Logged-out navigation chrome (all logged-out surfaces)

Persistent on every logged-out screen: **Sign up** (links to `/signup`) and **Sign in** (links to
`/signin`). The product wordmark routes to `SCR-landing_timeline`. This chrome is never replaced
by a "you must sign in" gate for reading surfaces.

### States of `SCR-landing_timeline`

| State | Trigger | Required UI behavior | One-state-model token |
|---|---|---|---|
| **loading** | Timeline fetch in-flight (initial load or refetch) | Shape-matched skeleton placeholders matching chirp card geometry; header chrome and Sign up / Sign in remain usable | `loading` |
| **content** | Timeline fetch succeeded; ≥1 chirp returned | Reverse-chronological list of chirp cards; each author name/handle is a link to their `SCR-profile` | `content` |
| **empty** | Timeline fetch succeeded; 0 chirps returned | One-line statement of what chirp is + "be the first" message + working **Create account** action; never a blank page | `empty` |
| **error** | Timeline fetch failed (network error, server error) | Plain-language message + **Try again** button that triggers in-place refetch (no full-page reload); header chrome visible | `error` |
| **end_of_list** | Timeline fetch returned final page; user has scrolled to bottom | Explicit "you're all caught up" (or equivalent) marker after last chirp; visually distinct from `empty` state | `end_of_list` |

### States of `SCR-profile` (read-only)

The design docs specify this screen is reachable without a session (REQ-UX-031) but do not
provide a full per-state matrix for the logged-out profile view. Minimum implied states:

| State | Trigger | Required UI behavior | One-state-model token |
|---|---|---|---|
| **loading** | Profile fetch in-flight | Shape-matched placeholders (consistent with landing_timeline pattern) | `loading` |
| **content** | Profile fetch succeeded; profile + chirps returned | Profile header + chirps list; header chrome with Sign up / Sign in visible | `content` |
| **empty** | Profile exists; user has no chirps | Profile header + "no chirps yet" message; not a blank page | `empty` |
| **not_found** | No profile for that handle | Honest "this user doesn't exist" message with a route back to landing | `not_found` |

### States of `SCR-signin`

Relevant to AC-4: must include a visible **Create an account** / **Sign up** link. No other
logged-out state behavior specified in the scoped design docs beyond REQ-UX-036/037 (which are
beyond this feature's AC scope).

### States of `SCR-signup`

Relevant to AC-4 (the destination a "Create an account" CTA reaches). No additional state
behavior is in scope for this logged-out reading feature beyond confirming the route is reachable.

---

## 3. Open Questions

The following ambiguities in the design docs are worth flagging for the backend and frontend tasks:

**OQ-1 — Public timeline API endpoint existence**
The design docs specify unauthenticated reading is required (REQ-PROD-013) but do not describe
the HTTP shape of the public timeline endpoint. The backend task should confirm: does a
`GET /api/timeline` (or equivalent unauthenticated route) exist, or does the current timeline
endpoint require a session? The API contract (`contracts/public_api_contract.md`) declares the
intended surface; the backend survey will clarify current state.

**OQ-2 — Profile route auth behavior**
REQ-UX-031 says profiles reached from the landing are readable without signing in, but it's
unclear whether the existing `/<handle>` route is currently gated. The backend survey should
confirm whether the profile handler passes authentication as optional or mandatory.

**OQ-3 — SCR-profile state matrix**
The design docs specify `SCR-landing_timeline` states in full detail (REQ-UX-032) but only
imply the read-only profile states via REQ-UX-031. The frontend task should apply the same
one-state-model tokens (loading / content / empty / not_found) consistently, but should note that
no verbatim AC covers the exact profile state copy or layout.

**OQ-4 — "What chirp is" copy**
REQ-UX-030 requires "a one-line statement of what chirp is" in the empty state and as persistent
above-the-fold context, but the design docs do not specify the exact copy. The frontend task will
need to supply or request this copy before implementing the empty state.

**OQ-5 — Skeleton placeholder specifics**
REQ-UX-032 requires "shape-matched placeholders" for the loading state but does not prescribe
the exact card geometry (dimensions, number of placeholder cards). The frontend task will need to
derive these from the actual chirp card design or specify them in its implementation notes.

**OQ-6 — Sign-in prompt mechanism for account-required actions**
REQ-UX-031 specifies that a sign-in prompt appears only when a logged-out visitor attempts an
action requiring an account (post, like, follow). The design docs do not specify the exact
mechanism — modal overlay, inline callout, or redirect. This is a frontend UX detail that falls
outside this feature's gating ACs (which cover reading, not interactive actions), but the frontend
task should decide the approach consistently with the one-state-model (the `session_expired` token
is the nearest analogue in the vocabulary).
