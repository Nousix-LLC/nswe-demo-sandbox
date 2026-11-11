# Concern Findings: Authoring Model

## concern_name

Authoring model — `view!` macro, props, children, named slots, context (`REQ-API-*`)

---

## document_validated

`design/ferric/authoring-model.md` on branch `work/design-ferric-1_0`

Compared against prior-art draft at `prior-art/authoring-model.md`.

---

## req_ids_found

**Band A — `view!` macro (29 assigned):**
REQ-API-001, REQ-API-002, REQ-API-003, REQ-API-004, REQ-API-005,
REQ-API-006, REQ-API-007, REQ-API-008, REQ-API-009, REQ-API-010,
REQ-API-011, REQ-API-012, REQ-API-013, REQ-API-014, REQ-API-015,
REQ-API-016, REQ-API-017, REQ-API-018, REQ-API-019, REQ-API-020,
REQ-API-021, REQ-API-022, REQ-API-023, REQ-API-024, REQ-API-025,
REQ-API-026, REQ-API-027, REQ-API-028, REQ-API-029

**Band B — component model (23 assigned, REQ-API-053–059 reserved):**
REQ-API-030, REQ-API-031, REQ-API-032, REQ-API-033, REQ-API-034,
REQ-API-035, REQ-API-036, REQ-API-037, REQ-API-038, REQ-API-039,
REQ-API-040, REQ-API-041, REQ-API-042, REQ-API-043, REQ-API-044,
REQ-API-045, REQ-API-046, REQ-API-047, REQ-API-048, REQ-API-049,
REQ-API-050, REQ-API-051, REQ-API-052

**Band C — context (11 assigned, REQ-API-071–079 reserved):**
REQ-API-060, REQ-API-061, REQ-API-062, REQ-API-063, REQ-API-064,
REQ-API-065, REQ-API-066, REQ-API-067, REQ-API-068, REQ-API-069,
REQ-API-070

**Total assigned: 63. Reserved headroom: REQ-API-053–059, REQ-API-071–079 (16 slots).**

Cross-area references (read-only, not owned here): REQ-FW-005, REQ-FW-006,
REQ-FW-009, REQ-FW-014, REQ-ASYNC-* (additive EventKind set, event-payload handler
form), REQ-PERF-* (coarse-grained re-render cost).

---

## status

needs-fix

---

## specific_issues

- type: completeness
  description: >
    The §2.6 diagnostics table commits to "Handler value is not a closure →
    `on:click` expects a handler closure at the value span" as a macro-generated
    compile error, but no specific REQ-API-* id covers this case. REQ-API-025 is
    scoped to "wrong-typed attribute or text value" (`Into<String>` failures);
    REQ-API-026 covers "unknown event name"; REQ-API-028 is the umbrella
    trybuild-checkable bar but does not state the specific expected diagnostic text.
    The handler-closure type check therefore falls between requirements: the table
    promises a human-readable error at the author's span, but no REQ pins what the
    message must say or that a trybuild fixture must exist for it.
  severity: minor

---

## gaps

- id: GAP-020
  description: >
    The §2.6 diagnostics table includes "Handler value is not a closure →
    `on:click` expects a handler closure at the value span" as a named expected
    diagnostic. No REQ-API-* id specifies this case's required message text or
    requires a trybuild fixture for it. REQ-API-025 covers wrong-typed attr/text
    values; REQ-API-028 says the diagnostics suite as a whole is trybuild-checkable.
    Neither pins the specific handler-closure diagnostic message. A requirement is
    needed — either added to the reserved Band A headroom or folded into REQ-API-025
    with its scope broadened to include handler values — to make this diagnostic as
    testable as the other named cases.
  severity: minor
  action_required: >
    Add a requirement (e.g. REQ-API-029b or widen REQ-API-025) stating: when the
    value on an `on:<name>=` binding is not `Fn()`, the macro emits a diagnostic at
    the value span naming the event and stating the closure expectation; a trybuild
    fixture covers this case. Alternatively, update REQ-API-025's acceptance
    criterion to enumerate "or event handler value not `Fn()`" and add a
    corresponding trybuild fixture.

---

## validation notes (non-schema)

**Prior-art reconciliation.** The branch version carries all 63 assigned REQ-API-*
requirements from the prior-art draft without change to ID, statement, acceptance
criterion, stage, or verification method. Structural differences are editorial
consolidations, not content drops:

- §3.3 merges children (prior-art §3.3) and named slots (prior-art §3.4) into one
  section; both surface areas and their requirements are present.
- Context design decisions and implementation notes (prior-art §4.5–4.6) are
  condensed into §4's narrative paragraphs; no acceptance criteria were dropped.
- Prior-art §3.8 (component invocation seam table) and §4.7 (context seam
  assertions) are consolidated into §5 ("The authoring seams") in the branch version.
  The seam table in §5 is a superset: it adds the `row={Rc::new(...)}` /
  `SlotFn<T>` row absent from the prior-art table, consistent with REQ-API-045.
- Prior-art §6 (peer comparison) renumbers to §7 in the branch version; a new §6
  summarises the additive-surface guarantee.

No prior-art open question markers were found in either document.

**`view!` macro requirements.** REQ-API-001–029 are present and testable. Each
carries an acceptance criterion with a named verification method (`automated_test`,
`example_build`, or `doc_inspection`). The trybuild umbrella (REQ-API-028) and
individual diagnostic fixtures (REQ-API-024–027) provide a checkable bar for the
macro's error-reporting surface, modulo GAP-020 above.

**Props, children, named slots requirements.** REQ-API-030–044 cover the full
declared surface: required/optional/defaulted/converting/reactive props, children
as a deferred thunk, optional children, named slots, slot multiplicity rules,
required vs optional slots, slot+children coexistence, parameterized slots (one_oh).
Each requirement has an `example_build` or `automated_test` acceptance criterion.
REQ-API-050–052 cover the diagnostic bar for component surface misuse with
trybuild-fixture acceptance criteria.

**Context and dependency injection.** Context is Ferric's DI mechanism:
`provide_context`/`use_context`/`expect_context` inject a typed value into a
component subtree without prop threading. REQ-API-060–070 cover the full surface:
provide, read, type-keyed nearest-ancestor lookup, explicit no-provider handling,
reactive value re-render, untracked lookup, seam IA3 (readable from a component
body), app-global context, scoped cleanup, additive prelude, and clone-out semantics.
All 11 requirements are `usable_early` and `release_gating: true`.

**Component type-level diagnostics.** REQ-API-050–052 commit to trybuild fixtures
for: missing/mistyped required prop, unknown prop, children on a childless
component, undeclared or double-filled slot, and missing required slot. Each case
names the component and offending prop or region.

**Requirement testability.** Every assigned requirement states what the author
writes and what must hold against a running framework, with an explicit acceptance
criterion from the vocabulary `automated_test` | `example_build` | `doc_inspection`.
No requirement is stated as an aspiration only. The `one_oh`-staged requirements
(REQ-API-034, 045, 049) are clearly labelled and do not gate `usable_early`.

**Seam closure.** The invocation seam (IA2) is closed in both directions in §5:
every macro passing form maps to a component-side declaration, and every declaration
form is reachable from the macro. The context seam (IA3) is closed in §5 and pinned
by REQ-API-066 (readable from a component body) and REQ-API-068 (bounded by owner
scope).
