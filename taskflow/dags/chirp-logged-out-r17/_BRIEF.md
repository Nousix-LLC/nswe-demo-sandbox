# _BRIEF.md — chirp-logged-out-r17

## Objective

Verify and complete the logged-out visitor experience for `Nousix-LLC/nswe-demo` (issue #35), and produce `SYNTHESIS.md` as the final act of this DAG. This is the 17th attempt to bring this goal to completion; r10–r16 all stalled or failed to produce `SYNTHESIS.md`.

**Branch**: `work/chirp-logged-out`  
**Current head**: `21dca556301a58c5ae286509a797a6c202225c71`  
**CI**: Run 42173990246 — 6/6 ALL PASS on head `21dca556`  
**PR**: #263 (`feat: logged-out public timeline and user profiles (#35)`) — OPEN/MERGEABLE  

## Issue #35 — Acceptance Criteria

AC-1: Logged-out visitors can browse the public timeline at `/` or `/timeline` without authentication.  
AC-2: Logged-out visitors can view public user profiles at `/u/:username`.  
AC-3: The landing page and navigation accurately reflect the logged-out state (no authenticated-user UI shown to anonymous visitors).  
AC-4: A sign-up call-to-action is present and visible for logged-out visitors on the landing/timeline pages.  
AC-5: All existing authenticated user flows remain unbroken (no regressions on logged-in paths).

## Code already on the branch (do not force-push)

- `eaf96cf` (r10): backend APIs — public timeline endpoint, public user profile endpoint (chirp-server)
- `e02b1d8a` (r10): frontend routes — public timeline and profile pages wired in (chirp-frontend)
- `fed1fc8e` (r11): fix(chirp-frontend) — corrections from prior review pass
- `21dca556` (r12): AC-4 sign-up form added to landing/timeline pages (chirp-frontend)

The branch has feature-complete code for AC-1–AC-4 and AC-5 (regressions). CI is 6/6 ALL PASS.

## What to evaluate

1. **Verify AC-1–AC-5 against the code on the branch**: confirm each criterion is met by what is committed. Read the relevant source files, the route table, the server endpoints, and the frontend components.
2. **Identify and complete any gaps**: if any criterion is not met, make the minimal changes needed. No force-push on `work/chirp-logged-out`; new commits only.
3. **Verify CI remains green**: if new commits are pushed, confirm CI passes (or note clearly if a push was needed but CI cannot be verified within the DAG).
4. **Produce `SYNTHESIS.md`**: this is the DAG's mandatory final act — a root `SYNTHESIS.md` at the top of this DAG's workspace, with a PASS or FAIL verdict and an account of each AC (met, or not and why). The DAG MUST NOT terminate without producing `SYNTHESIS.md`.

## Root cause pattern (from r13–r16 stalls)

DAGs r13 through r16 were dispatched and stalled without producing `SYNTHESIS.md`. The branch has had no new commits since `21dca556` (r12). The pattern is: the DAG is dispatched, it may evaluate the branch, but it terminates without synthesizing. r17 MUST synthesize. Producing `SYNTHESIS.md` is not optional and is not deferred — it is the DAG's terminal act.

## Declared output

- Root `SYNTHESIS.md` at `taskflow/dags/chirp-logged-out-r17/SYNTHESIS.md` — PASS or FAIL verdict, accounting for each AC.
- If any code gaps were found and fixed: new commits on `work/chirp-logged-out` (no force-push).
- PR #263 remains open and updated.

## Constraints

- Repo: `Nousix-LLC/nswe-demo`
- Branch: `work/chirp-logged-out` — no force-push
- Do not modify or close PR #263
- Do not close issue #35 (the overseer does that on landing)
- Scope: issue #35 (AC-1–AC-5) only
