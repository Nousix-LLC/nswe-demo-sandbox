# Ferric 1.0 — BAR-FERRIC-* Release Criteria

This document is the complete `BAR-FERRIC-*` register for Ferric 1.0. It has two parts:

**Part 1 — Criteria.** Each criterion states a checkable condition, names the `REQ-*` requirements it
enforces, gives a verification method, and assigns a stage (`usable_early` | `one_oh`). Criteria are
numbered `BAR-FERRIC-001` through `BAR-FERRIC-027` in the order of the gap analysis surfaces.
`usable_early` criteria define the floor at which Ferric can carry a real (non-toy) app. `one_oh`
criteria are what a credible 1.0 adds on top, with SSR + hydration as the must-have gate.

**Part 2 — Coverage map.** An appendix tracing every `one_oh`-gating `REQ-*` across all spoke registers
to the `BAR-FERRIC-*` that enforces it. This is the direct evidence for identity I3.

Constraints observed: `BAR-FERRIC-*` ids are owned here; no `REQ-*` is created or modified. Every
referenced `REQ-*` id appears in the named spoke design document. No `BAR-FERRIC-*` references a
surface with `status=out-of-1.0` in the gap analysis.

---

## Part 1 — Criteria

### BAR-FERRIC-001: Reactive signals, memos, effects, and batch
- **statement**: `create_signal`, `create_memo`, `create_effect`, and `batch` work as documented:
  signal reads track the active reactive scope, memos recompute only when their signal dependencies
  change, effects run on first subscription and re-run on each dependency change, and `batch` defers
  effect runs until the batch ends. A reactive scope that is dropped unsubscribes every signal and
  memo it owned (no stale-subscriber leak). Each behavior is demonstrated by a passing `cargo test`
  or `wasm-bindgen-test`.
- **references**: REQ-FW-005
- **verification_method**: automated_test
- **stage**: usable_early

---

### BAR-FERRIC-002: Keyed virtual DOM and live-DOM patching
- **statement**: Mounting a Ferric component via `dom::mount` renders the initial view to real DOM
  nodes. When a reactive dependency of a rendered component changes, the framework applies a keyed
  diff to the live DOM rather than replacing the subtree. A list of keyed elements reconciles by
  identity: items that survive a list change keep their DOM nodes; items that are new are inserted;
  items that are gone are removed. A passing `wasm-bindgen-test` or example build demonstrates each
  of these three list operations.
- **references**: REQ-FW-005, REQ-API-001
- **verification_method**: automated_test
- **stage**: usable_early

---

### BAR-FERRIC-003: View macro — declarative HTML authoring
- **statement**: An author can write a component's view using the `view!` macro with HTML elements,
  attributes and properties, dynamic expressions in braces, boolean and conditional rendering, and
  keyed list rendering via `<For>`. Component invocation is written in the same macro surface. A
  stated example compiles, renders the described UI, and the tutorial's `view!`-authored end state
  builds without modification.
- **references**: REQ-API-001
- **verification_method**: example_build
- **stage**: usable_early

---

### BAR-FERRIC-004: Component props and children
- **statement**: A component can declare required and optional props with default values. Children
  passed to a component are receivable as `VNode`. An example that passes typed props (required and
  optional with a default) and children to a component compiles and renders the expected output.
- **references**: REQ-API-030
- **verification_method**: example_build
- **stage**: usable_early

---

### BAR-FERRIC-005: Named slots, converting props, and dynamic dispatch
- **statement**: A component can declare named slots and have callers fill them. A component can
  declare converting props that accept a value convertible to the declared type via `Into`. A
  component can accept `Box<dyn Fn() -> VNode>` or an equivalent dynamic-dispatch form for its
  render prop. Each of these three surfaces is demonstrated by a compiling example.
- **references**: REQ-API-034, REQ-API-045, REQ-API-049
- **verification_method**: example_build
- **stage**: one_oh

---

