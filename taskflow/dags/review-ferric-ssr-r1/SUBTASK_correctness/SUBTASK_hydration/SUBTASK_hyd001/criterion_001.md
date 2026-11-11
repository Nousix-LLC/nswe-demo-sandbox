# REQ-HYD-001 — hydrate() DOM Walk Without Re-creating Nodes

**Status**: CLEAN
**What was checked**: The `hydrate()` entry point in `crates/ferric/src/hydrate.rs` on branch
`work/ferric-ssr-r1`, specifically the adopt pass (`adopt_root_vnode` → `adopt_vnode` →
`adopt_children`), every call site of `appendChild`, `replace_child`, `replaceWith`,
`create_element`, and `create_text_node` in that file, and the signal-listener wiring path
(`set_events`).

**Evidence**:

1. **Happy-path: element tag match — zero structural mutations.**
   `adopt_vnode` casts the existing DOM node with `dom_node.dyn_ref::<web_sys::Element>()`
   (no creation), checks the tag, then calls `set_events(el, &ve.events)` on `el` — the
   already-present element — and recurses into children. No `create_element`, no
   `append_child`, no `replace_child`.
   `crates/ferric/src/hydrate.rs:98–105`

2. **Happy-path: text node match — zero structural mutations.**
   `adopt_vnode` matches on `dom_node.dyn_ref::<web_sys::Text>()` and checks `t.data() ==
   *text`. On match the branch comment reads "Perfect text match — nothing to do" and no
   operations are performed.
   `crates/ferric/src/hydrate.rs:113–115`

3. **Signal (event) listeners wired to existing nodes, not freshly created ones.**
   `set_events(el, &ve.events)` is called with `el` derived from `dom_node.dyn_ref()` — the
   server-rendered element already in the DOM. The function calls
   `element.add_event_listener_with_callback(...)` on that existing element.
   `crates/ferric/src/hydrate.rs:102–103`; `set_events` body at `hydrate.rs:280–325`

4. **Child traversal is positional, not `querySelector`/`data-hydration-id`.**
   `adopt_children` iterates `parent_dom.child_nodes()` (the live DOM child list) in order,
   skipping sentinel Comment nodes (`TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER`), and matches
   each DOM node against the VNode at the same index. No `querySelector` call and no
   `data-hydration-id` attribute is used anywhere in the file. The mechanism is the
   "shared path addressing" described in Issue #224's acceptance criteria.
   `crates/ferric/src/hydrate.rs:148–192`

5. **`appendChild` and `replace_child` appear only in mismatch-recovery branches.**
   `append_child` is called in `adopt_root_vnode` when the DOM under the root is empty
   (recovery: hydrate.rs:88) and in `adopt_children` when the VNode list is longer than
   the DOM list (missing-child recovery: hydrate.rs:187). `replace_child` is called only
   in the element-tag-mismatch branch (hydrate.rs:120–122) and the text-node-type-mismatch
   branch (hydrate.rs:131–133). The module-level doc comment states this explicitly: "No
   structural DOM mutation occurs when every node matches (REQ-SSR-004)."
   `crates/ferric/src/hydrate.rs:5–11`

6. **Post-adopt sentinel cleanup is not a content-node mutation.**
   After the adopt pass, `strip_sentinels` removes `<!--$t-->` / `<!--/$t-->` Comment nodes
   inserted by `render_to_string` as text-boundary markers. These are SSR implementation
   artifacts, not VNode content nodes. Their removal is documented as step 2 of the
   hydration protocol and is necessary so DOM child indices align with VNode path indices
   for the subsequent diff/patch reactive loop.
   `crates/ferric/src/hydrate.rs:65–67`; `strip_sentinels` body at `hydrate.rs:198–226`

**Finding**: none. REQ-HYD-001 is satisfied. The adopt pass walks the server-rendered DOM
using `child_nodes()` positional traversal, wires event handlers onto the existing nodes,
and performs zero structural mutations on content nodes when the server and client VNode
trees agree. The absence of `querySelector`/`data-hydration-id` is intentional design
(positional path addressing), consistent with the Issue #224 acceptance text.
