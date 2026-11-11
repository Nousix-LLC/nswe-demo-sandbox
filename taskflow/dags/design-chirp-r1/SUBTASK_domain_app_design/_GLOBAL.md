# _GLOBAL.md — SUBTASK_domain_app_design (domain & application design subtree hub)

## Project Context

**Status**: Active

### Objective

Design chirp's application and domain **as the requirements and structure the product must have** — concrete
enough to build against, held to the existing crate contracts (`ferric`, `chirp-types`, `chirp-server`,
`chirp-frontend`) — not as implementation. The output is one design file,
`design/domain-application-design.md`, owning the `REQ-DOM-*` requirements, assembled from three focused parts
by a verification synthesis.

This node is `SUBTASK_domain_app_design` in `design-chirp-r1` (see `../_GLOBAL.md`, `../contracts/`). It reached
`NeedsDecompose`: its own brief enumerates four distinct concerns (domain model; modules & responsibilities;
persistence & state; interfaces & entry points) and a full `REQ-DOM-*` design with testable acceptance criteria
for a Twitter-style product exceeds one invocation. The concerns share one tight seam — a single entity
vocabulary and one `REQ-DOM-*` numbering space — frozen in `contracts/` before any child runs.

### What this subtree states, and what it defers

It states **what must be true**: the domain model (entities, relationships, invariants), the module
responsibilities and their seams held to the crates, the **durable-persistence requirement** (the current
in-memory `chirp-server` repository loses all data on restart — a release blocker), where state lives, and the
product's entry points. Every engineering *how* (which database, migration mechanics, connection handling) is
stated as a design requirement and deferred by prose to the `software` domain's later code DAGs. No product code,
no implementation runbook.

### Scope

**In Scope:**
- The domain model of a Twitter-style product, as `REQ-DOM-*` requirements with testable acceptance criteria.
- Module responsibilities and interfaces/entry points, held to the four existing crates, as requirements.
- The durable-persistence requirement with a testable bar input (what must survive a restart) and where state
  lives.
- One consolidated `design/domain-application-design.md` carrying every required section and every `REQ-DOM-*`.

**Out of Scope:**
- Writing product code or an implementation runbook; choosing a specific DB/library (state the requirement,
  defer the how).
- Any `REQ-*` area other than `DOM` (owned by sibling concern tasks in `../_GLOBAL.md`).
- The release bar itself (`BAR-*`, owned by `SUBTASK_release_bar`); this subtree marks `release_gating` on each
  `REQ-DOM-*` so the bar task can consume it.

### Success Criteria

- [ ] `design/domain-application-design.md` contains every required section in `../contracts/design_artifact_map.yaml`
      (`domain_model`, `modules_and_responsibilities`, `persistence_requirement`, `interfaces_and_entry_points`,
      `requirements_and_acceptance_criteria`).
- [ ] A clear durable-persistence requirement with a testable bar input: a named list of what must survive a
      restart, verifiable by an operational check.
- [ ] Domain model, module responsibilities, interfaces, and entry points stated as requirements, concrete
      enough to build against and consistent with the existing crates.
- [ ] Every `REQ-DOM-*` has an id, a statement from the user's/operator's side, testable acceptance criteria, and
      a `release_gating` flag; `REQ-DOM-*` trace to `REQ-PROD-*` where applicable.
- [ ] Composes against `../contracts/` and this subtree's `contracts/`; the `REQ-<AREA>-NNN` scheme is used, not
      redefined; `REQ-DOM-*` numbering does not collide across parts; one entity vocabulary throughout.

---

## Constraints and Requirements

### Process Constraints
- Requirements/structure only — no product code, no implementation runbook. Where an engineering how is tempting
  (DB choice, migration mechanics, session storage), state it as a requirement and defer the how to the
  `software` domain by prose.
- Compose against the inherited contracts (`../contracts/`) and this subtree's `contracts/`. MUST NOT redefine
  the `REQ`/`BAR` id scheme, the area→owner map, or the design-artifact file map.
- Repository-ready hygiene on anything destined for the repo (`design/domain-application-design.md` and the
  `REQ-DOM-*`): no host/system/taskflow detail, no agent/DAG/run ids, no attribution trailers. Name things by
  repository identity (`owner/repo`, repo-relative path, crate name, commit SHA).

