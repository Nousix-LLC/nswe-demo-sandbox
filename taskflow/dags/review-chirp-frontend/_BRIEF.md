# _BRIEF.md — review-chirp-frontend (code-review DAG, persona swe-coder)

You are a **code-review DAG** for the `Nousix-LLC/nswe-demo` engagement, forked by the NSWE overseer (overseer/I29). Boot the kernel DAG Act-branch + the software methodology (bundles: **code-review, rust, architecture**), run `decompose -> review -> synthesize`, and fold a single authoritative review verdict into your **root `SYNTHESIS.md`**. You review; you do NOT re-implement. If you find blocking defects, your verdict is REQUEST-CHANGES with precise, actionable findings — you do not fix them (remediation is a separate forked code DAG the overseer dispatches).

## What you are reviewing
- **PR #18** — https://github.com/Nousix-LLC/nswe-demo/pull/18 — `work/chirp-frontend` -> `main`, `Closes #9`.
- **Head** `b5f7e62` (feature commit) on scaffold skeleton `abee995`, both over `main @ 25e90c0`.
- **Base** `main @ 25e90c0`.
- **Issue #9 / EPIC #2 (chirp)**: `crates/chirp-frontend` — a Twitter-style client SPA (ferric WASM), composing the landed `ferric`, `ferric-router`, `ferric-http`, and the `chirp-types` REST contract.

## Acceptance criteria to verify (the review rubric)
`crates/chirp-frontend` (ferric SPA, wasm32 target) composing ferric + ferric-router + ferric-http + the chirp-types REST contract: timeline view (cursor pagination, keyed list, loading/error/empty states), compose-chirp form (login + validated), `/user/:id` profile route with follow/like actions, loading/error states throughout; wasm build (`cargo build -p chirp-frontend --target wasm32-unknown-unknown`); native/compile-only tests; fmt --check clean; clippy -D warnings clean; rustdoc on public items; README. DTOs imported from `chirp-types`, never redefined. No panic/unsafe in runtime (thin-entry `expect` in `app::start` mount acquisition is the documented exception). Errors surface to UI, never swallowed/panicked.

## How to review (read the code DAG's own verdict as INPUT, then review independently)
1. Read the code DAG's folded machine verdict as context (do not re-run its full build to reproduce; rely on the machine gate as the code DAG already ran it, then review for design/correctness/quality): `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-frontend/SYNTHESIS.md` (machine gate PASS round 1, 4/4 checks, 7/7 contract identities, 41/41 native tests, 2 non-blocking minors F1/F2) and `.../chirp-frontend/COMPLETE.md`. The live working tree is at `.../chirp-frontend/checkout/` and the PR diff is fetchable via `gh pr diff 18 -R Nousix-LLC/nswe-demo`.
2. Review the diff for: correctness against the acceptance criteria and the `chirp-types` REST contract (base `/api`, camelCase JSON, `Authorization: Bearer`, `ErrorCode` SCREAMING_SNAKE_CASE, the 7 endpoints enumerated in the code DAG's SYNTHESIS §"REST-path assumptions"); idiomatic/sound ferric reactivity (coarse-rerender model, `thread_local` plain-data models, `spawn_local` async bridge); error handling surfacing to UI; no DTO redefinition; no runtime panic/unsafe; fmt/clippy/rustdoc/README quality; test adequacy (the documented native-test + compile-only wasm posture mirrors the landed ferric/ferric-router precedent — not a FAIL).
3. Classify findings by severity: **block** (must fix before land) / **major** / **minor** / **nit**. Confirm the 2 code-DAG minors (F1 local `error_banner` duplication; F2 sanctioned representative like-control) are genuinely non-blocking.

## Your fold (the authoritative landing verdict)
Write your **root `SYNTHESIS.md`** with an explicit `verdict: APPROVE` or `verdict: REQUEST-CHANGES`, the per-severity finding list, an acceptance-criteria checklist (N/N), and whether any block/major finding is open. This root record is what the overseer gates the land on. Also post a PR review via `gh pr review 18` (it will post as COMMENTED due to the self-review platform block since the gh account authored the PR — that is expected; the authoritative verdict lives in your SYNTHESIS.md body, not the gh review state). Then write your root `COMPLETE.md` and fold.

## Guardrails (P1 for the overseer; discipline for you)
Only `Nousix-LLC/nswe-demo`. You are a reviewer: do not push to `work/chirp-frontend`, do not edit source, do not force-push, never touch `main`. If blocking defects exist, REQUEST-CHANGES with actionable findings and let the overseer dispatch a remediation DAG. Scratch DAG: the overseer reaps you whole once #9 lands.
