# _GLOBAL.md — SUBTASK_bar_ux_screens subtree hub (the screens & flows slice of the UX release bar)

## Project Context

**Status**: Active

### Objective

Author the screens-&-flows release-bar fragment `SUBTASK_bar_ux_screens/outputs/bar-ux-screens.md`:
`BAR-230..264` criteria that hold every **release-gating** `REQ-UX-*` in the screens band (`REQ-UX-040..089`,
43 gating) to a concrete, testable release condition, plus the coverage note the parent UX synthesis gate needs
to assert screens-area gating coverage without re-deriving the gating set. This subtree is the decomposition of
the task `SUBTASK_bar_ux_screens`; its single deliverable is that task's declared output
(`SUBTASK_bar_ux_screens/outputs/bar-ux-screens.md`), produced by `SUBTASK_bar_screens_synthesis`.

This hub carries the shared context for the subtree. The authoritative parent spec is this task's own `_BRIEF.md`
(`../SUBTASK_bar_ux_screens/_BRIEF.md`); the parent subtree hub is `../_GLOBAL.md`. The inherited seams are
`contracts/` here (this subtree's own, which sub-partitions `BAR-230..264`), `../../contracts/`
(`SUBTASK_bar_ux` UX partition), `../../../contracts/` (`SUBTASK_release_bar` BAR partition), and
`../../../../contracts/` (DAG-root id/traceability schema).

### Why this task decomposed

The brief owns the screens-&-flows slice of the UX release bar: `BAR-230..264` enforcing the 43 release-gating
`REQ-UX-040..089`. This is the **largest UX sub-area** (43 of the 106 gating UX requirements — ~40%). The brief
**enumerates eight distinct screen groups, each its own body of gating requirements** (entry & auth; home
timeline & compose core loop; conversation/like/follow; profiles & discovery lists; onboarding & profile edit;
settings & account lifecycle; safety/help/rules/not-found; cross-screen state patterns). Under the kernel's
**enumerated-concerns rule**, naming two or more distinct areas fires the Scope-Based trigger by that enumeration
alone; the Distinct-Concerns Test passes (these chapters could be authored by parallel specialists); and
**Trigger Precedence** forbids the weak Output-Size signal (~280–330 lines, a single file) and the low token
estimate from overriding the fired scope trigger. The evaluation is independent at this depth: "my parent already
split UX into areas" is NOT grounds for `Atomic`; the designer instinct to hold the screens picture whole is
explicitly disqualified as grounds for `Atomic`. With the scope trigger fired, the normative asymmetric bias
requires decomposition. This recursively mirrors the parent `SUBTASK_bar_ux` by-area fan-out.

The sound cut merges the eight enumerated groups into **five coherent screen-chapter spokes** (so each spoke is a
genuine body of work, not a 3-requirement micro-task), each owning a disjoint `BAR-*` sub-range of `230..264`,
plus a synthesis gate that assembles the single `outputs/bar-ux-screens.md`, finalizes the within-screens
proposed stages into one coherent set, asserts the sub-identities with recorded evidence, mints the cross-cutting
`BAR-264` only for a finding no single chapter owns, builds the whole coverage note, and folds
`SUBTASK_bar_ux_screens`.

### Scope

**In Scope:**
- Five per-chapter BAR-authoring spokes: each reads the experience design
  `../../../../SUBTASK_experience_design/outputs/experience-design.md` for its chapter's requirements, composes
  against `contracts/`, `../../contracts/`, `../../../contracts/`, and `../../../../contracts/`, and authors
  `BAR-*` (in its assigned sub-range) enforcing that chapter's **release-gating** `REQ-UX-*`, with a per-chapter
  coverage note and a proposed stage per `BAR-*`.
- A synthesis gate that assembles the five sub-fragments into the single `outputs/bar-ux-screens.md`, finalizes
  the screens proposed stages into one coherent set, asserts the sub-identities with recorded evidence (no silent
  plugs), mints cross-cutting `BAR-264` only for a finding no single chapter owns, authors the whole coverage
  note and `SYNTHESIS.md`, and folds `SUBTASK_bar_ux_screens`.

**Out of Scope:**
- Re-authoring any `REQ-UX-*` (the bar **references** them; it does not restate them).
- The other four UX area fragments (`bar-ux-ia`, `bar-ux-visual`, `bar-ux-responsive`, `bar-ux-a11y`) and the UX
  whole-fragment assembly — those are sibling spokes and the parent `SUBTASK_bar_ux_synthesis`'s.
- Any requirement that is **not** release-gating. Non-gating screens-band `REQ-UX-*` (`057, 064, 071, 072, 078,
  080, 081`) may be referenced for context but MUST NOT be the sole justification of a `BAR-*`.
- Engineering "how" — each `BAR-*` states a release condition as a checkable fact, not an implementation.

### Success Criteria

- [ ] Every **release-gating** `REQ-UX-*` in 040..089 (43 total) is referenced by ≥1 `BAR-*` in `outputs/bar-ux-screens.md`.
- [ ] Every `BAR-*` lies within `BAR-230..264`, names a `verification_method` from the frozen vocabulary,
      references ≥1 `REQ-*`, and carries a stage ∈ {`usable_early`, `releasable`}.
- [ ] `BAR-*` ids are distinct across all sub-fragments and the synthesis cross-cutting bar; each spoke stayed
      within its assigned sub-range.
- [ ] No `BAR-*` is justified solely by a non-gating `REQ-UX-*`.
- [ ] `outputs/bar-ux-screens.md` carries the coverage note (every release-gating screens `REQ-UX-*` → the `BAR-*`
      covering it) so the parent UX synthesis gate asserts screens-area gating coverage without re-deriving the set.
- [ ] `outputs/bar-ux-screens.md` is repository-ready: no host/system/taskflow detail, no attribution trailer.

---

## Constraints and Requirements

- **Compose against the inherited contracts** and this subtree's `contracts/`: use the `BAR-<NNN>` id scheme
  (3-digit), the closed `verification_methods` vocabulary (`manual_user_check`, `automated_test`, `inspection`,
  `operational_check`), and the stage vocabulary (`usable_early` | `releasable`). This subtree's `contracts/`
  only **sub-partitions** the `BAR-230..264` range and fixes the fragment layout; it redefines nothing inherited.
- **Stay in range.** Each spoke mints `BAR-*` ONLY within its assigned sub-range. A `BAR-*` MAY reference
  `REQ-UX-*` from more than one chapter; it is owned by the spoke whose chapter most centrally holds the gating
  requirement it enforces. Cross-chapter references are expected; siblings do not duplicate a `BAR-*`.
- **The id budget is tight by design** — 35 ids for 43 gating requirements. One `BAR-*` MAY (and often MUST)
  enforce several related `REQ-UX-*` in the same chapter. Cluster related gating requirements into one checkable
  release condition rather than restating each `REQ` one-to-one.
- **Gating is read from the design doc.** Each `REQ-UX-*` carries a `release_gating: true|false` field; a spoke
  covers exactly the `true` set for its chapter (listed in `contracts/bar_screens_partition.yaml`). A `false`
  requirement is not covered (the experience-design author's recorded reason stands).
- **A bar, not an aspiration** — each `BAR-*` checkable by someone who was not in the room. State the release
  condition as a checkable fact in the user's terms (what a stranger can observe on the live product), not an
  implementation. A `BAR-*` is not a restatement of a `REQ-*`.
- **Repository hygiene** (binding on the outputs): no host/cluster addresses, no filesystem/taskflow paths, no
  agent/DAG/run ids, no `SYNTHESIS.md`/`SUSPENSION.md` locations, no attribution trailers. Name things by
  repository identity (`REQ-UX-*`/`BAR-*` ids, repo-relative `design/experience-design.md`). This subtree's
  internal files are taskflow-internal and are not repository content.

### Methodology posture

The Phase-B `design` methodology loader is **unavailable in this environment** (the methodology surface returns
`agent_domain_unset`, run-wide; ancestors recorded the same and proceeded). Each spoke's brief relays its bundle
IDs (Release Definition primary; Experience Design, Product Strategy supporting); spokes apply the
product-designer persona's release-definition judgment and that relayed guidance rather than blocking. This
constraint is recorded in internal fold/suspension records only and kept out of the repository-bound deliverable.

---

## Input Specifications

| Source | Identity | Role |
|--------|----------|------|
| Experience design | `../../../../SUBTASK_experience_design/outputs/experience-design.md` | The authoritative `REQ-UX-040..089` set and the per-REQ `release_gating` flag; each spoke reads its chapter's requirements |
| This subtree contract | `contracts/` (read-only for spokes) | The `BAR-230..264` sub-partition across the five chapter spokes + synthesis; the per-chapter gating set; the sub-fragment layout; the proposed_stage convention |
| UX partition contract | `../../contracts/` (read-only) | `SUBTASK_bar_ux`: screens owns `BAR-230..264` + the `bar-ux-screens.md` fragment |
| Release-bar partition | `../../../contracts/` (read-only) | `SUBTASK_release_bar`: UX owns `BAR-200..299` |
| DAG-root schema | `../../../../contracts/` (read-only) | `BAR-<NNN>` scheme, closed `verification_methods` vocab, stage vocab |

---

## Task Structure

### Overview

```
SUBTASK_bar_ux_screens/
├── _GLOBAL.md                          (this hub)
├── _BRIEF.md                           (my brief from the parent)
├── contracts/                          (READ-ONLY for descendants; sub-partitions BAR-230..264 additively)
│   ├── _MANIFEST.yaml
│   └── bar_screens_partition.yaml
├── SUBTASK_bar_screens_entry_auth/_BRIEF.md
├── SUBTASK_bar_screens_core_loop/_BRIEF.md
├── SUBTASK_bar_screens_social_profiles/_BRIEF.md
├── SUBTASK_bar_screens_account_lifecycle/_BRIEF.md
├── SUBTASK_bar_screens_safety_states/_BRIEF.md
├── SUBTASK_bar_screens_synthesis/_BRIEF.md
└── outputs/bar-ux-screens.md           (produced by SUBTASK_bar_screens_synthesis — SUBTASK_bar_ux_screens's declared output)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_bar_screens_entry_auth` | none | Author `BAR-230..237` enforcing each release-gating `REQ-UX-040..050` (Landing, sign-up, sign-in, recover access, set new credential, sign-out, per-screen empty/error/loading states, and the land-right / no-leak behaviour). | `SUBTASK_bar_screens_entry_auth/outputs/bar-screens-entry-auth.md` |
| `SUBTASK_bar_screens_core_loop` | none | Author `BAR-238..242` enforcing each release-gating `REQ-UX-051..056` (own+followed newest-first bounded timeline, catch-up, timeline states, 280-char compose limit, publish lock/confirm/keep-draft, one compose surface in three placements). | `SUBTASK_bar_screens_core_loop/outputs/bar-screens-core-loop.md` |
| `SUBTASK_bar_screens_social_profiles` | none | Author `BAR-243..247` enforcing each release-gating `REQ-UX-058..063` (reply-from-conversation incl. reply-to-gone, idempotent like toggle, idempotent follow w/ no self-follow; public profile, owner profile w/ edit entry, paginated followers/following lists). | `SUBTASK_bar_screens_social_profiles/outputs/bar-screens-social-profiles.md` |
| `SUBTASK_bar_screens_account_lifecycle` | none | Author `BAR-248..255` enforcing each release-gating `REQ-UX-065..077` (onboarding explains/never-dead-ends; edit-profile persistence + in-place validation; settings hub; contact control & verification; sessions & devices; server-side sign-out no-leak; data export; delete-account confirmation/consequence/retention + explicit-confirmation flow). | `SUBTASK_bar_screens_account_lifecycle/outputs/bar-screens-account-lifecycle.md` |
| `SUBTASK_bar_screens_safety_states` | none | Author `BAR-256..263` enforcing each release-gating `REQ-UX-079, 082..089` (report acknowledged; help & support from both shells; stated rules; not-found screen; and the cross-screen state patterns: considered states per surface, empty-explained, loading-shows-shape-never-forever, failures-at-point-of-action, expired-session/transient-error recovery without losing work). | `SUBTASK_bar_screens_safety_states/outputs/bar-screens-safety-states.md` |
| `SUBTASK_bar_screens_synthesis` | `SUBTASK_bar_screens_entry_auth`, `SUBTASK_bar_screens_core_loop`, `SUBTASK_bar_screens_social_profiles`, `SUBTASK_bar_screens_account_lifecycle`, `SUBTASK_bar_screens_safety_states` | **Verification gate + fold.** Assemble the five sub-fragments into `outputs/bar-ux-screens.md`; finalize the screens proposed stages into one coherent set; assert the sub-identities with recorded evidence (no silent plugs); mint cross-cutting `BAR-264` only for a finding no single chapter owns; build the whole coverage note; author `SYNTHESIS.md` and fold `SUBTASK_bar_ux_screens`. | `SUBTASK_bar_ux_screens/outputs/bar-ux-screens.md`, `SUBTASK_bar_ux_screens/SYNTHESIS.md` |

### Dependency Graph (the table above is authoritative)

```
bar_screens_entry_auth        ─┐
bar_screens_core_loop         ─┤
bar_screens_social_profiles   ─┼─> bar_screens_synthesis ─(fold)─> resumes SUBTASK_bar_ux_screens
bar_screens_account_lifecycle ─┤
bar_screens_safety_states     ─┘
```

---

## Contract

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` — extends the inherited `../../contracts/`, `../../../contracts/`, and
`../../../../contracts/` additively (sub-partitions the screens `BAR-230..264` range across the five chapter
spokes + the synthesis cross-cutting slot, and fixes the sub-fragment layout). It redefines nothing inherited.

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| DAG-root id/traceability schema | `../../../../contracts/` | `BAR-<NNN>` 3-digit format; the per-BAR field set; the closed `verification_methods` vocab; stage ∈ {`usable_early`, `releasable`} |
| `SUBTASK_release_bar` BAR partition | `../../../contracts/` | UX owns `BAR-200..299` |
| `SUBTASK_bar_ux` UX partition | `../../contracts/` | The screens slice owns `BAR-230..264` and the `bar-ux-screens.md` fragment; the `proposed_stage` convention; the bar-fragment + coverage-note layout |

### Structural Declarations
- `contracts/_MANIFEST.yaml` — kind, per-spoke ownership, the sub-identities the synthesis gate asserts, derived artifact.
- `contracts/bar_screens_partition.yaml` — the disjoint `BAR-*` sub-range per chapter spoke, the synthesis
  cross-cutting slot, the per-BAR field set (inherited), the sub-fragment layout each spoke emits, and the
  per-chapter release-gating `REQ-UX-*` set each spoke must cover.

### Ownership (one producer per artifact)

| Artifact | Owning subtask |
|----------|----------------|
| `SUBTASK_bar_screens_entry_auth/outputs/bar-screens-entry-auth.md` + `BAR-230..237` | `SUBTASK_bar_screens_entry_auth` |
| `SUBTASK_bar_screens_core_loop/outputs/bar-screens-core-loop.md` + `BAR-238..242` | `SUBTASK_bar_screens_core_loop` |
| `SUBTASK_bar_screens_social_profiles/outputs/bar-screens-social-profiles.md` + `BAR-243..247` | `SUBTASK_bar_screens_social_profiles` |
| `SUBTASK_bar_screens_account_lifecycle/outputs/bar-screens-account-lifecycle.md` + `BAR-248..255` | `SUBTASK_bar_screens_account_lifecycle` |
| `SUBTASK_bar_screens_safety_states/outputs/bar-screens-safety-states.md` + `BAR-256..263` | `SUBTASK_bar_screens_safety_states` |
| `outputs/bar-ux-screens.md` + `BAR-264` (cross-cutting) + `SYNTHESIS.md` | `SUBTASK_bar_screens_synthesis` |

### Identities (asserted by `SUBTASK_bar_screens_synthesis` with recorded evidence; no silent plugs)
1. **SCREENS_BAR_RANGE_RESPECTED** — every `BAR-NNN` lies within its owning spoke's assigned sub-range; all within `BAR-230..264`.
2. **SCREENS_NO_BAR_COLLISION** — all `BAR-NNN` ids across the five sub-fragments + the synthesis cross-cutting bar are distinct.
3. **SCREENS_GATING_REQ_COVERAGE** — every release-gating `REQ-UX-*` in 040..089 (43) is referenced by ≥1 `BAR-*`; evaluated per chapter against its gating set.
4. **SCREENS_BAR_TESTABLE** — every `BAR-*` names a `verification_method` from the frozen vocabulary and references ≥1 `REQ-*`.
5. **SCREENS_BAR_STAGED** — every `BAR-*` carries one stage ∈ {`usable_early`, `releasable`} (no criterion staged two ways); the screens-view proposal.
6. **SCREENS_NONGATING_EXCLUDED** — no `BAR-*` is justified solely by a non-gating `REQ-UX-*` (`057, 064, 071, 072, 078, 080, 081`).
7. **SCREENS_COVERAGE_NOTE_PRESENT** — `bar-ux-screens.md` carries the coverage note mapping every release-gating screens `REQ-UX-*` to the `BAR-*`(s) covering it.
8. **SCREENS_HYGIENE** — `bar-ux-screens.md` carries no host/system/taskflow detail and no attribution trailer.

### Derived Artifact
- **screens BAR↔REQ coverage map** — assembled by `SUBTASK_bar_screens_synthesis` from the five sub-fragments;
  is the coverage note in `bar-ux-screens.md` and feeds the parent `SUBTASK_bar_ux_synthesis` UX coverage map.

### Thin-Seam Note
The seam is not thin: a shared flat `BAR-230..264` id space with a tight budget (clustering required), a
per-chapter gating-coverage obligation, and one coherent per-`BAR-*` staging proposal are a rich contract. Spokes
MUST compose against `contracts/` and MUST NOT mint `BAR-*` outside their sub-range or redefine any inherited schema.

---

## Output Specifications

| Deliverable | Format | Location | Description |
|-------------|--------|----------|-------------|
| Screens release-bar fragment | Markdown | `SUBTASK_bar_ux_screens/outputs/bar-ux-screens.md` | The single assembled screens bar fragment (`BAR-230..264` blocks + coverage note), owned by `SUBTASK_bar_ux_screens` and consumed by the parent `SUBTASK_bar_ux_synthesis`. Repository-ready. |
| Fold record | Markdown | `SUBTASK_bar_ux_screens/SYNTHESIS.md` | The synthesis gate's fold record (identities asserted with evidence); taskflow-internal. |
