# Ferric 1.0 Release Bar

## 1. Introduction

The release bar defines what Ferric 1.0 must do before it ships. Each entry in the
`BAR-FERRIC-*` register is a checkable condition — a test, a build, an inspection, or
a benchmark — that someone outside the project can run against the live product and
reach the same pass/fail verdict. No entry is aspirational.

The bar answers three questions: what the framework can do, for whom, and when a given
condition must clear. It does not prescribe how any condition gets built.

**How to read this document**

- Every `BAR-FERRIC-*` entry carries: its id, a checkable statement, the `REQ-*`
  requirements it covers, the verification method, and the stage at which it must pass
  (`usable_early` or `one_oh`). The one gating `must_have` criterion is BAR-FERRIC-020.
- §4 (Coverage map) traces every `one_oh`/release-gating requirement to the criterion
  that covers it, organized by spoke area.
- §5 (Completeness and gap review) names every surface in the design — covered,
  out-of-1.0, or gap — with the recorded reasons.

---

## 2. Staging principle

The design document (`scope-and-requirements.md §5`) defines two stages:

**`usable_early`** — Requirements whose absence makes building a real application
impossible: the reactive primitives, the authoring macro, the component model, context,
async resources and suspense, forms, DOM events, client routing, HTTP client, a
stable-Rust WASM build, actionable macro diagnostics, client-side examples, and a
troubleshooting reference. Criteria at this stage must pass before any real application
can be built on the framework.

**`one_oh`** — Requirements that a credible 1.0 of this framework kind must provide
before it can be recommended to a new user: SSR and hydration, the reference
application, crates.io publishing, semver and compatibility policy, complete
documentation, a named-peer performance comparison with measured bundle size, and the
cargo-generate starter templates. All criteria at this stage must pass at the 1.0
release.

### The SSR+hydration gating requirement

SSR and hydration together constitute the one `must_have: true` condition in this
release bar. The requirement is BAR-FERRIC-020 (§3). A release that fails it — meaning
the client replaces or re-renders server-rendered DOM nodes on hydration — does not
meet the bar for 1.0, regardless of how many other criteria pass.

This is not a judgment that SSR matters more than the reactive model or the authoring
surface. It is the recorded position of the design: Ferric 1.0 is differentiated from
browser-only Rust/WASM frameworks by its SSR path. If that path cannot complete
hydration without a re-render, the product is a browser-only framework with incomplete
SSR code in it, not a 1.0.

---

## 3. BAR-FERRIC-* criteria

Criteria are grouped by capability area. Each entry lists stage, then must_have (only
BAR-FERRIC-020), then statement, then references, then verification method.

---

### Reactive state

**BAR-FERRIC-001** · stage: `usable_early`

`create_signal`, `create_memo`, `create_effect`, `batch`, and scoped cleanup all
function correctly against the frozen 276138f VNode surface. A change to a signal
propagates to all dependent memos and effects in one synchronous batch cycle.
Disposing a reactive scope runs all nested cleanup callbacks exactly once without
re-triggering any dependent effects.

References: REQ-FW-005, REQ-FW-009  
Verification: automated_test

---

### View macro and authoring

**BAR-FERRIC-002** · stage: `usable_early`

The `view!` macro accepts HTML elements with typed attributes and properties, dynamic
reactive expressions, conditional rendering via `if`/`else` inside the macro, and
`<For key=...>` keyed-list rendering with a user-supplied key function. All Band A
requirements (REQ-API-001..029) compile and run without unsafe code. A component
invocation inside `view!` passes props at the call site and renders the component's
output in place.

References: REQ-API-001, REQ-API-023, REQ-API-028  
Verification: automated_test

**BAR-FERRIC-003** · stage: `usable_early`

A trybuild test suite covers at least three classes of invalid `view!` invocations:
unrecognized element name, mismatched closing tag, and missing required prop. Each
class produces a compiler error that names the file, line, and the specific violation,
not a Rust-internals panic or a generic macro syntax error. The diagnostics are checked
by CI on every merge to `main`.

References: REQ-FW-014, REQ-API-001  
Verification: automated_test

---

### Component model

**BAR-FERRIC-004** · stage: `usable_early`

A component function decorated with `#[component]` and accepting required and optional
props (with `#[prop(default)]`) compiles. Children passed as `VNode` render at the
call site. An invalid prop type produces a compile-time diagnostic, not a runtime
panic.

References: REQ-API-030, REQ-API-031, REQ-API-032  
Verification: automated_test

**BAR-FERRIC-015** · stage: `one_oh`

A component whose `#[component]` macro derives `Into<Props>` accepts a bare literal
where a typed prop is expected at the call site. A slot declared with a type parameter
renders the caller-supplied view for each item in the parameter. A `DynComponent`
trait object accepts any component that matches the declared prop shape, and
substituting one implementation for another at the call site does not require changing
the parent component.

References: REQ-API-034, REQ-API-045, REQ-API-049  
Verification: automated_test

