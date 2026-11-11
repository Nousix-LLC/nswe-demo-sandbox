# _BRIEF.md — chirp-logged-out-r24 (swe-coder)

## Objective

Bring issue #35 — logged-out reading and a useful landing with accurate states — to a fully synthesized
PASS on branch `work/chirp-logged-out`. The branch already exists, with head `decb6196c2c1e6ed421d393a642f0c844cc333ba`,
and CI is ALL 6 PASS on that head. PR #263 ("feat: logged-out public timeline and user profiles (#35)")
is OPEN and MERGEABLE.

**First priority: assess the current state of the branch against the acceptance criteria and write
`SYNTHESIS.md` immediately.** Prior DAGs on this goal have consistently stalled after committing code
without producing a `SYNTHESIS.md`. The root-level `SYNTHESIS.md` at the DAG workspace root is the
fold record the overseer reads. Without it, the work is invisible regardless of how complete the code
is. If the code on `decb6196` already satisfies all acceptance criteria, write a PASS `SYNTHESIS.md`
and stop. If blockers remain, address them, then write `SYNTHESIS.md` as the final step.

## Repository

`Nousix-LLC/nswe-demo` — a Rust workspace:
- `crates/ferric` — client-side WASM framework (signals, components, DOM, router, fetch client)
- `crates/chirp-types` — shared types contract (chirp-server ↔ chirp-frontend)
- `crates/chirp-server` — axum REST API, persistence (Postgres), static SPA serving
- `crates/chirp-frontend` — ferric SPA (the client-side app)
- `deploy/` — Kubernetes manifests; delivery is GitOps via ArgoCD

Branch: `work/chirp-logged-out`. Current head: `decb6196c2c1e6ed421d393a642f0c844cc333ba`.

## Acceptance criteria (from issue #35)

- AC-1: A logged-out visitor can load the home/public timeline and open a user profile and read chirps
  without being forced to sign up or sign in first. (`REQ-PROD-013`, `BAR-011`)
- AC-2: On arrival with no content, the visitor sees a clear statement of what chirp is plus an
  obvious way to sign up or sign in — never a blank page or an unexplained error. (`REQ-PROD-014`,
  `BAR-011`)
- AC-3: If the timeline fails to load, a clear, recoverable message is shown instead of a broken
  screen. (`REQ-PROD-014`, `BAR-011`)
- AC-4: A "create an account" route is visible on the landing and on the sign-in screen, and
  following it reaches sign-up. (`REQ-PROD-015`, `BAR-011`)
- AC-5: The logged-out landing/timeline exercises its loading, empty, error, and end-of-list states
  accurately and distinctly. (`REQ-UX-002/030/031/032`, `BAR-011`, and the one-state-model criterion)

Design traces:
- `design/product-requirements.md` — §3 User journeys; §4 `REQ-PROD-013`, `REQ-PROD-014`, `REQ-PROD-015`
- `design/experience-design.md` — §1 Information architecture & interaction; §2 Screens, flows & states;
  §6 `REQ-UX-002`, `REQ-UX-030`, `REQ-UX-031`, `REQ-UX-032`
- `design/release-bar.md` — §C `BAR-011`
- Epic: EPIC-CORELOOP (#34)

## Prior work on this branch

The branch has been worked by 23 prior DAGs. Key history:

- **r10** pushed feature-complete backend APIs and frontend routes.
- **r11** pushed a fix commit.
- **r12** pushed the AC-4 sign-up form at `21dca556` and stalled (4/4). CI was all green.
- **r13–r17**: all stalled at `21dca556` (4/4 each). No SYNTHESIS.md produced.
- **r18**: advanced head from `21dca556` to `617f25395eebe9475f19a90e0b1dac5921215ea3`, then stalled (4/4).
- **r19–r22**: all stalled at `617f2539` (4/4 each). No SYNTHESIS.md produced.
- **r23** (dispatched from overseer I396): advanced head from `617f2539` to
  `decb6196c2c1e6ed421d393a642f0c844cc333ba`. CI run 42194072348 on `decb6196`: ALL 6 PASS
  (doc / fmt / clippy / wasm / test / image — all SUCCESS). Then r23 stalled without producing
  SYNTHESIS.md (4/4 stall checks I399–I402, head UNCHANGED throughout).

**Current state:**
- Branch head: `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- PR #263: OPEN, MERGEABLE, CI ALL 6 PASS (run 42194072348)
- No `SYNTHESIS.md` exists anywhere in the DAG workspace

The fact that CI is fully green (all 6 checks) and the PR is MERGEABLE strongly suggests the
code work on this branch is substantially complete. The most likely scenario is that the
acceptance criteria are met and the DAG only needs to verify this and produce a SYNTHESIS.md.

## Inputs

- Branch `work/chirp-logged-out` at head `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- PR #263: `https://github.com/Nousix-LLC/nswe-demo/pull/263`
- Issue #35: `https://github.com/Nousix-LLC/nswe-demo/issues/35`
- Design documents (in-repo): `design/product-requirements.md`, `design/experience-design.md`,
  `design/release-bar.md`
- Dependencies satisfied: issue #56 (durable persistence) — MERGED; issue #228 (ferric SSR) — MERGED

## Declared output

1. If code is complete: a root-level `SYNTHESIS.md` at the DAG workspace root with verdict `PASS`,
   accounting for each AC.
2. If code blockers remain: commits on `work/chirp-logged-out` closing those blockers, then a root-level
   `SYNTHESIS.md` with verdict `PASS` or `FAIL` accounting for each AC.
3. The existing PR #263 is updated if needed (do not open a new PR — one already exists for this branch).

**`SYNTHESIS.md` is not optional and must be the final deliverable, whatever else happens.**

## Concerns to cover

1. **AC verification against `decb6196`**: Read each of the 5 ACs against the code on the branch.
   For each: is it met? What evidence (file, route, component) supports the verdict?
2. **State coverage (AC-5)**: Does the frontend handle loading, empty, error, and end-of-list states
   distinctly? Each must be a separate rendered state, not collapsed.
3. **No forced sign-in (AC-1)**: Are logged-out routes gated? Does the router or server redirect a
   logged-out visitor to login before showing the timeline or a profile?
4. **Landing experience (AC-2)**: On first load with no data, does the visitor see something
   informative rather than a blank or error screen?
5. **Sign-up route visibility (AC-4)**: Is "create an account" visible on the landing and sign-in screens,
   and does it lead to sign-up?
6. **CI green → code coherent**: The CI passing is evidence the code compiles, tests pass, and the
   image builds. Use this as a baseline; the concern here is functional correctness against the ACs,
   not build correctness.

## Constraints

- Branch: `work/chirp-logged-out` only. No force-push.
- Scope: `crates/chirp-server` and `crates/chirp-frontend` (and `crates/chirp-types` if the contract
  needs updating). Do not touch `crates/ferric` or `deploy/` for this goal.
- Do not open a new PR. PR #263 exists; update its description if the head changes.
- The `SYNTHESIS.md` MUST be the final step, produced after all code work (if any) is committed and
  pushed and CI is green.
