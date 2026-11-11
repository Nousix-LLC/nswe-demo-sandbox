## Setup/teardown and DOM cleanup

**Severity**: Warning
**Evidence**: hydrate_wasm.rs:97, 158, 194 (cleanup calls); hydrate_wasm.rs:59, 107, 171 (container allocations)

All three tests follow the same pattern: `make_container()` appends a `<div>` to `<body>` at the top of the function, and `cleanup(&container)` removes it at the very end — after every `.expect()` and assertion. That placement is the problem. If any earlier operation panics, the cleanup line is never reached.

In `wasm-bindgen-test` with `run_in_browser` configured (line 17), all tests share one browser page. When a test panics before returning, the container it allocated stays in `<body>` for the rest of the session. In this framework, cleanup code that follows a failed assertion does not run — the panic exits the test body before reaching it.

The early-exit points in each test, all preceding `cleanup()`:

- **`hydrate_adopt_walk_no_structural_mutations`**: `.expect()` at lines 67, 70, 82, 91; `assert!` at lines 83–86 and 92–95. `cleanup()` is at line 97.
- **`hydrate_event_wiring_post_hydration`**: `.expect()` at lines 118, 137, 139, 145; `assert_eq!` at lines 146–150; `assert!` at lines 153–156. `cleanup()` is at line 158.
- **`hydrate_mismatch_detection_recovery`**: `.expect()` at lines 184, 187; `assert_eq!` at lines 188–192. `cleanup()` is at line 194.

The comment on `make_container()` (line 29) already states the invariant: "Must be paired with `cleanup` to avoid leaking between tests." The code acknowledges the contract but does not enforce it mechanically.

**Why Warning and not Blocker**: every test scopes its DOM queries to its own `container` reference. `container.first_child()` looks inside the specific element that test created, not across `<body>`. Orphaned containers from a failed prior test accumulate in `<body>` but do not reach those queries, so test results stay correct in the current suite. This becomes a Blocker if any test adds a broader query — `body.children`, `document.query_selector("div")`, or similar — which would see leftovers from earlier failures.

**What would satisfy this finding**: replace the end-of-function cleanup with a RAII guard. A local struct holding the container element, with a `Drop` implementation that calls `parent.remove_child(&el)`, runs cleanup on both the happy path and on any panic exit. One guard per test function; the existing `cleanup()` helper can be called from `Drop`. Example shape:

```rust
struct ContainerGuard(web_sys::Element);
impl Drop for ContainerGuard {
    fn drop(&mut self) { cleanup(&self.0); }
}
let _g = ContainerGuard(make_container());
let container = _g.0.clone();
```

The three tests are otherwise structurally identical in this regard, so the fix applies uniformly.

**What was clean**: `cleanup()` itself is correct — it checks `parent_node()` before attempting removal, so calling it on an already-detached element is a no-op. The `make_container()` helper correctly returns the appended element. The issue is exclusively placement of the teardown call.
