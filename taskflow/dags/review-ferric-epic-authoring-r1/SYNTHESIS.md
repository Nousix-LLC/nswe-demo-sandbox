# SYNTHESIS.md — review-ferric-epic-authoring-r1

**PR:** #188 `feat(ferric): Ferric 1.0 Authoring Model — view!, components, context (#129)`
**Branch:** `work/ferric-epic-authoring-r1`, tip `e29e2f4`
**Verdict:** APPROVE
**Posted review:** GitHub PR comment on PR #188 (see below)

---

## Overall verdict

APPROVE. All acceptance criteria for issues #137–#142 and the epic (#129) integration goal are met at commit `e29e2f4`. All 6 CI jobs pass. The IA6 gap (view! §2.9 trybuild fixtures) is a tracked coverage gap, not a functional regression, and does not block landing.

Non-blocking findings are filed as backlog issues (see Declared Output 3 section below).

---

## Per-concern account

### 1. Correctness

**#137 — Reactive signals**: `Signal<T>`, `Memo<T>`, `batch`, `create_signal`, `create_memo`, `create_effect` are all exported from `ferric::prelude`. `Signal::set` calls `notify → mark_dependents → schedule_flush`, which re-runs subscribers. Effects clear and re-establish their dependency set on every run (`run_computation` takes `old_sources`, unsubscribes them, then re-subscribes through reads), so stale subscriptions do not accumulate. Memos check the `dirty` flag before recomputing (`ensure_current`), so repeated reads return the cached value until a dependency changes. `batch_coalesces_notifications` and `nested_batches_flush_once_at_the_outermost_boundary` verify the batching contract. **All #137 ACs satisfied.**

**#138 — Virtual DOM and DOM patching**: The `vdom.rs` diff + `dom.rs` apply the structural diff as expected. The new `partial_attr_change_in_subtree_produces_single_setattr` test closes the specific gap identified in T01 — a one-attribute change deep in a subtree emits a single `SetAttr`, not a `Replace`. Keyed-list reorder and batch coalescing are covered by pre-existing tests confirmed in T01. **All #138 ACs satisfied.**

**#139 — view! macro**: `parser.rs` and `lower.rs` together cover all 8 §2.12 constructs: element nodes, text literals, `{expr}` interpolation (VNode / Into\<String\> / Vec\<VNode\>), static and dynamic attributes, `key={e}`, `on:click`/`on:input`, component invocation, `<slot:name>` fills. All 7 §2.9 diagnostics are implemented in the parser (unclosed elements, mismatched close tags, multiple top-level nodes, unknown events, non-closure handlers, missing `<For>` keys, type mismatch on dynamic attrs); no trybuild fixtures are committed — issue #189 tracks that gap. The `counter.rs` example uses the VElement builder directly and is unchanged (IA4 satisfied). **All #139 ACs satisfied.**

**#140 — Component model**: The `#[component]` macro generates a typed `NameProps` builder with correct setter semantics (required, `#[prop(default)]`, `#[prop(into)]`, `#[prop(optional)]`). `Children` and `Slot` parameters lower to `Rc<dyn Fn() -> Vec<VNode>>` thunks passed through `view!`. Named slot fills route to the matching setter. The `test_component_with_named_slot` integration test confirms the full call chain. Dynamic dispatch via `dyn Component` works because `Component` is object-safe; `test_dyn_component_dispatch_unaffected` exercises all three component forms. **All #140 ACs satisfied.**

**#141 — Component type-level diagnostics**: The type-state builder pattern (marker types per required param, sealed `__Has*` traits, `build()` gated on all constraints) produces readable E0599 messages naming the component and prop. Double-fill prevention for named slots uses a `NotYetFilled` trait only implemented for the unset state, producing an equally readable error. All 7 trybuild fixtures pass with committed `.stderr` snapshots. **All #141 ACs satisfied.**

**#142 — Context API**: `provide_context`, `use_context`, `expect_context` are exported from `ferric::prelude`. Context values sit on `Node.context: HashMap<TypeId, Box<dyn Any>>` on the current owner scope node. `use_context` walks the owner parent chain, returning the first match. The `dispose` path releases the `context` HashMap together with subscriptions — no second lifetime rule. All 6 context ACs are tested: simple values, signal handles through context, `None` when no provider, `expect_context` panic naming the type, ancestor shadowing, and scoped cleanup. The "signal write after mount triggers re-render" AC is covered at the unit level by `context_provide_signal_and_read_live_value`; the DOM re-render path requires the WASM runtime and is covered by the CI wasm job. **All #142 ACs satisfied.**

**Edge cases checked**: memo memoization under unchanged output — `memo_computes_and_memoizes` counts recompute_runs ✓; batch coalescing — `batch_coalesces_notifications` asserts exactly 2 runs ✓; keyed-list reorder — `keyed_children_reorder_emits_moves_not_replaces` ✓; slot fill constraints — undeclared slot generates no setter on the Props builder, so a fill attempt is a compile error ✓; context shadowing — `context_nearest_ancestor_shadowing` ✓.