### Input Specifications

| Source | Identity | Role |
|--------|----------|------|
| Subtree hub (this file) | `_GLOBAL.md` | Shared context for the three parts + synthesis |
| Parent hub | `../_GLOBAL.md` | design-chirp-r1 context, scope, hygiene, the whole task tree |
| Inherited contract | `../contracts/` (read-only) | `REQ-DOM-*` scheme, area→owner map, required sections for the file |
| Subtree contract | `contracts/` (read-only) | `REQ-DOM-*` number partition, entity-vocabulary seam, section ownership |
| Product requirements | `../SUBTASK_product_requirements/outputs/product-requirements.md` | What the product must do; `REQ-PROD-*` to trace `REQ-DOM-*` against |
| Repository | `Nousix-LLC/nswe-demo` @ `c805525` | The crates (`ferric`, `chirp-types`, `chirp-server` axum REST + in-memory repo, `chirp-frontend` SPA) and the current in-memory server to design against |

---

## Subtree Methodology Posture

The Phase-B application boot file is the **`design` domain loader/index**. Each child's `_BRIEF.md` names the
design bundle ID(s) its concern maps to — **Product Strategy** (product-definition framing) and **Release
Definition** (what the bar requires, including the durability requirement) — per the loader's Domain Mapping; the
executing child loads full bundle content on demand. Where an engineering how is implied, reach to the `software`
domain's engineering method by prose and defer the how; do not design code here.

**Synthesis is a verification gate, not a prose summary.** `SUBTASK_dad_synthesis` (Task Kind: `synthesis`) assembles
the three parts into the one consolidated design file, asserts this subtree's contract identities with recorded
evidence (entity-vocabulary consistency, `REQ-DOM-*` non-collision, section coverage, `release_gating` present,
`REQ-PROD-*` traces), and folds this node. A fixable gap is remediated by decomposing a remediation subtree, never
by a silent plug.

---

## Task Structure

### Overview

```
SUBTASK_domain_app_design/
├── _GLOBAL.md                          (this hub)
├── contracts/                          (READ-ONLY for descendants)
│   ├── _MANIFEST.yaml                  (kind, ownership, identities, derived artifacts)
│   └── req_dom_partition.yaml          (REQ-DOM-* number ranges + entity-vocabulary seam + section ownership)
├── SUBTASK_domain_model/_BRIEF.md
├── SUBTASK_persistence_state/_BRIEF.md
├── SUBTASK_module_structure/_BRIEF.md
├── SUBTASK_dad_synthesis/_BRIEF.md
└── outputs/domain-application-design.md  (the consolidated file — produced by SUBTASK_synthesis)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_domain_model` | none | Define the domain model of the Twitter-style product as `REQ-DOM-*`: the canonical entities, their relationships, and their invariants, held to `chirp-types`. Establishes the entity vocabulary the other parts reference. Owns the `domain_model` section + `REQ-DOM-001..049`. | `outputs/domain-model.md` |
| `SUBTASK_persistence_state` | `SUBTASK_domain_model` | State the **durable-persistence requirement** (the in-memory store is a release blocker, not a baseline): what must survive a restart, where state lives, the durability/backup posture as a requirement with the how deferred. Owns the `persistence_requirement` section + `REQ-DOM-100..149`. | `outputs/persistence-state.md` |
| `SUBTASK_module_structure` | `SUBTASK_domain_model` | State how the product's parts divide and the seams and entry points between them, as `REQ-DOM-*`, held to the `ferric`/`chirp-types`/`chirp-server`/`chirp-frontend` contracts. Owns the `modules_and_responsibilities` + `interfaces_and_entry_points` sections + `REQ-DOM-200..249`. | `outputs/module-structure.md` |
| `SUBTASK_dad_synthesis` | `SUBTASK_domain_model`, `SUBTASK_persistence_state`, `SUBTASK_module_structure` | **Verification gate + fold.** Assemble the three parts into `outputs/domain-application-design.md` with every required section and the consolidated `requirements_and_acceptance_criteria`; assert the contract identities with recorded evidence; author `SYNTHESIS.md` at this node's directory and fold this node. | `outputs/domain-application-design.md`, `SYNTHESIS.md` |

