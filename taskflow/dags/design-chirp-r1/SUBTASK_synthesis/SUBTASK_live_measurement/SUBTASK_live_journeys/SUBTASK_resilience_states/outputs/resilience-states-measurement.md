# Resilience & feedback states — live measurement (`manual_user_check`)

**Cluster**: `SUBTASK_resilience_states` — empty / loading / failed / not-found states, onboarding,
session-expiry recovery, and action feedback.
**Owned criteria (12)**: BAR-026, BAR-027, BAR-028, BAR-029, BAR-226, BAR-240, BAR-248, BAR-259,
BAR-260, BAR-261, BAR-262, BAR-263.

## Access note

Measured against the deployed chirp product at `Nousix-LLC/nswe-demo` commit `c805525`. The running
product was reachable and was exercised read-only through a single throwaway account (registered,
logged in, posted one chirp; no other mutation). The shipped UI is a client-side WebAssembly bundle
whose rendered states cannot be captured outside a browser here, so for what each state actually
renders the authoritative artifact is the SPA/API source at `c805525` — `crates/chirp-frontend`
(the three route views plus the shared error type), `crates/chirp-server`, and `crates/chirp-types`
— read alongside the live API's observed responses, which were exercised directly. Where a verdict
rests on UI rendering, it is grounded in the source at the stated repo-relative path; where it rests
on server behaviour, it is grounded in an observed live API response.

The product at `c805525` is a three-route walking skeleton: the route table
(`crates/chirp-frontend/src/app.rs`) defines only `/` (timeline), `/compose` (handle login +
compose), `/user/:id` (profile), and a generic "Not found" fallback; the nav offers only Timeline and
Compose. There is no landing, sign-up, onboarding, settings, notifications, discovery, followers, or
reporting surface. Many criteria below are therefore `missing` because the surface they describe is
absent, not because a present surface failed.

The `design`-domain methodology loader was unavailable for this node (`agent_domain_unset`); recorded,
and measurement proceeded on the principal-product-designer persona and the release-bar statements.

## Verdicts

One row per owned `BAR-*`, keyed by `bar_id`; columns `bar_id, live_status, observation` per the
inherited `verdict_row_schema`. `live_status ∈ {met, partial, missing, not_applicable}`.

