# Synthesis — chirp-logged-out-r6

**Branch**: `work/chirp-logged-out`  
**PR**: https://github.com/Nousix-LLC/nswe-demo/pull/263  
**PR title**: `feat: logged-out public timeline and user profiles (#35)`  
**CI status at assessment time**: All six checks passed — `fmt`, `clippy`, `test`, `wasm`, `doc`, `image` — all COMPLETED SUCCESS.  
**Verdict**: All five acceptance criteria are **met**.

---

## AC-1 — Logged-out visitor can read the public timeline and user profiles without signing in

**Met.**

The public API endpoints carry no authentication requirement:

- `GET /api/chirps` → `handlers::public_chirps` (`crates/chirp-server/src/api/handlers.rs`): the handler signature takes only `State(state)` and `Query(query)` — no `AuthUser` extractor. The module doc explicitly notes "no bearer-token requirement" for this endpoint and its unit tests call it directly without any session token.
- `GET /api/users/{username}/chirps` → `handlers::user_chirps` (`crates/chirp-server/src/api/handlers.rs`): same pattern — `State`, `Path(username)`, `Query`. No `AuthUser` extractor. The handler table in the module doc confirms: auth = no.
- The router (`crates/chirp-server/src/api/router.rs`) applies no auth middleware to either route.

The frontend routes `/` → `landing_view` and `/@:handle` → `public_profile_view` are registered in `crates/chirp-frontend/src/app.rs` without any auth guard — `AppContext` carries a `Signal<Option<Session>>` but neither view checks it before rendering.

`public_profile.rs` module doc: "Accepts a `:handle` route parameter, fetches `GET /api/users/:username/chirps`, and renders six distinct states: loading, not-found (HTTP 404), empty (user exists, no chirps), loaded (user and chirps), end-of-list (last page displayed), and error (recoverable failure)."

---

## AC-2 — Empty state shows what Chirp is and a path to sign up or sign in; never a blank page

**Met.**

`crates/chirp-frontend/src/landing.rs`, `empty_view()` function:

```rust
fn empty_view() -> VNode {
    VElement::new("div")
        .attr("class", "chirp-landing-empty")
        .child(VElement::new("h2").child(text("Welcome to Chirp")))
        .child(
            VElement::new("p")
                .attr("class", "chirp-landing-description")
                .child(text(
                    "Chirp is a place to share short thoughts and follow people you find interesting.",
                )),
        )
        .child(
            VElement::new("div")
                .attr("class", "chirp-landing-cta")
                .child(link("/signup", "Create an account"))
                .child(text(" · "))
                .child(link("/signin", "Sign in")),
        )
        .into()
}
```

The module doc confirms: "The empty state explains what Chirp is and offers prominent sign-up and sign-in entry points so logged-out visitors have a path into the authenticated flow." The `view_tree()` function branches to `empty_view()` only when `model.loaded && model.chirps.is_empty()` — there is no code path that produces a blank render. The test `empty_model_renders_welcome_statement_and_cta_links` asserts the welcome copy and both CTA links are present in the rendered tree.

---

## AC-3 — Timeline load failure shows a clear, recoverable message

**Met.**

`crates/chirp-frontend/src/landing.rs`, `view_tree()`:

```rust
let body: VNode = if !model.loaded {
    match &model.error {
        None => loading_view(),
        Some(err) => VElement::new("div")
            .attr("class", "chirp-landing-error")
            .child(error_banner(&err.user_message()))
            .child(button("Retry", on_retry))
            .into(),
    }
} // ...
```

`error_banner()` renders `<p class="chirp-error" role="alert">` — the `role="alert"` attribute makes the error visible to screen readers. The "Retry" button invokes `on_retry` → `reload()` → `begin_initial()` + `request_load()`, fully resetting state and re-fetching.

After a successful initial load, pagination errors are handled in `footer()` with an inline error banner and "Try again" button that retriggers the continuation fetch. Neither error path produces a blank or permanently broken screen.

