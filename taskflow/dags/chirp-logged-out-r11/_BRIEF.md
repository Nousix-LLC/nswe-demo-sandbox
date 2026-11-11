# _BRIEF.md — chirp-logged-out-r11 (swe-coder)

## Objective

Complete the logged-out visitor experience for the chirp application and produce a root `SYNTHESIS.md` accounting for all acceptance criteria in issue #35 ("Logged-out reading and a useful landing with accurate states").

r10 made substantial progress: it pushed backend API routes (GET /api/chirps + GET /api/users/:username/chirps) in commit `eaf96cf` and frontend routes (landing, public_profile, sign_in, sign_up with correct states) in commit `e02b1d8a`. However r10 stalled before producing SYNTHESIS.md. r11 starts from that branch state, verifies the implementation meets all five acceptance criteria, completes any remaining gaps, and synthesizes.

## Repository

`Nousix-LLC/nswe-demo`

## Branch and PR

- Branch: `work/chirp-logged-out` (existing — do NOT create a new branch)
- PR: #263 — "feat: logged-out reading and accurate landing states (#35)" (OPEN)
- Current head: `e02b1d8af69113e6a51ec8ccf1092f61f382c833`
- CI status at current head: ALL 6 PASS — clippy, doc, fmt, test, wasm, image (run 42169201251)

Do not force-push. Do not open a new PR.

## Issue #35 — Acceptance Criteria

Taken directly from the issue:

1. A logged-out visitor can load the home/public timeline and open a user profile and read chirps without being forced to sign up or sign in first. (`REQ-PROD-013`, `BAR-011`)
2. On arrival with no content, the visitor sees a clear statement of what chirp is plus an obvious way to sign up or sign in — never a blank page or an unexplained error. (`REQ-PROD-014`, `BAR-011`)
3. If the timeline fails to load, a clear, recoverable message is shown instead of a broken screen. (`REQ-PROD-014`, `BAR-011`)
4. A "create an account" route is visible on the landing and on the sign-in screen, and following it reaches sign-up. (`REQ-PROD-015`, `BAR-011`)
5. The logged-out landing/timeline exercises its loading, empty, error, and end-of-list states accurately and distinctly. (`REQ-UX-002/030/031/032`, `BAR-011`, and the one-state-model criterion)

## Design references

- `design/product-requirements.md` — §3 User journeys; §4 `REQ-PROD-013`, `REQ-PROD-014`, `REQ-PROD-015`
- `design/experience-design.md` — §1 Information architecture & interaction; §2 Screens, flows & states; §6 `REQ-UX-002`, `REQ-UX-030`, `REQ-UX-031`, `REQ-UX-032`
- `design/release-bar.md` — §C `BAR-011`

## Context from prior work

- Dependencies: durable persistence (#56) is DONE; ferric SSR (#223/#224/#226) is DONE. Both were blocking #35.
- r10 pushed real work before stalling:
  - Commit `eaf96cf`: backend API routes — `GET /api/chirps` (public timeline) + `GET /api/users/:username/chirps` (user chirps). 71 tests pass.
  - Commit `e02b1d8a`: frontend routes — landing page, public_profile page, sign_in page, sign_up page with correct states.
- CI is fully green at the current head (run 42169201251, all 6 checks PASS). No CI blockers.
- Architecture: chirp is a ferric SPA (`crates/chirp-frontend`) backed by an axum REST API (`crates/chirp-server`). The frontend uses ferric's reactive signals, component model, router, and http client. The public timeline reads from a persistent store already delivered.

## Task

1. Inspect the current branch (`work/chirp-logged-out` at head `e02b1d8a`) to understand what r10 implemented.
2. Evaluate each acceptance criterion above against the current implementation.
3. Implement whatever is missing or incomplete to meet all five criteria.
4. Ensure all 6 CI checks continue to pass (clippy, doc, fmt, test, wasm, image).
5. Push any additional commits to `work/chirp-logged-out` (or zero commits if the implementation is already complete).
6. Produce a root `SYNTHESIS.md` that:
   - States the overall verdict (PASS or FAIL).
   - Accounts for each of the five acceptance criteria above, one by one (met or not met and why).
   - Notes the CI status at the final head.
   - Notes any remaining gaps, if any.

## Declared output

- Commits on `work/chirp-logged-out` (zero or more additional commits beyond `e02b1d8a`).
- PR #263 updated (if new commits are pushed).
- Root `SYNTHESIS.md` at the DAG workspace root (`taskflow/dags/chirp-logged-out-r11/SYNTHESIS.md`), with the verdict and per-criterion accounting.

## Constraints

- Repo scope: `Nousix-LLC/nswe-demo`, crates `chirp-frontend`, `chirp-server`, `chirp-types`, `ferric`.
- Do not touch other crates, namespaces, or repos.
- Do not force-push. Do not open a new PR.
- Do not carry forward any host paths, internal addresses, or taskflow internals into code, comments, issues, or PR descriptions.
