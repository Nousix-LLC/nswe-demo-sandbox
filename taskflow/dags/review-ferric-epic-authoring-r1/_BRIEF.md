# _BRIEF.md — review-ferric-epic-authoring-r1 (swe-reviewer)

**Repo:** `Nousix-LLC/nswe-demo`
**DAG kind:** PR review
**Branch under review:** `work/ferric-epic-authoring-r1`, tip `e29e2f4`
**Root SYNTHESIS.md path:** `taskflow/dags/review-ferric-epic-authoring-r1/SYNTHESIS.md`

---

## Target

**PR #188**: `feat(ferric): Ferric 1.0 Authoring Model — view!, components, context (#129)`
- Branch: `work/ferric-epic-authoring-r1`, tip commit `e29e2f4`
- Status: OPEN, MERGEABLE, all 6 CI jobs PASS (run 41743675354: fmt ✅, clippy ✅, test ✅, wasm ✅, doc ✅, image ✅)
- Closes: #129 (epic), #137, #138, #139, #140, #141, #142

**Issues and their acceptance criteria:**

**#129 — Ferric 1.0 Authoring Model (epic, `usable_early`)**
Integration goal: a developer can build a Ferric WASM app using reactive signals, a virtual DOM, the view! macro, the component model (props / children / slots / dyn dispatch), compile-time diagnostics for component misuse, and the context API — with the counter.rs example unchanged (backward compatibility).

**#137 — Reactive signal model**
- AC: `Signal<T>`, `Computed<T>`, `Effect` are publicly usable from `ferric::prelude`
- AC: `Signal::set` triggers downstream effects
- AC: Effects re-run on signal change and not spuriously
- AC: Memo (`Computed`) reuses its cached value when the upstream is unchanged

**#138 — Virtual DOM and DOM patching**
- AC: `VNode` tree maps to real DOM nodes via `wasm-bindgen`/`web-sys`
- AC: Patching updates only changed nodes (structural diff)
- AC: Keyed lists are reordered without full re-render
- AC: Batch coalescing: multiple signal writes in one tick produce one patch pass

