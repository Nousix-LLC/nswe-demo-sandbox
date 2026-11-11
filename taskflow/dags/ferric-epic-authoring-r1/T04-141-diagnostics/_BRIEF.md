# _BRIEF.md — T04: Component type-level diagnostics (#141)

**Task ID:** ferric-authoring-141-diag  
**Hub:** ferric-epic-authoring-r1  
**Branch:** `work/ferric-epic-authoring-r1` (with component model from T03)  
**Closes:** GitHub issue #141

---

## Objective

Add a `trybuild`-based compile-fail test suite that covers the diagnostic requirements for
component authoring mistakes per `design/ferric/authoring-model.md` §3.7 and BAR-FERRIC-010.
Each fixture is a small Rust file that triggers exactly one kind of component authoring mistake;
the committed `expected` stderr must name the mistake in terms of the author's code, not in
terms of macro internals or generated type names.

This task adds test fixtures only. If the existing `#[component]` implementation (from T03)
already emits the correct messages, the work is to write and commit the fixtures. If a message
needs improvement to meet the bar, the fix belongs here — the diagnostic quality is part of this
task's acceptance criteria.

---

## Inputs

- Branch `work/ferric-epic-authoring-r1` as left by T03.
- `design/ferric/authoring-model.md` §3.7 — the required diagnostic set for component mistakes.
- `design/ferric/release-bar.md` §BAR-FERRIC-010.
- GitHub issue #141 and its acceptance criteria.
- The `trybuild` crate (to be added as a dev-dependency if not already present after T02).

---

## Acceptance criteria (from issue #141 and authoring-model.md §3.7)

Each row below requires a `trybuild` compile-fail fixture with a committed `stderr` whose
message contains the stated phrasing (or equivalent phrasing in terms of the author's code):

| Author mistake | Required message character |
|---|---|
| Omit a required prop on a `#[component]` invocation | Names the missing prop and the component: "missing required prop `<name>` on `<Component>`" or equivalent |
| Pass a prop value of the wrong type | Names the prop and expected type: "prop `<name>` on `<Component>` expects `<type>`" or equivalent |
| Pass a prop the component does not declare | Names the unknown prop and the component: "`<Component>` has no prop `<name>`" or equivalent |
| Nest children inside a component with no `children` parameter | States the component does not accept children |
| Fill a slot the component did not declare | Names the undeclared slot and the component |
| Fill a slot twice | Names the doubly-filled slot and the component |
| Omit a required slot | Names the missing slot |

Each fixture must:
- Fail to compile.
- Produce a `stderr` that is committed alongside the fixture and matches exactly.
- Name the mistake in terms that an author (not a framework implementer) would recognize.
- Point at or near the call site — not deep inside the generated props type.

All fixtures pass as part of `cargo test`.

---

## Declared outputs

- `trybuild` compile-fail fixtures covering all seven cases above, with committed `stderr` files.
- Any diagnostic-quality improvements to `crates/ferric-macros/` needed to meet the bar.
- Issue #141 closed.
- `COMPLETE.md` in this workspace.

---

## Constraints

- Changes to `crates/ferric-macros/` are permitted when needed to improve diagnostic quality.
- Do not change any behavior that is already correct — only improve messages where the bar is
  not yet met.
- Fixtures live in `crates/ferric/tests/` or `crates/ferric-macros/tests/` (match the
  convention established by T02 for view! diagnostic fixtures).
- MSRV: stable Rust 1.82.
- Leave the branch at a clean, CI-ready state for T06.
