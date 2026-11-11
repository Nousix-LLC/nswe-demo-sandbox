# SUBTASK_release_bar — Ferric 1.0 Release Bar subtree hub

## Project Context

**Status**: Active

### Objective

Produce `release-bar.md` — the Ferric 1.0 release bar: a concrete, testable statement of what "a real
1.0 framework" means for Ferric. The document owns the `BAR-FERRIC-*` register and is structured in
three parts: (1) a gap review over the surfaces a Rust/WASM UI framework is expected to have; (2) the
`BAR-FERRIC-*` criteria, each with a statement, `REQ-*` references, a `verification_method`, and a
`stage`; (3) the MVP-vs-1.0 staging principle and a coverage map (`REQ-*` → `BAR-FERRIC-*`).

### Scope

**In Scope:**
- Sweeping all framework surfaces listed in the brief (reactivity, rendering, SSR/hydration, authoring
  ergonomics, async/data, routing, HTTP, docs/DX, release/semver, performance, accessibility-of-output,
  testing story, MSRV) and any surfaces the spoke designs surface that the list doesn't name
- Writing every `BAR-FERRIC-*` criterion against the `REQ-*` registers from all eight spoke designs
- Assigning `usable_early | one_oh` stages to every criterion
- Recording out-of-1.0 items (scoped CSS/styling, devtools, hot reload, desktop/mobile) in the gap
  review with no BAR criterion enforcing them (identity I5)
- Verifying identities I2–I5 from the parent contract at synthesis

**Out of Scope:**
- Authoring or modifying any `REQ-*` (those belong to the spoke owners)
- Implementation choices (how Ferric meets any criterion)

### Success Criteria

- [ ] `gap-analysis.md` covers every expected surface; status for each is checkable against the design docs
- [ ] `bar-criteria.md` has a `BAR-FERRIC-*` criterion for every covered surface; every criterion
      references ≥1 real `REQ-*` id (identity I2)
- [ ] `release-bar.md` is assembled from both inputs, follows the repo's release-bar.md shape, and
      passes the avoid-ai-writing pass
- [ ] Identities I2, I3, I4, I5 verified clean at synthesis

---

## Input Specifications

| Source | Location | Purpose |
|--------|----------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared constraints, identity table, scope |
| Parent contracts | `../../contracts/id_and_traceability_schema.yaml`, `../../contracts/design_artifact_map.yaml` | `BAR-FERRIC-*` schema, verification vocabulary, stage vocabulary |
| Scope + requirements | `../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | `REQ-FW-*` register; master in/out-of-1.0 list |
| SSR/hydration design | `../../SUBTASK_ssr_hydration/ssr-hydration.md` | `REQ-SSR-*` register |
| Authoring model design | `../../SUBTASK_authoring_model/authoring-model.md` | `REQ-API-*` register |
| Async/forms/events | `../../SUBTASK_async_forms_events/async-forms-events.md` | `REQ-ASYNC-*` register |
| Router + HTTP design | `../../SUBTASK_router_and_http/router-and-http.md` | `REQ-RT-*`, `REQ-HTTP-*` registers |
| Docs + DX design | `../../SUBTASK_docs_and_dx/docs-and-dx.md` | `REQ-DX-*` register |
| Release + distribution | `../../SUBTASK_release_and_distribution/release-and-distribution.md` | `REQ-REL-*` register |
| Performance + benchmark | `../../SUBTASK_performance_and_benchmark/performance-and-benchmark.md` | `REQ-PERF-*` register |
| This subtree's contract | `contracts/` (read-only) | gap-analysis.md and bar-criteria.md format specs |

---

## Task Structure

### Overview

```
_GLOBAL.md (this hub)
├── contracts/
│   └── _MANIFEST.yaml
├── SUBTASK_rbar_gap_review/
│   └── _BRIEF.md
├── SUBTASK_rbar_criteria/       ← _BRIEF.md authored but NOT added to DAG (see note below)
│   └── _BRIEF.md
└── SUBTASK_rbar_synthesis/
    └── _BRIEF.md
