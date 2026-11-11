# _GLOBAL.md — chirp-logged-out-r6 subtree hub

**Goal**: Implement the logged-out visitor experience for Chirp — public timeline, public user
profiles, and an accurate landing with loading/empty/error/end-of-list states (issue #35).

## Discovery findings

The full implementation was produced by an earlier sibling attempt and landed on
`work/chirp-logged-out`. PR #263 (`feat: logged-out public timeline and user profiles (#35)`)
is OPEN and MERGEABLE; all six CI checks (fmt, clippy, test, wasm, doc, image) show
COMPLETED SUCCESS. Branch is 12 commits ahead of `main` at `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`.

The implementation covers:
- `GET /api/chirps` — public, unauthenticated timeline endpoint (20-item paginated)
- `GET /api/users/:username/chirps` — public user chirps endpoint
- `chirp-frontend` landing route (`/`) with loading, empty, error, end-of-list, paginated states
- Public user profile view at `/@:handle` with its own full state set
- Sign-up form at `/signup` and sign-in stub at `/signin`
- Persistent nav bar with "Create account" and "Sign in" links on every page
- 30+ frontend unit/component tests; server integration tests for public endpoints

## Subtree shape

One child task: `SUBTASK_synthesis` — verify each AC against the actual implementation and
produce the root `SYNTHESIS.md` at the observation seam.

## Observation seam

`taskflow/dags/chirp-logged-out-r6/SYNTHESIS.md`
