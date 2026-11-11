# Task: Product definition, users & journeys, and product requirements for chirp

## Task Specification
**Slug**: SUBTASK_product_requirements
**Task Kind**: standard
**Status**: Pending

### Objective
Define what `chirp` must be — the product and its kind, who it serves, the journeys through it, and the
testable product requirements and acceptance criteria that the rest of the design (and its release bar) trace
back to.

### Context
Part of the design-chirp-r1 product design (see `../_GLOBAL.md` and `../contracts/`). This is the foundation
task: every other concern depends on your output. You write **what the product must do, for whom, and why** —
not how it is built.
**Dependencies**: none. **Dependents**: all other design tasks trace to `REQ-PROD-*`.

## Distinct concerns in this task
Your brief spans more than one distinct concern; evaluate your own scope against them and decompose if they
warrant it:
- **Product definition & kind** — what chirp is as a releasable Twitter-style product, which product kind(s)
  apply (consumer web app / SaaS / COTS / OSS) and what each kind makes users assume without asking.
- **Users, personas & journeys** — who the users are and their end-to-end journeys: first visit, sign-up,
  sign-in, the core posting/reading/timeline/follow loops, daily use, and the day they leave (incl. account
  deletion and taking their data).
- **Requirements & acceptance criteria** — the testable `REQ-PROD-*` requirements that follow, each with
  acceptance criteria a stranger could check, and a clear in-scope/out-of-scope statement for a product of
  this kind.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, success criteria |
| Contract | `../contracts/` (read-only) | `REQ-PROD-*` id scheme; your file + required sections |
| Repo | `Nousix-LLC/nswe-demo` @ `c805525` | The product as it exists (crates, SPA, API) |
| Engagement aim | `TASK.md` (repo root) | The aim to translate into product requirements |

## Methodology
Bundle IDs to load on demand (Domain Mapping): **Product Strategy** (primary — product definition & kind,
users/personas/journeys, requirements & acceptance criteria); **Release Definition** and **Product Surfaces**
(supporting — so requirements reflect what a releasable product of this kind includes, including the recurring
account/operational surfaces). Load full bundle content yourself only for the work you execute.

## Output
- `SUBTASK_product_requirements/outputs/product-requirements.md`, carrying the required sections in
  `../contracts/design_artifact_map.yaml` for this file, with `REQ-PROD-*` ids per the schema. Write it as
  repository-ready design content (no host/system/taskflow detail).

## Success criteria
- [ ] Composes against `../contracts/` (uses `REQ-PROD-*`; does not redefine the schema).
- [ ] Product kind(s) named with what each implies for a releasable product.
- [ ] Journeys walked end-to-end incl. first visit, daily use, and leaving (deletion/data export).
- [ ] Every `REQ-PROD-*` has acceptance criteria testable by someone who never met you; release-gating flag set.
- [ ] In-scope/out-of-scope stated; any concern judged out-of-scope recorded with a reason.

## Constraints
- Design and requirements only — defer every implementation "how" to later code DAGs.
- Repository-ready hygiene: no host/system/taskflow detail, no attribution trailers, names by repo identity.
