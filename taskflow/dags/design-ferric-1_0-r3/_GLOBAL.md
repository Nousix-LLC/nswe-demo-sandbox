# Ferric 1.0 Design Gap Review — Subtree Hub

## Project Context

**Status**: Active  
**PR under review**: #128 (`design: Ferric 1.0 framework design`, branch `work/design-ferric-1_0`, head `bbdeb480`)  
**Directive**: Issue #114 — "Directive: design and build Ferric to a 1.0 framework, with server-side rendering"  
**Design location**: `design/ferric/` in `Nousix-LLC/nswe-demo` (14 files in PR)  
**Issues filed from design**: #129–#164 (36 items: 8 epics + 28 features, all on the board as Todo)

### What Ferric Is

Ferric is a client-side-first Rust/WebAssembly UI framework. The 1.0 milestone adds SSR + hydration as its defining new capability, plus a `view!` macro, a component model, async resources, full DOM events, docs, benchmarks, and crates.io publishing. The design in PR#128 covers all of these across 10 design documents plus a README, a contract manifest, and two traceability contract files.

### What the Review Must Deliver

1. An APPROVE or REQUEST-CHANGES verdict posted as a review comment on PR#128
2. A `SYNTHESIS.md` at this workspace root (`taskflow/dags/design-ferric-1_0-r3/SYNTHESIS.md`) with per-concern findings, verdict, and references to filed issues
3. Non-blocking findings filed as board issues, labeled and linked to PR#128

### Review Concerns (mapped to spokes)

| Concern | Spoke | Description |
|---|---|---|
| 1. Completeness vs. directive | SUBTASK_design-doc-review | Does the design cover all of #114? Any obvious gaps? |
| 2. Release bar quality | SUBTASK_design-doc-review | Is `release-bar.md` concrete and mechanically testable? |
| 3. Coherence and traceability | SUBTASK_design-doc-review | Do REQ-* IDs, artifact map, and tickets agree? |
| 4. Buildability on existing foundation | SUBTASK_foundation-buildability | Does design align with existing ferric/router/http code? |
| 5. Ticket quality and wave plan | SUBTASK_ticket-review | Are the 36 issues accurate and correctly ordered? |

### Verdict rule

- **REQUEST-CHANGES** if any BLOCKING finding exists across the three spokes.
- **APPROVE** if all findings are non-blocking (the synthesis task may still file board issues).

---

## Shared Inputs

All spokes may access the PR branch via `git show origin/work/design-ferric-1_0:<path>` from the checkout at `taskflow/dags/ferric-foundation/checkout/` (already fetched as of this node's boot). Issues are accessible via `gh issue view <n>`.

**Design document inventory** (`design/ferric/` on the PR branch):

| File | Owner register | Notes |
|---|---|---|
| `README.md` | — | Navigation index |
| `scope-and-requirements.md` | REQ-FW-* | Framework definition, users, requirements, MVP/1.0 line |
| `ssr-hydration.md` | REQ-SSR-* | SSR + hydration architecture (the must-have) |
| `authoring-model.md` | REQ-API-* | view! macro, props, children, slots, context |
| `async-forms-events.md` | REQ-ASYNC-* | Async resources, suspense, forms, events |
| `router-and-http.md` | REQ-RT-*, REQ-HTTP-* | Router + HTTP/JSON client |
| `docs-and-dx.md` | REQ-DX-* | Guide, tutorial, API docs, examples, starter template |
| `release-and-distribution.md` | REQ-REL-* | crates.io, semver, changelog, versioning |
| `performance-and-benchmark.md` | REQ-PERF-* | js-framework-benchmark, peer comparison |
| `release-bar.md` | BAR-FERRIC-* | Consolidated 1.0 release bar, checkable criteria |
| `release-plan.md` | — | 8 epics, ordering, work items, wave plan |
| `contracts/_MANIFEST.yaml` | — | Contract manifest |
| `contracts/design_artifact_map.yaml` | — | Maps REQ-* to design artifacts and issues |
| `contracts/id_and_traceability_schema.yaml` | — | ID and traceability schema |

**Existing foundation** (already landed at `main`):
- `ferric-foundation` (#4): core signals, virtual DOM, basic `view!` macro
- `ferric-router` (#5): History API router with frozen prelude
- `ferric-http` (#6): Fetch-based HTTP/JSON client with frozen prelude
- `chirp` app: functioning SPA with durable persistence (PR#113)

---

## Task Structure

| Task id | Task Kind | Depends on | Description | Output |
|---|---|---|---|---|
| `SUBTASK_design-doc-review` | standard | none | Read all 14 design files + directive #114; evaluate completeness, release bar quality, and coherence | `design-doc-findings.md` |
| `SUBTASK_foundation-buildability` | standard | none | Read design docs + existing codebase; evaluate buildability on existing foundation | `buildability-findings.md` |
| `SUBTASK_ticket-review` | standard | none | Read issues #129–#164 + design docs; evaluate ticket quality and wave plan | `ticket-findings.md` |
| `SUBTASK_synthesis` | synthesis | `SUBTASK_design-doc-review`, `SUBTASK_foundation-buildability`, `SUBTASK_ticket-review` | Compile all findings; post verdict on PR#128; file board issues; write SYNTHESIS.md | `SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_design-doc-review    ──┐
                               │
SUBTASK_foundation-buildability─┼── SUBTASK_synthesis
                               │
SUBTASK_ticket-review        ──┘
```

---

## Subtree Methodology Posture

The three analysis spokes apply:
- **Release Definition** bundle (`release-definition/`) — specifically `ReleaseDefinition_CompletenessAndGapReview_Methodology.md` for gaps, `ReleaseDefinition_ReleaseBar_Methodology.md` for bar quality
- **Product Strategy** bundle (`product-strategy/`) — `ProductStrategy_RequirementsAndAcceptanceCriteria_Methodology.md` for traceability
- **Delivery** bundle (`delivery/`) — `Delivery_DesignToBacklogPlanning_Methodology.md` for ticket quality

The synthesis task is a verification gate: it reconciles the three spoke findings, asserts the subtree identities (every finding has a severity, every BLOCKING finding has a location, verdict follows from findings), and produces the final deliverables.

---

## Contract

Contract location: `contracts/` (read-only for descendants).  
Contract kind: `yaml_schema`  
See `contracts/_MANIFEST.yaml` and `contracts/findings_schema.yaml` for the full contract.

### Structural Declarations

Each spoke MUST produce a findings file that conforms to the findings schema in `contracts/findings_schema.yaml`.

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/findings_schema.yaml` | yaml_schema | Structure every spoke's findings file must follow |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `SUBTASK_design-doc-review/design-doc-findings.md` | SUBTASK_design-doc-review |
| `SUBTASK_foundation-buildability/buildability-findings.md` | SUBTASK_foundation-buildability |
| `SUBTASK_ticket-review/ticket-findings.md` | SUBTASK_ticket-review |
| `SYNTHESIS.md` (at this workspace root) | SUBTASK_synthesis |

### Identities

- [ ] Every finding has a `severity` field that is either `BLOCKING` or `non-blocking`
- [ ] Every finding has a `location` field naming the specific document/section or issue number
- [ ] Every finding has a `recommendation` field
- [ ] Verdict is `REQUEST-CHANGES` if and only if at least one BLOCKING finding exists; otherwise `APPROVE`
- [ ] Every non-blocking finding becomes a board issue (synthesis task verifies this)
