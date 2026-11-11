# SYNTHESIS.md — review-ferric-router-r1

**Task:** Principal-engineer code review of PR #192  
**PR:** https://github.com/Nousix-LLC/nswe-demo/pull/192  
**Branch:** `work/ferric-router-r1` → `main`  
**Head commit:** `2bf76698c474fb60ca663f6cd074845600caea93`  
**CI run:** 41778305739 — all 6 checks PASS  
**Review posted:** https://github.com/Nousix-LLC/nswe-demo/pull/192#issuecomment-6623982987

---

## Overall Verdict: REQUEST CHANGES

The ferric-router work (four additions: `navigate_replace`, active-route awareness,
`RoutePattern::match_prefix`, `Router::nest`) is correct, well-tested, and well-documented
against its three acceptance criteria. The router work would receive APPROVE in isolation.

The PR also ships twelve commits — ~3 290 lines of `crates/ferric-macros/` (a new proc-macro
crate) and ferric context/slot/re-export changes — that the PR title, body, and stated
acceptance criteria do not describe. Those changes close issues #137–#142; the PR body closes
only #131, #146, and #147. A reviewer's approval covers all changes in a PR; approving as
written would mean approving ~3 000 lines of proc-macro code that was never presented for
review against a brief.

**Path forward:** Split the PR. The four router commits (`89687da7`, `cab18b9d`, `3868b2c8`,
`2bf76698`) close #131, #146, and #147 and can be approved immediately. The ferric-macros and
context-API commits belong in a separate PR reviewed against the acceptance criteria for
#137–#142.

---

## Per-Concern Summary

### 1. Correctness — PASS (router scope)

**What was checked:**
- `navigate_replace`: wasm path (`history.replace_state_with_url`), native path
  (`set_current_path`), reactive-signal consistency, error-path behavior (missing history
  object silently absorbed — same as `navigate`).
- Active-link awareness: `Link::build()` aria-current logic (active case, inactive case,
  strict-equality comparison, frozen `link()` signature unchanged).
- Nested routes: `RoutePattern::match_prefix` (exact-prefix, root, param capture, too-few
  segments, static mismatch), `Router::nest` signature, `outlet()` ordering (nested before
  flat), per-level fallback, flat-route regression.
- Edge cases: empty/root path with `match_prefix`, trailing-slash behavior in aria-current
  comparison.

**Found:** All three acceptance criteria are met. One correctness gap worth noting: the
`aria-current` comparison is strict string equality while `RoutePattern::match_path` ignores
trailing slashes. Not a criteria failure; tracked in issue #178.

**Severity:** No blocking correctness findings on the router scope.

---

### 2. Code quality — PASS (router scope) / NOT REVIEWED (ferric-macros)

**What was checked (router):**
- Responsibility boundaries: `RoutePattern` / `Router` / `Link` split is coherent; no
  unwarranted coupling.
- `navigate_replace` vs `navigate` duplication: minimal and intentional.
- `ChildOutlet` adapter: clean, single-purpose.
- Naming and function sizes: clear and small throughout.
- Error handling: `if let Some(history)` is consistent with `navigate`; no panic paths in the
  wasm path.

