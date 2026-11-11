# Task: Ferric 1.0 Release Bar — synthesis (complete release bar and fold parent)

## Task Specification
**Slug**: SUBTASK_rbar_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_scope_and_requirements, SUBTASK_ssr_hydration, SUBTASK_authoring_model, SUBTASK_async_forms_events, SUBTASK_router_and_http, SUBTASK_docs_and_dx, SUBTASK_release_and_distribution, SUBTASK_performance_and_benchmark
**Status**: Pending

### Objective

Read every `REQ-*` register from the eight spoke designs; perform the framework surface gap sweep;
write the `BAR-FERRIC-*` register with stages; assemble `release-bar.md`; verify the contract
identities; write `SYNTHESIS.md` at the parent workspace; and fold SUBTASK_release_bar from SUSPENDED
to COMPLETED.

### Context

This is the synthesis task for the SUBTASK_release_bar decomposition (see `../_GLOBAL.md`). It runs
concurrently with SUBTASK_rbar_gap_review (which produces a supplemental `gap-analysis.md`); it does
NOT wait for rbar_gap_review to complete. Instead, it does its own gap sweep directly from the spoke
outputs and the surface list in the brief. If `../SUBTASK_rbar_gap_review/gap-analysis.md` is readable
by the time this task runs, use it as a cross-check; if not, proceed independently.

The final `release-bar.md` this task produces is the parent's declared output; `SUBTASK_design_pr`
will place it at `design/ferric/release-bar.md`.

---

## Distinct concerns (address all three in one invocation)

1. **Framework surface gap review** — for each surface a Rust/WASM UI framework is expected to have
   (see the surface list below), determine: covered by the design (cite the `REQ-*`), placed explicitly
   out-of-1.0, or a gap. Record each surface's status and notes.

2. **BAR-FERRIC-* criteria and staging** — for every covered surface, write a `BAR-FERRIC-NNN`
   criterion: a checkable statement, `REQ-*` references, a `verification_method` from the contract
   vocabulary, and a `stage` (`usable_early` | `one_oh`). Apply the staging principle consistently.
   Mark the SSR+hydration criterion(a) `must_have: true` (identity I4). Write a coverage-map appendix
   (every `one_oh`-gating `REQ-*` → the `BAR-FERRIC-*` enforcing it).

