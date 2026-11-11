## Hardcoded strings vs. imported constants

**Severity**: Blocker
**Evidence**: hydrate_wasm.rs:62, hydrate_wasm.rs:113, hydrate_wasm.rs:174

All three tests inject HTML whose text nodes are bare strings — no `<!--$t-->` / `<!--/$t-->` sentinel markers. `render_to_string` in `ssr.rs` wraps every `VNode::Text` in `TEXT_OPEN_MARKER` and `TEXT_CLOSE_MARKER`, so actual SSR output for any text node contains flanking comment nodes the hydration path must handle. The gap between what each test injects and what SSR would produce:

| Test | Injected (line) | Actual SSR output |
|---|---|---|
| `hydrate_adopt_walk_no_structural_mutations` | `<div><span>hello</span></div>` (line 62) | `<div><span><!--$t-->hello<!--/$t--></span></div>` |
| `hydrate_event_wiring_post_hydration` | `<button>0</button>` (line 113) | `<button><!--$t-->0<!--/$t--></button>` |
| `hydrate_mismatch_detection_recovery` | `<div>text</div>` (line 174) | `<div><!--$t-->text<!--/$t--></div>` |

The import block (lines 11–15) imports nothing from `ferric::ssr`. There are no local constant definitions for `TEXT_OPEN_MARKER` or `TEXT_CLOSE_MARKER` anywhere in the file — the sentinels are absent entirely, not duplicated.

The hydration walk in `hydrate.rs` must count or skip the `<!--$t-->` and `<!--/$t-->` comment nodes when determining structural VNode children and when adopting text nodes. Because no test injects those comment nodes, the sentinel-handling code paths are never reached. All three tests — including the REQ-SSR-004 adopt-walk test — pass on input that production SSR cannot generate. The adopt-walk coverage is false: the test verifies identity preservation against a DOM whose structure differs from what `render_to_string` would produce.