**Found (router):** No code-quality blockers in the router scope. One non-blocking note:
commit `89687da7`'s parenthetical description of issue #146 is narrower than what #146
actually covers (filed as issue #195).

**Not reviewed:** `crates/ferric-macros/src/component.rs` (929 lines), `src/lower.rs` (442
lines), `src/parser.rs` (482 lines), and the ferric context-API additions in `signal.rs`
(+163 lines) — not reviewed against the design specs for issues #137–#142. This is part of
blocking finding B1.

---

### 3. Test coverage — PASS (router scope)

**What was checked:**
- Native tests in `crates/ferric-router/src/router.rs` and `crates/ferric-router/src/link.rs`:
  nine tests covering all three acceptance criteria, the per-level fallback, the flat-route
  regression, and the aria-current dynamic toggle.
- Wasm test: `navigate_replace_does_not_grow_history` verifies `history.length` is unchanged
  after `navigate_replace`.
- Each test asserts behavior (signal values, attribute presence/absence, matched VNode
  structure), not just that something ran.

**Found:** Coverage is adequate for the stated acceptance criteria. Missing but non-blocking:
`navigate_replace` with an empty string; trailing-slash case in aria-current; `replaceState`
error path (untestable from native).

---

### 4. Security — PASS (router scope) / INCOMPLETE (ferric-macros)

**What was checked:**
- No `unsafe` blocks in `router.rs`, `matcher.rs`, `link.rs`.
- `closure.forget()` in `install_popstate_listener`: intentional, documented lifetime
  extension — same pattern as `ferric::dom`. Correct.
- No host-specific paths, internal network addresses, or server URLs in the router diff.
  Checked: `CHANGELOG.md`, `README.md`, `examples/app.rs`, all four router source files.

**Found (router):** No security findings in the router scope.

**Not reviewed:** `crates/ferric-macros/` is a new proc-macro crate introduced by this PR.
Proc-macros execute at compile time and are a first-class build-time trust-surface addition.
The proc-macro source was not reviewed against a security or design brief. This is part of
blocking finding B1.

---

### 5. Rust idioms — PASS (router scope)

**What was checked:**
- `navigate_replace` `cfg` gating: follows the same `#[cfg(target_arch = "wasm32")]`-block
  pattern as `navigate`. Idiomatic.
- `match_prefix` return type: `Option<(Params, String)>` — correct ownership (caller needs
  an owned path string for child routing).
- `Router::nest` layout type: `Box<dyn Fn(&Params, &dyn Component) -> VNode + 'static>` —
  `'static` bound correct for a Router that outlives the builder site.
- `#[must_use]` on all builder-pattern returns: consistent.
- CI `clippy -D warnings`: passes at head commit.

**Found:** No Rust-idiom findings on the router scope.

---

### 6. API/contract stability — PASS

**What was checked:**
- `ferric-router::prelude`: additive only. `navigate_replace` added; no frozen item removed
  or redefined. Prelude union matches the code-DAG SYNTHESIS.md's `prelude_union` identity.
- `ferric::prelude`: additive only. New items (`Children`, `Slot`, `SlotFn`, context
  functions, `component`, `view` macros) added; no existing item removed or redefined. `view`
  and `component` are macro names added to the wildcard prelude — a name-collision risk for
  downstream code with identically named locals, but CI (including the full app build) passes.
- `crates/chirp-frontend`, `crates/chirp-types`, `crates/chirp-server`: no files in this
  diff; existing router usage in `chirp-frontend` is unaffected.

**Found:** No API/contract stability blockers.

---

## Blocking Findings

### B1 — PR bundles ~3 290 lines of undescribed, unreviewed scope

**Where:** `crates/ferric-macros/` (3 049 lines added, new crate), `crates/ferric/src/signal.rs`
(+163 lines, context API), `crates/ferric/src/component.rs` (+34 lines, slot types),
`crates/ferric/src/lib.rs` (+13 lines, re-exports)

**Criterion:** Code quality / Security — the reviewer cannot give an informed verdict on code
that was not presented with a brief or acceptance criteria.

**Detail:** Twelve of sixteen commits add work that the PR title and body do not describe,
closing issues #137–#142. Those commits include a new proc-macro crate (`crates/ferric-macros/`)
— a build-time trust-surface addition — with ~1 955 lines of source code (component.rs, lower.rs,
parser.rs, lib.rs) that I have not reviewed against the design specs from #139–#142.

**How it maps to acceptance criteria:** Issue #131 (navigate_replace), #146 (core routing),
and #147 (active-route awareness) are covered. The ferric-macros and context-API code implements
#137–#142, which are not stated in this review brief and cannot be evaluated here.

**To resolve:** Split the PR. Router commits → dedicated router PR. ferric-macros and
context-API commits → separate PR with its own review brief covering #137–#142.

---

## Non-Blocking Findings

| ID | Finding | Issue filed |
|----|---------|-------------|
| NB1 | `navigate` / `navigate_replace` have no input validation; a non-absolute path silently updates `current_path()` to an unmatchable value. Recommend a doc-comment note or `debug_assert!` guard. | [#194](https://github.com/Nousix-LLC/nswe-demo/issues/194) |
| NB2 | `Link::build()` aria-current uses strict string equality while `RoutePattern::match_path` ignores trailing slashes. A link to `"/settings"` is not active when `current_path()` is `"/settings/"`. Design gap; deferred to issue #178. | [#178](https://github.com/Nousix-LLC/nswe-demo/issues/178) (pre-existing) |
| NB3 | Commit `89687da7` parenthetical describes issue #146 as "replace-navigation requirement" but #146 is the broader "Core routing" issue. The `Closes #146` link is correct; the description is narrower than the actual issue. | [#195](https://github.com/Nousix-LLC/nswe-demo/issues/195) |

---

## Concerns Not Fully Covered

| Concern | Reason |
|---------|--------|
| Code quality / Security / Rust idioms — `crates/ferric-macros/` proc-macro source | Not in the review brief; no design spec or acceptance criteria for #139–#141 were provided. The source was not reviewed. |
| Code quality / Rust idioms — ferric context API (`signal.rs` +163 lines) | Not in the review brief; no acceptance criteria for #142 were provided. The diff was read but not evaluated against the design. |
