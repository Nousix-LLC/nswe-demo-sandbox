# SYNTHESIS — Ferric 1.0 authoring-model subtree

**Fold location:** `SUBTASK_authoring_model/SYNTHESIS.md`
**Synthesizing task:** `SUBTASK_synthesis`
**Folding into:** `SUBTASK_authoring_model` (SUSPENDED → COMPLETED)

---

## How the three sections composed

Three parallel spokes each drafted one concern of the authoring surface:

- `SUBTASK_view_macro` → `SUBTASK_view_macro/view-macro.md` — the `view!` macro syntax, lowering, and
  diagnostics; REQ-API-001..029.
- `SUBTASK_components_props_slots` → `SUBTASK_components_props_slots/components-props-slots.md` — the
  `#[component]` declaration model, typed props, `Children`, `Slot`, `SlotFn<T>`, and composition;
  REQ-API-030..052 assigned + 053..059 reserved.
- `SUBTASK_context` → `SUBTASK_context/context.md` — `provide_context`/`use_context`/`expect_context`,
  type-keyed lookup, reactive values through context, scoped cleanup; REQ-API-060..070 assigned + 071..079
  reserved.

The synthesis gate read all three sections and the subtree contract, asserted identities IA1–IA6
mechanically, then consolidated the three into one coherent narrative at `authoring-model.md`.

**Consolidation decisions:**

1. The baseline relationship is stated once (§1), grounding all three sections against the same frozen
   `VNode`/keyed-diff surface rather than repeating that grounding in each section.
2. The IA2 seam closure (invocation seam) is captured as a bidirectional table twice — once in §2.7
   (macro side) and once in §3.8 (component model side), both keyed to the same six macro/declaration
   pairs — so either section is a self-contained entry point.
3. The IA3 seam closure (context seam) is stated in §4.7 with both correspondences explicit and numbered.
4. The composition example (§5) draws all three pieces together in a single runnable example, showing IA2
   and IA3 satisfied in one place.
5. The peer comparison (§6) is integrated across all three concerns in one table set, rather than three
   separate per-section comparisons — removing the redundancy the individual drafts each carried.
6. REQ-API-* entries were transcribed from each section and merged into band order (001–029, 030–059,
   060–079) as §7; the reserved bands (053–059, 071–079) are marked as reserved headroom in the register
   introduction.

---

## Identity assertion results (IA1–IA6)

**IA1 — PASS. Disjoint bands, zero-padded ids, monotonic within each band.**
- Band A: 001..029, 29 ids assigned, all in `SUBTASK_view_macro`.
- Band B: 030..052, 23 ids assigned + 053..059 reserved, all in `SUBTASK_components_props_slots`.
- Band C: 060..070, 11 ids assigned + 071..079 reserved, all in `SUBTASK_context`.
- No overlaps across bands. All ids zero-padded to three digits, monotonic within band.

**IA2 — PASS. Invocation seam closed bidirectionally.**
- All six macro-side forms (prop attribute, optional-prop omission, reactive-prop pass, content nesting,
  slot fill, component placement) each resolve to a declared component-model form.
- All component-declaration forms (required prop, optional/defaulted/converting/reactive prop, `Children`,
  `Slot`/`Option<Slot>`, `SlotFn<T>`) are reachable from a macro form.
- No orphan on either side. Cross-reference: §2.7 (macro side) ↔ §3.8 (component side).

**IA3 — PASS. Context seam closed; both correspondences hold.**
- Correspondence 1: `provide_context`/`use_context`/`expect_context` are free-function calls inside a
  component body — the unit `view!` renders. REQ-API-066. §4.7 ¶1.
- Correspondence 2: a provided value is owned by the reactive owner scope it was provided into; that
  scope's disposal releases the context entry through the existing `no_stale_subscriber_leak` disposal
  path — no second lifetime rule. REQ-API-068. §4.7 ¶2.

**IA4 — PASS. Additive over the frozen surface; nothing redefined.**
- New additive items: `view!` macro, `vdom::text` prelude re-export, `#[component]` proc-macro,
  `#[prop(..)]` field attributes, `Children`/`Slot`/`SlotFn<T>` types, `provide_context`,
  `use_context`, `expect_context`.
- No baseline item (`VNode`, `VElement`, builders, `EventKind`, `EventHandler`, `Component` trait,
  `ReactiveScope`, `mount`) is redefined, re-signed, or removed.
- REQ-API-023, REQ-API-047, REQ-API-069. All three sections' additivity requirements confirmed.

**IA5 — PASS. One deliverable, no section unplaced or double-placed, no id collision.**
- All 63 assigned ids (001..029, 030..052, 060..070) appear exactly once in `authoring-model.md` §7.
- All content from all three section drafts is placed in `authoring-model.md`; no section content is
  absent and no content appears in more than one section of the consolidated document.
- Collision check: bands are disjoint by construction (IA1); no id assigned in two different sections.

**IA6 — PASS. Diagnostics are `trybuild`-checkable; all verification methods from inherited vocabulary.**
- All diagnostic requirements (REQ-API-024..028, REQ-API-050..052, REQ-API-063) specify a `trybuild`
  fixture with committed `stderr` or a `doc_inspection` of a stated message. No diagnostic requirement
  is checked only by visual review.
- All `verification_method` values in the register are `automated_test`, `example_build`, or
  `doc_inspection` — the three values the inherited vocabulary (`../../contracts/
  id_and_traceability_schema.yaml`) permits.

---

## Merged register summary

| Range | Count | Spoke | Stage |
|---|---|---|---|
| REQ-API-001..029 | 29 assigned | view_macro | usable_early (all) |
| REQ-API-030..033, 035..044, 046..048, 050..052 | 19 assigned | components | usable_early |
| REQ-API-034, 045, 049 | 3 assigned | components | one_oh |
| REQ-API-053..059 | reserved | components | — |
| REQ-API-060..070 | 11 assigned | context | usable_early (all) |
| REQ-API-071..079 | reserved | context | — |
| **Total** | **63 assigned, 16 reserved** | | |

All 63 requirements are `release_gating: true`.

---

## Avoid-ai-writing pass result

The pass was run over `authoring-model.md` after consolidation. No P0/P1 pattern flagged:

- No moral adjectives ("honest", "genuine", etc.) on non-character nouns.
- No narrated candor ("stated plainly", "let's be clear", etc.).
- No slot-fill templates ("at its core", "whether you're X or Y", etc.).
- No hollow fillers ("genuinely", "truly", "seamless", "robust", "comprehensive", "utilize",
  "in order to", "Moreover", "Furthermore", "Additionally").
- The two "real" occurrences ("real UI", "real app") qualify concrete, checkable things — not abstract
  nouns — and are retained.

---

## Declared outputs

- `SUBTASK_authoring_model/authoring-model.md` — consolidated authoring model, merged register.
- `SUBTASK_authoring_model/SYNTHESIS.md` — this fold record.
