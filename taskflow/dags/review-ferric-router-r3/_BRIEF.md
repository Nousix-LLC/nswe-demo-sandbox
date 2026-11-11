# _BRIEF.md — review-ferric-router-r3

**Kind**: Review DAG  
**Launch agent**: swe-reviewer  
**Disposition**: reap-whole-after-land

## Target

**PR #203** — `work/ferric-router-r3` on `Nousix-LLC/nswe-demo`  
Title: "fix(ferric-router): remove unused VNode import from test closure (remediation r3)"  
Base: `main` (sha `aa2468771eccd9e2ee79c12c79b8943fca18e07a`)  
Head: `7219e21beff6768bdbc271a45b90355066870551`  
State: OPEN / MERGEABLE  
CI run: **41796577463** — all 6 checks SUCCESS (fmt, clippy, test, wasm, doc, image)

**4 commits** in this PR (on top of main):

1. `3404dea` — feat(ferric-router): add navigate_replace (REQ-RT-003)
2. `9c9fdd8` — ferric-router: active-route awareness on Link::build() (REQ-RT-007)
3. `c03818f` — feat(ferric-router): nested routes, replace navigation, active links
4. `7219e21` — fix(ferric-router): remove unused VNode import from nested route test closure

Commits 1–3 are cherry-picks of the router scope from the original PR #192 (ferric-router-r1), isolated
into this router-only PR by remediation ferric-router-r2. Commit 4 (7219e21) is the ferric-router-r3
fix for the clippy `unused import: VNode` error that caused ferric-router-r2's machine gate FAIL.

## Issues covered

- **#131** — Ferric Router epic: nested routes, replace navigation, active-route awareness (usable_early)
- **#146** — `navigate_replace()` history API (REQ-RT-003)
- **#147** — Active-route awareness on `<Link>` (REQ-RT-007)

## Design source

`design/ferric/router-and-http.md` — **Part 1 (Router)**, requirements REQ-RT-001 through REQ-RT-008.
This is the design this change is held to. The review's correctness concern checks the change against
each requirement and each issue's acceptance criteria.

## Prior review and disposition

- **review-ferric-router-r1** gave REQUEST_CHANGES with a single blocker:
  - **B1**: PR #192 bundled unreviewed scope — ferric-macros + context API (3 290 lines, 12/16 commits)
    not covered by the review brief. That scope is entirely separate from the router.
  - Disposition: B1 is **fully resolved** by the PR split. PR #203 is router-only (4 commits, all
    router scope). The macros/context scope landed separately in PR #188 (reviewed and approved by
    review-ferric-epic-authoring-r1).
- Non-blockers from review-ferric-router-r1: #194 (navigate input validation — `href=""`), #195
  (commit description narrower than #146 scope). These are filed as backlog issues; this review is
  free to close them if the router-only change addresses them, or note whether they remain open.

**This review is a first full code review of the router-only change** (4 commits, PR #203).

## Code DAG synthesis

`taskflow/dags/ferric-router-r3/SYNTHESIS.md` — the ferric-router-r3 DAG's verdict. Machine gate PASS.

## Review concerns

Evaluate all five concerns. Each concern's findings are classified as a blocker (must fix before landing)
or non-blocker (backlog issue), and the review accounts for what it found clean, not only what it found
wrong.

### 1. Correctness

Does the change satisfy each requirement in REQ-RT-001 through REQ-RT-008 and each acceptance criterion
for issues #131, #146, and #147? Check:
- Router state transitions (mount, navigate, replace, pop, nested route resolution).
- Edge cases: empty path, trailing slash, root route, unmatched route fallback, nested outlet with no
  matching child.
- Error paths: invalid `href`, navigate called before mount, nested outlet with no outlet registered
  in the parent.
- Invariants: history entries after replace vs push; active-route signal updates on navigation;
  `<Link>` aria-current on active/inactive; correct outlet render on nested route match.
- Concurrency and reactivity: signal updates after navigation fire synchronously or in the correct
  reactive order; no stale signals, no double-render.
- Whether #194 (navigate input validation) and #195 (commit description narrower than #146 scope) are
  addressed by this change, or remain open as stated.

### 2. Code quality

Responsibilities and coupling: does each type/function have one clear job? Are abstraction boundaries
well placed between the router state, the history API bridge, the outlet component, and the `<Link>`
component?
- Naming: types, functions, constants clear and consistent with the rest of the ferric codebase.
- Function size: are any functions doing more than one thing in a way that obscures logic?
- Error-handling style: are errors surfaced consistently (Result, panic, silent fail)? Is the choice
  appropriate for client-side WASM?
- Does the change leave the router code simpler to extend (e.g., adding query-string support or
  hash routing later)?

### 3. Test coverage

Do the tests exercise each acceptance criterion from #131, #146, and #147, and each REQ-RT-001..008
requirement that has testable behavior?
- Edge and error paths: are unmatched routes, root-route match, nested outlet with no match,
  navigate-before-mount, and replace-vs-push all tested?
- Do the tests assert real behavior (the signal value, the rendered outlet content, the history length)
  rather than pass vacuously?
- Coverage of the new nested-route test added in commit 7219e21 (the clippy-fix commit): does the test
  actually validate layout-with-child-view rendering, or is it a skeleton?

### 4. Rust idioms

- Lifetime correctness: are the router's internal references, signal closures, and outlet component
  handles lifetime-safe? No use-after-free, no dangling wasm-bindgen handles.
- `pub` surface: is the public API surface additive and minimal? No internal types accidentally exported.
- wasm-bindgen idioms: are `JsValue`, `Closure`, and `web_sys` handles managed correctly? No closure
  leaks, no forgotten `forget()`/`into_js_value()` where the closure must stay alive.
- Soundness: any `unsafe` blocks? If so, what invariants do they rely on and are they upheld?

### 5. API and contract stability

- Is the change additive on the public surface (the `ferric_router` prelude/re-exports)? No breaking
  changes to existing consumers.
- Items frozen by REQ-RT-001..008 (the router's core navigation API): are they unchanged?
- Interoperability with ferric's signal/component model (landed in PR #188): are the contracts at the
  seam (signal subscription, component registration, outlet rendering) honored?

## Declared output

1. **Posted review on PR #203** — the review as a PR comment carrying the verdict (APPROVE or
   REQUEST_CHANGES) and the findings per concern. If the platform blocks posting as a formal approval
   (same account), post as a review comment with the verdict stated explicitly.
2. **Root `SYNTHESIS.md`** at `taskflow/dags/review-ferric-router-r3/SYNTHESIS.md` with:
   - Overall verdict: APPROVE or REQUEST_CHANGES.
   - For each of the 5 concerns: what was checked, what was found clean, any findings with severity
     and blocker/non-blocker classification.
   - Disposition of non-blockers: each filed as a backlog issue on `Nousix-LLC/nswe-demo`, or noted
     as already filed (#194, #195, #178).
3. **Non-blocking findings filed as backlog issues** on `Nousix-LLC/nswe-demo` with labels and links
   to the relevant file/line in the repository.

Findings posted to GitHub are written for the repository's readers: they reference files and lines in
the repo, not host paths or DAG internals.
