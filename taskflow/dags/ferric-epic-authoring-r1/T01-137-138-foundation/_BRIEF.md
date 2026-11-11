# _BRIEF.md — T01: Reactive core and VDOM foundation (#137, #138)

**Task ID:** ferric-authoring-137-138  
**Hub:** ferric-epic-authoring-r1  
**Branch:** `work/ferric-epic-authoring-r1`  
**Closes:** GitHub issues #137 and #138

---

## Objective

Create the epic branch and confirm that the existing reactive core and virtual DOM layer already
satisfy the acceptance criteria for issues #137 and #138. The existing code on `main` implements
both: `src/signal.rs` is a complete reactive system; `src/vdom.rs` and `src/dom.rs` are the full
virtual DOM and DOM patch runtime. Neither issue requires new feature code.

The concrete deliverable is an initial commit on the branch that records the baseline, confirms
the stated acceptance criteria are satisfied, closes both issues, and leaves the branch ready for
subsequent tasks.

---

## Inputs

- Repository `Nousix-LLC/nswe-demo`, main branch at HEAD `65413bbe59cb65641d6f1a85123a87f300900b83`.
- GitHub issue #137: Reactive state primitives (BAR-FERRIC-001).
- GitHub issue #138: Virtual DOM and keyed DOM patching (BAR-FERRIC-002).
- `design/ferric/scope-and-requirements.md` (on main) — the REQ-API-* register for reference.
- `design/ferric/release-bar.md` (on main) — BAR-FERRIC-001 and BAR-FERRIC-002.

---

## Acceptance criteria

### For #137 (BAR-FERRIC-001)

The ferric prelude exports `create_signal`, `create_memo`, `create_effect`, `batch`, `Signal`,
`Memo` from `crates/ferric/src/lib.rs`. These compile on stable Rust at MSRV 1.82. The existing
test suite in `src/signal.rs` demonstrates:

- `create_memo` does not recompute when its output is unchanged (memoization).
- `batch` defers effect execution until the batch closes.
- Scoped cleanup (`ReactiveScope::dispose`) unsubscribes reactive subscriptions without stale
  subscriber leaks.

The existing prelude is preserved verbatim — no previously exported item is removed or redefined.

### For #138 (BAR-FERRIC-002)

The existing test suite in `src/vdom.rs` demonstrates:
- Keyed list reorder produces `MoveChild` patches, not `Replace` — keyed nodes are moved, not
  recreated (see `keyed_children_reorder_emits_moves_not_replaces`).
- A partial attribute change (e.g. one attribute change in a subtree) produces a single `SetAttr`
  patch, not a wholesale tree replace.

The `src/dom.rs` browser test demonstrates that a signal write after mount updates only the
affected DOM text node (the `mount_renders_initial_view_and_reacts_to_signal_change` wasm test).

---

## Declared outputs

- Branch `work/ferric-epic-authoring-r1` created from `65413bbe59cb65641d6f1a85123a87f300900b83`.
- At least one commit on the branch establishing the baseline (the branch may start with just the
  main HEAD, plus a small commit documenting the baseline audit if any gap is found and filled).
- Issues #137 and #138 closed with a comment referencing the commit(s) on the branch that
  satisfy each issue's acceptance criteria.
- `COMPLETE.md` in this workspace recording which acceptance criteria passed.

---

## Constraints

- Do not add new feature code. The scope is the existing `crates/ferric` code on main.
- If a test is missing for a specific acceptance criterion (e.g., a test named after the
  criterion), add it — but add only what the criterion requires, nothing speculative.
- Do not modify any existing test, any existing public API, or any file outside `crates/ferric`.
- Leave the branch tip at a clean, CI-ready state for T02 to build on.
