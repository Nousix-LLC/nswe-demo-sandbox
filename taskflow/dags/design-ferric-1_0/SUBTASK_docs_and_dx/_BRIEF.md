# Task: Ferric 1.0 — documentation & developer experience (concern 6)

## Task Specification
**Slug**: SUBTASK_docs_and_dx
**Task Kind**: standard
**Status**: Pending

### Objective
Design the documentation and developer-experience bar for the 1.0: a guide, a tutorial, API docs, examples, and
a **cargo-generate** starter template. Bar: a new user can scaffold from the starter and follow the guide to a
working app. Design the DX plan and its testable bar — what docs and tooling must exist and how "a new user can
get to a working app" is checked — not the prose of the guide itself (that is downstream build work).

### Context
Part of the Ferric 1.0 framework design (see `../_GLOBAL.md`); owns `REQ-DX-*`. Today there is a crate README
and one `counter.rs` example. A 1.0 of a framework is judged in the first minute by whether a stranger can
start; the DX surface is part of the product, not an afterthought.

**Dependencies**: `SUBTASK_scope_and_requirements`.

### Distinct concerns to cover (name them; let your own evaluation decide how to split)
- **The learning path**: the guide + tutorial structure (what a new user reads, in what order, to a first
  working app); the examples set that must exist.
- **API docs**: the rustdoc/API-doc expectations for the public surfaces across the crates.
- **The cargo-generate starter**: what the starter template scaffolds, how a user runs it, and the "scaffold →
  working app" acceptance path.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context + constraints. |
| Contract | `../contracts/` | `REQ-DX-*` schema; your namespace. |
| 1.0 requirements | `../SUBTASK_scope_and_requirements/scope-and-requirements.md` | The frame to specialize. |
| Ferric baseline | `crates/ferric/README.md`, `examples/counter.rs`, the router/http READMEs | The docs/examples that exist to build on. |
| Peer precedent | Leptos book, Dioxus docs/CLI, Yew docs, `cargo-generate` templates (e.g. leptos starters) | Honest comparison of framework DX; cite by name. |

### Declared output
- `docs-and-dx.md` (this task's workspace) — the docs/DX plan + the `REQ-DX-*` register.
  Repo target `design/ferric/docs-and-dx.md`.

### Success criteria
- [ ] The guide/tutorial/API-docs/examples/starter are each specified with testable `REQ-DX-*` acceptance
      criteria (e.g. the starter scaffolds and builds; the tutorial's end state compiles), conforming to the
      contract schema.
- [ ] The "new user → working app" path is concrete and checkable (verification via `example_build` /
      `doc_inspection`).
- [ ] Peer DX approaches compared by name.

### Constraints
- Write `REQ-DX-*` only (identity I1). Design the DX bar, not the guide's prose. Load your own methodology.
- Honor the writing-voice rules.
