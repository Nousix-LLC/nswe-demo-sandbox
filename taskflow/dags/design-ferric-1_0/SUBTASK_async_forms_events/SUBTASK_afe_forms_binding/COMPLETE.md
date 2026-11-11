# COMPLETE — SUBTASK_afe_forms_binding (Ferric 1.0, concern 4c)

## What was done

Designed Ferric's **forms** capability — two-way input binding, validation ergonomics, and submission
ergonomics — stated as testable behavior from the app author's side and registered as the `REQ-ASYNC-040..059`
fragment. Composed on top of the payload-carrying handler seam owned by the events sibling, referenced read-only.

## Output produced

- `forms-binding.md` — the forms + two-way-binding design and the `REQ-ASYNC-040..043` register (within the
  assigned `REQ-ASYNC-040..059` range).

## Requirements registered (all stage `usable_early`, `release_gating: true`)

- **REQ-ASYNC-040** — Two-way binding of a `Signal<T>` to an input so the model and field stay in sync (the
  `REQ-FW-006` forms clause made concrete). Built on the payload handler (`REQ-ASYNC-020`/`022`) for field→signal
  and the render effect for signal→field; grounded in Ferric's single `Copy` read-write signal handle.
- **REQ-ASYNC-041** — Two-way binding across the common input kinds (text/textarea, checkbox, radio group, single
  and multiple select, number) with per-kind value semantics.
- **REQ-ASYNC-042** — Validation ergonomics: per-field and per-form validity and error messages expressed over
  the bound signals with the reactive core and surfaced reactively in the view (substrate, not a bundled
  validator).
- **REQ-ASYNC-043** — Submission ergonomics: suppress the default navigation (`REQ-ASYNC-023`), read the
  submitted values from the bound signals, and gate on validity (`REQ-ASYNC-042`).

## How it composes with the parent

The fragment is one of three capability fragments of concern 4. `SUBTASK_afe_synthesis` merges it in order into
the single continuous `REQ-ASYNC` register of `../async-forms-events.md` (repo target
`design/ferric/async-forms-events.md`).

## Sub-identities honored

- **J1** — ids only within `REQ-ASYNC-040..059` (minted `040..043`); verified mechanically.
- **J2** — covers the forms clause of `REQ-FW-006` and extends it with the per-kind, validation, and submission
  surface an author needs.
- **J3** — two-way binding, value reads, submit control, and the live-read guarantee are referenced read-only at
  `REQ-ASYNC-020`/`022`/`023`/`024`; no handler form is redefined here.
- **J4** — additive over the frozen `Signal`/`create_signal`, `EventKind`, `EventHandler`, `VElement::on`,
  `dom::mount`; nothing frozen is redefined or removed.
- **J7** — conforms to `../../contracts/id_and_traceability_schema.yaml` (requirement fields, stage vocabulary,
  `verification_method` vocabulary, `release_gating`); adds no vocabulary.

## Verification performed

- Writing-voice (avoid-ai-writing) scan: no machine-writing tells found.
- Id-range scan: only `REQ-ASYNC-040..043` minted; `020..024` appear only as read-only references.
- Peer comparison: Leptos, Svelte, and Vue rows verified against current docs (cited by URL); Dioxus and Solid
  rows marked directional, not freshly re-read.
- Grounding: baseline read from source at `Nousix-LLC/nswe-demo` @ `276138f`
  (`crates/ferric/src/{signal,vdom,dom}.rs`); dependency output (`events-and-payloads.md`) read.

## Execution note

The methodology surface was not bindable in this reconstructed node (`agent_domain_unset` from the `design`
loader). Per the orchestrated-execution rule, the work proceeded on product-design and form-ergonomics judgment
and was grounded in the read baseline source, the dependency fragment, and the verified peer sources, with the
assumption recorded in the deliverable — matching how the completed events sibling recorded the same condition.
</content>
