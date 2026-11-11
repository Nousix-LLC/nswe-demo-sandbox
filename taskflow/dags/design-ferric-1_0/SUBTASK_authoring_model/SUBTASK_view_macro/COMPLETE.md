# COMPLETE — SUBTASK_view_macro (Ferric 1.0 `view!` macro authoring surface)

## Status
COMPLETED (resumed/reconstructed node). Declared output `view-macro.md` is present, well-formed, and meets
the brief's bar.

## What this task owns
The `view!` macro authoring surface — what an app author writes instead of hand-building
`VElement::new(..).child(..)` trees — its lowering onto the frozen `VNode` model, the `trybuild`-checkable
compile-diagnostics bar, and the `REQ-API-001 … REQ-API-029` register (band A, identity IA1). Design, not
the proc-macro's internal token expansion.

## What this resume invocation did
On dispatch the prior run's `view-macro.md` (≈650 lines) was present and substantively complete, but carried
two defects that are now fixed:

1. **Corrupted tail.** The prior write left stray `</content>` and `</invoke>` tool-call tags appended after
   the real content (after the "Folds into:" line). Removed; the file now ends cleanly on its last content
   line.
2. **Writing-voice tells (avoid-ai-writing pass, required by the brief).** Removed a cluster of the tells the
   writing-voice rules flag: "honest" used as a quality adjective on things that cannot hold a character
   (8 occurrences across §1.2, §1.5, §1.6, §1.9, §3, §4) and "stated plainly" candor-narration
   (3 occurrences across §1.2, §1.4, §4). Each was replaced with the plain claim; no substantive content
   changed. A final sweep confirms zero residual occurrences of these tells and no residual corruption
   markers.

## Grounding verified (evidence over memory)
Every baseline claim the document rests on was re-read from the checkout at
`taskflow/dags/ferric-foundation/checkout/crates/ferric/` and confirmed:
- `src/vdom.rs` — `VNode = Element(VElement) | Text(String)`; `VElement { tag, key: Option<Key>, attrs:
  Vec<(String,String)>, events: Vec<(EventKind, EventHandler)>, children: Vec<VNode> }`; `Key = String`;
  `EventKind = Click | Input`; `EventHandler = Rc<dyn Fn()>` (zero-arg); builders `new/key/attr/on/child/
  children`, `vdom::text`, `From<VElement> for VNode`; `all_keyed` keyed-diff precondition; `SetEvents` only
  on kind-set change; `Replace` on kind/tag change; `keyed_children_*` tests.
- `src/dom.rs` — `mount` wraps the whole render in one `create_effect`; a read subscribes it; a write re-runs
  the whole render and patches via the keyed diff; handlers bound to `click`/`input`; the
  `mount_renders_initial_view_and_reacts_to_signal_change` wasm-bindgen test backs REQ-API-008.
- `examples/counter.rs` — matches the §0 baseline snippet exactly.
- `src/lib.rs` — frozen `prelude` = `{Component, mount, batch, create_effect, create_memo, create_signal,
  Memo, Signal, EventKind, VElement, VNode}`; `text` lives in `vdom` (not the prelude), so re-exporting it is
  additive — exactly as §2 states.

## Success criteria (brief) — met
- [x] Surface facets (elements/text/attrs, events + open set, interpolated reactive values, conditionals,
      lists/keys) shown with author-side snippets concrete enough for a code DAG to build — §1.1–1.10.
- [x] Lowering onto `VNode`/keyed-diff stated as additive; no frozen `prelude` item redefined — §2 + IA4.
- [x] Compile-diagnostics bar is `trybuild`-checkable with stated example failures — §3.
- [x] `REQ-API-001..029` acceptance criteria testable; every criterion uses an inherited
      `verification_method` (`automated_test` | `example_build` | `doc_inspection`) — §5, IA6.
- [x] Peer view-macros (Leptos `view!`, Yew `html!`, Dioxus `rsx!`, Sycamore `view!`; Solid/Vue 3 analogs)
      compared by name with ergonomic trade-offs — §4.

## Identities upheld (asserted by SUBTASK_synthesis, not here)
- IA1 (band 001–029 only), IA2 (macro side of the invocation seam — §1.7/§5 F), IA4 (additive over the frozen
  surface), IA6 (`trybuild`-checkable diagnostics + inherited verification vocab). IA3 (context) and IA5
  (one consolidated deliverable) are composed/asserted downstream.

## Output
- `view-macro.md` (this workspace) — folds into `../authoring-model.md` at `SUBTASK_synthesis`.
