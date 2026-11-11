# _GLOBAL.md — SUBTASK_bar_ux subtree hub (the experience-area release-bar slice)

## Project Context

**Status**: Active

### Objective

Author the experience-area release-bar fragment `SUBTASK_bar_ux/outputs/bar-ux.md`: `BAR-200..299`
criteria that hold every **release-gating** `REQ-UX-*` from the experience design to a concrete, testable
release condition, plus the coverage note the parent synthesis gate needs to assert gating coverage without
re-deriving the gating set. This subtree is the decomposition of the task `SUBTASK_bar_ux`; its single
deliverable is that task's declared output (`SUBTASK_bar_ux/outputs/bar-ux.md`, owned by `SUBTASK_bar_ux` per
the parent `../contracts/bar_partition.yaml`).

This hub carries the shared context for the subtree. The authoritative parent spec is `../SUBTASK_bar_ux`'s
`_BRIEF.md` (my own brief); the parent subtree hub is `../_GLOBAL.md`; the inherited seams are `../../contracts/`
(DAG-root id/traceability scheme) and `../contracts/` (the `SUBTASK_release_bar` BAR partition). The subtree's
own frozen seam is `contracts/` here, which sub-partitions my `BAR-200..299` range across the sub-area spokes.

### Why this task decomposed

My brief owns the experience-area slice of the whole-product release bar: `BAR-200..299` enforcing every
release-gating `REQ-UX-*`. The experience design is 4,671 lines with 119 `REQ-UX-*`, of which **106 are
release-gating** across five enumerated experience areas (information architecture & interaction, the visual
language & component system, screens & flows, responsive layout, accessibility). The **Output-Size trigger
fires** (a comprehensive UX bar fragment plus a ~106-row coverage note is an estimated ~450–650 lines, over
the 400-line MUST-decompose line), and the brief enumerates five distinct areas (the screens & flows area
alone carries ~43 gating requirements). With a trigger fired and the evaluation genuinely uncertain, the
normative asymmetric bias requires decomposition. "A flat `BAR-200..299` id space is best held in one head /
splitting fragments the natural cross-area bar clusters" is **not** grounds to keep it atomic — the standing
design contract disqualifies that instinct and the triggers govern. This recursively mirrors the parent
`SUBTASK_release_bar` by-area fan-out.

The sound cut is a **by-sub-area fan-out** of the UX bar authoring (one spoke per experience area, each owning
a disjoint `BAR-*` sub-range of `200..299`), with a synthesis hub that assembles the single `outputs/bar-ux.md`,
finalizes the within-area proposed stages into one coherent set, asserts the sub-identities with recorded
evidence, mints any cross-cutting `BAR-295..299` a single area does not own, and folds `SUBTASK_bar_ux`.

### Scope

**In Scope:**
- Five per-area BAR-authoring spokes: each reads the experience design `../../SUBTASK_experience_design/outputs/experience-design.md`
  for its area's requirements, composes against `../../contracts/`, `../contracts/`, and this subtree's `contracts/`,
  and authors `BAR-*` (in its assigned sub-range) enforcing that area's **release-gating** `REQ-UX-*`, with a
  per-area coverage note and a proposed stage per `BAR-*`.
- A synthesis hub that assembles the five sub-fragments into the single `outputs/bar-ux.md`, finalizes the
  experience-area proposed stages into one coherent set, asserts the sub-identities with recorded evidence
  (no silent plugs), mints cross-cutting `BAR-295..299` only for a finding no single sub-area owns, authors
  `SYNTHESIS.md`, and folds `SUBTASK_bar_ux`.

**Out of Scope:**
- Re-authoring any `REQ-UX-*` (the bar **references** them; it does not restate them).
- The other four area fragments (`bar-prod`, `bar-dom`, `bar-id`, `bar-ops`) and the whole-bar assembly,
  cross-area staging line, and whole-design gap review — those are the parent `SUBTASK_bar_synthesis`'s.
- Any requirement that is **not** release-gating (`release_gating: false`). Non-gating `REQ-UX-*` may be
  referenced for context but MUST NOT be the sole justification of a `BAR-*` in this fragment.
- Engineering "how" — each `BAR-*` states a release condition as a checkable fact, not an implementation.

### Success Criteria

