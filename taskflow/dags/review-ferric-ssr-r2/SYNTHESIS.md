# Review: PR #228 — ferric-ssr-r2 Re-Review

**Repository**: Nousix-LLC/nswe-demo  
**Branch**: `work/ferric-ssr-r1`  
**Commits reviewed**: `7fb90c7`, `e625c3f`, `75c1eef`  
**Pinned commit**: `75c1eef`

---

## Verdict: APPROVE

Both blockers from review-ferric-ssr-r1 are resolved. Nine regression criteria hold. Security is clean. Three non-blocker observations are noted below; none gates the approval.

---

## Synthesis Gate Result

| Check | Result | Evidence |
|---|---|---|
| Contract coverage | PASS | All in-scope requirements appear in at least one spoke verdict |
| Wiring / no dead verdicts | PASS | All three verdict files contain substantive evidence with file/commit/line citations |
| Dedup / no contradictions | PASS | REQ-SSR-005 and `has_child_nodes()` appear in multiple spokes; analyses are complementary, not contradictory |
| Code review of combined output | PASS | No block-severity finding; three Note/Non-blocker observations listed below |

---

## B1 — REQ-HYD-003 (`hydrate()` wiring)

**RESOLVED.**

`app.rs` at `75c1eef` (lines 154–161) calls `ferric::hydrate(root, app)` when `root.has_child_nodes()` returns `true` on the wasm32 target, and falls back to `mount(root, app)` otherwise. The `#[cfg(target_arch = "wasm32")]` gate is correctly placed: `ferric::hydrate` is a wasm32-only export (re-exported conditionally in `crates/ferric/src/lib.rs`), so the gate keeps native `cargo test` and `cargo clippy --all-targets` clean while preserving the conditional for wasm builds.

`ferric::hydrate` (`crates/ferric/src/hydrate.rs`, same commit) is the full hydration path: adopt-walk to wire existing DOM nodes to the VNode tree, sentinel-comment cleanup, and reactive-effect setup for subsequent signal-driven re-renders. Prior to `7fb90c7`, `start()` called `mount` unconditionally; after `75c1eef`, the SSR path routes to `hydrate` with no residual gap.

No findings on B1.

---

## B2 — REQ-SSR-006 (`wasm-bindgen-test` coverage)

**RESOLVED.**

`crates/ferric/tests/hydrate_wasm.rs` (197 lines, commits `e625c3f`/`75c1eef`) contains three `#[wasm_bindgen_test]` functions with `wasm_bindgen_test_configure!(run_in_browser)`:

| Test | REQ | What it asserts |
|------|-----|----------------|
| `hydrate_adopt_walk_no_structural_mutations` | REQ-SSR-004 | `is_same_node()` before/after hydration — a recreated node fails the assertion |
| `hydrate_event_wiring_post_hydration` | REQ-SSR-005 | `text_content() == Some("1")` after click; `is_same_node()` on the button — broken event wiring or replace-instead-of-patch each fail a different assertion |
| `hydrate_mismatch_detection_recovery` | REQ-SSR-006 | `tag_name().to_lowercase() == "p"` after deliberate `<div>` vs `<p>` mismatch — passes only if `replace_child` executes |

Each test isolates its container via a `cleanup()` call. `wasm` CI job (run 42120246308, job 127570408865) passed at `75c1eef`.

One note-level observation from B2 (see Non-Blockers, NB-2).

---

## Regression Check

All 9 previously-clean criteria hold at `75c1eef`:

| Requirement | Location verified | Outcome |
|---|---|---|
| REQ-SSR-001 | `crates/ferric/src/ssr.rs` import list | Clean — no `web_sys`/`wasm_bindgen` added |
| REQ-SSR-002 | `signal.rs:502` `impl Drop for ReactiveScope`; `chirp-server/src/ssr.rs` `ssr_handler` closure | Clean — subscriptions purged; no `create_signal` in handler |
| REQ-SSR-003 | `ssr.rs` `render_node` recursion | Clean — no depth counter added |
| REQ-SSR-004 | `hydrate.rs` `adopt_vnode` match path | Clean — no `createElement` on matching-tag branch (also covered by B2 test) |
| REQ-SSR-005 | `ferric/src/lib.rs` re-export; `chirp-server/src/ssr.rs` call site | Clean — unconditional re-export present |
| REQ-HYD-001 | `hydrate.rs` `adopt_vnode` | Clean — `set_events` and `adopt_children` called without creating new nodes |
| REQ-HYD-002 | `hydrate.rs` `hydrate`; `app.rs` `start()` | Clean — effect-based reactive updates intact; one Note on predicate precision (NB-1) |
| REQ-HYD-004 | `hydrate.rs` marker imports | Clean — single import from `ssr`, no local copies |
| REQ-MIS-001 | `chirp-server/src/ssr.rs` `assemble_document` | Clean — `escape_html` output fed to format string; ferric `ssr.rs` change is docstring-only |
| REQ-MIS-002 | `hydrate.rs` mismatch recovery paths | Clean — node-scoped replacement, no structural corruption; one Non-blocker on test completeness (NB-3) |

