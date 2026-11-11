# _GLOBAL.md — design-ferric-1_0 (framework design subtree hub)

## Project Context

**Status**: Active

### Objective

Settle what **Ferric** (`crates/ferric` in `Nousix-LLC/nswe-demo`) must become to be a credible **1.0**
Rust/WebAssembly UI framework — with **server-side rendering + hydration as the one must-have** — and deliver
that as (a) the design in the repository as one reviewable PR on branch `work/design-ferric-1_0`, (b) a
traceable board backlog of epics and work-items under the **Ferric epic (#1)** that folds in the existing
router (#5) and HTTP/JSON-client (#6) issues, and (c) a root `SYNTHESIS.md` that states the Ferric 1.0
release bar and indexes the filed issues by epic.

This subtree designs **what the framework must do, for whom, and why, and what "a real 1.0" looks like from a
framework user's side — not how it is built.** Its users are Rust/WASM application authors (chirp is the first
real consumer). Every topic with an engineering "how" (the hydration algorithm, the macro expansion, the
router matcher) is stated here as a **requirement or an architecture with a testable bar**; the implementation
is deferred to later code DAGs, one epic at a time. This subtree writes **design and tickets, not framework
code.**

The authoritative task spec is this directory's `_BRIEF.md` (read it). This hub carries the shared context,
the task tree, and the contract every child composes against.

### What Ferric is today (the baseline the 1.0 builds on)

A client-side Rust/WASM framework: Solid/Leptos-style fine-grained reactivity (`Signal`, `Memo`, `Effect`,
`batch`, scoped cleanup), components as `Fn() -> VNode`, a keyed virtual-DOM diff applied to the live DOM
through `web-sys`, and click/input events. Dependencies are only `wasm-bindgen`, `web-sys`, `js-sys`. The
foundation crate (#4) has landed; `crates/ferric-router` (#5) and `crates/ferric-http` (#6) already exist as
walking-skeleton composition roots with **frozen public API surfaces** (`prelude`) to be absorbed and carried
to 1.0. Closest design analog: Vue 3 (fine-grained reactivity + a VDOM); among Rust peers it sits between
Leptos/Sycamore (signals, no VDOM) and Dioxus (React-like VDOM).

### Scope

**In Scope:**
- The nine framework design concerns in `_BRIEF.md`, each carried to a **testable bar**: (1) framework scope &
  1.0 requirements; (2) SSR + hydration; (3) the authoring model (`view!` macro, props/children/slots,
  context); (4) async/forms/events; (5) router + HTTP/JSON client (absorbing #5/#6); (6) docs & DX; (7) release
  & distribution; (8) performance & honest comparison; (9) the plan — the 1.0 release bar + a traceable
  backlog.
- Reconciling the router/http designs with the **existing frozen public API surfaces** of `ferric-router` and
  `ferric-http` (additive-only; supersede/extend, never silently redefine or duplicate #5/#6).
- The design PR into `main`; the board backlog under epic #1; the root `SYNTHESIS.md`.

**Out of Scope:**
- Writing framework code or implementing any ticket (later code DAGs).
- The **chirp product design** in `design/` — that is a *consumer* of Ferric, not Ferric itself. The end-user
  concerns of an application (sign-up screens, accounts, a product threat model) do **not** apply to a library.
- **Out of the 1.0 bar** (recorded as post-1.0, not designed now): a scoped CSS/styling story, devtools, hot
  reload, and desktop/mobile targets. These are named as deliberate non-1.0 items, never as silent omissions.
- Any repo other than `Nousix-LLC/nswe-demo`.

### Success Criteria

- [ ] The **Ferric 1.0 release bar** is concrete and testable — a reviewer, code DAG, or gap review can hold
      the framework to it criterion by criterion. "It compiles / the examples run / CI is green" is NOT a bar.
- [ ] Every applicable framework concern is covered; the explicit out-of-1.0 items are recorded with their
      reason, not silently dropped.
- [ ] One design PR on `work/design-ferric-1_0` into `main` carries the requirements, the release bar, and the
      design artifacts, written for the repository's readers.
- [ ] A board backlog of epics + work-items under **#1** whose acceptance criteria **trace to the design**,
      de-duplicated against the existing board, in dependency order (one epic = one coherent capability a code
      DAG can build, review, and land as one change). Existing **#5** and **#6** are **extended/superseded**,
      not duplicated.
- [ ] Root `SYNTHESIS.md` states the Ferric 1.0 release bar and indexes the filed issues by epic (the
      overseer's observation seam).

---

## Constraints and Requirements

### Process Constraints
- **Repository scope**: `Nousix-LLC/nswe-demo` only — its code, branches, PRs, issues, labels, Project board.
  Touch nothing else.
- **Design branch**: `work/design-ferric-1_0`; open exactly **one** PR into `main`. Never force-push `main`.
- **GitHub hygiene**: everything posted to GitHub (issues, PR, comments) is written for the repository's
  readers and names only **repository identities** (`owner/repo`, issue/PR numbers, commits). **No attribution
  trailers.** Nothing on GitHub carries host, cluster, SSH, path, or any system/environment detail.

### Quality Requirements
- **What, not how.** Design docs state the user-facing requirement, the architecture, and the testable bar;
  they do not choose the internal implementation. A requirement reads as something a stranger could check.
- **Evidence over memory.** Honest peer comparisons (Leptos, Sycamore, Dioxus, Yew; Solid/Svelte/Vue for
  design precedent) cite the frameworks by name; claims of "common practice" rest on something actually read.
  Cite peers by name, never by host path.
- **Writing voice.** Plain, checkable prose. No machine-writing tells (no "honest" on things that cannot hold
  a character, no narrated candor, no unpaired contrasts, no slot-fill templates, no padded triads, no hollow
  intensifiers). Run the avoid-ai-writing pass over every narrative deliverable before finalizing.

### Methodology
- No methodology is named by the fork or the brief. Each child **selects and loads its own** methodologies for
  its concern (API/library design, isomorphic-rendering architecture, macro/DSL design, release engineering,
  benchmark methodology, docs/DX) and applies them; this hub names none.

---

## Input Specifications

| Source | Location | Purpose |
|--------|----------|---------|
| Ferric crate (baseline) | `crates/ferric/` in `Nousix-LLC/nswe-demo` @ `main` (HEAD `276138f`) | The reactive/VDOM/DOM foundation the 1.0 extends; its frozen `prelude`. |
| Router scaffold (#5) | `crates/ferric-router/` (frozen `prelude`) | Absorb/extend into the router design — do not duplicate. |
| HTTP scaffold (#6) | `crates/ferric-http/` (frozen `prelude`) | Absorb/extend into the HTTP/JSON-client design — do not duplicate. |
| Repo design precedent | `design/` (chirp release bar, `REQ-*`/`BAR-*` scheme, `contracts/`) | The repo's own way of stating a release bar + a traceable backlog. Match its shape. |
| Owner directive #114 + epic #1 | board `NSWE Delivery`, issues #1/#5/#6 and #1's children | Authoritative scope; the epic to plan under; the issues to fold. |
| Peer frameworks | Leptos, Sycamore, Dioxus, Yew (Rust); Solid, Svelte, Vue (design analog) | Reference material for honest comparison; cite by name. |

---

## Task Structure

### Overview

```
_GLOBAL.md (this hub)
├── contracts/                              (traceability + artifact map — READ-ONLY for descendants)
│   ├── _MANIFEST.yaml
│   ├── id_and_traceability_schema.yaml
│   └── design_artifact_map.yaml
├── SUBTASK_scope_and_requirements/         (concern 1 — owns REQ-FW-*)
├── SUBTASK_ssr_hydration/                  (concern 2 — owns REQ-SSR-*)
├── SUBTASK_authoring_model/                (concern 3 — owns REQ-API-*)
├── SUBTASK_async_forms_events/             (concern 4 — owns REQ-ASYNC-*)
├── SUBTASK_router_and_http/                (concern 5 — owns REQ-RT-*, REQ-HTTP-*; absorbs #5/#6)
├── SUBTASK_docs_and_dx/                    (concern 6 — owns REQ-DX-*)
├── SUBTASK_release_and_distribution/       (concern 7 — owns REQ-REL-*)
├── SUBTASK_performance_and_benchmark/      (concern 8 — owns REQ-PERF-*)
├── SUBTASK_release_bar/                    (concern 9a — owns BAR-FERRIC-*)
├── SUBTASK_release_plan/                   (concern 9b — owns the epic/work-item plan)
├── SUBTASK_design_pr/                      (delivery — assembles design/ferric/ + opens the PR)
├── SUBTASK_file_backlog/                   (delivery — files/extends board issues under #1)
└── SUBTASK_synthesis/                      (fold — root SYNTHESIS.md + resume)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_scope_and_requirements` | none | Framework scope, users & what they build, the testable 1.0 requirements and the explicit MVP-vs-1.0 line and out-of-1.0 list. Owns `REQ-FW-*`. | `scope-and-requirements.md` |
| `SUBTASK_ssr_hydration` | `SUBTASK_scope_and_requirements` | SSR (Axum integration) + hydrate-without-re-render architecture; state carry server→client; event wiring on hydrate. The one must-have. Owns `REQ-SSR-*`. | `ssr-hydration.md` |
| `SUBTASK_authoring_model` | `SUBTASK_scope_and_requirements` | A `view!`/JSX-style macro; props/children/slots/composition; context. Owns `REQ-API-*`. | `authoring-model.md` |
| `SUBTASK_async_forms_events` | `SUBTASK_scope_and_requirements` | Async resources w/ suspense loading+error states; forms with two-way binding; full DOM event coverage. Owns `REQ-ASYNC-*`. | `async-forms-events.md` |
| `SUBTASK_router_and_http` | `SUBTASK_scope_and_requirements` | Router (params, nested routes, links) + HTTP/JSON client; reconciled with the frozen `ferric-router`/`ferric-http` surfaces; absorbs #5/#6. Owns `REQ-RT-*`, `REQ-HTTP-*`. | `router-and-http.md` |
| `SUBTASK_docs_and_dx` | `SUBTASK_scope_and_requirements` | Guide, tutorial, API docs, examples, and a cargo-generate starter; the DX bar. Owns `REQ-DX-*`. | `docs-and-dx.md` |
| `SUBTASK_release_and_distribution` | `SUBTASK_scope_and_requirements` | crates.io publishing, semver, changelog, versioning/compatibility policy for the multi-crate workspace. Owns `REQ-REL-*`. | `release-and-distribution.md` |
| `SUBTASK_performance_and_benchmark` | `SUBTASK_scope_and_requirements` | A js-framework-benchmark entry (speed, memory, bundle size) + honest peer-comparison methodology. Owns `REQ-PERF-*`. | `performance-and-benchmark.md` |
| `SUBTASK_release_bar` | `SUBTASK_scope_and_requirements`, `SUBTASK_ssr_hydration`, `SUBTASK_authoring_model`, `SUBTASK_async_forms_events`, `SUBTASK_router_and_http`, `SUBTASK_docs_and_dx`, `SUBTASK_release_and_distribution`, `SUBTASK_performance_and_benchmark` | The consolidated Ferric 1.0 release bar: `BAR-FERRIC-*`, MVP-vs-1.0 staging, completeness/gap review over framework-kind surfaces. Owns `BAR-FERRIC-*`. | `release-bar.md` |
| `SUBTASK_release_plan` | `SUBTASK_scope_and_requirements`, `SUBTASK_ssr_hydration`, `SUBTASK_authoring_model`, `SUBTASK_async_forms_events`, `SUBTASK_router_and_http`, `SUBTASK_docs_and_dx`, `SUBTASK_release_and_distribution`, `SUBTASK_performance_and_benchmark`, `SUBTASK_release_bar` | Epics + work-items under #1, each a coherent landable capability, acceptance criteria tracing to REQ/BAR, dependencies + order, explicit fold of #5/#6. | `release-plan.md` |
| `SUBTASK_design_pr` | `SUBTASK_scope_and_requirements`, `SUBTASK_ssr_hydration`, `SUBTASK_authoring_model`, `SUBTASK_async_forms_events`, `SUBTASK_router_and_http`, `SUBTASK_docs_and_dx`, `SUBTASK_release_and_distribution`, `SUBTASK_performance_and_benchmark`, `SUBTASK_release_bar`, `SUBTASK_release_plan` | Assemble every design artifact into `design/ferric/` (+ index + contracts) on `work/design-ferric-1_0`, commit, open one PR into `main`. | PR record |
| `SUBTASK_file_backlog` | `SUBTASK_release_plan`, `SUBTASK_design_pr` | File/extend board issues under epic #1 from the release plan; extend/supersede #5 and #6; de-dup against the board. | filed-issues record |
| `SUBTASK_synthesis` | `SUBTASK_scope_and_requirements`, `SUBTASK_ssr_hydration`, `SUBTASK_authoring_model`, `SUBTASK_async_forms_events`, `SUBTASK_router_and_http`, `SUBTASK_docs_and_dx`, `SUBTASK_release_and_distribution`, `SUBTASK_performance_and_benchmark`, `SUBTASK_release_bar`, `SUBTASK_release_plan`, `SUBTASK_design_pr`, `SUBTASK_file_backlog` | Verify the contract identities, then author the root `SYNTHESIS.md` (release bar + issues indexed by epic) and fold the parent. | `SYNTHESIS.md` |

### Dependency Graph

```
scope_and_requirements ──┬─► ssr_hydration ───────────┐
                         ├─► authoring_model ──────────┤
                         ├─► async_forms_events ───────┤
                         ├─► router_and_http ──────────┼─► release_bar ─► release_plan ─► design_pr ─► file_backlog ─► synthesis
                         ├─► docs_and_dx ──────────────┤                                     ▲                           ▲
                         ├─► release_and_distribution ─┤      (all capability spokes + bar feed the plan; the plan + bar + all
                         └─► performance_and_benchmark ┘       capability docs feed the PR; the plan + PR feed the backlog filing)
```

---

## Contract

**REQUIRED and present.** The contract lives in `contracts/` (read-only for every descendant). It is the
co-designed structural output of this decomposition alongside the task tree. The children are parts of one
framework design and share a tight seam — a single shared **id-and-traceability scheme** (`REQ-<AREA>-*`,
`BAR-FERRIC-*`), a fixed **design-artifact layout** (`design/ferric/<file>.md`), and a fixed **epic/work-item
schema** — so the release bar, the plan, the PR, and the filed issues compose mechanically. Without it,
reconciliation would be deferred to synthesis across docs already built to divergent id schemes.

**Contract location**: `contracts/` · **Contract kind**: `yaml_schema` + `json_schema` (traceability) and a
`yaml` artifact map.

### Ownership (REQ namespace + output file per child)

| Child | Owns id namespace | Output file (repo target `design/ferric/…`) |
|---|---|---|
| `SUBTASK_scope_and_requirements` | `REQ-FW-*` | `scope-and-requirements.md` |
| `SUBTASK_ssr_hydration` | `REQ-SSR-*` | `ssr-hydration.md` |
| `SUBTASK_authoring_model` | `REQ-API-*` | `authoring-model.md` |
| `SUBTASK_async_forms_events` | `REQ-ASYNC-*` | `async-forms-events.md` |
| `SUBTASK_router_and_http` | `REQ-RT-*`, `REQ-HTTP-*` | `router-and-http.md` |
| `SUBTASK_docs_and_dx` | `REQ-DX-*` | `docs-and-dx.md` |
| `SUBTASK_release_and_distribution` | `REQ-REL-*` | `release-and-distribution.md` |
| `SUBTASK_performance_and_benchmark` | `REQ-PERF-*` | `performance-and-benchmark.md` |
| `SUBTASK_release_bar` | `BAR-FERRIC-*` | `release-bar.md` |
| `SUBTASK_release_plan` | epic/work-item plan ids | `release-plan.md` |
| `SUBTASK_design_pr` | `design/ferric/README.md` index + the PR | (assembles all of the above) |
| `SUBTASK_file_backlog` | board issue numbers | (none in repo; issues on the board) |
| `SUBTASK_synthesis` | `SYNTHESIS.md` | `SYNTHESIS.md` (at this hub root) |

Full field schemas, the verification-method and stage vocabularies, and the artifact-path map are in
`contracts/id_and_traceability_schema.yaml` and `contracts/design_artifact_map.yaml`.

### Identities (the synthesis gate asserts these; no silent plugs)

- [ ] **I1 — disjoint registers.** Each spoke writes only its own `REQ-<AREA>-*` ids; the namespaces do not
      overlap. Cross-references to another area's REQ are read-only.
- [ ] **I2 — no invented REQ.** Every `BAR-FERRIC-*` references ≥1 `REQ-*` id that exists in some spoke's
      register.
- [ ] **I3 — gating coverage.** Every `one_oh`-stage-gating `REQ-*` is referenced by ≥1 `BAR-FERRIC-*`.
- [ ] **I4 — SSR is the must-have.** ≥1 `one_oh` `BAR-FERRIC-*` marks SSR+hydration as the gating must-have
      (a server-rendered page becomes interactive by hydration with no client-side re-render).
- [ ] **I5 — out-of-1.0 is recorded.** Scoped CSS/styling, devtools, hot reload, and desktop/mobile targets
      appear as explicit non-1.0 items in scope + release bar and are referenced by **no** `BAR-FERRIC-*`.
- [ ] **I6 — plan traces.** Every epic maps to ≥1 design-doc area; every `one_oh` `BAR-FERRIC-*` is covered by
      ≥1 work-item; every work-item cites the `REQ-*`/`BAR-*` it satisfies.
- [ ] **I7 — #5/#6 folded, not duplicated.** The router/HTTP epic(s) supersede/extend board issues #5 and #6;
      the plan records the fold and `file_backlog` edits #5/#6 rather than filing duplicates.
- [ ] **I8 — artifacts placed once.** Each owned design doc lands exactly once at its mapped
      `design/ferric/<file>.md` path; none is unplaced or double-placed.
- [ ] **I9 — frozen surfaces respected.** The router/HTTP design is additive over the existing
      `ferric-router`/`ferric-http` frozen `prelude` surfaces (extend, never silently redefine).

### Derived artifacts

- `id_and_traceability_schema.yaml` is the validator shape the synthesis task runs I1–I9 against.
- `design_artifact_map.yaml` is the map the `design_pr` task consumes to place each owned doc at its repo path.
- The `release_plan` output is the source the `file_backlog` task consumes to create/extend issues.

---

## Output Specifications

| Deliverable | Location | Description |
|-------------|----------|-------------|
| Design artifacts | `design/ferric/*.md` (via the PR) | Scope+requirements, SSR/hydration, authoring model, async/forms/events, router+http, docs/DX, release/distribution, performance/benchmark, the release bar, the release plan, and an index README. |
| The design PR | `work/design-ferric-1_0` → `main` | One reviewable PR carrying the above. |
| The backlog | board, under epic #1 | Epics + work-items tracing to the design; #5/#6 folded in. |
| Root `SYNTHESIS.md` | this hub root | The Ferric 1.0 release bar + issues indexed by epic (the overseer seam). |
