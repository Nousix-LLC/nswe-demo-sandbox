# COMPLETE — SUBTASK_afe_events_payloads

**Task:** Full DOM event coverage + the payload-carrying handler form (Ferric 1.0, concern 4b).
**Evaluation:** Atomic (one responsibility — the author-facing event-binding surface; one output register).
**Status:** completed.

## What was produced

`events-and-payloads.md` — the event-coverage + payload-handler design and the `REQ-ASYNC-020..024` register,
within the assigned range `REQ-ASYNC-020..039`:

- **REQ-ASYNC-020** — the payload-carrying handler form (the seam J3), additive over the frozen zero-arg
  `EventHandler = Rc<dyn Fn()>`; the baseline `.on(kind, || …)` form is preserved and its preservation is a
  checkable acceptance criterion.
- **REQ-ASYNC-021** — full DOM event coverage beyond click/input (submit, keyboard, focus/blur, change, plus a
  bind-by-name escape hatch), additive over the frozen `EventKind`.
- **REQ-ASYNC-022** — reading the triggering event's data (value, key, raw `web_sys::Event`) from the payload.
- **REQ-ASYNC-023** — default-action and propagation control from a handler (the `submit`/`preventDefault` the
  forms sibling needs).
- **REQ-ASYNC-024** — re-binding across the keyed diff's `SetEvents`, stated from the author's side (listener
  stability on an unchanged bound-event set; re-bind on add/remove; read live signals inside handlers).

## How it composes with the parent

- Owns the event-payload handler seam (J3): the handler form is defined once here; `events-and-payloads.md`
  carries a "Seam for the forms sibling" table naming the exact ids `REQ-ASYNC-040..059` reference read-only.
- The fragment merges into `../async-forms-events.md` by `SUBTASK_afe_synthesis` as the middle range of the one
  continuous `REQ-ASYNC` register.

## Verification against success criteria (all met)

- [x] Event coverage beyond click/input as testable `REQ-ASYNC-*` within 020..039, additive over frozen
      `EventKind` — REQ-ASYNC-021.
- [x] Payload handler form specified once as a `REQ-ASYNC-02x`, frozen zero-arg form explicitly preserved —
      REQ-ASYNC-020 (A1).
- [x] Interaction with `SetEvents`/re-binding stated from the author's side — REQ-ASYNC-024.
- [x] At least one acceptance criterion checkable per the schema's `verification_method` vocabulary — every
      criterion tags `automated_test`/`example_build`/`doc_inspection`.
- [x] Peer approaches compared by name — Leptos, Dioxus, Yew, Sycamore, Solid (Leptos and Dioxus verified against
      current sources; the rest marked directional).

## Identities honored

J1 (ids within 020..039, monotonic), J2 (covers the event clause of `REQ-FW-006`), J3 (owns and singly-defines
the payload seam), J4 (additive over the frozen `EventKind`/`EventHandler`/`VElement::on`/`SetEvents`),
J7 (conforms to `../../contracts/id_and_traceability_schema.yaml`). Design, not framework code; `REQ-ASYNC-*`
only.

## Grounding

`Nousix-LLC/nswe-demo` @ `276138f` — `crates/ferric/src/vdom.rs` (`EventKind`, `EventHandler`, `diff_events`,
`Patch::SetEvents`) and `dom.rs` (`set_events` wrapper receiving and discarding `web_sys::Event`), read via
`gh api`. Peer behavior verified for Leptos (`event_target_value`, Forms chapter) and Dioxus (event-handler
guide, `oninput`, `dioxus_core::Event`).

## Assumption recorded

The methodology domain was unbound in this reconstructed node (`agent_domain_unset` from the `design` loader both
before and after boot-complete). Proceeded per the orchestrated-execution rule — most reasonable interpretation,
assumption documented — using product-design / event-system-design practice grounded in the read sources. Noted
in the deliverable's "Note on execution".

## Output

- `events-and-payloads.md` (this task's workspace).