The test `initial_error_renders_error_message_and_retry_button` asserts that an `AppError::Network` applied to an unloaded model renders both an error message and a Retry action.

---

## AC-4 — "Create an account" route is visible on the landing and the sign-in screen; following it reaches sign-up

**Met.**

Three independent rendering paths guarantee the link's presence:

**On every page via persistent nav** (`crates/chirp-frontend/src/app.rs`, `nav_bar()`):
```rust
fn nav_bar() -> VNode {
    VElement::new("nav")
        .attr("class", "chirp-nav")
        // ...
        .child(link("/signup", "Create account"))
        // ...
        .child(link("/signin", "Sign in"))
        .into()
}
```
This nav bar is rendered above the reactive outlet on every route, including `/signin`. The function carries an explicit `(AC-4)` reference in its doc comment.

**Directly in the landing view** (`crates/chirp-frontend/src/landing.rs`, `header_nav()`): a second "Create account" link is rendered inside every landing-view state tree with the doc comment "Persistent sign-up / sign-in links shown in every landing-view state (AC-4)".

**Explicitly on the sign-in screen** (`crates/chirp-frontend/src/sign_in.rs`, `sign_in_view()`):
```rust
VElement::new("p")
    .attr("class", "chirp-signin-links")
    .child(text("New to Chirp? "))
    .child(link("/signup", "Create an account"))
    // ...
```

The `/signup` route is registered in `app.rs` as `"/signup" → sign_up_view`, so following any of these links reaches the sign-up view.

---

## AC-5 — Loading, empty, error, and end-of-list states are each visually distinct; no blank or stale views

**Met.**

`crates/chirp-frontend/src/landing.rs` `view_tree()` implements an exhaustive state machine over `LandingModel`:

| Condition | Rendered element | CSS class |
|---|---|---|
| `!loaded && no error` | `<p>Loading…</p>` | `chirp-loading` |
| `!loaded && error` | error banner + Retry button | `chirp-landing-error` |
| `loaded && chirps.is_empty()` | Welcome / what-is-Chirp copy + CTAs | `chirp-landing-empty` |
| `loaded && !chirps.is_empty()` | chirp list + footer below | `chirp-landing-loaded` |
| — footer: pagination error | inline error + "Try again" | `chirp-load-more-error` |
| — footer: `loading_more` | "Loading more…" | `chirp-loading-more` |
| — footer: `has_more` | "Load more" button | _(button)_ |
| — footer: end of list | "You're all caught up." | `chirp-end` |

Each branch is a distinct `VNode` tree with a distinct CSS class. No branch produces an empty element or falls through to a default. Tests exercise every branch: `unloaded_model_renders_loading_state`, `loaded_model_renders_chirp_list_and_load_more_button`, `last_page_renders_end_note_not_load_more`, and `initial_error_renders_error_message_and_retry_button`.

`public_profile.rs` applies the same pattern across six distinct states (loading, not-found, empty, loaded, end-of-list, error) for the user-profile route.

---

## Residual concerns

**Sign-in form is a placeholder.** `sign_in.rs` renders a form with the submit button marked `disabled` and labelled "Sign in (coming soon)". The route is reachable, the "Create an account" link on it is live, and the view's own doc explicitly scopes this out: "The actual authentication flow is out of scope for the public-timeline feature; this view exists so the sign-in route is reachable." This does not affect any of the five ACs — issue #35 concerns the logged-out read experience, not authentication. The placeholder will need to be replaced before a full sign-in flow ships.

**`before` cursor type deviation.** The `GET /api/chirps` endpoint accepts `before` as a millisecond timestamp (integer) while the original spec describes it as an ISO 8601 string. The handlers.rs doc comment explicitly acknowledges this: "noted as a spec deviation." The frontend produces and consumes millisecond timestamps consistently, so the round-trip works. If a third-party client needs to conform to the ISO 8601 spec, an adapter would be required.

---

*Assessment produced against branch `work/chirp-logged-out` at commit `fed1fc8e187d2e706c0aa5d8a6a1f65fb5e92411`.*
