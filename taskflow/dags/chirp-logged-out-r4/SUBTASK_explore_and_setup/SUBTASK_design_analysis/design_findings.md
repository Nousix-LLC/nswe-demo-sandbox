# Design Documents Findings

> Source documents read:
> - `design/product-requirements.md` (via `taskflow/dags/design-chirp-r1/SUBTASK_product_requirements/outputs/product-requirements.md`)
> - `design/experience-design.md` (via `taskflow/dags/design-chirp-r1/SUBTASK_experience_design/outputs/experience-design.md`)
> - `design/release-bar.md` (via `taskflow/dags/design-chirp-r1/SUBTASK_release_bar/outputs/release-bar.md`)
>
> Note: canonical design documents live in the design-chirp-r1 task outputs; the paths in the brief (`design/*.md`) refer to these same documents as committed to the repository. All content is current as of commit `c805525`.

---

## Screen States Required

### Public home/timeline (Landing at `/`, no session)

The Landing is the signed-out face of `/`. When a sample of real public chirps is served, the content column shows:

- **Loading**: `LoadingState` skeleton `ChirpCard` rows rendered at real ChirpCard dimensions while the resource resolves — the column does not jump when content arrives; the shell and explanatory hero render immediately on first paint.
- **Empty** (no public content available): The Landing shows the explanatory hero block explaining what chirp is + Sign up and Sign in actions. The sample content region shows an explanatory block with a next step; never a blank area.
- **Error** (failed load): An inline `"couldn't load — try again"` message with a retry control replaces the unloaded items while any already-loaded content stays on screen. Visibly distinct from the empty state; never a frozen screen or silent failure.
- **End-of-list**: A load-older control at the bottom of the list; when no more items remain the control is absent (no phantom spinner).

### Sign up screen (`/signup`)

- **Empty**: Fresh form — labels and placeholders, no values, Create account disabled; required-but-empty fields not shown as errors until touched.
- **Error**: Field-level `InlineError` against the offending field (e.g., taken handle → "That handle's already taken — try another"; ill-formed handle → "Handles can use letters, numbers, and underscores, up to 15"). A failed submit shows an `InlineError` at the point of the problem with the person's values preserved.
- **Loading**: Handle availability check shows a pending state on the handle field (not prematurely valid or invalid).

### Sign in screen (`/signin`)

- **Empty**: Labelled fields, no values, Sign in disabled.
- **Error**: Not-found and wrong-credential are distinguishable; neither reveals account existence beyond what the public profile already shows; no raw system code.

### General (all surfaces)

Per REQ-UX-031 and BAR-260: every surface has three visually distinct states — an **explained empty block** (never blank), a **loading skeleton** (never a blank spinner), and a **"couldn't load — try again" inline error** (never a frozen screen). These three are visually different from each other.

---

## Route Names from Design

Exact routes as specified in the experience-design.md screen inventory (§1 Information Architecture):

| Screen | Route | Auth State |
|--------|-------|------------|
| Landing (public home/timeline) | `/` (no session) | signed-out |
| Sign up | `/signup` | signed-out |
| Sign in | `/signin` | signed-out |
| Public profile | `/@:handle` | both (signed-out & signed-in) |
| Recover access | `/recover` | signed-out |
| Set new credential | `/recover/confirm` | signed-out |
| Home timeline | `/` (session present) | signed-in |

**Key route names for this feature:**
- **Sign-in route name/path**: `Sign in` / `/signin`
- **Sign-up route name/path**: `Sign up` / `/signup`
- **Public home/timeline route**: Landing at `/` (no session) — same path as home timeline but rendered in the signed-out shell
- **Public profile route**: `/@:handle` — uses the handle as the URL segment (not the internal id as in the current codebase `c805525` which uses `/user/:id`)

> Note: The current codebase at `c805525` uses `/user/:id` for profiles. The design specifies `/@:handle`. The frontend implementation will need to route `/@:handle`.

---

## Product Requirements (REQ-PROD-013..015)

### REQ-PROD-013 — Self-service account recovery
- **Statement**: A person who has lost their credential can regain access themselves, through the verified contact, without another person acting on their behalf.
- **Acceptance criteria**: Having lost your credential, use a "can't get in?" path, prove control of the verified contact, and regain access. Someone without that verified contact cannot recover the account.
- **Release gating**: `true` (depends on REQ-PROD-012 — verified contact captured at sign-up)

### REQ-PROD-014 — Sign-out that ends the session server-side
- **Statement**: A person can end their session so it can no longer be used — important on a shared or public device.
- **Acceptance criteria**: Sign out; then present the session that was in use — it is rejected. The next person at that device is not signed in as you.
- **Release gating**: `true`

### REQ-PROD-015 — Stay signed in across ordinary visits on a trusted device
- **Statement**: On a device a person chooses to trust, they remain signed in across ordinary visits, subject to session expiry and to sign-out.
- **Acceptance criteria**: Sign in, close and reopen the app on the same device within the session's validity; you are still signed in. After expiry or sign-out, you are returned to sign-in.
- **Release gating**: `false` — a releasable product may require sign-in each visit; staying signed in is an expected convenience the experience/identity design tunes. Recorded so the choice is explicit rather than assumed.

