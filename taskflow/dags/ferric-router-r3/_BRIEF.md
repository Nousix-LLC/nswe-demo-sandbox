# _BRIEF.md — ferric-router-r3

**Goal**: Fix the clippy `unused import: VNode` error in `crates/ferric-router` test code. Build on the
clean 3-commit router-only branch from ferric-router-r2 (`work/ferric-router-r2`), producing a fresh branch
`work/ferric-router-r3` and a new PR that supersedes PR #202. All 6 CI checks must PASS.

**Repository**: Nousix-LLC/nswe-demo

---

## Context and Lessons from ferric-router-r2

ferric-router-r2 (PR #202, branch `work/ferric-router-r2`) delivered a clean router-only 3-commit branch
(cherry-picks c03818f, 9c9fdd8, 3404dea — rebased on main commit aa24687). The macros/context scope is NIL
DIFF (all already on main via PR #188). PR #202 is OPEN and MERGEABLE.

**CI result** (run 41786452070):
- fmt: SUCCESS
- clippy: **FAILURE** — `unused import: VNode` in `crates/ferric-router` lib tests (`-D unused-imports`
  implied by `-D warnings`). Error location: test code in `crates/ferric-router`.
- test: SUCCESS
- wasm: SUCCESS
- doc: SUCCESS
- image: SKIPPED

**The fix is minimal**: find the `use ferric::prelude::VNode` (or similar) import in the `crates/ferric-router`
test section, remove it. The import was added but `VNode` is not referenced in the test body. No other CI
jobs fail and no other crate is affected.

**Do NOT re-introduce macros/context scope**. This is router-only: `crates/ferric-router/` only.

---

## Inputs

- Repository: Nousix-LLC/nswe-demo
- Base: branch `work/ferric-router-r2` (3 commits: c03818f, 9c9fdd8, 3404dea — router-only scope,
  `crates/ferric-router/` files only)
- Failing CI run: 41786452070, clippy job: `unused import: VNode` in `crates/ferric-router` test code
- PR #202 (open, to be superseded — do NOT close it manually)
- PR #192 (open, superseded by PR #202; will be closed when PR #203 merges — do not close it either)
- Design: `design/ferric/router-and-http.md` Part 1 (REQ-RT-001..008) — the same design as ferric-router-r1/r2
- Issues: #131 (navigate_replace — REQ-RT-003), #146 (active-route awareness — REQ-RT-005/006), #147
  (nested routes — REQ-RT-004)

---

## Declared Output

1. Branch `work/ferric-router-r3` on Nousix-LLC/nswe-demo — the 3 router commits from `work/ferric-router-r2`
   plus one additional commit that removes the unused `VNode` import from `crates/ferric-router` tests.
   Alternatively, a fresh cherry-pick onto main (aa2468771eccd9e2ee79c12c79b8943fca18e07a) with the fix
   incorporated — the approach is the DAG's choice; what matters is the branch scope (router-only) and that
   CI is all green.
2. PR #203 (new PR) on Nousix-LLC/nswe-demo targeting `main`, title and body describing the router
   implementation, closing issues #131, #146, #147, and noting it supersedes PR #202.
3. All 6 CI checks PASS on PR #203 (fmt, clippy, test, wasm, doc, image or image SKIPPED on a non-image
   branch).
4. Root `SYNTHESIS.md` accounting for all 3 issues (#131, #146, #147) and the CI result (all checks PASS).

---

## Concerns to Evaluate

1. **CI fix completeness**: The clippy error `unused import: VNode` is removed and all 6 CI checks PASS. No
   new clippy warnings introduced. The fix does not add any new imports or leave dead code that could trigger
   further warnings.

2. **Scope integrity**: Branch diff vs `main` (aa24687) remains router-only — only `crates/ferric-router/`
   files. Zero ferric-macros or other crate files in the diff. Verify the diff is clean before opening PR #203.

3. **Issue coverage**: All 3 issues (#131 — navigate_replace REQ-RT-003; #146 — active-route awareness
   REQ-RT-005/006; #147 — nested routes REQ-RT-004) are covered by the router implementation. PR body
   correctly closes them (e.g. `Closes #131, #146, #147`).

4. **Correctness of the router code**: The underlying router implementation (REQ-RT-001..008) is functionally
   correct. The fix is minimal (import removal only) and does not regress any test. All existing passing tests
   continue to pass.

---

## Constraints

- Branch MUST be `work/ferric-router-r3`; do NOT force-push to `work/ferric-router-r2`.
- Do NOT close PR #202 manually; it will be superseded by PR #203.
- Do NOT close PR #192 manually; it will close when PR #203 merges (or when handled later).
- Router-only scope: no changes outside `crates/ferric-router/`.
- No force-push to any existing branch (including `work/ferric-router-r1` or `work/ferric-router-r2`).
- Remediation budget: this is attempt **2 of 2** (the final attempt). If CI cannot be made green, report
  clearly in SYNTHESIS.md what blocks remain and what was attempted.
- PR #203 must target `main` and must be MERGEABLE (no conflicts) when it is opened.