---

### Context

**BAR-FERRIC-005** · stage: `usable_early`

`provide_context`, `use_context`, and `expect_context` pass a value down the component
tree without prop drilling. `use_context` returns `None` when no provider is present
in any ancestor. `expect_context` panics with a message that names the missing type,
not a generic index-out-of-bounds or unwrap panic.

References: REQ-API-060, REQ-API-065, REQ-API-070  
Verification: automated_test

---

### Async resources and suspense

**BAR-FERRIC-006** · stage: `usable_early`

`create_resource` creates a resource that passes through loading, loaded, empty, and
error states across successive fetch cycles. A `<Suspense>` boundary renders its
fallback slot while any descendant resource is in the loading state and replaces it
with the resolved view on completion, without re-mounting the parent component. A
derived resource created via `create_memo` over a resource value reflects the source
resource's current state.

References: REQ-ASYNC-001, REQ-ASYNC-002, REQ-ASYNC-003, REQ-ASYNC-007,
REQ-ASYNC-009, REQ-ASYNC-011  
Verification: automated_test

**BAR-FERRIC-016** · stage: `one_oh`

A `create_resource` declared in a component rendered with `FerricSsr::render_to_string`
resolves its future before rendering completes. The resolved value appears in the HTML
output. On the client, `ferric_hydrate` reads the serialized value and does not issue
a second network request for the same resource key; the resource reaches the `Loaded`
state without a fetch.

References: REQ-ASYNC-012, REQ-ASYNC-013  
Verification: automated_test

---

### DOM events

**BAR-FERRIC-007** · stage: `usable_early`

The `on:` attribute form in `view!` handles submit, click, input, change, keydown,
keyup, focus, blur, and mouseenter events using a typed event payload. A handler can
call `event.prevent_default()` and `event.stop_propagation()` on the received event
object. The escape-hatch string form compiles for any valid DOM event name not covered
by the typed variants.

References: REQ-ASYNC-020, REQ-ASYNC-021, REQ-ASYNC-022, REQ-ASYNC-023,
REQ-ASYNC-024, REQ-FW-006  
Verification: automated_test

---

### Forms

**BAR-FERRIC-008** · stage: `usable_early`

`bind:value` connects a `WriteSignal<String>` to a text `<input>`, a `<textarea>`, and
a `<select>`. `bind:checked` connects a `WriteSignal<bool>` to a checkbox. On user
input the signal updates synchronously and any dependent memo or effect re-runs in the
same cycle. A form component that calls `prevent_default()` on submit and reads all
bound signals compiles and runs without requiring unsafe code.

References: REQ-ASYNC-040, REQ-ASYNC-041, REQ-ASYNC-042, REQ-ASYNC-043  
Verification: automated_test

---

### Client-side routing

**BAR-FERRIC-009** · stage: `usable_early`

A route table with static paths and `:param` path segments renders the correct
component at each URL. `<Outlet>` renders the matched component in place within the
parent layout. `<Link href="...">` navigates via the History API without a full-page
reload and is keyboard-focusable with `role="link"` announced by assistive technology.
`create_router()` accepts the route table and mounts to `document.body`.

References: REQ-RT-001, REQ-RT-002, REQ-RT-003, REQ-RT-004, REQ-RT-008  
Verification: example_build

**BAR-FERRIC-010** · stage: `usable_early`

A route with child routes renders a parent component containing a nested `<Outlet>`
that shows the matching child. An unmatched URL renders the route's declared fallback
component. Removing the fallback and navigating to an unmatched URL does not panic; the
router renders nothing for the outlet rather than unwrapping a missing value.

References: REQ-RT-005, REQ-RT-006  
Verification: automated_test

**BAR-FERRIC-017** · stage: `one_oh`

A `<Link>` element whose `href` matches the current URL carries `aria-current="page"`.
When navigation changes the URL away from that link, `aria-current` is removed on the
same tick. The active class (if one is configured on the `<Link>`) updates on the
same navigation cycle without requiring a manual signal write.

References: REQ-RT-007  
Verification: automated_test

---

### HTTP client

**BAR-FERRIC-011** · stage: `usable_early`

A `FerricClient` configured with a base URL issues GET, POST, PUT, and DELETE requests.
A request body serialized via `body_json` is sent with `Content-Type: application/json`.
A JSON response deserialized via `response_json::<T>` into a Rust struct succeeds when
the server's content-type is `application/json`. Non-2xx responses return
`Err(FerricHttpError::Status(status))` rather than `Ok`.

References: REQ-HTTP-001, REQ-HTTP-004, REQ-HTTP-005, REQ-HTTP-007, REQ-HTTP-008  
Verification: automated_test

**BAR-FERRIC-018** · stage: `one_oh`

A `FerricClient` request built with `.method(Method::Patch)` compiles and issues a
PATCH request. `.timeout(Duration::from_secs(5))` applied to a request returns
`Err(FerricHttpError::Timeout)` after five seconds if no response arrives.
`.cancel_token(token)` allows the caller to abort the in-flight request by dropping
the token; the cancelled future resolves to `Err(FerricHttpError::Cancelled)`.

