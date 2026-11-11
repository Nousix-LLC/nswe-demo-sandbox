# Frontend Logged-Out Experience — Summary

## Status

Implementation was **already complete** on `work/chirp-logged-out` prior to this task
executing. The branch commits `e02b1d8` ("feat(frontend): public timeline, user profile,
sign-in/sign-up routes"), `fed1fc8` ("fix(chirp-frontend): align public API structs with
backend wire format"), and `21dca55` ("feat(chirp-frontend): implement sign-up form at
/signup route (AC-4)") carry the full frontend deliverable. This task verified correctness,
ran CI, and documents the as-built contract.

Branch HEAD: `21dca55`

---

## Routes Added / Modified

| Path | Handler | Auth Required | Module | Notes |
|------|---------|:---:|--------|-------|
| `/` | `landing::landing_view` | No | `landing.rs` | Public timeline; 4 distinct states (AC-1, AC-2, AC-3, AC-5) |
| `/@:handle` | `public_profile::public_profile_view` | No | `public_profile.rs` | Public user profile + chirps; 6 states (AC-1) |
| `/signin` | `sign_in::sign_in_view` | No | `sign_in.rs` | Sign-in entry stub; navigation target for AC-4 |
| `/signup` | `compose::signup_view` | No | `compose.rs` | Full account-creation form with `POST /users` + auto-login (AC-4) |

The existing authenticated routes (`/compose`, `/user/:id`, `/timeline`) are unchanged.
The persistent `nav_bar()` in `app.rs` renders "Create account" (→ `/signup`) and
"Sign in" (→ `/signin`) links on every page (AC-4).

---

## Components Created

### `landing.rs` — Public Home / Timeline

**Purpose**: The `/` route for logged-out visitors. Fetches `GET /api/chirps` and renders
the public chirp timeline with four distinct, visually non-blank states.

| State | Trigger | CSS class | Visible content |
|-------|---------|-----------|-----------------|
| **Loading** | Initial page load; before first response | `chirp-loading` | "Loading…" spinner text |
| **Empty** | First page loads with zero chirps | `chirp-landing-empty` | Welcome statement ("Welcome to Chirp — a place for short thoughts") + "Create an account" (→ `/signup`) + "Sign in" (→ `/signin`) CTA links |
| **Error** | First fetch fails (network or API error) | `chirp-landing-error` | Error banner with `role="alert"` + "Retry" button |
| **Loaded** | First page loads with ≥1 chirps | `chirp-list` | Chirp list + footer |

Footer sub-states (within **Loaded**):
- `has_more=true`: "Load more" button
- `loading_more=true`: "Loading more…" text (button disabled)
- `has_more=false`: "You're all caught up." end-of-list note

The `header_nav()` fragment renders sign-in / sign-up links within the landing view itself
(in addition to the global `nav_bar()`), satisfying AC-4's "visible from landing" requirement.

**State model**: `LandingModel` in `thread_local!` storage. Reducer methods
`begin_initial`, `apply_initial`, `begin_more`, `apply_more`, `apply_error`. Re-render
gated by route guard `current_path().as_str() != "/"` to prevent stale updates after
navigation.

---

### `public_profile.rs` — Public User Profile

**Purpose**: The `/@:handle` route. Fetches `GET /api/users/:username/chirps` and renders
the user's public profile with six distinct states.

| State | Trigger | CSS class |
|-------|---------|-----------|
| **Loading** | Route entered; before first response | `chirp-profile chirp-profile-loading` |
| **Not Found** | First fetch → HTTP 404 | `chirp-profile chirp-profile-not-found` |
| **Error** | First fetch fails (non-404) | `chirp-profile chirp-profile-error` |
| **Loaded (empty)** | User exists, zero chirps | `chirp-profile` + "No chirps yet." paragraph |
| **Loaded (with chirps)** | User exists, chirps present | `chirp-profile` + `chirp-list` + footer |
| **End-of-list** | Loaded, `has_more=false` | Footer: "No more chirps." paragraph |

The model resets fully when the route handle changes, so navigating from `/@alice` to
`/@bob` starts a fresh fetch rather than showing stale alice data.

---

### `compose.rs::signup_view` — Account Creation (`/signup`)

**Purpose**: The active `/signup` route handler. Renders a functional account-creation
form (handle + display name fields). On submit, calls `POST /api/users` to create the
account then `POST /api/sessions` to auto-log the new user in. On success, writes the
`Session` into `ctx.session` (the reactive anchor), which re-renders every dependent view
to show the logged-in state.

This is a full functional form, not a stub. The separate `sign_up.rs` module (declared in
`lib.rs`) is a simpler placeholder stub retained for forward-compatibility; it is not
wired to the router.

---

### `sign_in.rs` — Sign-In Stub (`/signin`)

**Purpose**: Makes `/signin` a reachable route so logged-out visitors who click "Sign in"
in the nav do not reach a 404. The form renders username/password inputs with
`disabled=""` submit button. Full authentication (credential validation + `POST /sessions`)
is pending a future authentication feature sprint.

---

## State Machine Summary

```
Landing:
  entry → begin_initial() → spawn_local fetch GET /api/chirps
    → apply_initial(resp) → loaded=true; bump()
    → apply_error(err)    → error; bump()
  "Load more" click → begin_more() + spawn_local fetch GET /api/chirps?before=…
    → apply_more(resp)    → chirps appended; bump()
  "Retry" click → begin_initial() + spawn_local fetch (reset all state)

Public profile:
  route entry (new handle) → reset_for(handle) + request_load(Initial)
    → apply_initial(resp) → phase=Loaded; bump()
    → apply_error(404)    → phase=NotFound; bump()
    → apply_error(other)  → phase=Error(_); bump()
  "Load more" → begin_more() + request_load(More)
    → apply_more(resp)    → chirps extended; bump()
    → apply_error(err)    → continuation_error set (phase stays Loaded)
  "Retry" → reload() = reset_for + request_load(Initial)
  navigate away → guard in bump() (starts_with("/@")) drops stale responses
```

---

## Test Coverage

All tests are native Rust unit tests (`#[cfg(test)]`). They test the pure view-tree and
state-reduction functions in isolation — no DOM, no browser runtime required. The CI
`wasm` job validates that the crate and its `examples/chirp.rs` entry compile cleanly to
`wasm32-unknown-unknown`, exercising the full wasm code path.

### chirp-frontend total: 76 unit tests, 0 failures

| Module | Tests | States / scenarios covered |
|--------|-------|---------------------------|
| `landing.rs` | 11 | Loading state, empty state (welcome + CTA links), error state (retry), loaded state (chirp list + load-more), end-of-list (no load-more), header nav always present, state transitions (apply_initial, apply_more, apply_error, begin_initial) |
| `public_profile.rs` | 11 | Loading, not-found (404→NotFound phase), server error (Error phase), empty-loaded (no chirp-list), loaded-with-chirps (chirp-list + load-more), end-of-list (no load-more), state transitions (reset_for, apply_initial, apply_more, apply_error × Initial/More) |
| `sign_up.rs` | 3 | Renders correct class, links to sign-in, links back to home |
| `compose.rs` | 14 | Handle/chirp/signup validation, submit enablement, error messages |
| `api.rs` | 12 | Client construction, path building, query param building, error mapping |
| other crates | ~315 | chirp-server (27), chirp-types (96), ferric/* (various) |

### Per-distinct-state coverage (AC-5 requirement)

| Required state | Test(s) | Module |
|---------------|---------|--------|
| Loading | `unloaded_model_renders_loading_state` | `landing` |
| Empty (welcome + CTA) | `empty_model_renders_welcome_statement_and_cta_links` | `landing` |
| Error (recoverable) | `initial_error_renders_error_message_and_retry_button` | `landing` |
| End-of-list | `last_page_renders_end_note_not_load_more` | `landing` |

The `public_profile.rs` module additionally tests distinct loading / not-found / error /
end-of-list states for the user profile view.

---

## CI Results (run on `work/chirp-logged-out` HEAD `21dca55`)

| Check | Command | Result |
|-------|---------|--------|
| `fmt` | `cargo fmt --all --check` | ✓ pass |
| `clippy` | `cargo clippy --workspace --all-targets --locked -- -D warnings` | ✓ pass |
| `test` | `cargo test --workspace --locked` | ✓ pass — 76 chirp-frontend tests, 0 failures |
| `wasm (build)` | `cargo build -p chirp-frontend --target wasm32-unknown-unknown --locked` | ✓ pass |
| `wasm (example)` | `cargo build -p chirp-frontend --example chirp --target wasm32-unknown-unknown --locked` | ✓ pass |
| `doc` | `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps --locked` | ✓ pass |

---

## SSR Strategy

**Hydration path** (in `app.rs`):
```rust
#[cfg(target_arch = "wasm32")]
if root.has_child_nodes() {
    ferric::hydrate(root, app);
} else {
    mount(root, app);
}
```

The app adopts SSR markup when present (Axum SSR integration) and falls back to a fresh
client-side mount when the root is empty. For the current deployment (client-only SPA),
the root starts empty and `mount()` runs. If a future server-side render of the landing
pre-populates `#app`, the WASM bundle will hydrate it without a flicker.

The public timeline views (`landing.rs`, `public_profile.rs`) issue their data fetches
via `wasm_bindgen_futures::spawn_local`, which is client-side only. SSR pre-rendering of
the initial timeline chirps would require a separate Axum SSR handler calling
`ferric::render_to_string`; that is out of scope for this feature.

---

## Deviations from Analysis Document

| # | Deviation | Explanation |
|---|-----------|-------------|
| 1 | `thread_local!` state pattern instead of `AsyncResource` | The analysis suggested using Ferric's `AsyncResource` for the public timeline. The actual implementation uses the same `thread_local! { MODEL, RERENDER, STARTED }` pattern used by `timeline.rs`. This gives explicit control over the 4 distinct required states (loading/empty/error/end-of-list) and the pagination reducer, which `AsyncResource` does not natively expose as separate phases. |
| 2 | `compose::signup_view` is the active `/signup` handler; `sign_up.rs` is an unused stub | The analysis proposed a simple sign-up stub at `/signup`. The actual implementation routes `/signup` to the full functional `compose::signup_view` (account creation + auto-login), while `sign_up.rs` was added as a simpler placeholder module retained for forward-compatibility but not wired to the router. |
| 3 | `created_at` is `i64` (ms since epoch) not ISO 8601 | Consistent with the backend's `Timestamp` type and the backend_summary.md documented deviation. The frontend `api.rs` types (`PublicChirp.created_at`, `PublicUserChirp.created_at`) match the wire format exactly. |
| 4 | Public profile route is `/@:handle` not `/user/:username` | The analysis proposed a path; the implemented path is `/@:handle` (Twitter-style `@username` prefix), which the router extracts as `params.get("handle")`. The unauthenticated `/user/:id` route remains for the authenticated profile view. |