### Dependency Graph (human-readable; the table above is authoritative)

```
SUBTASK_domain_model ─┬─> SUBTASK_persistence_state ─┐
                      └─> SUBTASK_module_structure ──┴─> SUBTASK_dad_synthesis
```

---

## Contract

The two co-designed outputs of this decomposition are the task tree above and the contract in `contracts/`. The
three parts are pieces of one design document and share a real seam: one canonical entity vocabulary, one
`REQ-DOM-*` numbering space, and the required-section ownership that lets synthesis assemble them mechanically.
That seam is frozen before any child runs.

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` (extends the inherited `design-chirp-r1` contract; never overrides it)

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| `_MANIFEST.yaml` | `../contracts/_MANIFEST.yaml` | One owner per `design/*.md`; this node owns `design/domain-application-design.md` + `REQ-DOM-*`. |
| `design_artifact_map.yaml` | `../contracts/design_artifact_map.yaml` | The required sections of `domain-application-design.md`. |
| `id_and_traceability_schema.yaml` | `../contracts/id_and_traceability_schema.yaml` | `REQ-<AREA>-NNN` format; area `DOM`→this node; each `REQ-DOM-*` has id/statement/acceptance_criteria/release_gating. |

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/req_dom_partition.yaml` | `yaml_schema` | The `REQ-DOM-NNN` number range owned by each part; which required section each part owns; the entity-vocabulary seam (domain_model establishes the canonical entity names; the other parts reference only those). |

### Ownership (one producer per artifact)

| Artifact | Owning subtask |
|---|---|
| `domain_model` section + `REQ-DOM-001..049` + entity vocabulary | `SUBTASK_domain_model` |
| `persistence_requirement` section + `REQ-DOM-100..149` | `SUBTASK_persistence_state` |
| `modules_and_responsibilities` + `interfaces_and_entry_points` sections + `REQ-DOM-200..249` | `SUBTASK_module_structure` |
| `outputs/domain-application-design.md` (consolidated) + `SYNTHESIS.md` | `SUBTASK_dad_synthesis` |

### Identities (asserted by `SUBTASK_dad_synthesis` with recorded evidence; no silent plugs)
1. The consolidated file contains every required section in `../contracts/design_artifact_map.yaml`.
2. Every `REQ-DOM-*` has an id, a statement, testable acceptance_criteria, and a `release_gating` flag.
3. `REQ-DOM-*` ids are unique — no number collides across the three parts (each stays in its declared range).
4. One entity vocabulary throughout: persistence and module-structure reference only entities the domain model
   defines (no entity named in one part is absent from the model).
5. The durable-persistence requirement names a concrete, testable set of what must survive a restart.
6. Each `REQ-DOM-*` that restates or refines a product requirement traces to a `REQ-PROD-*`.
7. Nothing in the repo-destined content carries host/system/taskflow detail or an attribution trailer.

### Derived Artifacts
- `outputs/domain-application-design.md` — the consolidated design file, assembled by `SUBTASK_synthesis` from the
  three parts (by `SUBTASK_dad_synthesis`), carrying the union of all `REQ-DOM-*` in `requirements_and_acceptance_criteria`.

### Thin-Seam Note
The seam here is real but modest: a shared entity vocabulary, a partitioned `REQ-DOM-*` space, and section
ownership. Children MUST compose against `contracts/` and MUST NOT redefine the id scheme or the file map.

---

## Output Specifications

| Deliverable | Format | Location | Description |
|-------------|--------|----------|-------------|
| Domain model part | Markdown | `SUBTASK_domain_model/outputs/domain-model.md` | Entities, relationships, invariants as `REQ-DOM-001..049` + entity vocabulary |
| Persistence & state part | Markdown | `SUBTASK_persistence_state/outputs/persistence-state.md` | Durable-persistence requirement + where state lives as `REQ-DOM-100..149` |
| Module & interface part | Markdown | `SUBTASK_module_structure/outputs/module-structure.md` | Module responsibilities, interfaces, entry points as `REQ-DOM-200..249` |
| Consolidated design | Markdown | `outputs/domain-application-design.md` | Repository-ready; all required sections + all `REQ-DOM-*` |
| Fold record | Markdown | `SYNTHESIS.md` | Verification evidence + fold of this node |
