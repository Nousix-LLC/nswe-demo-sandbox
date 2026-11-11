# _BRIEF.md — chirp-logged-out-r23 (swe-coder)

## Objective

Write `taskflow/dags/chirp-logged-out-r23/SYNTHESIS.md` — this is the **only deliverable that matters**.

The code for issue #35 ("Logged-out reading and a useful landing with accurate states") is already on branch
`work/chirp-logged-out` at head `617f25395eebe9475f19a90e0b1dac5921215ea3`. PR #263 is OPEN/MERGEABLE/CLEAN.
CI run 42183715802 is green (all 6 checks pass: fmt, clippy, test, wasm, doc, image).

**Ten consecutive DAGs (r13–r22) have all stalled without writing SYNTHESIS.md.** That is the only failure.
The code is there. CI is green. Each DAG ran, did work or found nothing to do, and then terminated without
writing `SYNTHESIS.md`. This DAG must not do that.

**Write `taskflow/dags/chirp-logged-out-r23/SYNTHESIS.md` first, before anything else significant.** Even a
preliminary SYNTHESIS.md that says "evaluating" and is overwritten later is better than no SYNTHESIS.md.
The goal is: by the time this DAG terminates for any reason, that file exists with a verdict.

## Stall history

The `work/chirp-logged-out` branch has been in progress across 22 consecutive DAG attempts:

- **r1–r11**: Various stalls; r10 pushed feature-complete code (eaf96cf, e02b1d8a); r11 pushed fix (fed1fc8e);
  r12 pushed AC-4 sign-up form (head advanced to `21dca556`).
- **r13–r17**: All stalled at `21dca556` (4/4 stall checks each), never synthesizing.
- **r18**: Advanced head from `21dca556` to `617f25395eebe9475f19a90e0b1dac5921215ea3`, then stalled 4/4.
- **r19**: Head UNCHANGED at `617f2539` through all 4 stall checks. Brief explicitly required SYNTHESIS.md. Stalled.
- **r20**: Head UNCHANGED at `617f2539` through all 4 stall checks. Stalled.
- **r21**: Head UNCHANGED at `617f2539` through all 4 stall checks. Stalled.
- **r22**: Head UNCHANGED at `617f2539` through all 4 stall checks. Brief was entirely about writing SYNTHESIS.md.
  Stalled anyway — workspace contains only `_BRIEF.md` and `_FORK.md`, no child tasks started.

The pattern: the DAG either never starts executing or starts and terminates without reaching synthesis.

## Branch and PR state

- **Branch**: `work/chirp-logged-out`
- **Head**: `617f25395eebe9475f19a90e0b1dac5921215ea3`
- **PR**: #263 — "feat: logged-out public timeline and user profiles (#35)" — OPEN/MERGEABLE/CLEAN
- **CI run 42183715802**: completed with conclusion=success (all 6 checks green: fmt, clippy, test, wasm, doc, image)
- **Issue**: #35 — OPEN/In Progress/assigned (mattsmcknight)

## Declared outputs (required)

1. **`taskflow/dags/chirp-logged-out-r23/SYNTHESIS.md`** — mandatory, must exist before this DAG terminates.

   Minimum acceptable content:
   ```
   # SYNTHESIS — chirp-logged-out-r23
   verdict: PASS | FAIL
   head_sha: 617f25395eebe9475f19a90e0b1dac5921215ea3
   [per-criterion assessment: AC-1 through AC-5]
   ```

2. Any commits to `work/chirp-logged-out` if changes are needed to meet acceptance criteria. (Not required if
   AC-1 through AC-5 are already met by the code at `617f2539`.)

**Write SYNTHESIS.md before terminating. This requirement overrides all else.**

## Issue #35 acceptance criteria

Evaluate the code at head `617f2539` against each criterion. The design documents
`design/product-requirements.md`, `design/experience-design.md`, and `design/release-bar.md` are the
reference for what each criterion requires.

**AC-1**: A logged-out visitor can load the home/public timeline and open a user profile and read chirps
without being forced to sign up or sign in first. (`REQ-PROD-013`, `BAR-011`)

**AC-2**: On arrival with no content, the visitor sees a clear statement of what chirp is plus an obvious way
to sign up or sign in — never a blank page or an unexplained error. (`REQ-PROD-014`, `BAR-011`)

**AC-3**: If the timeline fails to load, a clear, recoverable message is shown instead of a broken screen.
(`REQ-PROD-014`, `BAR-011`)

**AC-4**: A "create an account" route is visible on the landing and on the sign-in screen, and following it
reaches sign-up. (`REQ-PROD-015`, `BAR-011`)

**AC-5**: The logged-out landing/timeline exercises its loading, empty, error, and end-of-list states
accurately and distinctly. (`REQ-UX-002/030/031/032`, `BAR-011`, and the one-state-model criterion)

## Constraints

- Repo: `Nousix-LLC/nswe-demo`
- Branch: `work/chirp-logged-out` — **no force-push**
- Do not modify files outside the application's scope
- The root `SYNTHESIS.md` at `taskflow/dags/chirp-logged-out-r23/SYNTHESIS.md` is mandatory — the DAG must
  not terminate without it
