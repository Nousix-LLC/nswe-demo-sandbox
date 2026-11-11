# _BRIEF.md — SUBTASK_macro_impl: view! proc-macro implementation

**Task ID:** ferric-authoring-139-view-impl-macro  
**Hub:** SUBTASK_impl  
**Task Kind:** standard  
**Depends on:** SUBTASK_scaffold

---

## Objective

Implement the full `view!` proc-macro in `crates/ferric-macros/src/lib.rs`, covering all 8 construct
rows in `design/ferric/authoring-model.md` §2.12, the single-root rule (§2.10), and all 7 diagnostic
error cases (§2.9). The macro must produce output byte-identical to the equivalent hand-built `VNode`
builder chain.

SUBTASK_scaffold has already created the crate infrastructure; this task replaces the stub `src/lib.rs`
with the full implementation.

---

## Inputs

| Input | Location |
|-------|----------|
| Macro specification | `design/ferric/authoring-model.md` §2 — READ THIS FULLY FIRST |
| Lowering table | `design/ferric/authoring-model.md` §2.12 — 8 rows, authoritative |
| Diagnostics spec | `design/ferric/authoring-model.md` §2.9 — 7 required error cases |
| Single-root rule | `design/ferric/authoring-model.md` §2.10 |
| Frozen VNode builder API | `crates/ferric/src/vdom.rs` — read-only; confirm exact builders |
| Hub context | `../_GLOBAL.md` |
| Hub contract | `../contracts/_MANIFEST.yaml` |
| Scaffold output | `crates/ferric-macros/Cargo.toml` and stub `src/lib.rs` (from SUBTASK_scaffold) |

Access branch files via:
```
ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 \
  'bash -lc "git -C ~/nswe-demo show origin/work/ferric-epic-authoring-r1:FILE"'
```

Read the design spec via:
```
ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 \
  'bash -lc "cat ~/nswe-demo/design/ferric/authoring-model.md"'
```

---

## Lowering table reference (§2.12 — all 8 constructs)

| Author writes | Lowers to |
|---|---|
| `<div>…</div>` / `<br/>` | `VElement::new("div").children([…])` / `VElement::new("br")` |
| `"text"` | `vdom::text("text")` |
| `{expr}` where `expr: Into<String>` | `vdom::text(expr)` |
| `{expr}` where `expr: VNode` | the `VNode` itself, spliced as a child |
| `{vec}` / `<For …>` | `Vec<VNode>`, via `.children(vec)` |
| `name="v"` / `name={e}` | `.attr("name", v)` / `.attr("name", e)` |
| `key={e}` | `.key(e)` |
| `on:click={h}` / `on:input={h}` | `.on(EventKind::Click, h)` / `.on(EventKind::Input, h)` |

**`<For>` special lowering:**
```
<For each={items} key={key_fn} let:item>{body}</For>
```
lowers to:
```rust
items.into_iter().map(|item| {
    let mut __e = {body_expr};
    if let VNode::Element(ref mut el) = __e { el.key = Some(key_fn(&item)); }
    __e
}).collect::<Vec<VNode>>()
```
passed to `.children(…)`.

**Component invocation (capitalized first character):**
```
<MyComp prop={v}/>
```
lowers per authoring-model.md §2.11.

---

## Diagnostics reference (§2.9 — 7 required error cases)

| Author mistake | Expected diagnostic text |
|---|---|
| Unclosed element | "unclosed element `<TAG>`" at the open tag span |
| Mismatched close | "closing tag `</TAG>` does not match open tag `<OTHER>`" |
| Multiple top-level nodes | "a `view!` must have a single root element; wrap these in one element" |
| Dynamic attr not `Into<String>` | type error at `{expr}` span naming required conversion |
| Unknown event name | "unknown event `NAME`; bound events are: click, input" |
| Handler not a closure | "`on:EVENT` expects a handler closure" at value span |
| `<For>` without key | "list item needs `key={…}` for keyed reconciliation" |

