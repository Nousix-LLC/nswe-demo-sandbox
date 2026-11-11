# SYNTHESIS.md — ferric-router-r1

**Task**: synthesis-verify (re-verification after clippy-fix commit)  
**PR**: https://github.com/Nousix-LLC/nswe-demo/pull/192  
**Branch**: `work/ferric-router-r1` → `main`  
**Head commit**: `2bf76698c474fb60ca663f6cd074845600caea93`  
**CI re-run**: triggered automatically by the clippy-fix push

---

## CI Status — Final

All six GitHub Actions CI checks reached COMPLETED/SUCCESS on run
`41778305739` (triggered by head commit `2bf76698`):

| Check | Status | Conclusion |
|-------|--------|------------|
| `fmt` | COMPLETED | **SUCCESS** |
| `clippy` | COMPLETED | **SUCCESS** |
| `test` | COMPLETED | **SUCCESS** |
| `wasm` | COMPLETED | **SUCCESS** |
| `doc` | COMPLETED | **SUCCESS** |
| `image` | COMPLETED | **SUCCESS** |

Gate: **PASS** — all six checks green.

---

## Clippy-fix Scope Confirmation

The commit `2bf76698` (`fix(ferric-router): remove unused VNode import in test`) touches
exactly one line in one file:

```diff
# crates/ferric-router/src/router.rs  (mod tests block only)
-                use ferric::vdom::{VElement, VNode};
+                use ferric::vdom::VElement;
```

Change is confined to the `mod tests` block (line 433). No production code changed, no
public API surface altered. All five contract identities are unaffected.

---

## Contract Identity Verification

Five contract identities from `contracts/ferric_router_r1_api.md` — all verified against
head commit `2bf76698`.

### 1. `frozen_surface_preserved` ✅

All frozen #5 items are present with their original signatures. Verified via `src/lib.rs`
prelude export and previously confirmed line references:

| Item | Location | Status |
|------|----------|--------|
| `Params::get / is_empty / len / iter` | `src/matcher.rs` | ✅ Unchanged |
| `impl Default for Params` | `src/matcher.rs` | ✅ Unchanged |
| `RoutePattern::new / match_path` | `src/matcher.rs` | ✅ Unchanged |
| `Router::new / route / fallback / mount_history / outlet` | `src/router.rs` | ✅ Unchanged |
| `navigate / current_path` | `src/router.rs` | ✅ Unchanged |
| `impl Default for Router` | `src/router.rs` | ✅ Unchanged |
| `LINK_CLASS / link / Link::new / class / build` | `src/link.rs` | ✅ Unchanged |

No frozen item was removed, renamed, or redefined.

### 2. `navigate_replace_added` ✅

- `navigate_replace(path: &str)` present in `src/router.rs`
- On wasm32: calls `history.replace_state_with_url(...)` — no history growth
- Off-wasm: calls `set_current_path(path.to_string())` — reactive update only
- Prelude export confirmed:
  ```rust
  pub use crate::router::{current_path, navigate, navigate_replace, Router};
  ```
- Tests: `navigate_replace_updates_current_path`, `navigate_replace_and_navigate_both_update_path`,
  `navigate_replace_does_not_grow_history` (wasm32)
- Clippy-fix did not touch router production code — identity unaffected ✅

### 3. `active_link_awareness` ✅

- `Link::build()` reads `current_path()` and conditionally emits `aria-current="page"`
- Active case (`self.to == current_path()`): `attr("aria-current", "page")` present
- Inactive case: no `aria-current` — structurally identical to frozen surface
- Tests: `active_link_emits_aria_current_when_path_matches`, `inactive_link_has_no_aria_current`,
  `aria_current_toggles_on_navigation`
- Frozen `link(to, label) -> VNode` signature unchanged ✅
- Clippy-fix did not touch `src/link.rs` — identity unaffected ✅

### 4. `nested_routes_added` ✅

**`RoutePattern::match_prefix`** (REQ-RT-005 prerequisite):
- Present in `src/matcher.rs`
- Behavioral contract cases verified in prior synthesis (all 6 cases pass)
- Clippy-fix did not touch `src/matcher.rs` ✅

**`Router::nest(prefix, layout, child_builder)`** (REQ-RT-005):
- Present in `src/router.rs`
- `Router::outlet()` tries nested routes BEFORE flat routes
- Per-level fallback applies when no child route matches remaining path
- Frozen flat `Router::route / outlet` behavior preserved
- Tests: `nested_route_renders_layout_with_child_view`, `nested_route_index_path_renders_index_child`,
  `nested_route_uses_child_fallback_on_unmatched_child`,
  `nested_route_prefix_non_match_falls_through_to_flat_routes`
- Clippy-fix removed an unused `VNode` import from one of these test cases — test logic and
  assertions unchanged, identity unaffected ✅

### 5. `prelude_union` ✅

`src/lib.rs` prelude (verified via GitHub API against head commit `2bf76698`):

```rust
pub mod prelude {
    pub use crate::link::link;
    pub use crate::matcher::{Params, RoutePattern};
    pub use crate::router::{current_path, navigate, navigate_replace, Router};
}
```

Exact match to the contracts requirement. No frozen item removed; `navigate_replace`
added additively. ✅

---

## Issue Coverage

### #131 — navigate_replace (REQ-RT-003) ✅

**Acceptance criteria met**:
- `navigate_replace(path)` exists and is exported from prelude ✅
- Uses `history.replaceState` on wasm32 (no history growth) ✅
- Updates `current_path()` reactively on all targets ✅
- Native tests verify path update ✅
- wasm32 tests verify no history growth ✅

### #146 — Active-link awareness (REQ-RT-007) ✅

**Acceptance criteria met**:
- `Link::build()` calls `current_path()` and conditionally adds `aria-current="page"` ✅
- Active case: `aria-current="page"` on match ✅
- Inactive case: no `aria-current` ✅
- Frozen `link()` signature unchanged ✅

### #147 — Nested routes (REQ-RT-005) ✅

**Acceptance criteria met**:
- `RoutePattern::match_prefix` exists with correct semantics ✅
- `Router::nest(prefix, layout, child_builder)` exists ✅
- `Router::outlet()` tries nested routes first ✅
- Per-level fallback confirmed ✅
- Frozen flat-route behaviour preserved ✅

---

## Gate Verdict

**PASS** — All contract identities met, all six CI checks green, all three issue acceptance
criteria satisfied. The branch `work/ferric-router-r1` is ready for overseer review and merge.
