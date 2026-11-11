# Task: REQ-PROD-* requirements, acceptance criteria & scope for chirp

## Task Specification

**Slug**: SUBTASK_requirements
**Task Kind**: standard
**Status**: Pending

### Objective

Turn the product definition and the user journeys into the **testable `REQ-PROD-*` requirement register** — each
requirement checkable by a stranger against the live product, each flagged for whether the release depends on it —
and write the consolidated **in-scope / out-of-scope** statement for a releasable product of this kind.

### Context

This task is part of the product-requirements subtree (see `../_GLOBAL.md`). It is the requirements spoke: it
reads the two precursor fragments and is the **sole minter** of `REQ-PROD-*` ids. It owns the
`requirements_and_acceptance_criteria` and `in_scope_out_of_scope` sections.

**Dependencies**: `SUBTASK_product_definition`, `SUBTASK_users_and_journeys` (read their outputs).
**Dependents**: `SUBTASK_synthesis`.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, scope, constraints |
| Parent hub | `../../_GLOBAL.md` | Engagement context and release intent |
| Subtree contract | `../contracts/` (read-only) | Section ownership; the sole-REQ-PROD-minter rule; the need-handle convention |
| Parent contract | `../../contracts/id_and_traceability_schema.yaml` (read-only) | The `REQ-PROD-*` format and the `each_requirement_has` fields you MUST satisfy; do not redefine |
| Product definition | `../SUBTASK_product_definition/outputs/product-definition.md` | Product-kind needs + the kind-lens scope draft |
| Users & journeys | `../SUBTASK_users_and_journeys/outputs/users-and-journeys.md` | Journey-derived needs to formalize |
| Repository | `Nousix-LLC/nswe-demo` @ `c805525` | The product as it exists — ground acceptance criteria in what can actually be checked |

---

## Scope — the concern this task owns

- **The `REQ-PROD-*` register**: formalize every need surfaced by the two precursor fragments (and any you find
  missing) into requirements. Each requirement MUST carry exactly the inherited `each_requirement_has` fields:
  `id` (`REQ-PROD-NNN`), `statement` (what must be true from the user's/operator's side), `acceptance_criteria`
  (checkable by someone who never met you — a person can exercise the live product and get the same yes/no you
  would), and `release_gating` (true|false — does a releasable product depend on it). Keep each requirement
  "what, not how". Ensure every end-to-end journey — including first visit, daily use, and **leaving (account
  deletion and data export)** — is covered by ≥1 requirement, so the synthesis gate's journey→requirement
  identity holds.
- **Consolidated in-scope / out-of-scope**: merge the product-kind scope draft with what the requirements settle,
  into one statement of what a releasable product of this kind includes and leaves out. Every concern judged
  out-of-scope carries a reason.

Where a need belongs to a sibling design area's register (`REQ-DOM-*`, `REQ-UX-*`, `REQ-ID-*`, `REQ-OPS-*`),
state the product-level requirement from the user's side and note the area that will carry the detailed one;
do not mint another area's ids.

### Methodology

Load on demand per the `design` loader's Domain Mapping: **Product Strategy** (primary — requirements &
acceptance criteria); **Release Definition**, **Delivery** (supporting — so release-gating flags and
testability are sound). Load full bundle content yourself for the work you execute.

---

## Output Specification

- `SUBTASK_requirements/outputs/requirements.md` — repository-ready design content carrying the
  `requirements_and_acceptance_criteria` register (the `REQ-PROD-*` set) and the consolidated
  `in_scope_out_of_scope` section. No host/system/taskflow detail, no attribution trailers; repository identity
  naming.

## Success Criteria

- [ ] Every `REQ-PROD-*` has `id`, `statement`, stranger-testable `acceptance_criteria`, and a `release_gating` flag.
- [ ] Every end-to-end journey (incl. first visit, daily use, and leaving: deletion & data export) is covered by ≥1 `REQ-PROD-*`.
- [ ] The product kind's implications are each reflected in a requirement or recorded out-of-scope with a reason.
- [ ] `in_scope_out_of_scope` is stated; out-of-scope concerns carry reasons.
- [ ] Composes against the inherited schema (uses `REQ-PROD-NNN`; does not redefine fields or the id format). Hygiene holds.

## Constraints

- Design & requirements only — defer every implementation "how" to later code DAGs.
- Sole minter of `REQ-PROD-*`; mint no other area's ids. Treat all `contracts/` as read-only.
