# Ferric 1.0 — Async resources and suspense (concern 4a)

**Owns**: `REQ-ASYNC-001 .. REQ-ASYNC-019` (sub-identity J1; range from `../contracts/_MANIFEST.yaml`).
**Specializes**: `REQ-FW-006` — the async clause ("load data asynchronously with explicit loading /
loaded / empty / error states (suspense)"), owned read-only by `SUBTASK_scope_and_requirements`.
**Writes**: what an app author can express and what must work. Not how the framework is built.

This fragment is one of three in `async-forms-events.md`; the events (`REQ-ASYNC-020..039`) and forms
(`REQ-ASYNC-040..059`) fragments are owned by the sibling children. Cross-area references here —
`REQ-SSR-*`, `REQ-HTTP-*`, `REQ-API-*` — are **read-only**; no id outside `REQ-ASYNC-*` is minted (J5,
parent I1).

---

## 1. What this capability is, from the app author's side

Today a Ferric author who needs data from a server has to hand-roll it. The reactive core
(`crates/ferric/src/signal.rs` @ `276138f`) is synchronous: `create_effect(impl FnMut() + 'static)`
runs to completion with no `await`, `Signal<T>`/`Memo<T>` are `Copy` handles read with `.get()` /
`.with(|&T|)`, and the crate depends only on `wasm-bindgen` / `web-sys` / `js-sys` — there is no async
primitive and no `wasm-bindgen-futures`. So an author who wants to fetch a list writes a `create_signal`
holding `Option<Result<Vec<T>, E>>`, spawns a future by hand, remembers to set a separate "loading" flag
before and clear it after, and threads both through the view. The loading flag and the fetch are not
connected to the data, so they drift: a second fetch races the first, an error leaves a stale spinner,
"no results" and "still loading" render the same empty screen.

The async-resource primitive makes the data source and its state **one reactive value**. The author
declares *where the data comes from* (an async fetcher) and *what it depends on* (a reactive source); the
framework owns the rest — running the fetch, tracking whether it is loading / loaded / empty / failed,
re-running it when the source changes, and driving the view to re-render as that state moves. The author
describes each of the four states once, declaratively, and never writes a loading flag again.

Two surfaces deliver this:

- a **resource** — a reactive handle (like `Signal`) whose value is the current async state; and
- a **suspense boundary** — a view wrapper that shows one fallback while the resources read inside it
  are still loading, so a screen with several pending fetches has one coherent loading state.

### 1.1 Illustrative shape (not a mandated signature)

The requirements below are behavior, not an API. This sketch exists so the acceptance criteria that say
`example_build` have something concrete to build against; the exact signatures are the implementing code
DAG's to finalize. `view!`, `create_signal`, and `create_effect` are the author-facing surfaces owned by
the authoring model (`REQ-API-*`) and the frozen reactive core — shown here read-only, used, not redefined.

```rust
// A reactive input the fetch depends on.
let filter: Signal<Filter> = create_signal(Filter::All);

// A resource: a reactive source + an async fetcher. Re-fetches when `filter` changes.
let todos = create_resource(
    move || filter.get(),                       // source — read reactively
    |f| async move { api::fetch_todos(f).await }, // fetcher — returns Future<Output = Result<Vec<Todo>, FetchError>>
);

// Declarative four-state render for one resource. `is_empty` routes a loaded-but-empty
// value to the Empty arm; default is "never empty".
view! {
    { todos.render()
        .empty_when(|items| items.is_empty())
        .loading(|| view! { <p>"Loading…"</p> })
        .empty(||   view! { <p>"No todos match this filter."</p> })
        .loaded(|items| view! { <ul>{ items.iter().map(todo_row).collect_view() }</ul> })
        .error(|e| view! {
            <p class="err">{ e.to_string() }</p>
            <button on:click=move |_| todos.refetch()>"Retry"</button>
        })
    }
}

// A boundary aggregating several pending resources into one fallback.
suspense(
    || view! { <Spinner/> },                    // shown until every resource read inside resolves
    move || view! { <Profile/> <Feed/> },
)
```

---

## 2. Requirements register (`REQ-ASYNC-001 .. REQ-ASYNC-019`)

Each requirement conforms to `../../contracts/id_and_traceability_schema.yaml` (`requirement_fields`,
`stage`, `release_gating`, `verification_method`, `references`). Statements are what must be true from an
app author's side; acceptance criteria are checkable by someone who was not in the room.

### REQ-ASYNC-001 — Async-resource primitive
- **Statement**: An author can declare an asynchronous data source — a fetcher that returns a Rust
  `Future` — and receive a reactive **resource** handle whose current value is that fetch's state. The
  framework drives the fetcher to completion and updates the resource without the author spawning the
  future or managing a loading flag.
- **Rationale**: A data-backed app is the stated target (`REQ-FW-006`, journey JA2). Every peer provides
  this as the core async primitive: Leptos `create_resource`, Solid `createResource`, Dioxus
  `use_resource`. Ferric has none today, so authors hand-build the future-plus-flag pattern the framework
  should own.
- **Acceptance criteria**:
  1. An example declares a resource from a reactive source and an async fetcher and compiles against the
     1.0 `ferric` surface (`example_build`).
  2. With no manual future-spawning or loading flag in author code, the resource's value becomes the
     fetched data after the fetch resolves, observed by a reactive read (`automated_test`,
     `wasm-bindgen-test`).
- **Stage**: usable_early · **Release gating**: true
- **References**: `REQ-FW-006`; data source abstraction in REQ-ASYNC-014.

### REQ-ASYNC-002 — Four distinct states, read reactively
- **Statement**: A resource exposes, as a reactive read, exactly which of four states it is in —
  **loading**, **loaded**, **empty**, **error** — so the author can branch on the current state and have
  the branch re-evaluate when the state changes.
- **Rationale**: `REQ-FW-006` names "distinct loading, loaded, empty, and error states (suspense)" as the
  acceptance bar. Solid exposes `resource.loading` / `resource.error`; Leptos exposes `Option<T>` plus an
  error boundary. "Empty" is the state peers leave to the author and apps routinely get wrong (an empty
  list rendered identically to a still-loading one); naming it as a first-class state closes that gap.
- **Acceptance criteria**:
  1. A reactive read of the resource's state returns a value distinguishing loading, loaded, empty, and
     error; reading it inside an effect or the view subscribes to changes (`automated_test`).
  2. The four states are documented with the condition that produces each (`doc_inspection`).
- **Stage**: usable_early · **Release gating**: true
- **References**: `REQ-FW-006`; emptiness in REQ-ASYNC-004; error carriage in REQ-ASYNC-005.

### REQ-ASYNC-003 — Declarative per-resource state render
- **Statement**: An author can map each of a resource's four states to view content once, declaratively,
  and the framework renders the content for the current state and re-renders when the state moves —
  without the author writing conditional show/hide logic or loading flags.
- **Rationale**: The point of suspense is that the author describes states, not transitions. Leptos uses
  `<Suspense>` + pattern-matching `Option<T>`; Solid uses `<Show>` / `<Switch>` over resource accessors.
  Ferric's view is built from `VNode`, so the natural surface is a state-to-`VNode` mapping that composes
  with the existing render path.
- **Acceptance criteria**:
  1. An example renders four different `VNode`s for the four states of one resource, selected by state,
     with no imperative DOM manipulation in author code (`example_build`).
  2. Moving the resource from loading to loaded to error re-renders to the matching content, verified by
     inspecting the mounted DOM across the transitions (`automated_test`, `wasm-bindgen-test`).
- **Stage**: usable_early · **Release gating**: true
- **References**: `REQ-API-*` (the `view!`/component surface this render composes with, read-only).

### REQ-ASYNC-004 — Empty as a first-class, author-defined state
- **Statement**: An author can declare, per resource, when a successfully loaded value counts as **empty**
  (for example, an empty collection), and a loaded-but-empty value renders the empty content rather than
  the loaded content. When the author declares no emptiness condition, a loaded value always renders as
  loaded.
- **Rationale**: `REQ-FW-006` lists empty as distinct from loaded. No peer makes empty first-class —
  Leptos/Solid/Dioxus all leave it to an author `if items.is_empty()` inside the loaded branch, which is
  the check apps forget. Making it a declared predicate means the four-state contract is complete and the
  empty screen is designed, not accidental.
- **Acceptance criteria**:
  1. With an emptiness predicate declared, a fetch resolving to an empty value renders the empty content;
     a non-empty value renders the loaded content (`automated_test`).
  2. With no predicate declared, a resolved value renders as loaded regardless of its contents
     (`automated_test`).
- **Stage**: usable_early · **Release gating**: true
- **References**: REQ-ASYNC-002.

### REQ-ASYNC-005 — Error state carries the failure and does not break the view
- **Statement**: When the fetcher's `Future` resolves to an error (or the author's fallible fetch yields
  one), the resource enters the error state carrying the error value; the error content can read it (for
  example to show a message); and a failed fetch neither panics nor leaves the view wedged in loading.
