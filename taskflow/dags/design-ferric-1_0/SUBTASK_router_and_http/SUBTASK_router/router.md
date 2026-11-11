# Ferric 1.0 — Client-Side Router Design (`REQ-RT-*`)

*Owns the `REQ-RT-*` register. Sibling spoke: the HTTP/JSON client (`REQ-HTTP-*`, `SUBTASK_http`). Both compose
into `router-and-http.md` at the synthesis gate. Conforms to `../../contracts/id_and_traceability_schema.yaml`
and the sub-contract `../contracts/_MANIFEST.yaml` (`doc_layout`, identities SI1–SI6).*

## Overview

*(section: `overview`)*

This is the design for Ferric 1.0's **client-side router** — the capability an app author (persona A2, "I'm
building a real app on it") uses to move a single-page application between views, and that the evaluating author
(A1) expects any credible framework to provide. It specializes the framework-level routing requirement
`REQ-FW-007` (client routing with route parameters, nested routes, and in-app links, with the view re-rendering
on path change) into a testable `REQ-RT-*` register, and it is held to the additive-over-frozen-surface rule
`REQ-FW-009` (identity SI2 / parent I9).

The router exists today as a landed crate, not a blank page. Board issue #5 shipped `crates/ferric-router` as a
working walking skeleton: a declarative route table with path parameters, History-API navigation, a reactive
current path, a reactive outlet, and an in-app link — all composing `ferric`'s signals and component model
rather than re-implementing reactivity or the DOM diff. Its `prelude` surface is frozen. The 1.0 design therefore
does two things: it states the bar the already-shipped capabilities must keep meeting, and it adds, **additively**,
the two capabilities the baseline does not yet have — **nested routes** (with a nested outlet) and **replace**
semantics for History navigation — plus one credible-1.0 affordance, **active-route awareness** for links.

**Who it is for.** The app author (A2) building a multi-view, data-backed SPA (the repository's `chirp-frontend`
is the first real one). They declare routes, drop one outlet into their shell, link between views, and read the
current route — and they expect the router, the HTTP client, and the view framework to compose without
mismatched assumptions (journey JA2, "Navigate" and "Compose the pieces").

**Non-goals (stated so the cut is explicit, not silent).**

- **Route-level data loaders are not a router concern.** Peer routers bolt data loading onto routes; Ferric keeps
  the router navigation-only and composes data loading from the async surface (`REQ-ASYNC-*`, read-only
  cross-reference): an author fetches inside a route's view with a resource/suspense, so loading and error states
  live in one place rather than being split between the router and the async layer. This keeps the router's
  surface small and its single responsibility — resolve the path to a view and re-render on change — intact.
- **Query/search-string parameters** are a recorded post-1.0 deferral (`REQ-RT-009`), not a 1.0 capability.
- **Typed/enum routes** (the Dioxus model) are deliberately not adopted; the router stays string-pattern based,
  matching the frozen `RoutePattern`. The rationale is in the peer comparison below.

---

## Relationship to the frozen `ferric-router` surface

*(section: `relationship_to_frozen`)*

The baseline `ferric-router` `prelude` is frozen (verified by reading `crates/ferric-router/src/` at `276138f`
and `contracts/ferric_router_api.rs`). The 1.0 design is additive over it: every item below is carried forward
with its signature unchanged, and the 1.0 additions are new items that do not remove or redefine any of them
(identity SI2 / parent I9).

### What exists and is carried forward unchanged