3. **Assembly and verification** — assemble `release-bar.md` (five sections: introduction, staging
   principle, BAR-FERRIC-* table, coverage map, gap review); verify identities I2–I5 from
   `../contracts/_MANIFEST.yaml`; run the avoid-ai-writing pass; write `SYNTHESIS.md` and fold parent.

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Context, identity table, output location |
| Parent contracts | `../../contracts/id_and_traceability_schema.yaml` | `BAR-FERRIC-*` schema, verification vocabulary, stage vocabulary |
| This contract | `../contracts/_MANIFEST.yaml` | Identity assertions, format specs |
| Scope + requirements | `../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | `REQ-FW-*`; master in/out-of-1.0 list |
| SSR/hydration design | `../../SUBTASK_ssr_hydration/ssr-hydration.md` | `REQ-SSR-*` |
| Authoring model design | `../../SUBTASK_authoring_model/authoring-model.md` | `REQ-API-*` |
| Async/forms/events | `../../SUBTASK_async_forms_events/async-forms-events.md` | `REQ-ASYNC-*` |
| Router + HTTP design | `../../SUBTASK_router_and_http/router-and-http.md` | `REQ-RT-*`, `REQ-HTTP-*` |
| Docs + DX design | `../../SUBTASK_docs_and_dx/docs-and-dx.md` | `REQ-DX-*` |
| Release + distribution | `../../SUBTASK_release_and_distribution/release-and-distribution.md` | `REQ-REL-*` |
| Performance + benchmark | `../../SUBTASK_performance_and_benchmark/performance-and-benchmark.md` | `REQ-PERF-*` |
| Gap analysis (optional) | `../SUBTASK_rbar_gap_review/gap-analysis.md` | Cross-check if readable; skip if not yet present |

---

## Framework surface list for the gap sweep (minimum — extend if spoke docs surface more)

| Surface | Primary source |
|---------|----------------|
| Reactive state model (signals, memos, effects, batch) | scope doc, REQ-FW-* |
| Virtual DOM and DOM patching | scope doc |
| Server-side rendering (SSR) | REQ-SSR-* |
| Hydration (no re-render on client pick-up) | REQ-SSR-* |
| Authoring ergonomics / view macro / JSX-style DSL | REQ-API-* |
| Component model (props, children, slots) | REQ-API-* |
| Context / dependency injection | REQ-API-* |
| Async resources and suspense | REQ-ASYNC-* |
| Forms and two-way data binding | REQ-ASYNC-* |
| DOM event handling | REQ-ASYNC-* |
| Client-side routing (params, nested routes, navigation) | REQ-RT-* |
| HTTP / JSON client | REQ-HTTP-* |
| Developer documentation (guide, tutorial, API reference) | REQ-DX-* |
| DX (starter, cargo-generate, error messages) | REQ-DX-* |
| Release and publishing (crates.io, semver, changelog) | REQ-REL-* |
| Versioning / compatibility policy | REQ-REL-* |
| Performance and bundle size | REQ-PERF-* |
| Honest peer comparison methodology | REQ-PERF-* |
| Accessibility of framework output (ARIA, semantic HTML) | scope doc; check REQ-FW-* |
| Testing story (how app authors test components, routes, async) | scope doc; check REQ-FW-* |
| MSRV policy | scope doc; check REQ-REL-* or REQ-FW-* |
| Scoped CSS / styling story | explicitly out-of-1.0 |
| Browser devtools / inspector integration | explicitly out-of-1.0 |
| Hot reload / live reload | explicitly out-of-1.0 |
| Desktop / mobile targets (non-WASM) | explicitly out-of-1.0 |

---

## Declared outputs

- `../release-bar.md` — the final release bar document at the SUBTASK_release_bar workspace root
  (repo target `design/ferric/release-bar.md`)
- `../SYNTHESIS.md` — the fold record at the SUBTASK_release_bar root

### release-bar.md structure (five sections)

1. **Introduction** — what the bar is, what it is for, how to read it
2. **Staging principle** — the `usable_early` / `one_oh` cut; why SSR+hydration is the gating
   must-have at 1.0; what separates a usable-early state from a full 1.0
3. **BAR-FERRIC-* criteria** — complete list organized by capability area; `must_have` criteria
   marked; each criterion: id, statement, references, verification_method, stage
4. **Coverage map** — `REQ-*` → `BAR-FERRIC-*` table for all `one_oh`-gating requirements
5. **Completeness & gap review** — the surface table (surface | status | REQ-refs | notes);
   out-of-1.0 items explicitly named with their recorded reason; any gaps noted

### SYNTHESIS.md content

- Verification results for each identity (IA, IB, I2, I3, I4, I5): `passed` or `FAILED: <finding>`
- Summary: total `BAR-FERRIC-*` count, `usable_early` / `one_oh` split, must-have criterion IDs,
  out-of-1.0 surface count, gap count
- Declared output paths

---

## Success criteria

- [ ] All surfaces in the list (and any added) appear in the gap review section
- [ ] A `BAR-FERRIC-*` criterion exists for every covered surface
- [ ] Every criterion references ≥1 real `REQ-*` id from the named spoke output (identity I2)
- [ ] No criterion references an out-of-1.0 surface (identity IB / I5)
- [ ] ≥1 `one_oh` criterion marks SSR+hydration `must_have: true` (identity I4)
- [ ] The coverage map covers every `one_oh`-gating `REQ-*` (identity I3)
- [ ] All five sections of `release-bar.md` are present and complete
- [ ] `release-bar.md` passes the avoid-ai-writing pass (no machine-writing tells)
- [ ] `SYNTHESIS.md` is written at `../SYNTHESIS.md` (not inside this task's workspace)
- [ ] `engine_resume_suspended` is called with the SUBTASK_release_bar task ID as target

### Constraints

- Write `release-bar.md` at `../release-bar.md` (the SUBTASK_release_bar root, not this workspace)
- Write `SYNTHESIS.md` at `../SYNTHESIS.md`
- Own the `BAR-FERRIC-*` namespace; do not create or modify any `REQ-*`
- Every statement in release-bar.md is checkable — not aspirational
- Report any failed identity assertion in `SYNTHESIS.md`; do not silently adjust outputs to force a pass
- Honor the writing-voice rules for all narrative content
