# Synthesis record — concern 4 (async resources, events, forms)

**Synthesized by**: `SUBTASK_afe_synthesis`
**Folds**: `SUBTASK_async_forms_events`
**Assembled artifact**: `async-forms-events.md` (parent workspace)
**Sub-contract evaluated**: `contracts/_MANIFEST.yaml`
**Date**: 2026-10-29

---

## J1–J7 verdict

### J1 — Sub-registers are disjoint

**PASS.**

- `SUBTASK_afe_async_resources`: REQ-ASYNC-001..016. All 16 ids are within the assigned range
  001..019. No id falls in the events or forms ranges.
- `SUBTASK_afe_events_payloads`: REQ-ASYNC-020..024. All 5 ids are within the assigned range
  020..039. No id overlaps with async-resources or forms.
- `SUBTASK_afe_forms_binding`: REQ-ASYNC-040..043. All 4 ids are within the assigned range
  040..059. No id overlaps with either of the other two.

Total: 25 ids across three disjoint ranges. No id minted twice; no range boundary crossed.

Unused headroom preserved: REQ-ASYNC-017..019, REQ-ASYNC-025..039, REQ-ASYNC-044..059.

---

### J2 — Covers every clause of REQ-FW-006

**PASS.**

REQ-FW-006 has three clauses:

1. **Async data with loading / empty / loaded / error states and suspense.**
   Covered by: REQ-ASYNC-001 (resource primitive), REQ-ASYNC-002 (four states), REQ-ASYNC-003
   (declarative state render), REQ-ASYNC-004 (empty as first-class), REQ-ASYNC-005 (error carries
   value), REQ-ASYNC-009 (suspense boundary), REQ-ASYNC-010 (nested suspense). The `references`
   field in each cites `REQ-FW-006`.

2. **Event handlers beyond `click` and `input`, including submit, keyboard, focus/blur, and change.**
   Covered by: REQ-ASYNC-021 (full DOM event coverage) and REQ-ASYNC-020 (payload-carrying handler
   form, without which submit/keyboard handlers are useless because they cannot read their event).
   Both cite `REQ-FW-006`.

3. **Two-way form binding so model and field stay in sync.**
   Covered by: REQ-ASYNC-040 (two-way binding affordance), REQ-ASYNC-041 (per-kind coverage),
   REQ-ASYNC-042 (validation ergonomics), REQ-ASYNC-043 (submission ergonomics). All cite
   `REQ-FW-006`.

No clause is absent from the assembled register.

---

### J3 — The event-payload handler seam is defined once and referenced read-only by forms

**PASS.**

The payload-carrying handler form is defined in REQ-ASYNC-020, owned by
`SUBTASK_afe_events_payloads`. The assembled seam for forms lists four ids the forms section
depends on from the events section (REQ-ASYNC-020, 022, 023, 024), all read-only.

Evidence from the forms fragment:

- REQ-ASYNC-040 A2: "this requirement does not define a second handler form… references
  REQ-ASYNC-020/022."
- REQ-ASYNC-043 A4: "does not define its own handler form or its own `preventDefault`… references
  REQ-ASYNC-023."
- REQ-ASYNC-040 A3: "rests on the live-read/re-bind guarantee of REQ-ASYNC-024."

The forms register (REQ-ASYNC-040..043) contains no new handler form definition, no new
`preventDefault` surface, and no new re-binding contract. Each is cited to the events id that owns
it. The seam is honored.

---

### J4 — All three fragments are additive over the frozen Ferric surface

**PASS.**

Frozen surface at `276138f`: `create_signal`, `Signal<T>` (read-write handle), `Memo<T>`,
`create_memo`, `create_effect(impl FnMut() + 'static)`, `batch`, `mount`, `VNode`, `VElement`,
`EventHandler = Rc<dyn Fn()>`, `EventKind::Click`, `EventKind::Input`.

Fragment-by-fragment additivity evidence:

**Async resources (REQ-ASYNC-015):** States explicitly: "the synchronous contract of
`create_effect(impl FnMut() + 'static)`, the `Signal`/`Memo` handle API, `create_signal` /
`create_memo` / `batch`, and the `mount` / `VNode` render path are unchanged." Acceptance criterion
A1 requires the frozen prelude items to retain their current signatures (verified by existing
reactive-core tests passing). The resource and suspense boundary are new names, not redefinitions.

**Events and payloads (REQ-ASYNC-020 A1, REQ-ASYNC-021 A3):** REQ-ASYNC-020 A1 requires "an app
written against the baseline — handlers bound with the zero-argument `.on(kind, || …)` form —
compiles and runs unchanged." REQ-ASYNC-021 A3 states "no frozen variant is removed or renamed;
the baseline `EventKind` variants and the baseline `.on` binding are unchanged." The payload form
is additive: both forms coexist on every event.

**Forms binding (REQ-ASYNC-040 A4):** States explicitly: "Binding is additive over the frozen
surfaces: an app written against the baseline signal and event APIs still compiles, and binding adds
a new affordance rather than redefining `Signal`, `EventKind`, `EventHandler`, or `VElement::on`."

No frozen item is redefined, removed, or renamed across any of the three fragments.

---

### J5 — SSR and HTTP client referenced read-only; no REQ-SSR-* or REQ-HTTP-* id minted

**PASS.**

Locations where external namespaces appear:

- REQ-ASYNC-012 (`one_oh`): "The mechanism that serializes the resolved state and carries it into
  hydration is **not defined here** — it is owned by `REQ-SSR-*` (`SUBTASK_ssr_hydration`)."
  Acceptance criterion: "cites the `REQ-SSR-*` requirement that carries it, minting no `REQ-SSR-*`
  id here (`doc_inspection`)."
