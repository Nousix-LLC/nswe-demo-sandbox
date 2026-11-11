# _BRIEF.md — T02: view! macro surface and diagnostics (#139)

**Task ID:** ferric-authoring-139-view  
**Hub:** ferric-epic-authoring-r1  
**Branch:** `work/ferric-epic-authoring-r1` (started by T01)  
**Closes:** GitHub issue #139

---

## Objective

Implement the `view!` declarative macro per `design/ferric/authoring-model.md` §2. The macro
enables angle-bracket HTML-like view trees that lower to existing `VNode` builder calls — the
same nodes a hand-built builder chain produces. It is a new, additive item; it redefines nothing
in the frozen prelude (identity IA4).

The macro lives in a new proc-macro crate `crates/ferric-macros/` added to the workspace.
The `ferric` crate depends on it; the `ferric` prelude re-exports `view!`.

---

## Inputs

- Branch `work/ferric-epic-authoring-r1` as left by T01.
- `design/ferric/authoring-model.md` §2 on main — the authoritative specification for the macro
  surface, lowering table (§2.12), diagnostics (§2.9), fragment/single-root rule (§2.10), and
  interop (§2.11).
- `crates/ferric/src/vdom.rs` — the frozen builder API the macro lowers onto.
- GitHub issue #139 and its acceptance criteria.
- `design/ferric/release-bar.md` §BAR-FERRIC-007, §BAR-FERRIC-008.

---

## Acceptance criteria (from issue #139 and authoring-model.md §2)

The following valid inputs all compile and produce the stated VNode output:

| Input | Expected output |
|---|---|
| `view! { <div class="x"><p>"hello"</p></div> }` | VElement("div") with attr class="x", one child VElement("p") with text child "hello" |
| `view! { <br/> }` | VElement("br") with no children |
| `view! { <button on:click={h}>"go"</button> }` | VElement("button") with EventKind::Click handler, text child "go" |
| `view! { <p>{n.to_string()}</p> }` | VElement("p") with text child from the expression |
| `view! { <p>{some_vnode}</p> }` | VElement("p") with the VNode expression spliced as a child |
| `view! { <ul>{vec_of_vnodes}</ul> }` | VElement("ul") with Vec<VNode> spliced via .children(..) |
| `view! { <div>{ if b { view!{<span/>} } else { view!{<a/>} } }</div> }` | Conditional rendering works |
| `view! { <ul><For each={items} key={|i| i.id.to_string()} let:item><li>{item.name}</li></For></ul> }` | Keyed list produces fully-keyed VNode children |
| `view! { <MyComp prop={v}/> }` | Component invocation (capitalized tag) lowered to Component::render, yielding a VNode child |
| `key={expr}` on any element | Lowers to .key(expr) |

Whitespace between tags is discarded; only quoted string literals produce text nodes.

A `view!` and the equivalent hand-built builder tree produce equal `VNode`s (automated test).

The macro produces exactly one root `VNode`. Multiple top-level nodes are a compile-time error.

**Diagnostics** (`trybuild` fixtures, all with committed expected `stderr`):
- Unclosed element: error at open tag naming the unclosed element.
- Mismatched close tag: error naming the mismatch.
- Multiple top-level nodes: error naming the single-root rule.
- Dynamic attr/text value not `Into<String>`: type error at the `{expr}` span.
- Unknown event name (`on:klick`): error naming the unknown event and listing `click, input`.
- Handler value is not a closure: error at the value span.
- `<For>` without a `key` attribute: compile error flagging the missing key.

All `trybuild` fixtures pass as part of `cargo test`.

---

## Declared outputs

- New crate `crates/ferric-macros/` committed to the branch, registered in workspace `Cargo.toml`.
- `crates/ferric/Cargo.toml` updated to depend on `ferric-macros`.
- `view!` exported from `crates/ferric/src/lib.rs` prelude.
- Test suite (native, no browser) verifying the lowering table against hand-built equivalent trees.
- `trybuild` fixture suite under `crates/ferric/tests/` (or `crates/ferric-macros/tests/`) with
  committed expected `stderr` files for every diagnostic case.
- Issue #139 closed.
- `COMPLETE.md` in this workspace.

---

## Constraints

- All additions are strictly additive. No existing public item in the ferric prelude is modified.
- The macro produces builder-identical output for every construct in the lowering table
  (authoring-model.md §2.12). No new VNode variant or new builder method is introduced.
- MSRV: stable Rust 1.82; no nightly features.
- Diagnostic messages must be in terms of the author's code, not macro internals (BAR-FERRIC-008).
- The `<For each key let:item>` list form is in scope. The `let:item` binding syntax (a Rust
  identifier introduced into the template body) is part of the specified surface.
- Leave the branch at a clean, CI-ready state for T03.
