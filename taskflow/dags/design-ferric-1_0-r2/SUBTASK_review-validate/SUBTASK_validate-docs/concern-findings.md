# concern-findings: Documentation & Developer Experience

## concern_name

Documentation & Developer Experience

---

## document_validated

`design/ferric/docs-and-dx.md` on branch `work/design-ferric-1_0`

---

## req_ids_found

- REQ-DX-001 — A conceptual guide
- REQ-DX-002 — A start-to-finish tutorial whose end state compiles
- REQ-DX-003 — Rendered API documentation for the public surface
- REQ-DX-004 — A curated examples set across the capability span
- REQ-DX-005 — A cargo-generate starter template
- REQ-DX-006 — The "new user → working app" acceptance path
- REQ-DX-007 — Build and toolchain documentation (client and SSR)
- REQ-DX-008 — Troubleshooting and diagnostics documentation
- REQ-DX-009 — An accurate README / landing for the evaluating author
- REQ-DX-010 — Documentation and examples kept in sync with the release

All ten are `release_gating: true`. Eight are `one_oh`; REQ-DX-004 (client-side examples) and
REQ-DX-007 (client build path) carry a `usable_early` tier for their client-side halves; REQ-DX-008
is fully `usable_early`. No `REQ-DX-*` is `post_one_oh`.

---

## status

needs-fix

---

## specific_issues

- type: testability
  severity: minor
  description: >
    REQ-DX-001 acceptance criterion reads "a reviewer confirms each topic is present and that its
    description matches the shipped behavior for a stated example." The phrase "a stated example"
    names no specific example; a reviewer checking this independently does not know which artifact to
    run to verify behavioral accuracy. The design should name the example (e.g. the tutorial end-state
    app, or the counter) against which guide claims are validated, or state that any named example in
    the guide itself supplies the reference.

- type: testability
  severity: minor
  description: >
    REQ-DX-006 acceptance bar requires that a reviewer "reaches a running app at each stage" — a
    functional bar with no effort ceiling. A path that is technically completable but requires several
    hours of debugging missing toolchain steps would satisfy the criterion as written. For a DX
    requirement whose explicit purpose is "the one the framework's first minute is judged by," the
    acceptance bar should state a maximum setup time or characterize the expected effort (e.g.,
    "within one working session on a standard workstation"), so a painful path does not pass as done.

- type: testability
  severity: minor
  description: >
    REQ-DX-008 requires "a troubleshooting section...listing a stated set of common mistakes."
    The requirement names three illustrative examples parenthetically (malformed view!, misused prop,
    missing mount element) but does not declare the minimum set the design mandates. As written, the
    build team defines the set rather than building to a design-specified minimum, leaving the
    requirement's bar underdetermined. The design should enumerate the minimum cases the section must
    cover so a reviewer can check completeness without reverse-engineering what was intended.

---

## gaps

- id: GAP-050
  description: >
    REQ-DX-006 acceptance bar has no effort ceiling. "Completes the four documented steps...and
    reaches a running app at each stage" is a functional pass/fail with no time or complexity bound,
    which means a newcomer spending a full day on toolchain errors could still satisfy it. The
    requirement is the integrating DX bar; it should add a stated effort expectation so the path is
    not just possible but practical.
  severity: minor
  action_required: >
    Add an effort bound to the REQ-DX-006 acceptance criteria — for example: "a reviewer unfamiliar
    with Ferric completes all four steps within [N hours / one working session] on a current
    workstation following only the documented path, with no steps that require out-of-band knowledge."

- id: GAP-051
  description: >
    REQ-DX-001 acceptance criterion references "a stated example" for behavioral verification without
    naming the example. The reviewer has no anchor for what to run when checking that guide
    descriptions match shipped behavior, leaving the verification step underspecified.
  severity: minor
  action_required: >
    Specify in REQ-DX-001 acceptance criteria which artifact supplies the behavioral ground truth —
    e.g., "a reviewer reads the guide's description of a named capability (reactivity, routing, forms)
    and confirms the behavior against the tutorial end-state app or against the relevant example in
    REQ-DX-004."

- id: GAP-052
  description: >
    REQ-DX-008 defers the minimum case list for the troubleshooting section to the build — "a stated
    set of common mistakes" means the section itself declares the set, not that the design has
    declared it. A reviewer checking completeness against the design has no reference list, so the
    bar is effectively set at build time rather than design time.
  severity: minor
  action_required: >
    Enumerate in REQ-DX-008 the minimum set of common mistakes the troubleshooting section must cover
    (e.g., malformed view! macro, misused prop type, missing mount-point element, type-mismatch on a
    signal, incorrect async resource usage). Three parenthetical examples are a hint, not a bar.

---

## validation notes

All six brief criteria were assessed against the document:

1. **Conceptual guide as 1.0 requirement** — REQ-DX-001 is `one_oh`, `release_gating: true`, with
   explicit acceptance criteria and peer rationale (Leptos Book, Dioxus guide, Yew guide). Passes.

2. **Tutorial with stated acceptance bar** — REQ-DX-002 requires the end-state source to build to
   `wasm32-unknown-unknown` and run as described using only documented commands. The bar is concrete
   and independently checkable. Passes.

3. **API reference docs with stated scope** — REQ-DX-003 covers all public items across the three
   preludes (ferric, ferric-router, ferric-http), crate-level overviews, intra-doc links, and a clean
   `cargo doc` run. Scope is fully stated. Passes.

4. **cargo-generate starter template** — REQ-DX-005 addresses both a CSR starter and an SSR+Axum
   variant, with peer comparison (Leptos start-trunk, Dioxus dx new, Yew Trunk scaffold) supporting
   the rationale. Passes.

5. **DX acceptance bar in newcomer-checkable terms** — REQ-DX-006 defines a four-step path
   (prerequisites → scaffold → serve → tutorial) and requires a first-time reviewer to reach a
   running app at each stage using only the documentation. The bar is checkable but lacks an effort
   ceiling (GAP-050). Partially passes.

6. **Freshness** — Document is grounded at commit `276138f` on `main`, current peer tooling is named
   accurately (Leptos start-trunk / cargo leptos new, Dioxus dx new templates, Yew Trunk scaffold),
   and no deprecated APIs or version numbers that could go stale are cited. Passes.

The document is well-structured, complete in its register (REQ-DX-001 through REQ-DX-010), and
grounds every requirement in a user need tied to the scope document's personas. The three gaps are
all minor testability refinements — none blocks the design's validity. No accuracy or coherence
issues were found.