References: REQ-HTTP-009, REQ-HTTP-010, REQ-HTTP-012  
Verification: automated_test

---

### WASM build

**BAR-FERRIC-012** · stage: `usable_early`

`cargo build --target wasm32-unknown-unknown` on the ferric workspace succeeds on the
stable Rust toolchain at the declared MSRV (workspace `rust-version = "1.82"`) with
no nightly feature flags. All three prelude crates (`ferric`, `ferric-ssr`,
`ferric-http`) link and produce valid WASM output. The build passes in CI without any
`--cfg` flags that are absent from stable.

References: REQ-FW-003  
Verification: automated_test

---

### Documentation and DX — early surfaces

**BAR-FERRIC-013** · stage: `usable_early`

A written troubleshooting guide covers at least five documented failure modes: missing
wasm-pack, missing `wasm32-unknown-unknown` target, CORS error from the dev server,
binary size above the documented threshold, and a hydration mismatch. Each entry names
the symptom, the probable cause, and the fix, with enough specificity to distinguish
it from a different error with a similar message.

References: REQ-DX-008  
Verification: doc_inspection

**BAR-FERRIC-014** · stage: `usable_early`

The `examples/` directory contains working client-side code covering reactive state,
component props and slots, context, async resources, forms, and routing. All
client-only examples pass `cargo check --target wasm32-unknown-unknown` on CI. Build
path documentation for the CSR path — installing trunk, adding the `wasm32-unknown-unknown`
target — is accurate for the declared MSRV and links to the relevant rustup command.

References: REQ-DX-004, REQ-DX-007  
Verification: example_build

---

### SSR and hydration

**BAR-FERRIC-019** · stage: `one_oh`

`FerricSsr::render_to_string(view)` returns a complete, valid HTML string on a native
server target (not wasm32) for any component tree that includes reactive state, context,
conditional rendering, and keyed lists. The server binary compiles without the
`wasm32-unknown-unknown` target and does not import `web-sys` or `wasm-bindgen`.

References: REQ-SSR-001, REQ-SSR-002, REQ-SSR-003  
Verification: automated_test

**BAR-FERRIC-020** · stage: `one_oh` · **must_have: true**

`ferric_hydrate(view, document.body)` attaches event handlers to existing
server-rendered markup without removing or replacing any DOM nodes. For a component
tree whose server-rendered and client-computed states agree, the number of DOM
mutations between the end of `FerricSsr::render_to_string` and the end of
`ferric_hydrate` is zero. This condition is verified by a MutationObserver wrapped
test, not by visual inspection.

References: REQ-SSR-004, REQ-FW-004  
Verification: automated_test

**BAR-FERRIC-021** · stage: `one_oh`

An event handler declared on a server-rendered element fires on the first user
interaction after `ferric_hydrate` completes, without requiring a re-render of the
surrounding component tree to wire the handler.

References: REQ-SSR-005  
Verification: automated_test

**BAR-FERRIC-022** · stage: `one_oh`

Signal state initialized on the server is carried into the serialized HTML and is
available to effects on the first client render cycle, before any user interaction.
A resource resolved during SSR serializes its payload into the state island. On the
client, `ferric_hydrate` reads that payload and the resource's initial client state
is `Loaded` without issuing a network request.

References: REQ-SSR-006, REQ-SSR-007, REQ-SSR-008  
Verification: automated_test

**BAR-FERRIC-023** · stage: `one_oh`

When server-rendered markup does not match the component tree's client-computed output,
the hydration layer records a structured diagnostic at the `FERRIC_HYDRATE_MISMATCH`
log target and falls back to a client-only render of the affected subtree. The mismatch
does not panic and does not silently lose event handlers on unaffected subtrees.

References: REQ-SSR-009  
Verification: automated_test

**BAR-FERRIC-024** · stage: `one_oh`

The serialized state island embedded in server-rendered HTML is escaped so that a
`</script>` sequence appearing in any serialized data value cannot close the island's
`<script>` tag. The escaped island survives a round-trip through an HTML parser
(DOMParser or equivalent) without alteration to its content.

References: REQ-SSR-010  
Verification: automated_test

**BAR-FERRIC-025** · stage: `one_oh`

An Axum handler that calls `FerricSsr::render_to_string(view)` and returns the result
as `Html<String>` compiles and serves a complete HTML page. The cargo-generate SSR
starter template wires this handler path by default so that a freshly generated
project serves a rendered page without modification.

References: REQ-SSR-011  
Verification: example_build

**BAR-FERRIC-026** · stage: `one_oh`

The SSR API surface — `FerricSsr::render_to_string`, `ferric_hydrate`, and the state
island mechanism — is additive over the frozen usable_early reactive and authoring
surfaces. No SSR-specific import path shadows or replaces a name declared stable in the
three preludes. Adding `ferric-ssr` as a server-target dependency does not change the
compilation of any code that imports only `ferric`.

