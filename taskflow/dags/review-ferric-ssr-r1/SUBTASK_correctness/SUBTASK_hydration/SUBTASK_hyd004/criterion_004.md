# REQ-HYD-004 — Marker Schema Consistency

**Status**: CLEAN
**What was checked**: The two files that own the marker scheme — `crates/ferric/src/ssr.rs`
(constants defined and used by the server render) and `crates/ferric/src/hydrate.rs` (constants
imported and used by the client adopt walk). Checked that neither side defines its own copy of the
marker literals. Checked that the client's sentinel-detection logic matches what the server emits.
Checked determinism of the marker values. No `data-hydration-id` attribute, `get_attribute`,
`dataset`, or `querySelector` calls appear anywhere in `hydrate.rs`; the marker mechanism uses HTML
comment nodes, not element attributes.
**Evidence**: `crates/ferric/src/ssr.rs:28,35` (constant definitions), `crates/ferric/src/hydrate.rs:32` (import), `crates/ferric/src/hydrate.rs` `is_sentinel_comment` function (sentinel detection)

---

## Marker Schema (mandatory — for synthesis cross-check)

**Attribute name**: None — the PR does not use `data-hydration-id` or any element attribute.
Markers are HTML comment nodes that bracket each `VNode::Text` boundary in the serialized HTML.

**Value format**:
- Open sentinel: an HTML comment node whose `.data()` is `$t` — written into the HTML string as
  `<!--$t-->`
- Close sentinel: an HTML comment node whose `.data()` is `/$t` — written as `<!--/$t-->`
- Example: `VNode::Text("hello")` renders as `<!--$t-->hello<!--/$t-->`
- Constant strings: `TEXT_OPEN_MARKER = "<!--$t-->"` and `TEXT_CLOSE_MARKER = "<!--/$t-->"`

**Determinism mechanism**: Both constants are `pub const &str` values in `crates/ferric/src/ssr.rs`
(lines 28 and 35). They contain no counter, timestamp, hash, or any per-render state. The same
component tree always produces the same sentinel placement, and therefore the same DOM comment
sequence.

---

## Detail

### Server side

`render_node` in `crates/ferric/src/ssr.rs` wraps every `VNode::Text` arm with `TEXT_OPEN_MARKER`
before and `TEXT_CLOSE_MARKER` after the HTML-escaped text content:

```rust
VNode::Text(s) => {
    out.push_str(TEXT_OPEN_MARKER);
    out.push_str(&escape_html(s));
    out.push_str(TEXT_CLOSE_MARKER);
}
```

The constants are exported as `pub const` at module scope and documented with the note "Both sides
MUST use this exact literal — never define a local copy."

### Client side

`crates/ferric/src/hydrate.rs:32` imports both constants from the same module:

```rust
use crate::ssr::{TEXT_CLOSE_MARKER, TEXT_OPEN_MARKER};
```

The `is_sentinel_comment` helper detects sentinel nodes by stripping the `<!--` / `-->` wrappers
from the constant strings and comparing the result against `comment.data()` (the DOM API returns
only the content between the delimiters, not the delimiters themselves):

```rust
let open_data = TEXT_OPEN_MARKER
    .strip_prefix("<!--").and_then(|s| s.strip_suffix("-->")).unwrap_or("");
let close_data = TEXT_CLOSE_MARKER
    .strip_prefix("<!--").and_then(|s| s.strip_suffix("-->")).unwrap_or("");
data == open_data || data == close_data
```

The `adopt_children` walk skips sentinel comments when pairing VNode children to DOM nodes, and
`strip_sentinels` removes them afterward so DOM child indices align with VNode path indices for
subsequent diff/patch passes.

### What is clean

The design enforces single-source-of-truth at the type level: the import in `hydrate.rs` refers
directly to `crate::ssr::{TEXT_CLOSE_MARKER, TEXT_OPEN_MARKER}`. There is no string literal in
`hydrate.rs` that could diverge from the server constants. Because the constants are static, the
sentinel placement is fully deterministic for any given component tree.

The `.unwrap_or("")` fallback in `is_sentinel_comment` is dead code — the constants always carry the
`<!--` / `-->` delimiters — but it cannot produce a false positive in practice because an empty-data
comment (`<!-- -->`) would need to exist in the SSR output to match, and `render_node` never emits
one. This is a marginal observation; it does not affect correctness.

### Note on the brief's `data-hydration-id` framing

The brief's scope section uses `data-hydration-id` as the expected attribute name. Issue #224 asks
for "shared path addressing" between server and client; it does not mandate a `data-` attribute. The
PR chose HTML comment sentinels instead, a well-established pattern for text-node disambiguation
(React's SSR uses a comparable comment scheme). The requirement — same format on both sides,
consistent, deterministic — is satisfied. No finding is raised on the basis of mechanism choice.