- **Rationale**: The hand-rolled pattern's worst failure is a fetch error leaving a permanent spinner.
  Leptos routes resource errors to `<ErrorBoundary>`; Solid to `<ErrorBoundary>` and `resource.error`.
  Ferric authors need the error value at the render site and a guarantee the framework caught it.
- **Acceptance criteria**:
  1. A fetcher that resolves to an error moves the resource to the error state with the error value
     readable in the error content (`automated_test`).
  2. After an error, the resource is not in the loading state, and a subsequent `refetch` (REQ-ASYNC-007)
     can recover it (`automated_test`).
- **Stage**: usable_early · **Release gating**: true
- **References**: REQ-ASYNC-002, REQ-ASYNC-007.

### REQ-ASYNC-006 — Re-fetch when a reactive dependency changes
- **Statement**: A resource re-runs its fetcher when a signal or memo read by its reactive **source**
  changes. While a re-fetch is in flight, a later source change supersedes the earlier fetch so the
  resource's resolved value always reflects the most recent source (no out-of-order result wins).
- **Rationale**: This is the behavior that makes a resource reactive rather than a one-shot promise. Solid
  re-runs `createResource` when its source signal changes; Leptos re-runs when the source closure's
  tracked signals change; Dioxus `use_resource` restarts when reactive reads in its body change. The
  out-of-order guarantee is the race the hand-rolled flag pattern cannot express.
