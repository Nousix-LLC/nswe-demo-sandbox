# _BRIEF.md — chirp-logged-out-r19 (swe-coder)

## Objective

Continue from the r18 branch state to complete issue #35 — Logged-out reading and a useful landing with accurate states. The branch `work/chirp-logged-out` is at head `617f25395eebe9475f19a90e0b1dac5921215ea3` (CI all green, PR #263 OPEN/MERGEABLE/CLEAN). r10–r18 made substantial progress: backend APIs, public timeline endpoint, user profile endpoint, frontend routes, sign-up form, and auth-gating work are all present in the existing code.

**The goal for r19**: (a) verify the full AC-1–AC-5 checklist against the live code at head `617f2539`, (b) address any gaps or regressions found, and (c) produce `SYNTHESIS.md` at the DAG root reporting whether each acceptance criterion is met.

**Critical requirement**: This DAG MUST produce `SYNTHESIS.md` at `taskflow/dags/chirp-logged-out-r19/SYNTHESIS.md` as its declared output — this is what the overseer thread reads to confirm the DAG has folded. Prior rounds r10–r18 all stalled without producing SYNTHESIS.md; r19 must explicitly complete this step.

## Acceptance criteria (issue #35)

Each AC must be evaluated against the live code and reported as MET or NOT MET (with explanation) in SYNTHESIS.md:

- **AC-1**: A logged-out visitor can load the home/public timeline and open a user profile and read chirps without being forced to sign up or sign in first. (`REQ-PROD-013`, `BAR-011`)
- **AC-2**: On arrival with no content, the visitor sees a clear statement of what chirp is plus an obvious way to sign up or sign in — never a blank page or an unexplained error. (`REQ-PROD-014`, `BAR-011`)
- **AC-3**: If the timeline fails to load, a clear, recoverable message is shown instead of a broken screen. (`REQ-PROD-014`, `BAR-011`)
- **AC-4**: A "create an account" route is visible on the landing and on the sign-in screen, and following it reaches sign-up. (`REQ-PROD-015`, `BAR-011`)
- **AC-5**: The logged-out landing/timeline exercises its loading, empty, error, and end-of-list states accurately and distinctly. (`REQ-UX-002/030/031/032`, `BAR-011`, and the one-state-model criterion)

## Inputs

- **Repo**: `Nousix-LLC/nswe-demo` (GitHub)
- **Branch**: `work/chirp-logged-out` at head `617f25395eebe9475f19a90e0b1dac5921215ea3`
- **PR**: #263 (OPEN/MERGEABLE/CLEAN, CI run 42183715802 all green)
- **Issue**: #35 — Logged-out reading and a useful landing with accurate states
- **Prior work**: r10 pushed backend APIs + frontend routes (eaf96cf, e02b1d8a); r11 pushed fix commit (fed1fc8e); r12 pushed AC-4 sign-up form (21dca556); r18 advanced head to 617f2539 (CI green). All prior rounds stalled without SYNTHESIS.md — the pattern suggests missing the final synthesis step.
- **Prior DAG**: `taskflow/dags/chirp-logged-out-r18/`

## Declared output

1. **Commits** on `work/chirp-logged-out` addressing any AC gaps found (zero commits is valid if all ACs are already met at head `617f2539`)
2. **`SYNTHESIS.md`** at `taskflow/dags/chirp-logged-out-r19/SYNTHESIS.md` — the DAG's fold/verdict, accounting for each AC (met, or not and why). This file is **mandatory** — it is what the overseer reads to confirm the DAG has completed.
3. **No new PR** — push to the existing `work/chirp-logged-out` branch; PR #263 remains open.

## Concerns to cover

1. **AC verification**: Read the current code at head `617f2539` for each AC. For AC-1: confirm public timeline and user profile routes are accessible without auth. For AC-2: confirm the empty-state messaging is present and meaningful. For AC-3: confirm an error state component is present and shown on load failure. For AC-4: confirm sign-up link is visible from landing/sign-in screens. For AC-5: confirm the four states (loading, empty, error, end-of-list) are implemented as distinct UI states, not conflated.

2. **Gap remediation**: For any AC not met at head `617f2539`, make the minimum changes to bring it to met. Each AC is independently testable; a gap in one does not block the others.

3. **Synthesis completion**: After verification (and any gap fixes), write `taskflow/dags/chirp-logged-out-r19/SYNTHESIS.md` with verdict `PASS` (all ACs met) or `FAIL` (listing unresolved ACs and their blockers). This is the final, mandatory step — do not exit without it.

## Constraints

- **Repo scope**: `Nousix-LLC/nswe-demo` only. No other repos.
- **Branch**: `work/chirp-logged-out` only. Do not create new branches; do not push to `main`.
- **No force-push**.
- **No new PR**: PR #263 is the existing PR; do not open another.
- **SYNTHESIS.md is mandatory**: The DAG must produce `taskflow/dags/chirp-logged-out-r19/SYNTHESIS.md` before it exits. This is the declared output the overseer checks.