References: REQ-SSR-012, REQ-FW-009  
Verification: automated_test

---

### Reference application

**BAR-FERRIC-027** · stage: `one_oh`

The `chirp-frontend` application, built against the released `ferric`, `ferric-ssr`,
and `ferric-http` crates from crates.io (not path dependencies), compiles to
`wasm32-unknown-unknown`, renders its landing page at the served URL, and exercises
all eight capability areas: reactive state, view macro, component model (props + slots),
context, async resources and suspense, client routing, HTTP client, and forms. The
application ships the SSR + hydrate code path; the server-rendered HTML and the
hydrated page produce the same visible content.

References: REQ-FW-008  
Verification: example_build

---

### Release, versioning, and compatibility

**BAR-FERRIC-028** · stage: `one_oh`

Each of the three crates (`ferric`, `ferric-ssr`, `ferric-http`) passes `cargo package
--dry-run` with no warnings. Each carries a SPDX `license` field, an `authors` list,
a non-empty `description`, a `repository` URL pointing to the live repository, and a
`documentation` URL pointing to docs.rs. No crate has a path-only dependency;
all intra-workspace deps use `{ workspace = true }` with a version field or an explicit
`version` key. `cargo publish --dry-run` succeeds from CI on every merge to `main`.

References: REQ-REL-001, REQ-REL-002, REQ-REL-003, REQ-REL-004, REQ-REL-005,
REQ-REL-006  
Verification: publishability

**BAR-FERRIC-029** · stage: `one_oh`

The crate names `ferric`, `ferric-ssr`, and `ferric-http` are owned by the project on
crates.io at the time of 1.0 publication. All three crates publish in one coordinated
CI run so their 1.0 versions appear in the registry simultaneously. `cargo add ferric`
from an empty project resolves to the 1.0 release without requiring a pre-release flag.

References: REQ-FW-001, REQ-REL-007, REQ-REL-008, REQ-REL-009, REQ-REL-010,
REQ-REL-011  
Verification: publishability

**BAR-FERRIC-030** · stage: `one_oh`

A written semver surface document identifies the public API of each crate — the three
preludes and their re-exported types, functions, and traits — and classifies each item
as `breaking`, `additive`, or `internal`. A `cargo-semver-checks` run against the
previous published version passes with no violations. The CI gate on `main` blocks any
merge that introduces a semver violation to the classified public surface.

References: REQ-FW-010, REQ-REL-020, REQ-REL-021, REQ-REL-022, REQ-REL-023,
REQ-REL-025, REQ-REL-026  
Verification: doc_inspection

**BAR-FERRIC-031** · stage: `one_oh`

A `CHANGELOG.md` following Keep a Changelog 1.1.0 exists at the repository root and
is updated before every release. Every released version entry has at least one of
`[Added]`, `[Changed]`, or `[Fixed]`. Breaking changes carry an `[BREAKING]` prefix
in the entry. Each crate's changes are namespaced so a reader can filter by crate
without reading unrelated entries. The changelog covers all releases from 1.0 forward;
the `[Unreleased]` section is non-empty on any branch with unreleased commits.

References: REQ-REL-024, REQ-REL-027, REQ-REL-028, REQ-REL-029, REQ-REL-030,
REQ-REL-031, REQ-REL-032, REQ-REL-033  
Verification: doc_inspection

**BAR-FERRIC-032** · stage: `one_oh`

The workspace `[workspace.package]` section declares `rust-version`. The declared
value is the lowest stable Rust release on which `cargo test` passes on the CI matrix.
A written policy (in the compatibility document or the contributing guide) states that
MSRV may rise only in a minor release — not a patch release — and that the rise is
recorded in the changelog. The CI matrix includes a job that builds and runs tests on
the declared MSRV value.

References: REQ-FW-003, REQ-REL-040, REQ-REL-041  
Verification: doc_inspection

**BAR-FERRIC-033** · stage: `one_oh`

A discoverable written compatibility policy states what the 1.x stability promise
covers — the three preludes and their public re-exports — and what it does not cover:
items under `ferric::internal`, proc-macro internals, and any item behind an unstable
feature flag. The policy states the rule for MSRV changes within 1.x. It is linked
from the repository README and the crates.io description for each crate. Changes to
the preludes in any 1.x minor release are additive only; no name exported from a
prelude at 1.0 is removed or renamed in any 1.x release.

References: REQ-REL-042, REQ-REL-043, REQ-REL-044, REQ-REL-045, REQ-REL-046,
REQ-REL-047  
Verification: doc_inspection

---

### Documentation and DX — one_oh surfaces

**BAR-FERRIC-034** · stage: `one_oh`

A written conceptual guide covers the reactive model (signals, memos, effects,
ownership and scope), the component model (props, children, slots, context), and the
async model (resources, suspense). A start-to-finish tutorial whose declared end state
is a working browser application compiles on the project's MSRV when the reader
follows the steps literally; the tutorial skips no required installation or toolchain
step.

