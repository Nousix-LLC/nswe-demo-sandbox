# SYNTHESIS.md — chirp-logged-out-r21

## Overall Verdict: PASS

All 5 acceptance criteria for issue #35 — "Logged-out reading and a useful landing with accurate states" — are MET by the code on branch `work/chirp-logged-out`.

**Final head SHA at synthesis time**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`
(Branch advanced one commit beyond the brief's stated head `617f2539`; this commit — "fix(chirp-frontend): add /sign-in alias route" — was included in CI run 42194072348 which completed with conclusion=success on all 6 checks.)

**CI**: Run 42194072348 — all 6 checks green (`wasm`, `doc`, `test`, `clippy`, `fmt`, `image`) on `decb6196`.

**PR**: #263 — OPEN / mergeable=true / mergeable_state=clean.

---

## Per-Criterion Assessment

### AC-1 — Unauthenticated Public Timeline and User Profile
**STATUS: MET**

A logged-out visitor can load the home/public timeline and read a user profile without signing in.

Evidence:
- **Backend**: `GET /api/chirps` → `handlers::public_chirps` — no `AuthUser` extractor; uses only `Query<PublicTimelineQuery>` and `State<AppState>`. Returns `PublicTimelineResponse { chirps, has_more }` unauthenticated.
- **Backend**: `GET /api/users/{username}/chirps` → `handlers::user_chirps` — no `AuthUser` extractor; returns 404 on unknown username, 200 with chirps otherwise. No auth required.
- **Frontend router** (`app.rs`): Routes `"/"` → `landing_view` and `"/@:handle"` → `public_profile_view` have no session guard. The router outlet renders either view whether or not a session exists.
- **Frontend API client** (`app.rs`): `AppContext::client()` returns an unauthenticated `ChirpClient` when `session.get()` is `None`. The landing and profile views call API methods through this client without requiring a session.
- **API client** (`api.rs`): `public_timeline()` calls `GET /chirps`; `user_chirps(username)` calls `GET /users/{username}/chirps`. Both methods accept `&ChirpClient` with no session dependency.
- **Server tests** (`tests/api.rs`): `mod public_timeline` has a `requires_no_auth` test confirming the endpoint returns 200 without an `Authorization` header.

### AC-2 — Useful Empty State (Welcome + Sign-Up/Sign-In CTA)
**STATUS: MET**

On first arrival with no content, visitors see a clear welcome message and obvious sign-up/sign-in paths — never a blank page.

Evidence:
- **`landing.rs` `empty_view()`**: Renders an `h2` "Welcome to Chirp" headline, a description paragraph ("Chirp is a place to share short thoughts and follow people you find interesting."), and two explicit CTA links — "Create an account" (→ `/signup`) and "Sign in" (→ `/signin`).
- **State trigger** (`view_tree()`): `model.loaded && model.chirps.is_empty()` → `empty_view()`. This state fires when the API returns a successful empty page, ensuring a welcoming experience rather than a blank screen.
- **Unit test**: `empty_model_renders_welcome_statement_and_cta_links` — asserts the welcome text and both CTA links are present in the rendered tree.

### AC-3 — Recoverable Error State
**STATUS: MET**

If the timeline fails to load, a clear, actionable error message is shown with a path to recovery — not a broken or blank screen.

Evidence:
- **`landing.rs` `view_tree()`**: When `!model.loaded && model.error.is_some()` → renders an `error_banner` containing the error message and a "Retry" button. Clicking "Retry" re-dispatches the initial fetch.
- **Load-more error** (secondary state): When `model.loaded && model.error.is_some()` (failure during pagination) → chirp list remains visible; inline "Try again" button is shown below the last loaded chirp. The loaded data is preserved; only the incremental load failed.
- **Unit tests**: `initial_error_renders_error_message_and_retry_button` asserts the error message and Retry button are present. `loaded_with_load_more_error_renders_inline_retry` covers the secondary case.
- **`/sign-in` alias route** (`app.rs`, added in `decb6196`): The commit message references "AC-3" but this alias is primarily a navigation robustness fix — it ensures links to `/sign-in` (without hyphen variant) land correctly on the sign-in view rather than the fallback/error screen.

### AC-4 — "Create an Account" CTA Visible on Landing and Sign-In Screen
**STATUS: MET**

The "create an account" call-to-action is visible on the landing page, on the sign-in screen, and following it leads to sign-up.

Evidence:
- **Persistent `nav_bar()` in `app.rs`**: Rendered above the router outlet on every page. Contains "Create account" link (→ `/signup`) and "Sign in" link (→ `/signin`), visible in every state including landing, public profile, and sign-in.
- **`header_nav()` in `landing.rs`**: An additional sign-up/sign-in nav rendered within the landing view itself, in every landing state (loading, empty, loaded, error, end-of-list). Unit test `every_state_includes_header_nav_links` asserts both links are present across all 5 states.
- **Sign-in view** (`sign_in.rs`): Renders "New to Chirp? Create an account" anchor (→ `/signup`) and "Back to home" link (→ `/`). The CTA is contextually visible exactly when a visitor is on the sign-in screen.
- **Sign-up route** (`app.rs`): `"/signup"` → `signup_view`. The sign-up view renders "Create an account" heading with a form placeholder, confirming the route reaches sign-up.
- **Route completeness**: Both `/signin` and `/sign-in` routes are wired to `sign_in_view`, preventing broken navigation regardless of which URL form is used.

### AC-5 — Distinct Loading, Empty, Error, and End-of-List States
**STATUS: MET**

The logged-out landing/timeline implements all required states distinctly and accurately, with no state ambiguity.

Evidence:
- **`LandingModel` state machine** (`landing.rs`): Five+ non-overlapping states controlled by `{ loaded, chirps, has_more, error, loading_more }`. The `view_tree()` function branches cleanly:
  1. **Loading**: `!loaded && no error` → `loading_view()` renders "Loading…" with class `chirp-loading`
  2. **Initial error**: `!loaded && error.is_some()` → error banner + "Retry" button  
  3. **Empty**: `loaded && chirps.is_empty()` → `empty_view()` (welcome + CTAs)
  4. **Loaded (has more)**: `loaded && !chirps.is_empty() && has_more` → chirp list + "Load more" button
  5. **End-of-list**: `loaded && !chirps.is_empty() && !has_more` → chirp list + "You're all caught up."
  6. **Load-more error**: `loaded && !chirps.is_empty() && error.is_some()` → chirp list + inline error + "Try again"
  7. **Loading more**: `loaded && !chirps.is_empty() && loading_more` → chirp list + "Loading more…"
- **One-state-model criterion**: The state fields are designed so only one primary state is active per render. The `view_tree()` conditional structure is a clean if/else-if chain with no overlapping branches for the primary states.
- **Unit tests** (`landing.rs`): 11 tests covering all states:
  - `unloaded_model_renders_loading_state`
  - `empty_model_renders_welcome_statement_and_cta_links`
  - `loaded_model_renders_chirp_list_and_load_more_button`
  - `last_page_renders_end_note_not_load_more`
  - `initial_error_renders_error_message_and_retry_button`
  - `every_state_includes_header_nav_links`
  - (plus 5 additional tests for pagination, load-more, model transitions)
- **Public profile view** (`public_profile.rs`): 6 distinct states (Loading, NotFound, Empty, Loaded, EndOfList, Error) with 13 unit tests — consistent pattern across both public-facing views.

---

## Summary

The implementation at `decb6196c2c1e6ed421d393a642f0c844cc333ba` satisfies all 5 acceptance criteria of issue #35. The branch is CI-green, PR #263 is clean and mergeable. No code changes were needed during this evaluation — the work completed in prior DAGs is functionally complete and meets the bar.

**Recommendation**: Merge PR #263 into `main`.
