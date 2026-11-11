# _BRIEF.md — ferric-router-r2 (swe-coder) — Remediation: PR split for ferric-router

**Repo**: `Nousix-LLC/nswe-demo`
**Base branch**: `main`
**Working branch**: `work/ferric-router-r2`
**Remediation attempt**: 1 of 2

---

## Background

PR #192 (`work/ferric-router-r1`) was reviewed by `review-ferric-router-r1` and received **REQUEST CHANGES**
with one blocker:

> **B1**: The PR bundles ~3,290 lines of unreviewed scope across 12 of 16 commits:
> - `crates/ferric-macros/` (new proc-macro crate: component.rs, lower.rs, parser.rs, lib.rs — 3,049 lines)
> - `crates/ferric/src/signal.rs` (+163 lines, context API additions)
> - `crates/ferric/src/component.rs` (+34 lines, slot types)
> - `crates/ferric/src/lib.rs` (+13 lines, re-exports)
>
> These files were NOT in the review brief and NOT reviewed. The proc-macro crate is a build-time
> trust-surface addition reviewed against no security or design brief.
>
> The router scope (4 commits: 89687da7, cab18b9d, 3868b2c8, 2bf76698) was fully reviewed and **PASS**:
> correctness, code quality, test coverage, security, Rust idioms, API/contract stability. It closes
> issues #131 (epic: nested routes, replace navigation, active links), #146, and #147.

PR #188 (`work/ferric-epic-authoring-r1`) was merged at commit `aa2468771eccd9e2ee79c12c79b8943fca18e07a`,
closing issues #129, #137, #138, #139, #140, #141, #142. It landed the ferric authoring model including
`crates/ferric-macros/`, `signal.rs` context API, `component.rs` slot types, and `lib.rs` re-exports
(the same ferric-macros/context scope that is bundled into PR #192).

---

## Objective

Split PR #192 so that:
1. The reviewed and passing router scope lands as a clean, focused PR (`work/ferric-router-r2`).
2. The ferric-macros/context scope is handled appropriately (see Goal 2 below).

---

## Goal 1: Create a clean router-only PR (`work/ferric-router-r2`)

### What to do
Create a new branch `work/ferric-router-r2` from `main` containing only the 4 router commits:
- `89687da7` — first router commit
- `cab18b9d` — second router commit
- `3868b2c8` — third router commit
- `2bf76698` — fourth router commit (HEAD of `work/ferric-router-r1`)

The technique: cherry-pick or rebase these 4 commits onto `main` (commit `aa2468771eccd9e2ee79c12c79b8943fca18e07a`).

### Verification
- All 6 CI jobs must pass on the new PR in `Nousix-LLC/nswe-demo`.
- The PR must close issues #131, #146, and #147 via closing keywords in the description.
- The PR must NOT include any files from `crates/ferric-macros/` or the context-API changes to `signal.rs`,
  `component.rs`, or `lib.rs` that were not part of the original `work/ferric-router-r1` base relative to
  `main` after PR #188 merged. If those files appear in the diff (because the router commits reference them),
  they must be exactly what is on `main` after `aa2468771` — not new additions.
- Close (don't just abandon) PR #192 once the new PR is open and CI is green.

### Acceptance criteria (from issues #131, #146, #147)

**#131 (epic: nested routes, replace navigation, active links):**
- Nested `<Route>` components that render their child routes in an `<Outlet>` placeholder.
- Programmatic navigation via `navigate()` / `use_navigate()` hook that replaces browser history entry.
- `<Link active_class="...">` applies the named CSS class when the link's href matches the current path.
- Router state accessible via `use_location()` hook returning the current path and query string.
- All router components and hooks exported from `ferric` crate's public API.
- CI all 6 jobs PASS.

**#146 (replace navigation):** Programmatic navigation replaces the current history entry, not pushes.

**#147 (active links):** `<Link>` accepts an `active_class` prop applied when the route matches.

---

## Goal 2: Assess and handle the ferric-macros/context scope

### Assessment required
Before creating any additional PR, determine what the ferric-macros/context scope in `work/ferric-router-r1`
adds **beyond what is already on `main`** after PR #188 merged (commit `aa2468771`).

Compare:
- `crates/ferric-macros/` diff between `work/ferric-router-r1` HEAD (`2bf76698`) and `main` (`aa2468771`)
- `crates/ferric/src/signal.rs` diff (same comparison)
- `crates/ferric/src/component.rs` diff (same comparison)
- `crates/ferric/src/lib.rs` diff (same comparison)

### Possible outcomes
1. **Nil diff (all already on main)**: The ferric-macros/context scope in PR #192 is identical to what PR #188
   landed. In this case no additional PR is needed. Record this finding explicitly in `SYNTHESIS.md`.
2. **Non-nil diff (new code beyond main)**: The router commits added new content to these files beyond what
   was in PR #188. In this case create a separate PR for that incremental scope, with CI passing and a brief
   description of what it adds and what issues it relates to (if any). Note: issues #137–#142 were closed by
   PR #188 — do not duplicate-close them. File new issues if the incremental scope is not already tracked.

---

## Declared output

- Branch `work/ferric-router-r2` with the 4 router commits cherry-picked/rebased onto `main`.
- PR in `Nousix-LLC/nswe-demo` targeting `main` from `work/ferric-router-r2`, closing #131, #146, #147.
- PR #192 closed (not merged — replaced by the new PR).
- All 6 CI jobs passing on the new PR.
- If Goal 2 finds new code: a second PR for the ferric-macros/context scope increment, CI passing.
- If Goal 2 finds nil diff: explicit statement in `SYNTHESIS.md`.
- Root `SYNTHESIS.md` accounting for all goals:
  - Goal 1: PR URL, CI status, issues closed.
  - Goal 2: diff outcome (nil or non-nil), disposition.
  - Machine gate verdict: PASS if Goal 1 CI passes; FAIL otherwise.

---

## Constraints

- Repo: `Nousix-LLC/nswe-demo` only. No other repos.
- No force-push to `main`.
- No inline fix of the ferric-macros code — assess only; if new code is found, a PR is the deliverable.
- The router scope (4 commits) is already reviewed and PASS. No re-implementation needed; cherry-pick or
  rebase is the correct operation.
- `work/ferric-router-r2` must be rebased on `main` at `aa2468771eccd9e2ee79c12c79b8943fca18e07a` or
  later (whatever `main` HEAD is at time of execution — confirm with `git log main -1`).
- Non-blockers from the previous review (#194, #195) are on the board as follow-up issues and do NOT need
  to be fixed in this PR. They are tracked separately.