### BAR-FERRIC-006: Context — provide and consume shared values
- **statement**: `provide_context` places a value into the component tree; `use_context` reads it
  from any descendant without threading it through intermediate props; `expect_context` panics with a
  legible message if the value is absent. An example that provides a value at an ancestor and reads
  it at a descendant compiles and the value is accessible.
- **references**: REQ-API-060
- **verification_method**: example_build
- **stage**: usable_early

---

### BAR-FERRIC-007: Async resources, suspense, loading, and error states
- **statement**: `create_resource` wraps an async fetch; it exposes four distinct states — loading,
  loaded with a value, empty (resolved to nothing), and error. A `<Suspense>` boundary renders a
  fallback while any resource inside it is loading, then reveals the loaded content. Each of the four
  resource states is demonstrated by a passing `wasm-bindgen-test` or example.
- **references**: REQ-ASYNC-001
- **verification_method**: automated_test
- **stage**: usable_early

---

### BAR-FERRIC-008: Async resource state carried across the SSR seam
- **statement**: A resource resolved on the server carries its value to the hydrating client so the
  client does not refetch the same data during hydration. A stated SSR + hydration example shows the
  resource value rendered in the server HTML and available on the client without a second network
  request.
- **references**: REQ-ASYNC-012, REQ-ASYNC-013
- **verification_method**: example_build
- **stage**: one_oh

---

### BAR-FERRIC-009: Two-way form binding and form submission
- **statement**: `<input>`, `<textarea>`, `<select>`, and `<input type="checkbox">` can be bound
  two-way so the signal and the field stay in sync in both directions. A form's `submit` event fires
  and the handler receives the current field values. Validation feedback can be shown reactively on
  a field. An example demonstrating two-way binding on each input kind, a submit handler, and
  conditional validation feedback compiles and runs.
- **references**: REQ-ASYNC-040, REQ-ASYNC-041, REQ-ASYNC-042, REQ-ASYNC-043
- **verification_method**: example_build
- **stage**: usable_early

---

### BAR-FERRIC-010: Full DOM event coverage
- **statement**: Event handlers for `click`, `submit`, `keydown`, `keyup`, `focus`, `blur`,
  `change`, and `input` can be attached in the view macro using the payload-handler form. Default
  behaviour and event propagation can be prevented. Events not in this list can be attached by
  string name using an escape-hatch API. Each of the named event types is demonstrated by a passing
  test or example that shows the handler firing.
- **references**: REQ-ASYNC-020, REQ-ASYNC-021, REQ-ASYNC-022, REQ-ASYNC-023, REQ-ASYNC-024,
  REQ-FW-006
- **verification_method**: automated_test
- **stage**: usable_early

---

### BAR-FERRIC-011: Client-side routing
- **statement**: A route table maps URL paths with named parameters to components via a declarative
  route definition. A `<Router>` and `<Outlet>` pair renders the matched route component, and the
  view updates without a page reload when the path changes. History-API push and replace navigation
  are available programmatically. `<Link>` renders a keyboard-focusable, assistive-technology-
  announced anchor that navigates in-app. Nested routes with a nested `<Outlet>` render a parent
  layout and a matched child. A per-level `<Fallback>` route handles unmatched paths. An active-link
  API surfaces whether a given route is the current route. The existing `ferric-router` public
  surface is extended, not redefined. A multi-route example exercising path parameters, nested
  routes, a fallback, and an active link compiles and navigates as described.
- **references**: REQ-RT-001, REQ-RT-002, REQ-RT-003, REQ-RT-004, REQ-RT-005, REQ-RT-006,
  REQ-RT-007, REQ-RT-008
- **verification_method**: example_build
- **stage**: usable_early

---