| bar_id | live_status | observation |
|--------|-------------|-------------|
| BAR-026 | missing | No landing or "what is chirp" surface exists. The route table (`crates/chirp-frontend/src/app.rs`) has only `/` (timeline), `/compose`, `/user/:id`, and a generic fallback, and the nav is just Timeline · Compose. `GET /api/timeline` requires auth — observed `401 {"code":"UNAUTHORIZED","message":"unauthorized: missing Authorization header"}` with no token — so a visitor with no session opening `/` gets the timeline's full-screen error banner and a Retry button, not an explanation or a path to sign up. There is no sign-up anywhere: the login form (`compose.rs`) calls only `POST /sessions`. |
| BAR-027 | missing | There is no sign-up and no onboarding screen. The only post-auth empty state is the timeline's `empty_view` (`crates/chirp-frontend/src/timeline.rs`), which renders the bare text "No chirps yet." — no guidance explaining the empty state and no actionable route toward a first follow or first chirp. Exercised with a fresh throwaway account, `GET /api/timeline` returned `{"items":[],"nextCursor":null}`, which the SPA renders as that bare line. |
| BAR-028 | partial | Three states exist and none is blank or silent: loading renders "Loading timeline…", the empty list renders "No chirps yet.", and a failed load renders an error banner (`role="alert"`) with a Retry; a failed compose or like/follow shows an inline error at the control with input/state preserved (`timeline.rs`, `compose.rs`, `profile.rs`; a failed like was observed to return `404 NOT_FOUND`, surfaced at the control). But the empty state offers no action to take, and loading is a plain text line rather than a designed placeholder — so "a state the person can understand and act on" is only partly met. |
| BAR-029 | partial | The transient-error half holds: the compose field is uncontrolled and the draft is retained on a failed post, so the person can press Chirp again without retyping (`compose.rs` `submit_chirp` error branch). The session half is missing: the session is held only client-side, a rejected/expired token returns `401 UNAUTHORIZED` (observed), and the view shows it as an inline error banner — it does not clear the session, explain the person's place, or route them to sign-in. |
| BAR-226 | partial | Present: a failed continuation load shows an inline error with "Try again" while already-loaded chirps stay on screen, and failed actions show an inline error at the point of action (`timeline.rs` footer; `compose.rs`/`profile.rs`). Not present: the brand-new empty timeline is the bare "No chirps yet." with no explanatory block or next step, and the first-load state is a "Loading timeline…" text line rather than skeleton rows at the real item size. The error "danger styling" cannot be confirmed — `index.html` ships only minimal inline CSS and defines no treatment for the `chirp-error` class. |
| BAR-240 | partial | Failure states are correct: a failed first page shows a message with Retry and is distinct from the empty state (the model's `loaded` flag separates them), and a failed load-more shows at the list boundary while loaded chirps stay (`timeline.rs`). The nav shell stays visible and the load always resolves (no endless spinner). But the empty state does not explain why the timeline is empty and offers no route to Explore (no Explore surface exists) or to composing a first chirp, and the first-load state is a "Loading timeline…" text line, not skeleton rows at real card size. |
| BAR-248 | missing | No onboarding screen and no sign-up exist; the route table has no onboarding route and no discovery/suggestions surface. After auth, a brand-new account lands on the timeline's bare "No chirps yet." (`timeline.rs`) with no explanation of the empty state and no control that opens compose to write a first chirp (`app.rs`). |
| BAR-259 | partial | Not-found surfaces exist and are safe: a mistyped path renders the SPA fallback "Not found / No route matched this path." (`app.rs`), and an unavailable account at `/user/:id` renders "User not found / No user exists with that id." (`profile.rs`; `GET /api/users/999999` observed `404 NOT_FOUND`, revealing no private detail). But the route back to a known place is only the generic persistent nav (Timeline · Compose), not a contextual affordance; a signed-out visitor has no landing to return to (none exists, and the Timeline link errors without a session); and there is no addressable chirp, so the "deleted chirp" and "in-place tombstone consistency" cases have no surface. |
| BAR-260 | missing | This cross-surface check targets Notifications, the report/block/mute dialogs, the blocked & muted screen, and the followers list — none of which exist in the product (the route table has only timeline, compose, profile). On the one applicable surface, the timeline, the empty state ("No chirps yet.") carries no next step, so the required "explained empty with at least one next step" is not met even there, though the empty and failed treatments are visibly distinct. |
| BAR-261 | partial | Incremental loading is handled well: a "Loading more…" indicator shows at the list boundary while loaded content stays, and a load that cannot resolve stops at an error with Retry rather than spinning forever (`timeline.rs` footer and `apply_error`); the persistent nav frame stays visible during a first load. But the first-load state is a plain text line ("Loading timeline…", and "Loading {id}…" on a profile), not skeletons sized to the real content (`timeline.rs` `loading_view`, `profile.rs` `loading_view`). |
| BAR-262 | partial | Largely present for the surfaces that exist: compose and login show inline, plain-language validation and API errors at the field with the typed input preserved (uncontrolled fields; `compose.rs`), and like/follow are non-optimistic (counts move only on success, so a failed action never shows a result that did not happen), with the server's plain message shown at the control (confirmed: a failed like returned `404 NOT_FOUND` whose human message is displayed, not the code field). Two gaps: the "taken handle at sign-up" example has no surface (no sign-up exists), and a non-decodable transport failure surfaces an HTTP status and URL in the message ("Something went wrong: HTTP status … for …", `crates/chirp-frontend/src/error.rs`), so a system code can leak on that path. |
| BAR-263 | partial | The transient-server-error half holds: a failed post keeps the drafted text and can be retried in place without re-typing (`compose.rs`). The session-expiry half is missing: an expired session is not routed to sign-in with the reason stated, and the person is not returned to where they were afterward; a rejected token just yields an inline error banner (observed `401 UNAUTHORIZED`), with the session left client-side and uncleared. |

## Summary (non-authoritative; the fold re-derives from the rows)

12 criteria: 0 met · 8 partial (BAR-028, BAR-029, BAR-226, BAR-240, BAR-259, BAR-261, BAR-262,
BAR-263) · 4 missing (BAR-026, BAR-027, BAR-248, BAR-260) · 0 not_applicable. The recurring shortfalls
are the absent first-use surfaces (no landing, sign-up, or onboarding), empty states that state a fact
but offer no next step, loading states rendered as text rather than skeletons sized to real content,
and no detection or routing of an expired session. The error/retry and draft-preservation patterns
that do exist are sound for the surfaces the walking skeleton ships.