References: REQ-DX-001, REQ-DX-002  
Verification: doc_inspection

**BAR-FERRIC-035** · stage: `one_oh`

All public items in the three preludes carry a doc comment. docs.rs builds each crate
without missing-doc warnings. The doc comment for every type, trait, and public
function exported from a prelude includes a usage example that passes `cargo test --doc`.
CI keeps the examples and doctests passing on every merge to `main`.

References: REQ-DX-003, REQ-DX-010, REQ-FW-011  
Verification: doc_inspection

**BAR-FERRIC-036** · stage: `one_oh`

`cargo generate ferric/ferric-templates --name my-app` produces a CSR project that
compiles to WASM and serves a "Hello, Ferric!" page with `trunk serve` without
modification. A second template, selected with `--template ssr`, produces a project
that compiles and serves an SSR + hydrate Axum application without modification. Both
templates match the tutorial's project layout and naming so the tutorial can be
continued from either scaffold without restructuring.

References: REQ-DX-005, REQ-DX-006, REQ-FW-002  
Verification: example_build

**BAR-FERRIC-037** · stage: `one_oh`

Build and toolchain documentation for the SSR + Axum path covers: adding the
`wasm32-unknown-unknown` target, structuring the workspace with a server member and a
client member, running the server binary and serving the compiled WASM in development,
and the production build step. The documentation is accurate for the current stable
Rust version and links from the SSR template's generated README.

References: REQ-DX-007  
Verification: doc_inspection

**BAR-FERRIC-038** · stage: `one_oh`

The `examples/` directory contains a complete SSR + hydrate example that compiles and
runs against the published `ferric-ssr` crate (not a path dependency). The example
produces a server-rendered page, completes hydration with zero DOM mutations on the
happy path (verified with a MutationObserver), and includes at least one interactive
element — a click counter — that functions correctly after hydration without a
re-render.

References: REQ-DX-004  
Verification: example_build

**BAR-FERRIC-039** · stage: `one_oh`

The repository README states what Ferric is; lists the three crate names and their
roles; shows a minimal working `view!` example that is compile-verified in CI; links
to the conceptual guide, the tutorial, and the compatibility policy; states the MSRV
and target platform (`wasm32-unknown-unknown`); and states the current release version.
No claim in the README contradicts the shipped API, and the README is checked for
drift by CI.

References: REQ-DX-009  
Verification: doc_inspection

---

### Performance

**BAR-FERRIC-040** · stage: `one_oh`

A Ferric entry in the js-framework-benchmark `keyed` category uses the framework's
public `view!` API — no hand-crafted DOM calls — and runs on the benchmark's own
harness without modification to the harness. The entry reports per-operation timings
(create rows, replace all rows, partial update, select row, swap rows, remove row,
append rows, clear rows), geometric mean, memory after creation, and binary and
startup size from the optimized WASM build (release profile + wasm-opt).

References: REQ-FW-012, REQ-PERF-001, REQ-PERF-002, REQ-PERF-003, REQ-PERF-004,
REQ-PERF-005  
Verification: benchmark_run

**BAR-FERRIC-041** · stage: `one_oh`

The benchmark writeup states the exact version of each named Rust/WASM peer measured
(Leptos, Sycamore, Dioxus, Yew). All comparisons use the `keyed` category. The report
shows the full per-operation table; no operations are omitted or averaged away. Measured
results are presented separately from any pre-measurement targets. The writeup includes
a note that WASM and JS frameworks differ in how memory and bundle size are reported,
so the raw numbers are not directly comparable across runtime targets.

References: REQ-PERF-006, REQ-PERF-007, REQ-PERF-008, REQ-PERF-009  
Verification: benchmark_run

**BAR-FERRIC-042** · stage: `one_oh`

The optimized WASM binary size from the benchmark build (release + wasm-opt) is
reported alongside the declared dependency set. The measured size does not exceed the
lean-footprint threshold documented in REQ-FW-013. Removing any non-test, non-dev
dependency from the `ferric` crate increases the compilation failure count in the test
suite, confirming the declared dependency set is not padded with unused crates.

References: REQ-FW-013, REQ-PERF-010  
Verification: benchmark_run

---

## 4. Coverage map

Every `one_oh` / `release_gating: true` requirement and the BAR-FERRIC-* criterion
that covers it. Usable_early requirements covered by one_oh criteria are included where
the criterion statement spans both stages.

### REQ-FW

| Requirement | Criterion |
|---|---|
| REQ-FW-001 | BAR-FERRIC-029 |
| REQ-FW-002 | BAR-FERRIC-036 |
| REQ-FW-004 | BAR-FERRIC-020 |
| REQ-FW-008 | BAR-FERRIC-027 |
| REQ-FW-010 | BAR-FERRIC-030 |
| REQ-FW-011 | BAR-FERRIC-035 |
| REQ-FW-012 | BAR-FERRIC-040 |
| REQ-FW-013 | BAR-FERRIC-042 |

