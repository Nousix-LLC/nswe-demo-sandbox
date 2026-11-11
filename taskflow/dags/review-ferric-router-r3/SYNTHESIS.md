# SYNTHESIS — review-ferric-router-r3

**Task**: Code review of PR #203 (`work/ferric-router-r3`) — ferric-router r1 additions.  
**Verdict**: **APPROVE**  
**CI**: 6/6 checks PASS (run 41796577463).  
**Blockers**: None.  
**Non-blockers**: 3 (filed as backlog issues).

---

## Per-concern findings

### 1. Correctness

**What was checked**: Each requirement REQ-RT-001..008 and each acceptance criterion for issues #131, #146, #147. Edge cases: trailing-slash, too-few-segments, root-pattern prefix, navigate before mount, no-child-fallback. Prior non-blockers #194 and #195.

**Found clean**:

- **REQ-RT-003** (`navigate_replace`): On wasm32, calls `history.replace_state_with_url(&JsValue::NULL, "", Some(path))` — the correct `replaceState` overload. On all targets, calls `set_current_path`. Both native acceptance-criterion tests are substantive: `navigate_replace_updates_current_path` checks the signal value; `navigate_replace_and_navigate_both_update_path` checks interleaving. The wasm32 test `navigate_replace_does_not_grow_history` checks `history.length` before and after replace, then confirms a subsequent push-navigate grows it. ✓

- **REQ-RT-005** (`Router::nest`): `match_prefix` correctly returns `Some((params, remaining))` with remaining normalized as a `/`-led string. The outlet resolution loop tries nested entries before flat routes. `NestedEntry` flattening correctly consumes the child `Router` at `outlet()` call time. The index-path case (`/settings` → remaining `"/"` → child route `"/"`) is tested. The fall-through case (prefix non-match → flat route) is tested.

- **REQ-RT-006** (per-level fallback): `nested_route_uses_child_fallback_on_unmatched_child` correctly verifies the child fallback fires while the prefix still matches. The outer fallback and inner fallback are independent, as documented.

- **REQ-RT-007** (`aria-current="page"`): `Link::build()` reads `current_path()` at build time and conditionally adds the attribute. The inactive branch is structurally identical to the frozen surface. The three tests (active, inactive, toggle) are substantive attribute-value assertions.

- **REQ-RT-008** (additive composition): All 44 native tests pass. No frozen signatures changed. CHANGELOG records all additions explicitly as additive.

- **Reactivity / signal handling**: `navigate_replace` and `navigate` both call `set_current_path`, so the outlet's reactive re-render path is identical. The `ChildOutlet` wraps a pre-rendered `VNode` and clones it on `render()` — cheap, `Rc`-backed. No stale signals; the outlet closure holds the signal reference by lazy access on each render call.

- **Edge cases**: `match_prefix` on the root pattern (zero segments) correctly matches any path and returns the full path as remaining. Too-few-segments correctly returns `None`. All seven `match_prefix` unit tests cover the documented examples from the CHANGELOG.

- **#194, #195**: Both remain open and unaddressed by this PR. Neither is a blocker for landing.

**Findings**:

- **NB-C1 (non-blocker)**: Missing end-to-end test for a parameterized prefix passing params to the layout. The design criterion for REQ-RT-005 mentions "parent layout with child bound to `id="7"`" (i.e., a `/user/:id` prefix capturing into layout params). The `match_prefix` unit test `match_prefix_param_captures_and_remaining` verifies the extraction mechanism, but no test drives this through `Router::nest` → `outlet.render()` to confirm the layout receives the correct params. Filed as backlog issue.

---

### 2. Code quality

**What was checked**: Responsibilities, coupling, naming, function size, error-handling style, extensibility.

**Found clean**:

- `ChildOutlet` has one job: wrap a pre-rendered `VNode` and implement `Component` so it can be passed as `&dyn Component` to the layout closure. Well-scoped and unexported.

