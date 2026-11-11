# Task: Product definition & kind for chirp

## Task Specification

**Slug**: SUBTASK_product_definition
**Task Kind**: standard
**Status**: Pending

### Objective

Define **what chirp is** as a releasable product and **which product kind(s)** it is — so the rest of the
product requirements stand on a clear statement of the thing being built and the expectations its kind carries.

### Context

This task is part of the product-requirements subtree (see `../_GLOBAL.md`) of the chirp product design. It is
one of three concern-spokes feeding a synthesis gate. It is a precursor: `SUBTASK_requirements` will formalize
the needs this definition implies into the `REQ-PROD-*` register.

**Dependencies**: none.
**Dependents**: `SUBTASK_requirements`, `SUBTASK_synthesis`.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, scope, constraints |
| Parent hub | `../../_GLOBAL.md` | Engagement context and release intent |
| Subtree contract | `../contracts/` (read-only) | Your owned section + the sole-REQ-PROD-minter rule (you do NOT mint ids) |
| Parent contract | `../../contracts/` (read-only) | Inherited id/traceability + artifact-map schema (do not redefine) |
| Repository | `Nousix-LLC/nswe-demo` @ `c805525` | The product as it exists (crates, SPA, REST API, deploy) — clone into your own workspace to inspect |
| Engagement aim | `TASK.md` (repo root) | The aim to ground the definition in |

---

## Scope — the concern this task owns

- **What chirp is**: a plain statement of the product — a Twitter-style microblogging product (post short
  messages, read a timeline, follow others) built on a Rust/WebAssembly web-application framework — grounded in
  what the repository actually is at `c805525`, described from the user's side (what it is *for*), not the code's.
- **Product kind(s)**: which of consumer web app / multi-tenant SaaS / commercial off-the-shelf (COTS) /
  open-source project apply to chirp, and **what each applicable kind makes its users assume without asking**
  (e.g. an OSS user assumes they can self-host and read how; a consumer web user assumes they can sign up, trust
  it with their data, and leave with it). Name the kind(s) concretely for *this* product, not generically.
- **A product-kind-lens scope draft**: an initial in/out-of-scope view implied by the kind(s) — what a releasable
  product of this kind is expected to include and what it may reasonably leave out — for `SUBTASK_requirements`
  to consolidate into the final `in_scope_out_of_scope` section. Record any expectation you judge out-of-scope
  with a reason.

Express needs in prose; you MAY tag them with informal `need:` handles per `../contracts/section_ownership_map.yaml`.
Do **not** assign `REQ-PROD-NNN` ids — `SUBTASK_requirements` is the sole minter.

### Methodology

Load on demand per the `design` loader's Domain Mapping: **Product Strategy** (primary — product definition &
kind); **Release Definition** and **Product Surfaces** (supporting — so the kind's implied inclusions reflect
what a releasable product of this kind carries). Load full bundle content yourself for the work you execute.

---

## Output Specification

- `SUBTASK_product_definition/outputs/product-definition.md` — repository-ready design prose carrying the
  `product_definition_and_kind` section source and the product-kind scope draft. No host/system/taskflow detail,
  no attribution trailers; name things by repository identity.

## Success Criteria

- [ ] chirp is defined from the user's side, grounded in the product as it exists at `c805525`.
- [ ] The applicable product kind(s) are named, each with what it makes users assume without asking.
- [ ] A product-kind-lens in/out-of-scope draft is provided for consolidation downstream; out-of-scope items carry reasons.
- [ ] Needs are prose/`need:` handles only — no `REQ-PROD-*` ids minted here.
- [ ] Composes against `../contracts/` and `../../contracts/`; redefines no schema. Repository-ready hygiene holds.

## Constraints

- Design & requirements only — defer every implementation "how" to later code DAGs.
- Treat `contracts/` (this subtree's and the parent's) as read-only.
