# Task: Ferric 1.0 — server-side rendering + hydration (concern 2, the one must-have)

## Task Specification
**Slug**: SUBTASK_ssr_hydration
**Task Kind**: standard
**Status**: Pending

### Objective
Design the isomorphic rendering architecture that lets Ferric render a component tree to HTML on the server
(an **Axum** integration) and **hydrate it in the browser without re-rendering**: how reactive state is carried
server→client and resumed, and how event listeners are wired on hydrate. This is the **single must-have** of
the 1.0. State the architecture and its testable bar — what the framework must do, not the final implementation.

### Context
Part of the Ferric 1.0 framework design (see `../_GLOBAL.md`); owns `REQ-SSR-*`. Builds on today's client-side
reactivity + keyed-VDOM foundation (`crates/ferric`). The guiding bar: **a server-rendered page becomes
interactive by hydration with no client-side re-render.**

**Dependencies**: `SUBTASK_scope_and_requirements` (the 1.0 requirements + MVP-vs-1.0 line to specialize).

### Distinct concerns to cover (name them; let your own evaluation decide how to split)
- **Render-to-HTML on the server**: turning a `VNode`/component tree into HTML off-wasm; the Axum integration
  shape (what a server app wires up); how the existing component model renders without a DOM.
- **Hydration without re-render**: how the client adopts the server-rendered DOM and attaches reactivity and
  event listeners without rebuilding the subtree; how mismatches are detected/handled.
- **State carry & resume**: how reactive state created on the server is serialized, shipped to the client, and
  resumed so hydration is consistent (and the relationship to async resources resolved on the server).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context + constraints. |
| Contract | `../contracts/` | `REQ-SSR-*` schema, stage vocabulary; your namespace. |
| 1.0 requirements | `../SUBTASK_scope_and_requirements/scope-and-requirements.md` | The `REQ-FW-*` frame + the 1.0 line to specialize. |
| Ferric baseline | `crates/ferric/` (`signal`, `vdom`, `component`, `dom`) | The reactive/VDOM/DOM model SSR must render and hydration must adopt. |
| Peer precedent | Leptos SSR+hydration, Dioxus SSR, Sycamore, Solid/Qwik (resumability contrast) | Honest comparison of isomorphic approaches; cite by name. |

### Declared output
- `ssr-hydration.md` (this task's workspace) — the SSR/hydration architecture + the `REQ-SSR-*` register.
  Repo target `design/ferric/ssr-hydration.md`.

### Success criteria
- [ ] The architecture states how a component tree renders to HTML on the server, how the client hydrates
      **without re-rendering**, and how state is carried and resumed — concretely enough for a code DAG to build.
- [ ] `REQ-SSR-*` acceptance criteria are testable (e.g. an automated test / example build asserting no
      client re-render on hydrate), conforming to `../contracts/id_and_traceability_schema.yaml`.
- [ ] At least one `REQ-SSR-*` is `stage: one_oh` and flagged as the gating must-have (feeds identity I4).
- [ ] Peer approaches compared by name; the chosen approach's trade-offs stated plainly.

### Constraints
- Write `REQ-SSR-*` only (identity I1). Design, not implementation. Axum is the named server integration.
- Load your own isomorphic-rendering / hydration methodology. Honor the writing-voice rules.
