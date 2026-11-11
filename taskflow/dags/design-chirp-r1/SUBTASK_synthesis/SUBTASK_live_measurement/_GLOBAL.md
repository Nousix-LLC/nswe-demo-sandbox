# _GLOBAL.md — SUBTASK_live_measurement (live-product measurement subtree hub)

## Project Context

**Status**: Active

### Objective

Measure the deployed chirp product at commit `c805525` against **every** `BAR-*` in the release bar (278
criteria) and judge each `met | partial | missing | not_applicable`, each with a recorded observation grounding the
verdict — what was exercised or inspected, and what was seen. The one consolidated output is
`outputs/live-measurement.md`, one row per `BAR-*`, keyed by `bar_id` so the gate's fold joins it into the
traceability matrix mechanically.

This is the empirical half of `SUBTASK_synthesis` (the DAG's verification gate). It writes **no product code** and
measures the live product **read-only**.

### Why this decomposes

The work is 278 criteria across five areas (Product 35, Domain 60, Experience 94, Identity 40, Operational 49),
verified by four distinct methods. Each method is a different kind of observation against a different access surface:

- `manual_user_check` (139) — a person exercises the running product and observes the result.
- `operational_check` (68) — a running-service property is observed (data surviving a restart, a backup restored, a
  limit enforced, a readiness signal).
- `automated_test` (36) — a test in the repository at `c805525` asserts it.
- `inspection` (35) — a declared property is read from a config, manifest, or code artifact at `c805525`.

Each `BAR-*` names exactly one of these methods, so partitioning by method is disjoint and covers all 278 with no
overlap. The four partitions are measured independently and in parallel, then a synthesis fold unions them into the
single `bar_id`-keyed table and confirms every `BAR-*` is present exactly once. Splitting by method keeps each child
to one coherent kind of observation and lets the one expensive setup for each access surface (a live user session, a
restart drill, the cloned repo, a config read) happen once rather than being repeated per area.

### Scope

**In Scope:**
- Judging every `BAR-*` against the live product at `c805525` and the repository at `c805525`, by the method each
  `BAR-*` declares, to a recorded observation.
- Consolidating the four partition verdicts into `outputs/live-measurement.md` and confirming totality
  (every `BAR-*` once) and vocabulary conformance.

**Out of Scope:**
- Writing product code, editing the design docs or backlog, or mutating the live product beyond the normal effect of
  a throwaway test account's own actions.
- The traceability-matrix skeleton and the identity assertions (owned by the sibling `SUBTASK_identity_traceability`),
  the join into the matrix, and the root verdict (owned by `SUBTASK_fold` at the gate level).
- Any repo/cluster/namespace other than `Nousix-LLC/nswe-demo` and the project's own live deployment.

### Success Criteria

- [ ] Every one of the 278 `BAR-*` carries exactly one `live_status` ∈ {met, partial, missing, not_applicable} and a
      recorded observation in `outputs/live-measurement.md`.
- [ ] Each observation is grounded in an actual exercise of the live product or an actual repository artifact at
      `c805525` — no assumed or confabulated results. A criterion that cannot be observed in this environment is
      judged conservatively (not optimistically) with the reason stated.
- [ ] Verdicts use the inherited `live_status` vocabulary and reference `BAR-*` ids verbatim.
- [ ] The four partitions are disjoint and total: each `BAR-*` appears in exactly the partition matching its declared
      `verification_method`, and the union is all 278.
- [ ] Measurement is read-only on the live product; the output touches only `Nousix-LLC/nswe-demo` and the project's
      own deployment.

---

## Constraints and Requirements

### Process Constraints
- **Read-only measurement.** Exercising the live product MUST NOT mutate it beyond the normal effect of a user's own
  actions on a throwaway test account, and MUST NOT touch any repo/cluster/namespace outside the project's own. No
  product code is written.
- **Conservative where unobservable.** Where a method cannot be run in this environment, say so in the observation and
  judge conservatively (`missing`/`partial` with the reason) rather than optimistically. Do not invent an observation.
- **Each `BAR-*` once.** A criterion is measured by the child owning its declared method and appears in exactly one
  partition. No criterion is measured twice or left out.

### Hygiene (binding on the output and on anything that could reach GitHub)
The host and deployment facts needed to reach the live product (per the project `CLAUDE.md`) are for running checks
only and MUST NOT appear in the output. No host or cluster address, no SSH detail, no filesystem or taskflow path, no
agent/DAG/run id. Name things by repository identity only — `owner/repo`, commit SHA, repo-relative paths, and
`BAR-*`/`REQ-*` ids. `outputs/live-measurement.md` carries a short preamble recording only *that* the live product was
reached (or why it could not be), by repository/commit identity — never how.

---

## Input Specifications

Paths are relative to each child's own workspace (`SUBTASK_live_measurement/SUBTASK_<slug>/`). The sibling tasks these
read from are COMPLETED; read their outputs directly (do not poll, do not re-verify completion).

| Source | Location (from a child) | Role |
|--------|--------------------------|------|
| This subtree hub | `../_GLOBAL.md` | Shared context (this file) |
| This subtree's sub-contract | `../contracts/_MANIFEST.yaml` | The method partition, the per-row schema, ownership, the totality identity, the `live_status` vocab |
| Gate hub | `../../_GLOBAL.md` | Verification-gate context |
| Gate sub-contract | `../../contracts/_MANIFEST.yaml` | `live_status` vocab + the measurement join seam |
| Root id/traceability schema | `../../../contracts/id_and_traceability_schema.yaml` | `live_status` vocab + the closed `verification_method` vocabulary (authoritative, not redefined) |
| Release bar | `../../../SUBTASK_release_bar/outputs/release-bar.md` | The 278 `BAR-*`, each with its statement, enforced `REQ-*`, stage, and `verification_method` |
| Design PR record | `../../../SUBTASK_design_pr/outputs/design-pr.md` | PR #, branch, and the repo `design/` map, for context |
| Repository @ `c805525` | cloned under `../../../SUBTASK_design_pr/repo` (or a fresh `gh repo clone Nousix-LLC/nswe-demo` into the child's own workspace, checked out at `c805525`) | Inspect code/config/manifests and run/read tests |
| Live deployment | ArgoCD app `chirp` @ `c805525` (reached per the project `CLAUDE.md` host notes) | Exercise the product read-only; observe running-service properties |

---

## Methodology Posture

The Phase-B `design` methodology loader is unavailable run-wide (`agent_domain_unset`; every sibling gate hit the same
and proceeded). Each child applies the **principal-product-designer persona** and the relayed **Release Definition**
guidance — **ReleaseBar**: measure the product criterion by criterion as someone who was not in the design room, and
match each `BAR-*`'s declared `verification_method` to how it is observed. Children record the loader limitation and
proceed; they do not block on it.

---

## Task Structure

### Overview

```
SUBTASK_live_measurement/
├── _GLOBAL.md                          (this hub)
├── contracts/
│   └── _MANIFEST.yaml                  (sub-contract: method partition, row schema, ownership, totality — READ-ONLY)
├── outputs/                            (the fold writes outputs/live-measurement.md here)
├── SUBTASK_live_journeys/_BRIEF.md     (measure every manual_user_check BAR-*)
├── SUBTASK_automated_tests/_BRIEF.md   (measure every automated_test BAR-*)
├── SUBTASK_inspection_checks/_BRIEF.md (measure every inspection BAR-*)
├── SUBTASK_operational_checks/_BRIEF.md(measure every operational_check BAR-*)
└── SUBTASK_measurement_fold/_BRIEF.md  (synthesis: union the four, assert totality, write outputs/live-measurement.md, fold)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_live_journeys` | none | Exercise the deployed product at `c805525` as a user and judge every `BAR-*` whose `verification_method` is `manual_user_check` (139), each with a recorded observation. | `outputs/live-journeys-measurement.md` |
| `SUBTASK_automated_tests` | none | Run and read the repository test suite at `c805525` and judge every `BAR-*` whose `verification_method` is `automated_test` (36), each with a recorded observation. | `outputs/automated-test-measurement.md` |
| `SUBTASK_inspection_checks` | none | Inspect config/manifest/code at `c805525` and judge every `BAR-*` whose `verification_method` is `inspection` (35), each with a recorded observation. | `outputs/inspection-measurement.md` |
| `SUBTASK_operational_checks` | none | Observe running-service properties of the deployment at `c805525` (restart survival, backup/restore, limits, readiness) and judge every `BAR-*` whose `verification_method` is `operational_check` (68), each with a recorded observation. | `outputs/operational-measurement.md` |
| `SUBTASK_measurement_fold` | `SUBTASK_live_journeys`, `SUBTASK_automated_tests`, `SUBTASK_inspection_checks`, `SUBTASK_operational_checks` | **Synthesis.** Union the four partition verdicts into the one `bar_id`-keyed table, assert the partition is disjoint and total (278 `BAR-*`, each once) and the vocabulary conforms, compose the access-note preamble, write `../outputs/live-measurement.md` (this subtree's declared output), and fold this subtree to COMPLETED. | `../outputs/live-measurement.md` (+ `../SYNTHESIS.md`) |

### Dependency Graph

```
SUBTASK_live_journeys      ──┐
SUBTASK_automated_tests    ──┤
SUBTASK_inspection_checks  ──┼── SUBTASK_measurement_fold ── (fold → SUBTASK_live_measurement COMPLETED)
SUBTASK_operational_checks ──┘
```

---

## Contract

The two co-designed outputs of this decomposition are the task tree above and the sub-contract in `contracts/`. The
four measurement children are parts of one measurement; they share a real seam — one `bar_id`-keyed verdict table,
partitioned by each `BAR-*`'s declared `verification_method`, then unioned and checked for totality by the fold. That
seam is frozen in `contracts/_MANIFEST.yaml` before any child runs.

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` (extends the inherited `../../contracts/` and `../../../contracts/` additively; never
overrides the `live_status` vocab, the `verification_method` vocab, or the matrix columns)

### Inherited Contracts

| Ancestor contract | Path (from a child) | What it binds here |
|---|---|---|
| id & traceability schema | `../../../contracts/id_and_traceability_schema.yaml` | `live_status` vocab; the closed `verification_method` vocab |
| gate sub-contract | `../../contracts/_MANIFEST.yaml` | `live_status_key: bar_id`; one verdict per `BAR-*`; the measurement join seam |

This subtree composes against these and MUST NOT redefine the `live_status` vocab, the `verification_method` vocab, or
the matrix columns.

### Thin-Seam Note

The seam is not thin: a shared, method-partitioned `bar_id`-keyed verdict table with a totality invariant is a real
contract. Children compose against `contracts/` and MUST NOT redefine the inherited vocabularies.
