# CTA link concern

## Concern: CTA link correctness — link("/compose", "Log in →")

## Checked

**compose.rs `render_signup()`** at commit `decb6196`:

`crates/chirp-frontend/src/compose.rs`, line 519:
```rust
.child(link("/compose", "Log in →")),
```

This line is in the trailing hint paragraph of `render_signup()`, which is the view rendered at
`/signup`. It produces a "Log in →" anchor that navigates to `/compose`.

**app.rs route table** at commit `decb6196`:

- Line 146: `.route("/signin", move |_params| sign_in_view(&signin_ctx))` — dedicated sign-in view
- Line 147: `.route("/sign-in", move |_params| sign_in_view(&signin_hyphen_ctx))` — alias
- Line 148: `.route("/signup", move |_params| signup_view(&signup_ctx))` — sign-up view (source)
- Line 150: `.route("/compose", move |_params| compose_view(&compose_ctx))` — compose view (target)

`/compose` routes to `compose_view`. When a logged-out visitor reaches `compose_view`, it renders
`render_login` (a handle-entry login form) rather than the dedicated `sign_in_view`. Both paths
allow login, but they are distinct views bound to distinct routes. The dedicated sign-in view at
`/signin` exists specifically to serve the "I already have an account" journey.

## Verdict

fail

## Finding or Clean Item

**Location**: `crates/chirp-frontend/src/compose.rs`, line 519, commit `decb6196`

**Principle**: A CTA should route to the view whose purpose matches the user's stated intent.
The intent of "Log in →" on the sign-up page is to reach the sign-in flow, not the compose flow.

**Rationale**: A user on the sign-up page who clicks "Already have an account? Log in →" expects
to reach the sign-in page. The app has a dedicated `/signin` route (`sign_in_view`) for exactly
this purpose. The link sends them to `/compose` instead, which routes to `compose_view`. While
`compose_view` incidentally shows a login form when the session is absent, the destination is
semantically and structurally wrong:

1. The URL the user lands on reads `/compose`, not `/signin` — the wrong context for a login
   journey originating from sign-up.
2. `sign_in_view` and `compose_view`'s login form are separate implementations; any post-login
   redirect logic or UX differences in `sign_in_view` are bypassed.
3. The route table shows the developer established `/signin` and `/sign-in` as the canonical
   sign-in destinations; routing a "Log in" CTA to `/compose` contradicts that decision.

**Severity**: blocker

This is a routing correctness defect in a user-facing feature introduced by this PR. The sign-up
→ log-in navigation is a primary user journey. Shipping with the wrong target route would send
users to the compose view when they intend to sign in, and would bypass whatever behavior
`sign_in_view` provides that `compose_view` does not.

**Resolution**: Change the link target from `/compose` to `/signin`:

```rust
// compose.rs line 519 — render_signup()
// Before:
.child(link("/compose", "Log in →"))
// After:
.child(link("/signin", "Log in →"))
```