### BAR-FERRIC-012: HTTP/JSON client — core
- **statement**: `ferric-http` exposes a `Client` that can be configured with a base URL, default
  headers, and a default timeout. A `RequestBuilder` constructs requests with a URL resolved
  relative to the base, RFC 3986–encoded path parameters and query values, and a typed JSON request
  body serialized by `serde`. The `Response` type exposes the status code and a typed JSON response
  body deserialized by `serde`. Non-2xx responses produce a matchable error value by default rather
  than silently succeeding. `GET`, `POST`, `PUT`, and `DELETE` methods are available. An example
  that sends a typed JSON request and handles a typed response and a non-2xx error compiles and runs.
- **references**: REQ-HTTP-001, REQ-HTTP-004, REQ-HTTP-005, REQ-HTTP-007, REQ-HTTP-008, REQ-HTTP-009
- **verification_method**: example_build
- **stage**: usable_early

---

### BAR-FERRIC-013: HTTP — PATCH method, per-request timeout, and cancellation
- **statement**: The `PATCH` HTTP method is available via the same request-builder API as the other
  methods. A per-request timeout can be set that overrides the client default; a request past its
  timeout resolves to a timeout error. An in-flight request can be cancelled; cancellation resolves
  the future to a cancellation error. Each behavior is demonstrated by a passing test or example.
- **references**: REQ-HTTP-010, REQ-HTTP-013
- **verification_method**: automated_test
- **stage**: one_oh

---

### BAR-FERRIC-014: Stable Rust and standard WASM toolchain
- **statement**: A Ferric app builds on the current stable Rust release targeting
  `wasm32-unknown-unknown` with `wasm-bindgen` and no nightly-only features. The minimum supported
  Rust version is declared in `[workspace.package] rust-version` and matches the documented value.
  The documented build path for both the CSR starter and the SSR + Axum variant succeeds on this
  toolchain from fresh. Compatible Rust version ranges are stated in the documentation.
- **references**: REQ-FW-003
- **verification_method**: example_build
- **stage**: usable_early

---

### BAR-FERRIC-015: Frozen public surfaces extended additively
- **statement**: The `prelude` modules of `ferric`, `ferric-router`, and `ferric-http` as they stood
  at the design baseline remain importable and usable at 1.0 without modification to the calling
  code. Any change to these surfaces since the baseline is additive: no previously exported name is
  removed, renamed, or has its type changed without a semver-major bump recorded in the changelog.
  An application written against the baseline preludes compiles at 1.0 without source changes.
- **references**: REQ-FW-009
- **verification_method**: automated_test
- **stage**: usable_early

---

### BAR-FERRIC-016: Actionable compile-time and runtime diagnostics
- **statement**: A stated set of common authoring mistakes — a malformed `view!` expression, a
  required prop omitted at a call site, a misused event handler type — each produces a compile-time
  diagnostic that names the problem in terms of the author's code rather than internal macro
  expansion. The diagnostic set is checked by `trybuild` tests that fail if a diagnostic regresses.
  A representative runtime panic (for example `expect_context` with a missing provider) carries a
  message that identifies the missing type by name.
- **references**: REQ-FW-014
- **verification_method**: automated_test
- **stage**: usable_early

---

### BAR-FERRIC-017: Server-side rendering
- **statement**: A Ferric app can render its initial view to an HTML string on a server running the
  Axum web framework, with the `ferric` crate building without the `wasm32-unknown-unknown` target
  for the server build path. Each HTTP request that triggers a server render runs in isolation: one
  request's reactive scope does not leak into another's. The Axum integration is provided by a
  stated integration point in the framework. An SSR example ships real HTML content as the initial
  response, confirmed by inspecting the raw response before the WASM loads.
- **references**: REQ-SSR-001, REQ-SSR-002, REQ-SSR-003, REQ-SSR-011
- **verification_method**: example_build
- **stage**: one_oh

---

