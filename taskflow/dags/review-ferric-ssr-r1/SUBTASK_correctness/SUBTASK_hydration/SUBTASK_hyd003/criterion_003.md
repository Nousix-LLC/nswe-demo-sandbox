# REQ-HYD-003 — hydrate() Called Once From WASM Entry Point

**Status**: FINDING (BLOCKER)

**What was checked**:

1. **WASM entry point** — `crates/chirp-frontend/examples/chirp.rs` (`fn main()`) and
   `crates/chirp-frontend/src/app.rs` (`pub fn start()`). These are the functions that run when
   the WASM bundle initializes in the browser. Neither file is modified by PR #228.

2. **`ferric::hydrate()` implementation** — `crates/ferric/src/hydrate.rs` (new in PR #228).
   The function exists, is correctly implemented (adopt pass + sentinel cleanup + reactive effect
   loop), and is re-exported from `crates/ferric/src/lib.rs` as a `wasm32`-only public item.

3. **Server-side assembly** — `crates/chirp-server/src/ssr.rs` (new in PR #228). The
   `assemble_document` function emits `<script type="module" src="{wasm_script_path}"></script>`,
   loading `/pkg/chirp.js` as an ES module. The `ssr_handler` calls `render_to_string` and
   `assemble_document`.

4. **The connection between the WASM bundle and `hydrate()`** — traced the full call chain from
   `chirp.rs:fn main()` through `chirp_frontend::start()` to the actual DOM interaction.

5. **Integration tests and demos** — searched all files touched by PR #228 and the full branch
   tree for `wasm_bindgen_test`, integration test harnesses, and E2E demos exercising the
   SSR→hydrate path.

---

## Finding 1 — hydrate() is not called from the WASM entry point [BLOCKER]

**Evidence**:
- `crates/chirp-frontend/examples/chirp.rs:16` — the binary entry point:
  ```rust
  fn main() {
      chirp_frontend::start();
  }
  ```
- `crates/chirp-frontend/src/app.rs` (the `start()` body, lines ~114–135) — `start()` calls
  `mount(root, app)`, not `ferric::hydrate(root, app)`.
- PR #228 does **not** modify `crates/chirp-frontend/examples/chirp.rs` or
  `crates/chirp-frontend/src/app.rs`. The diff touches only:
  `Cargo.lock`, `crates/chirp-server/Cargo.toml`, `crates/chirp-server/src/api/router.rs`,
  `crates/chirp-server/src/lib.rs`, `crates/chirp-server/src/ssr.rs`,
  `crates/ferric/src/hydrate.rs`, `crates/ferric/src/lib.rs`, `crates/ferric/src/ssr.rs`.

**What this means**: When the browser loads the SSR page produced by `ssr_handler`, the
`<script type="module" src="/pkg/chirp.js">` tag loads the WASM bundle. That bundle's start
function calls `chirp_frontend::start()`, which calls `ferric::dom::mount()`. `mount()` creates
a new reactive tree and **replaces** the existing DOM under `#app` with client-rendered content —
it does not adopt the server-rendered markup. `ferric::hydrate()` is never called.

The PR therefore delivers two things that cannot cooperate: a correct `hydrate()` function and
a correct SSR document shell, but no wiring between them. The SSR+hydration feature is not
functional end-to-end: every SSR page load degrades to a client-side re-render (REQ-SSR-004,
zero structural mutations during hydration, is violated at runtime even though the
`hydrate()` implementation satisfies it in isolation).

**False docstring**: `crates/chirp-server/src/ssr.rs:141` asserts "the WASM bundle initialises
and calls `ferric::hydrate` after the document is parsed." This is incorrect given the current
entry point.

**What satisfies this finding**: A change to `crates/chirp-frontend/src/app.rs::start()` (or a
new `start_ssr()` variant) that calls `ferric::hydrate(root, app_closure)` when the page already
contains server-rendered markup in `#app`, together with the corresponding wiring update to
`chirp.rs` and correction of the `ssr.rs` docstring.

---

## Finding 2 — No integration test or demo exercises the SSR→hydrate path [NON-BLOCKER]

**Evidence**: Searched the full diff and branch tree for `wasm_bindgen_test`, integration test
harnesses, and demo files. No test exercises the sequence: `render_to_string` → deliver HTML →
load WASM bundle → `hydrate()` → assert DOM unchanged. The tests that do exist are:
- `crates/chirp-server/src/ssr.rs` `#[cfg(test)]` — unit tests for `assemble_document` (pure
  string output; no WASM load, no `hydrate()` call)
- `crates/ferric/src/ssr.rs` `#[cfg(test)]` — unit tests for `render_to_string` output
- No `wasm_bindgen_test` harness in the diff or in `crates/ferric/tests/`

This is a non-blocker in isolation (CI passing is the floor, and the entry-point wiring blocker
above already prevents landing), but the absence means the fixed entry-point wiring will also
ship without an end-to-end test catching future regressions of this exact failure mode.

**What satisfies this finding**: A `wasm_bindgen_test` test (or Playwright / headless-browser
E2E test) that calls `render_to_string`, inserts the HTML into a test DOM, calls `hydrate()`,
and asserts that the DOM nodes are the same objects before and after (zero structural mutations).

---

## What was clean

- **`hydrate()` implementation** (`crates/ferric/src/hydrate.rs`): the adopt pass, sentinel
  cleanup, and reactive-effect wiring are all correctly implemented. The function is `wasm32`-
  gated, re-exported cleanly, and handles mismatch recovery with appropriate `console.warn`
  diagnostics in debug builds.
- **`assemble_document` / `ssr_handler`** (`crates/chirp-server/src/ssr.rs`): the HTML shell
  shape (doctype, charset, `#app` container, ES-module script tag) matches the design spec.
  The debug-only `assert!` on `wasm_script_path` quoting prevents attribute injection. Unit
  tests cover the structure, the empty-HTML case, and the quote-injection guard.
- **Module layout**: `ferric/src/lib.rs` correctly gates `hydrate` on `target_arch = "wasm32"`
  and keeps `ssr` unconditional, matching the stated design constraint that `ssr` must compile
  natively.
