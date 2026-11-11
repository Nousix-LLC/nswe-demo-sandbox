# _GLOBAL.md — ferric-epic-authoring-r1 hub

**Hub:** ferric-epic-authoring-r1  
**Owner:** overseer/I187  
**Branch:** `work/ferric-epic-authoring-r1`  
**Base commit:** `65413bbe59cb65641d6f1a85123a87f300900b83` (main HEAD at fork time)  
**Repo:** `Nousix-LLC/nswe-demo`  
**Closes:** #137, #138, #139, #140, #141, #142 (all sub-issues of epic #129)

---

## What this subtree builds

The Ferric 1.0 Authoring Model (`usable_early`): the declarative authoring surface over the existing
reactive/VDOM foundation. When all six issues are closed, an author can write reactive components in
angle-bracket `view!` syntax, compose them with typed props and named slots, pass state down without
prop drilling via context, and render keyed lists — a complete client-side authoring story.

The design authority is `design/ferric/authoring-model.md` on `main` (merged PR #128). No sub-task
redefines that specification; every sub-task satisfies it.

---

## Foundation audit (basis for T01)

The existing code on `main` already fully implements:
- **Reactive signals** (`src/signal.rs`): generational arena, `Signal<T>`, `Memo<T>`, `create_signal`,
  `create_memo`, `create_effect`, `batch`, `ReactiveScope`, scoped disposal, full test suite.
- **Virtual DOM + keyed diff** (`src/vdom.rs`): `VNode`, `VElement`, `Patch`, `diff`, keyed and
  positional child reconciliation, full test suite.
- **DOM runtime** (`src/dom.rs`): `mount`, reactive re-render loop, keyed patch application,
  event-handler binding/unbinding.
- **Prelude exports**: `create_signal`, `create_memo`, `create_effect`, `batch`, `Signal`, `Memo`,
  `Component`, `mount`, `EventKind`, `VElement`, `VNode`.

Issues #137 and #138 are satisfied by this baseline. T01's work is to establish the branch, confirm
the existing tests demonstrate the acceptance criteria, and close both issues.

The new additions (T02–T05) are strictly additive: they add a proc-macro crate, new types, and new
free functions. No existing public export is modified.

---

## Task tree and dependency graph

```
T01-137-138-foundation   (branch setup + verify #137 + #138)
        |
T02-139-view-macro       (view! proc-macro, trybuild diagnostics, closes #139)
        |
T03-140-component        (#[component] macro + Children/Slot/SlotFn<T>, closes #140)
       / \
T04-141   T05-142        (parallel: component diagnostics closes #141;
  diagnostics  context    context API closes #142)
       \ /
T06-synthesis            (PR, CI check, closes all issues, SYNTHESIS.md)
```

| Task ID                      | Workspace path               | Depends on    |
|------------------------------|------------------------------|---------------|
| ferric-authoring-137-138     | T01-137-138-foundation/      | (none)        |
| ferric-authoring-139-view    | T02-139-view-macro/          | T01           |
| ferric-authoring-140-comp    | T03-140-component/           | T02           |
| ferric-authoring-141-diag    | T04-141-diagnostics/         | T03           |
| ferric-authoring-142-ctx     | T05-142-context/             | T03           |
| ferric-authoring-synthesis   | T06-synthesis/               | T04, T05      |

---

## Shared branch protocol

Every code task (T01–T05) commits to `work/ferric-epic-authoring-r1`. Because tasks are serial
except T04 and T05, each task starts by pulling the branch tip left by its predecessor and continues
from there. T04 and T05 may work in parallel on separate commits; T06 merges the final tip.

T06 creates the PR and verifies CI. The PR body references all closed issues (#137–#142).

---

## Contract reference

Contracts are at `contracts/_MANIFEST.yaml` relative to this hub. The identity assertions below
are what the SYNTHESIS.md must confirm pass before the PR is opened.

---

## Subtree posture

- **Scope**: `crates/ferric` only, plus a new proc-macro crate `crates/ferric-macros/` and
  workspace-level `Cargo.toml` / `Cargo.lock` changes to register it.
- **No breaking changes**: the frozen prelude surface as of main is preserved verbatim (identity IA4).
- **MSRV**: `rust-version = "1.82"` (workspace `Cargo.toml`; stable-only features).
- **No force-push to main**, no changes outside the ferric scope.
