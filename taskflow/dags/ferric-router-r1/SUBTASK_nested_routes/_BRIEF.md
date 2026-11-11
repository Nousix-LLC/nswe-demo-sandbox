# _BRIEF.md — nested-routes

**Goal slug**: `nested-routes`
**Kind**: code (atomic)
**Repo**: Nousix-LLC/nswe-demo
**Branch**: `work/ferric-router-r1`
**Workspace**: `taskflow/dags/ferric-router-r1/SUBTASK_nested_routes/`

---

## Objective

Implement nested routes with a nested outlet and per-level fallback for `crates/ferric-router`.
This is the largest spoke: it adds `RoutePattern::match_prefix` to the matcher and `Router::nest`
to the router, then updates `Router::outlet()` to handle nested routes. All additions are
additive over the frozen surface.

This closes the nested-routes + nested-outlet requirement (REQ-RT-005) and the per-level fallback
requirement (REQ-RT-006) for issue #146.

---

## Inputs

- Working branch: `work/ferric-router-r1` (after `active-link` spoke)
- Source files to extend:
  - `crates/ferric-router/src/matcher.rs` (add `match_prefix` to `RoutePattern`)
  - `crates/ferric-router/src/router.rs` (add `NestedRoute`, `Router::nest()`, update `outlet()`)
  - `crates/ferric-router/src/lib.rs` (additive only, if new types need exporting)
- Contract: `taskflow/dags/ferric-router-r1/contracts/ferric_router_r1_api.md`
  (identities: `nested_routes_added`, `frozen_surface_preserved`)

---

## Declared output

Commits on `work/ferric-router-r1`:

### In `crates/ferric-router/src/matcher.rs`

New method on `RoutePattern`:

```rust
pub fn match_prefix(&self, path: &str) -> Option<(Params, String)>
```

Behavioral contract:
- Returns `Some((params, remaining))` where `remaining` is the path suffix after the matched
  segments, normalized as a `/`-led string
- Root pattern (zero segments): matches any path; remaining is the full path normalized
- `/settings` against `/settings/profile` → `Some((Params::default(), "/profile"))`
- `/settings` against `/settings` → `Some((Params::default(), "/"))`
- `/user/:id` against `/user/42/edit` → `Some((params{id="42"}, "/edit"))`
- `/user/:id` against `/user` → `None` (too few segments)
- `/other` against `/settings/profile` → `None` (mismatch)

Implementation note: match the first `self.segments.len()` path segments exactly (same logic
as `match_path`), then collect the remaining path segments into a `/`-joined string prefixed
with `/`. An empty remaining (all segments consumed) normalizes to `"/"`.

### In `crates/ferric-router/src/router.rs`

New internal struct and new `Router` method:

```rust
struct NestedRoute {
    prefix: RoutePattern,
    layout: Box<dyn Fn(&Params, &dyn Component) -> VNode>,
    child_outlet: Box<dyn Fn() -> VNode>,
}
```

The `child_outlet` is a `Fn() -> VNode` closure built inside `Router::nest()` that:
1. Reads `current_path()` reactively (subscribes the calling render effect to path changes)
2. Strips the prefix from the current path using `prefix.match_prefix`
3. Matches the remaining path against the child router's routes (first-match-wins)
4. Falls back to the child router's fallback (if any) or returns `text("")`

```rust
impl Router {
    pub fn nest(
        self,
        prefix: &str,
        layout: impl Fn(&Params, &dyn Component) -> VNode + 'static,
        child_builder: impl FnOnce(Router) -> Router,
    ) -> Self;
}
```

Updated `Router::outlet()`: before iterating flat routes, iterate nested routes. For each
`NestedRoute`, try `nested.prefix.match_prefix(&path)`. On first match, call
`(nested.layout)(&params, &nested.child_outlet)` and return the result. If no nested route
matches, fall through to flat routes as before.

The `Router` struct gains a new field `nested: Vec<NestedRoute>` (initially empty for existing
usages — `Router::new()` returns a router with an empty `nested` vec, so the degenerate
single-level case is unchanged).

### In `crates/ferric-router/src/lib.rs`

No changes unless new public types need exporting. `NestedRoute` is an internal implementation
detail and must NOT be exported. `Router::nest` is a method on the existing exported `Router`
type, requiring no new prelude export.

### Native tests in `src/matcher.rs` and `src/router.rs`

matcher tests:
- `match_prefix_static_prefix_match`: `/settings` against `/settings/profile` → remaining `/profile`
- `match_prefix_consumes_all_segments`: `/settings` against `/settings` → remaining `/`
- `match_prefix_root_matches_anything`: root pattern against `/a/b/c` → remaining `/a/b/c`
- `match_prefix_too_few_segments`: `/user/:id` against `/user` → `None`
- `match_prefix_static_mismatch`: `/user` against `/settings/profile` → `None`
- `match_prefix_extracts_params`: `/user/:id` against `/user/42/edit` → params{id="42"}, remaining `/edit`

router tests:
- `nested_route_renders_layout_with_child_view`: two-level config (parent `/users` + child
  `/:id`); navigate to `/users/7`; outlet renders parent layout with child view showing `id=7`
- `nested_route_child_index_renders`: navigate to `/users`; outlet renders parent layout with
  child fallback (or empty child)
- `nested_route_per_level_fallback`: navigate to `/users/no/such/path`; child fallback renders;
  parent layout is still rendered around it
- `nested_route_flat_fallback_for_prefix_miss`: navigate to `/other`; app-root fallback renders
  (prefix `/users` did not match)
- `flat_routes_still_work_alongside_nested`: verify that adding `nest()` does not break
  `route()` behavior in the same router

---

## Success criteria

1. `cargo test -p ferric-router` passes all tests (new + pre-existing frozen tests).
2. `cargo build -p ferric-router --target wasm32-unknown-unknown` succeeds.
3. `cargo clippy -p ferric-router -- -D warnings` clean.
4. `cargo fmt --check -p ferric-router` clean.
5. Contract identities `nested_routes_added` and `frozen_surface_preserved` are met.
6. All pre-existing frozen tests in matcher.rs and router.rs pass without modification.

---

## Design notes

The child outlet closure captures the child router's data (routes + fallback + prefix) and
reads `current_path()` reactively. This means the child outlet is itself a `Fn() -> VNode`
(a `Component`). The `layout` closure receives a `&dyn Component` reference to this child
outlet and embeds it via `child_outlet.render()`. Because the child outlet reads
`current_path()`, the ferric render effect that runs the parent outlet's render also subscribes
to path changes through the child outlet — so navigation re-renders both parent and child.

Avoid storing `Signal<String>` for the remaining path in the `NestedRoute` struct (this would
require mutation inside a render effect, which can cause recursive rendering). Instead, compute
the remaining path fresh inside the child outlet closure on each render by calling
`current_path()` and `prefix.match_prefix`.

Do not introduce `Rc<RefCell<>>` sprawl; the design above requires none. The `Box<dyn Fn>`
closures are sufficient.

---

## Constraints

- Only touch `crates/ferric-router/src/matcher.rs`, `src/router.rs`, and `src/lib.rs`
  (additive only on lib.rs). Do not touch `src/link.rs` or `examples/`.
- Additive only: do not change any frozen #5 method signatures.
- `NestedRoute` is an internal struct — do not export it.
- Do not create a PR; leave that to the synthesis gate.
- Commit messages must NOT include the host server address, SSH key path, user name, or
  local paths.
