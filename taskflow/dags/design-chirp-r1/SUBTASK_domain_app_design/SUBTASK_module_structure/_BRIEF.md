# Task: Modules, responsibilities, interfaces & entry points, as REQ-DOM-*

## Task Specification
**Slug**: SUBTASK_module_structure
**Task Kind**: standard
**Status**: Pending

### Objective
State how the product's parts divide and how they meet — module responsibilities, the interfaces/seams between
them, and the product's entry points — **as requirements and structure**, held to the existing crates (`ferric`,
`chirp-types`, `chirp-server`, `chirp-frontend`), concrete enough to build against. What each part is responsible
for and the contracts between them, not how any part is implemented.

### Context
Part of `SUBTASK_domain_app_design` (see `../_GLOBAL.md`, `../contracts/`). You own the
`modules_and_responsibilities` and `interfaces_and_entry_points` sections of `design/domain-application-design.md`
and the `REQ-DOM-200..249` range.
**Dependencies**: `SUBTASK_domain_model` (assign responsibilities over its entities by name). **Dependents**:
`SUBTASK_synthesis` consolidates your `REQ-DOM-*`.

### Distinct facets in this task
Evaluate your own scope against these and decompose if warranted:
- **Modules & responsibilities** — how the product divides across `ferric` (frontend framework), `chirp-types`
  (shared types), `chirp-server` (axum REST API + the repository + serving the SPA), and `chirp-frontend` (the
  SPA): what each is responsible for, held to the existing crate boundaries.
- **Interfaces & entry points** — the seams between the parts (the REST API surface as a contract, the shared
  types boundary, how the SPA is served, health/readiness endpoints) and the product's entry points, as
  requirements rather than implementations.

### What to decide
State the responsibility of each part and the contract at each seam from the outside: what the REST API must
offer the SPA (as a surface, not route-by-route code), what `chirp-types` must carry so server and frontend
agree, how the frontend is delivered, and the entry points a user or operator reaches (the app URL, the health
endpoint). Keep the division consistent with the entities the domain model defines and reference them by name.
Where an engineering how is implied (framework internals, serialization choices), state the requirement and defer
the how to the `software` domain by prose.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context/constraints |
| Subtree contract | `../contracts/` (read-only) | Your `REQ-DOM-*` range, section ownership, the entity-vocabulary seam to read from |
| Inherited contract | `../../contracts/` (read-only) | `REQ-<AREA>-NNN` scheme + per-requirement fields; do not redefine |
| Domain model | `../SUBTASK_domain_model/outputs/domain-model.md` | The entity vocabulary; assign responsibilities over those entities |
| Product requirements | `../../SUBTASK_product_requirements/outputs/product-requirements.md` | Trace `REQ-DOM-*` to `REQ-PROD-*` where applicable |
| Repository | `Nousix-LLC/nswe-demo` @ `c805525` | The four crates and their current boundaries to hold the structure to |

## Methodology
Bundle IDs (Domain Mapping): **Product Strategy** (how the product's parts serve the product) and **Release
Definition** (mark `release_gating`). The `design` domain loader is the Phase-B boot file. State requirements;
defer every how to the `software` domain by prose.

## Output
- `SUBTASK_module_structure/outputs/module-structure.md`: the `modules_and_responsibilities` and
  `interfaces_and_entry_points` section content, as `REQ-DOM-200..249`, each with a statement, testable
  acceptance criteria, a `release_gating` flag, and `REQ-PROD-*` traces where applicable. Repository-ready
  content.

## Success criteria
- [ ] Composes against `../contracts/` and `../../contracts/`; `REQ-DOM-*` used within `200..249`; references only
      entities the domain model names.
- [ ] Module responsibilities, interfaces/seams, and entry points stated as requirements, concrete enough to
      build against and consistent with the four existing crates.
- [ ] Every `REQ-DOM-*` has a statement, testable acceptance criteria, and a `release_gating` flag; the
      engineering how is deferred by prose.

## Constraints
- Requirements/structure only — no product code, no route-by-route implementation, no framework internals.
- Repository-ready hygiene: no host/system/taskflow detail, no attribution trailers.
