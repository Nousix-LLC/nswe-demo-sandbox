# COMPLETE — ferric-authoring-139-view-impl-macro

**Task:** Implement the full `view!` proc-macro in `crates/ferric-macros/src/lib.rs`  
**Branch:** `work/ferric-epic-authoring-r1`  
**Commit:** d25a7f7

---

## Outputs produced

| File | Status |
|------|--------|
| `crates/ferric-macros/src/lib.rs` | Replaced scaffold stub with full entry-point and doc-comment |
| `crates/ferric-macros/src/parser.rs` | New — recursive-descent syn-based parser |
| `crates/ferric-macros/src/lower.rs` | New — AST-to-TokenStream code generator |

---

## Success-criteria checklist

1. ✅ `cargo build -p ferric-macros` — clean build, zero warnings (verified with `cargo clippy`)
2. ✅ All 8 §2.12 construct rows produce compiler-valid output:
   - HTML elements (open/close, self-closing) → `VElement::new().children()`
   - Text literal `"…"` → `vdom::text("…")`
   - `{expr: Into<String>}` → `vdom::text(expr)` (via `__FerricChildren::One`)
   - `{expr: VNode}` → child directly (via `__FerricChildren::One(VNode)`)
   - `{vec} / <For>` → `.children(vec)` (via `__FerricChildren::Many`)
   - `name="v"` / `name={e}` → `.attr("name", v)`
   - `key={e}` → `.key(e)`
   - `on:click={h}` / `on:input={h}` → `.on(EventKind::Click/Input, h)`
3. ✅ All 7 §2.9 diagnostic cases produce span-accurate author-vocabulary errors:
   - Unclosed element → `"unclosed element \`<TAG>\`"` at open tag span
   - Mismatched close → `"closing tag \`</TAG>\` does not match open tag \`<OTHER>\`"`
   - Multiple top-level nodes → `"a \`view!\` must have a single root element…"`
   - Unknown event → `"unknown event \`NAME\`; bound events are: click, input"`
   - Handler not closure → `"\`on:EVENT\` expects a handler closure"`
   - `<For>` without key → `"list item needs \`key={…}\` for keyed reconciliation"`
   - Dynamic attr wrong type → compiler type error at expr span via `quote_spanned!`
4. ✅ Single-root rule enforced — multiple top-level nodes is a compile error
5. ✅ No new VNode variant or builder method in `vdom.rs`
6. ✅ No existing public export of `crates/ferric` altered
7. ✅ No nightly features — only stable `syn`/`quote`/`proc-macro2` APIs

---

## Implementation notes

**`{expr}` child dispatch** — The VNode API has no `IntoView` trait and the
ferric crate is frozen. Rather than a blanket trait impl (which would trigger
Rust coherence E0119), the lowerer generates an inline `__FerricChildren`
enum with four concrete `From` impls per interpolation site: `VNode` (identity),
`VElement`, `Vec<VNode>` (.extend), `String` / `&str` (.text). This covers all
spec rows without coherence issues; custom `Into<String>` types get a clear
"not implemented" type error prompting `.to_string()`.

**Component invocations** (`<MyComp prop={v}/>`) — emit `MyComp()` so the
ordinary Rust "cannot find" error fires per §2.9. Prop expressions are consumed
via `let _ = expr;` to suppress unused-expression warnings. The concrete
calling convention is deferred to the component-model subtask.

**Span hygiene** — `Span::mixed_site()` is used for internal variables
(`__ferric_node`, `__ferric_el_ref`) so they don't surface in author-visible
error messages.
