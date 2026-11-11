# _BRIEF.md — chirp-logged-out-r15 (swe-coder DAG)

## Objective

Complete the logged-out visitor experience for the Chirp app — issue #35: "Logged-out reading and a useful landing with accurate states". The branch `work/chirp-logged-out` has prior code from r9–r12; your job is to verify that every acceptance criterion is fully met in the current code, complete any gaps, and produce a root `SYNTHESIS.md` accounting for each criterion.

This is a continuation run. Prior rounds (r9 through r14) pushed real code that is on the branch. The PR is already open. **r14 stalled without producing SYNTHESIS.md** (four consecutive overseer checks with head unchanged — stall confirmed I360). r13 stalled before it. Your task is to evaluate the current code against the acceptance criteria, complete what remains, and close out with SYNTHESIS.md.

**Repository**: `Nousix-LLC/nswe-demo`
**Branch**: `work/chirp-logged-out` (current HEAD: `21dca556301a58c5ae286509a797a6c202225c71`)
**PR**: #263 (OPEN/MERGEABLE) — "feat: logged-out public timeline and user profiles (#35)"
**CI**: Run 42173990246 for `21dca556` — 6/6 ALL PASS (all checks green including image build)

## Issue #35 — Acceptance Criteria

The following criteria must all be satisfied:

**AC-1**: A logged-out visitor can view the public timeline at `/` — displays a list of recent chirps from all users (requires backend `GET /api/chirps` and frontend rendering).

**AC-2**: A logged-out visitor can view a public user profile page (e.g. `/users/alice`) — displays that user's chirps (requires backend `GET /api/users/:username/chirps` and frontend UserProfile component).

**AC-3**: A logged-out visitor is shown a sign-in prompt/page at `/sign-in` — a useful landing with a form to sign in.

**AC-4**: A logged-out visitor can reach a sign-up form at `/signup` — form to create an account. (r12 commit `21dca556`: "feat(chirp-frontend): implement sign-up form at /signup route (AC-4)" — verify this is complete.)

**AC-5**: The UI accurately reflects logged-in vs logged-out states — a logged-out visitor does not see authenticated-only controls (e.g. compose box, "my feed"), and the navigation and landing states are correct for a visitor.

## What prior rounds implemented

- **r9** (`2615ba1d`): Fixed WASM compilation blockers; CI went green.
- **r10** (`e02b1d8a`): Backend APIs (`GET /api/chirps`, `GET /api/users/:username/chirps`) + frontend routes (landing page, public profile, sign-in, sign-up with placeholder states). CI 6/6 ALL PASS.
- **r11** (`fed1fc8e`): `fix(chirp-frontend)` — a frontend fix commit. CI green.
- **r12** (`21dca556`): AC-4 sign-up form at `/signup` route. CI 6/6 ALL PASS.
- **r13**: Stalled without producing SYNTHESIS.md (confirmed I356 — 4/4 stall checks, head unchanged at `21dca556`).
- **r14**: Stalled without producing SYNTHESIS.md (confirmed I360 — 4/4 stall checks, head unchanged at `21dca556`).

The branch has real, working code. The critical gap has been **producing SYNTHESIS.md** — both r13 and r14 failed to do so.

## What to do

1. **Inspect the current branch code** against each acceptance criterion (AC-1 through AC-5). Check the backend routes, the frontend route registrations, the component implementations, and the authenticated-vs-logged-out state handling.

2. **Identify and fix any gaps**: If a criterion is not fully met in the current code, implement the missing piece. Use the existing patterns and conventions in the codebase. All work goes on branch `work/chirp-logged-out`.

3. **Run the full CI suite**: the CI is 6/6 ALL PASS on `21dca556`; any new commits must keep it green. Do not break existing passing tests.

4. **Produce `SYNTHESIS.md`** at the DAG root (`taskflow/dags/chirp-logged-out-r15/SYNTHESIS.md`) accounting for each of AC-1 through AC-5:
   - For each criterion: MET or NOT MET and why.
   - Overall verdict: PASS (all criteria met, CI green, PR mergeable) or FAIL (blockers remain with details).

## Critical constraint: SYNTHESIS.md is the primary deliverable

**Two consecutive runs (r13 and r14) stalled without producing SYNTHESIS.md.** This is the main failure mode. The DAG MUST produce `taskflow/dags/chirp-logged-out-r15/SYNTHESIS.md` as its final act, before returning. Do not stall: evaluate the code thoroughly, implement any needed fixes, and produce SYNTHESIS.md. Even if all five criteria are already met by the existing code, the SYNTHESIS.md documenting that must be written.

## Declared output

- Commits on `work/chirp-logged-out` closing any remaining gaps (may be zero new commits if everything is already done).
- PR #263 kept open and MERGEABLE (do not close or force-push; push only additional fix commits if needed).
- `taskflow/dags/chirp-logged-out-r15/SYNTHESIS.md` with the verdict and criterion-by-criterion accounting.

## Constraints

- Repo: `Nousix-LLC/nswe-demo` only.
- Branch: `work/chirp-logged-out` only. No force-push.
- Do not close PR #263 or push to main.
- Keep CI green: 6/6 checks must pass on the final HEAD.
- **SYNTHESIS.md MUST be produced** — this is the primary deliverable this run is here to complete. r13 and r14 both failed to produce it. Do not stall: evaluate thoroughly and produce SYNTHESIS.md before returning.
- No scope expansion beyond issue #35 and its five acceptance criteria.