- **Acceptance criteria**:
  1. Changing a signal the source reads triggers a new fetch with the new source value (`automated_test`).
  2. When two source changes produce two fetches that resolve out of order, the resource's final value is
     the one for the later source change (`automated_test`).
- **Stage**: usable_early · **Release gating**: true
- **References**: REQ-ASYNC-008 (reactive composition); REQ-ASYNC-016 (superseded-fetch cleanup).

### REQ-ASYNC-007 — Imperative refetch
- **Statement**: An author can trigger a re-fetch on demand (for example a Retry button after an error, or
  a manual refresh) without changing the source.
- **Rationale**: Retry-after-error and pull-to-refresh are standard; Solid exposes `refetch`, Leptos
  `resource.refetch()`, Dioxus `resource.restart()`. Without it, the only recovery from an error state is
  a contrived source change.
- **Acceptance criteria**:
  1. Calling the resource's refetch runs the fetcher again with the current source value and moves the
     resource back through loading to its new resolved state (`automated_test`).
- **Stage**: usable_early · **Release gating**: true
- **References**: REQ-ASYNC-005.

### REQ-ASYNC-008 — Composition with the reactive graph
- **Statement**: A resource's state is a reactive value in the same graph as signals and memos: reading it
  inside `create_effect`, `create_memo`, or a view subscribes the reader to its changes; a state change
  schedules the readers to re-run exactly as a signal write does; and a `batch` that spans a resource read
  and a signal write behaves consistently with the frozen batching semantics.