```

### DAG Note

The three-child chain (gap_review → criteria → synthesis) would push release_bar's effective
completion to execution group 4, while the downstream SUBTASK_release_plan lives in group 3.
The engine rejects that as a scheduling cycle. The resolution: SUBTASK_rbar_synthesis handles
all three concerns in one invocation — independent gap sweep, BAR-FERRIC-* criteria, and
assembly — depending directly on the 8 spokes (group 2). SUBTASK_rbar_gap_review runs
concurrently (also group 2) and produces `gap-analysis.md` as a supplemental artifact;
SUBTASK_rbar_synthesis reads it as an optional cross-check if it is available.
SUBTASK_rbar_criteria was briefed but not added to the DAG.

### Task Summary

| Task id | Depends on | Status | Description | Output |
|---------|------------|--------|-------------|--------|
| `SUBTASK_rbar_gap_review` | all 8 spokes | RUNNING | Sweep all expected framework surfaces; record covered/out-of-1.0/gap status for each with REQ-* references | `gap-analysis.md` (supplemental) |
| `SUBTASK_rbar_criteria` | — | NOT IN DAG | _BRIEF.md exists for reference; work absorbed by rbar_synthesis | — |
| `SUBTASK_rbar_synthesis` | all 8 spokes | PENDING | Gap sweep, BAR-FERRIC-* criteria, assembly, identities, fold parent | `release-bar.md`, `SYNTHESIS.md` |

### Dependency Graph (as registered)

```
[all 8 spokes] ──► SUBTASK_rbar_gap_review    (concurrent, group 2; supplemental output)
[all 8 spokes] ──► SUBTASK_rbar_synthesis      (concurrent, group 2; owns release-bar.md)
```

---

## Contract

**Contract location**: `contracts/` · **Contract kind**: `yaml_schema`

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| id_and_traceability_schema | `../../contracts/id_and_traceability_schema.yaml` | `BAR-FERRIC-*` id pattern, field requirements, verification_method vocabulary, stage vocabulary |
| design_artifact_map | `../../contracts/design_artifact_map.yaml` | `release-bar.md` repo target: `design/ferric/release-bar.md` |

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/_MANIFEST.yaml` | yaml_schema | Format of `gap-analysis.md` rows and `bar-criteria.md` entries |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `gap-analysis.md` | `SUBTASK_rbar_gap_review` |
| `bar-criteria.md` | `SUBTASK_rbar_criteria` |
| `release-bar.md` | `SUBTASK_rbar_synthesis` |
| `SYNTHESIS.md` | `SUBTASK_rbar_synthesis` |

### Identities (the synthesis task asserts these; no silent plugs)

- [ ] **IA** — every surface with status=covered in `gap-analysis.md` has ≥1 `BAR-FERRIC-*` in `bar-criteria.md`
- [ ] **IB** — every surface with status=out-of-1.0 in `gap-analysis.md` is enforced by no `BAR-FERRIC-*`
- [ ] **I2** — every `BAR-FERRIC-*` references ≥1 `REQ-*` id that exists in some spoke register
- [ ] **I3** — every `one_oh`-gating `REQ-*` across all spoke registers is referenced by ≥1 `BAR-FERRIC-*`
- [ ] **I4** — ≥1 `one_oh` `BAR-FERRIC-*` marks SSR+hydration as the gating must-have (`must_have: true`)
- [ ] **I5** — the named out-of-1.0 items (scoped CSS/styling, devtools, hot reload, desktop/mobile) appear
      in `gap-analysis.md` with `status=out-of-1.0` and are enforced by no `BAR-FERRIC-*`

### Derived Artifacts

None beyond the `_MANIFEST.yaml` format declarations.

---

## Output Specifications

| Deliverable | Location | Description |
|-------------|----------|-------------|
| `gap-analysis.md` | this workspace | Framework surface sweep: covered/out-of-1.0/gap per surface |
| `bar-criteria.md` | this workspace | Complete `BAR-FERRIC-*` register with coverage-map appendix |
| `release-bar.md` | this workspace root | Final assembled release bar (repo target `design/ferric/release-bar.md`) |
| `SYNTHESIS.md` | this workspace root | Fold record; consumed by `engine_resume_suspended` |
