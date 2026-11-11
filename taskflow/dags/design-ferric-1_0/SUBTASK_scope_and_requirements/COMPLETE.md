# COMPLETE — SUBTASK_scope_and_requirements

**Task:** Ferric 1.0 — framework scope & 1.0 requirements (concern 1). Owns the `REQ-FW-*` register.
**Decompose evaluation:** Atomic (one responsibility: the cross-cutting requirements spine, one owned namespace,
one output file).

## What was produced

`scope-and-requirements.md` (this workspace; repo target `design/ferric/scope-and-requirements.md`) — the
foundation every other Ferric 1.0 design concern traces back to. Six required sections:

1. **Framework definition & kind** — Ferric as a client-side-first Rust/WASM UI framework (signals + keyed VDOM,
   lean deps), grounded at baseline `276138f`; what today's framework has and the three defining gaps (no SSR,
   no declarative authoring, partial composite surface); which framework kinds apply (library / source-available)
   and which do not (end-user product, SaaS, governed OSS), each with a reason.
2. **Users & what they build** — four app-author personas (evaluating author, application author, library/component
   author, build operator); the kinds of app a 1.0 must let them build; a named-peer positioning table (Leptos,
   Sycamore, Dioxus, Yew; Solid, Svelte, Vue 3) placing Ferric closest to Vue 3 and naming the two gaps — SSR and
   a declarative macro — the bar must close.
3. **Author journeys** — JA1 getting started, JA2 building a real app, JA3 SSR & hydration, JA4 shipping,
   JA5 depend & upgrade, each walked with its states and current gaps; a journey→REQ coverage table.
4. **Requirements & acceptance criteria** — the `REQ-FW-*` register, `REQ-FW-001`–`014` (1.0, release_gating true)
   with statement/rationale/testable acceptance criteria/stage/gating, each cross-cutting and delegating area
   detail read-only to the owning sibling spoke; journey→REQ and framework-kind→REQ coverage tables.
5. **The MVP-vs-1.0 line** — the `usable_early` floor (build a real client-side app) vs the `one_oh` full bar
   (SSR+hydration the gating must-have, real reference app, crates.io/semver, docs, performance), with the
   separating principle and the per-stage requirement lists.
6. **Out-of-1.0 list** — `REQ-FW-015`–`018`: scoped CSS/styling, devtools, hot reload, desktop/mobile — each a
   recorded post-1.0 deferral with a reason, `post_one_oh`, `release_gating: false`, referenced by no `BAR`.

## Contract conformance

- **I1 (disjoint registers):** wrote only `REQ-FW-*`; all references to `REQ-SSR/API/ASYNC/RT/HTTP/DX/REL/PERF-*`
  are read-only and named to their owning spoke.
- **I5 (out-of-1.0 recorded):** styling, devtools, hot reload, desktop/mobile each appear as explicit
  `post_one_oh` / `release_gating: false` items, referenced by no `BAR-FERRIC-*`.
- Schema (`../contracts/id_and_traceability_schema.yaml`): REQ id pattern `REQ-FW-<NNN>`, monotonic; every REQ
  carries the required fields; stage vocabulary (`usable_early`/`one_oh`/`post_one_oh`) and `release_gating` used
  as defined.
- Supports downstream identities the bar/plan spokes assert: I3 (one_oh-gating REQs available to be referenced by
  a BAR), I4 (SSR named as the gating must-have at `REQ-FW-004`), I7 (#5/#6 fold flagged at `REQ-FW-007`), I9
  (frozen-surface carry-forward at `REQ-FW-009`).

## Success criteria

- [x] Every `REQ-FW-*` has statement (what, not how), rationale, testable acceptance criteria, stage, and
      release_gating, conforming to the schema.
- [x] MVP-vs-1.0 line explicit and principled (what absence makes Ferric unusable for a real app vs. what a
      credible 1.0 adds); no hidden cuts.
- [x] Out-of-1.0 list names styling, devtools, hot reload, desktop/mobile, each with a reason; none enforced by a
      later bar criterion.
- [x] Peer comparisons cite frameworks by name, grounded in their documented behavior and the baseline source read.

## Constraints honored

- Wrote only the `REQ-FW-*` register; cross-references read-only.
- Design, not code — no implementation choices.
- Writing-voice rules applied; avoid-ai-writing pass run over the deliverable (removed "honest"/"genuinely"
  category-error and narrated-candor tells; re-scanned clean).

## Grounding / inputs read

Subtree hub `../_GLOBAL.md`; contract `../contracts/` (`_MANIFEST.yaml`, `id_and_traceability_schema.yaml`,
`design_artifact_map.yaml`); Ferric baseline source (`crates/ferric`, `crates/ferric-router`, `crates/ferric-http`
preludes + READMEs) at `Nousix-LLC/nswe-demo`; chirp design precedent (`design/product-requirements.md`,
`design/release-bar.md`) at commit `ab824a5` for register/bar shape; peer frameworks by name.

## Notes for downstream spokes

- The eight capability spokes specialize the cross-cutting `REQ-FW-*` into their own `REQ-<AREA>-*` registers;
  the cross-references in §4 name which area owns each mechanism.
- The release-bar spoke must reference the one_oh-gating `REQ-FW-*` (per I3) and mark SSR+hydration (`REQ-FW-004`)
  as the gating must-have (I4), and must reference none of `REQ-FW-015`–`018` (I5).
- The release-plan spoke's epics trace to these requirements; the router/HTTP epic folds board issues #5/#6
  (I7), flagged at `REQ-FW-007`.

**Output:** `scope-and-requirements.md`