- **Rationale**: The resource must not be a second, parallel reactivity system. Authors already know
  `.get()` / `.with()` / effects / `batch`; a resource that participates in that graph composes with memos
  (a memo derived from resource state) and effects (an effect that reacts to load completion) with no new
  mental model. This is how Leptos (signals) and Solid (fine-grained graph) both do it.
- **Acceptance criteria**:
  1. A memo that reads a resource's state recomputes when the state changes (`automated_test`).
  2. An effect that reads a resource's state re-runs when the state changes, and does not re-run on an
     unrelated signal write (`automated_test`).
- **Stage**: usable_early · **Release gating**: true
- **References**: frozen `signal.rs` surface (`create_memo`, `create_effect`, `batch`) — read-only.

### REQ-ASYNC-009 — Suspense boundary over multiple pending resources
- **Statement**: An author can wrap a region of the view in a **suspense boundary** with a single
  fallback; the boundary shows the fallback while any resource read within the region is loading, and
  shows the region's content once every such resource has resolved. One screen with several concurrent
  fetches thus has one coherent loading state instead of several independent spinners.
- **Rationale**: This is the "suspense" named in `REQ-FW-006`. Leptos `<Suspense fallback=…>` and Solid
  `<Suspense>` both aggregate pending resource reads in their subtree into one fallback; coordinating
  several fetches by hand is exactly the plumbing the framework should own.
- **Acceptance criteria**:
  1. A boundary containing two resources shows the fallback until both resolve, then shows the content
     (`automated_test`, `wasm-bindgen-test`).
  2. An example composes a boundary over a region with more than one resource and builds against the 1.0
     surface (`example_build`).
- **Stage**: usable_early · **Release gating**: true
- **References**: REQ-ASYNC-003 (per-resource render is the complement); REQ-ASYNC-010.

### REQ-ASYNC-010 — Nested suspense boundaries
- **Statement**: Suspense boundaries nest: an inner boundary resolves on its own resources independently
  of the outer boundary, and an outer boundary's fallback depends only on the resources read directly in
  its region (not on those already delegated to a resolved inner boundary). An author can thus reveal part
  of a screen while a slower nested part still loads.
- **Rationale**: Real screens load in stages — shell first, then a slow panel. Solid and Leptos both allow
  nested `<Suspense>` for staged reveal. Without defined nesting, an author cannot show anything until the
  slowest fetch on the page resolves.
- **Acceptance criteria**:
  1. With a fast resource in an outer boundary and a slow resource in a nested inner boundary, the outer
     content (with the inner fallback) appears when the fast resource resolves, and the inner content
     replaces its fallback when the slow resource later resolves (`automated_test`).
- **Stage**: usable_early · **Release gating**: true
- **References**: REQ-ASYNC-009.

### REQ-ASYNC-011 — Loading-with-previous-value distinguishable from first load
- **Statement**: While a resource re-fetches after having already loaded once, the author can tell that a
  prior loaded value exists and choose to keep showing it (avoiding a flash back to the loading state on
  every refresh), distinct from the first load where no prior value exists.
- **Rationale**: Re-fetching on every keystroke of a search filter should not blank the results list each
  time. Solid's resource keeps its latest value readable while `loading` is true; Leptos exposes the prior
  value during refetch. Without this distinction, REQ-ASYNC-006's re-fetch produces a visible flicker on
  each source change.
- **Acceptance criteria**:
  1. After a first load, a source-change-triggered re-fetch leaves the previously loaded value readable
     while the new fetch is in flight, and the loading indication distinguishes "reloading" from "first
     load" (`automated_test`).