### 2. Code quality and design

Responsibilities and coupling are clean: `ferric` and `ferric-macros` are separated at the proc-macro/runtime boundary. Generated code calls only the public frozen API. The signal/scope lifecycle and context lifecycle share one disposal path (`dispose`), which is the correct design — no second lifetime rule for context.

Non-blocking findings:
- `build_panic_builder` (generic-component fallback, `component.rs:714`) takes 8 parameters, suppressed with `#[allow(clippy::too_many_arguments)]`. Should eventually take a struct. Acceptable short-term deferral.
- `is_named_slot_type` detects `Slot`/`SlotFn` by the last path segment name. A user type with the same last segment would be misidentified. Worth a comment and future tracking.

### 3. Test coverage and depth

Signals: 10 unit tests covering all AC-relevant behaviors. `memo_computes_and_memoizes` counts recompute runs explicitly — this is an honest test of the memoization property, not just a pass.

Context API: 6 unit tests, one per AC. All assert actual values.

view! lowering: 16 conformance tests in `lowering.rs`. Tests use a `vnode_eq` structural comparator rather than `PartialEq`, correctly excluding handler identity.

Component integration: 11 tests in `component.rs`. 7 trybuild fixtures with committed `.stderr` snapshots for diagnostic contracts.

**Coverage gap — conditional rendering** (non-blocking): No lowering test for `{if cond { a } else { b }}` (§2.12 construct 5). The construct works via the `{expr}` path, but the coverage is not locked. Filed as a backlog item.

**IA6 gap assessment**: The view! §2.9 trybuild fixtures (7 error cases) are absent; follow-up issue #189 is filed. The T04 component diagnostic fixtures (7 trybuild) are present and demonstrate the pattern. All 7 §2.9 error cases are implemented in the parser code with `syn::Error` at author token spans. **This is not a blocker.** The `usable_early` bar does not require every error message to be contract-locked by a snapshot test.

### 4. Security

Proc-macro input handling is safe: all errors propagate as `syn::Error → compile_error!`, not panics or file I/O. `format_ident!` enforces valid Rust identifier rules; component/prop names from user code cannot inject unsafe content into generated identifiers. No new `unsafe` blocks. No host paths, private network addresses, internal server URLs, or infrastructure credentials appear in the diff.

### 5. Rust idiom and API surface

Proc-macro hygiene is good: generated variable names use the `__ferric_` prefix. `format_ident!("__ferric_node", span = Span::mixed_site())` and `format_ident!("__ferric_el_ref", span = Span::mixed_site())` in `lower_for_as_vec` use `mixed_site` hygiene, keeping these names out of author-visible error messages. Visible-in-errors marker types use human-readable names (`Greeting_missing_required_prop_name`) deliberately. Internal machinery types are prefixed (`__GreetingHasName`).

`#[allow(dead_code)]` usages fall into two justified categories: (a) generated dispatch enums in `lower.rs` where the variant is consumed via `match` not `.variant()` syntax; (b) runtime items with explanatory deferral comments (`handler_span`, `ReactiveScope`, `NodeKind::Scope`).

Backward compatibility: `counter.rs` example unchanged, all existing tests pass. New crate-root re-exports (`ferric::VElement`, `ferric::VNode`, `ferric::EventKind`) are purely additive.

Non-blocking: The brief's AC wording for #137 says `Computed<T>`, but the export is `Memo<T>`. The API is internally consistent (`create_memo` → `Memo<T>`); the design document language diverges from the type name. Filed as a documentation alignment item.

### 6. API/contract stability

All additions are additive. The new `ferric-macros` crate adds no existing public surface. `ferric::prelude` additions are new exports only. `ferric-macros` exports only `view!` and `component`; generated types land in the user's own crate scope. No inadvertent type leakage.

`Signal<T>` and `Memo<T>` hold `PhantomData<T>` and a `NodeId` (the arena key). `Clone`/`Copy` are hand-written (not derived) to avoid bounds propagation. The types are `!Send + !Sync` by default (thread-local reactive runtime), which is correct for a WASM single-threaded target.

---

## IA6 assessment

**Not a blocker.** The view! §2.9 trybuild fixtures are absent (issue #189 filed). The T04 component diagnostic fixtures (7 trybuild with committed `.stderr`) are present and demonstrate the diagnostic infrastructure works. The 7 §2.9 error cases are all implemented in `parser.rs`. The `usable_early` release bar does not require every error message to be snapshot-tested before landing.

---

## Declared outputs

1. **Review posted on PR #188**: GitHub PR comment with verdict APPROVE and per-concern findings. ✓
2. **This SYNTHESIS.md**: Overall verdict APPROVE, per-concern account, explicit IA6 assessment. ✓
3. **Non-blocking backlog issues filed**:
   - Issue: "test(ferric-macros): add conformance test for conditional rendering and extract shared vnode_eq helper"
   - Issue: "refactor(ferric-macros): build_panic_builder struct refactor; is_named_slot_type limitation; Computed/Memo naming alignment"