---

## UX Requirements

### REQ-UX-002 — A signed-in shell exposing every primary destination
- **Statement**: After signing in, a persistent shell exposes Home, Explore, Notifications, Profile, Settings, and a Compose affordance, present and reachable from every signed-in screen.
- **Acceptance criteria**: Signed in, from the timeline, a profile, a conversation, and a settings sub-section: Home, Profile, and each primary destination the product ships are reachable from each in one step, and the current destination is marked active.
- **Release gating**: `true`
- **Logged-out relevance**: Establishes the signed-in shell against which the signed-out shell (REQ-UX-001) is defined. The landing screen and public profile render in the signed-out shell (Sign up + Sign in entries) rather than this signed-in shell.

### REQ-UX-030 — People are shown consistently, and a missing picture is never broken
- **Statement**: Avatars are rendered consistently (circular, from a fixed set of sizes), and a person with no picture is shown a readable initials placeholder rather than a broken-image glyph.
- **Acceptance criteria**: Across the feed, a profile header, and the navigation, the same person's avatar is the same size and shape; a person with no uploaded picture shows readable initials rather than a broken image or an empty box.
- **Release gating**: `false` — the designed avatar system is polish; the hard minimum (no broken image) is carried by REQ-UX-031 / REQ-PROD-033.

### REQ-UX-031 — Empty, loading, and error states have a designed visual treatment
- **Statement**: Empty lists, loading content, and failed actions each have a defined visual treatment drawn from the system — an explanatory empty block, a loading skeleton, and an inline error in the danger role — rather than a blank area, a frozen screen, or a raw failure.
- **Acceptance criteria**: Force an empty list, a loading list, and a failed action on each of the timeline, a conversation, and a profile; each shows a visually distinct designed treatment, not a blank, a frozen spinner, or a raw failure.
- **Release gating**: `true`
- **Logged-out relevance**: Directly maps to AC-5. The public timeline Loading / Empty / Error / End-of-list states must each have a distinct visual treatment.

### REQ-UX-032 — A consistent voice, with plain and actionable errors
- **Statement**: UI copy follows one voice — sentence case, verbs on action buttons, consistent product terms — and error messages are in plain language that says what happened and what to do, never exposing a system or error code.
- **Acceptance criteria**: Action buttons across several screens read as sentence-case verbs (e.g., "Post", "Follow", "Save changes"). A forced error (invalid form entry, failed submit) shows a plain-language message with a way forward and no raw error code, stack text, or internal identifier.
- **Release gating**: `true`
- **Logged-out relevance**: Error messages on the Landing ("couldn't load" etc.) and navigation labels ("Sign up", "Sign in") must follow this voice rule.

---

## BAR-011 Checklist Items

BAR-011 in the release bar enforces REQ-PROD-023 (authorization boundary): "Signed in as one account, every attempt through the product's surfaces to act as another account — post, reply, like, or follow as them, edit their profile or settings, or delete their content — is refused." This is the authorization floor; for the logged-out feature, the complementary check is that unauthenticated readers can reach public endpoints (GET only) without a bearer token.

The release bar criteria that check each AC for issue #35:

- **AC-1** (logged-out visitor loads public timeline and profile without sign-up/sign-in):
  BAR-006 (`usable_early` · `automated_test`) — A user's public profile — handle, display name, bio, and follower/following counts — is viewable with no session. _Enforces REQ-PROD-007._ (The public timeline itself is new functionality from this issue; no existing BAR covers it yet — it will need a new automated_test criterion.)

- **AC-2** (on arrival with no content, visitor sees "what chirp is" + sign-up/sign-in route):
  BAR-026 (`usable_early` · `manual_user_check`) — A visitor arriving with no account and no session sees an explanation of what chirp is and a clear path to sign up, rather than being stopped at a sign-in wall. _Enforces REQ-PROD-030._

- **AC-3** (if timeline fails to load, a clear recoverable message is shown — not a broken screen):
  BAR-028 (`usable_early` · `manual_user_check`) — An empty list, a loading list, and a failed action each present a state the person can understand and act on, rather than a blank area or a silent failure. _Enforces REQ-PROD-033._

- **AC-4** ("Create an account" route visible on landing and sign-in screen, leads to sign-up):
  BAR-200 (`usable_early` · `manual_user_check`) — With no session, every signed-out screen (at minimum the landing and a public profile opened by direct link) carries the chirp wordmark, a Sign in entry, and a prominent Sign up entry; from each, a person can act (sign in, sign up) without first being signed in and without reaching a dead end. _Enforces REQ-UX-001._

- **AC-5** (loading, empty, error, and end-of-list states each visually distinct, never blank):
  BAR-260 (`usable_early` · `manual_user_check`) — On each surface a person can force an empty result, a failed load, and a first load and sees, respectively, an explained empty treatment carrying at least one next step (never a blank region), a distinct "couldn't load — try again" treatment with a retry, and a loading treatment — with the empty treatment and the failed treatment visibly different from each other. _Enforces REQ-UX-085, REQ-UX-086, REQ-PROD-033, REQ-PROD-034._