- [ ] Every **release-gating** `REQ-UX-*` (106 total) is referenced by ≥1 `BAR-*` in `outputs/bar-ux.md`.
- [ ] Every `BAR-*` lies within `BAR-200..299`, names a `verification_method` from the frozen vocabulary,
      references ≥1 `REQ-*`, and carries a stage ∈ {`usable_early`, `releasable`}.
- [ ] `BAR-*` ids are distinct across all sub-fragments and the synthesis cross-cutting bars; each spoke stayed
      within its assigned sub-range.
- [ ] `outputs/bar-ux.md` carries the coverage note (every release-gating `REQ-UX-*` → the `BAR-*` covering it)
      so the parent synthesis gate asserts `GATING_REQ_COVERAGE` for the UX area without re-deriving the set.
- [ ] `outputs/bar-ux.md` is repository-ready: no host/system/taskflow detail, no attribution trailer.

---

## Constraints and Requirements

- **Compose against the inherited contracts** (`../../contracts/` and `../contracts/`) and this subtree's
  `contracts/`: use the `BAR-<NNN>` id scheme (3-digit), the closed `verification_methods` vocabulary
  (`manual_user_check`, `automated_test`, `inspection`, `operational_check`), and the stage vocabulary
  (`usable_early` | `releasable`). This subtree's `contracts/` only **sub-partitions** the UX range and fixes the
  fragment layout; it redefines nothing inherited.
- **Stay in range.** Each spoke mints `BAR-*` ONLY within its assigned sub-range. A `BAR-*` MAY reference
  `REQ-UX-*` from more than one sub-area; it is owned by the spoke whose sub-area most centrally holds the
  gating requirement it enforces. Cross-sub-area references are expected and fine; siblings do not duplicate
  a `BAR-*`.
- **Gating is read from the design doc.** Each `REQ-UX-*` carries a `release_gating: true|false` field in the
  experience design; a spoke covers exactly the `true` set for its sub-area. A `false` requirement is not
  covered (the experience-design author's recorded reason stands).
- **A bar, not an aspiration** — each `BAR-*` checkable by someone who was not in the room. Accessibility
  criteria name the concrete check (e.g. a stated WCAG 2.1 AA conformance level verified by inspection /
  automated scan / keyboard / screen-reader pass), never "accessible".
- **Repository hygiene** (binding on `outputs/bar-ux.md`): no host/cluster addresses, no filesystem/taskflow
  paths, no agent/DAG/run ids, no `SYNTHESIS.md`/`SUSPENSION.md` locations, no attribution trailers. Name
  things by repository identity (`REQ-UX-*`/`BAR-*` ids, repo-relative `design/experience-design.md`). This
  subtree's internal files (`_GLOBAL.md`, `contracts/`, per-spoke `_BRIEF.md`, `SYNTHESIS.md`, `SUSPENSION.md`)
  are taskflow-internal and are not repository content.

### Methodology posture

The Phase-B `design` methodology loader is **unavailable in this environment** (the methodology surface
returns `agent_domain_unset`, run-wide; the parent subtree recorded the same and proceeded). Each spoke's
brief relays its bundle IDs (Release Definition primary; Experience Design, Product Strategy supporting);
spokes apply the product-designer persona's release-definition judgment and that relayed guidance rather than
blocking. This constraint is recorded in internal fold/suspension records only and kept out of the
repository-bound deliverable.

---

## Input Specifications

| Source | Identity | Role |
|--------|----------|------|
| Experience design | `../../SUBTASK_experience_design/outputs/experience-design.md` | The authoritative `REQ-UX-*` set (119) and the per-REQ `release_gating` flag; each spoke reads its sub-area's requirements |
| DAG-root contract | `../../contracts/` (read-only) | `REQ`/`BAR` id scheme, closed `verification_methods` vocab, stages, design-artifact map |
| Parent subtree contract | `../contracts/` (read-only) | The `SUBTASK_release_bar` BAR partition: this subtree owns `BAR-200..299` and the `bar-ux.md` fragment; the per-BAR field set; the `proposed_stage` convention |
| This subtree contract | `contracts/` (read-only for spokes) | The `BAR-200..299` sub-partition across the five area spokes + synthesis; the sub-fragment layout; the sub-identities |

Each spoke reads the experience design for its own sub-area's authoritative gating set (the `release_gating`
field per `REQ-UX-*`).

