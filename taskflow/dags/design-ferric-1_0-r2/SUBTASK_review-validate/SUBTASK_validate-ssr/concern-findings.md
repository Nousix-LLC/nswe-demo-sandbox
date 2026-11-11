# Concern Findings — SSR + Hydration

## concern_name

Server-Side Rendering & Hydration (`REQ-SSR-*`)

## document_validated

`ssr-hydration.md` on branch `work/design-ferric-1_0`
(grounded at `Nousix-LLC/nswe-demo` commit `276138f` on `main`)

## req_ids_found

- REQ-SSR-001 — Render a component tree to HTML on the server
- REQ-SSR-002 — The renderable core builds and runs off-wasm
- REQ-SSR-003 — Per-request reactive isolation on the server
- REQ-SSR-004 — Hydrate the server-rendered DOM without a client re-render *(gating must-have)*
- REQ-SSR-005 — Event handlers are wired on hydrate
- REQ-SSR-006 — Carry server render state across the seam
- REQ-SSR-007 — Resume server-resolved async resources without refetch
- REQ-SSR-008 — First client render is value-identical to the server render
- REQ-SSR-009 — Hydration mismatches are detected and recovered safely
- REQ-SSR-010 — Server markup and the state island are injection-safe
- REQ-SSR-011 — A documented Axum server-integration path
- REQ-SSR-012 — The SSR surface is additive over the frozen foundation

Cross-reference IDs cited (read-only, owned elsewhere): REQ-FW-003, REQ-FW-004, REQ-FW-008,
REQ-FW-009, REQ-FW-014, REQ-ASYNC-*, REQ-API-*, REQ-HTTP-*, REQ-REL-*, REQ-DX-*.

## status

needs-fix

## specific_issues

### Issue 1

- **type**: completeness
- **description**: REQ-SSR-001 and REQ-SSR-003 are not connected in the API surface specification.
  The document requires `render_to_string` to perform "no effects" (§2.1) and per-request reactive
  isolation (REQ-SSR-003), but does not explicitly state that `render_to_string` calls
  `component.render()` outside of any reactive effect — i.e., without pushing an observer onto the
  thread-local runtime's observer stack. This omission matters because the thread-local RUNTIME in
  `signal.rs` (grounded at `276138f`) accumulates subscriptions for any read that occurs while an
  observer is active. If an implementer wraps the server render in a `create_effect` (the way
  `dom::mount` does), signal reads during `render_to_string` would accumulate subscriptions that
  are never cleaned up, producing a state leak across requests on the same thread and violating
  REQ-SSR-003. The design's "performs no effects" phrasing implies the correct behaviour but does
  not make it a named design constraint, leaving the mechanism for per-request isolation underdeclared
  for an implementer. The acceptance criterion for REQ-SSR-003 tests the observable result
  (two renders get separate outputs) but says nothing about what the render API must do internally
  to guarantee isolation — specifically, that the render must not register an active observer.
- **severity**: major

### Issue 2

- **type**: completeness
- **description**: The document specifies recovery from hydration mismatch (§3: detect, emit
  diagnostic, client-render the mismatched subtree) but is silent on what happens if a component
  panics during `render_to_string` on the server. Production SSR frameworks must answer whether the
  framework catches the panic at the render boundary (catch-unwind and return a Result), whether it
  propagates and crashes the worker thread, or whether the server falls back to client-only rendering.
  The document draws a correctness bar for mismatch recovery on the client (§3, REQ-SSR-009) but
  draws no bar for the analogous failure mode on the server. An Axum handler calling
  `render_to_string` in production has no specified behaviour when the component tree panics.
- **severity**: minor

## gaps

### GAP-010

- **id**: GAP-010
- **description**: The reactive context contract for `render_to_string` is not specified. The design
  requires per-request isolation (REQ-SSR-003) and states that server render "performs no effects"
  (§2.1), but does not name "bypass the reactive observer stack" as a design constraint on the
  `render_to_string` API. Without this explicit constraint, an implementer who follows `mount`'s
  pattern of wrapping the render in `create_effect` would compile and appear correct for a single
  request, but would silently leak subscriptions and violate per-request isolation under concurrent
  load. The connection between "performs no effects" and "achieves REQ-SSR-003 isolation" must be
  made explicit: the acceptance criterion for REQ-SSR-003 tests the observable output but cannot
  be satisfied without the API contract being stated.
- **severity**: major
- **action_required**: Add a named design constraint to REQ-SSR-001 and §2.1 stating that
  `render_to_string` MUST call `component.render()` without an active reactive observer on the
  thread-local stack — i.e., outside of any `create_effect` — so that signal reads during server
  render do not register subscriptions. This is the mechanism that satisfies REQ-SSR-003; it
  should appear in the acceptance criteria for REQ-SSR-001 or as a named isolation contract in
  §2.1 alongside the "performs no effects" sentence.

### GAP-011

- **id**: GAP-011
- **description**: No error-handling bar for component panics during server-side rendering. The
  document draws a recovery bar for the client-side mismatch path (§3, REQ-SSR-009) but not for
  a component panic during `render_to_string`. An Axum handler that calls `render_to_string` in
  production has no specified fallback behaviour when rendering fails.
- **severity**: minor
- **action_required**: Add a requirement (or an explicit recorded deferral) for error handling
  during server render: either `render_to_string` returns `Result<String, ...>` and callers handle
  the error, or the document explicitly defers panic handling to the implementing work-item and
  notes the production risk. A one-sentence recorded deferral is sufficient if the intent is to
  leave it to the implementation.

---

## Validation assessment — criteria from brief

| Criterion | Result |
|---|---|
| Architecture grounded in codebase at `276138f` | **Pass** — all factual claims verified |
| "No re-render on hydration" stated as testable | **Pass** — REQ-SSR-004 has observable criteria and a verification mechanism |
| State carry across SSR seam addressed | **Pass** — §2.3 and REQ-SSR-006 |
| Async resource resume addressed | **Pass** — REQ-SSR-007 |
| Concern marked as 1.0 must-have | **Pass** — all 12 REQ-SSR-* are `stage: one_oh`, `release_gating: true`; REQ-SSR-004 is the gating must-have |
| Document complete for SSR framework | **Needs fix** — two gaps (GAP-010 major, GAP-011 minor) |

### Architecture accuracy detail

The document's observations of the codebase at `276138f` are accurate:

- **`dom::mount` empties root before rendering** — confirmed: `dom.rs` removes all children of
  root before the first render (lines 71–73), exactly as §1 describes.
- **`vdom` and `component` are `web-sys`-free** — confirmed: neither module imports `web_sys`;
  `vdom.rs` module doc states "pure and native-testable: it performs no `web-sys` calls."
- **Path-based DOM resolution (`first_child` then `child_nodes().item(i)`)** — confirmed:
  `dom.rs` `resolve()` at lines 197–208 walks `root.first_child()` then `child_nodes().item(index)`,
  exactly matching the description in §1.
- **Reactive arena uses thread-local `Box<dyn Any>`, event handlers use `Rc<dyn Fn()>`** —
  confirmed: `signal.rs` has `thread_local! { static RUNTIME: RefCell<Runtime> }` and
  `ValueCell = Rc<RefCell<Box<dyn Any>>>`. `vdom.rs` has `EventHandler = Rc<dyn Fn()>`.
- **Framework currently binds `Click` and `Input` only** — confirmed: `dom.rs` `set_events()`
  line 224 iterates `[EventKind::Click, EventKind::Input]` for detachment; `vdom.rs` `EventKind`
  has exactly those two variants.
