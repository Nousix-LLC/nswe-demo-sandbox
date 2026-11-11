# SYNTHESIS.md — SUBTASK_synthesis: verification gate + commit

**Task ID:** ferric-authoring-139-view-impl-synthesis  
**Hub:** SUBTASK_impl (ferric-authoring-139-view-impl)  
**Verdict:** ✅ ALL PASS — commit created

---

## Go / No-Go Decision

**PASS** — All 7 identity assertions from `contracts/_MANIFEST.yaml` hold. Git commit created and pushed.

---

## Verification Checks

### Check 1 — Compilation (I-BUILD-01, I-BUILD-02)

| Command | Result |
|---------|--------|
| `cargo build -p ferric-macros` | ✅ Exit 0, no errors |
| `cargo build -p ferric` | ✅ Exit 0, no errors |

Both crates build successfully on stable Rust 1.82.

### Check 2 — Existing test suite (I-TEST-01, I-ADDITIVE-01)

| Command | Result |
|---------|--------|
| `cargo test -p ferric --lib` | ✅ 37 tests PASSED, 0 FAILED |

Pre-existing 37 tests all pass. No existing exports broken.

### Check 3 — Lowering coverage (I-LOWER-ALL)

All 8 §2.12 construct rows confirmed present in `crates/ferric-macros/src/lower.rs`:

| Construct | Implementation |
|-----------|---------------|
| DOM element open/close and self-closing | `lower_element()` → `VElement::new(tag)` + `.child()` chain |
| Text literals → `vdom::text("…")` | `ViewNode::Text(lit)` → `quote! { ::ferric::vdom::text(#s) }` |
| `{expr: Into<String>}` → `vdom::text(expr)` | `lower_interp_child()` → `__FerricChild::from()` dispatch |
| `{expr: VNode}` → child splice | `lower_interp_child()` → `From<VNode>` impl (identity) |
| `{vec}` / `<For>` → `.children(iter)` | `lower_for_as_vec()` + `lower_interp_children_push()` |
| Attributes static/dynamic → `.attr("name", value)` | `lower_attr()` for both `AttrValue::Lit` and `AttrValue::Expr` |
| `key={e}` → `.key(e)` | `if let Some(key_expr) = &el.key` guard in `lower_element()` |
| `on:click={h}` / `on:input={h}` → `.on(EventKind::…, h)` | `lower_event()` → `EventKind::Click` / `EventKind::Input` |

Component invocation (capitalized tag) also implemented via `lower_component()`.

### Check 4 — Diagnostic coverage (I-DIAG-ALL) + Export check (I-EXPORT-01)

**Diagnostics — all 7 §2.9 cases confirmed:**

| # | Case | Mechanism | Location |
|---|------|-----------|----------|
| 1 | Empty `view!` invocation | `syn::Error` at `input.span()` | `parser.rs` ViewRoot::parse |
| 2 | Multiple top-level nodes | `syn::Error` at `input.span()` | `parser.rs` ViewRoot::parse |
| 3 | Unclosed element | `syn::Error` at `open_span` | `parser.rs` parse_attrs / parse_children |
| 4 | Dynamic attr value not Into<String> | `quote_spanned! { val_span }` type error | `lower.rs` lower_attr |
| 5 | Unknown event name | `syn::Error` at `ev_span` | `parser.rs` parse_attrs |
| 6 | Handler not a closure | `syn::Error` at `handler_span` | `parser.rs` parse_attrs |
| 7 | `<For>` without key | `syn::Error` at `span` | `parser.rs` parse_for_body |

All 7 cases produce span-accurate errors. Cases 1–3, 5–7 use `syn::Error` directly; case 4 uses `quote_spanned!` to route the Rust type error to the author's expression span.

**Export check:** `pub use ferric_macros::view;` present in `crates/ferric/src/lib.rs` prelude module. ✅

---

## Identity Assertions

| ID | Statement | Status |
|----|-----------|--------|
| I-BUILD-01 | `cargo build -p ferric-macros` succeeds | ✅ PASS |
| I-BUILD-02 | `cargo build -p ferric` succeeds | ✅ PASS |
| I-TEST-01 | 37 pre-existing tests pass, 0 failed | ✅ PASS |
| I-EXPORT-01 | `ferric::prelude::view!` accessible | ✅ PASS |
| I-ADDITIVE-01 | No existing exports broken | ✅ PASS |
| I-LOWER-ALL | All 8 §2.12 constructs implemented | ✅ PASS |
| I-DIAG-ALL | All 7 §2.9 diagnostics, span-accurate | ✅ PASS |

---

## Git Commit

**Branch:** `work/ferric-epic-authoring-r1`  
**Commit SHA:** `3c3d4aa`  
**Message:** `feat(ferric-macros): implement view! macro (#139)`  
**Pushed to remote:** yes (`d25a7f7..3c3d4aa`)

The commit includes the `Cargo.lock` update (ferric-macros added to ferric's resolved dependency list), completing the work of SUBTASK_scaffold, SUBTASK_macro_impl, and SUBTASK_wire.

---

## Coverage Assertion

The combined work of SUBTASK_scaffold + SUBTASK_macro_impl + SUBTASK_wire + this synthesis commit delivers:

- A complete `ferric-macros` proc-macro crate with `view!` macro
- Full §2.12 lowering coverage (all 8 constructs + component invocation)
- Full §2.9 diagnostic coverage (all 7 error cases, span-accurate)
- `ferric::prelude::view!` export wired
- All 37 pre-existing ferric tests passing
- Branch CI-ready: builds clean on stable Rust 1.82

SUBTASK_impl hub: **COMPLETE**.