---

## Task Structure

### Overview

```
SUBTASK_bar_ux/
├── _GLOBAL.md                        (this hub)
├── _BRIEF.md                         (my brief from the parent)
├── contracts/                        (READ-ONLY for descendants; sub-partitions BAR-200..299 additively)
│   ├── _MANIFEST.yaml
│   └── bar_ux_partition.yaml
├── SUBTASK_bar_ux_ia/_BRIEF.md
├── SUBTASK_bar_ux_visual/_BRIEF.md
├── SUBTASK_bar_ux_screens/_BRIEF.md
├── SUBTASK_bar_ux_responsive/_BRIEF.md
├── SUBTASK_bar_ux_a11y/_BRIEF.md
├── SUBTASK_bar_ux_synthesis/_BRIEF.md
└── outputs/bar-ux.md                 (produced by SUBTASK_bar_ux_synthesis — SUBTASK_bar_ux's declared output)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_bar_ux_ia` | none | Author `BAR-200..214` enforcing each release-gating `REQ-UX-001..019` (information architecture & interaction model). | `SUBTASK_bar_ux_ia/outputs/bar-ux-ia.md` |
| `SUBTASK_bar_ux_visual` | none | Author `BAR-215..229` enforcing each release-gating `REQ-UX-020..039` (visual language & component system). | `SUBTASK_bar_ux_visual/outputs/bar-ux-visual.md` |
| `SUBTASK_bar_ux_screens` | none | Author `BAR-230..264` enforcing each release-gating `REQ-UX-040..089` (screens & flows, incl. entry/auth, core loop, profiles, settings, account lifecycle, safety, and the cross-screen empty/error/loading/session states). | `SUBTASK_bar_ux_screens/outputs/bar-ux-screens.md` |
| `SUBTASK_bar_ux_responsive` | none | Author `BAR-265..274` enforcing each release-gating `REQ-UX-090..099` (responsive layout). | `SUBTASK_bar_ux_responsive/outputs/bar-ux-responsive.md` |
| `SUBTASK_bar_ux_a11y` | none | Author `BAR-275..294` enforcing each release-gating `REQ-UX-100..119` (accessibility). | `SUBTASK_bar_ux_a11y/outputs/bar-ux-a11y.md` |
| `SUBTASK_bar_ux_synthesis` | `SUBTASK_bar_ux_ia`, `SUBTASK_bar_ux_visual`, `SUBTASK_bar_ux_screens`, `SUBTASK_bar_ux_responsive`, `SUBTASK_bar_ux_a11y` | **Verification gate + fold.** Assemble the five sub-fragments into `outputs/bar-ux.md`; finalize the experience-area proposed stages into one coherent set; assert the sub-identities with recorded evidence (no silent plugs); mint cross-cutting `BAR-295..299` only for a finding no single sub-area owns; build the whole coverage note; author `SYNTHESIS.md` and fold `SUBTASK_bar_ux`. | `SUBTASK_bar_ux/outputs/bar-ux.md`, `SUBTASK_bar_ux/SYNTHESIS.md` |

### Dependency Graph (the table above is authoritative)

```
bar_ux_ia         ─┐
bar_ux_visual     ─┤
bar_ux_screens    ─┼─> bar_ux_synthesis ─(fold)─> resumes SUBTASK_bar_ux
bar_ux_responsive ─┤
bar_ux_a11y       ─┘
```

---

