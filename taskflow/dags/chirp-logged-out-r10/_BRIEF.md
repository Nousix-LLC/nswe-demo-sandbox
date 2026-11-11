# _BRIEF.md — chirp-logged-out-r10 (swe-coder)

## Objective

Complete the logged-out visitor experience for the chirp application and produce a root `SYNTHESIS.md` accounting for all acceptance criteria in issue #35 ("Logged-out reading and a useful landing with accurate states").

The previous coding DAG (r9) resolved the wasm CI blocker (non-exhaustive `EventKind` match) and pushed code to the branch. All 6 CI checks are passing. r10 starts from that branch state, reviews what is there, completes whatever remains to satisfy the acceptance criteria, and synthesizes.

## Repository

`Nousix-LLC/nswe-demo`

## Branch and PR

- Branch: `work/chirp-logged-out` (existing — do NOT create a new branch)
- PR: #263 — "feat: logged-out reading and accurate landing states (#35)" (OPEN)
- Current head: `2615ba1d91509e505290d577b4997aa134fab4bf`
- CI status at current head: ALL 6 PASS — clippy, doc, fmt, test, wasm, image

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
- The wasm CI blocker (non-exhaustive `EventKind` match in `crates/ferric/src/vdom.rs`) was resolved in head `2615ba1d` by the previous DAG run.
- CI is fully green at the current head. No CI blockers remain.
- Architecture: chirp is a ferric SPA (`crates/chirp-frontend`) backed by an axum REST API (`crates/chirp-server`). The frontend uses ferric's reactive signals, component model, router, and http client. The public timeline reads from a persistent store already delivered.

## Task

1. Inspect the current branch (`work/chirp-logged-out` at head `2615ba1d`) to understand what the previous DAG implemented.
2. Evaluate each acceptance criterion above against the current implementation.
3. Implement whatever is missing or incomplete to meet all five criteria.
4. Ensure all 6 CI checks continue to pass (clippy, doc, fmt, test, wasm, image).
5. Push any additional commits to `work/chirp-logged-out`.
6. Produce a root `SYNTHESIS.md` that:
   - States the overall verdict (PASS or FAIL).
   - Accounts for each of the five acceptance criteria above, one by one (met or not met and why).
   - Notes the CI status at the final head.
   - Notes any remaining gaps, if any.

## Declared output

- Commits on `work/chirp-logged-out` (zero or more additional commits beyond `2615ba1d`).
- PR #263 updated (if new commits are pushed).
- Root `SYNTHESIS.md` at the DAG workspace root, with the verdict and per-criterion accounting.

## Constraints

- Repo scope: `Nousix-LLC/nswe-demo`, crates `chirp-frontend`, `chirp-server`, `chirp-types`, `ferric`.
- Do not touch other crates, namespaces, or repos.
- Do not force-push. Do not open a new PR.
- Do not carry forward any host paths, internal addresses, or taskflow internals into code, comments, issues, or PR descriptions.