**#139 — view! macro (§2.12 constructs)**
- AC: view! lowers all 8 constructs from the §2.12 lowering table: element nodes, text interpolation, attribute binding, event handlers, conditional rendering (`if`/`if-else`), list rendering (`for`), component invocation, and slot fill
- AC: §2.9 error cases produce correct compile-time diagnostics (trybuild fixtures filed as follow-up #189 — absent fixtures are a coverage gap, not a functional regression)
- AC: `counter.rs` example compiles and passes its test unchanged (IA4)

**#140 — Component model (props, children, slots, dyn dispatch)**
- AC: Components accept typed props via a `#[derive(Props)]`-like mechanism
- AC: Components accept children via a `children` slot
- AC: Named slot fills work: `<Slot name="header" />`
- AC: Slot fill constraints are enforced (no fill for an undeclared slot)
- AC: Dynamic dispatch via a component trait object compiles and runs

**#141 — Component type-level diagnostics**
- AC: Passing wrong prop types is a compile error with a clear message
- AC: Missing required props is a compile error
- AC: Trybuild fixtures in `crates/ferric-macros/tests/compile_fail_component/` present and passing (T04)

**#142 — Context API**
- AC: `provide_context` / `use_context` thread context values through the component tree
- AC: Context shadowing: a child provider shadows the parent for its subtree
- AC: `use_context` returns `None` when no provider is in scope (not a panic)
- AC: Signal write after mount triggers a reactive re-render

**Design:** PR #128 (`design: Ferric 1.0 framework design`) merged. Design documents at `design/ferric/` on `main`.

**Code DAG synthesis:** `taskflow/dags/ferric-epic-authoring-r1/SYNTHESIS.md`
Verdict: PARTIAL — all functional ACs met; IA6 gap: view! §2.9 trybuild fixtures from T02 were never committed (follow-up issue #189 filed on board Todo). All 6 CI jobs PASS on `e29e2f4`.

---

## Review concerns

Review the change as a whole, held issue by issue to its acceptance criteria. Cover each concern below.

### 1. Correctness
Does the diff implement each acceptance criterion of the 6 sub-issues (#137–#142) and the epic's integration goal (#129)?

Specific checks:
- Reactive signals: `Signal<T>`/`Computed<T>`/`Effect` exported from `ferric::prelude`; `Signal::set` triggers effects; effects don't re-run spuriously; memo reuses cached value under unchanged output.
- Virtual DOM / DOM patching: `VNode` maps to DOM; structural diff patches only changed nodes; keyed-list reorder works; batch coalescing produces one patch pass for multiple writes in one tick.
- view! macro lowering: all 8 §2.12 constructs lower correctly; `counter.rs` example unchanged and passing (backward compat, IA4).
- Component model: typed props accepted; children slot works; named slots fill and their constraints enforced; dyn dispatch compiles and runs.
- Component diagnostics: wrong prop types and missing required props are compile errors with clear messages; trybuild fixtures present and passing (T04 component fixtures, `crates/ferric-macros/tests/compile_fail_component/`).
- Context API: `provide_context`/`use_context` thread values through the tree; context shadowing; `use_context` returns `None` when no provider; signal write after mount triggers re-render.
- Edge cases: memo memoization under unchanged output; batch coalescing; keyed-list reorder; slot fill constraints; context shadowing; signal write after mount.

### 2. Code quality and design
Responsibilities and coupling across `crates/ferric` and `crates/ferric-macros`; abstraction boundaries (macro / runtime seam; component trait surface; signal/scope lifecycle); duplication; naming; function size (note: `build_panic_builder` suppression in the diff — `#[allow(clippy::too_many_arguments)]`). Does the code leave the ferric internals easier to extend?

### 3. Test coverage and depth
Does the test suite exercise each AC and the edge/error paths? Do the tests assert real behavior (not vacuous pass)? Unit tests in `crates/ferric`; proc-macro tests in `crates/ferric-macros/tests/lowering.rs` and `component.rs`; trybuild suite in `crates/ferric-macros/tests/compile_fail_component/` (T04).

Note the IA6 gap: view! §2.9 trybuild fixtures are absent (follow-up issue #189 filed). Assess whether the absent fixtures constitute a blocker for landing, or whether the functional coverage and T04 component diagnostic fixtures make it an acceptable tracked gap.

### 4. Security
Input handling in the proc-macro (untrusted token streams from user code); `unsafe` / FFI boundaries (wasm-bindgen, web-sys); any host-specific or internal infrastructure detail committed to the diff (absolute host paths, private network addresses such as `100.x` tailnet IPs or LAN IPs, internal server URLs, host runtime or taskflow directory paths, internal credentials or tokens).

### 5. Rust idiom and API surface
Proc-macro hygiene (identifier collision avoidance, span hygiene); `pub` surface of `ferric::prelude` additions; `#[allow(dead_code)]` and `#[allow(clippy::too_many_arguments)]` suppressions (acceptable short-term deferral or blocker?); backward compatibility (`counter.rs` example unchanged — IA4).

### 6. API/contract stability
The diff extends `ferric::prelude` and introduces a new crate `ferric-macros`. Verify that the additions are additive only and do not break the existing public API. Check the new crate's pub surface for inadvertent leakage.

---

## Declared output

1. **A review posted on PR #188** as a GitHub comment carrying the verdict and findings. If the platform will not permit a formal approval (same-account author/reviewer), post the review as a comment with the verdict (APPROVE or REQUEST-CHANGES) and the concern-by-concern findings.
2. **Root `SYNTHESIS.md`** at `taskflow/dags/review-ferric-epic-authoring-r1/SYNTHESIS.md` with:
   - Overall verdict: APPROVE or REQUEST-CHANGES
   - Per-concern account: what each concern checked, what it found clean, and any findings (severity + whether blocks)
   - Explicit IA6 assessment: blocker or tracked gap?
3. **Non-blocking findings** filed as grouped, linked backlog issues on `Nousix-LLC/nswe-demo`, de-duplicated against existing issues. Each issue: descriptive title, severity, the PR and concern it came from, placed in the backlog.

Findings point at files and lines in the repository. Nothing in the posted review or filed issues names host paths, internal network addresses, or DAG-internal paths.

---

## Constraints

- Repo: `Nousix-LLC/nswe-demo`
- Read-only: do not push to `work/ferric-epic-authoring-r1` or any branch
- Review tip commit: `e29e2f4` on branch `work/ferric-epic-authoring-r1`
- Do not name host paths, tailnet IPs, internal server URLs, or taskflow internals in any GitHub output
