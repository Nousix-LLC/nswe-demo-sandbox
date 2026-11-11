# Review Synthesis — PR #228 ferric SSR/hydration

## Verdict

**REQUEST-CHANGES**

Two distinct blockers prevent landing. Both must be resolved and re-reviewed before this PR merges.

---

## Concern-by-Concern Account

### 1. Correctness

**What was checked**: All eleven in-scope acceptance criteria from issues #223 (REQ-SSR-001 through REQ-SSR-005), #224 (REQ-HYD-001 through REQ-HYD-004), and #226 (REQ-SSR-006, REQ-MIS-001, REQ-MIS-002). REQ-SSR-007 / #225 was confirmed as a non-goal and is explicitly absent from review scope.

**Findings**:

**BLOCKER — REQ-HYD-003**: `hydrate()` is never called from the WASM entry point. `crates/chirp-frontend/src/app.rs::start()` calls `ferric::dom::mount(root, app)`, not `ferric::hydrate(root, app)`. PR #228 does not modify `crates/chirp-frontend/examples/chirp.rs` or `crates/chirp-frontend/src/app.rs`. The SSR+hydration feature is not functional end-to-end: every page load degrades to a client-side re-render. A secondary docstring at `crates/chirp-server/src/ssr.rs:141` asserts hydrate is called; it is not.

**BLOCKER — REQ-SSR-006**: No `wasm-bindgen-test` exists for the mismatch detection, warning, or recovery code paths. `crates/ferric/src/hydrate.rs` (466 lines) has no `#[cfg(test)]` block; `crates/ferric/tests/` does not exist on this branch. Issues #224 and #226 (both `release-gating: true`) explicitly require headless `wasm-bindgen-test` coverage. CI passing on `ssr.rs` tests does not satisfy this — those cover server-render output, not hydration or mismatch paths.