- **Stage**: usable_early · **Release gating**: true
- **References**: REQ-ASYNC-006.

### REQ-ASYNC-012 — SSR resolution handed to the client (by reference)
- **Statement**: A resource created during a server render resolves its fetcher on the server, and its
  resolved state is made available to the client so that the first client render shows the loaded (or
  empty / error) state rather than loading. The mechanism that serializes the resolved state and carries
  it into hydration is **not defined here** — it is owned by `REQ-SSR-*` (`SUBTASK_ssr_hydration`), which
  this requirement references read-only.
- **Rationale**: SSR exists so the first paint is content, not a spinner; a resource that re-entered
  loading on the client would defeat it. Leptos serializes resource values into the SSR payload for
  exactly this reason. Ferric's async resource must be designed to *participate* in that handoff; the
  carrying mechanism is the SSR child's to build (J5).
- **Acceptance criteria**:
  1. The design states that a resource's resolved server-side state is the input to client hydration and
     cites the `REQ-SSR-*` requirement that carries it, minting no `REQ-SSR-*` id here (`doc_inspection`).
- **Stage**: one_oh · **Release gating**: true
- **References**: `REQ-SSR-*` (read-only, `SUBTASK_ssr_hydration`); REQ-ASYNC-013.

### REQ-ASYNC-013 — No refetch on hydration when SSR provided the state (by reference)
- **Statement**: When a resource's resolved state was produced during SSR and carried to the client, the
  client does not re-run the fetcher on initial hydration; it adopts the carried state. The carriage
  mechanism is `REQ-SSR-*` (read-only); this requirement states only the resource-side obligation not to
  refetch what SSR already resolved.
- **Rationale**: A double fetch (once on the server, again on hydration) wastes a request and can flash
  the UI. This is the client-side half of REQ-ASYNC-012 and the behavior Leptos's serialized resources
  guarantee.
- **Acceptance criteria**:
  1. The design states that a hydrating resource with a carried SSR state performs no initial fetch, and
     references the `REQ-SSR-*` hydration requirement without minting one (`doc_inspection`).
- **Stage**: one_oh · **Release gating**: true
- **References**: REQ-ASYNC-012; `REQ-SSR-*` (read-only).

### REQ-ASYNC-014 — Abstract data source (HTTP client by reference)
- **Statement**: The resource's data source is any async fetcher returning a Rust `Future`; the resource
  does not define or require a particular HTTP or JSON client. A fetcher backed by the framework's HTTP
  client (`REQ-HTTP-*`, read-only), by a third-party client, or by a non-network async source (a timer, a
  local async computation) all satisfy the primitive equally.
- **Rationale**: Coupling the resource to one HTTP client would force that client on apps that use a
  different one and would blur the two concerns. Solid's `createResource` and Dioxus's `use_resource` take
  an arbitrary async function; the fetch client is orthogonal. The HTTP/JSON client is `REQ-HTTP-*`'s to
  design (`SUBTASK_router_and_http`); no `REQ-HTTP-*` id is minted here (J5).
- **Acceptance criteria**:
  1. An example builds a resource over a non-HTTP async source (`example_build`).
  2. The design states the fetcher contract as "returns a `Future`" with no dependency on a specific
     client, referencing `REQ-HTTP-*` read-only (`doc_inspection`).
- **Stage**: usable_early · **Release gating**: true
- **References**: `REQ-HTTP-*` (read-only, `SUBTASK_router_and_http`).

### REQ-ASYNC-015 — Additive over the frozen reactive core and runtime
- **Statement**: The async-resource primitive is additive over the frozen `ferric` surface. The
  synchronous contract of `create_effect(impl FnMut() + 'static)`, the `Signal`/`Memo` handle API,
  `create_signal` / `create_memo` / `batch`, and the `mount` / `VNode` render path are unchanged; the
  resource, the suspense boundary, and the async executor that drives fetchers are new items, not
  redefinitions of any frozen item.
