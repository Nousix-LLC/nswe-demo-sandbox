# _BRIEF.md — chirp-logged-out-r25 (swe-coder DAG)

**Repo**: Nousix-LLC/nswe-demo
**Branch**: `work/chirp-logged-out`
**PR**: #263 (OPEN, MERGEABLE, CI-green — ALL 6 PASS on `decb6196`)

---

## Objective

Complete issue #35 — "Logged-out reading and a useful landing with accurate states" — on branch
`work/chirp-logged-out`. PR #263 is OPEN and CI-green (ALL 6 checks PASS on commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`).

---

## ⚠️ FIRST PRIORITY — ASSESS BEFORE ANY CODE CHANGES

**Before writing a single line of code, assess the current state of `work/chirp-logged-out` at
`decb6196c2c1e6ed421d393a642f0c844cc333ba` against all 5 acceptance criteria below.**

If all 5 ACs are met at `decb6196`, write `SYNTHESIS.md` IMMEDIATELY with a PASS verdict. Do NOT proceed
to any code changes before writing it.

This is the defining pattern across r1–r24: code work was done (the head advanced at r18, r23), but
SYNTHESIS.md was never written. CI is ALL 6 PASS. If the ACs are met, write SYNTHESIS.md and stop.

The root `SYNTHESIS.md` at `taskflow/dags/chirp-logged-out-r25/SYNTHESIS.md` is the declared output.
Write it whether the ACs pass or fail.

---

## Acceptance Criteria

All 5 must be met for a PASS verdict:

1. **Logged-out public access** (`REQ-PROD-013`, `BAR-011`): A logged-out visitor can load the home/public
   timeline and open a user profile and read chirps without being forced to sign up or sign in first.

2. **Useful empty/landing state** (`REQ-PROD-014`, `BAR-011`): On arrival with no content, the visitor sees
   a clear statement of what Chirp is plus an obvious way to sign up or sign in — never a blank page or an
   unexplained error.

3. **Timeline error handling** (`REQ-PROD-014`, `BAR-011`): If the timeline fails to load, a clear,
   recoverable message is shown instead of a broken screen.

4. **Sign-up route visible** (`REQ-PROD-015`, `BAR-011`): A "create an account" route is visible on the
   landing and on the sign-in screen, and following it reaches sign-up.

5. **Accurate UI states** (`REQ-UX-002/030/031/032`, `BAR-011`): The logged-out landing/timeline exercises
   its loading, empty, error, and end-of-list states accurately and distinctly.

---

## Inputs

- Repository: `Nousix-LLC/nswe-demo`
- Branch: `work/chirp-logged-out` at `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- PR: #263 (OPEN, MERGEABLE, CI-green — ALL 6 PASS: fmt, clippy, test, wasm, doc, image)
- Design references (in repo):
  - `design/product-requirements.md` — §3 User journeys; §4 `REQ-PROD-013`, `REQ-PROD-014`, `REQ-PROD-015`
  - `design/experience-design.md` — §1 Information architecture & interaction; §2 Screens, flows & states;
    §6 `REQ-UX-002`, `REQ-UX-030`, `REQ-UX-031`, `REQ-UX-032`
  - `design/release-bar.md` — §C `BAR-011`
- Epic: EPIC-CORELOOP (#34) — Core product loop & accurate UX states
- Dependencies: Durable persistence (#56) DONE. ferric-ssr (#223/#224/#226) DONE. ferric-async-forms
  (#130/#143/#144/#145) DONE.

---

## Stall History (r1–r24 — all produced `_BRIEF.md` and `_FORK.md` only, never `SYNTHESIS.md`)

This DAG (r25) is dispatched because all prior runs stalled without writing SYNTHESIS.md:

- r1–r12: stalled at various heads
- r13–r17: stalled at `21dca556` (4/4 each)
- r18: advanced from `21dca556` to `617f2539`, then stalled (4/4)
- r19–r22: stalled at `617f2539` (4/4 each)
- r23: advanced from `617f2539` to `decb6196`, then stalled (4/4)
- r24: dispatched, stalled at `decb6196` (4/4, confirmed)

The consistent stall pattern is: code is committed, but SYNTHESIS.md is never written. The fix is simple:
**write SYNTHESIS.md**. Assessment comes first; code changes only if ACs are not yet met.

---

## Declared Output

1. **Root `taskflow/dags/chirp-logged-out-r25/SYNTHESIS.md`** — mandatory, always written; carries:
   - Verdict: PASS or FAIL
   - Accounting for each of the 5 acceptance criteria (met / not met, with evidence)

2. **If ACs are already met at `decb6196`**: SYNTHESIS.md with PASS verdict, no code changes needed.

3. **If code changes are needed**: commits on `work/chirp-logged-out` and PR #263 updated (no force-push),
   then SYNTHESIS.md with the verdict after the fix.

---

## Constraints

- Branch: `work/chirp-logged-out` only
- No force-push
- Repo scope: `Nousix-LLC/nswe-demo`
- PR #263 is the target PR — do not open a new PR
- CI is ALL 6 PASS on `decb6196` — confirm the ACs in the existing code first before any changes
- Do not rewrite any merged history
