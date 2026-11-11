# Task: Domain model of chirp (entities, relationships, invariants) as REQ-DOM-*

## Task Specification
**Slug**: SUBTASK_domain_model
**Task Kind**: standard
**Status**: Pending

### Objective
Define the domain model of the Twitter-style product **as requirements and structure** — the canonical entities,
their relationships, and their invariants — concrete enough to build against and consistent with the existing
`chirp-types` crate and the current `chirp-server` domain. Establish the entity vocabulary the rest of this
subtree references.

### Context
Part of `SUBTASK_domain_app_design` (see `../_GLOBAL.md`, `../contracts/`), itself part of `design-chirp-r1`
(see `../../_GLOBAL.md`, `../../contracts/`). You own the `domain_model` section of
`design/domain-application-design.md`, the `REQ-DOM-001..049` range, and the canonical **entity vocabulary**
every sibling part reads from your output.
**Dependencies**: none (within this subtree). **Dependents**: `SUBTASK_persistence_state` and
`SUBTASK_module_structure` reference your entities by name; `SUBTASK_synthesis` consolidates your `REQ-DOM-*`.

### What to decide
State *what* must be true about the model, not *how* it is stored or served (persistence is a sibling part; code
is a later DAG). Cover the entities a Twitter-style product needs and their invariants — who/what posts, the
posting relationship, the social graph (following), engagement (likes), the timeline a reader sees, identity
handles, and replies/mentions if the product requires them — each as a requirement traceable to `REQ-PROD-*`
where it refines a product requirement. Name entities by what they are in the product and note where an existing
`chirp-types` type already carries them. Make each invariant checkable (for example, constraints on handles,
post length, or self-following) via acceptance criteria.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context/constraints |
| Subtree contract | `../contracts/` (read-only) | Your `REQ-DOM-*` range, section ownership, the entity-vocabulary seam you own |
| Inherited contract | `../../contracts/` (read-only) | `REQ-<AREA>-NNN` scheme + per-requirement fields; do not redefine |
| Product requirements | `../../SUBTASK_product_requirements/outputs/product-requirements.md` | What the product must do; trace `REQ-DOM-*` to `REQ-PROD-*` |
| Repository | `Nousix-LLC/nswe-demo` @ `c805525` | `chirp-types` shapes and the current `chirp-server` domain to hold the model to |

## Methodology
Bundle IDs (Domain Mapping): **Product Strategy** (what the product's domain must be) and **Release Definition**
(mark `release_gating` on each `REQ-DOM-*`). The `design` domain loader is the Phase-B boot file. Where an
engineering how is tempting, state it as a requirement and defer the how to the `software` domain by prose.

## Output
- `SUBTASK_domain_model/outputs/domain-model.md`: the `domain_model` section content and a clearly labelled
  **entity vocabulary** (the canonical entity names + one-line definitions), plus the `REQ-DOM-001..049`
  requirements, each with a statement, testable acceptance criteria, a `release_gating` flag, and a `REQ-PROD-*`
  trace where applicable. Repository-ready content.

## Success criteria
- [ ] Composes against `../contracts/` and `../../contracts/`; `REQ-DOM-*` used within `001..049`; id scheme not
      redefined.
- [ ] Entities, relationships, and invariants stated as requirements, concrete enough to build against and
      consistent with `chirp-types`/`chirp-server`.
- [ ] A labelled entity vocabulary the sibling parts can reference by name.
- [ ] Every `REQ-DOM-*` has a statement, testable acceptance criteria, and a `release_gating` flag; traces to
      `REQ-PROD-*` where it refines one.

## Constraints
- Requirements/structure only — no product code, no storage mechanics (persistence is a sibling part).
- Repository-ready hygiene: no host/system/taskflow detail, no attribution trailers.
