# COMPLETE — T04: Component type-level diagnostics (#141)

**Task ID:** ferric-authoring-141-diag  
**Status:** completed  
**Commit:** 763f4d6 on `work/ferric-epic-authoring-r1`  
**Issue closed:** #141

---

## Work performed

### 1. `#[component]` macro rewritten to type-state builder

The original macro used `.expect("missing required prop…")` at runtime. That does not meet
BAR-FERRIC-010 (compile-time errors). The macro was rewritten to generate:

- **Marker types** per required param — an "unset" type and a "set" type.
- **A sealed trait** `__CompHasProp` gating `build()` on the builder, only callable when all
  required params are in the Set state.
- **Double-fill prevention** for named-slot params: a second sealed trait `__CompSlotNotYetFilled`
  gates the slot setter itself; once a slot transitions to its "set" state the setter can no
  longer be called.

### 2. Human-readable marker type names

`#[diagnostic::on_unimplemented]` does not fire for E0599 (method not found with unsatisfied
bounds) in stable Rust. The attribute is present for forward compatibility, but the primary
message mechanism is the **unset marker type name**, which appears verbatim in E0599 output.
Naming convention chosen:

| Situation | Type name | Appears in error as |
|---|---|---|
| Required prop missing | `Greeting_missing_required_prop_name` | "Greeting missing required prop name" |
| Required slot missing | `Page_missing_required_slot_header` | "Page missing required slot header" |
| Slot filled twice | `Page_slot_header_already_filled` | "Page slot header already filled" |

### 3. trybuild dev-dependency added

`trybuild = { version = "1", features = ["diff"] }` added to `crates/ferric-macros/Cargo.toml`.

### 4. Seven compile-fail fixtures committed

Location: `crates/ferric-macros/tests/compile_fail_component/`

| Fixture | Mistake covered | Diagnostic quality |
|---|---|---|
| `01_missing_required_prop` | Omit required prop | `Greeting_missing_required_prop_name` in note ✓ |
| `02_wrong_type_prop` | Wrong-type prop value | `expected \`String\`, found \`i32\`` with prop name ✓ |
| `03_unknown_prop` | Prop not on component | `no method named \`color\`` on `GreetingProps` ✓ |
| `04_children_in_no_children_component` | Children on no-children component | `no method named \`children\`` on `LabelProps` ✓ |
| `05_fill_undeclared_slot` | Slot not declared by component | `no method named \`footer\`` on `CardProps` ✓ |
| `06_fill_slot_twice` | Fill slot twice | `PageProps<Page_slot_header_already_filled>` ✓ |
| `07_missing_required_slot` | Omit required slot | `Page_missing_required_slot_header` in note ✓ |

Each `.stderr` file is committed alongside its fixture and matches exactly.

---

## Acceptance criteria — all met

- [x] All seven fixture scenarios covered.
- [x] Each fixture fails to compile.
- [x] Each `.stderr` committed and matches exactly.
- [x] Messages name the mistake in terms the author recognises (component name + prop/slot name).
- [x] Errors point at or near the call site, not inside generated props internals.
- [x] All fixtures pass as part of `cargo test -p ferric-macros`.
- [x] No regressions in `ferric-macros` or `ferric` test suites (28 tests pass).
- [x] Issue #141 closed.
- [x] MSRV 1.82 maintained (no features beyond stable 1.82 used).

---

## Declared outputs

- `crates/ferric-macros/src/component.rs` — rewritten type-state builder macro
- `crates/ferric-macros/Cargo.toml` — trybuild dev-dependency added
- `crates/ferric-macros/tests/component_diagnostics.rs` — trybuild test runner
- `crates/ferric-macros/tests/compile_fail_component/01_missing_required_prop.{rs,stderr}`
- `crates/ferric-macros/tests/compile_fail_component/02_wrong_type_prop.{rs,stderr}`
- `crates/ferric-macros/tests/compile_fail_component/03_unknown_prop.{rs,stderr}`
- `crates/ferric-macros/tests/compile_fail_component/04_children_in_no_children_component.{rs,stderr}`
- `crates/ferric-macros/tests/compile_fail_component/05_fill_undeclared_slot.{rs,stderr}`
- `crates/ferric-macros/tests/compile_fail_component/06_fill_slot_twice.{rs,stderr}`
- `crates/ferric-macros/tests/compile_fail_component/07_missing_required_slot.{rs,stderr}`
- GitHub issue #141 closed