**NON-BLOCKER — REQ-SSR-002**: The `subscriber_count == 0` invariant from the acceptance criterion is not directly asserted in the SSR test suite (filed as #239).

**NON-BLOCKER — REQ-SSR-005**: Two stale comments in `chirp-server/src/ssr.rs` describe `render_to_string` as a stub that panics via `todo!()`. Filed as #229.

**NON-BLOCKER — REQ-HYD-002**: No `wasm-bindgen-test` for the hydrate→signal→DOM update sequence. This gap is subsumed by Blocker 2 (the full absence of wasm-bindgen-test for hydrate.rs).

**NON-BLOCKER — REQ-MIS-001**: Stale comment at `crates/chirp-server/src/ssr.rs:165–168` also references the stub. Filed as #229 (same issue as REQ-SSR-005 stale comment).

**NON-BLOCKER — REQ-SSR-006 (secondary)**: Extra DOM nodes beyond the VNode child list are warned but not removed in `adopt_children`. After `strip_sentinels`, the live DOM contains more children than the VNode tree expects. Filed as #240.

**Clean (9 of 11 criteria)**:
- REQ-SSR-001: `render_to_string` has no `web_sys` or DOM dependency; compiles and runs on native.
- REQ-SSR-002 (mechanism): Reactive scope isolation is correct; `impl Drop for ReactiveScope` purges all subscribers.
- REQ-SSR-003: Nested VNode recursion is unbounded and exercised.
- REQ-SSR-004: Marker constants defined once in `ssr.rs`, imported (not copied) by `hydrate.rs`.
- REQ-SSR-005 (code path): `render_to_string` is a crate-root export, dependency ungated, `ssr_handler` calls correctly.
- REQ-HYD-001: Adopt pass casts existing DOM nodes; no `createElement` on matching paths.
- REQ-HYD-002 (mechanism): Reactive update path uses `create_effect` → `diff` → `apply_patches_impl`, same as `dom::mount`.
- REQ-HYD-004: Marker format consistency enforced at the type level — single import, no local copies.
- REQ-MIS-002: `assemble_document` produces a valid HTML5 document; BAR-005 placeholder is a well-formed comment.

---

### 2. Code Quality and Design

**What was checked**: Public API surface and naming consistency (Area A), abstraction boundary between SSR (native) and DOM (wasm32) modules (Area B), error handling choices in `hydrate.rs` and `chirp-server/src/ssr.rs` (Area C), function sizes and duplication between `hydrate.rs` and `dom.rs` (Area D), test coverage for the hydration path (Area E), documentation for new public items (Area F).

**Findings**:

**BLOCKER — Area E**: Zero tests in `hydrate.rs`; issues #224 and #226 require `wasm-bindgen-test`. (Same underlying gap as REQ-SSR-006 correctness blocker — one fix resolves both.)

**NON-BLOCKER — Area A (Finding 1)**: `ferric::hydrate` names both a module and a crate-root function. `use ferric::hydrate;` imports the module, not the function. Filed as #230.

**NON-BLOCKER — Area A (Finding 2)**: `chirp_server::ssr::ssr_handler` stutters the module name; Rust API Guideline C-WORD-ORDER recommends `handler`. Filed as #231.

**NON-BLOCKER — Area B**: `pub mod dom;` lacks the `#[cfg(target_arch = "wasm32")]` gate that `pub mod hydrate;` correctly carries. Now that `ferric` is a native server dependency, `ferric::dom::mount` is silently callable from `chirp-server` and would panic at runtime. Filed as #232.

**NON-BLOCKER — Area C (Finding 1)**: `strip_sentinels` discards `remove_child` result with `let _ =` on a correctness-critical operation. Filed as #233.

**NON-BLOCKER — Area C (Finding 2)**: `assemble_document` injection guard is `debug_assert!`, stripped in release builds, covers only `"`. Filed as #234.

**NON-BLOCKER — Area D (Finding 1)**: Seven private helpers duplicated between `hydrate.rs` and `dom.rs`; next edit must land in both; two divergence paths are silent. Filed as #235.

**NON-BLOCKER — Area D (Finding 2)**: `render_to_string` signature has no seam for async resource injection (#130). Filed as #236.

**NON-BLOCKER — Area F (Finding 1)**: `hydrate()` missing calling contract (must call after SSR HTML is in DOM); no usage example. Filed as #237.

**NON-BLOCKER — Area F (Finding 2)**: `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER` missing stability note. Filed as #238.

**Clean**: The SSR render path (`render_to_string`, `escape_html`, `render_node`) is well-factored and thoroughly tested (13 unit tests). `assemble_document` and `ssr_handler` documentation is adequate for first-time callers. Function sizes are appropriate throughout. Closure bounds (`FnOnce` for `render_to_string`, `Fn + 'static` for `hydrate`) are as permissive as the implementations allow. New exports are correctly excluded from the frozen `prelude`.

---

### 3. Security — HTML Escaping

**What was checked**: Text node escaping, attribute value escaping, attribute name handling, raw HTML insertions via `format!`/`push_str`, and test coverage for escaping regressions in both `crates/ferric/src/ssr.rs` and `crates/chirp-server/src/ssr.rs`.

**Verdict: PASS** — no blocking findings.

**NON-BLOCKER — `wasm_script_path` insertion**: `assemble_document` inserts `wasm_script_path` into an HTML `src` attribute without escaping; only a `debug_assert!` guards against `"`, stripped in release builds. The current caller is not exploitable (hardcoded literal). Filed as #234 (same as Area C Finding 2 above).

**NON-BLOCKER — attribute names**: `render_node` does not escape attribute names; `VElement::attr` accepts any `Into<String>`, creating no type-level barrier against future misuse. Filed as #241.

**NON-BLOCKER — test gaps**: No end-to-end injection test through `assemble_document`; no release-build test for `wasm_script_path` with metacharacters beyond `"`. Filed as #242.

**Clean**: `escape_html` covers all five injection characters (`<`, `>`, `&`, `"`, `'`). Both text node content and attribute values go through `escape_html` without exception. `server_html` raw insertion in `assemble_document` is intentional — all user data was escaped by `render_node` before this point, documented in the function's doc comment. `hydrate.rs` format strings (`emit_mismatch_warning`) go to `console.warn`, not to the HTML output. Existing escaping tests would catch a regression in the core paths.

---

### 4. Security — Infrastructure Exposure

**What was checked**: All added lines in all eight changed files for host filesystem paths, Tailscale and LAN IP addresses, credentials and secrets (API keys, tokens, passwords, SSH markers), and new external supply-chain additions in `Cargo.toml` / `Cargo.lock`.

**Verdict: PASS** — no findings.

**Clean**: No host paths, IP addresses, credentials, or external supply-chain additions. The only Cargo change is `ferric = { path = "../ferric" }` in `crates/chirp-server/Cargo.toml` — a workspace-local path dependency on a sibling crate. No external packages enter the dependency graph.

---

## Blockers

Two blockers must be resolved before landing:

**Blocker 1 — REQ-HYD-003 (wiring gap)**

`hydrate()` is never called from the WASM entry point. `crates/chirp-frontend/src/app.rs::start()` calls `ferric::dom::mount(root, app)`, not `ferric::hydrate(root, app)`.

What satisfies this:
- Change `crates/chirp-frontend/src/app.rs::start()` (or add a new `start_ssr()` variant) to call `ferric::hydrate(root, app_closure)` when the page contains server-rendered markup in `#app`.
- Update the entry-point wiring in `crates/chirp-frontend/examples/chirp.rs`.
- Correct the false docstring at `crates/chirp-server/src/ssr.rs:141`.

**Blocker 2 — REQ-SSR-006 / Area E (missing wasm-bindgen-test)**

`crates/ferric/src/hydrate.rs` has no tests. Issues #224 and #226 require headless `wasm-bindgen-test` coverage.

What satisfies this:
1. A `wasm-bindgen-test` for the adopt walk (REQ-SSR-004 / #224): hydrate a component against SSR-rendered DOM; confirm zero structural mutations.
2. A `wasm-bindgen-test` for event wiring (REQ-SSR-005 / #224): after hydration, dispatch a click; assert DOM updates via signal/patch path; element not recreated.
3. A `wasm-bindgen-test` for mismatch detection (REQ-SSR-006 / #226): hydrate against a deliberately mismatched server DOM; assert `console.warn` fired; assert live DOM matches client render; assert siblings remain adopted.

Tests runnable via `wasm-pack test --headless` or `cargo test --target wasm32-unknown-unknown` with `wasm-bindgen-test-runner`. PR identity table must include `wasm-tests-pass: ✅` before merge.

---

## Non-Blocking Findings Filed as Issues

All fourteen non-blocking findings are new (no duplicates found on the board as of 2026-11-04).

| # | Finding | Severity | Issue |
|---|---------|----------|-------|
| NB-01 | Stale todo-panic comments in `chirp-server/src/ssr.rs` (two locations) | NON-BLOCKER | #229 |
| NB-02 | `ferric::hydrate` naming collision — module and function share crate-root path | NON-BLOCKER | #230 |
| NB-03 | `ssr_handler` stutters module name; idiomatic name is `handler` | NON-BLOCKER | #231 |
| NB-04 | `pub mod dom;` missing `#[cfg(target_arch = "wasm32")]` gate | NON-BLOCKER | #232 |
| NB-05 | `strip_sentinels` silently discards `remove_child` result with `let _ =` | NON-BLOCKER | #233 |
| NB-06 | `wasm_script_path` insertion uses `debug_assert!` stripped in release; covers only `"` | NON-BLOCKER | #234 |
| NB-07 | Seven private helpers duplicated between `hydrate.rs` and `dom.rs` | NON-BLOCKER | #235 |
| NB-08 | `render_to_string` signature has no seam for async resource injection (#130) | NON-BLOCKER | #236 |
| NB-09 | `hydrate()` doc missing calling contract (must call after SSR HTML is in DOM) | NON-BLOCKER | #237 |
| NB-10 | `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER` missing stability note | NON-BLOCKER | #238 |
| NB-11 | Missing `subscriber_count == 0` assertion in SSR isolation tests | NON-BLOCKER | #239 |
| NB-12 | `adopt_children` warns on trailing DOM nodes but does not remove them | NON-BLOCKER | #240 |
| NB-13 | Attribute names not HTML-escaped; convention undocumented | NON-BLOCKER | #241 |
| NB-14 | No end-to-end injection test through `assemble_document`; no release-build test for `wasm_script_path` metacharacters | NON-BLOCKER | #242 |

---

## Review Gaps

**Label discrepancy**: Issue #226 and `crates/ferric/src/hydrate.rs:11` label the mismatch criterion REQ-SSR-009. The subtree spec uses REQ-SSR-006 for the same criterion. This review used REQ-SSR-006 (spec label). The discrepancy should be resolved before closing #226.

No other review gaps. All eleven in-scope acceptance criteria have named findings (clean or finding) in `SUBTASK_correctness/correctness_findings.md`.

---

## GitHub Review

Formal review status blocked by GitHub same-account restriction. Review posted as a comment carrying the verdict:

https://github.com/Nousix-LLC/nswe-demo/pull/228#issuecomment-6647644348

This SYNTHESIS.md is the authoritative landing decision: **REQUEST-CHANGES**. The two blockers above must be resolved before this PR merges.