### BAR-FERRIC-018: Hydration — client picks up server HTML
- **statement**: The WASM bundle attaches to the server-rendered DOM without replacing it: no
  visible re-render or full DOM replacement occurs on load. Event handlers wire up on the existing
  DOM nodes. Reactive state that was resolved on the server (resources, context values) is
  reconstructed on the client from serialized data, not by refetching. The first client render
  produces output structurally identical to the server render; any mismatch is detected and reported
  rather than silently accepted. A stated SSR + hydration example demonstrates each of these
  properties verifiably: the server HTML, the absence of a full re-render on client load, and the
  wired event handlers.
- **references**: REQ-SSR-004, REQ-SSR-005, REQ-SSR-007, REQ-SSR-008, REQ-SSR-009
- **verification_method**: example_build
- **stage**: one_oh
- **must_have**: true

---

### BAR-FERRIC-019: Real reference application
- **statement**: A non-toy reference application — the repository's `chirp-frontend` crate — is
  built on Ferric and exercises reactive state, keyed list rendering, forms, the full DOM event
  range, client-side routing with route parameters, backend data fetching with loading and error
  states, and SSR + hydration end to end. The application builds and runs from the documented steps
  without modification to the framework's public surface.
- **references**: REQ-FW-008
- **verification_method**: example_build
- **stage**: one_oh

---

### BAR-FERRIC-020: crates.io publishing and workspace metadata
- **statement**: Each of `ferric`, `ferric-router`, and `ferric-http` passes `cargo publish
  --dry-run` and `cargo package` with no errors. Each crate's `Cargo.toml` carries the required
  crates.io metadata fields (`name`, `version`, `license`, `description`, `repository`). Intra-
  workspace dependencies use the path-plus-version form so the published crates resolve from
  crates.io rather than a workspace path. The three crates publish at the same semver version in
  lockstep.
- **references**: REQ-FW-001, REQ-REL-001, REQ-REL-004, REQ-REL-005, REQ-REL-009
- **verification_method**: publishability
- **stage**: one_oh

---

### BAR-FERRIC-021: Semver level contract and changelog
- **statement**: The type of change a semver level signals is documented: patch for backwards-
  compatible bug fixes, minor for backwards-compatible additions, major for breaking changes. A
  `cargo-semver-checks` run in CI classifies each change to the public API surface as breaking or
  additive; a change classified as breaking triggers a major version bump. Each release carries a
  changelog entry in Keep a Changelog 1.1.0 format with `Added`, `Changed`, `Deprecated`,
  `Removed`, `Fixed`, and `Security` sections as applicable. A reviewer can confirm the CI check
  and the changelog by inspection.
- **references**: REQ-REL-020, REQ-REL-021, REQ-REL-026, REQ-REL-030, REQ-REL-031
- **verification_method**: doc_inspection
- **stage**: one_oh

---

### BAR-FERRIC-022: MSRV declaration, compatibility policy, and lockstep versioning
- **statement**: The minimum supported Rust version for the 1.0 release is declared in
  `[workspace.package] rust-version`. The rule for raising the MSRV within the 1.x line (minor
  release only, recorded in the changelog) is written and discoverable in the repository. The
  `prelude` modules of all three crates are stable across the 1.x line: no item is removed or have
  its type changed in a minor or patch release. The three crates version together under a single
  lockstep rule stated in a written compatibility policy. The compatibility policy names both what
  the stability promise covers and what it does not. All of these are verifiable by doc inspection.
- **references**: REQ-FW-010, REQ-REL-040, REQ-REL-041, REQ-REL-042, REQ-REL-043, REQ-REL-044,
  REQ-REL-046, REQ-REL-047
- **verification_method**: doc_inspection
- **stage**: one_oh

---

### BAR-FERRIC-023: Developer documentation — guide, tutorial, API docs, and examples
- **statement**: The repository provides: a conceptual guide covering Ferric's reactive model,
  component authoring, routing, and async data; a tutorial whose stated end state compiles and runs
  without modification; rendered API documentation for the public preludes of all three crates on
  docs.rs; a curated examples set that spans the capability range including an SSR + hydration
  example; a troubleshooting entry that covers at least one common failure mode; a README that
  accurately describes what Ferric is, its current state, and how to get started. CI enforces that
  the documented public surface matches the shipped API so documentation does not drift. A reviewer
  can confirm each item exists and that the tutorial's end state builds.
