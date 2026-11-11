# _BRIEF.md — chirp-public-landing-r1 (swe-coder)

**Goal**: Implement logged-out reading and a useful landing for the chirp app — issue #35 under epic #34.

**Branch**: `work/chirp-public-landing-r1`
**Integration branch**: `main`
**Repository**: Nousix-LLC/nswe-demo
**PR**: open against `main` closing #35

---

## Objective

A logged-out visitor can read the public chirp timeline and open user profiles without signing in. The
landing handles its loading, empty, error, and end-of-list states accurately and distinctly. The site never
shows a blank page or an unexplained error to a visitor who has not signed up.

---

## Acceptance Criteria

- A logged-out visitor can load the home/public timeline and open a user profile and read chirps without
  being forced to sign up or sign in first. (`REQ-PROD-013`, `BAR-011`)
- On arrival with no content, the visitor sees a clear statement of what chirp is plus an obvious way
  to sign up or sign in — never a blank page or an unexplained error. (`REQ-PROD-014`, `BAR-011`)
- If the timeline fails to load, a clear, recoverable error message is shown instead of a broken screen.
  (`REQ-PROD-014`, `BAR-011`)
- A "create an account" route is visible on the landing and on the sign-in screen, and following it
  reaches sign-up. (`REQ-PROD-015`, `BAR-011`)
- The logged-out landing/timeline exercises its loading, empty, error, and end-of-list states accurately
  and distinctly. (`REQ-UX-002`, `REQ-UX-030`, `REQ-UX-031`, `REQ-UX-032`, `BAR-011`, one-state-model criterion)

---

## Scope

**In scope:**
- `crates/chirp-frontend/`: add or extend the public timeline view, the logged-out landing screen, loading/
  empty/error/end-of-list state renders, and the sign-up route link.
- Routes and navigation changes in the ferric router as needed to support public (unauthenticated) timeline
  and profile access.
- Backend API endpoints required for the public timeline and public profile reads, in `crates/chirp-server/`
  — if any are missing.

**Out of scope:**
- Authentication, login, or sign-up forms themselves (those are a separate goal).
- BAR-005 / #225 (SSR state carry + async resource resume) — that is a follow-up for the async-forms epic.
- Modifying the ferric framework core (`crates/ferric/`) beyond what is needed to wire the new views.

---

## Inputs

- Issue #35 and its acceptance criteria (above).
- Epic #34 — EPIC-CORELOOP.
- Design documents in the repository:
  - `design/product-requirements.md` — §3 User journeys; §4 `REQ-PROD-013`, `REQ-PROD-014`, `REQ-PROD-015`
  - `design/experience-design.md` — §1 Information architecture & interaction; §2 Screens, flows & states;
    §6 `REQ-UX-002`, `REQ-UX-030`, `REQ-UX-031`, `REQ-UX-032`
  - `design/release-bar.md` — §C `BAR-011`
- Existing codebase: `crates/chirp-frontend/`, `crates/chirp-server/`, `crates/ferric/` on `main`.

---

## Declared Output

- Commits on branch `work/chirp-public-landing-r1` implementing the acceptance criteria above.
- One PR against `main` with:
  - A description written for the repository's readers: outcome, what changed, how it was verified, and
    `Closes #35` as plain text in the description body.
  - CI passing (all checks green) at the head commit.
- Root `SYNTHESIS.md` at this workspace (`taskflow/dags/chirp-public-landing-r1/SYNTHESIS.md`) with:
  - Overall verdict: PASS or FAIL.
  - Per-criterion verdict table covering each acceptance criterion above.
  - Evidence: file paths, function names, test names, and CI run URL.
  - Any remaining gaps or issues that did not reach the bar, with a note on what is left.

---

## Concerns to cover

1. **Route guard / auth check** — ensure no route guard forces redirect-to-login on the public timeline
   or public profile routes. A logged-out visitor must reach them without an auth wall.
2. **Loading state** — the timeline shows a recognisable loading indicator while the fetch is in flight;
   it never shows stale content while loading.
3. **Empty state** — when the timeline has no chirps yet, a friendly empty-state message (what chirp is,
   plus a sign-up/sign-in CTA) is shown, never a blank white page.
4. **Error state** — if the fetch fails, a user-readable error message with a retry affordance is shown.
5. **End-of-list state** — when paginating, reaching the end shows a distinct end-of-list indicator, not
   a repeated load or an ambiguous silence.
6. **Sign-up / sign-in link** — a visible "create an account" link on the landing page and on the sign-in
   screen reaches the sign-up route.
7. **Public profile route** — a logged-out visitor can follow a username link from the timeline and read
   that user's public chirp history without being forced to sign in.
8. **State model compliance** — loading, empty, error, and end-of-list are distinct UI states, never
   collapsed together (e.g., empty-on-error or end-of-list treated as empty).
9. **No regression** — existing authenticated views and routes continue to work; CI stays green across
   fmt, clippy, test, wasm, doc, and image checks.
