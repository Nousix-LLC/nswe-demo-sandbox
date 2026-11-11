# Task: Users, personas & end-to-end journeys for chirp

## Task Specification

**Slug**: SUBTASK_users_and_journeys
**Task Kind**: standard
**Status**: Pending

### Objective

Characterize **who chirp serves** and walk **their end-to-end journeys** — from first visit to daily use to the
day they leave — so the product requirements are grounded in real people doing real things, not a feature list.

### Context

This task is part of the product-requirements subtree (see `../_GLOBAL.md`). It is one of three concern-spokes
feeding a synthesis gate, and a precursor: `SUBTASK_requirements` will formalize the journey-derived needs into
the `REQ-PROD-*` register. It owns two required sections (`users_personas`, `user_journeys`).

**Dependencies**: none.
**Dependents**: `SUBTASK_requirements`, `SUBTASK_synthesis`.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, scope, constraints |
| Parent hub | `../../_GLOBAL.md` | Engagement context and release intent |
| Subtree contract | `../contracts/` (read-only) | Your owned sections + the sole-REQ-PROD-minter rule (you do NOT mint ids) |
| Parent contract | `../../contracts/` (read-only) | Inherited id/traceability + artifact-map schema (do not redefine) |
| Repository | `Nousix-LLC/nswe-demo` @ `c805525` | The product as it exists — clone into your own workspace; you MAY exercise the live deployment read-only to ground the journeys |
| Engagement aim | `TASK.md` (repo root) | The aim to ground the personas in |

---

## Scope — the concern this task owns

- **Users & personas**: the distinct user types a Twitter-style product of this kind serves — at minimum the
  everyday reader/poster and the person operating/administering the service; include others you judge real for
  this product (e.g. a new/unregistered visitor, a self-hoster if the kind warrants it). Give each a goal and
  context, not demographics for their own sake.
- **End-to-end journeys**: walk each persona's journey through the product, **including the unglamorous ends** —
  first visit and what an unregistered visitor can see/do; sign-up, sign-in, and account recovery; the core
  loops (compose/post, read the timeline, follow/unfollow, view a profile); daily/returning use and its empty,
  error, and second-visit states; and **leaving** — account deletion and taking their data out (export). Walk
  the operator/admin journey too (how the service is kept running for users). Surface the needs each journey
  implies as prose; you MAY tag them with informal `need:` handles per
  `../contracts/section_ownership_map.yaml`.

Do **not** assign `REQ-PROD-NNN` ids — `SUBTASK_requirements` is the sole minter. Where a journey touches a
surface owned by a sibling design area (detailed screens → `REQ-UX-*`; auth internals → `REQ-ID-*`), describe
the journey and the need from the user's side and leave that area's formal requirement to it.

### Methodology

Load on demand per the `design` loader's Domain Mapping: **Product Strategy** (primary — users, personas &
journeys); **Experience Design**, **Product Surfaces**, **Identity and Trust** (supporting — so first-visit,
account-lifecycle, and leaving journeys are walked completely). Load full bundle content yourself for the work
you execute.

---

## Output Specification

- `SUBTASK_users_and_journeys/outputs/users-and-journeys.md` — repository-ready design prose carrying the
  `users_personas` and `user_journeys` section sources. No host/system/taskflow detail, no attribution trailers;
  name things by repository identity.

## Success Criteria

- [ ] The distinct user types are given as personas with goals and context.
- [ ] Journeys are walked end-to-end incl. first visit, sign-up/in/recovery, the core loops, daily use, and
      leaving (account deletion and data export), plus the operator/admin journey.
- [ ] Empty / error / second-visit states are addressed where they shape the journey.
- [ ] Journey-derived needs are prose/`need:` handles only — no `REQ-PROD-*` ids minted here.
- [ ] Composes against `../contracts/` and `../../contracts/`; redefines no schema. Repository-ready hygiene holds.

## Constraints

- Design & requirements only — defer every implementation "how" to later code DAGs.
- Treat `contracts/` (this subtree's and the parent's) as read-only.
