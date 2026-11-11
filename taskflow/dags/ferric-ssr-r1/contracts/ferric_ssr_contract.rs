// ferric_ssr_contract.rs
//
// Structural declarations for the ferric-ssr-r1 decomposition.
// Contract kind: rust_trait (function signatures + compile-time constants).
//
// This file is READ-ONLY for all descendant tasks.
// It declares the composition seam; it implements nothing.
// Descendant tasks must conform to these signatures exactly.
//
// All implementing tasks import these constants; they MUST NOT define their own
// marker strings. The hydration walk is correct only when both sides use the
// same literal bytes.

// ── Text-boundary marker format ───────────────────────────────────────────────
//
// Server-side render_to_string wraps every VNode::Text node in these HTML
// comment markers. Comment nodes are invisible to end users but are present in
// the DOM as Comment nodes (nodeType === 8).
//
// The client hydration walk scans child nodes. When it encounters a Comment
// node whose data matches TEXT_OPEN_MARKER it knows the following node(s) form a
// text boundary region. It DOES NOT count comment nodes as structural VNode
// children — only element and text nodes advance the VNode child index.
//
// This scheme (comment sentinels around text) is consistent with the approach
// used by Leptos and React's server components for the same purpose: allowing
// unambiguous, index-stable text node location in the adopted DOM.

pub const TEXT_OPEN_MARKER: &str = "<!--$t-->";
pub const TEXT_CLOSE_MARKER: &str = "<!--/$t-->";

// ── Server-side API ───────────────────────────────────────────────────────────
//
// Location: crates/ferric/src/ssr.rs
// Owner: ferric-ssr-r1-server-render (skeleton creates the stub file)
//
// render_to_string renders a component closure to an HTML string.
//
// Signature (implemented in crates/ferric/src/ssr.rs):
//
//   pub fn render_to_string<F>(f: F) -> String
//   where
//       F: FnOnce() -> VNode;
//
// Constraints (REQ-SSR-001, REQ-SSR-002, REQ-SSR-003, REQ-SSR-010, REQ-SSR-012):
//
//   COMPILE TARGET
//     - No `use web_sys` or `use wasm_bindgen` anywhere in src/ssr.rs.
//     - The file must be reachable when compiled with `cargo check --lib -p ferric`
//       on a native (non-wasm) host target.
//
//   REACTIVE ISOLATION
//     - The closure is invoked inside a fresh ReactiveScope (from crate::signal).
//     - That scope is dropped before render_to_string returns.
//     - No signal subscriptions survive the call; signal state does not leak
//       across concurrent render_to_string invocations.
//
//   HTML ESCAPING (applied to all text content and attribute values)
//     - '<'  →  "&lt;"
//     - '>'  →  "&gt;"
//     - '&'  →  "&amp;"
//     - '"'  →  "&quot;"
//     - '\'' →  "&#39;"
//
//   TEXT NODE ENCODING
//     - VNode::Text(s) emits: TEXT_OPEN_MARKER + escape(s) + TEXT_CLOSE_MARKER
//
//   ELEMENT ENCODING
//     - VNode::Element(e) emits:
//         <{tag} {attr_name}="{escape(attr_value)}" ...>
//           {children recursively rendered}
//         </{tag}>
//     - Void elements (area, base, br, col, embed, hr, img, input, link, meta,
//       param, source, track, wbr) emitted as self-closing: <{tag} ... />

// ── Client-side API ───────────────────────────────────────────────────────────
//
// Location: crates/ferric/src/hydrate.rs
// Owner: ferric-ssr-r1-client-hydrate (skeleton creates the stub file)
// Target: cfg(target_arch = "wasm32") only
//
// hydrate adopts a server-rendered DOM subtree rooted at `root`.
//
// Signature (implemented in crates/ferric/src/hydrate.rs):
//
//   #[cfg(target_arch = "wasm32")]
//   pub fn hydrate<F>(root: web_sys::Element, f: F)
//   where
//       F: Fn() -> VNode + 'static;
//
// Constraints (REQ-SSR-004, REQ-SSR-005, REQ-SSR-009):
//
//   ZERO STRUCTURAL MUTATIONS (gating bar)
//     - The adopt pass MUST NOT create, replace, move, or remove any DOM node
//       under `root`. This is verifiable by MutationObserver or node-identity
//       comparison in a headless wasm-bindgen-test.
//
//   COMMENT NODE HANDLING
//     - During the adopt walk, Comment nodes whose data == TEXT_OPEN_MARKER or
//       TEXT_CLOSE_MARKER are recognized as text-boundary sentinels. They are NOT
//       counted as VNode children when advancing the child index.
//
//   EVENT WIRING
//     - Existing Click and Input event handlers in the VNode tree are wired onto
//       the adopted DOM elements using the same Reflect-based approach as dom.rs.
//
//   REACTIVE EFFECTS
//     - A reactive effect is established with the first adopted tree as the
//       "previous" VNode for the diff/patch cycle. Subsequent signal updates
//       invoke the existing keyed-patch path exactly as dom::mount does.
//
//   MISMATCH DETECTION (dev builds only)
//     - If the DOM node at a child-index path has a different tag or text than
//       the VNode at that path:
//         #[cfg(debug_assertions)]
//         web_sys::console::warn_1(&format!(
//             "ferric hydration mismatch at [{}]: expected {:?}, found {:?}",
//             path_string, expected, found
//         ).into());
//
//   MISMATCH RECOVERY
//     - The mismatched subtree is recovered by client-rendering it (as if
//       dom::mount were called on that node alone).
//     - Sibling and ancestor nodes that were successfully adopted are NOT
//       disturbed by the recovery render.
