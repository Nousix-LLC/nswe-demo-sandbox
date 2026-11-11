# _BRIEF.md — SUBTASK_impl: view! macro implementation

**Task ID:** ferric-authoring-139-view-impl  
**Hub:** T02-139-view-macro  
**Branch:** `work/ferric-epic-authoring-r1`  
**Starts from:** commit `1ccdce0` (T01 tip; fetch `origin/work/ferric-epic-authoring-r1` before starting)  
**Owned artifacts:** `crates/ferric-macros/` (all files), `crates/ferric/Cargo.toml`, `crates/ferric/src/lib.rs`

---

## Objective

Create the `ferric-macros` proc-macro crate and implement the `view!` macro in full per
`design/ferric/authoring-model.md` §2. The macro must lower every construct in the §2.12
lowering table to the existing frozen `VNode` builder API — producing builder-identical output
to a hand-written builder chain. Wire the new crate into the workspace and re-export `view!`
from the ferric prelude.

---

## Inputs

| Input | Location |
|-------|----------|
| Macro specification | `design/ferric/authoring-model.md` §2 (on `main`; `ssh … cat ~/nswe-demo/design/ferric/authoring-model.md`) |
| Lowering table | `design/ferric/authoring-model.md` §2.12 — 8 construct rows, authoritative |
| Diagnostics spec | `design/ferric/authoring-model.md` §2.9 — 7 required error cases |
| Frozen VNode builder API | `crates/ferric/src/vdom.rs` on the branch — read-only; no new builders |
| Current ferric prelude | `crates/ferric/src/lib.rs` on the branch — read-only except for the additive change below |
| Workspace manifest | `Cargo.toml` at repo root — read-only except for the additive member entry |
| Release bars | `design/ferric/release-bar.md` §BAR-FERRIC-007, §BAR-FERRIC-008 |
| Hub contract | `../contracts/_MANIFEST.yaml` |

---

## Scope

The work is centered on these distinct concerns:

**1. New proc-macro crate scaffold**  
Create `crates/ferric-macros/Cargo.toml` as a `proc-macro = true` crate with dependencies on
`proc-macro2`, `quote`, and `syn` (features: `full`). Set `edition = "2021"` and
`rust-version = "1.82"`. Add the crate to the workspace `Cargo.toml` members list.

**2. Token-stream parser**  
Parse the `view!{...}` token stream — angle-bracket tag open/close, attributes (literal and
dynamic `{expr}`), `on:event={closure}` forms, `key={expr}`, self-closing tags, text nodes
(quoted string literals only; bare whitespace discarded), interpolated expressions `{expr}`,
and `<For each={expr} key={fn} let:ident>` with its body. Capitalized first character identifies
a component tag vs. a DOM element tag.

**3. Single-root validation**  
Enforce the single-root rule (§2.10): multiple top-level siblings are a compile-time error at
the second sibling's span. The error message must name the single-root rule in author terms.

**4. Lowering to VNode builders**  
Map each parsed construct to the §2.12 output:
- DOM element `<tag …>…</tag>` or `<tag …/>` → `VElement::new("tag")` chain of `.attr`,
  `.on(EventKind::X, closure)`, `.key(expr)`, `.child(child)`, or `.children(iter)`, then
  `VNode::from(element)` (or the `Into<VNode>` implicit coercion at child sites).
- Text literal `"…"` → `vdom::text("…")`.
- Interpolated expr `{expr}` where `expr: impl Into<String>` → `vdom::text(expr)`.
- Interpolated VNode expr `{expr}` where `expr: VNode` → passes as child directly.
- Interpolated `Vec<VNode>` → passes via `.children(expr)`.
- Conditional `{ if … }` / `{ match … }` → passes the block expression as a child.
- `<For each={items} key={key_fn} let:item>{body}</For>` → `items.into_iter().map(|item| { let mut __e = {body_expr}; if let VNode::Element(ref mut el) = __e { el.key = Some(key_fn(&item)); } __e }).collect::<Vec<VNode>>()` passed to `.children(…)`.
- Component `<MyComp prop={v}/>` → calls `MyComp::render(prop: v)` or the specified component
  invocation form in authoring-model.md §2.11.

**5. Diagnostic quality**  
All 7 error cases from §2.9 must produce span-accurate messages in the author's vocabulary
(not macro-internal language). Use `syn::Error::new(span, "…").to_compile_error()` or
`proc_macro_error` / `proc_macro2::Span` attachment. Diagnostic messages must satisfy
BAR-FERRIC-008: author-code spans, author-vocabulary descriptions.

**6. Ferric crate wiring**  
In `crates/ferric/Cargo.toml` add `ferric-macros = { path = "../ferric-macros", version = "0.1" }`
under `[dependencies]`. In `crates/ferric/src/lib.rs` inside `pub mod prelude { pub use … }`,
add `pub use ferric_macros::view;` as the last additive line. No existing pub item is altered.

---

## Declared outputs

- `crates/ferric-macros/Cargo.toml`
- `crates/ferric-macros/src/lib.rs` (and any sub-modules: `parser.rs`, `lower.rs`, etc.)
- Updated `Cargo.toml` (workspace, +1 member line)
- Updated `crates/ferric/Cargo.toml` (adds ferric-macros dependency)
- Updated `crates/ferric/src/lib.rs` (adds `pub use ferric_macros::view;` to prelude)
- A commit on `work/ferric-epic-authoring-r1` containing exactly the above changes.
  Commit message must state which §2.12 constructs are implemented and reference issue #139.

---

## Success criteria

1. `cargo build -p ferric-macros` succeeds with no warnings on stable Rust 1.82.
2. `cargo build -p ferric` succeeds; existing `cargo test -p ferric --lib` (37 tests) all pass.
3. The lowering table §2.12 is fully covered — every row produces compiler-valid output for a
   well-formed input.
4. `view!` is reachable as `ferric::prelude::view!` without additional imports.
5. All 7 diagnostic error cases (`syn::Error`) compile-fail with span-accurate messages.
6. MSRV 1.82 — no nightly features. No new VNode variant or builder method introduced.
7. No pre-existing test fails; no pre-existing public export altered.

---

## Constraints

- Read `design/ferric/authoring-model.md` §2 fully before writing any implementation code.
- Read `crates/ferric/src/vdom.rs` to confirm the exact builder API before code generation.
- Proc-macro deps: `proc-macro2`, `quote`, `syn` only. No `proc-macro-error` or other
  additional crates unless they compile on stable 1.82 and add clear necessity.
- Diagnostic messages: author's vocabulary, author's spans. Never expose generated variable
  names or internal AST node types in error text.
- Do not modify any file outside `crates/ferric-macros/`, `crates/ferric/Cargo.toml`,
  `crates/ferric/src/lib.rs`, and the root `Cargo.toml` members list.
- Never put server address, SSH key path, user name, or host paths into committed files.
- Use `ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 'bash -lc "…"'`
  for all remote git and cargo operations (see project CLAUDE.md).
- Leave the branch at a clean, CI-ready state for SUBTASK_tests.
