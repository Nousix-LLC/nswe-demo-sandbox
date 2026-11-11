# _BRIEF.md — SUBTASK_frontend

## Objective

On branch `work/chirp-logged-out` (created by SUBTASK_server), implement all frontend
changes for the logged-out visitor experience: wire the timeline view to the new public
endpoint, give logged-out visitors accurate loading/empty/error/end-of-list states, link
chirp author names to profile pages, and add visible Sign up and Sign in navigation to
every screen — satisfying all AC-1 through AC-5 from GitHub issue #35 on the frontend side.

## Context

**Repository:** `Nousix-LLC/nswe-demo`  
**Branch:** `work/chirp-logged-out` (already created by SUBTASK_server; check it out)  
**Codebase root:** `crates/chirp-frontend/`

**Current state of `chirp-frontend`:**

`src/api.rs` — `ApiClient` with `timeline(&self, query: &TimelineQuery)` calling
`GET /timeline` (authenticated endpoint). Need: add `pub_timeline` calling
`GET /public/timeline`.

`src/timeline.rs` — `timeline_view` calls `ctx.client().timeline(&query)` (hits 401 for
logged-out visitors). `empty_view()` returns "No chirps yet." (blank, no context). `chirp_item`
shows `chirp.author_id.to_string()` as plain text (not a link). The existing state machine
(loading, error, loaded, end-of-list, load-more) is correct structurally — do not replace it,
extend/fix it.

`src/app.rs` — `nav_bar()` renders "Timeline" and "Compose" links only. No Sign up or Sign in.
Router: `/` → `timeline_view`, `/compose` → `compose_view`, `/user/:id` → `profile_view`.
`AppContext { session: Signal<Option<Session>> }`. When session is `None` (logged out),
currently only "Timeline · Compose" appears. `AppContext::client()` returns an `ApiClient` with
`token: None` for logged-out visitors.

`src/profile.rs` — already handles logged-out state correctly (shows "Log in to follow" etc.).
`GET /api/users/{id}` is already unauthenticated. No changes needed here.

**New server endpoint (from SUBTASK_server):**  
`GET /api/public/timeline` — unauthenticated, returns `Page<Chirp>`, query params
`limit?: u32`, `cursor?: Cursor` (same `TimelineQuery` shape).

## Declared outputs

- Commits on `work/chirp-logged-out` containing all frontend changes
- Timeline view loads public chirps without authentication
- Distinct loading / empty / error / end-of-list states visible and accurate
- Chirp author names are clickable links to `/user/{author_id}`
- Sign up and Sign in links visible in the nav on every screen

## Scope (this task only)

**In scope — exactly these changes to exactly these files:**

**`crates/chirp-frontend/src/api.rs`:**
1. Add `pub async fn pub_timeline(&self, query: &TimelineQuery) -> Result<Page<Chirp>, AppError>` to `ApiClient` — calls `GET /public/timeline` with the same query param serialization as the existing `timeline` method (no Authorization header; `self.token` is ignored for this call)

**`crates/chirp-frontend/src/timeline.rs`:**
2. Update `timeline_view` (and the effect that kicks off loading) to call `ctx.client().pub_timeline(&query)` instead of `ctx.client().timeline(&query)` for the initial page and load-more calls
3. Update `empty_view()`: replace "No chirps yet." with a statement of what Chirp is (e.g., "Chirp is a place to share short thoughts and follow people you find interesting.") plus two visible controls — a "Create account" link (to `/compose` or the current sign-up entry point) and a "Sign in" link (to `/compose` or the sign-in entry point)
4. Update `chirp_item(chirp: &Chirp)`: the author display (`chirp.author_id.to_string()`) must become an anchor/link to `/user/{author_id}` — use the router's link mechanism (the same pattern `profile_view` uses internally, or a plain `<a href="/user/{id}">` using the Ferric DOM builder)

**`crates/chirp-frontend/src/app.rs`:**
5. Update `nav_bar()`: add "Sign up" and "Sign in" links — show them when `session` is `None` (logged out); they may be hidden or replaced when `session` is `Some` (logged in). The simplest approach: render "Sign up" and "Sign in" links at all times or conditionally based on `session.get()`. Sign up and Sign in currently both route to `/compose` (the compose view is the entry point for both in the current app) unless a dedicated route exists — use whatever the current routing supports.

**Out of scope:** No server changes; no changes to `src/profile.rs`; no changes to routing structure; no SSR changes; no new crate dependencies (use what `chirp-frontend` already has).

## Success criteria

- Timeline view calls `GET /api/public/timeline` (not `GET /api/timeline`) when the user is logged out
- Loading state shown before first page loads (spinner, placeholder, or "Loading…" text)
- Empty state: "what Chirp is" statement + visible Sign up and Sign in controls — not a blank page
- Error state: a plain recoverable error message (not a blank page) if the timeline fails to load
- End-of-list state: visible "No more chirps" / end indicator (already in model — verify it renders)
- Chirp author display is a link to `/user/{author_id}`
- Sign up and Sign in are visible in the nav bar when logged out
- `cargo build --target wasm32-unknown-unknown` for `chirp-frontend` succeeds (the `wasm` CI check)
- `cargo fmt --check` passes
- `cargo clippy -- -D warnings` passes
- All changes committed on `work/chirp-logged-out` with commit message attribution

## Constraints (inherited from parent hub)

- **Security**: Do not put any host address, SSH key path, username, or host path into any committed file or PR comment
- **API contract**: Call `GET /public/timeline` exactly as defined in `../../contracts/_MANIFEST.yaml`. Do not change the authenticated `GET /timeline` call path elsewhere in the codebase
- **Ferric reactive model**: Use `spawn_local` for async, `bump()` for reactive updates, thread-local MODEL/RERENDER pattern. The existing timeline state machine structure must be preserved — extend it, do not replace it
- **No auth changes**: Do not modify authentication state management or add/remove session logic beyond showing/hiding nav links based on existing `session` signal
- **Git**: Check out `work/chirp-logged-out` (already created by SUBTASK_server). Commit message ends with:
  ```
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
  ```

## Suggested Methodology Files

Domain mapping row matched: **"Rust ↔ WebAssembly / browser bindings"** → primary bundle `Rust`,
supporting bundle `Framework Design`. Also: **"Writing new Rust code"** → `Rust`, `Core`.

**Primary:**
- `rust/Rust_WebAssembly_Browser_Methodology.md` — WASM-specific patterns: `spawn_local`, `wasm-bindgen`, `web-sys`, DOM manipulation from Rust. Directly applicable to the Ferric reactive frontend model.
- `rust/Rust_Error_Handling_Methodology.md` — Error types in an async WASM context; mapping `AppError` to displayed error strings. Required for the error state rendering.

**Supporting:**
- `core/BestPractices_Coding_Standards_Methodology.md` — Consistency with existing `timeline.rs` patterns when extending the state machine.
- `core/CodeManagement_Commit_Practices_Methodology.md` — Commit message format and attribution.

The above are the parent's flagged methodologies based on the task type. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.

## Out-of-Scope Methodologies

- `rust/Rust_Web_Services_Axum_Methodology.md` — server-side Axum is SUBTASK_server's concern
- `rust/Rust_Trait_Design_Methodology.md` — no new trait changes in this task
- `Synthesis` bundle — synthesis is a separate child task