Implement diagnostics using `syn::Error::new(span, "…").to_compile_error()`. Spans must point to the
author's tokens (open tag span for unclosed, closing tag span for mismatch, etc.) — never to generated
code. Error messages must use author vocabulary, never macro internals.

---

## Declared Outputs

1. `crates/ferric-macros/src/lib.rs` — full implementation (replaces scaffold stub)
2. Optionally: `crates/ferric-macros/src/parser.rs`, `crates/ferric-macros/src/lower.rs` (sub-modules if needed)

Files must be written directly to the server checkout on branch `work/ferric-epic-authoring-r1`.

---

## Success Criteria

1. `cargo build -p ferric-macros` succeeds with no warnings on stable Rust 1.82.
2. All 8 §2.12 construct rows produce compiler-valid output for a well-formed input.
3. All 7 §2.9 diagnostic cases produce span-accurate author-vocabulary error messages.
4. Single-root rule is enforced — multiple top-level nodes is a compile error.
5. No new VNode variant or builder method introduced in `vdom.rs`.
6. No existing public export of `crates/ferric` is altered.
7. No nightly features used.

---

## Constraints

- Read `design/ferric/authoring-model.md` §2 fully before writing any implementation code.
- Read `crates/ferric/src/vdom.rs` to confirm exact builder API before code generation.
- Proc-macro deps: `proc-macro2`, `quote`, `syn` (features = ["full"]) only.
- Do not modify any files outside `crates/ferric-macros/src/`.
- Use `syn::Error::new(span, "…").to_compile_error()` for diagnostics. No `proc-macro-error` crate.
- Diagnostic messages: author's vocabulary, author's spans. Never expose generated variable names.
- Never put server address, SSH key path, user name, or host paths into committed files.

---

## Suggested Methodology Files

**Task-type rows matched:**
- "Write (or avoid) a Rust proc-macro / codegen" → Primary: `rust`; file: `Rust_Macros_And_Codegen_Methodology.md`
- "Make my Rust library's error messages teach the fix" → `rust/Rust_Library_Diagnostics_Methodology.md`
- "Improve compiler error messages" → `compilers/Compiler_Error_Diagnostics_Methodology.md`

Specific files:
- `rust/Rust_Macros_And_Codegen_Methodology.md` — the primary methodology; covers proc-macro mechanics,
  `syn`/`quote`/`proc-macro2` patterns, attribute parsing, code generation patterns, diagnostics
- `rust/Rust_Library_Diagnostics_Methodology.md` — author-facing spans, vocabulary requirements,
  how to attach error spans to the right tokens
- `compilers/Compiler_Parsing_Theory_Methodology.md` — parsing theory for the custom view! grammar;
  recursive descent patterns applicable to syn-based TokenStream parsers
- `compilers/Compiler_Error_Diagnostics_Methodology.md` — quality bar for compile-time diagnostics:
  author-code spans, author-vocabulary descriptions (BAR-FERRIC-008)
- `core/BestPractices_Coding_Standards_Methodology.md` — Rust code quality standards

The above are the parent's flagged methodologies based on the task type. The child agent SHOULD load
these as a starting point but is the final judge of what its work requires.

## Inherited Constraints

- MSRV: stable Rust 1.82; no nightly features, no unstable proc-macro APIs.
- The VNode API is frozen: `VElement::new`, `.key`, `.attr`, `.on`, `.child`, `.children`, `vdom::text`,
  `From<VElement> for VNode`. No new builders may be introduced.
- EventKind variants are `Click` and `Input` only.
- `EventHandler` is `Rc<dyn Fn()>` — zero-argument closure.
- `Key` is a type alias for `String`.
- Diagnostic messages must NOT expose generated variable names like `__e` or macro-internal types.
- The workspace uses `[workspace.lints]` with `missing_docs = "warn"` and `unsafe_code = "warn"`.
  Add doc comments on public items.

## Out-of-Scope Methodologies

- `Rust_Cargo_Ecosystem_Methodology.md` — Cargo file setup was SUBTASK_scaffold's job.
- `synthesis/Synthesis_Overview_Methodology.md` — verification is SUBTASK_synthesis's job.