### REQ-SSR

| Requirement | Criterion |
|---|---|
| REQ-SSR-001 | BAR-FERRIC-019 |
| REQ-SSR-002 | BAR-FERRIC-019 |
| REQ-SSR-003 | BAR-FERRIC-019 |
| REQ-SSR-004 | BAR-FERRIC-020 |
| REQ-SSR-005 | BAR-FERRIC-021 |
| REQ-SSR-006 | BAR-FERRIC-022 |
| REQ-SSR-007 | BAR-FERRIC-022 |
| REQ-SSR-008 | BAR-FERRIC-022 |
| REQ-SSR-009 | BAR-FERRIC-023 |
| REQ-SSR-010 | BAR-FERRIC-024 |
| REQ-SSR-011 | BAR-FERRIC-025 |
| REQ-SSR-012 | BAR-FERRIC-026 |

### REQ-API

| Requirement | Criterion |
|---|---|
| REQ-API-034 | BAR-FERRIC-015 |
| REQ-API-045 | BAR-FERRIC-015 |
| REQ-API-049 | BAR-FERRIC-015 |

### REQ-ASYNC

| Requirement | Criterion |
|---|---|
| REQ-ASYNC-012 | BAR-FERRIC-016 |
| REQ-ASYNC-013 | BAR-FERRIC-016 |

### REQ-RT

| Requirement | Criterion |
|---|---|
| REQ-RT-007 | BAR-FERRIC-017 |

### REQ-HTTP

| Requirement | Criterion |
|---|---|
| REQ-HTTP-009 | BAR-FERRIC-018 |
| REQ-HTTP-010 | BAR-FERRIC-018 |
| REQ-HTTP-012 | BAR-FERRIC-018 |

### REQ-DX

| Requirement | Criterion |
|---|---|
| REQ-DX-001 | BAR-FERRIC-034 |
| REQ-DX-002 | BAR-FERRIC-034 |
| REQ-DX-003 | BAR-FERRIC-035 |
| REQ-DX-004 (SSR example) | BAR-FERRIC-038 |
| REQ-DX-005 | BAR-FERRIC-036 |
| REQ-DX-006 | BAR-FERRIC-036 |
| REQ-DX-007 (SSR build path) | BAR-FERRIC-037 |
| REQ-DX-009 | BAR-FERRIC-039 |
| REQ-DX-010 | BAR-FERRIC-035 |

### REQ-REL

| Requirement | Criterion |
|---|---|
| REQ-REL-001 | BAR-FERRIC-028 |
| REQ-REL-002 | BAR-FERRIC-028 |
| REQ-REL-003 | BAR-FERRIC-028 |
| REQ-REL-004 | BAR-FERRIC-028 |
| REQ-REL-005 | BAR-FERRIC-028 |
| REQ-REL-006 | BAR-FERRIC-028 |
| REQ-REL-007 | BAR-FERRIC-029 |
| REQ-REL-008 | BAR-FERRIC-029 |
| REQ-REL-009 | BAR-FERRIC-029 |
| REQ-REL-010 | BAR-FERRIC-029 |
| REQ-REL-011 | BAR-FERRIC-029 |
| REQ-REL-020 | BAR-FERRIC-030 |
| REQ-REL-021 | BAR-FERRIC-030 |
| REQ-REL-022 | BAR-FERRIC-030 |
| REQ-REL-023 | BAR-FERRIC-030 |
| REQ-REL-025 | BAR-FERRIC-030 |
| REQ-REL-026 | BAR-FERRIC-030 |
| REQ-REL-028 | BAR-FERRIC-031 |
| REQ-REL-029 | BAR-FERRIC-031 |
| REQ-REL-030 | BAR-FERRIC-031 |
| REQ-REL-031 | BAR-FERRIC-031 |
| REQ-REL-032 | BAR-FERRIC-031 |
| REQ-REL-033 | BAR-FERRIC-031 |
| REQ-REL-040 | BAR-FERRIC-032 |
| REQ-REL-041 | BAR-FERRIC-032 |
| REQ-REL-042 | BAR-FERRIC-033 |
| REQ-REL-043 | BAR-FERRIC-033 |
| REQ-REL-044 | BAR-FERRIC-033 |
| REQ-REL-045 | BAR-FERRIC-033 |
| REQ-REL-046 | BAR-FERRIC-033 |
| REQ-REL-047 | BAR-FERRIC-033 |

### REQ-PERF

| Requirement | Criterion |
|---|---|
| REQ-PERF-001 | BAR-FERRIC-040 |
| REQ-PERF-002 | BAR-FERRIC-040 |
| REQ-PERF-003 | BAR-FERRIC-040 |
| REQ-PERF-004 | BAR-FERRIC-040 |
| REQ-PERF-005 | BAR-FERRIC-040 |
| REQ-PERF-006 | BAR-FERRIC-041 |
| REQ-PERF-007 | BAR-FERRIC-041 |
| REQ-PERF-008 | BAR-FERRIC-041 |
| REQ-PERF-009 | BAR-FERRIC-041 |
| REQ-PERF-010 | BAR-FERRIC-042 |

