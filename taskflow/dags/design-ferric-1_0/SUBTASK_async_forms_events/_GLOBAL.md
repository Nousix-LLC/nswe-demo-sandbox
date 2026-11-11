# _GLOBAL.md — SUBTASK_async_forms_events (concern 4 subtree hub)

## Project Context

**Status**: Active

### Objective

Design concern 4 of the Ferric 1.0 framework design: the three capabilities a real app needs beyond
static rendering — **async resources with suspense-style loading/error states**, **forms with two-way
input binding**, and **full DOM event coverage** — each stated as testable behavior from the app
author's side (what they can express and what must work), registered as `REQ-ASYNC-*` requirements that
conform to the inherited contract, and assembled into the single design doc `async-forms-events.md`.

This is a design subtree: it states **what** an app author can do and the testable bar, not **how**
the framework is built. It owns the `REQ-ASYNC-*` register (parent identity I1) and writes **design and
requirements, not framework code.**

This hub decomposes concern 4 because its brief enumerates three distinct capabilities, each with its
own peer precedent and its own bar; the Scope-Based trigger fired on that enumeration. The three share
one tight seam — the event-payload handler form that both forms and events stand on — which the
sub-contract at `contracts/` freezes rather than leaving to synthesis.

The authoritative spec for this task is this directory's `_BRIEF.md` and the parent hub `../_GLOBAL.md`.

### The frame this subtree specializes

The upstream requirement this subtree makes concrete is **`REQ-FW-006` — "Async data, forms, and full
event coverage"** (owned by `SUBTASK_scope_and_requirements`, read-only here). Its acceptance criteria:
a stated example fetches data and shows distinct loading / loaded / empty / error states; a form binds
an input two-way so model and field stay in sync; event handlers beyond `click`/`input` (submit,
keyboard, focus/blur, change) can be attached and fire. Stage `usable_early`, release-gating true.
Every `REQ-ASYNC-*` this subtree registers traces back to one of those three clauses (identity J2).

### What Ferric does today (baseline `Nousix-LLC/nswe-demo` @ `276138f`, `crates/ferric`)

Grounded in the baseline source so the 1.0 line is drawn against what is real:

- **Reactivity** (`signal.rs`): `create_signal` / `create_memo` / `create_effect` / `batch`; `Signal<T>`
  and `Memo<T>` are `Copy` handles with `.get()` / `.with(|&T|)` / `.set(T)` / `.update(|&mut T|)`.
  Effects are **synchronous** `FnMut()`; there is **no async primitive** and the core depends only on
  `wasm-bindgen`, `web-sys`, `js-sys` (no `wasm-bindgen-futures`, no `serde`).
- **View tree** (`vdom.rs`): `VNode` = `Element(VElement)` | `Text`. `VElement` carries `tag`, `key`,
  `attrs`, `events: Vec<(EventKind, EventHandler)>`, `children`. `EventKind` is a **closed enum with
  only `Click` and `Input`**. `EventHandler = Rc<dyn Fn()>` — **zero-argument; a handler cannot read the
  triggering event's payload**. The keyed `diff` emits `Patch::SetEvents` only when the **set of bound
  `EventKind`s changes**. The module doc explicitly sanctions an **additive** handler enrichment "to
  carry a `web_sys::Event` when it needs the event payload."
- **Runtime** (`dom.rs`): `mount(root, Component)` wraps render in an effect; binds only `click` and
  `input` via a per-kind stash key (`__ferric_on_click` / `__ferric_on_input`); the enrichment-friendly
  wrapper already receives a `web_sys::Event` internally but discards it (`move |_event| handler()`).
- **Frozen prelude**: `create_signal`, `create_memo`, `create_effect`, `batch`, `Memo`, `Signal`,
  `mount`, `EventKind`, `VElement`, `VNode`, `Component`.

