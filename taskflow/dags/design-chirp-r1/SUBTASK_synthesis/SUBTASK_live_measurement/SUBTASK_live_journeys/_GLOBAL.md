# _GLOBAL.md — SUBTASK_live_journeys (manual_user_check measurement subtree hub)

## Project Context

**Status**: Active

### Objective

Judge **every `BAR-*` whose declared `verification_method` is `manual_user_check`** (139 criteria) against the
deployed chirp product at commit `c805525`, by exercising the product as a user who was not in the design room. Each
`BAR-*` gets exactly one `live_status` ∈ {met, partial, missing, not_applicable} and one grounded observation — what
was exercised and what was seen. The one consolidated output is `outputs/live-journeys-measurement.md`, one row per
`BAR-*`, keyed by `bar_id`, so the parent measurement fold unions it mechanically with the other three method
partitions.

This subtree is the `manual_user_check` partition of `SUBTASK_live_measurement` (see `../_GLOBAL.md` and
`../contracts/_MANIFEST.yaml`). It writes **no product code** and measures the live product **read-only**.

### Why this decomposes

The 139 `manual_user_check` criteria are not one journey. They span the product's whole user surface — genuinely
distinct journeys and surfaces a person reaches at different points, each with its own setup and its own idea of
"done." Measuring them in one invocation would exceed the atomic tool-call envelope many times over and would mix
unrelated concerns (the sign-in flow, the visual type scale, the screen-reader path). Per the kernel's decomposition
triggers the enumerated distinct concerns fire the Scope-Based trigger and the Distinct Concerns Test, so the work is
partitioned into nine coherent journey/surface clusters that different people could exercise in parallel, plus a
synthesis fold that unions them and asserts totality.

The partition key is an **explicit assignment of each `BAR-*` to exactly one cluster** (frozen in
`contracts/_MANIFEST.yaml`), not a mechanical area/number rule — because a journey cluster cuts across the release
bar's area blocks (the "get in" journey touches Product, Domain, Experience, and Identity criteria alike). The
assignment is disjoint (each of the 139 appears under exactly one child) and total (the nine clusters union to all
139), verified before any child runs.

### Scope

**In Scope:**
- Judging every `manual_user_check` `BAR-*` against the live product at `c805525` (and the repository/SPA/API source
  at `c805525` where the running product is unreachable or ambiguous), to a recorded observation, by the cluster that
  owns it.
- Unioning the nine cluster verdict tables into `outputs/live-journeys-measurement.md`, confirming totality (139
  `BAR-*`, each once) and vocabulary conformance, and folding this subtree to COMPLETED.

**Out of Scope:**
- Any `BAR-*` of another `verification_method` (owned by sibling measurement partitions `SUBTASK_automated_tests`,
  `SUBTASK_inspection_checks`, `SUBTASK_operational_checks`).
- Writing product code, editing design docs or backlog, or mutating the live product beyond the normal effect of a
  throwaway test account's own actions.
- The union across all four methods, the traceability matrix, and the root verdict (owned higher in the gate).

### Success Criteria

- [ ] Every one of the 139 `manual_user_check` `BAR-*` carries exactly one `live_status` and a grounded observation in
      `outputs/live-journeys-measurement.md`; none omitted, and no `BAR-*` of another method included.
- [ ] Each observation is grounded in an actual exercise of the live product — or an actual SPA/API source artifact at
      `c805525` where the running product was unreachable or ambiguous — never assumed or confabulated. A criterion
      that cannot be observed is judged conservatively (`missing`/`partial`) with the reason stated.
- [ ] `live_status` values are from the inherited vocab; `bar_id`s are verbatim release-bar ids.
- [ ] The nine cluster partitions are disjoint and total: each `BAR-*` appears under exactly one cluster, the union is
      all 139.
- [ ] Read-only on the live product; the output touches only `Nousix-LLC/nswe-demo` and the project's own deployment;
      no host/system/taskflow detail in the output.

---

## Constraints and Requirements

### Process Constraints
- **Read-only measurement.** Exercising the live product MUST NOT mutate it beyond the normal effect of a user's own
  actions on a throwaway test account, and MUST NOT touch any repo/cluster/namespace outside the project's own. No
  product code is written.
- **Conservative where unobservable.** Where a surface cannot be reached (the product at `c805525` uses an in-memory
  store and may omit whole release-layer surfaces — recovery, settings, contact, sessions-and-devices, export,
  deletion, reporting, operator, status), confirm its absence from the running UI and, where a code artifact can
  settle it, the SPA/API source at `c805525`, and record a grounded `missing`/`partial` with the reason — never a
  presumed verdict, never an optimistic one.
- **Each `BAR-*` once.** A criterion is measured by exactly the cluster that owns it in `contracts/_MANIFEST.yaml`.

### Hygiene (binding on the output and on anything that could reach GitHub)
The host and deployment facts needed to reach the live product (per the project `CLAUDE.md`) are for running checks
only and MUST NOT appear in any output. No host or cluster address, no SSH detail, no filesystem or taskflow path, no
agent/DAG/run id. Name things by repository identity only — `owner/repo`, commit SHA, repo-relative paths, and
`BAR-*`/`REQ-*` ids. Each output carries a short preamble recording only *that* the live product was reached (or why
it could not be), by repository/commit identity — never how.