## Contract

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` — extends the inherited `../contracts/` and `../../contracts/` additively
(sub-partitions the UX `BAR-200..299` range across the five area spokes + the synthesis cross-cutting range,
and fixes the sub-fragment layout). It redefines nothing inherited.

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| DAG-root id/traceability schema | `../../contracts/` | `BAR-<NNN>` 3-digit format; the per-BAR field set (`id`, `statement`, `references` ≥1 `REQ-*`, `verification_method`, `stage`); the closed `verification_methods` vocab; stage ∈ {`usable_early`, `releasable`} |
| `SUBTASK_release_bar` BAR partition | `../contracts/` | This subtree owns `BAR-200..299` and the `SUBTASK_bar_ux/outputs/bar-ux.md` fragment; the `proposed_stage` convention (spokes propose; the parent synthesis finalizes the cross-area line); the bar-fragment layout + coverage-note requirement |

### Structural Declarations
- `contracts/_MANIFEST.yaml` — kind, per-spoke ownership, the sub-identities the synthesis gate asserts, derived artifact.
- `contracts/bar_ux_partition.yaml` — the disjoint `BAR-*` sub-range per area spoke, the synthesis cross-cutting
  sub-range, the per-BAR field set (inherited), the sub-fragment layout each spoke emits, and the per-area
  release-gating `REQ-UX-*` set each spoke must cover.

### Ownership (one producer per artifact)

| Artifact | Owning subtask |
|----------|----------------|
| `SUBTASK_bar_ux_ia/outputs/bar-ux-ia.md` + `BAR-200..214` | `SUBTASK_bar_ux_ia` |
| `SUBTASK_bar_ux_visual/outputs/bar-ux-visual.md` + `BAR-215..229` | `SUBTASK_bar_ux_visual` |
| `SUBTASK_bar_ux_screens/outputs/bar-ux-screens.md` + `BAR-230..264` | `SUBTASK_bar_ux_screens` |
| `SUBTASK_bar_ux_responsive/outputs/bar-ux-responsive.md` + `BAR-265..274` | `SUBTASK_bar_ux_responsive` |
| `SUBTASK_bar_ux_a11y/outputs/bar-ux-a11y.md` + `BAR-275..294` | `SUBTASK_bar_ux_a11y` |
| `outputs/bar-ux.md` + `BAR-295..299` (cross-cutting) + `SYNTHESIS.md` | `SUBTASK_bar_ux_synthesis` |

### Identities (asserted by `SUBTASK_bar_ux_synthesis` with recorded evidence; no silent plugs)
1. **UX_BAR_RANGE_RESPECTED** — every `BAR-NNN` lies within its owning spoke's assigned sub-range; no spoke wrote outside its sub-range.
2. **UX_NO_BAR_COLLISION** — all `BAR-NNN` ids across the five sub-fragments + synthesis cross-cutting bars are distinct.
3. **UX_GATING_REQ_COVERAGE** — every release-gating `REQ-UX-*` (the 106 with `release_gating: true`) is referenced by ≥1 `BAR-*`; evaluated per sub-area against that sub-area's gating set.
4. **UX_BAR_TESTABLE** — every `BAR-*` names a `verification_method` from the frozen vocabulary and references ≥1 `REQ-*`.
5. **UX_BAR_STAGED** — every `BAR-*` carries a stage ∈ {`usable_early`, `releasable`}; the assembled fragment states one stage per `BAR-*` (no criterion staged two ways). The parent `SUBTASK_bar_synthesis` owns the final cross-area line; this subtree's stages are the UX-view proposal.
6. **UX_NONGATING_EXCLUDED** — no `BAR-*` is justified solely by a non-gating `REQ-UX-*` (`release_gating: false`).
7. **UX_COVERAGE_NOTE_PRESENT** — `bar-ux.md` carries the coverage note mapping every release-gating `REQ-UX-*` to the `BAR-*`(s) covering it.
8. **UX_HYGIENE** — `bar-ux.md` carries no host/system/taskflow detail and no attribution trailer.

### Derived Artifact
- **UX BAR↔REQ coverage map** — assembled by `SUBTASK_bar_ux_synthesis` from the five sub-fragments; is the
  coverage note in `bar-ux.md` and feeds the parent `SUBTASK_bar_synthesis` BAR↔REQ coverage map.

### Thin-Seam Note
The seam is not thin: a shared flat `BAR-200..299` id space, a per-sub-area gating-coverage obligation, and one
coherent per-`BAR-*` staging proposal are a rich contract. Spokes MUST compose against `contracts/` and MUST
NOT mint `BAR-*` outside their sub-range or redefine any inherited schema.

---

## Output Specifications

| Deliverable | Format | Location | Description |
|-------------|--------|----------|-------------|
| UX release-bar fragment | Markdown | `SUBTASK_bar_ux/outputs/bar-ux.md` | The single assembled UX bar fragment (BAR-200..299 blocks + coverage note), owned by `SUBTASK_bar_ux` and consumed by the parent `SUBTASK_bar_synthesis`. Repository-ready. |
| Fold record | Markdown | `SUBTASK_bar_ux/SYNTHESIS.md` | The synthesis gate's fold record (identities asserted with evidence); taskflow-internal. |