- `NestedEntry` correctly flattens the child `Router` at `outlet()` call time, moving the child's route table and fallback into the `'static` outlet closure. This avoids carrying the `Router` type into the closure and is the right decomposition.

- The outlet resolution loop is readable: try nested (prefix), then flat (exact), then fallback. The two-phase structure is easy to extend (e.g., adding a third "query-string routes" tier later).

- `navigate_replace` follows the same error-handling style as `navigate`: silent `let _ = ...` discard of the History API result. Consistent with existing code and appropriate for client-side WASM where `replaceState` failures are not actionable.

- Naming is consistent with the existing codebase: `navigate_replace` mirrors `navigate`; `LayoutFn` mirrors `ViewFn`; `nest` mirrors `route`/`fallback`.

**Findings**:

- **NB-CQ1 (non-blocker)**: In `Router::outlet()`, the terminal `child_view.unwrap_or_else(|| text(""))` is dead code. By the time control reaches that line, `child_view` is always `Some`: the preceding `or_else(|| Some(text("")))` guarantees it. Replacing with `unwrap()` (with a comment naming the invariant) or restructuring to remove the redundant assignment would make the invariant explicit. Filed as backlog issue.

---

### 3. Test coverage

**What was checked**: Each acceptance criterion for REQ-RT-003, REQ-RT-005, REQ-RT-006, REQ-RT-007; edge cases in `match_prefix`; whether assertions check behavior or vacuously pass; the clippy-fix commit's test.

**Found clean**:

- All acceptance-criterion tests are substantive. `navigate_replace_updates_current_path` asserts the signal value. The aria-current tests assert exact attribute values and their absence. The nested-route layout test (`nested_route_renders_layout_with_child_view`) deconstructs the `VNode::Element` tree and asserts both children by value — this is a real behavior test, not a skeleton.

- The `nested_route_renders_layout_with_child_view` test added by the clippy-fix commit (7219e21) is complete: it verifies the outer `div` tag, two children, and each child's text content. ✓

- `match_prefix` has seven tests covering each documented example from the CHANGELOG, including the root pattern, too-few-segments, param capture, and static mismatch. ✓

- The wasm32 test asserts `history.length` before and after, then checks push-navigate growth. The comparison is relative (before == after replace; after < after push), which is robust to test-runner isolation. ✓

**Findings**:

- **NB-TC1 (non-blocker)**: Two test gaps filed together as one issue: (a) no end-to-end test for a parameterized `Router::nest` prefix (layout receives prefix params); (b) no test for the no-child-fallback case (prefix matches, no child route matches, no child fallback registered → outlet renders an empty text node). The behavior is correct per the code, but neither path has an explicit assertion. Filed as backlog issue.

---

### 4. Rust idioms

**What was checked**: Lifetime correctness, pub surface, wasm-bindgen handle management, soundness.

**Found clean**:

- No `unsafe` blocks in the diff. ✓

- The outlet closure captures `routes`, `fallback`, and `nested` by move. All are `'static` (boxed closures). ✓

- `Component` as `&dyn Component` is object-safe: `fn render(&self) -> VNode` has no generic parameters, no `Self` by value, and returns a concrete type. ✓

- `LayoutFn = Box<dyn Fn(&Params, &dyn Component) -> VNode>` — double dynamic dispatch is appropriate here: layouts are heterogeneous by design. ✓

- No new `Closure` objects are created. The only `closure.forget()` in the file is in the pre-existing `install_popstate_listener`, unchanged. `navigate_replace` on wasm32 is a synchronous call with no closure lifecycle concerns. ✓

- `ChildOutlet` and `NestedEntry` are private structs (not in prelude). `LayoutFn` is a private type alias. The public surface added is exactly `navigate_replace` and `Router::nest`, which is correct. ✓

- `VNode` clone is cheap (RC-backed event handlers per the CHANGELOG comment). ✓

---

### 5. API and contract stability

**What was checked**: Additive-only changes, frozen surface items unchanged, seam with PR #188.

**Found clean**:

- All additions are additive. `navigate_replace`, `Router::nest`, and `Router::match_prefix` are new items. No existing signatures removed or modified.

- The frozen `link(to, label) -> VNode` signature is unchanged. The behavior extension (adding `aria-current` on the active case) is per-spec and documented. The inactive case is structurally identical to the frozen surface — the existing test suite (44 tests all pass) confirms no regressions.

- The outlet behavior for flat-route-only routers is unchanged: nested routes are tried first, but with an empty `nested` vec, the loop is a no-op.

- Seam with PR #188 (`ferric::Component`, `ferric::Signal<String>`, `ferric::VNode`, `ferric::mount`): all contracts honored. `ChildOutlet` implements `Component` correctly. The signal model is unchanged. ✓

---

## Disposition of non-blockers

| ID | Concern | Severity | Filed as |
|----|---------|----------|---------|
| NB-C1 | Missing end-to-end test for parameterized `Router::nest` prefix passing params to layout | test gap | backlog issue (filed) |
| NB-CQ1 | Redundant `unwrap_or_else` in nested-route outlet branch (dead code) | code quality | backlog issue (filed) |
| NB-TC1 | Two test gaps: (a) parameterized prefix E2E; (b) no-child-fallback renders empty node | test gap | backlog issue (filed with NB-C1) |

Prior non-blockers #194 (navigate input validation) and #195 (commit description narrower than #146 scope) remain open and unchanged by this PR.