---

## Input Specifications

Paths below are relative to each child's own workspace (`SUBTASK_live_journeys/SUBTASK_<slug>/`).

| Source | Location (from a child) | Role |
|--------|--------------------------|------|
| This subtree hub | `../_GLOBAL.md` | Shared context (this file) |
| This subtree's sub-contract | `../contracts/_MANIFEST.yaml` | The child's owned `BAR-*` cluster, the verdict-row schema, the `live_status` vocab, ownership, totality identity |
| Parent measurement hub | `../../_GLOBAL.md` | The measurement subtree context |
| Parent measurement sub-contract | `../../contracts/_MANIFEST.yaml` | `verdict_row_schema`, `live_status`/`verification_method` vocab, `live_status_key: bar_id` |
| Root id/traceability schema | `../../../../contracts/id_and_traceability_schema.yaml` | `live_status` + closed `verification_method` vocab (authoritative) |
| Release bar | `../../../../SUBTASK_release_bar/outputs/release-bar.md` | The 278 `BAR-*`; each child reads the statements of the `BAR-*` it owns |
| Design PR record | `../../../../SUBTASK_design_pr/outputs/design-pr.md` | PR #, branch, repo `design/` map, for context |
| Live deployment | ArgoCD app `chirp` @ `c805525` (reached per the project `CLAUDE.md` host notes) | Exercise the product read-only |
| Repository @ `c805525` | `../../../../SUBTASK_design_pr/repo` (or a fresh `gh repo clone Nousix-LLC/nswe-demo` checked out at `c805525`) | Confirm presence/absence of a surface in the SPA/API source where the running UI is ambiguous |

> Note the input depth: a cluster child sits one level deeper than the measurement children did, so the release bar
> and root contracts are reached with one extra `../` (`../../../../`). Each child resolves paths from its own
> workspace.

---

## Methodology Posture

The Phase-B `design` methodology loader is unavailable run-wide (`agent_domain_unset`); every gate node hit the same
and proceeded. Each child applies the **principal-product-designer persona** and the relayed **ReleaseBar** guidance:
measure the product criterion by criterion as someone who was not in the design room, exercise the journey each
`BAR-*` describes, and record what the product actually does. Children record the loader limitation and proceed; they
do not block on it.

---

## Task Structure

### Overview

