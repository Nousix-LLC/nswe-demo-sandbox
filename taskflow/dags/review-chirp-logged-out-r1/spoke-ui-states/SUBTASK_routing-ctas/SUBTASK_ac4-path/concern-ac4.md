# AC-4 path concern

## Concern: AC-4 sign-in-to-sign-up path

## Checked

**Step 1 — CTA in sign_in.rs**

`crates/chirp-frontend/src/sign_in.rs` at commit `decb6196`:
- Line 68: `.child(link("/signup", "Create an account"))` — the sign-in view's
  `chirp-signin-links` paragraph links to `/signup` with the label "Create an account".

**Step 2 — Route table resolution in app.rs**

`crates/chirp-frontend/src/app.rs` at commit `decb6196`:
- Line 25: `use crate::compose::{compose_view, signup_view};` — `signup_view` is imported
  from `compose.rs`, not from `sign_up.rs`.
- Line 148: `.route("/signup", move |_params| signup_view(&signup_ctx))` — the `/signup`
  path resolves to `crate::compose::signup_view`, confirmed by the module-doc route table
  at line 14: `/signup` -- `signup_view` (crate::compose::signup_view): full account-creation form.
- Note: `sign_up.rs`'s `sign_up_view` is not imported anywhere in `app.rs` and is not wired
  to any route.

**Step 3 — Destination handler: compose.rs signup_view**

`crates/chirp-frontend/src/compose.rs` at commit `decb6196`:
- Line 627: `pub fn signup_view(ctx: &AppContext) -> VNode` — this is the functional
  account-creation form.
- Line 55: `const SIGNUP_HANDLE_ID: &str = "chirp-signup-handle";` and line 57 (implicit):
  `const SIGNUP_DISPLAY_NAME_ID` — real input fields with stable IDs for DOM reads.
- Line 83: `signup_busy: bool` in `ComposeState` — the form tracks in-flight API requests.
- Line 539: `s.signup_busy = true;` — the submit handler fires a `POST /users` call; this
  is active code, not a stub.

**Step 4 — Confirming sign_up.rs is the placeholder**

`crates/chirp-frontend/src/sign_up.rs` at commit `decb6196`:
- Line 23: `pub fn sign_up_view(_ctx: &AppContext) -> VNode` — a different function name
  (`sign_up_view`, not `signup_view`).
- Lines 61–62: `.attr("disabled", "")` / `.child(text("Create account (coming soon)"))` —
  the submit button is permanently disabled with a "coming soon" label.
- Module doc (lines 1–9): "Renders a placeholder form … intentionally non-functional".
- This module is not imported in `app.rs` and is not reachable via any route.

## Verdict

pass

## Clean Item

The AC-4 sign-in-to-sign-up navigation path is correctly wired.

- Checked: `sign_in.rs:68` — CTA `link("/signup", "Create an account")` targets `/signup`.
- Checked: `app.rs:148` — route `/signup` dispatches to `signup_view` from `compose.rs`.
- Checked: `compose.rs:627` — `signup_view` is a functional form with active state management
  and a live `POST /users` submission path.
- Checked: `sign_up.rs` — the confusably-named placeholder `sign_up_view` (line 23) is not
  in the route table and is not reachable from normal navigation. The disabled "coming soon"
  button (lines 61–62) stays behind this dead path.

A visitor who clicks "Create an account" from the sign-in page reaches the functional
account-creation form, satisfying AC-4.
