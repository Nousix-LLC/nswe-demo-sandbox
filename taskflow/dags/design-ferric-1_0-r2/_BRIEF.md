# _BRIEF.md — Design DAG (recovery): Ferric → a credible 1.0 framework (with SSR + hydration)

You are a design DAG for the repository **`Nousix-LLC/nswe-demo`**. Settle what Ferric must become to be a real
1.0 framework, produce the design as a reviewable PR, and produce the backlog that reaches it — under the
existing **Ferric framework epic (issue #1)**. You decide how a framework of this kind is designed and which
methodologies that takes; this brief describes the work, it does not prescribe a method, a decomposition, or a
verdict.

## This is a recovery re-fork — build on prior art, do not start from zero

A prior design DAG for this same directive ran, drafted four of the concerns below, then **froze and failed
before producing the server-side-rendering concern, the requirements, the plan, and the root synthesis** (its
subtree reached a failed terminal state with no root `SYNTHESIS.md`, roughly five days with no progress). Its
usable partial output is carried forward for you under **`prior-art/`** at this workspace so that work is not
lost. Treat it as **prior art to validate and build on, not gospel and not something to redo**:

| `prior-art/` file | Concern it drafts | State |
|---|---|---|
| `authoring-model.md` | Authoring model: `view!`/JSX-style macro, props/children/slots/composition, context | drafted (spoke output, not independently re-reviewed) |
| `async-forms-events.md` | Async resources (suspense-style loading/error), forms + two-way binding, full DOM events | drafted (owns the `REQ-ASYNC-*` register) |
| `router-and-http.md` | Router (params, nested routes, links) + HTTP/JSON client | drafted **and folded** — passed its subtree synthesis |
| `router-and-http.SYNTHESIS.md` | the fold record / verdict for the router+HTTP subtree | the one clean fold the prior run produced |
| `release-and-distribution.md` | Release & distribution: crates.io, semver, changelog, versioning/compat | drafted |
| `frozen-dag-_GLOBAL.md` | the prior run's subtree hub — its identity/traceability scheme (`REQ-FW-*`, `REQ-RT-*`, `REQ-HTTP-*`, `REQ-ASYNC-*`) and artifact map | reference for a consistent id scheme |

**What the prior run never produced and you must** (the gaps that make this a recovery, not a triage): the
**SSR + hydration concern (the one must-have)**, the **framework scope & 1.0 requirements**, the
**documentation & developer-experience** concern, the **performance & honest comparison** concern, and **the
plan — the Ferric 1.0 release bar + the traceable backlog** — plus the **root `SYNTHESIS.md`** that ties it all
together. You own all nine concerns: for the four with prior art, confirm they still hold against the live repo
and the rest of the design and reconcile their requirement registers; for the five that are missing, design
them. The carried-forward id scheme (`REQ-FW-*` / `REQ-RT-*` / `REQ-HTTP-*` / `REQ-ASYNC-*`) is a sensible
convention to keep so the registers stay disjoint and traceable, but you decide your own decomposition and
methodology.

## Objective

Take **Ferric** (the crate under `crates/ferric` in `Nousix-LLC/nswe-demo`) from where it is today to a credible
**1.0**. This is the design half of owner directive **#114**: design first, so the build can then proceed as
reviewed PRs under the Ferric epic. Plan the 1.0 under **epic #1**.

**What Ferric is today** (the baseline you build the 1.0 on): a client-side Rust/WebAssembly framework —
Solid/Leptos-style fine-grained reactivity (`Signal`, `Memo`, `Effect`, `batch`, scoped cleanup), components as
`Fn() -> VNode`, a keyed virtual-DOM diff applied to the live DOM through web-sys, and click/input events. Its
only dependencies are `wasm-bindgen`, `web-sys`, and `js-sys`. Its closest design analog is Vue 3 (fine-grained
reactivity plus a virtual DOM); among Rust frameworks it sits between Leptos/Sycamore (signals, no VDOM) and
Dioxus (React-like VDOM). The **foundation crate has landed, and the client-side router (#5) and HTTP/JSON
client (#6) have already landed as closed issues** — confirm what is actually in `crates/ferric` on `main` and
design the 1.0 router/HTTP work as **additive over those landed surfaces** (nested routes, route params,
active-link, typed JSON, timeouts), superseding #5/#6 in the backlog with `supersedes:` rather than filing
duplicates. The carried-forward `router-and-http.md` already takes this additive-over-frozen stance; verify it
against the code as landed.

## What this design is for

A first, dedicated **framework** design for Ferric's 1.0. This is distinct from the chirp *product* design that
already lives in the repo (`design/`, the chirp release bar); that design is a consumer of Ferric, not Ferric
itself. Ferric is a library whose users are Rust/WASM application authors — chirp is its first real consumer and
is expected to surface real framework gaps as it exercises the 1.0. Name only the concerns that apply to a
framework/library product (API, architecture, developer experience, distribution, performance); the end-user
concerns of an application design (sign-up screens, accounts, a product threat model) do not apply here.

## The concerns to cover — as distinct concerns, each with its goal and its bar

Treat each of the following as its own concern with its own acceptance bar; your evaluation decides how to
decompose and which methodology each needs. For concerns that have prior art under `prior-art/`, your job is to
validate and integrate it; for the rest, to design it.

1. **Framework scope & 1.0 requirements.** *(no prior art — design it)* Who uses Ferric and what they must be
   able to build; what a credible 1.0 of a Rust/WASM UI framework must provide, stated as testable requirements
   and acceptance criteria; the explicit MVP-vs-1.0 line. **Out of the 1.0 bar** (nice-to-have *after* 1.0, to
   be stated as such, not designed now): a scoped CSS/styling story, devtools, hot reload, and desktop/mobile
   targets.

2. **Server-side rendering + hydration — the one must-have.** *(no prior art — design it; this is the gap that
   most matters)* Render a component tree to HTML on the server (an **Axum** integration) and **hydrate it in
   the browser without re-rendering**: the isomorphic rendering architecture, how reactive state is carried from
   server to client and resumed, and how event listeners are wired on hydrate. Bar: a server-rendered page
   becomes interactive by hydration with no client-side re-render.

3. **Authoring model: a `view!`/JSX-style macro, props/children/slots/composition, and context.** *(prior art:
   `authoring-model.md` — validate and integrate)* A declarative view macro (builder calls do not scale to real
   apps); component props, children/slots, and composition; context for sharing state without prop drilling.
   Bar: real applications can be written ergonomically without builder-call boilerplate.

4. **Async, forms, and events.** *(prior art: `async-forms-events.md` — validate and integrate)* Async resources
   with suspense-style loading and error states; forms with two-way input binding; full DOM event coverage. Bar:
   each stated as testable behavior.

5. **Router + HTTP/JSON client.** *(prior art: `router-and-http.md` + its `SYNTHESIS.md` — validate and
   integrate)* A router with route params, nested routes, and links; an HTTP/JSON client. Additive over the
   **landed** #5/#6 surfaces — supersede, do not duplicate. Bar: the journeys a real app needs (nested routing,
   linking, typed JSON fetch) are expressible.

6. **Documentation & developer experience.** *(no prior art — design it)* A guide, a tutorial, API docs,
   examples, and a **cargo-generate** starter template. Bar: a new user can scaffold from the starter and follow
   the guide to a working app.

7. **Release & distribution.** *(prior art: `release-and-distribution.md` — validate and integrate)* Publishing
   to **crates.io** with **semver** and a **changelog**; the versioning and compatibility policy for a 1.0. Bar:
   the crates are publishable with a semver contract and a changelog.

8. **Performance & honest comparison.** *(no prior art — design it)* A **js-framework-benchmark** entry measuring
   speed, memory, and bundle size, with honest comparisons to peer frameworks. Bar: a reproducible benchmark
   entry with stated results.

9. **The plan — the Ferric 1.0 release bar + a traceable backlog.** *(no prior art — design it; it must cover
   all nine concerns)* Turn the design into **epics and work-items under the Ferric epic (#1)**, each with
   acceptance criteria that trace back to the requirements above, with dependencies and an order that reaches a
   usable framework early and the full 1.0 bar after. Each epic must be a coherent capability that one code DAG
   can build, review, and land as one change, with its dependencies on other epics stated. Produce a concrete
   **Ferric 1.0 release bar**: a testable statement of what "a real 1.0 framework" means for Ferric, held
   against what frameworks of its kind provide — not "it compiles" or "the examples run". Supersede the already
   -landed router (#5) and HTTP (#6) issues into this structure with `supersedes:` rather than duplicating them.

## Inputs

- The repository `Nousix-LLC/nswe-demo` at the current `main` (HEAD `276138f`): the Ferric crate
  (`crates/ferric`) as it stands, the landed foundation, the landed router (#5) and HTTP client (#6), and the
  existing `design/` product design and release bar (chirp-level — context for how the repo states a release
  bar, not the thing being designed).
- **The carried-forward prior art under `prior-art/`** at this workspace (see the table above): four drafted
  concern documents and one fold record from the prior, failed run. Validate them against the live repo and the
  rest of the design; build on them rather than redo them.
- Owner directive **#114** (the authoritative scope) and the Ferric epic **#1** with its existing children, on
  the `NSWE Delivery` board (GitHub Project #1 for this repository).
- Any peer Rust/WASM frameworks worth honest comparison are reference material; cite them by name, not by host
  path.

## Declared output

- **The design in the repository, as a PR** on a work branch (`work/design-ferric-1_0`), reviewed like any other
  change: the Ferric 1.0 requirements, the release bar, and the design artifacts (SSR/hydration architecture, the
  authoring model, the router/http design, async/forms/events, docs/DX plan, release plan, benchmark plan), where
  code DAGs and reviews can read them.
- **The backlog it implies, on the board**: epics and issues under the Ferric epic **#1**, each with acceptance
  criteria tracing to the design, with dependencies and order. Check the board first and **extend/supersede
  existing issues (notably the landed #5 and #6) instead of filing duplicates**. Tickets say what the framework
  needs and how it will be judged, not how to build it, and read as the repository's own — they trace to the
  design document in the repository, carry no engagement internals or host/taskflow paths.
- **A root `SYNTHESIS.md`** that states the Ferric 1.0 release bar and indexes the filed issues by epic.

You write design and tickets, not framework code.

## Constraints

- Repository scope: `Nousix-LLC/nswe-demo` only, and its **`NSWE Delivery` board (GitHub Project #1)**. Do **not**
  touch any other GitHub Project or any sibling repository. Work branch `work/design-ferric-1_0`; never
  force-push `main`.
- Everything you post to GitHub (issues, PR, comments) is written for the repository's readers and names only
  **repository identities** (`owner/repo`, issue/PR numbers, commits). **No attribution trailers.** Nothing on
  GitHub carries host, cluster, SSH, path, or other system/environment details — the `prior-art/` paths above are
  taskflow-internal inputs for you to read; they never appear in anything you post.
- Select and load your own methodologies for the concerns above; this brief names none, and none is carried in
  `_FORK.md` or `launch_context`.
