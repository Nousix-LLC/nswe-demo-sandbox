# Concern Findings: Framework Scope & 1.0 Requirements

## concern_name

Framework scope & 1.0 requirements

## document_validated

`design/ferric/scope-and-requirements.md` on branch `work/design-ferric-1_0`

## req_ids_found

REQ-FW-001, REQ-FW-002, REQ-FW-003, REQ-FW-004, REQ-FW-005, REQ-FW-006, REQ-FW-007,
REQ-FW-008, REQ-FW-009, REQ-FW-010, REQ-FW-011, REQ-FW-012, REQ-FW-013, REQ-FW-014,
REQ-FW-015, REQ-FW-016, REQ-FW-017, REQ-FW-018

REQ-FW-001–014: 1.0 requirements (`release_gating: true`), staged `usable_early`
(003, 005, 006, 007, 009, 014) or `one_oh` (001, 002, 004, 008, 010, 011, 012, 013).

REQ-FW-015–018: post-1.0 deferrals (`release_gating: false`).

Cross-references to sibling registers named in-document (read-only; formal validation
deferred to SUBTASK_validate-crossrefs): REQ-SSR-*, REQ-API-*, REQ-ASYNC-*, REQ-RT-*,
REQ-HTTP-*, REQ-DX-*, REQ-REL-*, REQ-PERF-*, BAR-FERRIC-*.

## status

needs-fix

## specific_issues

- type: completeness
  description: >
    No framework-level accessibility requirement appears in REQ-FW-* or in the out-of-1.0
    list. The document covers REQ-FW-008 (build a real app) and REQ-FW-005 (declarative
    authoring) without stating any framework-level accessibility expectation: whether ARIA
    attributes are supported on generated view-macro elements, whether the keyed-diff
    rendering preserves accessibility-tree integrity, whether the hydration pass avoids
    breaking screen-reader state. REQ-FW-006's "full range of DOM events" covers keyboard
    events at the handler level but does not address keyboard navigation or focus management
    as a framework concern. The item is absent from §6 as well, making it a silent omission
    rather than a deliberate deferral.
  severity: major

- type: completeness
  description: >
    Component-level error handling is not addressed. The document delegates async
    loading/error states to REQ-ASYNC-* and authoring-time diagnostics to REQ-FW-014, but
    says nothing about what happens when an error occurs during component rendering (a
    render-time panic, a signal update that throws). WASM panics currently abort the thread,
    which means any unhandled component error crashes the whole app. Peers address this with
    error boundary components (Leptos ErrorBoundary, Vue 3 onErrorCaptured, React error
    boundaries). A real app (REQ-FW-008) that cannot contain rendering errors is not
    production-credible, yet this concern appears nowhere in the requirements or in the
    out-of-1.0 deferrals.
  severity: major

- type: testability
  description: >
    REQ-FW-013 acceptance criterion uses "narrowly-scoped additions justified per crate"
    without a measurable reference. A reviewer cannot make a reproducible pass/fail
    determination: "narrowly-scoped" and "justified" are qualitative, not checkable. The
    acceptance criterion should name the expected dependency set explicitly (e.g. "the
    `ferric` crate depends on `wasm-bindgen`, `web-sys`, `js-sys` only; `ferric-http` adds
    `serde`, `serde_json`, `wasm-bindgen-futures`") or specify a bundle-size ceiling that
    can be measured against the performance numbers.
  severity: minor

## gaps

- id: GAP-001
  description: >
    Accessibility requirements absent from the framework scope. The document does not
    address ARIA attribute support on view-macro elements, accessibility-tree integrity
    under keyed-diff rendering and hydration, or focus management as a framework-level
    concern. The out-of-1.0 list does not mention accessibility, making this a silent
    omission. Every Rust-peer framework that targets production web apps (Leptos, Sycamore)
    expects authors to set ARIA attributes and relies on the framework not stripping or
    reordering them; the 1.0 document should state Ferric's position.
  severity: major
  action_required: >
    Add a cross-cutting framework-level accessibility statement — either a REQ-FW-* (if
    the framework commits to anything beyond "ARIA attributes pass through to the DOM") or
    an explicit post-1.0 deferral in §6 with a reason. At minimum the statement should
    address: (a) whether ARIA attributes on `view!`-macro elements are preserved to the real
    DOM, (b) whether the keyed diff and hydration pass maintain accessibility-tree integrity,
    and (c) whether focus management is in scope for 1.0 or deferred.

- id: GAP-002
  description: >
    Component error handling / error boundaries not addressed or explicitly deferred. The
    document has no requirement and no deferral entry for how Ferric handles errors thrown
    during component rendering. WASM panics abort the thread; without an error-boundary
    mechanism one component error takes down the whole app. This is a framework-level
    concern orthogonal to async loading errors (REQ-ASYNC-*) and authoring diagnostics
    (REQ-FW-014).
  severity: major
  action_required: >
    Add either (a) a cross-cutting REQ-FW-* requirement for component-level error
    containment (an error-boundary mechanism that catches render errors and renders a
    fallback UI without crashing the rest of the tree), or (b) an explicit post-1.0
    deferral entry in §6 acknowledging that WASM-thread panics are not yet bounded and
    stating the intended post-1.0 direction. Leaving it silently absent makes the 1.0
    release bar incomplete for production use.

- id: GAP-003
  description: >
    Testing utilities are not mentioned or explicitly deferred. The document neither
    includes a requirement for a test-friendly rendering path (running components in a
    headless or simulated-DOM environment) nor lists this as a known post-1.0 deferral.
    Peers (Leptos, Dioxus) and the broader web-framework ecosystem (testing-library for
    React/Vue) provide or document component-testing support. Its absence from §6 makes
    it a silent omission.
  severity: minor
  action_required: >
    Add an entry to §6 explicitly deferring component testing utilities to post-1.0 (with a
    reason, per the pattern used for REQ-FW-015–018), or add a minimal cross-cutting
    requirement noting that the framework's rendering is callable outside a browser context
    (or that it is not, and why). The goal is an explicit position, not silence.

- id: GAP-004
  description: >
    REQ-FW-013 acceptance criterion for "lean dependency footprint" is not reproducibly
    testable as written. "Narrowly-scoped additions justified per crate" leaves the pass/fail
    decision to the reviewer's judgment. A different reviewer might reach a different
    conclusion without a concrete reference to measure against.
  severity: minor
  action_required: >
    Replace the qualitative phrase with a named expected dependency set or a measurable
    threshold. For example: state that `ferric`'s transitive required dependencies are
    `wasm-bindgen`, `web-sys`, and `js-sys`; that `ferric-http` adds `serde`, `serde_json`,
    and `wasm-bindgen-futures`; and that any addition beyond this baseline requires a
    documented rationale in the crate's `Cargo.toml` comment. Tie the criterion to the
    bundle-size numbers required by REQ-FW-012 so "lean" is falsifiable against a measured
    result.