The three gaps concern 4 closes: (1) no async/suspense primitive; (2) no two-way binding — and the
zero-arg handler form means a handler literally cannot read an input's value; (3) only two event kinds,
no payload. Gaps (2) and (3) share the event-payload seam.

### Scope

**In Scope:**
- The three capabilities, each to a testable `REQ-ASYNC-*` bar: async resources + suspense states;
  forms + two-way binding; full DOM event coverage + the payload-carrying handler form.
- The **event-payload handler form** as the shared seam (owned by the events child; composed against by
  the forms child), additive over the frozen `EventHandler = Rc<dyn Fn()>`.
- Composition with reactivity (signals/effects) and, **by reference only**, with SSR resolution
  (`REQ-SSR-*`, read-only).
- Honest, named peer comparison (Leptos `Resource`/`Suspense`, Solid `createResource`/`Suspense`,
  Dioxus `use_resource`/events/forms; `bind:` precedents).
- Assembly of the three fragments into the single `async-forms-events.md`.

**Out of Scope:**
- Framework code / implementation of any requirement (later code DAGs).
- Minting any id outside `REQ-ASYNC-*` (no `REQ-SSR-*`, `REQ-API-*`, `REQ-HTTP-*`, etc. — cross-refs are
  read-only).
- The HTTP/JSON client itself (`REQ-HTTP-*`, `SUBTASK_router_and_http`) — async resources compose with a
  data source by reference, they do not define the client.
- Redefining any frozen `ferric` surface; changes are additive only.

### Success Criteria

- [ ] Async resources (loading/empty/loaded/error), two-way form binding, and full event coverage are
      each specified with testable `REQ-ASYNC-*` acceptance criteria conforming to
      `contracts/../../contracts/id_and_traceability_schema.yaml`.
- [ ] The event-payload story is stated once (how a handler receives event data when it needs it) and
      forms binding composes against it.
- [ ] Composition with reactivity and (by reference) SSR is addressed, not left as an owl.
- [ ] Peer approaches compared by name.
- [ ] Sub-identities J1–J7 hold; the three fragments assemble into one `async-forms-events.md`.

---

## Constraints and Requirements

- **What, not how.** Requirements read as something a stranger could check against the framework; no
  internal data structure or code path is mandated.
- **Additive over frozen surfaces.** Extend `EventKind`, the handler form, `mount`, and the reactive
  core; never redefine or remove a frozen item (identity J4; parent I9).
- **`REQ-ASYNC-*` only** (parent I1), each within the child's assigned NNN range (identity J1).
- **Evidence over memory.** Peer claims cite the framework by name and rest on its documented behavior.
- **Writing voice.** Plain, checkable prose. No machine-writing tells (no "honest"/"genuine" on things
  that cannot hold a character, no narrated candor, no unpaired contrasts, no slot-fill templates, no
  padded triads, no hollow intensifiers). Run the avoid-ai-writing pass over every narrative deliverable
  before finalizing.
- **Methodology.** No methodology is named by the fork or briefs; each child selects and loads its own
  (reactive/async API design, event-system design, form-ergonomics design) and applies it.

---

## Input Specifications

| Source | Location | Purpose |
|--------|----------|---------|
| This subtree hub | `_GLOBAL.md` (this file) | Shared context + the baseline facts. |
| Task brief | `_BRIEF.md` | The authoritative concern-4 spec. |
| Sub-contract | `contracts/_MANIFEST.yaml` | REQ-ASYNC sub-partition + the event-payload seam + J1–J7. |
| Parent contract | `../contracts/` | REQ-ASYNC pattern, field/stage/verification vocabularies, artifact map. |
| Parent hub | `../_GLOBAL.md` | Framework-wide context + constraints. |
| Upstream requirements | `../SUBTASK_scope_and_requirements/scope-and-requirements.md` | `REQ-FW-006` and the MVP-vs-1.0 staging to specialize. |
| Ferric baseline | `Nousix-LLC/nswe-demo` @ `276138f`, `crates/ferric/src/{signal,vdom,dom,component,lib}.rs` | The reactive core, the `EventKind`/`EventHandler` form, and the event binding to extend (read via `gh api`). |
| Peer frameworks | Leptos, Solid, Dioxus (async/forms/events); Svelte/Vue (binding analog) | Honest comparison; cite by name. |

