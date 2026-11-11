# _BRIEF.md — Spoke: AC-1 Public Access and Auth Boundaries

## Objective

Review the access-control and authentication boundaries introduced in PR #263 against AC-1 of
issue #35, and check that removing auth guards on the new public endpoints does not create auth
bypass paths for authenticated endpoints or regress the authenticated home timeline.

**AC-1**: A logged-out visitor can load the home/public timeline and open a user profile without
being forced to sign up or sign in first.

## Inputs

- PR #263 diff: `Nousix-LLC/nswe-demo`, head `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Global context: `taskflow/dags/review-chirp-logged-out-r1/_GLOBAL.md`
- Primary code areas:
  - `crates/chirp-server/src/api/router.rs` — route registration for new public endpoints
  - `crates/chirp-server/src/api/handlers.rs` — `public_chirps`, `user_chirps`, `public_timeline`
    handlers (no `AuthUser` extractor)
  - `crates/chirp-frontend/src/api.rs` — `pub_timeline()` vs `public_timeline()` client methods
  - `crates/chirp-frontend/src/app.rs` — route table (absence of auth gate on `/` and `/@:handle`)
  - `crates/chirp-frontend/src/timeline.rs` — switched from `ctx.client().timeline()` to
    `ctx.client().pub_timeline()`; this may route the authenticated home timeline through the
    public global feed instead of the per-user following feed
  - `crates/chirp-server/tests/api.rs` — integration tests in `mod public_timeline`
  - `crates/chirp-server/src/api/handlers.rs` — unit tests including
    `public_timeline_requires_no_auth`

## Declared output

A `REVIEW.md` at `taskflow/dags/review-chirp-logged-out-r1/spoke-access-auth/REVIEW.md`
containing:

- Verdict for this concern: PASS or FINDINGS
- For each finding: location (file + line at the pinned commit), what principle is at stake, why
  it matters, severity (blocker / non-blocking), and what would satisfy it
- An account of what each sub-concern checked and found clean (or the absence of findings is not
  meaningful without saying what was examined)

## Success criteria

- Every public endpoint (`GET /api/chirps`, `GET /api/users/{username}/chirps`,
  `GET /api/public/timeline`) is confirmed to have no auth extractor and returns 200 to
  unauthenticated requests
- Authenticated endpoints (`POST /api/chirps`, `GET /api/timeline`, `POST /api/sessions`,
  etc.) are confirmed to still require and enforce auth
- The timeline regression question is answered: does the `timeline.rs` change route
  authenticated users through the public global feed instead of the per-user home following feed,
  and if so is that a defect?
- Any auth bypass surface introduced by the route changes is identified

## Constraints

- Repository: `Nousix-LLC/nswe-demo` only
- Do not post to the PR; that is the synthesis child's responsibility
- Findings point at repository file paths and lines; do not name host paths, private IPs, or
  internal infrastructure details