- **references**: REQ-FW-011, REQ-DX-001, REQ-DX-002, REQ-DX-003, REQ-DX-004, REQ-DX-008,
  REQ-DX-009, REQ-DX-010
- **verification_method**: doc_inspection
- **stage**: one_oh

---

### BAR-FERRIC-024: Zero-to-app starter and build documentation
- **statement**: A `cargo generate` template exists for both a CSR (client-side-only) Ferric app
  and an SSR + Axum Ferric app. Running the template command produces a project that builds to WASM
  and runs from documented commands using the standard toolchain, with no undocumented prerequisite.
  Build and toolchain documentation covers both paths. An author who has never used Ferric can go
  from nothing to a running app using only the documented path. The path from scaffold through
  `cargo generate`, `cargo build`, and `trunk serve` (or the SSR equivalent) to a browser-visible
  app is demonstrated end to end.
- **references**: REQ-FW-002, REQ-DX-005, REQ-DX-006, REQ-DX-007
- **verification_method**: example_build
- **stage**: one_oh

---

### BAR-FERRIC-025: Performance benchmark — speed, memory, and bundle size
- **statement**: Ferric has an entry in the js-framework-benchmark that uses only the public API
  (no benchmark-specific internal access). The entry runs in the benchmark harness and produces a
  per-operation timing table covering every standard benchmark operation. A memory-usage measurement
  and the optimized-build WASM + JS bundle size (in kilobytes after `wasm-opt`) are stated alongside
  the timing results. The results are reproducible: a reviewer can re-run the benchmark from the
  documented steps and reach comparable numbers.
- **references**: REQ-FW-012, REQ-PERF-001, REQ-PERF-002, REQ-PERF-003, REQ-PERF-004, REQ-PERF-010
- **verification_method**: benchmark_run
- **stage**: one_oh

---

### BAR-FERRIC-026: Named-peer performance comparison
- **statement**: The benchmark results are presented alongside results for Leptos, Sycamore, Dioxus,
  and Yew run under the same conditions (same benchmark version, same hardware, same optimisation
  flags). The comparison table covers every standard operation and states speed, memory, and bundle
  size for each peer. JavaScript peers (Solid, Vue 3) appear as context with the WASM-vs-JS memory
  and bundle-size caveats explicitly stated. Results that were measured are kept separate from
  pre-measurement targets. Cherry-picking individual operations is not acceptable: the full per-
  operation table is published.
- **references**: REQ-PERF-005, REQ-PERF-006, REQ-PERF-007, REQ-PERF-008, REQ-PERF-009
- **verification_method**: benchmark_run
- **stage**: one_oh

---

### BAR-FERRIC-027: Lean, documented dependency footprint
- **statement**: The core `ferric` crate's required dependencies are limited to `wasm-bindgen`,
  `web-sys`, and `js-sys`. The `ferric-http` crate may additionally depend on `serde`,
  `serde_json`, and `wasm-bindgen-futures`. No crate in the workspace introduces a heavy general-
  purpose runtime dependency. The full dependency set of each crate at 1.0 is listed in the
  documentation. The bundle-size numbers in BAR-FERRIC-025 reflect this dependency set; any
  addition to the documented set that increases the optimized bundle size by more than 5% requires a
  documented justification.
- **references**: REQ-FW-013, REQ-PERF-010
- **verification_method**: doc_inspection
- **stage**: one_oh

---

## Part 2 — Coverage map

Every `one_oh`-gating `REQ-*` (stage=one_oh, release_gating=true) across all spoke registers,
with the `BAR-FERRIC-*` that enforces it. This is the evidence for identity I3.