---

## Security

No security findings.

**Surfaces checked:**

- **HTML injection** (`crates/ferric/src/ssr.rs`, `75c1eef`): `escape_html` covers all five injection-risky characters (`<>&"'`) for both text-content and attribute-value contexts. Tag and attribute names are developer-controlled static values.
- **DOM spoofing** (`app.rs:154–161`, `75c1eef`): `has_child_nodes()` is not a security boundary. Triggering the hydration path via injected nodes requires prior XSS, which already grants capabilities beyond this branch. No new attack vector.
- **Test injection safety** (`hydrate_wasm.rs`, `75c1eef`): All `set_inner_html` calls use hardcoded literals. The only non-literal DOM value is a typed `i32` constant. No `#[wasm_bindgen]` export provides an external callable surface.

---

## Code Quality

No new instances of patterns #229–#242 in the ferric-ssr-r4 commits (`7fb90c7`, `e625c3f`, `75c1eef`).

**Surfaces checked on `app.rs` new code**: branch logic readability, dead-code reachability under each cfg gate, cfg gate coverage and complementarity, comment accuracy on the cfg rationale and `#app` acquisition. All clean.

**Surfaces checked on `hydrate_wasm.rs` new code**: helper naming and role separation (`document()`, `make_container()`, `cleanup()`), behavioral specificity of assertions per test, copy-paste divergence between test bodies. All clean.

Three non-blocker observations are noted below.

---

## Non-Blockers

None blocks APPROVE. Each warrants a follow-on ticket.

**NB-1 (Note) — `has_child_nodes()` predicate precision**  
`crates/chirp-frontend/src/app.rs:154`, commit `75c1eef`, REQ-HYD-002.  
`Element::has_child_nodes()` returns `true` for whitespace text nodes and HTML comment nodes, not only element-node children produced by SSR markup. If `#app` contains a whitespace or comment node on a non-SSR page, the wasm32 path calls `ferric::hydrate` with that root, which treats the mismatch as a recovery case. The fix is either to tighten the predicate to `root.first_element_child().is_some()` (true only for element-node children) or to document at the call site that `#app` must be completely empty when SSR is not in use.

**NB-2 (Note) — missing `console.warn` assertion in `hydrate_mismatch_detection_recovery`**  
`crates/ferric/tests/hydrate_wasm.rs`, `hydrate_mismatch_detection_recovery`, commit `75c1eef`, REQ-SSR-009.  
`emit_mismatch_warning()` executes in this test run (debug builds), but the test does not assert it was called. If the warning were removed or silenced, this test would still pass. Adding a `console.warn` stub — installed before calling `hydrate()`, asserted after — would catch that regression. Out of scope for the B2 blocker; leaves REQ-SSR-009 without coverage.

**NB-3 (Non-blocker) — `hydrate_mismatch_detection_recovery` missing `text_content()` assertion**  
`crates/ferric/tests/hydrate_wasm.rs:185–189`, commit `75c1eef`, REQ-MIS-002 / REQ-SSR-006.  
The test asserts `tag_name().to_lowercase() == "p"` after recovery, confirming the element was replaced. It does not check `text_content()`. A regression that replaces `<div>text</div>` with an empty `<p>` would pass the current assertion while content fidelity after mismatch recovery is broken. Adding `assert_eq!(el.text_content().as_deref(), Some("text"), "REQ-SSR-006: recovered <p> missing text content")` after the `tag_name` assertion would close this.

---

## CI

Run https://github.com/Nousix-LLC/nswe-demo/actions/runs/42120246308 — **PASS** (7 checks) at commit `75c1eef`. Jobs include `fmt`, `clippy`, `test`, `wasm`, `doc`, `image`. Annotation notices (Node.js 20 deprecation, ubuntu-latest runner migration) are infrastructure notices, not test failures.
