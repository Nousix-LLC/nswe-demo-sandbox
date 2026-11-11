# _BRIEF.md — Design DAG: Ferric → a credible 1.0 framework (with SSR + hydration)

You are a design DAG for the repository **`Nousix-LLC/nswe-demo`**. Settle what Ferric must become to be a
real 1.0 framework, produce the design as a reviewable PR, and produce the backlog that reaches it — under the
existing **Ferric framework epic (issue #1)**. You decide how a framework of this kind is designed and which
methodologies that takes; this brief describes the work, it does not prescribe a method, a decomposition, or a
verdict.

## Objective

Take **Ferric** (the crate under `crates/ferric` in `Nousix-LLC/nswe-demo`) from where it is today to a
credible **1.0**. This is the design half of owner directive **#114**: design first, so the build can then
proceed as reviewed PRs under the Ferric epic. Plan the 1.0 under **epic #1**, and **fold in the router and
HTTP/JSON-client issues already on the board** (currently tracked as **#5 `ferric-router`** and **#6
`ferric-http`**) — extend or supersede them into the 1.0 plan rather than filing duplicates.

**What Ferric is today** (the baseline you build the 1.0 on): a client-side Rust/WebAssembly framework —
Solid/Leptos-style fine-grained reactivity (`Signal`, `Memo`, `Effect`, `batch`, scoped cleanup), components
as `Fn() -> VNode`, a keyed virtual-DOM diff applied to the live DOM through web-sys, and click/input events.
Its only dependencies are `wasm-bindgen`, `web-sys`, and `js-sys`. Its closest design analog is Vue 3
(fine-grained reactivity plus a virtual DOM); among Rust frameworks it sits between Leptos/Sycamore (signals,
no VDOM) and Dioxus (React-like VDOM). The foundation crate (#4) has landed; the router (#5) and HTTP client
(#6) are on the board and are to be absorbed into this 1.0 design.

## What this design is for

A first, dedicated **framework** design for Ferric's 1.0. This is distinct from the chirp *product* design that
already lives in the repo (`design/`, the chirp release bar); that design is a consumer of Ferric, not Ferric
itself. Ferric is a library whose users are Rust/WASM application authors — chirp is its first real consumer and
is expected to surface real framework gaps as it exercises the 1.0. Name only the concerns that apply to a
framework/library product (API, architecture, developer experience, distribution, performance); the end-user
concerns of an application design (sign-up screens, accounts, a product threat model) do not apply here.

## The concerns to cover — as distinct concerns, each with its goal and its bar

Treat each of the following as its own concern with its own acceptance bar; your evaluation decides how to
decompose and which methodology each needs.

1. **Framework scope & 1.0 requirements.** Who uses Ferric and what they must be able to build; what a credible
   1.0 of a Rust/WASM UI framework must provide, stated as testable requirements and acceptance criteria;
   the explicit MVP-vs-1.0 line. **Out of the 1.0 bar** (nice-to-have *after* 1.0, to be stated as such, not
   designed now): a scoped CSS/styling story, devtools, hot reload, and desktop/mobile targets.

2. **Server-side rendering + hydration — the one must-have.** Render a component tree to HTML on the server
   (an **Axum** integration) and **hydrate it in the browser without re-rendering**: the isomorphic rendering
   architecture, how reactive state is carried from server to client and resumed, and how event listeners are
   wired on hydrate. Bar: a server-rendered page becomes interactive by hydration with no client-side re-render.

3. **Authoring model: a `view!`/JSX-style macro, props/children/slots/composition, and context.** A declarative
   view macro (builder calls do not scale to real apps); component props, children/slots, and composition;
   context for sharing state without prop drilling. Bar: real applications can be written ergonomically without
   builder-call boilerplate.

4. **Async, forms, and events.** Async resources with suspense-style loading and error states; forms with
   two-way input binding; full DOM event coverage. Bar: each stated as testable behavior.

5. **Router + HTTP/JSON client.** A router with route params, nested routes, and links; an HTTP/JSON client.
   This concern **absorbs board issues #5 and #6** — supersede or extend them, do not duplicate. Bar: the
   journeys a real app needs (nested routing, linking, typed JSON fetch) are expressible.

6. **Documentation & developer experience.** A guide, a tutorial, API docs, examples, and a **cargo-generate**
   starter template. Bar: a new user can scaffold from the starter and follow the guide to a working app.

7. **Release & distribution.** Publishing to **crates.io** with **semver** and a **changelog**; the versioning
   and compatibility policy for a 1.0. Bar: the crates are publishable with a semver contract and a changelog.

8. **Performance & honest comparison.** A **js-framework-benchmark** entry measuring speed, memory, and bundle
   size, with honest comparisons to peer frameworks. Bar: a reproducible benchmark entry with stated results.

9. **The plan — the Ferric 1.0 release bar + a traceable backlog.** Turn the design into **epics and
   work-items under the Ferric epic (#1)**, each with acceptance criteria that trace back to the requirements
   above, with dependencies and an order that reaches a usable framework early and the full 1.0 bar after.
   Each epic must be a coherent capability that one code DAG can build, review, and land as one change, with
   its dependencies on other epics stated. Produce a concrete **Ferric 1.0 release bar**: a testable statement
   of what "a real 1.0 framework" means for Ferric, held against what frameworks of its kind provide — not
   "it compiles" or "the examples run". Fold the existing router (#5) and HTTP (#6) issues into this structure.

## Inputs

- The repository `Nousix-LLC/nswe-demo` at the current `main` (HEAD `276138f`): the Ferric crate
  (`crates/ferric`) as it stands, the landed foundation (#4), and the existing `design/` product design and
  release bar (chirp-level — context for how the repo states a release bar, not the thing being designed).
- Owner directive **#114** (the authoritative scope) and the Ferric epic **#1** with its existing children,
  including router **#5** and HTTP/JSON client **#6**, on the `NSWE Delivery` board.
- Any peer Rust/WASM frameworks worth honest comparison are reference material; cite them by name, not by host
  path.

## Declared output

- **The design in the repository, as a PR** on a work branch (`work/design-ferric-1_0`), reviewed like any
  other change: the Ferric 1.0 requirements, the release bar, and the design artifacts (SSR/hydration
  architecture, the authoring model, the router/http design, docs/DX plan, release plan, benchmark plan),
  where code DAGs and reviews can read them.
- **The backlog it implies, on the board**: epics and issues under the Ferric epic **#1**, each with
  acceptance criteria tracing to the design, with dependencies and order. Check the board first and
  **extend/supersede existing issues (notably #5 and #6) instead of filing duplicates**. Tickets say what the
  framework needs and how it will be judged, not how to build it, and read as the repository's own — they
  trace to the design document in the repository, carry no engagement internals.
- **A root `SYNTHESIS.md`** that states the Ferric 1.0 release bar and indexes the filed issues by epic.

You write design and tickets, not framework code.

## Constraints

- Repository scope: `Nousix-LLC/nswe-demo` only. Work branch `work/design-ferric-1_0`; never force-push
  `main`.
- Everything you post to GitHub (issues, PR, comments) is written for the repository's readers and names only
  **repository identities** (`owner/repo`, issue/PR numbers, commits). **No attribution trailers.** Nothing on
  GitHub carries host, cluster, SSH, path, or other system/environment details.
- Select and load your own methodologies for the concerns above; this brief names none, and none is carried in
  `_FORK.md` or `launch_context`.
