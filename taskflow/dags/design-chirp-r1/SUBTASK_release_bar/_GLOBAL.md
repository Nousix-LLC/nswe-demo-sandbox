# _GLOBAL.md — SUBTASK_release_bar subtree hub (the release bar + completeness/gap review)

## Project Context

**Status**: Active

### Objective

Consolidate the five completed concern designs into the one `design/release-bar.md`: an **MVP-vs-releasable
scoping**, a concrete **testable release bar** (`BAR-*`, each referencing the `REQ-*` it enforces and naming a
verification method), and a **completeness & gap review** that records an in/out-of-scope judgment for every
surface a product of this kind is expected to have. This subtree is the decomposition of the parent task
`SUBTASK_release_bar`; its single deliverable is the parent's declared output.

This hub carries the shared context for the subtree. The authoritative parent spec is `../_BRIEF.md` and the
parent hub is `../_GLOBAL.md` (read for the engagement-wide constraints and the contract this subtree composes
against). The subtree's own frozen seam is `contracts/` here.

### Why this task decomposed

The parent brief enumerates three facets — MVP/releasable scoping, the `BAR-*` bar, and the completeness/gap
review — and the bar must cover **every release-gating requirement across five large area designs** (≈395
requirements total: PROD 42, DOM 81, UX 119, ID 78, OPS 75; the experience design alone is 4,671 lines). The
Token, Scope-Based, and Output-Size triggers all fire; faithfully consuming all five designs and authoring
comprehensive bar coverage far exceeds one atomic invocation. The sound cut is a **by-area fan-out** of the bar
authoring (one spoke per source area, each owning a disjoint `BAR-*` number range) with the **cross-cutting**
staging and the **whole-design** gap review done once in the synthesis hub. This mirrors the sibling
`SUBTASK_operational_readiness` pattern. "A release bar is one coherent judgment best held whole" is **not**
grounds to keep it atomic — the standing contract disqualifies that instinct, and the triggers govern.

### Scope

**In Scope:**
- Five per-area BAR-authoring spokes: each reads one area's design doc + `../contracts/` + this subtree's
  `contracts/`, and authors `BAR-*` (in its assigned range) enforcing that area's **release-gating** `REQ-*`.
- A synthesis hub that assembles the single `outputs/release-bar.md` with the three required sections, finalizes
  the cross-cutting MVP-vs-releasable staging, runs the completeness & gap review over the whole design, asserts
  the identities below with recorded evidence, and folds the parent.

**Out of Scope:**
- Rewriting or restating any area's `REQ-*` (the bar **references** them; it does not re-author them).
- The design PR, the board backlog, and the whole-DAG live-product measurement (later sibling tasks).
- Repo/engineering "how" — the bar states release conditions as checkable facts, not implementations.

### Success Criteria

- [ ] Every **release-gating** `REQ-*` in each area is referenced by ≥1 `BAR-*`.
- [ ] Every `BAR-*` is testable (names a verification method from the frozen vocabulary) and references ≥1 `REQ-*`.
- [ ] Every `BAR-*` carries a stage ∈ {`usable_early`, `releasable`}; the scoping section agrees with the stages.
- [ ] The gap review records an in/out-of-scope judgment, with a reason, for each expected account/operational
      surface (sign-up/in/recovery, account deletion, data export, onboarding, settings, notifications,
      admin/support, billing).
- [ ] `outputs/release-bar.md` contains the three sections from `../contracts/design_artifact_map.yaml`
      (`mvp_vs_releasable_scoping`, `release_bar`, `completeness_and_gap_review`) and is repository-ready.

---

## Constraints and Requirements

- **Compose against the inherited contract** (`../contracts/`): use the `BAR-<NNN>` id scheme, the closed
  `verification_methods` vocabulary (`manual_user_check`, `automated_test`, `inspection`, `operational_check`),
  the stage vocabulary (`usable_early` | `releasable`), and the `design_artifact_map.yaml` required sections.
  Do **not** redefine the inherited schema; this subtree's `contracts/` only **extends** it (the BAR partition).
