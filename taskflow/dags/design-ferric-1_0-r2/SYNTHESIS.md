# Ferric 1.0 — Design Synthesis

**DAG**: design-ferric-1_0-r2 · **Produced by**: SUBTASK_synthesize-root · **Date**: 2026-11-03

---

## Design verdict

The Ferric 1.0 design is complete. All nine concern areas have requirements, acceptance criteria, and
coverage in the consolidated release bar; the release bar is defined in `design/ferric/release-bar.md`
with 29 `BAR-FERRIC-*` criteria across two stages. The full backlog — eight epics (#129–#136) and 28 child
issues (#137–#164) — is filed on the `NSWE Delivery` board (GitHub Project #1) and traces back to design
requirements. PR #128 ("design: Ferric 1.0 framework design") on `Nousix-LLC/nswe-demo` carries all ten
design documents on branch `work/design-ferric-1_0`; all 19 gaps from the review have been remediated and
the PR is ready to merge.

---

## Ferric 1.0 release bar

The consolidated release bar from `design/ferric/release-bar.md`. Two stages: `usable_early` (12 criteria)
is the floor at which Ferric is first buildable for real apps; `one_oh` (17 criteria) is what a credible
public 1.0 requires on top of that. One criterion is `must_have: true` — BAR-FERRIC-004.

| id | Statement | Stage | must-have? |
|---|---|---|---|
| BAR-FERRIC-001 | The reactive runtime provides `create_signal`, `create_memo`, `create_effect`, and `batch`, with scoped cleanup that unsubscribes every reactive subscription owned by a dropped scope without leaks; `create_memo` does not recompute when its output value has not changed; `batch` defers effect execution until the batch closes. An app written against the baseline `ferric` prelude compiles at 1.0 without modification to any previously exported item. | usable_early | — |
| BAR-FERRIC-002 | The framework renders component trees to real DOM and, when a signal changes, updates only the DOM nodes affected — not the whole subtree. Keyed sibling lists reconcile by their `key` value, so a reorder moves existing DOM nodes rather than destroying and recreating them. A test or example verifies that no unaffected DOM nodes are replaced on a partial-state update. | usable_early | — |
| BAR-FERRIC-003 | Ferric renders an app to an HTML string on the server (off WASM, on the server's native target) using a renderable core that compiles with `--features ssr`; each concurrent request gets its own isolated reactive scope; the produced HTML passes a standard HTML sanitizer without injected markup. A test produces the HTML string for a representative component and checks its content without running a browser. | one_oh | — |
| BAR-FERRIC-004 | The client WASM bundle attaches to the server-rendered DOM without replacing any server-rendered element. After hydration: event handlers fire, reactive state responds to changes, and no DOM node that was present in the server HTML is torn down and rebuilt on load. An SSR + hydrate example demonstrates the complete path: server renders HTML, browser receives it as the first paint, WASM loads and wires up, interaction works without a visible repaint. | one_oh | **true** |
| BAR-FERRIC-005 | State computed during the server render (including resolved async resources) is serialized into the page and deserialized on the client without a refetch; the client resource starts in the loaded state with the server's data, not the loading state. An SSR + hydrate example with at least one async resource verifies that no network request fires for that resource during hydration. | one_oh | — |
| BAR-FERRIC-006 | When the client-rendered structure diverges from the server HTML, Ferric detects the mismatch and recovers without a silent fault. The SSR integration works with Axum: the reference Axum server handler renders Ferric to HTML and returns it in an HTTP response that the browser then hydrates. An Axum integration example is documented and builds from the stated steps. | one_oh | — |
| BAR-FERRIC-007 | The `view!` macro accepts HTML element names with their standard attributes and properties, dynamic expressions (`{signal.get()}`), conditional rendering, keyed list rendering via `<For key=... each=... view=...>`, and component invocation by name with props and children. The output compiles and renders the described UI. A stated set of valid view! examples all compile without modification. | usable_early | — |
| BAR-FERRIC-008 | A stated set of malformed view! inputs — for example an unrecognized HTML element name, a missing required attribute, a structurally invalid expression — each produces a compile-time diagnostic that names the problem in terms of the author's code rather than macro internals. The diagnostic set is captured by trybuild tests that pass in CI. | usable_early | — |
| BAR-FERRIC-009 | A component function accepts required and optional props (with defaults), a `children: VNode` parameter, and named slots. A prop type can be converted from an accepted type to the stored type via a declared `From` implementation (converting props). A slot can carry a typed closure for parameterized rendering (`SlotFn<T>`). A component can be invoked dynamically through a `dyn Component` trait object. Stated examples for each of these forms compile and render correctly. | usable_early | — |
| BAR-FERRIC-010 | A stated set of component authoring mistakes — for example a missing required prop, a type mismatch in a prop value, a misused slot — each produces a compile-time error that names the problem at the call site rather than inside framework internals. The diagnostic set is captured by trybuild tests that pass in CI. | usable_early | — |
| BAR-FERRIC-011 | A component can provide a value into the component tree with `provide_context`, and any descendant can read it with `use_context` (returns `Option`) or `expect_context` (panics with a clear message if absent). The value does not need to be threaded through every intermediate call. Stated examples for provide/use/expect compile and pass. | usable_early | — |
| BAR-FERRIC-012 | `create_resource` tracks four states — loading, loaded (with data), empty (no data), and error — and components reading it re-render when the state changes. A `<Suspense>` boundary shows the `fallback` slot while any enclosed resource is loading and switches to the resolved content when all are loaded. The boundary can be nested. A resource can be refetched on demand; a stale-while-revalidating pattern keeps previous data visible during a refetch. An `<ErrorBoundary>` catches a resource error and renders the error slot with the error value; the author can reset it to retry. A deferred resource starts loading only when first read. Reactive scope cleanup cancels any in-flight resource load. Stated tests or examples cover each of these states and transitions. | usable_early | — |
| BAR-FERRIC-013 | An author attaches handlers to DOM events using `on:<event_name>={handler}` syntax in view!, where `handler` receives a typed payload (the concrete event type for named events). The full DOM event range is covered: click, input, change, submit, keydown/keyup/keypress, focus, blur. An author can call `event.prevent_default()` and `event.stop_propagation()`. For an event not in the named set, an author can attach a handler by string name as an escape hatch. The async/forms/events examples compile and demonstrate each category. | usable_early | — |
| BAR-FERRIC-014 | An author binds a signal to a form input two-way: the input reflects the signal's current value and a change to the input updates the signal. The binding covers text inputs, checkboxes, and `<select>` elements. A submit handler on a `<form>` fires with the form data. Validation feedback can be wired to a signal updated on submit or on change. Stated examples for each input kind compile and demonstrate the two-way relationship. | usable_early | — |
| BAR-FERRIC-015 | The router matches path patterns with named parameters and renders the matching route's component in a reactive `<Outlet>`. Nested routes nest their `<Outlet>` inside a parent route's view. Each route level can declare a fallback for no-match. `navigate(path)` and the History API `push` / `replace` functions change the current path reactively. An `<a>`-backed `<Link>` component is keyboard-focusable and announced by assistive technology as a link. The `ferric-router` prelude surfaces present at the baseline are present at 1.0; no previously exported item is removed or redefined. Stated router examples compile. | usable_early | — |
| BAR-FERRIC-016 | The `<Link>` component applies an `aria-current="page"` attribute when its href matches the current path. A stated test or example verifies that navigating to and away from a route toggles the attribute correctly. | one_oh | — |
| BAR-FERRIC-017 | The `Client` accepts a base URL at configuration time. A `RequestBuilder` chains URL resolution per RFC 3986, GET/POST/PUT/DELETE methods, a typed `body::<T>()` that serializes `T` to JSON, a typed `send::<T>()` that deserializes the response body as `T`, and a matchable `Error` enum covering network failure, non-2xx status, and deserialization failure. Non-2xx responses surface as `Err` by default. Request headers can be set per-request. The `ferric-http` prelude surfaces present at the baseline are present at 1.0 without removal or redefinition. Stated HTTP client examples compile. | usable_early | — |
| BAR-FERRIC-018 | The `RequestBuilder` supports the PATCH method in addition to GET/POST/PUT/DELETE. A per-request timeout cancels the in-flight request and returns an `Error::Timeout` after the specified duration. The HTTP client's dependency footprint (specifically `serde`, `wasm-bindgen-futures`, and any added crates) is documented per crate with its bundle-size rationale, and that footprint is reflected in the performance benchmark numbers. | one_oh | — |
| BAR-FERRIC-019 | The repository provides a conceptual guide that explains Ferric's reactive model, component system, and data-loading pattern in terms an author unfamiliar with the framework can read. The repository also provides a tutorial that starts from a blank project and ends at a compiling, running app that exercises view!, components, a signal, and at least one `create_resource`; a reviewer can follow the tutorial steps exactly and reach the stated end state. Documentation is sufficient to learn and build without reading the framework's source. | one_oh | — |
| BAR-FERRIC-020 | The public API of all three crates (`ferric`, `ferric-router`, `ferric-http`) is rendered on docs.rs at a published version; each public item carries a doc comment with at least a one-sentence description. The examples directory contains a curated set that spans the capability range — at minimum a client-side SPA example and an SSR + Axum + hydrate example. Each example builds from the documented steps. | one_oh | — |
| BAR-FERRIC-021 | A `cargo generate` (or equivalent scaffold) CSR starter and an SSR + Axum variant are available; both build and run from the documented commands on stable Rust and the standard toolchain. The non-toy reference application (`chirp-frontend`) is built on Ferric and exercises reactivity, keyed lists, events, forms, client routing, and backend data end to end; it builds and runs from documented steps. Following the documented new-user path from zero — scaffold, serve, tutorial to a compiling end state — can be completed without reverse-engineering toolchain details. | one_oh | — |
| BAR-FERRIC-022 | The landing README states what Ferric is, names its Rust/WASM peers with a brief positioning, and points to the guide, API docs, and getting-started path — all accurately reflecting the 1.0 state. At least one troubleshooting entry covers a common first-use failure (for example missing `wasm32-unknown-unknown` target). The CI pipeline verifies that stated code examples in the documentation compile against the current source, so the docs cannot drift from the API without a CI failure. | one_oh | — |
| BAR-FERRIC-023 | All three crates (`ferric`, `ferric-router`, `ferric-http`) publish cleanly to crates.io from `cargo publish` with no git or path dependencies on Ferric itself required to build a consuming project. Each crate's `Cargo.toml` carries a `license` field with an SPDX identifier, a `description`, a `repository` URL, and a `rust-version` field matching the workspace's declared MSRV. Intra-workspace dependencies are declared at a semver version, not a path. The crates are publishable in the order their dependency graph requires. `cargo add ferric` (and the companion crates) resolves published crates at a semver version from a fresh project. | one_oh | — |
| BAR-FERRIC-024 | The public API of each crate is identified; a change that removes or alters an existing public item in a way that breaks a caller's code requires a major version bump. Additive changes (new items) require at least a minor bump across the multi-crate workspace. `cargo semver-checks` runs in CI and fails on violations of this contract before release. An author can read, from the repository, what version-level change a given kind of modification requires. | one_oh | — |
| BAR-FERRIC-025 | `CHANGELOG.md` exists at the repository root, follows the Keep a Changelog 1.1.0 format (sections: Added, Changed, Deprecated, Removed, Fixed, Security; unreleased section at top), and contains an entry for the 1.0 release naming each user-visible change. Every breaking change in the 1.0 release is listed under Changed or Removed. | one_oh | — |
| BAR-FERRIC-026 | A keyed js-framework-benchmark implementation for Ferric is present in the benchmark harness, uses only the public `ferric` API (no framework internals), and covers all standard keyed-category operations: create rows, replace all rows, partial update, select row, swap rows, remove row, and create many rows. The benchmark runs from documented steps on a pinned browser version and pinned dependency versions, and produces duration and memory numbers for each operation. The setup steps and pinned conditions are documented so a reviewer can reproduce the run. | one_oh | — |
| BAR-FERRIC-027 | The optimized WASM bundle size for a representative Ferric app (built with `wasm-opt` and `wasm-bindgen` from documented steps) is measured and reported alongside the benchmark results. The framework's dependency set — `wasm-bindgen`, `web-sys`, `js-sys` for the core; `serde` and `wasm-bindgen-futures` for the HTTP client; any other additions — is documented per crate with a one-sentence justification for each addition. No heavy general-purpose runtime is introduced; the bundle-size impact of the dependency set is reflected in the measured numbers. | one_oh | — |
| BAR-FERRIC-028 | The benchmark results are presented in a table that includes the named Rust/WASM peers (Leptos, Sycamore, Dioxus, Yew) and places JS frameworks (Solid, Vue 3, vanilla JS) as context. All peers are run under the same conditions (same benchmark harness, same browser version, same hardware class). The table is a full per-operation comparison — no operation is omitted from the peer table. Measured numbers are kept distinct from pre-measurement targets; the document states which numbers are measured results. The WASM-vs-JS differences in memory and bundle-size accounting are stated explicitly so a reader can interpret the comparison. | one_oh | — |
| BAR-FERRIC-029 | The three crates (`ferric`, `ferric-router`, `ferric-http`) version together as a lockstep unit: they are published at the same version number and a consuming project depends on them at matched versions. The MSRV is declared in the workspace `Cargo.toml` via `rust-version`; raising the MSRV within the 1.x line requires at minimum a minor version bump and a changelog entry. The `ferric` prelude public surface is frozen for the 1.x line: new items may be added but no existing exported item is removed or altered without a major version bump. A written compatibility policy, discoverable from the repository root, states what the 1.x stability promise covers (the three preludes), what it does not cover (private modules, `#[doc(hidden)]` items, compiler-internal representations), and the versioning rule for the multi-crate workspace. | one_oh | — |

---

## Issues by epic

All eight epics (#129–#136) and 28 child issues (#137–#164) are filed on the `NSWE Delivery` board
(GitHub Project #1 on `Nousix-LLC/nswe-demo`).

| Epic # | Title | Stage | Child issues |
|---|---|---|---|
| #129 | EPIC: Ferric 1.0 — Authoring Model | usable_early | #137, #138, #139, #140, #141, #142 |
| #130 | EPIC: Ferric 1.0 — Async, Forms, and Events | usable_early | #143, #144, #145 |
| #131 | EPIC: Ferric 1.0 — Client-side Router | usable_early / one_oh | #146, #147 |
| #132 | EPIC: Ferric 1.0 — HTTP/JSON Client | usable_early / one_oh | #148, #149 |
| #133 | EPIC: Ferric 1.0 — SSR and Hydration | one_oh | #150, #151, #152, #153 |
| #134 | EPIC: Ferric 1.0 — Docs and DX | one_oh | #154, #155, #156, #157 |
| #135 | EPIC: Ferric 1.0 — Performance and Benchmark | one_oh | #158, #159, #160 |
| #136 | EPIC: Ferric 1.0 — Release and Distribution | one_oh | #161, #162, #163, #164 |

Note: #137 (Reactive state) is a child of epic #129 (Authoring Model).

---

## Design documents

All ten documents are on branch `work/design-ferric-1_0` under `design/ferric/` in `Nousix-LLC/nswe-demo`.

| File | Concern |
|---|---|
| `design/ferric/scope-and-requirements.md` | Framework scope and 1.0 requirements (`REQ-FW-*`, 21 ids) |
| `design/ferric/ssr-hydration.md` | SSR + hydration — must-have for 1.0 (`REQ-SSR-*`, 12 ids) |
| `design/ferric/authoring-model.md` | `view!` macro, props, children, named slots, context (`REQ-API-*`) |
| `design/ferric/async-forms-events.md` | Async resources, forms, DOM events (`REQ-ASYNC-*`) |
| `design/ferric/router-and-http.md` | Client-side router + HTTP/JSON client (`REQ-RT-*`, `REQ-HTTP-*`) |
| `design/ferric/docs-and-dx.md` | Documentation and developer experience (`REQ-DX-*`) |
| `design/ferric/release-and-distribution.md` | crates.io publishing, semver, changelog (`REQ-REL-*`) |
| `design/ferric/performance-and-benchmark.md` | js-framework-benchmark entry and peer comparison (`REQ-PERF-*`) |
| `design/ferric/release-bar.md` | Consolidated release bar (`BAR-FERRIC-001`–`BAR-FERRIC-029`) |
| `design/ferric/release-plan.md` | Ordered epics with GitHub issue references and dependency map |

---

## PR

PR #128 ("design: Ferric 1.0 framework design") on `Nousix-LLC/nswe-demo` carries all ten design documents
and the `design/ferric/contracts/` directory. All 19 remediation commits are present on
`work/design-ferric-1_0`. The PR is ready to merge; no design gap remains open.
