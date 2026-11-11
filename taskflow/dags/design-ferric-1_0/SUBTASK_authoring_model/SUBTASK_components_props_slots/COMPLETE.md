# COMPLETE — SUBTASK_components_props_slots

## What was done
Designed the Ferric 1.0 component authoring model — what an author writes to declare and compose a reusable
component — and its testable `REQ-API-030..059` bar. The deliverable states the authoring surface and what
must hold against it (design, not implementation; no `#[component]` macro-expansion internals).

This node was a reconstructed-resume: the declared output `components-props-slots.md` already existed from a
prior interrupted invocation. This invocation verified it against the brief, the subtree contract, and the
Ferric baseline, repaired a defect, and finalized it.

## Output produced
- `components-props-slots.md` — the component model (central decision, typed props, children, named slots,
  composition, the additive-lowering story, diagnostics bar, the IA2 component-side seam table, by-name peer
  comparison) and the `REQ-API-030..052` register slice (`053..059` reserved headroom) with testable
  acceptance criteria. Folds into `../authoring-model.md` at synthesis.

## Verification performed
- **Grounded against baseline source** (`taskflow/dags/ferric-foundation/checkout/crates/ferric/src/`):
  confirmed `trait Component { fn render(&self) -> VNode }` with the blanket `impl<F: Fn() -> VNode>`
  (`component.rs`); the two-variant frozen `VNode` and `VElement.children: Vec<VNode>` with `.child` /
  `.children` builders (`vdom.rs`); the frozen `prelude` exports (`lib.rs`); the render-inside-effect reactive
  model. Every load-bearing claim checks out.
- **Contract conformance**: ids confined to band `030..059` (IA1); component-side of invocation seam IA2
  stated as a both-directions-closed correspondence table; additive over the frozen surface, nothing redefined
  (IA4); every acceptance criterion uses an inherited `verification_method`
  (`automated_test` | `example_build` | `doc_inspection`) (IA6).
- **Success criteria**: props (required/optional/defaulted/into/reactive), children, named + parameterized
  slots, and composition each shown with author-facing snippets; peers (Leptos, Sycamore, Dioxus, Yew)
  compared by name with ergonomic trade-offs stated; the `PartialEq` divergence argued from the baseline
  reactive runtime.
- **Defect repaired**: the prior interrupted write had leaked its `engine_write` XML envelope
  (`</content>`/`</invoke>`) into the file tail; removed so the file ends on its last content line.
- **avoid-ai-writing pass**: cleared three tells in §10's closing paragraph — "stated plainly" (narrating
  candor), "genuine design choice" (hollow intensifier), and "the honest consequence" (a moral adjective on an
  abstraction); each replaced with a plain, checkable statement.

## How it composes with the parent
Supplies the component spoke of the authoring model. `SUBTASK_synthesis` folds `components-props-slots.md`
with `view-macro.md` and `context.md` into `../authoring-model.md` and merges the `REQ-API-*` register; the
synthesis gate asserts IA1/IA2/IA4/IA5/IA6. The IA2 macro-side counterpart is owned by `SUBTASK_view_macro`;
this node owns and closes the component-declaration side.
