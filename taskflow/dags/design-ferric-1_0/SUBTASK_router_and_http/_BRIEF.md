# Task: Ferric 1.0 — router + HTTP/JSON client (concern 5; absorbs board #5 and #6)

## Task Specification
**Slug**: SUBTASK_router_and_http
**Task Kind**: standard
**Status**: Pending

### Objective
Design two capabilities a real app needs: a **router** (route params, nested routes, links/navigation) and an
**HTTP/JSON client** (typed fetch). Reconcile both with the crates that **already exist** —
`crates/ferric-router` (#5) and `crates/ferric-http` (#6), each with a frozen public `prelude` surface —
**extending/superseding** them into the 1.0 design, never duplicating. Bar: the journeys a real app needs
(nested routing, linking, typed JSON fetch) are expressible.

### Context
Part of the Ferric 1.0 framework design (see `../_GLOBAL.md`); owns `REQ-RT-*` and `REQ-HTTP-*`. This concern
**absorbs board issues #5 and #6**. The existing crates are walking-skeleton composition roots: `ferric-router`
exposes `Params`, `RoutePattern`, `Router`, `navigate`, `current_path`, `link`; `ferric-http` exposes
`Client`/`ClientBuilder`, `RequestBuilder`, `Response`, `Error`/`Result`. The 1.0 design must build on these
frozen surfaces additively (identity I9) and say exactly how the 1.0 extends what #5/#6 already scoped.

**Dependencies**: `SUBTASK_scope_and_requirements`.

### Distinct concerns to cover (name them; let your own evaluation decide how to split)
- **Router**: route table, path params, **nested routes**, in-app links and History-API navigation, the
  reactive outlet; the relationship to the frozen `ferric-router` surface and what the 1.0 adds (e.g. nested
  routing if not yet present).
- **HTTP/JSON client**: typed JSON fetch (serde), request building, error model; the relationship to the
  frozen `ferric-http` surface and what the 1.0 adds.
- **The fold of #5/#6**: how each existing board issue is superseded or extended by this design (so the release
  plan can record the fold and `file_backlog` edits #5/#6 rather than duplicating them — identity I7).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context + constraints. |
| Contract | `../contracts/` | `REQ-RT-*` / `REQ-HTTP-*` schema; your namespaces. |
| 1.0 requirements | `../SUBTASK_scope_and_requirements/scope-and-requirements.md` | The frame to specialize. |
| Router scaffold | `crates/ferric-router/` (frozen `prelude`, `README`) | What exists (#5); extend additively. |
| HTTP scaffold | `crates/ferric-http/` (frozen `prelude`, `README`) | What exists (#6); extend additively. |
| Board issues | #5 `ferric-router`, #6 `ferric-http` under epic #1 | The issues to fold; read their current scope. |
| Peer precedent | leptos_router, Dioxus router, `reqwest`/`gloo-net` (fetch) | Honest comparison; cite by name. |

### Declared output
- `router-and-http.md` (this task's workspace) — router + HTTP/JSON design, with `REQ-RT-*` and `REQ-HTTP-*`
  registers and an explicit statement of how #5 and #6 are superseded/extended. Repo target
  `design/ferric/router-and-http.md`.

### Success criteria
- [ ] Nested routing, route params, links/navigation, and typed JSON fetch are each specified with testable
      `REQ-RT-*`/`REQ-HTTP-*` acceptance criteria, conforming to the contract schema.
- [ ] The design is additive over the frozen `ferric-router`/`ferric-http` `prelude` surfaces (identity I9);
      any change to an existing surface is called out as additive, never a silent redefinition.
- [ ] The fold of #5 and #6 is explicit (what each becomes under the 1.0 plan), feeding identity I7.
- [ ] Peer routers/HTTP clients compared by name.

### Constraints
- Write `REQ-RT-*` and `REQ-HTTP-*` only (identity I1). Design, not implementation. No duplicate issues implied.
- Load your own methodology. Honor the writing-voice rules.
