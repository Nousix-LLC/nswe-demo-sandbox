# _BRIEF.md — chirp-logged-out-r12 (swe-coder)

**Repo**: Nousix-LLC/nswe-demo
**Branch**: `work/chirp-logged-out`
**Current HEAD**: `fed1fc8e187d2e706c0aa5d8a6a1f65fb5e92411`
**CI status**: ALL 6/6 PASS — run 42171295267 (clippy/doc/fmt/image/test/wasm all PASS)
**PR**: #263 OPEN/MERGEABLE — `feat: logged-out reading and accurate landing states (#35)`

## Objective

Verify and complete the logged-out visitor experience for the Chirp app (issue #35), and produce a root-level
`SYNTHESIS.md` verdict. This is a continuation run from the same feature-complete branch state.

## Background

r10 pushed feature-complete code onto `work/chirp-logged-out`:
- **Backend** (eaf96cf): `GET /api/chirps` (public chirp timeline) and `GET /api/users/:username/chirps`
  (per-user public chirps) — both implemented in `crates/chirp-server`.
- **Frontend** (e02b1d8a): `landing`, `public_profile`, `sign_in`, and `sign_up` routes with logged-out states
  — implemented in `crates/chirp-frontend` using the ferric framework.
- **Fix** (fed1fc8e): `fix(chirp-frontend)` commit on top — correcting frontend issues in the logged-out state.

r11 (the previous DAG) stalled after pushing fed1fc8e: 4 consecutive checks showed no new commits and no
SYNTHESIS.md. All CI checks passed on the last known HEAD. r12 (this DAG) is a fresh attempt from the same
HEAD.

Prior stall comments on issue #35:
- r10→r11 stall: https://github.com/Nousix-LLC/nswe-demo/issues/35#issuecomment-6677962335
- r11→r12 stall: https://github.com/Nousix-LLC/nswe-demo/issues/35#issuecomment-6678431704

## Issue #35 — Acceptance Criteria

**AC-1**: A visitor not logged in can visit `/` (the landing/public timeline) and see recent chirps with
author names and timestamps, without being redirected to sign-in.

**AC-2**: A visitor not logged in can visit `/users/:username` (a public profile page) and see that user's
chirps, without being redirected to sign-in.

**AC-3**: The landing page `/` shows a clear call-to-action for signing up or signing in when the visitor is
not authenticated.

**AC-4**: The sign-in page (`/sign_in`) and sign-up page (`/sign_up`) display accurate states — no phantom
"logged in" state, no broken UI for first-time visitors.

**AC-5**: The backend routes serve the data correctly: `GET /api/chirps` returns recent public chirps and
`GET /api/users/:username/chirps` returns that user's chirps, both without authentication required.

## Scope

- **In scope**: Verifying AC-1–AC-5 against the code on `work/chirp-logged-out` at HEAD `fed1fc8e`.
  Identifying and fixing any remaining gaps (compilation errors, panics, missing route registrations, broken
  API calls, incorrect UI state logic) needed to satisfy the acceptance criteria. All work stays on branch
  `work/chirp-logged-out`; do not force-push.
- **Out of scope**: Authenticated user features (posting chirps, following, sessions). Design changes to
  the feature set or acceptance criteria. Changes to `main` or other branches.

## Declared output

- Commits on `work/chirp-logged-out` (if any gaps need fixing — if the code is already complete, no new
  commits are needed).
- A root-level `SYNTHESIS.md` at `taskflow/dags/chirp-logged-out-r12/SYNTHESIS.md` with:
  - Overall verdict: `PASS` or `FAIL`.
  - Verdict for each acceptance criterion (AC-1 through AC-5): met or not, with evidence.
  - If FAIL: specific blockers remaining (what failed, why, what would be needed to fix).

## Constraints

- Repository: `Nousix-LLC/nswe-demo` only.
- Branch: `work/chirp-logged-out`. No force-push.
- Do not open a new PR (PR #263 already exists on this branch).
- Do not touch `main` or any other branch.
- CI must pass on any new commits (or is already passing if no new commits are pushed).
