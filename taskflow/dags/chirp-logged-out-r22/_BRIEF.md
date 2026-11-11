# _BRIEF.md — chirp-logged-out-r22 (swe-coder)

## Objective

Complete issue #35 — "Logged-out reading and a useful landing with accurate states" — for the chirp application (`Nousix-LLC/nswe-demo`). The code is already on branch `work/chirp-logged-out` at head `617f25395eebe9475f19a90e0b1dac5921215ea3`, PR #263 is OPEN/MERGEABLE/CLEAN, and CI (run 42183715802) is fully green (all checks pass). The goal is to synthesize a completed assessment of the work and produce a root `SYNTHESIS.md`.

**This DAG's most critical deliverable is `taskflow/dags/chirp-logged-out-r22/SYNTHESIS.md`.** Previous DAGs (r13–r21) all stalled without producing this file. That file is the fold point the overseer reads: without it, the goal cannot advance. It MUST be written at that path, at the root of this DAG's workspace, before this DAG terminates.

**DO NOT terminate without writing `SYNTHESIS.md`.** This is the single most important requirement. Every previous attempt (r13–r21) failed only because the DAG terminated without writing this file. If your work is complete — whether the verdict is PASS or FAIL — write `SYNTHESIS.md` and state the verdict before you stop.

## Background and stall history

The `work/chirp-logged-out` branch has been in progress since r1. The stall history is:

- **r1–r12**: Various stalls; r12 pushed AC-4 sign-up form (head advanced to `21dca556`) but stalled without SYNTHESIS.md.
- **r13–r17**: All stalled at `21dca556` (4/4 stall checks each), never synthesizing.
- **r18**: Advanced head from `21dca556` to `617f25395eebe9475f19a90e0b1dac5921215ea3`, then stalled 4/4 without SYNTHESIS.md.
- **r19**: Head UNCHANGED at `617f2539` through all 4 stall checks (confirmed stalled). Brief explicitly required SYNTHESIS.md. Stalled anyway.
- **r20**: Head UNCHANGED at `617f2539` through all 4 stall checks (confirmed stalled). Stalled anyway.
- **r21**: Head UNCHANGED at `617f2539` through all 4 stall checks (confirmed stalled I392). Stalled anyway.

The code at `617f2539` is functionally complete and CI-green. The DAGs are stalling because they are not writing `SYNTHESIS.md` before terminating. This DAG's only remaining job is to evaluate the existing code, determine PASS or FAIL, and write that verdict in `SYNTHESIS.md`.

## Branch and PR state

- **Branch**: `work/chirp-logged-out`
- **Head**: `617f25395eebe9475f19a90e0b1dac5921215ea3`
- **PR**: #263 — "feat: logged-out public timeline and user profiles (#35)" — OPEN/MERGEABLE/CLEAN
- **CI run 42183715802**: completed with conclusion=success (all checks green) on head `617f2539`
- **Issue**: #35 — OPEN/In Progress

## Issue #35 acceptance criteria

The following criteria from issue #35 must be evaluated and accounted for in SYNTHESIS.md:

**AC-1**: A logged-out visitor can load the home/public timeline and open a user profile and read chirps without being forced to sign up or sign in first. (`REQ-PROD-013`, `BAR-011`)

**AC-2**: On arrival with no content, the visitor sees a clear statement of what chirp is plus an obvious way to sign up or sign in — never a blank page or an unexplained error. (`REQ-PROD-014`, `BAR-011`)

**AC-3**: If the timeline fails to load, a clear, recoverable message is shown instead of a broken screen. (`REQ-PROD-014`, `BAR-011`)

**AC-4**: A "create an account" route is visible on the landing and on the sign-in screen, and following it reaches sign-up. (`REQ-PROD-015`, `BAR-011`)

**AC-5**: The logged-out landing/timeline exercises its loading, empty, error, and end-of-list states accurately and distinctly. (`REQ-UX-002/030/031/032`, `BAR-011`, and the one-state-model criterion)

## What to evaluate

1. **Review the code on `work/chirp-logged-out` at head `617f2539`** against each acceptance criterion above. The design documents at `design/product-requirements.md`, `design/experience-design.md`, and `design/release-bar.md` are the reference for what each criterion requires.

2. **Assess CI pass**: CI run 42183715802 is green. Confirm the checks cover the relevant code paths.

3. **Determine PASS or FAIL**:
   - PASS: All 5 acceptance criteria are met by the code at head `617f2539`.
   - FAIL: One or more criteria are not met. For each failing criterion, state what is missing or wrong.

4. **If code changes are needed**: Commit them to `work/chirp-logged-out` with a clear commit message, then re-evaluate. Do not force-push.

## Declared outputs

1. **`taskflow/dags/chirp-logged-out-r22/SYNTHESIS.md`** — the DAG's fold record. **This file MUST be written before this DAG terminates.** It must contain:
   - Overall verdict: `PASS` or `FAIL`
   - Per-criterion assessment: AC-1 through AC-5, each listed as MET or NOT MET with evidence
   - If FAIL: the specific blockers (what is missing, what file/component, what must change)
   - Final head SHA at synthesis time

2. Any additional commits to `work/chirp-logged-out` if code changes were needed to meet the criteria.

## Critical reminder

**Write `taskflow/dags/chirp-logged-out-r22/SYNTHESIS.md` before you stop.** This is the one requirement that has caused 9 consecutive stalls (r13–r21). No matter what your assessment is — PASS or FAIL — write that file. The overseer cannot advance this goal without it.

## Constraints

- Repo: `Nousix-LLC/nswe-demo`
- Branch: `work/chirp-logged-out` — no force-push
- Do not modify files outside the application's scope
- The root `SYNTHESIS.md` at `taskflow/dags/chirp-logged-out-r22/SYNTHESIS.md` is mandatory output — the DAG must not terminate without it