- REQ-ASYNC-013 (`one_oh`): "The carriage mechanism is `REQ-SSR-*` (read-only); this requirement
  states only the resource-side obligation not to refetch." Acceptance criterion: same
  no-`REQ-SSR-*`-id-minted check.
- REQ-ASYNC-014: "The HTTP/JSON client is `REQ-HTTP-*`'s to design (`SUBTASK_router_and_http`); no
  `REQ-HTTP-*` id is minted here." Acceptance criterion: "referencing `REQ-HTTP-*` read-only
  (`doc_inspection`)."

The events and forms fragments contain no cross-namespace id references at all.

Scan of assembled `async-forms-events.md`: no id of the form `REQ-SSR-*`, `REQ-HTTP-*`, or
`REQ-API-*` is assigned or minted anywhere. All such references are read-only citations of
sibling-owned namespaces.

---

### J6 — One assembled artifact at the parent workspace

**PASS** (satisfied by this synthesis task).

`async-forms-events.md` is authored once, at `SUBTASK_async_forms_events/async-forms-events.md`
(the parent workspace). Per `../../contracts/design_artifact_map.yaml`, this corresponds to
`design/ferric/async-forms-events.md` on branch `work/design-ferric-1_0`. The three child
fragments (`async-resources.md`, `events-and-payloads.md`, `forms-binding.md`) remain in their
child workspaces; none is double-placed or duplicated in the assembled doc. The assembled doc is
the single artifact `design_artifact_map.yaml` maps this subtree to.

---

### J7 — Every requirement conforms to the parent schema

**PASS.**

Schema: `../../contracts/id_and_traceability_schema.yaml` (`requirement_fields`, `stage_values`,
`release_gating_values`, `verification_method_values`).

Required fields verified for all 25 requirements:

| Field | Verification |
|---|---|
| `id` | All 25 carry `REQ-ASYNC-NNN` in ascending order within each section. |
| `statement` | All 25 carry a behavioral statement written from the app author's side. |
| `rationale` | All 25 carry a rationale citing peers, the frozen baseline, or the user-facing gap. |
| `acceptance_criteria` | All 25 carry numbered criteria (A1+), each with a stated `verification_method`. |
| `stage` | All 25 carry `usable_early` or `one_oh`. Only REQ-ASYNC-012/013 are `one_oh` (SSR tie-in). |
| `release_gating` | All 25: `true`. |
| `references` | All 25 carry at least one reference (typically `REQ-FW-006` plus any intra-concern cross-ref). |

Verification method vocabulary (schema-valid values used across all 25):
- `automated_test` — used in most criteria (wasm-bindgen-test, trybuild, cargo test).
- `example_build` — used wherever a buildable example is the primary demonstration.
- `doc_inspection` — used for design-stated obligations, documented patterns, additive-diff checks.
- `benchmark_run` — not used (no performance-sensitive criteria in this concern).
- `publishability` — not used (this concern's criteria are functional, not publication-bar).

All three schema-valid values in use (`automated_test`, `example_build`, `doc_inspection`) appear
in the schema's `verification_method_values` set. No non-schema vocabulary is present.

---

## How the three fragments composed

**Dependency direction**: async-resources (no deps) and events-payloads (no deps) were designed in
parallel; forms-binding depends on events-payloads (for the payload seam). The synthesis node
depends on all three.

**The event-payload handler seam** is the primary composition point. The events fragment defined
the payload-carrying handler form in REQ-ASYNC-020 (definition), REQ-ASYNC-022 (reading the
payload), REQ-ASYNC-023 (default-action and propagation control), and REQ-ASYNC-024 (re-binding
guarantees). The forms fragment composed on those four ids read-only — no additional handler form,
no second `preventDefault` surface. This is the strongest piece of the composition: the two
sections share a load-bearing surface that, if defined twice, would diverge.

**Async resources and forms** share no load-bearing seam. REQ-ASYNC-001..016 and
REQ-ASYNC-040..043 are independent. An author may combine them (load data into a signal and bind
that signal to a form) but the requirements do not cross-reference because the composition is
author-level, not framework-level.

**Async resources and events** share no load-bearing seam. REQ-ASYNC-001..016 and
REQ-ASYNC-020..024 are independent. A resource's loaded data can be read in an event handler
(because both live in the reactive graph) but that is a use pattern, not a framework seam.

**SSR and HTTP seams**: REQ-ASYNC-012/013 point at `REQ-SSR-*` and REQ-ASYNC-014 points at
`REQ-HTTP-*`. Both are read-only references — the async-resources fragment states its participation
obligation and defers the mechanism. No fragment attempted to define SSR or HTTP machinery. J5
passes cleanly.

**Cross-reference resolution**: The forms seam table in the assembled doc cites REQ-ASYNC-020,
REQ-ASYNC-022, REQ-ASYNC-023, and REQ-ASYNC-024. Each of those ids is registered in the events
fragment within its assigned range (020..039). No cited id is missing, undefined, or out of range.
The cross-references resolve.

---

## Fold disposition

All J1–J7 pass. The assembled doc is complete, one continuous register from REQ-ASYNC-001 to
REQ-ASYNC-043, conforming to the parent schema, covering every REQ-FW-006 clause, additive over the
frozen surface, with SSR and HTTP cited by reference only, and the event-payload seam defined once.

The writing-voice pass was run over the assembled `async-forms-events.md` before finalizing:
modal filler ("seamless", "robust", "comprehensive") absent; no narrated candor openers;
character adjectives ("honest", "genuine") absent; no slot-fill phrases; peer comparison tables
cite verified sources where noted; contrast claims name both halves.

`SUBTASK_async_forms_events` folds to **COMPLETED**.
