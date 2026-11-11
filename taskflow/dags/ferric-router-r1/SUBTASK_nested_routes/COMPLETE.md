# COMPLETE — nested-routes

**Task**: `SUBTASK_nested_routes`
**Branch**: `work/ferric-router-r1`
**Commit**: `c077d8e`

## Work performed

### `crates/ferric-router/src/matcher.rs`
- Added `RoutePattern::match_prefix(&self, path: &str) -> Option<(Params, String)>`
  - Returns `Some((params, remaining))` where `remaining` is the `/`-led suffix after the matched prefix segments
  - Root pattern (zero segments) matches any path; remaining = full path normalized
  - Returns `None` when path has fewer segments than pattern or any segment mismatches
- Added `LayoutFn` private type alias for `Box<dyn Fn(&Params, &dyn Component) -> VNode>` (clippy::type_complexity)
- Added 6 new matcher tests (all pass):
  `match_prefix_static_prefix_match`, `match_prefix_consumes_all_segments`,
  `match_prefix_root_matches_anything`, `match_prefix_too_few_segments`,
  `match_prefix_static_mismatch`, `match_prefix_extracts_params`

### `crates/ferric-router/src/router.rs`
- Added private `NestedRoute` struct (`prefix`, `layout: LayoutFn`, `child_outlet: Box<dyn Fn() -> VNode>`)
- Added `nested: Vec<NestedRoute>` field to `Router` (initialized empty; degenerate single-level case unchanged)
- Added `Router::nest(self, prefix, layout, child_builder) -> Self`
  - Builds child outlet closure capturing child routes/fallback/prefix; closure reads `current_path()` reactively, strips prefix, matches remaining path
  - Child outlet is `Box<dyn Fn() -> VNode>` which implements `Component` via blanket impl; passed to layout as `&dyn Component`
- Updated `Router::outlet()` to try nested routes (prefix match) before flat routes (REQ-RT-005)
  - Per-level fallback: child router's fallback for unmatched child paths; app-root fallback for prefix misses (REQ-RT-006)
- Added 5 new router tests (all pass):
  `nested_route_renders_layout_with_child_view`, `nested_route_child_index_renders`,
  `nested_route_per_level_fallback`, `nested_route_flat_fallback_for_prefix_miss`,
  `flat_routes_still_work_alongside_nested`

## Success criteria

| Criterion | Result |
|-----------|--------|
| `cargo test -p ferric-router` | ✅ 44/44 pass |
| `cargo build -p ferric-router --target wasm32-unknown-unknown` | ✅ clean |
| `cargo clippy -p ferric-router -- -D warnings` | ✅ clean |
| `cargo fmt --check -p ferric-router` | ✅ clean |
| Contract identity `nested_routes_added` | ✅ `match_prefix` + `Router::nest` present |
| Contract identity `frozen_surface_preserved` | ✅ no frozen signatures modified |
| All pre-existing frozen tests pass | ✅ 15 matcher + 8 router pre-existing tests pass |

## Outputs

- `crates/ferric-router/src/matcher.rs` — `match_prefix` method + 6 tests
- `crates/ferric-router/src/router.rs` — `NestedRoute`, `Router::nest`, updated `Router::outlet`, 5 tests
- Commit `c077d8e` on `work/ferric-router-r1`