```
SUBTASK_live_journeys/
├── _GLOBAL.md                              (this hub)
├── contracts/
│   └── _MANIFEST.yaml                      (sub-contract: cluster partition + per-cluster BAR-* assignment, row schema, ownership, totality — READ-ONLY)
├── outputs/                                (the fold writes outputs/live-journeys-measurement.md here)
├── SUBTASK_getin_identity/_BRIEF.md        (get-in & identity journeys: sign-up, sign-in, sign-out, session, recovery, verified contact)
├── SUBTASK_core_loop/_BRIEF.md             (core loop: account model, compose/post, reply, like, follow, timeline, profiles)
├── SUBTASK_account_lifecycle/_BRIEF.md     (account management: settings hub, edit profile, contact, export, deletion, data rights)
├── SUBTASK_resilience_states/_BRIEF.md     (empty/loading/error/not-found states, onboarding, session-expiry recovery, action feedback)
├── SUBTASK_safety_trust_support/_BRIEF.md  (reporting, rules/terms, help & support, operator surface, status/degraded notice)
├── SUBTASK_visual_craft_nav/_BRIEF.md      (navigation shell, visual craft, consistency, layout, typography, contrast, copy)
├── SUBTASK_responsive_phone/_BRIEF.md      (typical-phone / responsive experience across the core loop and surfaces)
├── SUBTASK_accessibility/_BRIEF.md         (keyboard & screen-reader path, WCAG checks)
├── SUBTASK_web_delivery_api/_BRIEF.md      (one-address web delivery, SPA routing, typed API surface as experienced, health endpoint)
└── SUBTASK_journeys_fold/_BRIEF.md         (synthesis: union the nine, assert totality 139, write outputs/live-journeys-measurement.md, fold)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_getin_identity` | none | Exercise the get-in & identity journeys (signed-out entry, sign-up, sign-in, sign-out, session lifecycle, credential recovery, verified contact) and judge the 22 `manual_user_check` `BAR-*` assigned to this cluster. | `outputs/getin-identity-measurement.md` |
| `SUBTASK_core_loop` | none | Exercise the core value loop (account model, compose & post, reply, like, follow, home timeline, public profiles, follower/following lists) and judge the 24 `BAR-*` assigned to this cluster. | `outputs/core-loop-measurement.md` |
| `SUBTASK_account_lifecycle` | none | Exercise account management & lifecycle (settings hub, edit profile, verified-contact view/change, sessions-and-devices, data export, account deletion, data-rights baseline) and judge the 20 `BAR-*` assigned to this cluster. | `outputs/account-lifecycle-measurement.md` |
| `SUBTASK_resilience_states` | none | Exercise empty / loading / failed / not-found states, onboarding, session-expiry recovery, and action feedback, and judge the 12 `BAR-*` assigned to this cluster. | `outputs/resilience-states-measurement.md` |
| `SUBTASK_safety_trust_support` | none | Exercise the safety & trust surfaces (reporting, rules/terms, help & support, operator/support surface, status/degraded notice) and judge the 8 `BAR-*` assigned to this cluster. | `outputs/safety-trust-support-measurement.md` |
| `SUBTASK_visual_craft_nav` | none | Exercise the navigation shell and the visual craft (consistency, layout, reading column, typography, contrast, layering, motion, button copy, shared component treatment) and judge the 16 `BAR-*` assigned to this cluster. | `outputs/visual-craft-nav-measurement.md` |
| `SUBTASK_responsive_phone` | none | Exercise the typical-phone / responsive experience across the core loop and surfaces and judge the 9 `BAR-*` assigned to this cluster. | `outputs/responsive-phone-measurement.md` |
| `SUBTASK_accessibility` | none | Exercise the keyboard & screen-reader path and the WCAG checks and judge the 18 `BAR-*` assigned to this cluster. | `outputs/accessibility-measurement.md` |
| `SUBTASK_web_delivery_api` | none | Exercise the web-delivery surface as a user experiences it (one web address, SPA routing, the typed API operations end to end, pagination, typed errors, the health endpoint, data presence over time) and judge the 10 `BAR-*` assigned to this cluster. | `outputs/web-delivery-api-measurement.md` |
| `SUBTASK_journeys_fold` | `SUBTASK_getin_identity`, `SUBTASK_core_loop`, `SUBTASK_account_lifecycle`, `SUBTASK_resilience_states`, `SUBTASK_safety_trust_support`, `SUBTASK_visual_craft_nav`, `SUBTASK_responsive_phone`, `SUBTASK_accessibility`, `SUBTASK_web_delivery_api` | **Synthesis.** Union the nine cluster verdict tables into the one `bar_id`-keyed table, assert the partition is disjoint and total (139 `BAR-*`, each once) and the vocabulary conforms, compose the access-note preamble, write `../outputs/live-journeys-measurement.md` (this subtree's declared output), and fold this subtree to COMPLETED. | `../outputs/live-journeys-measurement.md` (+ `../SYNTHESIS.md`) |

### Dependency Graph

```
SUBTASK_getin_identity       ──┐
SUBTASK_core_loop            ──┤
SUBTASK_account_lifecycle    ──┤
SUBTASK_resilience_states    ──┤
SUBTASK_safety_trust_support ──┼── SUBTASK_journeys_fold ── (fold → SUBTASK_live_journeys COMPLETED)
SUBTASK_visual_craft_nav     ──┤
SUBTASK_responsive_phone     ──┤
SUBTASK_accessibility        ──┤
SUBTASK_web_delivery_api     ──┘
```

---

## Contract

The two co-designed outputs of this decomposition are the task tree above and the sub-contract in `contracts/`. The
nine measurement children are parts of one measurement; they share one real seam — one `bar_id`-keyed verdict table
over the 139 `manual_user_check` `BAR-*`, partitioned by an explicit per-cluster `BAR-*` assignment, then unioned and
checked for totality by the fold. That seam is frozen in `contracts/_MANIFEST.yaml` before any child runs.

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` (extends `../../contracts/` and `../../../../contracts/` additively; never overrides
the `live_status` vocab, the `verification_method` vocab, or the matrix columns)

### Inherited Contracts

| Ancestor contract | Path (from a child) | What it binds here |
|---|---|---|
| id & traceability schema | `../../../../contracts/id_and_traceability_schema.yaml` | `live_status` vocab; the closed `verification_method` vocab |
| measurement sub-contract | `../../contracts/_MANIFEST.yaml` | `verdict_row_schema` (columns `bar_id, live_status, observation`); `live_status_key: bar_id`; the `manual_user_check` partition belongs to this subtree |

This subtree composes against these and MUST NOT redefine the `live_status` vocab, the `verification_method` vocab, or
the matrix columns.

### Identities (asserted by the fold)

- [ ] `CLUSTER_DISJOINT_TOTAL` — the nine clusters' `bar_id` sets are pairwise disjoint and union to exactly the 139
      `manual_user_check` `BAR-*`.
- [ ] `MANUAL_STATUS_TOTAL` — every one of the 139 carries exactly one `live_status` and a recorded observation.
- [ ] `OBSERVATION_GROUNDED` — every observation is grounded in an actual exercise of the live product or an actual
      `c805525` source artifact; unobservable criteria judged conservatively with the reason stated.
- [ ] `VOCAB_CONFORMS` — every `live_status` is from the inherited vocab; every `bar_id` is verbatim.
- [ ] `OUTPUT_HYGIENE` — no host/system/taskflow detail in `outputs/live-journeys-measurement.md`; repository identity
      only.

### Thin-Seam Note

The seam is not thin: a shared, cluster-partitioned `bar_id`-keyed verdict table with a totality invariant over 139
criteria is a real contract. Children compose against `contracts/` and MUST NOT redefine the inherited vocabularies.