- **Rationale**: The 1.0 line is drawn against what is real (parent I9, J4). The core is explicitly
  synchronous today and the crate carries no `wasm-bindgen-futures`; introducing async must extend the
  surface, not quietly change the effect contract existing code relies on.
- **Acceptance criteria**:
  1. The frozen prelude items (`create_signal`, `create_memo`, `create_effect`, `batch`, `Signal`,
     `Memo`, `mount`, `VNode`) retain their current signatures and semantics; the async additions are new
     names (`automated_test` that existing reactive-core tests still pass; `doc_inspection` of the diff
     against `276138f`).
- **Stage**: usable_early · **Release gating**: true
- **References**: frozen `signal.rs` / `dom.rs` surfaces (read-only); parent I9.

### REQ-ASYNC-016 — Superseded and dropped fetches are cleaned up
- **Statement**: When a re-fetch supersedes an in-flight fetch (REQ-ASYNC-006), or when a resource's
  owning reactive scope is disposed, the result of the superseded or orphaned fetch does not update the
  resource's state. A resolved fetch never writes to a resource that has been superseded or disposed.
- **Rationale**: This is the correctness guarantee behind REQ-ASYNC-006's out-of-order rule and the leak
  that hand-rolled fetching causes most often (a late response overwriting newer data, or a response
  landing after the component is gone). Fine-grained frameworks (Solid) tie fetch lifetime to the reactive
  owner for exactly this reason.
- **Acceptance criteria**:
  1. A superseded fetch that resolves after its successor does not change the resource's resolved value
     (`automated_test`).
  2. A fetch that resolves after its resource's scope is disposed produces no state update and no panic
     (`automated_test`).
- **Stage**: usable_early · **Release gating**: true
- **References**: REQ-ASYNC-006.

*(`REQ-ASYNC-017 .. REQ-ASYNC-019` are unused headroom within this child's assigned range; the range is
deliberately generous per `../contracts/_MANIFEST.yaml`.)*

---

## 3. Composition, stated so it is not left as an owl

**With reactivity.** The resource is backed by the frozen graph (REQ-ASYNC-008, REQ-ASYNC-015): its state
is held in reactive cells, reads subscribe, writes schedule readers. A memo may derive from resource
state; an effect may fire on load completion; `batch` spans both. The resource adds a value *kind* to the
graph, not a second graph. The one new runtime capability is an executor that drives a fetcher `Future` on
the browser event loop and writes the result back into the reactive cells — additive, and its exact
vehicle (for example `wasm-bindgen-futures`) is the implementing DAG's choice, not a requirement here.

**With SSR (by reference only).** REQ-ASYNC-012 and REQ-ASYNC-013 state the resource-side obligations —
resolve on the server, adopt the carried state on hydration, do not double-fetch — and point at
`REQ-SSR-*` (`SUBTASK_ssr_hydration`) for the serialization-and-hydration mechanism. No `REQ-SSR-*` id is
minted and no hydration mechanism is designed here (J5). The seam is named, not deferred silently.

**With the data source (by reference only).** The fetcher is "any async function returning a `Future`"
(REQ-ASYNC-014). The HTTP/JSON client is `REQ-HTTP-*`'s (`SUBTASK_router_and_http`); the resource composes
with it by reference and mints no `REQ-HTTP-*` id (J5).

**With the authoring model (by reference only).** The render surfaces (`view!`, components) are
`REQ-API-*`'s; this fragment uses them read-only in illustration and defines none of them.

---

## 4. Peer comparison (cited by name)