- **Repository hygiene** (binding on the deliverable): no host/cluster addresses, no filesystem/taskflow paths,
  no agent/DAG/run ids, no `SYNTHESIS.md` locations, no attribution trailers. Name things by repository identity
  (`Nousix-LLC/nswe-demo`, repo-relative design paths, `REQ-*`/`BAR-*` ids, commit `c805525`). This subtree's
  internal files (`_GLOBAL.md`, `contracts/`, `SYNTHESIS.md`, `SUSPENSION.md`) are taskflow-internal and are not
  repository content.
- **A bar, not an aspiration** — each `BAR-*` checkable by someone who was not in the room.

### Methodology posture

The Phase-B `design` methodology loader is **unavailable in this environment** (the methodology surface returns
`agent_domain_unset`, run-wide; the sibling synthesis gates hit the same and proceeded). Each child's brief
relays its bundle IDs (Release Definition primary; Release Readiness, Product Strategy, Identity and Trust,
Product Surfaces supporting) per the parent Domain Mapping; children apply the product-design persona's
release-definition judgment and that relayed guidance rather than blocking. The constraint is recorded in
internal fold/suspension records only and kept out of the repository-bound deliverable.

---

## Input Specifications

| Source | Identity | Role |
|--------|----------|------|
| Product requirements | `../SUBTASK_product_requirements/outputs/product-requirements.md` | `REQ-PROD-*` (42) + journeys/scope |
| Domain & application design | `../SUBTASK_domain_app_design/outputs/domain-application-design.md` | `REQ-DOM-*` (81) incl. the durable-persistence blocker |
| Experience design | `../SUBTASK_experience_design/outputs/experience-design.md` | `REQ-UX-*` (119) incl. screens/flows, a11y |
| Identity & security | `../SUBTASK_identity_trust/outputs/identity-security.md` | `REQ-ID-*` (78) accounts/auth/authz/privacy |
| Operational readiness | `../SUBTASK_operational_readiness/SUBTASK_ops_synthesis/outputs/operational-readiness.md` | `REQ-OPS-*` (75) durable data/backups/limits/observability/incident |
| Inherited contract | `../contracts/` (read-only) | `REQ`/`BAR` id scheme, verification vocab, stages, design-artifact map |

Each area design records release-gating per requirement as a markdown field `- **release_gating**: true|false`;
spokes read their own area's doc for the authoritative gating set.

---

## Task Structure

### Overview

```
SUBTASK_release_bar/
├── _GLOBAL.md                         (this hub)
├── _BRIEF.md                          (parent spec)
├── contracts/                         (READ-ONLY for descendants; extends ../contracts/ additively)
│   ├── _MANIFEST.yaml
│   └── bar_partition.yaml
├── SUBTASK_bar_prod/_BRIEF.md
├── SUBTASK_bar_dom/_BRIEF.md
├── SUBTASK_bar_ux/_BRIEF.md
├── SUBTASK_bar_id/_BRIEF.md
├── SUBTASK_bar_ops/_BRIEF.md
├── SUBTASK_bar_synthesis/_BRIEF.md
└── outputs/release-bar.md             (produced by SUBTASK_bar_synthesis — the parent's declared output)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_bar_prod` | none | Author `BAR-001..099` enforcing each release-gating `REQ-PROD-*`; reads `product-requirements.md`. | `SUBTASK_bar_prod/outputs/bar-prod.md` |
| `SUBTASK_bar_dom` | none | Author `BAR-100..199` enforcing each release-gating `REQ-DOM-*` (incl. durable persistence); reads `domain-application-design.md`. | `SUBTASK_bar_dom/outputs/bar-dom.md` |
| `SUBTASK_bar_ux` | none | Author `BAR-200..299` enforcing each release-gating `REQ-UX-*`; reads `experience-design.md`. | `SUBTASK_bar_ux/outputs/bar-ux.md` |
| `SUBTASK_bar_id` | none | Author `BAR-300..399` enforcing each release-gating `REQ-ID-*`; reads `identity-security.md`. | `SUBTASK_bar_id/outputs/bar-id.md` |
| `SUBTASK_bar_ops` | none | Author `BAR-400..499` enforcing each release-gating `REQ-OPS-*`; reads `operational-readiness.md`. | `SUBTASK_bar_ops/outputs/bar-ops.md` |
| `SUBTASK_bar_synthesis` | `SUBTASK_bar_prod`, `SUBTASK_bar_dom`, `SUBTASK_bar_ux`, `SUBTASK_bar_id`, `SUBTASK_bar_ops` | **Verification gate + fold.** Assemble the five fragments into `outputs/release-bar.md` (three sections); finalize the cross-cutting MVP-vs-releasable staging; run the completeness & gap review over the whole design; assert the identities with evidence (no silent plugs); author `SYNTHESIS.md` and fold the parent. May mint cross-cutting `BAR-900..999` for a gap-review finding no single area owns. | `SUBTASK_release_bar/outputs/release-bar.md`, `SUBTASK_release_bar/SYNTHESIS.md` |