---

## Task Structure

### Overview

```
_GLOBAL.md (this hub)
├── contracts/                          (sub-contract — READ-ONLY for the children below)
│   └── _MANIFEST.yaml                  (REQ-ASYNC sub-partition + event-payload seam + J1-J7)
├── SUBTASK_afe_async_resources/        (async resources + suspense — REQ-ASYNC-001..019)
├── SUBTASK_afe_events_payloads/        (full event coverage + payload handler form — REQ-ASYNC-020..039)
├── SUBTASK_afe_forms_binding/          (forms + two-way binding — REQ-ASYNC-040..059; depends on events)
└── SUBTASK_afe_synthesis/              (fold — assemble async-forms-events.md + SYNTHESIS.md, resume parent)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_afe_async_resources` | none | Reactive async-resource primitive with loading/empty/loaded/error states rendered declaratively; composition with reactivity and (by reference) SSR resolution. Owns `REQ-ASYNC-001..019`. | `async-resources.md` |
| `SUBTASK_afe_events_payloads` | none | Full DOM event coverage beyond click/input, and the payload-carrying handler form (additive over the frozen zero-arg `EventHandler`). Owns `REQ-ASYNC-020..039`; owns the event-payload seam. | `events-and-payloads.md` |
| `SUBTASK_afe_forms_binding` | `SUBTASK_afe_events_payloads` | Two-way binding of input state to signals, plus validation/submission ergonomics, composed on top of the payload-carrying handler form. Owns `REQ-ASYNC-040..059`. | `forms-binding.md` |
| `SUBTASK_afe_synthesis` | `SUBTASK_afe_async_resources`, `SUBTASK_afe_events_payloads`, `SUBTASK_afe_forms_binding` | Verify J1–J7, merge the three fragments into one continuous `REQ-ASYNC` register, author `async-forms-events.md` at the parent workspace, and fold this subtree's parent. | `../async-forms-events.md`, `../SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_afe_async_resources ───────────────────────┐
                                                    │
SUBTASK_afe_events_payloads ──┬─────────────────────┼─► SUBTASK_afe_synthesis
                              └─► SUBTASK_afe_forms_binding ─┘
```

---

## Contract

**REQUIRED and present** at `contracts/` (read-only for the children). It is additive over the parent
contract at `../contracts/` and fixes the one seam the three children share: a disjoint sub-partition of
the `REQ-ASYNC-<NNN>` number space (one range per capability child, identity J1) and the **event-payload
handler seam** (owned by `SUBTASK_afe_events_payloads`, composed against read-only by
`SUBTASK_afe_forms_binding`, identity J3). Sub-identities J1–J7 are evaluated by `SUBTASK_afe_synthesis`.
Full ownership, ranges, and identities are in `contracts/_MANIFEST.yaml`.

---

## Output Specifications

| Deliverable | Location | Description |
|-------------|----------|-------------|
| Async-resources fragment | `SUBTASK_afe_async_resources/async-resources.md` | REQ-ASYNC-001..019 + the suspense design. |
| Events fragment | `SUBTASK_afe_events_payloads/events-and-payloads.md` | REQ-ASYNC-020..039 + the payload handler form. |
| Forms fragment | `SUBTASK_afe_forms_binding/forms-binding.md` | REQ-ASYNC-040..059 + two-way binding. |
| Assembled design doc | `async-forms-events.md` (this workspace) | The one continuous REQ-ASYNC register; repo target `design/ferric/async-forms-events.md`. |
| Fold record | `SYNTHESIS.md` (this workspace) | J1–J7 verdict + how the three fragments composed. |