| Framework | Async primitive | Re-fetch trigger | Suspense / error surface | Empty state | SSR handling |
|---|---|---|---|---|---|
| **Leptos** `Resource` | `create_resource(source, fetcher)`; value read as `Option<T>` | source closure's tracked signals change; `.refetch()` | `<Suspense fallback>` aggregates pending reads; `<ErrorBoundary>` for errors | author checks inside loaded branch | serializes resolved resource into SSR payload; hydration adopts it, no refetch |
| **Solid** `createResource` | `createResource(source, fetcher)` → accessor with `.loading` / `.error`; `{ mutate, refetch }` | source signal changes; `refetch()` | `<Suspense>`, `<SuspenseList>`, `<ErrorBoundary>`; keeps latest value during refetch | author checks inside loaded branch | `<Suspense>` resources resolve during SSR and stream/hydrate |
| **Dioxus** `use_resource` | `use_resource(async closure)` → `Resource<T>` | reactive reads in the closure change; `.restart()` | `SuspenseBoundary`; `.state()` / `.value()` read | author checks inside value branch | server futures resolve during SSR; hydration adopts |
| **Ferric 1.0 (this design)** | `create_resource(source, fetcher)` → reactive `Resource` (REQ-ASYNC-001) | reactive source change (REQ-ASYNC-006); `refetch` (007) | per-resource four-state render (003) **and** `suspense` boundary (009–010); error carries value (005) | **first-class, author-declared `empty_when`** (004) | resolves on server, adopts carried state, no double-fetch — mechanism via `REQ-SSR-*` (012–013) |

Where this design lands against the peers: the resource / re-fetch / suspense / error shape follows Leptos
and Solid closely, because that shape is settled and worth matching rather than reinventing. The one place
this design is deliberately more opinionated than all three peers is **empty as a first-class, declared
state** (REQ-ASYNC-004): Leptos, Solid, and Dioxus all leave empty to an author-written `if` inside the
loaded branch, which is the check apps forget. `REQ-FW-006` lists empty as distinct, so Ferric designs it
in. Where Ferric is *behind* until the SSR child lands: REQ-ASYNC-012/013 are stated as obligations but
their realization depends on `REQ-SSR-*`, so a 1.0 that ships SSR must ship these together — which is why
they are staged `one_oh`, matching where SSR+hydration sits on the MVP-vs-1.0 line.

---

## 5. Traceability and identity check (this fragment's part of J1–J7)

- **J1 (disjoint range)**: all ids are `REQ-ASYNC-001..016`, within the `001..019` range this child owns;
  no id outside that range is used.
- **J2 (covers REQ-FW-006, async clause)**: the "async data with loading / loaded / empty / error
  (suspense)" clause of `REQ-FW-006` is covered by REQ-ASYNC-001 (primitive), 002 (four states), 003
  (declarative render), 004 (empty), 005 (error), 009–010 (suspense). The forms and events clauses of
  `REQ-FW-006` are the sibling fragments' to cover.
- **J4 (additive over frozen)**: REQ-ASYNC-015 states additivity explicitly; every requirement that
  touches the core (006, 008, 016) extends it and redefines nothing frozen.
- **J5 (SSR / HTTP by reference only)**: REQ-ASYNC-012/013 reference `REQ-SSR-*` read-only and mint no
  `REQ-SSR-*`; REQ-ASYNC-014 references `REQ-HTTP-*` read-only and mints no `REQ-HTTP-*`.
- **J3, J6, J7**: the event-payload seam (J3) is the events/forms fragments' concern, not referenced here;
  single-artifact assembly (J6) and parent-schema conformance (J7) are evaluated by `SUBTASK_afe_synthesis`
  — every requirement above carries the schema's fields (id, statement, rationale, acceptance_criteria,
  stage, release_gating, references) for that check.

**Verification-method coverage**: acceptance criteria across the register use `example_build` (001, 003,
009, 014), `automated_test` (001–011, 015–016), and `doc_inspection` (002, 012, 013, 014, 015), satisfying
the brief's requirement that at least one criterion be checkable via the schema's vocabulary.
