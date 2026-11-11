# COMPLETE — ferric-ssr-r1-server-render

## Status: completed

## Objective

Implement `render_to_string` fully in `crates/ferric/src/ssr.rs`, addressing Issue #223
(BAR-003): server-side HTML rendering and per-request reactive scope isolation.

## What was delivered

**Branch**: `work/ferric-ssr-r1-server`  
**Commits**:
- `215dc9d feat(ferric/ssr): implement render_to_string (BAR-003, Issue #223)`
- `d8d56dc fix(ferric/ssr): resolve type inference ambiguity in test .into() calls`

**File**: `crates/ferric/src/ssr.rs` — the `todo!()` stub replaced with working logic.

### Implementation summary

- `escape_html(s)` — escapes `< > & " '` → `&lt; &gt; &amp; &quot; &#39;`
- `is_void_element(tag)` — recognises the 14 void elements from the contract
- `render_node(node, out)` — recursive VNode walk:
  - `VNode::Text(s)` → `TEXT_OPEN_MARKER + escape(s) + TEXT_CLOSE_MARKER`
  - `VNode::Element(el)` → `<tag attr="val">children</tag>` (or `<tag ... />` for void elements); event handlers dropped
- `render_to_string<F>(f)` — creates a fresh `ReactiveScope`, calls `f` inside it, renders the returned `VNode`, then drops the scope (disposing all reactive nodes before returning)

### Unit test coverage

14 new tests in `src/ssr.rs::tests`:

| Scenario | Tests |
|---|---|
| Basic element rendering | `renders_empty_element`, `renders_element_with_attributes`, `renders_element_with_text_child` |
| Text escaping (5 chars) | `escapes_all_five_injection_chars_in_text_content`, `escapes_all_five_injection_chars_in_attribute_values` |
| Text-boundary markers | `text_node_wrapped_in_markers`, `empty_text_node_wrapped_in_markers` |
| Nested elements | `renders_nested_children_at_correct_depth`, `renders_deeply_nested_structure` |
| Void elements | `void_element_emits_self_closing_tag`, `void_element_with_attributes_emits_self_closing` |
| Per-request isolation | `two_renders_produce_independent_outputs`, `signal_created_inside_render_does_not_survive_beyond_call` |

## Verification

```
cargo check --lib -p ferric   → Finished (0 errors, 0 warnings)
cargo test -p ferric          → test result: ok. 56 passed; 0 failed
```

All 56 tests pass (14 new SSR + 42 pre-existing). No `web_sys` or `wasm_bindgen` in scope.

## Requirements addressed

- **REQ-SSR-001** (server render path compiles off-wasm) — ✓ `cargo check --lib -p ferric` exits zero; no browser APIs imported
- **REQ-SSR-002** (HTML escaping) — ✓ all five characters escaped in text and attribute values
- **REQ-SSR-003** (text-boundary markers) — ✓ `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER` wrap every `VNode::Text`
- **REQ-SSR-010** (void elements) — ✓ 14 void elements emit self-closing `<tag ... />` with no end tag
- **REQ-SSR-012** (per-request reactive isolation) — ✓ each call runs inside a fresh `ReactiveScope` disposed before return; isolation verified by test

## Frozen files

`src/dom.rs`, `src/signal.rs`, `src/vdom.rs`, `src/component.rs` — not modified.
