owner_id: proc-1c6ca4d1-635c-4d0b-a52b-ee8be52d3350
observation_seam: taskflow/dags/chirp-logged-out-r9/SYNTHESIS.md
launch_agent: swe-coder
thread_type: dag
disposition: retain
reap: whole-after-land
launch_context:
  application: software

# _FORK.md — chirp-logged-out-r9 (swe-coder)

**Goal**: Implement the logged-out visitor experience for the Chirp application (issue #35), fixing the
existing CI blocker and ensuring all tests pass.

**Repo**: Nousix-LLC/nswe-demo  
**Branch**: `work/chirp-logged-out` (existing — push to this branch)  
**PR**: #263 "feat: logged-out reading and accurate landing states (#35)" (already open — do not create a new PR)

## Context

This is the 9th attempt (r9) to implement issue #35. The previous DAG (r8) opened PR #263 on `work/chirp-logged-out`
but stalled without completing its synthesis. The PR is open and functional commits exist on the branch,
but CI is blocked by one wasm build failure.

Previous stall history: r1 (6 checks), r2 (4 checks), r3 (4 checks), r4 (4 checks), r5 (4 checks),
r6 (4 checks), r7 (4 checks), r8 (4 checks — stall confirmed, this r9 dispatched).

## Objective

Implement the logged-out visitor experience for Chirp:

1. **Public timeline** — a visitor who is not logged in can browse the public chirp timeline at the root URL
   without being redirected to login.
2. **Public user profiles** — a visitor can browse individual user profile pages (e.g. `/u/:username`) without
   being authenticated.
3. **Accurate landing states** — the app's landing page and routing must correctly detect authentication state
   and route accordingly:
   - Authenticated users → their feed or home view
   - Unauthenticated visitors → the public timeline / landing view (not a login redirect)
4. **No regression** — all existing authenticated flows (login, posting, following, feeds) continue to work
   correctly.

## Acceptance criteria

- All CI checks pass: `test`, `clippy`, `fmt`, `doc`, `wasm`, `image` — all green.
- All 42 frontend unit tests, 59 server unit tests, and 26 integration tests continue to pass.
- PR #263 has the final commits pushed to `work/chirp-logged-out`.
- A visitor can load the root URL without authentication and see a public timeline.
- Authenticated routing is accurate (no false redirects for logged-in users, no access leaks for logged-out users).

## CI blocker to fix first

The wasm build is currently failing. This must be fixed before any other work is considered complete.

**Root cause**: Non-exhaustive match on `EventKind` in `crates/ferric/src/vdom.rs` around line 463.
New variants were added (DblClick, MouseDown, MouseUp, MouseEnter, MouseLeave, and approximately 43 more)
that are not covered by the existing match arms.

**Fix**: Add a catch-all `_ => todo!()` arm to the match, or handle all new variants explicitly. Either
approach will make the wasm build succeed. Confirm the fix compiles and that `wasm` CI passes.

## Scope

- **In scope**: `crates/chirp-frontend` (routing, page components, auth-state detection),
  `crates/chirp-server` (any public route handlers needed), `crates/ferric/src/vdom.rs` (the wasm blocker).
- **Out of scope**: changes to other ferric internals beyond the EventKind match fix, changes to the
  authentication flow itself (login/logout/session management), changes to `deploy/` or CI configuration.

## Branch and PR instructions

- Push all commits to `work/chirp-logged-out`.
- Do not create a new PR — PR #263 tracks this branch and will update automatically.
- After pushing, verify that CI re-triggers and all checks turn green.

## Declared output

`SYNTHESIS.md` in this DAG's workspace, with:
- Status: PASS or FAIL
- Summary of what was implemented
- CI result (all checks listed)
- Any remaining blockers (if FAIL)
