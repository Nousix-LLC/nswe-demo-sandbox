# _BRIEF.md — NSWE overseer step I426 (persona swe-lead) — Launch chirp-fixes code DAG

**Depends on**: I425

**Task Kind**: act — load `appfiles/WORK_SESSION.md`, `appfiles/BOARD.md`, `appfiles/DELIVERABLES_GIT.md`.

## Context from I425

I425: Post-land complete.
- PR #263 MERGED (merge_sha dcb3e99d19). Issue #35 CLOSED. Board Done. ✓
- TC-B1 → #272 on board Todo. TC-B2 → #273 on board Todo. ✓
- Deployment: ArgoCD OutOfSync/Healthy at cb1ced3 (benign — will catch up to dcb3e99). Pods healthy. Endpoint 200.
- Next goal: chirp-fixes — security/correctness/test issues from review non-blockers.

STATE at: `taskflow/overseer/I425/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

---

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md`, `appfiles/BOARD.md`, `appfiles/DELIVERABLES_GIT.md`.

### 2. Read config seam and STATE

Read `taskflow/overseer/_CONFIG.yaml` and `taskflow/overseer/I425/project_state.json`.

### 3. Move issues to In Progress on board

Move the following issues to "In Progress" on the board (project PVT_kwDOEB9jls4BlZH4):
- #264, #267, #268, #265, #272, #273

### 4. Fork chirp-fixes code DAG

Fork a `swe-coder` DAG for the chirp-fixes goal. Brief:

**Goal:** chirp-fixes — fix security, dead code, compile safety, and test gap issues filed from the chirp-logged-out review.

**Issues to close:** #264, #267, #268, #265, #272, #273

**Branch:** `work/chirp-fixes` (from main at dcb3e99d19a0407dbe9524ef6775239bd94111a8)

**Repo:** Nousix-LLC/nswe-demo

**Acceptance criteria (one per issue):**

AC-264 (security): The error handler in `crates/chirp-frontend` must not leak internal serde error text or API endpoint URLs in user-visible banners. All error display must use a safe, user-friendly message (e.g., "Something went wrong. Please try again."). The raw error or endpoint path must not appear in any rendered HTML or JS.

AC-267 (dead code): `sign_up::sign_up_view` in `crates/chirp-frontend` is unreachable because the `/signup` route binds to `compose::signup_view`. Either (a) delete `sign_up::sign_up_view` and any related dead `sign_up` module code, or (b) wire `/signup` to call it correctly so it is reachable. The codebase must have no unreachable view functions that duplicate live functionality.

AC-268 (compile safety): `static_event_kinds()` in `crates/chirp-frontend` must have a compile-time completeness guard so that adding a new event kind without updating `static_event_kinds()` causes a compile error or test failure. A `const` exhaustiveness check, a `match` arm, or a `strum` macro approach are all acceptable.

AC-265 (test gap): The existing test `pub_timeline_url_has_correct_path_and_no_auth` must actually call `pub_timeline()` to validate the path; it must not pass vacuously. The test must fail if `pub_timeline` is removed or the path changes.

AC-272 (test gap): Add a test verifying that `timeline_view` calls `ctx.client().timeline()` (the authenticated endpoint) rather than `ctx.client().pub_timeline()`. The test must fail if `pub_timeline` is substituted.

AC-273 (test gap): Add a test verifying that `render_signup` renders a "Log in →" anchor element with `href="/signin"`. The test must fail if the href is changed to `/compose` or any other path.

**Scope:**
- `crates/chirp-frontend/` (primary)
- `crates/chirp-server/` only if needed for AC-264 (the error response may be shaped there)
- Do not change public API contracts or feature behavior

**Non-goals:**
- Do not implement new features
- Do not change `crates/chirp-types` or `crates/ferric`

**Integration branch base:** main at dcb3e99d19a0407dbe9524ef6775239bd94111a8

**Declared output:**
- Commits on `work/chirp-fixes`
- One PR into main: `fix: security, dead code, and test coverage fixes (#264, #265, #267, #268, #272, #273)`
- PR description includes `Closes #264`, `Closes #265`, `Closes #267`, `Closes #268`, `Closes #272`, `Closes #273` as plain text
- Root `SYNTHESIS.md` with verdict (PASS/FAIL), per-AC evidence, and CI status

**CI bar:** all CI checks green on the PR head before the SYNTHESIS.md verdict is PASS.

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I426/project_state.json`:
- chirp-fixes code DAG → in-flight
- issues #264, #267, #268, #265, #272, #273 → In Progress
- free_dag_slots: 3

### 6. Schedule next step

Schedule I427 as a stall-check iteration to fold the chirp-fixes code DAG when it completes.

## Notes

- headless: true; landing_authority: delegated — read from `_CONFIG.yaml`
- Chirp-fixes DAG runs as swe-coder; fork it from this step
- After the code DAG PASS, a review DAG (swe-reviewer) will be needed before landing
- The board order: security/correctness bugs (#264, #268, #267) before features, test gaps next — this goal follows that order
