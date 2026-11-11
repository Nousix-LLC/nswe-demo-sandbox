# _BRIEF.md — SUBTASK_frontend_logged_out

**Parent:** chirp-logged-out  
**Global hub:** `taskflow/dags/chirp-logged-out/_GLOBAL.md`

## Objective

Update `chirp-frontend` so that logged-out visitors get a fully functional, state-accurate experience: the home route (`/`) loads and displays the public timeline from the now-available `GET /api/public/timeline` endpoint (delivered by `SUBTASK_server_public_timeline`), every timeline state (loading, empty, error, end-of-list) is visually distinct, the empty state explains what Chirp is, and sign-up / sign-in navigation is clearly visible from the landing.

## Background

The backend spoke (`SUBTASK_server_public_timeline`) adds `GET /api/public/timeline` as an unauthenticated endpoint. The frontend currently calls `ctx.client().timeline(..)`, which hits `GET /api/timeline` (requires auth → 401 for logged-out visitors).

`AppContext::client()` returns an `ApiClient` with no token when `session` is `None` (logged out). The `ApiClient` is in `crates/chirp-frontend/src/api.rs`.

The `TimelineModel` in `crates/chirp-frontend/src/timeline.rs` already implements the loading/empty/error/end-of-list state machine — the states are modeled but may not be visually distinct for every case.

`AppContext::session: Signal<Option<Session>>` distinguishes logged-in (`Some`) from logged-out (`None`).

The route table in `src/app.rs` already has `/ → timeline_view` and `/user/:id → profile_view`.

## Scope

Three distinct concerns to address:

**1. Public timeline API call**  
Add `ApiClient::public_timeline(&self, query: &TimelineQuery) -> Result<Page<Chirp>, AppError>` to `crates/chirp-frontend/src/api.rs`. This method calls `GET /public/timeline` (no auth needed). Update the timeline view in `crates/chirp-frontend/src/timeline.rs` to call `public_timeline` when the session is `None` and the existing authenticated `timeline` when the session is `Some`. The `TimelineModel` state machine is already correct; only the fetch call site changes.

**2. All four timeline states visually distinct**  
Verify and ensure that each of the four states the `TimelineModel` can represent is rendered as a visually distinct, non-blank screen:
- **Loading** (`!model.loaded && model.error.is_none()`): a visible loading indicator (spinner or "Loading…" text with appropriate CSS class).
- **Empty** (`model.loaded && model.chirps.is_empty() && model.next_cursor.is_none()`): a landing message explaining what Chirp is, with visible sign-up and sign-in links. Never a blank screen.
- **Error** (`model.error.is_some() && !model.loaded`): clear error message with a "Retry" affordance.
- **End-of-list** (`model.loaded && !model.chirps.is_empty() && model.next_cursor.is_none()`): a "You're all caught up" message after the final chirp. No "Load more" button when there is nothing more.

The CSS class hooks (`chirp-loading`, `chirp-empty`, etc.) already exist in the view skeleton; fill in any missing render branches so every state produces visible DOM content.

**3. Sign-up / sign-in navigation**  
The empty state must include visible links: "Sign in" (to the sign-in view if it exists, or the compose view as placeholder if not) and "Create an account" (to the sign-up / create-user flow). The nav bar or header must also carry a "Sign in" link when the session is `None`. Inspect `src/app.rs` and the existing nav to determine where the session-aware navigation lives; add the logged-out variant there. If a dedicated sign-up route does not exist in the router, the link should navigate to the existing account-creation path that does exist (e.g., the compose view's sign-up affordance, or a `#sign-up` anchor) — do not add a new route unless one is needed to satisfy AC-4.

## Declared outputs

- Commits on branch `work/chirp-logged-out` (this spoke commits on top of `SUBTASK_server_public_timeline`'s commits; pull before committing).
- `crates/chirp-frontend/src/api.rs` — `public_timeline` method added.
- `crates/chirp-frontend/src/timeline.rs` — fetch call updated; all four states visually distinct.
- `crates/chirp-frontend/src/app.rs` (or nav component) — sign-up/sign-in links in nav for logged-out session.
- `COMPLETE.md` in this workspace on completion.

## Success criteria

- A logged-out browser session on `/` loads chirps from `GET /api/public/timeline` (no 401 errors in the network log).
- The empty state shows a "what Chirp is" message and sign-up/sign-in links — not a blank screen.
- The loading state shows a spinner or "Loading…" indicator.
- The error state shows a message and a Retry button.
- The end-of-list state shows a "caught up" message with no "Load more" button.
- `GET /api/users/{id}` still loads user profiles without auth (already works; regression-check only).
- `cargo fmt --check`, `cargo clippy`, `cargo test`, and `cargo build --target wasm32-unknown-unknown` (or the project's wasm CI step) all pass on the branch.

## Constraints

- Repository: `Nousix-LLC/nswe-demo`
- Branch: `work/chirp-logged-out` (pull latest from `SUBTASK_server_public_timeline` before committing)
- Written for the repository's readers: no host paths, no internal addresses, no taskflow references in anything committed or posted to GitHub.
- Do not add authentication to any currently-unauthenticated code path.
- Do not change the authenticated timeline flow (session `Some`) — it must continue to call `GET /api/timeline`.
- Do not add new routes unless strictly required to satisfy AC-4.
