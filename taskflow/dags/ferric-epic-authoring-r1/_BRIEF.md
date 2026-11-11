# _BRIEF.md — ferric-epic-authoring-r1

**Task Kind**: code DAG (swe-coder)
**Goal**: Ferric 1.0 — Authoring Model (`usable_early`), epic #129
**Branch**: `work/ferric-epic-authoring-r1`
**Scope**: `crates/ferric` only
**Closes issues**: #137, #138, #139, #140, #141, #142
**Repo**: `Nousix-LLC/nswe-demo`

---

## Objective

Implement the Ferric 1.0 Authoring Model — the reactive signals, virtual DOM, `view!` macro, component
model, compile-time diagnostics, and context API that the design specifies. This is the first
`usable_early` epic; it has no blockers and no dependency on other in-flight epics. When every sub-issue
under epic #129 is met, an author can write reactive components, compose them with props and slots, pass
values through context, and render keyed lists — a working client-side foundation.

The design for this epic is in the repository at `design/ferric/authoring-model.md` and
`design/ferric/scope-and-requirements.md` (merged in PR #128; now on `main`). The release bar criteria
this epic satisfies are in `design/ferric/release-bar.md` (BAR-FERRIC-001, 002, 007, 008, 009, 010, 011).
All design documents are on `main`; read them from the repository's `main` branch.

The existing code baseline for `crates/ferric` is on `main`: reactive signals (`src/signal.rs`), a minimal
`VNode` model (`src/vdom.rs`), coarse-grained `mount`/`diff` DOM rendering (`src/dom.rs`), and the
counter example (`examples/counter.rs`). The authoring model builds on and does not break this baseline.

---

## Sub-issues and acceptance criteria

Each sub-issue is a DAG-verifiable acceptance criterion. The PR that closes this epic must account for
each one in `SYNTHESIS.md`.

### #137 — Reactive state primitives (BAR-FERRIC-001)

`create_signal`, `create_memo`, `create_effect`, and `batch` are present in the `ferric` prelude and
compile on stable Rust at the declared MSRV. Tests confirm:
- `create_memo` does not recompute when its output is unchanged.
- `batch` defers effect execution until the batch closes.
- Scoped cleanup unsubscribes every reactive subscription owned by a dropped scope without observable leaks.
- The `ferric` prelude as exported at the baseline compiles at 1.0 without modification to any
  previously exported item.

Depends on: none.

### #138 — Virtual DOM and keyed DOM patching (BAR-FERRIC-002)

Tests demonstrate:
- A partial signal change updates only the affected DOM nodes — not the whole subtree.
- A keyed list reorder moves existing DOM nodes rather than destroying and recreating them.

Depends on: #137.

### #139 — `view!` macro surface and compile-time diagnostics (BAR-FERRIC-007, BAR-FERRIC-008)

The stated set of valid `view!` inputs — HTML elements with standard attributes and properties, dynamic
expressions, conditional rendering, keyed list rendering via `<For key=... each=... view=...>`, and
component invocations — all compile without modification.

The stated set of malformed inputs — unrecognized element names, missing required attributes, structurally
invalid expressions — each produce a compile-time diagnostic that names the problem in terms of the
author's code rather than macro internals. `trybuild` tests for this set pass in CI.

Depends on: #138.

### #140 — Component model — props, children, named slots, and dynamic dispatch (BAR-FERRIC-009)

A component function accepts:
- Required and optional props (with defaults).
- A `children: VNode` parameter.
- Named slots; parameterized slot closures (`SlotFn<T>`).
- Prop conversion via a declared `From` implementation.
- Dynamic invocation through a `dyn Component` trait object.

Stated examples for each of these forms compile and render correctly.

Depends on: #139.

### #141 — Component type-level diagnostics (BAR-FERRIC-010)

The stated set of component authoring mistakes — missing required props, type mismatches in prop values,
misused slots — each produce a compile-time error that names the problem at the call site rather than
inside framework internals. `trybuild` tests for this set pass in CI.

Depends on: #140.

### #142 — Context and dependency injection (BAR-FERRIC-011)

`provide_context`, `use_context` (returning `Option`), and `expect_context` (panicking with a clear
message when the value is absent) are present in the `ferric` prelude. A value provided does not need
to be threaded through every intermediate component. Stated examples for each form compile and tests pass.

Depends on: #140.

---

## Design references (all on `main`)

- `design/ferric/authoring-model.md` — the full authoring model specification: the `view!` macro
  (elements, text, attributes, event handlers, interpolated reactive values, control flow, lists and
  keys, component invocation, invocation seam IA2), the component model (props, children, named slots,
  `SlotFn<T>`, converting props, dynamic dispatch, context seam IA3, invocation forms), context API
  (`provide_context`/`use_context`/`expect_context`), and compile-time diagnostics. This is the
  authoritative specification for every sub-issue.
- `design/ferric/scope-and-requirements.md` — the full `REQ-API-*`, `REQ-FW-*` requirements register.
  The sub-issues trace to individual REQ-IDs; read the REQ body for the normative statement.
- `design/ferric/release-bar.md` §3 — BAR-FERRIC-001, 002, 007, 008, 009, 010, 011. Each bar criterion
  is the external verifiable condition the sub-issue must satisfy.

---

## Concerns to cover

Each concern is a check the DAG runs; the brief describes the goal and the bar.

1. **Reactive core correctness** (#137): `create_signal`, `create_memo`, `create_effect`, `batch`, and
   scoped cleanup behave per BAR-FERRIC-001. The existing signal primitives may already satisfy this
   partially; audit and complete, do not duplicate.

2. **VDOM / keyed-diff correctness** (#138): Partial-state updates and keyed list reorders behave per
   BAR-FERRIC-002. The existing `src/vdom.rs` and `src/dom.rs` are the baseline — audit their keyed
   path (`diff_children`, the `all_keyed` precondition) and add tests that confirm the stated behaviors.

3. **`view!` macro surface** (#139): The macro covers the full surface in `design/ferric/authoring-model.md`
   §2 (elements, text, attributes, `on:<event>`, interpolation, control flow, `<For>`, component
   invocation) and produces builder-identical output to hand-built `VNode` trees
   (`authoring-model.md` §2.2–2.8). The macro lives as a separate proc-macro crate; scope the crate
   structure to fit the existing workspace.

4. **`view!` diagnostics** (#139): A trybuild test suite captures the diagnostic set from
   `authoring-model.md` §2.9; every error message names the author's mistake, not macro internals.

5. **Component model** (#140): Props, `children`, named slots, `SlotFn<T>`, converting props,
   `dyn Component` per BAR-FERRIC-009 and `authoring-model.md` §3. Use the `#[component]` derive/proc-
   macro path the design specifies; audit the existing `src/component.rs` baseline.

6. **Component diagnostics** (#141): A trybuild test suite captures the diagnostic set from
   `authoring-model.md` §3 / BAR-FERRIC-010; every compile-time error names the call-site mistake.

7. **Context API** (#142): `provide_context`, `use_context`, `expect_context` per BAR-FERRIC-011 and
   `authoring-model.md` §4. The context value must not require threading through intermediate components.

8. **Baseline compatibility** (#137): The prelude exported by the existing `ferric` baseline compiles
   without modification to any previously exported item (BAR-FERRIC-001; `REQ-FW-009`). No existing
   public surface is broken.

9. **CI green**: All CI jobs (`fmt`, `clippy`, `test`, `wasm`, `doc`) pass for the branch. The
   `wasm-bindgen-test` suite (if applicable) passes. `trybuild` tests pass in `cargo test`.

10. **PR scope**: The PR scope is `crates/ferric` only. No changes to `crates/chirp-*` or `deploy/`
    or any file outside `crates/ferric` and its proc-macro crate (if added), except to update
    `Cargo.lock` and workspace `Cargo.toml` if adding a new crate to the workspace.

---

## Declared output

- Commits on `work/ferric-epic-authoring-r1`, scoped to `crates/ferric`.
- One PR that closes #137, #138, #139, #140, #141, #142 (all sub-issues of epic #129).
- `SYNTHESIS.md` at the DAG root that accounts for each sub-issue (met, or not and why) and states
  the machine-gate verdict (PASS / FAIL / PARTIAL).

---

## Constraints

- Branch: `work/ferric-epic-authoring-r1`. Create from `main` at the current HEAD
  (`65413bbe59cb65641d6f1a85123a87f300900b83`).
- Do not force-push. Do not modify `crates/chirp-*`, `deploy/`, or anything outside the
  `crates/ferric` scope (plus workspace files for a new proc-macro crate, if added).
- Do not prescribe a decomposition, a methodology, or which crates to load. The design documents
  are the authority; the DAG selects its own approach and loads its own methodologies.