| REQ-* id | Statement summary | Enforced by |
|---|---|---|
| REQ-FW-001 | Installable as ordinary crates.io dependencies | BAR-FERRIC-020 |
| REQ-FW-002 | Documented path from zero to a running app | BAR-FERRIC-024 |
| REQ-FW-004 | SSR with hydration — the 1.0 must-have | BAR-FERRIC-017, BAR-FERRIC-018 |
| REQ-FW-008 | Real reference application that composes all capabilities | BAR-FERRIC-019 |
| REQ-FW-010 | Stable semver API with a compatibility policy | BAR-FERRIC-022 |
| REQ-FW-011 | Documentation sufficient to learn and build without the source | BAR-FERRIC-023 |
| REQ-FW-012 | Reproducible named-peer performance characterization | BAR-FERRIC-025, BAR-FERRIC-026 |
| REQ-FW-013 | Lean dependency footprint | BAR-FERRIC-027 |
| REQ-SSR-001 | Server renders app to HTML string | BAR-FERRIC-017 |
| REQ-SSR-002 | Renderable core builds without wasm32-unknown-unknown | BAR-FERRIC-017 |
| REQ-SSR-003 | Per-request reactive scope isolation | BAR-FERRIC-017 |
| REQ-SSR-004 | Hydration: client attaches to server HTML without re-render | BAR-FERRIC-018 |
| REQ-SSR-005 | Event handlers wire on hydrate | BAR-FERRIC-018 |
| REQ-SSR-007 | Server-resolved resource state carries to client | BAR-FERRIC-018 |
| REQ-SSR-008 | First client render matches server render | BAR-FERRIC-018 |
| REQ-SSR-009 | Hydration mismatch is detected, not silently accepted | BAR-FERRIC-018 |
| REQ-SSR-011 | Axum integration point for server rendering | BAR-FERRIC-017 |
| REQ-API-034 | Converting props accepting values via Into | BAR-FERRIC-005 |
| REQ-API-045 | Parameterized / named slots | BAR-FERRIC-005 |
| REQ-API-049 | Dynamic dispatch render props | BAR-FERRIC-005 |
| REQ-ASYNC-012 | Resource state seam: server to client, no refetch | BAR-FERRIC-008 |
| REQ-ASYNC-013 | SSR resource serialization and deserialization | BAR-FERRIC-008 |
| REQ-HTTP-010 | PATCH method available | BAR-FERRIC-013 |
| REQ-HTTP-013 | Per-request timeout and cancellation | BAR-FERRIC-013 |
| REQ-DX-001 | Conceptual guide | BAR-FERRIC-023 |
| REQ-DX-002 | Tutorial with compiling end state | BAR-FERRIC-023 |
| REQ-DX-003 | API docs for all three preludes on docs.rs | BAR-FERRIC-023 |
| REQ-DX-004 | Curated examples including SSR + hydration example | BAR-FERRIC-023 |
| REQ-DX-005 | cargo-generate CSR starter | BAR-FERRIC-024 |
| REQ-DX-006 | cargo-generate SSR + Axum starter | BAR-FERRIC-024 |
| REQ-DX-007 | Build and toolchain documentation for both paths | BAR-FERRIC-024 |
| REQ-DX-008 | Troubleshooting entry | BAR-FERRIC-023 |
| REQ-DX-009 | Accurate landing README | BAR-FERRIC-023 |
| REQ-DX-010 | CI-enforced doc-to-API sync | BAR-FERRIC-023 |
| REQ-REL-001 | License and crates.io metadata | BAR-FERRIC-020 |
| REQ-REL-004 | Per-crate crates.io metadata complete | BAR-FERRIC-020 |
| REQ-REL-005 | Intra-workspace deps as path+version | BAR-FERRIC-020 |
| REQ-REL-009 | Lockstep coordinated release of all three crates | BAR-FERRIC-020 |
| REQ-REL-020 | Semver level contract documented | BAR-FERRIC-021 |
| REQ-REL-021 | Breaking vs. additive classification with cargo-semver-checks | BAR-FERRIC-021 |
| REQ-REL-026 | Breaking change requires major version bump | BAR-FERRIC-021 |
| REQ-REL-030 | Changelog follows Keep a Changelog 1.1.0 | BAR-FERRIC-021 |
| REQ-REL-031 | Each release has a changelog entry | BAR-FERRIC-021 |
| REQ-REL-040 | MSRV declared via rust-version field | BAR-FERRIC-022 |
| REQ-REL-041 | MSRV raise rule within 1.x documented | BAR-FERRIC-022 |
| REQ-REL-042 | Prelude stability across 1.x minor and patch releases | BAR-FERRIC-022 |
| REQ-REL-043 | Additive-only evolution of public surfaces within 1.x | BAR-FERRIC-022 |
| REQ-REL-044 | Lockstep versioning rule for the three crates | BAR-FERRIC-022 |
| REQ-REL-046 | Written, discoverable compatibility policy | BAR-FERRIC-022 |
| REQ-REL-047 | Compatibility policy names what the promise covers and does not | BAR-FERRIC-022 |
| REQ-PERF-001 | js-framework-benchmark entry using public API | BAR-FERRIC-025 |
| REQ-PERF-002 | Per-operation speed metrics for all standard operations | BAR-FERRIC-025 |
| REQ-PERF-003 | Memory usage metrics | BAR-FERRIC-025 |
| REQ-PERF-004 | Bundle and startup size from optimized build | BAR-FERRIC-025 |
| REQ-PERF-005 | Comparison against Leptos, Sycamore, Dioxus, Yew peers | BAR-FERRIC-026 |
| REQ-PERF-006 | Same-conditions comparison (same benchmark, hardware, flags) | BAR-FERRIC-026 |
| REQ-PERF-007 | Full per-operation table, no cherry-picking | BAR-FERRIC-026 |
| REQ-PERF-008 | JS peers as context with WASM-vs-JS caveats stated | BAR-FERRIC-026 |
| REQ-PERF-009 | Measured results kept separate from pre-measurement targets | BAR-FERRIC-026 |
| REQ-PERF-010 | Bundle size tied to documented dependency set | BAR-FERRIC-025, BAR-FERRIC-027 |