### Dependency Graph (the table above is authoritative)

```
bar_prod ─┐
bar_dom  ─┤
bar_ux   ─┼─> bar_synthesis ─(fold)─> resumes SUBTASK_release_bar
bar_id   ─┤
bar_ops  ─┘
```

---

## Contract

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` (extends the inherited `../contracts/` additively — the BAR number-space
partition + the bar-fragment format + the subtree identities; it redefines nothing inherited).

### Structural Declarations
- `contracts/_MANIFEST.yaml` — kind, per-child ownership, the identities the synthesis gate asserts, derived artifact.
- `contracts/bar_partition.yaml` — the disjoint `BAR-*` number range per area spoke, the synthesis cross-cutting
  range, the per-BAR field set (inherited from the parent schema), the `proposed_stage` convention (spokes
  propose a stage; the synthesis hub finalizes the cross-cutting MVP line), and the fragment layout each spoke emits.

### Ownership (one producer per artifact)

| Artifact | Owning subtask |
|----------|----------------|
| `SUBTASK_bar_prod/outputs/bar-prod.md` + `BAR-001..099` | `SUBTASK_bar_prod` |
| `SUBTASK_bar_dom/outputs/bar-dom.md` + `BAR-100..199` | `SUBTASK_bar_dom` |
| `SUBTASK_bar_ux/outputs/bar-ux.md` + `BAR-200..299` | `SUBTASK_bar_ux` |
| `SUBTASK_bar_id/outputs/bar-id.md` + `BAR-300..399` | `SUBTASK_bar_id` |
| `SUBTASK_bar_ops/outputs/bar-ops.md` + `BAR-400..499` | `SUBTASK_bar_ops` |
| `outputs/release-bar.md` + `BAR-900..999` (cross-cutting) + `SYNTHESIS.md` | `SUBTASK_bar_synthesis` |

### Identities (asserted by `SUBTASK_bar_synthesis` with recorded evidence; no silent plugs)
1. **BAR_RANGE_RESPECTED** — every `BAR-NNN` lies within its owning spoke's assigned range; no spoke wrote outside its range.
2. **NO_BAR_COLLISION** — all `BAR-NNN` ids across the fragments + synthesis are distinct.
3. **GATING_REQ_COVERAGE** — every release-gating `REQ-*` in each area's design doc is referenced by ≥1 `BAR-*`
   (the inherited `BAR_COVERS_GATING_REQS`, evaluated per area against that area's gating set).
4. **BAR_TESTABLE** — every `BAR-*` names a `verification_method` from the frozen vocabulary and references ≥1 `REQ-*`.
5. **BAR_STAGED** — every `BAR-*` carries a stage ∈ {`usable_early`, `releasable`}; the `mvp_vs_releasable_scoping`
   section is consistent with the per-`BAR-*` stages (no criterion staged two ways).
6. **SURFACE_GAP_RECORDED** — the `completeness_and_gap_review` section records an in/out-of-scope judgment, with a
   reason, for each expected account/operational surface (the inherited `SURFACE_COVERAGE`, for this file).
7. **THREE_SECTIONS_PRESENT** — `release-bar.md` contains exactly the three sections required by `../contracts/design_artifact_map.yaml`.
8. **HYGIENE** — the deliverable carries no host/system/taskflow detail and no attribution trailer.

### Derived Artifact
- **BAR↔REQ coverage map** — assembled by `SUBTASK_bar_synthesis` from the five fragments; feeds the whole-DAG
  traceability matrix that `SUBTASK_synthesis` (the DAG root gate) consumes.

### Thin-Seam Note
The seam is not thin: a shared flat `BAR-*` id space, a cross-cutting staging line, and per-area gating coverage
are a rich contract. Spokes MUST compose against `contracts/` and MUST NOT mint `BAR-*` outside their range or
redefine the inherited schema.
