## Concern 6 — sign_up::sign_up_view Dead Code

## Investigation

The `/signup` route is defined in `crates/chirp-frontend/src/app.rs`. The import at the top of that file reads:

```rust
use crate::compose::{compose_view, signup_view};
```

The route binding in `start()` is:

```rust
.route("/signup", move |_params| signup_view(&signup_ctx))
```

The handler on that route is `compose::signup_view`, not `sign_up::sign_up_view`.

`crates/chirp-frontend/src/sign_up.rs` exports a `pub fn sign_up_view` (line 23) that renders a placeholder section with a disabled submit button labeled "Create account (coming soon)". The function is `pub` and the module is re-exported from `lib.rs` as `pub mod sign_up`, so it is part of the crate's surface, but no caller outside its own `#[cfg(test)]` block references it.

`compose::signup_view` (in `crates/chirp-frontend/src/compose.rs`) is the live implementation: it collects a handle and display name, calls `ApiClient::create_user`, auto-logs in on success, and surfaces errors inline. The PR added this function and wired `/signup` to it. `sign_up::sign_up_view` was not removed.

A search through `app.rs`, `lib.rs`, and the PR diff confirms there is no `use crate::sign_up::sign_up_view;` or equivalent anywhere in the codebase.

## Verdict

`sign_up::sign_up_view` is not reachable from any live route. The `/signup` route handler is `compose::signup_view`. `sign_up::sign_up_view` compiles and is tested in its own test module, but it cannot be reached through the application's URL routing.

## Finding

### Finding: sign_up::sign_up_view is an unreachable public export

- **Location**: `crates/chirp-frontend/src/sign_up.rs`, line 23 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle at stake**: Dead exports. A `pub` function that no caller in the crate can reach through any live code path is dead code, regardless of whether it compiles.
- **Why it matters**: Two functions now share the name concept "signup view" but do different things: `compose::signup_view` is the live handler with full registration logic; `sign_up::sign_up_view` is a disabled stub that was the intended home for that logic but was bypassed when the implementation landed in `compose.rs`. The `lib.rs` module-doc for `sign_up` says it is the "/signup -- sign-up entry point", which contradicts the route table. A contributor reading `sign_up.rs` to understand the signup flow will find a stub rather than the live code, and may not discover `compose::signup_view` without reading the route table. The stub's disabled button ("coming soon") is also misleading — registration is live.
- **Severity**: non-blocking
- **Satisfying condition**: Either remove `sign_up::sign_up_view` and its test module (and correct `lib.rs`'s doc for the `sign_up` module to reflect that `/signup` is now handled by `compose::signup_view`), or — if `sign_up.rs` is intentionally kept as the future home of a richer registration form — add a module-level doc note that the current export is not wired to any route and that `compose::signup_view` is the active handler.