---

## 5. Completeness and gap review

### Surface table

Sources: `SUBTASK_rbar_gap_review/gap-analysis.md` (primary) and
`SUBTASK_rbar_gap/gap-analysis-internal.md` (cross-check). Both analyses agree on all
status assignments. The cross-check note records that the sibling's output was not
readable during its independent run; the findings are aligned.

#### Required surfaces

| Surface | Status | REQ-refs | Notes |
|---|---|---|---|
| Reactive state model (signals, memos, effects, batch) | covered | REQ-FW-005 | REQ-FW-005 requires fine-grained signal reactivity and the frozen 276138f surface. |
| Virtual DOM and DOM patching | covered | REQ-FW-005, REQ-API-001 | The keyed VNode diff applied via web-sys; REQ-FW-005 covers the reactive rendering model, REQ-API-001 the view macro authoring interface. |
| Server-side rendering (SSR) | covered | REQ-SSR-001, REQ-SSR-002, REQ-SSR-003, REQ-SSR-011 | REQ-SSR-001..003 cover render to HTML, off-WASM build, and per-request isolation; REQ-SSR-011 covers Axum integration. |
| Hydration (no re-render on client pick-up) | covered | REQ-SSR-004, REQ-SSR-005, REQ-SSR-007, REQ-SSR-008, REQ-SSR-009 | REQ-SSR-004 is the gating must-have. The remaining ids cover event wiring, state carry, first-render determinism, and mismatch detection. |
| Authoring ergonomics / view macro | covered | REQ-API-001 | Band A (REQ-API-001..029) covers the full `view!` macro surface, all stage usable_early. |
| Component model (props, children, slots) | covered | REQ-API-030, REQ-API-034, REQ-API-045, REQ-API-049 | Band B (REQ-API-030..052) covers typed props, optional props, children, and slots; REQ-API-034, 045, 049 are one_oh. |
| Context / dependency injection | covered | REQ-API-060 | Band C (REQ-API-060..070) covers provide/use/expect_context, all usable_early. |
| Async resources and suspense | covered | REQ-ASYNC-001, REQ-ASYNC-012, REQ-ASYNC-013 | REQ-ASYNC-001..016 cover async resource creation, four suspense states, derived resources, and the SSR seam; REQ-ASYNC-012..013 are one_oh. |
| Forms and two-way data binding | covered | REQ-ASYNC-040, REQ-ASYNC-041, REQ-ASYNC-042, REQ-ASYNC-043 | REQ-ASYNC-040..043 cover two-way binding for the full input-kind range, all usable_early. |
| DOM event handling | covered | REQ-ASYNC-020, REQ-ASYNC-021, REQ-FW-006 | REQ-ASYNC-020..024 and REQ-FW-006 cover the typed handler form and the full DOM event range, all usable_early. |
| Client-side routing | covered | REQ-RT-001, REQ-RT-002, REQ-RT-003, REQ-RT-004, REQ-RT-005, REQ-RT-006, REQ-RT-007, REQ-RT-008 | REQ-RT-001..008 cover path params, reactive outlet, History navigation, focusable links, nested routes, fallback, and active-route awareness. |
| HTTP / JSON client | covered | REQ-HTTP-001, REQ-HTTP-004, REQ-HTTP-005, REQ-HTTP-007, REQ-HTTP-008, REQ-HTTP-009, REQ-HTTP-010, REQ-HTTP-013 | REQ-HTTP-001..013 cover client config, fluent request building, JSON round-trip, the error model, PATCH (one_oh), and timeout/cancel (one_oh). |
| Developer documentation (guide, tutorial, API reference) | covered | REQ-DX-001, REQ-DX-002, REQ-DX-003, REQ-DX-004, REQ-DX-008, REQ-DX-009, REQ-DX-010 | REQ-DX-001..010 require the conceptual guide, tutorial, API docs, examples, troubleshooting reference, and landing README. |
| DX (starter template, cargo-generate, error messages) | covered | REQ-DX-005, REQ-DX-006, REQ-DX-007, REQ-FW-014 | REQ-DX-005..007 cover the cargo-generate CSR and SSR starters and the build path docs; REQ-FW-014 owns macro diagnostic quality. |
| Release and publishing (crates.io, semver, changelog) | covered | REQ-REL-001, REQ-REL-004, REQ-REL-005, REQ-REL-009, REQ-REL-020, REQ-REL-021, REQ-REL-026, REQ-REL-030, REQ-REL-031 | REQ-REL-001..011 cover publishing readiness and lockstep release; REQ-REL-020..033 cover semver classification and changelog practice. |
| Versioning / compatibility policy | covered | REQ-REL-040, REQ-REL-041, REQ-REL-042, REQ-REL-043, REQ-REL-044, REQ-REL-046, REQ-REL-047 | REQ-REL-040..047 declare the MSRV policy, frozen-prelude stability, additive-only evolution, and a written discoverable compat policy. |
| Performance and bundle size | covered | REQ-PERF-001, REQ-PERF-002, REQ-PERF-003, REQ-PERF-004, REQ-PERF-010 | REQ-PERF-001..005 and REQ-PERF-010 require the js-framework-benchmark entry and measured bundle size tied to the lean-footprint commitment. |
| Named-peer comparison methodology | covered | REQ-PERF-005, REQ-PERF-006, REQ-PERF-007, REQ-PERF-008, REQ-PERF-009 | REQ-PERF-006..009 require stated comparison method, named Rust/WASM peers, full per-operation reporting, and the WASM-vs-JS caveat. |
| MSRV policy | covered | REQ-FW-003, REQ-REL-040, REQ-REL-041 | REQ-FW-003 anchors usable_early to stable Rust; REQ-REL-040 commits 1.0 to a declared MSRV; REQ-REL-041 states the MSRV-raise rule within 1.x. |
| Accessibility of framework output (ARIA, semantic HTML) | **gap** | — | No REQ-* in any spoke requires the framework's generated markup to meet an accessibility standard for general components. REQ-RT-004 and REQ-RT-007 require the link component to carry role="link" and aria-current, but that is a routing-specific provision, not a framework-level accessibility guarantee. |
| Testing story (how app authors test components, routes, async) | **gap** | — | No REQ-* specifies a testing harness, helper crate, or methodology for app authors testing their own Ferric components, routes, or async resources. REQ-FW-014 and REQ-API-* address trybuild diagnostics for the framework itself; neither addresses the app author's testing surface. |
| Scoped CSS / styling story | out-of-1.0 | — | REQ-FW-015 defers scoped CSS and a first-class styling story to post-1.0. App authors use global stylesheets or external CSS tooling for 1.0. |
| Browser devtools / inspector integration | out-of-1.0 | — | REQ-FW-016 defers component inspector and signal viewer integration to post-1.0. |
| Hot reload / live reload | out-of-1.0 | — | REQ-FW-017 defers hot/live reload to post-1.0. The edit-rebuild-refresh loop is the documented 1.0 development path. |
| Desktop / mobile targets (non-WASM) | out-of-1.0 | — | REQ-FW-018 defers non-WASM targets to post-1.0. Ferric 1.0 targets wasm32-unknown-unknown only. |

