# Task: Durable-persistence requirement & where state lives, as REQ-DOM-*

## Task Specification
**Slug**: SUBTASK_persistence_state
**Task Kind**: standard
**Status**: Pending

### Objective
State the **durable-persistence requirement** for chirp as requirements: what must survive a process restart,
where the product's state lives, and the durability/backup posture the release bar depends on — holding the *how*
(which database, migration mechanics) for a later `software` code DAG. The current `chirp-server` keeps its data
in an in-memory repository that does not survive a restart; this is a **release blocker**, not a baseline.

### Context
Part of `SUBTASK_domain_app_design` (see `../_GLOBAL.md`, `../contracts/`). You own the `persistence_requirement`
section of `design/domain-application-design.md` and the `REQ-DOM-100..149` range.
**Dependencies**: `SUBTASK_domain_model` (reference its entities by name when saying what must persist).
**Dependents**: `SUBTASK_synthesis` consolidates your `REQ-DOM-*`; `design-chirp-r1`'s
`SUBTASK_operational_readiness` consumes this persistence model, and `SUBTASK_release_bar` turns your
release-gating requirements into a `BAR-*`.

### What to decide
State *what durability the bar requires*, from the operator's and user's side: the concrete set of entities and
state (drawn from the domain model's vocabulary — accounts, posts, the social graph, engagement, and any
session/identity state the product needs) that MUST survive a restart; where state lives (a durable store
distinct from the serving process); and the backup/recovery and data-integrity properties the release depends on,
each expressed so an **operational check** can verify it (for example, data present and correct after a pod
restart). Translate every engineering how (DB engine, schema migration, connection pooling) into a design
requirement and defer the how by prose to the `software` domain.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context/constraints |
| Subtree contract | `../contracts/` (read-only) | Your `REQ-DOM-*` range, section ownership, the entity-vocabulary seam to read from |
| Inherited contract | `../../contracts/` (read-only) | `REQ-<AREA>-NNN` scheme + verification-method vocabulary; do not redefine |
| Domain model | `../SUBTASK_domain_model/outputs/domain-model.md` | The entity vocabulary; say what must persist by those names |
| Product requirements | `../../SUBTASK_product_requirements/outputs/product-requirements.md` | Trace durability `REQ-DOM-*` to `REQ-PROD-*` where applicable |
| Repository | `Nousix-LLC/nswe-demo` @ `c805525` | The current in-memory `chirp-server` repo (the blocker) and `deploy/` context |

## Methodology
Bundle IDs (Domain Mapping): **Release Definition** (what the durability bar requires) and **Product Strategy**
(why it matters to the product). The `design` domain loader is the Phase-B boot file. State requirements; defer
the how to the `software` domain by prose.

## Output
- `SUBTASK_persistence_state/outputs/persistence-state.md`: the `persistence_requirement` section content —
  a named, testable list of what must survive a restart, where state lives, and the backup/recovery posture — as
  `REQ-DOM-100..149`, each with a statement, testable acceptance criteria (prefer an operational check for
  durability), a `release_gating` flag, and `REQ-PROD-*` traces where applicable. Repository-ready content.

## Success criteria
- [ ] Composes against `../contracts/` and `../../contracts/`; `REQ-DOM-*` used within `100..149`; references only
      entities the domain model names.
- [ ] A clear durable-persistence requirement with a testable bar input: a concrete list of what must survive a
      restart, verifiable by an operational check; the in-memory store named as the blocker it closes.
- [ ] Where state lives and the backup/recovery posture stated as requirements; every engineering how deferred by
      prose.
- [ ] Every `REQ-DOM-*` has a statement, testable acceptance criteria, and a `release_gating` flag.

## Constraints
- Requirements/structure only — no DB choice, no migration mechanics, no product code.
- Repository-ready hygiene: no host/system/taskflow detail, no attribution trailers.