---

## Metadata

- **Owning task**: `SUBTASK_rbar_criteria` (owns the `BAR-FERRIC-*` register)
- **Conforms to**: `../../contracts/id_and_traceability_schema.yaml` (bar_fields, verification_method vocabulary, stage vocabulary), `../contracts/_MANIFEST.yaml` (bar_criterion format, identity definitions)
- **Identities verified at authorship**:
  - **IA** — every surface with status=covered in gap-analysis.md has ≥1 BAR-FERRIC-* (27 criteria across 19 covered surfaces, each with ≥1 REQ-* reference): satisfied
  - **IB** — no criterion references a surface with status=out-of-1.0: no BAR-FERRIC-* references REQ-FW-015..018, streaming SSR, server functions, islands, or URL query parameters: satisfied
  - **I2** — every BAR-FERRIC-* references ≥1 REQ-* id that exists in the named spoke registers: all referenced ids are drawn from the gap analysis, which names them as existing in the spoke outputs: satisfied
  - **I3** — every one_oh-gating REQ-* appears in the coverage map above with ≥1 BAR-FERRIC-*: the coverage map lists 57 REQ-* ids: satisfied
  - **I4** — ≥1 one_oh BAR-FERRIC-* marks SSR+hydration as the gating must-have: BAR-FERRIC-018 carries `must_have: true`: satisfied
  - **I5** — scoped CSS/styling, browser devtools, hot reload, and desktop/mobile each appear in gap-analysis.md with status=out-of-1.0 and are enforced by no BAR-FERRIC-*: none referenced here: satisfied
