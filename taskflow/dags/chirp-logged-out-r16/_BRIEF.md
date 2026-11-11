# _BRIEF.md — chirp-logged-out-r16 (swe-coder)

## Objective

Complete issue #35 — **Logged-out reading and a useful landing with accurate states** — for the `Nousix-LLC/nswe-demo` repository. This DAG must verify all five acceptance criteria (AC-1 through AC-5) against the current branch state, complete any gaps, and **produce a root `SYNTHESIS.md` as its final act** accounting for each AC (met, or not and why).

This is the 16th attempt on this goal. r13, r14, and r15 all stalled without producing SYNTHESIS.md. **Producing SYNTHESIS.md is the hard requirement and the terminal act of this DAG.**

## Repository

`Nousix-LLC/nswe-demo`

## Branch

`work/chirp-logged-out` — current HEAD `21dca556301a58c5ae286509a797a6c202225c71`

**Do NOT force-push this branch.** Build on the existing state; commits should be additive only.

## PR

PR #263 already exists: OPEN/MERGEABLE on `work/chirp-logged-out`. Head `21dca556`. CI run 42173990246: 6/6 ALL PASS. Do not create a new PR; update the existing one if needed.

## CI status

CI run 42173990246 for `21dca556`: 6/6 ALL PASS (all checks green including the image build). No CI blocker.

## What is already on the branch

r10 pushed the core backend and frontend code (backend REST APIs at `/api/timeline/public`, `/api/users/:username/public`, `/api/health`; frontend routes for public timeline and public user profiles using SSR with ferric).

r12 pushed AC-4: the sign-up call-to-action form on the landing page (commit `21dca556`).

**AC-4 is already pushed.** Do not re-implement it.

## Issue #35 acceptance criteria

Verify each of the following against the live branch (`work/chirp-logged-out`) and complete any that are not yet met:

- **AC-1**: A logged-out visitor can browse a public timeline of chirps at `/timeline` (or the root `/`) without being redirected to a login page. The route renders the public chirp feed.
- **AC-2**: A logged-out visitor can view a public user profile at `/users/:username` showing that user's chirps and profile info without being redirected.
- **AC-3**: The landing page (root `/` when no session) shows an accurate landing state — it does not show a logged-in dashboard or an error; it shows a welcoming/informative landing.
- **AC-4**: The landing page includes a sign-up call-to-action form or button. (**Already pushed at `21dca556`.**)
- **AC-5**: Navigation between the public pages (timeline, user profile, landing) works correctly without authentication errors or broken links.

## Scope

- Repository: `Nousix-LLC/nswe-demo`
- Branch: `work/chirp-logged-out` (additive commits only, no force-push)
- Crates in scope: `crates/chirp-frontend`, `crates/chirp-server`, `crates/chirp-types` (as needed)
- Out of scope: authenticated user features, any other issue, any other branch

## Declared output

1. Commits on `work/chirp-logged-out` (zero or more — if the branch is already complete, no new commits needed)
2. PR #263 updated if commits are added
3. **Root `SYNTHESIS.md`** at the DAG root (i.e., `taskflow/dags/chirp-logged-out-r16/SYNTHESIS.md`) — **REQUIRED as the DAG's final act**. The SYNTHESIS.md must:
   - State an overall verdict: `PASS` or `FAIL`
   - Account for each AC (AC-1 through AC-5): met or not met, and why
   - Reference specific commits or file paths for each met AC
   - List any blockers if verdict is FAIL

## Concerns to evaluate

1. **AC completeness**: Which of AC-1 through AC-5 are met by the current branch state? Inspect the actual code, routes, and handlers in `crates/chirp-frontend` and `crates/chirp-server`.
2. **Route accessibility**: Are the public routes accessible to logged-out visitors? Check server-side auth guards, middleware, and SSR rendering paths.
3. **Landing page state accuracy**: Does the root `/` correctly detect the absence of a session and render the logged-out landing state (AC-3)?
4. **Sign-up form/button presence** (AC-4): Confirm the sign-up CTA is present and functional in the frontend code (already on branch at `21dca556`).
5. **Navigation correctness** (AC-5): Verify links and navigation between public pages are correct and do not require authentication.
6. **CI green**: Ensure any new commits keep CI green (all 6 checks passing). The existing state is CI green.

## Constraints

- No force-push to `work/chirp-logged-out`
- Do not close or replace PR #263; update it if commits are added
- Do not touch other branches or other issues
- The root `SYNTHESIS.md` MUST be produced — this is the DAG's terminal deliverable

## Notes on prior stall history

r13, r14, and r15 each received a correctly scoped brief but stalled without producing `SYNTHESIS.md`. The branch code is in place. The likely gap is evaluation and synthesis: the DAG must actually read the code, check each AC, and write the SYNTHESIS.md verdict. If additional code changes are needed to meet an AC, make them. If all ACs are met, the SYNTHESIS.md should say so (PASS). Do not stall after the code work is done — write SYNTHESIS.md immediately as the final act.
