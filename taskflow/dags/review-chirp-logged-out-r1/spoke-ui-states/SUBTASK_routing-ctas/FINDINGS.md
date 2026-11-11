# Findings — routing-ctas review

## Concerns checked

- **AC-4 remaining (sign-in-to-sign-up path and usable sign-up)**: The CTA at
  `sign_in.rs:68` correctly targets `/signup`; that route resolves to the functional
  `compose.rs::signup_view`; the placeholder `sign_up.rs::sign_up_view` is not in the
  route table. Path is correctly wired. **Clean.**

- **CTA link correctness (`compose.rs` `link("/compose", "Log in →")`)**: The "Log in →"
  CTA in `render_signup()` at `compose.rs:519` navigates to `/compose` (the compose view)
  rather than to `/signin` (the sign-in view). **One blocker finding.**

- **Route annotation anomaly (`/sign-in` alias `"for AC-3"` comment)**: The module doc
  at `app.rs:13` attributes the `/sign-in` alias to AC-3 (recoverable error messages),
  which has no routing component. The developer cited AC-4 correctly elsewhere; this is
  a likely transposition. No behavioral impact. **One non-blocking finding.**

## Findings

**[F1] Blocker — CTA link routes to compose view instead of sign-in view**

- **Location**: `crates/chirp-frontend/src/compose.rs`, line 519,
  commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle**: A CTA should route to the view whose purpose matches the user's stated
  intent. The intent of "Log in →" on the sign-up page is to reach the sign-in flow,
  not the compose flow.
- **Rationale**: A user on the sign-up page who clicks "Log in →" expects to reach
  `/signin`. The link sends them to `/compose` instead. While `compose_view` shows a
  login form when the session is absent, the destination is semantically wrong: the URL
  reads `/compose`, not `/signin`; any post-login redirect logic or UX behavior specific
  to `sign_in_view` is bypassed; and the route table shows the developer established
  `/signin` and `/sign-in` as the canonical sign-in destinations, making the CTA's target
  contradict that design decision.
- **Severity**: blocker
- **Resolution**: Change `link("/compose", "Log in →")` to `link("/signin", "Log in →")`
  at `compose.rs:519`.

---

**[F2] Non-blocking — Route annotation cites wrong acceptance criterion**

- **Location**: `crates/chirp-frontend/src/app.rs`, line 13,
  commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle**: Code comments must accurately attribute the acceptance criteria they
  satisfy. A comment citing the wrong AC number creates a false traceability link that
  misleads reviewers on re-reads.
- **Rationale**: The module doc comment `(alias for AC-3)` attributes the `/sign-in`
  hyphenated alias to AC-3 (recoverable error messages / Retry / `role="alert"`). AC-3
  has no routing component. The same developer cited `(AC-4)` correctly at line 94 for
  the `nav_bar()` entry points, which makes the wrong AC-3 reference at line 13 a likely
  copy-paste transposition rather than a principled decision. The route registration at
  line 147 is mechanically correct; the error is confined to the doc comment and has no
  runtime effect.
- **Severity**: non-blocking
- **Resolution**: Correct to `(alias for AC-4)` if the hyphenated alias was added to
  satisfy AC-4 sign-in navigation; or replace with `(hyphen-spelling alias)` if no
  specific AC motivated it.

## Clean items

- **Concern**: AC-4 sign-in-to-sign-up path
  - **Checked**: `crates/chirp-frontend/src/sign_in.rs:68` — CTA
    `link("/signup", "Create an account")` targets `/signup`;
    `crates/chirp-frontend/src/app.rs:148` — `/signup` route dispatches to
    `compose.rs::signup_view` (confirmed by the module doc route table at `app.rs:14`);
    `crates/chirp-frontend/src/compose.rs:627` — `signup_view` is a functional form
    with live state management (`ComposeState::signup_busy`) and an active
    `POST /users` submission path; `crates/chirp-frontend/src/sign_up.rs:23` — the
    confusably-named `sign_up_view` stub (disabled button, "coming soon" label,
    module doc "intentionally non-functional") is not imported in `app.rs` and is not
    reachable from any route.
  - **Result**: The sign-in-to-sign-up navigation path is correctly wired. A visitor
    who clicks "Create an account" from the sign-in page reaches the functional
    account-creation form, satisfying AC-4.