| Frozen prelude item | What it is | 1.0 disposition |
|---|---|---|
| `matcher::Params` (`get`, `is_empty`, `len`, and the additive `iter`) | Named path parameters extracted from a matched route (stringly-typed `get(name) -> Option<&str>`). | Carried forward unchanged. The bar it meets is `REQ-RT-001`. |
| `matcher::RoutePattern` (`new`, `match_path`) | A compiled `/`-separated pattern with `:name` segments; exact-over-segments matching; trailing slash insignificant; root is the empty segment list. | Carried forward unchanged (`REQ-RT-001`). |
| `router::Router` (`new`, `route`, `fallback`, `mount_history`, `outlet`) | A flat, first-match-wins route table consumed into a reactive outlet component. | Carried forward unchanged; the flat table becomes the degenerate (single-level) case of nested routing (`REQ-RT-005`). |
| `router::navigate(&str)` | Programmatic navigation: `pushState` + update the reactive current path. | Carried forward unchanged — it remains the **push** path (`REQ-RT-003`). |
| `router::current_path() -> String` | Reads the routed path reactively (subscribes the calling reactive context). | Carried forward unchanged (`REQ-RT-002`, `REQ-RT-003`). |
| `link::link(to, label) -> VNode` (plus the additive `Link` builder and `LINK_CLASS`) | A declarative in-app link emitting a focusable, `role="link"` non-anchor element wired to `navigate` (ferric's `Fn()` click handler cannot `preventDefault`, so an `<a href>` is intentionally avoided). | Carried forward unchanged (`REQ-RT-004`). |

### What the 1.0 adds (every addition flagged additive)

| Addition | Requirement | Why it is additive, not a redefinition |
|---|---|---|
| **Nested routes + a nested outlet** — parent routes render a layout containing a child outlet; the matched child view renders into it. | `REQ-RT-005` | The frozen flat `Router::route`/`outlet` keep working as the single-level case; nested routing is a new declaration form and a new child-outlet item layered on top of the frozen `RoutePattern`/`current_path`. No frozen signature changes. |
| **Replace-navigation** — a `replaceState` counterpart to the push-only `navigate`. | `REQ-RT-003` | `navigate(&str)` keeps its exact signature and push semantics; replace is a new additive API (its exact shape is left to implementation), not an in-place change to `navigate`. |
| **Active-route awareness for links** — a link reflects whether its target is the active route (for styling / `aria-current`). | `REQ-RT-007` | The frozen `link(to, label)` is unchanged; active-state is an additive extension of the `Link` builder. |
| **Per-level fallback for nested routes** — a nested level may declare its own no-match view. | `REQ-RT-006` | The frozen flat `Router::fallback` behavior is preserved; per-level fallback is defined only for the new nested form. |

Any change to a frozen item that could not be expressed additively would require a semver-signalled break
documented in the changelog (`REQ-FW-010`, release area, read-only here). This design introduces none.

---

## Requirements register (`REQ-RT-*`)

*(section: `requirements_register`. Each requirement: id, statement (what, not how), rationale (peer evidence),
acceptance criteria (stranger-checkable, each naming a `verification_method` from
`../../contracts/id_and_traceability_schema.yaml`: `automated_test` / `example_build` / `doc_inspection`),
stage, release gating, references (read-only). Identities SI1/SI6.)*

### REQ-RT-001 — Declarative route table with path parameters

- **Statement:** An author can declare a table of routes — each a `/`-separated path pattern with named `:param`
  segments — mapped to a view, and the router resolves the current path to the first matching route and hands
  that view the named parameters it extracted.
- **Rationale:** Path parameters are table stakes for any multi-view app; both peers provide them
  (`leptos_router` reactive `use_params_map()` over `:id`; Dioxus typed route fields). The baseline froze
  `RoutePattern`/`Params`/`Router::route`, so 1.0 states the bar they must keep meeting rather than reinventing
  them.
- **Acceptance criteria:**
  - A native `cargo test` resolves the pattern `/user/:id` against `/user/42` to that route's view and
    `Params::get("id")` returns `"42"`; a path with an extra or missing segment (`/user/42/extra`, `/user`) does
    not match. *(verification_method: automated_test)*
  - A stated multi-route example builds to WASM and, navigated to a parameterized path, renders the matched
    view showing the bound parameter. *(verification_method: example_build)*
- **Stage:** usable_early · **Release gating:** true
- **Relationship to frozen:** frozen (`RoutePattern`, `Params`, `Router::route`) carried forward unchanged.
- **References:** `REQ-FW-007` (read-only).

### REQ-RT-002 — A reactive outlet that re-renders on path change

- **Statement:** An author mounts one router outlet that renders the currently matched route's view and
  re-renders to the newly matched view whenever the current path changes, without the author wiring any
  subscription by hand.
- **Rationale:** Re-rendering the view on navigation is the defining job of a client router (`REQ-FW-007`: "the
  view re-rendering on path change"). `leptos_router` renders the matched node reactively; Ferric composes its
  own signal and render-effect for the same effect. The baseline froze `Router::outlet`/`current_path`.
- **Acceptance criteria:**
  - A native `cargo test` shows that after `navigate("/a")` then `navigate("/b")` the outlet renders the `/b`
    route's view (the outlet reads `current_path` reactively, so the render effect re-runs on the path write).
    *(verification_method: automated_test)*
  - In a stated example, activating an in-app link changes the displayed view with no full-page reload.
    *(verification_method: example_build)*
- **Stage:** usable_early · **Release gating:** true
- **Relationship to frozen:** frozen (`Router::outlet`, `current_path`) carried forward unchanged.
- **References:** `REQ-FW-007`, `REQ-RT-003`, `REQ-RT-004` (read-only).

### REQ-RT-003 — History-API navigation: push, replace, back/forward, reactive current path

- **Statement:** An author can navigate programmatically so as to either **push** a new history entry (the
  default) or **replace** the current one; browser back/forward are reflected in the routed view; and the current
  path is readable as reactive state.
- **Rationale:** The push/replace distinction is a standard router affordance (`leptos_router`'s `use_navigate`
  options; Dioxus's `Navigator`): a redirect after a form submit, or a step in a wizard, needs replace so the
  back button does not return the user to a stale or intermediate URL. The baseline froze `navigate` (push),
  `current_path`, and the `popstate` sync; replace is not yet expressible, so the 1.0 adds it **additively**.
- **Acceptance criteria:**
  - A native `cargo test` shows `navigate("/x")` updates `current_path()` to `/x`. *(verification_method:
    automated_test)*
  - A `wasm-bindgen-test` in a headless browser shows that push navigation grows the history length and back
    (`popstate`) restores the previous path into `current_path`, while replace navigation changes
    `current_path` without growing history length. *(verification_method: automated_test)*
  - The guide documents push versus replace and when an author should choose each. *(verification_method:
    doc_inspection)*
- **Stage:** usable_early · **Release gating:** true
- **Relationship to frozen:** **additive** — `navigate` (push) and `current_path` carried forward with unchanged
  signatures; replace-navigation is a new additive API (its exact shape left to implementation), not an in-place
  change to `navigate`.
- **References:** `REQ-FW-007` (read-only).

### REQ-RT-004 — In-app links that navigate client-side

- **Statement:** An author can place a declarative in-app link that, when activated, navigates client-side (no
  full page reload) to its target, is keyboard-focusable, and is announced as a link by assistive technology.
- **Rationale:** Links are how a user moves through an SPA, and being focusable and announced is part of a
  link an author can ship, not an extra. The baseline froze `link(to, label)` and the additive `Link` builder;
  because ferric's click handler is a zero-argument `Fn()` that cannot call `preventDefault()`, the link is a
  focusable `role="link"` non-anchor element wired to `navigate` rather than an `<a href>` — a deliberate
  composition choice, recorded so a reader does not read the missing `<a>` as a defect.
- **Acceptance criteria:**
  - A native `cargo test` shows `link("/about", "About")` yields a non-anchor, focusable (`tabindex="0"`),
    `role="link"` element that carries exactly one click handler and records its destination. *(verification_method:
    automated_test)*
  - In a stated example, clicking a `link` changes the view client-side with no reload. *(verification_method:
    example_build)*
  - The guide states why the link is a non-anchor element (the `preventDefault` constraint) and lists its
    accessibility attributes. *(verification_method: doc_inspection)*
- **Stage:** usable_early · **Release gating:** true
- **Relationship to frozen:** frozen (`link`, `Link`, `LINK_CLASS`) carried forward unchanged.
- **References:** `REQ-FW-007`, `REQ-RT-002` (read-only).

### REQ-RT-005 — Nested routes with a nested outlet

- **Statement:** An author can compose routes hierarchically: a parent route renders a layout that contains a
  nested outlet, and the matched child route's view renders into that outlet — so a shared shell (navigation bar,
  section frame) is written once and only the child view swaps on navigation.
- **Rationale:** Nested routing is named directly in `REQ-FW-007`'s early-usable routing floor, and it is the one
  routing capability the baseline flat first-match table does not provide. Both peers center on it:
  `leptos_router` renders the matched child through an `<Outlet/>` (omit the outlet and the child does not
  show); Dioxus declares nesting with `#[nest]`/`#[layout]` and renders children through an `Outlet`. Without
  nested routing every view re-declares the whole shell, which does not scale past a toy.
- **Acceptance criteria:**
  - A native `cargo test` over a two-level configuration where `/users` renders a layout and `/users/:id`
    renders a child view into the parent's nested outlet shows that navigating `/users/7` renders the parent
    layout with the child view bound to `id = "7"`, and navigating `/users` renders the layout with its
    index/empty child. *(verification_method: automated_test)*
  - A stated example shows a persistent parent layout (for example a sidebar) with child content swapping on
    in-app link navigation, the parent layout not being torn down and rebuilt between child routes.
    *(verification_method: example_build)*
  - The guide documents declaring nested routes and placing the nested outlet. *(verification_method:
    doc_inspection)*
- **Stage:** usable_early · **Release gating:** true
- **Relationship to frozen:** **additive** — builds on the frozen `RoutePattern`/`Router`/`current_path`; the
  nested-route declaration and the child outlet are new items. The frozen flat `Router::route`/`outlet` remain
  valid as the single-level case.
- **References:** `REQ-FW-007`, `REQ-RT-001`, `REQ-RT-002` (read-only).

### REQ-RT-006 — No-match (fallback) handling at each routing level

- **Statement:** An author can declare a fallback (no-match / "404") view; when no route matches at a level, that
  level's fallback renders with empty parameters, and a nested level may declare its own fallback distinct from
  the app root's.
- **Rationale:** Every real app needs a defined answer for an unmatched URL. The baseline froze `Router::fallback`
  for the flat table (no match with no fallback renders an empty node); nested routing needs a per-level answer so
  that a miss within a section (`/users/<unknown>`) can render the section's own not-found rather than always
  falling through to the app root.
- **Acceptance criteria:**
  - A native `cargo test` shows that with a fallback declared, an unmatched path renders the fallback view
    invoked with empty parameters; with no fallback declared, an empty node renders (the baseline behavior is
    preserved). *(verification_method: automated_test)*
  - A native `cargo test` shows a nested level with its own fallback renders that fallback for an unmatched child
    while the parent layout still renders. *(verification_method: automated_test)*
  - The guide documents fallback resolution, including at nested levels. *(verification_method: doc_inspection)*
- **Stage:** usable_early · **Release gating:** true
- **Relationship to frozen:** frozen `Router::fallback` behavior carried forward; **additive** per-level fallback
  defined for the new nested form.
- **References:** `REQ-RT-005` (read-only).

### REQ-RT-007 — Active-route awareness for links

- **Statement:** An author can render a link that reflects whether its target is the currently active route, so
  active navigation can be styled and announced (for example via an active CSS class and `aria-current`) without
  the author hand-wiring a comparison against `current_path`.
- **Rationale:** Marking the active link is a standard router affordance — `leptos_router`'s `<A/>` sets
  `aria-current="page"` on the active link — and apps otherwise re-derive it from `current_path` at every nav
  item. An app can ship without it (so it is not on the early-usable floor), but a credible 1.0 router provides
  it.
- **Acceptance criteria:**
  - A native `cargo test` shows that when the current path matches a link's target the emitted element carries
    the active marker (an active class and/or `aria-current="page"`), and when it does not match the marker is
    absent. *(verification_method: automated_test)*
  - A stated navigation example visibly marks the active link and updates the marker on navigation.
    *(verification_method: example_build)*
  - The guide shows how to style the active link. *(verification_method: doc_inspection)*
- **Stage:** one_oh · **Release gating:** true
- **Relationship to frozen:** **additive** — extends the `Link` builder with active-state over the frozen
  `link`/`Link`; `link(to, label)` is unchanged.
- **References:** `REQ-RT-004`, `REQ-RT-002` (read-only).

### REQ-RT-008 — Composition over the frozen surface, additive-only

- **Statement:** The 1.0 router composes `ferric`'s signals and component model (it does not re-implement
  reactivity or the DOM diff) and extends the baseline `ferric-router` prelude additively: every baseline prelude
  item (`Params`, `RoutePattern`, `Router`, `navigate`, `current_path`, `link`) remains usable with an unchanged
  signature, and an app written against the baseline prelude still compiles and runs at 1.0.
- **Rationale:** This specializes `REQ-FW-009` and realizes identity SI2 (parent I9). The walking skeleton is a
  dependable base only while its evolution is additive; the shipped example and the future `chirp-frontend`
  depend on the frozen surface.
- **Acceptance criteria:**
  - A native `cargo test` / `example_build` shows the baseline 2–3 route example (built with
    `Router::new().route(...).fallback(...).mount_history().outlet()`, `navigate`, `current_path`, and `link`)
    compiles and its tests pass unchanged against the 1.0 crate. *(verification_method: automated_test)*
  - A reviewer confirms every 1.0 addition to the prelude is recorded as additive in the changelog and no
    baseline prelude item is removed or has its signature changed without a semver-signalled, changelog-documented
    break. *(verification_method: doc_inspection)*
- **Stage:** usable_early · **Release gating:** true
- **Relationship to frozen:** this requirement *is* the additive identity (SI2) stated as a testable condition.
- **References:** `REQ-FW-009`, `REQ-HTTP-*` (sibling spoke, read-only).

### REQ-RT-009 — Query / search-string parameters as reactive state (deferred)

- **Statement (deferred):** A router-owned reactive accessor for URL query/search parameters (`?q=...`) is **not**
  part of 1.0.
- **Reason:** The baseline matcher is path-only, and `REQ-FW-007` and the author journeys do not require
  router-owned query state for a credible 1.0. An app that needs the query string can read
  `window.location.search` or layer its own parsing until this is picked up. Recorded so the cut is explicit, not
  silent; `leptos_router`'s `use_query_map` is the peer precedent should this be designed post-1.0.
- **Verification:** none (post-1.0 item; referenced by no `BAR-FERRIC-*`, per trace rule "no out-of-1.0 item is
  enforced by any BAR").
- **Stage:** post_one_oh · **Release gating:** false
- **References:** `REQ-ASYNC-*` (read-only; query state, if added, would compose with the async surface rather
  than own data loading).

### Register summary

| REQ-RT | Capability | Stage | Release gating | Frozen / additive |
|---|---|---|---|---|
| 001 | Route table with path parameters | usable_early | true | frozen |
| 002 | Reactive outlet re-renders on path change | usable_early | true | frozen |
| 003 | History navigation: push, **replace**, back/forward, reactive path | usable_early | true | additive (replace) |
| 004 | In-app client-side links (focusable, announced) | usable_early | true | frozen |
| 005 | **Nested routes** with a nested outlet | usable_early | true | additive |
| 006 | No-match / fallback at each level | usable_early | true | frozen + additive (nested) |
| 007 | Active-route awareness for links | one_oh | true | additive |
| 008 | Additive composition over the frozen surface | usable_early | true | identity (SI2) |
| 009 | Query/search params (deferred) | post_one_oh | false | — |

`REQ-RT-001`–`REQ-RT-008` are 1.0 requirements (`release_gating: true`); `REQ-RT-009` is a recorded post-1.0
deferral. Every gating requirement carries at least one acceptance criterion a stranger could check with a
`verification_method` from the parent schema (SI6). This register writes only `REQ-RT-*` ids (SI1); all
`REQ-FW-*`, `REQ-ASYNC-*`, and `REQ-HTTP-*` references are read-only.

---

## Peer comparison

*(section: `peer_comparison`. Named comparison of routing models, per the sub-contract. Peer behavior is drawn
from each project's current public documentation.)*

Ferric's routing model is a **string-pattern route table of closures** (`Router::new().route("/user/:id", |p|
…)`) with stringly-typed parameters (`Params::get("id") -> Option<&str>`), first-match-wins resolution, a single
reactive current path, and one outlet component. The two Rust peers an evaluating author (A1) weighs take
different stances; the 1.0 nested-route design follows the one closest to Ferric's existing shape.

### `leptos_router`

- **Nested routes / outlet:** a URL matches a nested tree of `<Route>`s; the matched child renders through an
  `<Outlet/>` placed in the parent's view (omit the `<Outlet/>` and the child is not shown). This is the model
  Ferric's `REQ-RT-005` follows — a parent layout with a nested outlet into which the matched child renders.
- **Path parameters:** `:id` dynamic segments read **reactively** with `use_params_map()` / `use_params` inside
  the matched component.
- **Links:** an `<A/>` component that resolves relative nested routes and sets `aria-current="page"` on the link
  to the active page — the precedent for Ferric's `REQ-RT-007` active-route awareness.
- **Query:** reactive `use_query_map()` (the precedent cited by the deferred `REQ-RT-009`).
- **Closest to Ferric on:** the signal-reactive model and the outlet-based nested-routing shape. Ferric's current
  parameters are read by value (`Params::get`) from the view builder's `&Params` argument rather than through a
  reactive hook; the 1.0 keeps that shape (the matched view is already re-run reactively by the outlet), which is
  the main model difference to note for an author coming from Leptos.

### Dioxus router

- **Nested routes / layouts:** declared on an enum via `#[derive(Routable)]` with `#[route]`, `#[nest]` /
  `#[end_nest]`, `#[layout]` / `#[end_layout]`, `#[redirect]`, `#[child]`; a `#[layout]` component wraps child
  routes, which render through an `Outlet`.
- **Type-safe routing:** routes are **enum variants** and parameters are **typed struct fields**; the macro turns
  the enum into a parser/renderer. Links are typed — `Link { to: Route }` — so a destination that does not exist
  is a compile error, and programmatic navigation goes through a `Navigator` (`use_navigator()`).
- **Closest to Ferric on:** the outlet-based nested rendering (Ferric's `REQ-RT-005` matches the `Outlet`
  concept). It is **further from Ferric** on the authoring model: Dioxus's typed-enum routes and compile-checked
  links are a macro-heavy approach that would pull routing into the authoring-macro design (`REQ-API-*`), and they
  presuppose a route-enum abstraction the frozen `RoutePattern` does not have.

### The design choice this comparison settles

Ferric 1.0 keeps the **string-pattern, closure-table** model (additive over the frozen `RoutePattern`/`Router`)
and takes **nested routing via a nested outlet** from the leptos/Dioxus `Outlet` model. It does **not** adopt
Dioxus-style typed-enum routes: compile-time-checked destinations are attractive, but they require a route-enum
and macro that the frozen surface and this release's scope do not include, and retrofitting them would redefine
the frozen `Router`/`RoutePattern` rather than extend them — which `REQ-FW-009` / SI2 forbid. Typed routes are
therefore left as a possible future direction, not a 1.0 capability. The cost of this choice is concrete:
Ferric's links and route references stay string-based, so a mistyped path is a runtime no-match (handled by
`REQ-RT-006`), not a compile error.

---

## Board fold — issue #5

*(section: `board_fold`. How board issue #5 is superseded/extended by this design — identity SI3, feeds parent
I7. So the release plan and backlog filing edit #5 rather than duplicate it.)*

**Issue #5 — "ferric-router: client-side router (History API)" (epic #1, milestone "M1: Framework (ferric)") is
CLOSED.** It was delivered as the walking-skeleton crate `crates/ferric-router`: a declarative route table with
path parameters, a path→route matcher with named-parameter extraction, History-API navigation
(`pushState`/`popstate`), programmatic `navigate`, an in-app link, and a reactive outlet, unit-tested with
fmt/clippy clean and shipped as a PR into `main`. Its scope is realized and should be treated as the **delivered
baseline**, not reopened.

**The fold:** this 1.0 design **extends** #5; it does not duplicate or supersede it. The capabilities #5 shipped
map to `REQ-RT-001`, `REQ-RT-002`, `REQ-RT-004`, `REQ-RT-006`, and the push/back-forward half of `REQ-RT-003` —
stated here as the bar the baseline must keep meeting (carried forward unchanged). What this design adds on top of
#5 is new, unshipped work: **nested routes with a nested outlet** (`REQ-RT-005`), **replace-navigation**
(the additive half of `REQ-RT-003`), **active-route awareness** (`REQ-RT-007`), and **per-level nested fallback**
(the additive half of `REQ-RT-006`).

**Instruction to the release plan and backlog (read-only cross-references; the filing itself is owned by
`SUBTASK_release_plan` / `SUBTASK_file_backlog`):**

- Do **not** file a new issue that re-states #5's shipped scope. #5 is closed and its baseline stands.
- File the 1.0 router work as **new work-item(s) under epic #1** that **reference #5 as the superseded baseline**
  and cover only the additive capabilities above (`REQ-RT-005`, the replace half of `REQ-RT-003`, `REQ-RT-007`,
  the nested-fallback half of `REQ-RT-006`), each tracing to its `REQ-RT-*` id and to this design section.
- Per the id schema's epic rule, an epic that carries this work records `supersedes: #5` (extend/supersede, never
  duplicate — identity I7), signaling that #5 is folded in as the baseline the new work builds on.

---

## Metadata

- **Owning task:** `SUBTASK_router` (owns the `REQ-RT-*` register; identity SI1).
- **Sibling spoke:** `SUBTASK_http` (owns `REQ-HTTP-*`); composed with this document into `router-and-http.md`
  by `SUBTASK_synthesis`, landing at `design/ferric/router-and-http.md` (identity SI4 / parent I8).
- **Conforms to:** `../../contracts/id_and_traceability_schema.yaml` (REQ fields, stage vocabulary,
  `release_gating`, `verification_method`), `../contracts/_MANIFEST.yaml` (ownership, `doc_layout`, identities
  SI1–SI6).
- **Grounding:** the frozen surface was read from `crates/ferric-router/src/{lib,matcher,router,link}.rs` and
  `contracts/ferric_router_api.rs` in `Nousix-LLC/nswe-demo` at baseline `276138f`; board issue #5 state read from
  the repository's issue tracker (CLOSED). Peer-router behavior (`leptos_router`, Dioxus router) is from each
  project's current public documentation.
- **Assumption recorded:** the engine methodology loader was unavailable at execution (`agent_domain_unset`);
  this design was produced from the `_BRIEF.md`, the inputs it names, and the product-design persona, applying
  web-routing / UI-framework API-design and requirements-engineering judgment, per the brief's fallback clause.
  The sibling subtree hub `../_GLOBAL.md` was not read (its path was not relayed as named state); the identities
  this output is held to (SI1–SI6, parent I1/I7/I8/I9) were taken from the relayed `_BRIEF.md` and the sub-contract
  manifest, which restate them.
- **Register:** `REQ-RT-001`–`REQ-RT-009` (001–008 release-gating 1.0; 009 recorded post-1.0 deferral).