#### Additional surfaces found in spoke docs

| Surface | Status | REQ-refs | Notes |
|---|---|---|---|
| Streaming SSR | out-of-1.0 | — | The SSR design records streaming SSR as outside the 1.0 bar with no REQ-SSR-* assigned. The 1.0 model is full-page, eager server rendering. |
| Server functions / server actions | out-of-1.0 | — | The SSR design records server functions and server actions as outside the 1.0 bar. The async resource pattern (REQ-ASYNC-001..016) is the 1.0 data-loading model. |
| Islands / partial hydration | out-of-1.0 | — | The SSR design records islands architecture and partial hydration as outside the 1.0 bar. REQ-SSR-004 covers full-page hydration only. |
| URL query / search parameters | out-of-1.0 | — | REQ-RT-009 records router-owned reactive query/search-string parameters as a post-1.0 deferral. App authors can read `window.location.search` directly for 1.0. |

---

### Out-of-1.0 items — summary

The four items named in identity I5 are all recorded with status `out-of-1.0`:

1. **Scoped CSS / styling story** — REQ-FW-015, post-1.0 deferral
2. **Browser devtools / inspector** — REQ-FW-016, post-1.0 deferral
3. **Hot reload / live reload** — REQ-FW-017, post-1.0 deferral
4. **Desktop / mobile (non-WASM)** — REQ-FW-018, post-1.0 deferral

No BAR-FERRIC-* criterion references any of these four surfaces or their REQ-* ids.

---

### Gaps

Two surfaces have no REQ-* coverage in any spoke register:

1. **Accessibility of framework output** — no criterion is written. The gap is recorded
   here for visibility. It does not block the 1.0 release bar because no release-gating
   requirement exists for it; it is a candidate for a post-1.0 design pass.

2. **Testing story for app authors** — no criterion is written. Same status as above.
   The framework's own acceptance suite uses automated_test as its verification method
   throughout, but none of the spoke documents specify what testing surface, if any, the
   framework exposes to app authors.

---

### Summary counts

| Category | Count |
|---|---|
| BAR-FERRIC-* criteria total | 42 |
| stage: usable_early | 14 |
| stage: one_oh | 28 |
| must_have: true | 1 (BAR-FERRIC-020) |
| Surfaces covered | 18 |
| Surfaces out-of-1.0 | 7 (4 canonical + 3 additional) |
| Gaps (no REQ-* coverage) | 2 |
