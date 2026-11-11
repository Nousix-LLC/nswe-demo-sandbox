# Task: Domain & application design for chirp (as requirements and structure)

## Task Specification
**Slug**: SUBTASK_domain_app_design
**Task Kind**: standard
**Status**: Pending

### Objective
Design the application and domain **as the requirements and structure the product must have** — concrete enough
to build against, held to the existing crate contracts — not as implementation. Decide, in particular, what
**durable persistence** the release bar requires: the current `chirp-server` in-memory repository does not
survive a restart, which is a release blocker.

### Context
Part of design-chirp-r1 (see `../_GLOBAL.md`, `../contracts/`). You own `design/domain-application-design.md`
and the `REQ-DOM-*` requirements. State *what* must be true (the durability requirement, the domain model,
module responsibilities, interfaces, where state lives) and defer every *how* to later code DAGs — reaching to
the `software` domain's engineering method by prose where an architecture "how" is tempting.
**Dependencies**: `SUBTASK_product_requirements`. **Dependents**: `SUBTASK_operational_readiness` consumes your
persistence model; `SUBTASK_release_bar` consolidates your `REQ-DOM-*`.

## Distinct concerns in this task
Evaluate your own scope against these and decompose if warranted:
- **Domain model** — entities, relationships, and invariants of a Twitter-style product, as requirements.
- **Modules & responsibilities** — how the product's parts divide, held to `ferric`, `chirp-types`,
  `chirp-server`, `chirp-frontend` contracts.
- **Persistence & state** — the durable-persistence requirement (what durability the bar requires, what must
  survive a restart) and where state lives; the in-memory store is a blocker, not a baseline.
- **Interfaces & entry points** — the seams between parts and the product's entry points.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context/constraints |
| Contract | `../contracts/` (read-only) | `REQ-DOM-*` scheme; your file + required sections |
| Product requirements | `../SUBTASK_product_requirements/outputs/product-requirements.md` | What the product must do (trace `REQ-DOM-*` to `REQ-PROD-*`) |
| Repo | `Nousix-LLC/nswe-demo` @ `c805525` | The crates and current in-memory server to design against |

## Methodology
Bundle IDs (Domain Mapping): **Product Strategy** (product-definition framing) and **Release Definition**
(what the bar requires, incl. the durability requirement). Where an engineering "how" is implied (DB choice,
migration mechanics), state it as a design requirement and defer the how to the `software` domain by prose.

## Output
- `SUBTASK_domain_app_design/outputs/domain-application-design.md` with the required sections in
  `../contracts/design_artifact_map.yaml` and `REQ-DOM-*` ids. Repository-ready content.

## Success criteria
- [ ] Composes against `../contracts/`; `REQ-DOM-*` used; schema not redefined.
- [ ] A clear durable-persistence requirement with a testable bar input (what must survive a restart).
- [ ] Domain model, module responsibilities, interfaces, and entry points stated as requirements, concrete
      enough to build against and consistent with the existing crates.
- [ ] Every `REQ-DOM-*` has testable acceptance criteria and a release-gating flag; `REQ-DOM-*` trace to
      `REQ-PROD-*` where applicable.

## Constraints
- Requirements/structure only — no product code, no implementation runbook.
- Repository-ready hygiene (no host/system/taskflow detail, no attribution trailers).
