# _BRIEF.md — chirp-logged-out

## Objective

Implement the logged-out visitor experience for Chirp: a public timeline readable without an account, public user profiles reachable from it, and a landing that is useful even when there is no content yet. No authentication must be required to reach these screens.

This covers GitHub issue #35: "Logged-out reading and a useful landing with accurate states."

## Acceptance criteria

All criteria are from issue #35 and the design sources listed below.

- **AC-1 (REQ-PROD-013 / BAR-011):** A logged-out visitor can load the home/public timeline and open a user profile and read chirps without being forced to sign up or sign in first.
- **AC-2 (REQ-PROD-014 / BAR-011):** On arrival with no content, the visitor sees a clear statement of what chirp is plus an obvious way to sign up or sign in — never a blank page or an unexplained error.
- **AC-3 (REQ-PROD-014 / BAR-011):** If the timeline fails to load, a clear, recoverable message is shown instead of a broken screen.
- **AC-4 (REQ-PROD-015 / BAR-011):** A "create an account" route is visible on the landing and on the sign-in screen, and following it reaches sign-up.
- **AC-5 (REQ-UX-002 / REQ-UX-030–032 / BAR-011 / one-state-model criterion):** The logged-out landing/timeline renders its loading, empty, error, and end-of-list states accurately and distinctly — each state is a visually distinct screen, never a blank page or a stale view.

## What it builds on

**Ferric framework** (landed, `main` at `62febf5faf6023b3492365d246c7ac39c9f659a3`):
- Reactive signals, component model, DOM rendering, router (PR #203 merged — `Nousix-LLC/nswe-demo`, `crates/ferric`)
- Async resources and form/event binding (PR #193 open — `work/ferric-async-forms-r2`; the signed-in forms are on that branch; the public timeline does not require them, but `create_resource` for the fetch is in ferric on main if already landed; use whatever is on `main` at the branch point)
- SSR render_to_string + client-side hydration + Axum integration (PR #228 merged — `crates/ferric/src/ssr.rs`, `crates/ferric/src/hydrate.rs`)

**Chirp server** (`crates/chirp-server`): Axum REST API + persistence + static SPA serving. Durable persistence is complete (epic #56, PRs #182/#183 merged). Check whether a public chirps/timeline endpoint exists and whether it requires authentication; if no public endpoint exists, one is needed.

**Design documents** (all in `design/` on `main`):
- `design/product-requirements.md` — §3 User journeys; §4 REQ-PROD-013, REQ-PROD-014, REQ-PROD-015
- `design/experience-design.md` — §1 Information architecture & interaction; §2 Screens, flows & states; §6 REQ-UX-002, REQ-UX-030, REQ-UX-031, REQ-UX-032
- `design/release-bar.md` — §C BAR-011

## Scope

- **In scope:** Public timeline API endpoint (unauthenticated GET), public user profile API endpoint (unauthenticated GET if not present), chirp-frontend home/landing route showing the public timeline with accurate states, public user profile view, visible sign-up and sign-in navigation from the landing.
- **Out of scope:** Authenticated features (posting, following, notifications). Do not add authentication where it did not exist; do not remove it where it did. The ferric async-forms epic (#130 / PR #193) adds richer event handling; the public timeline does not require that PR to be merged — build on what is on `main`.

## Constraints

- Repository: `Nousix-LLC/nswe-demo`
- Branch: `work/chirp-logged-out` (create from `main` at `62febf5faf6023b3492365d246c7ac39c9f659a3`)
- One PR into `main` closing issue #35 with `Closes #35` as plain text in the description
- No force-push to `main`
- Written for the repository's readers: no host paths, no internal addresses, no taskflow references in anything committed or posted to GitHub

## Declared output

- Commits on `work/chirp-logged-out`
- One PR into `main` with `Closes #35` in the plain-text description body
- Root `SYNTHESIS.md` accounting for each acceptance criterion (met, or not met and why)
- CI must pass: `fmt`, `clippy`, `test`, `wasm`, `doc`, `image` checks

## Concerns to evaluate

1. **API surface:** Does chirp-server expose unauthenticated GET endpoints for the public timeline and public user profiles? If not, what minimal surface is needed? Are existing authenticated endpoints reusable with an optional auth check, or does a new route family make more sense?
2. **Frontend routing and states:** Does the router (ferric) support a public home route? Are the loading, empty, error, and end-of-list states modelled distinctly in the component, or would a single "not loaded" fallback collapse them? Each must be visually distinct per AC-5.
3. **Landing content:** When no chirps exist yet, what does the visitor see? The design requires a clear "what chirp is" statement and a sign-up/sign-in route — verify these are present and not hidden behind a loading state.
4. **Sign-up / sign-in navigation:** Is there a visible "create an account" link from the landing? Does it reach a sign-up flow? (Partial sign-up flows are in scope if the design has them; this AC covers the navigation being present and reachable.)
5. **SSR integration:** The SSR+hydration foundation is in place. Consider whether the public timeline benefits from server-side rendering for initial page load; if used, the hydration path must correctly adopt the SSR-rendered DOM.
6. **Test coverage:** Unit and integration tests for the new API endpoints; wasm-bindgen-test or component tests for the frontend states. Each distinct loading/empty/error/end-of-list state needs at least one test.
