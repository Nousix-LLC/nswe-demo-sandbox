# _GLOBAL.md — SUBTASK_account_lifecycle (account-lifecycle screens subtree hub)

## Project Context

**Status**: Active

### Objective

Design the **account-lifecycle surfaces** a releasable chirp needs — the surfaces that make the account
feel like the person's own, and let them leave cleanly: first-run onboarding off the empty timeline,
editing the profile, the settings hub and its sub-sections (account & contact, notification preferences,
sessions & devices), exporting one's data, and deleting the account with a confirmed, explained outcome.
Each is a **designed screen** — its layout, its content, its primary action, and its **empty, error, and
loading states** — to the bar *designed screens, not a skeleton*. This subtree produces the
`account_lifecycle` part of the screens-&-flows deliverable (`outputs/screens-account-lifecycle.md`) and
the `REQ-UX-065..077` register.

This node (`SUBTASK_account_lifecycle`) evaluated its brief against the decomposition triggers and found
the work is not atomic: the **Output Size** trigger fires (eight non-skeletal screens, each with three
designed states, plus thirteen traceable `REQ-UX` entries, is a >400-line deliverable) and the
**Scope-Based** trigger fires by the enumerated-concerns rule (the brief enumerates eight distinct
surfaces spanning separable concerns — a first-run experience, settings information architecture, the
verified contact and identity, session security, data portability, and destructive deletion). It
therefore decomposes into three surface-cluster spokes and one synthesis gate.

**This hub is this decomposing node's own `_GLOBAL.md`. The subtree above is `../_GLOBAL.md`
(screens-&-flows), then `../../_GLOBAL.md` (experience-design), then `../../../_GLOBAL.md` (the whole
design). Every ancestor governs above this one, and on any conflict the ancestor wins.**

### What this subtree designs into (grounding, from the dependencies)

chirp is a **hosted, public, account-based consumer web application** — a Twitter-style microblog. At the
current commit the live product presents only three screens (timeline, a compose+sign-in view, a profile)
above a persistent nav bar, and offers **no way to edit a profile, change any setting, export one's data,
or delete one's account** — the gaps this subtree's surfaces close. These are the "unglamorous" surfaces a
releasable account-based product is expected to have; their absence, not their styling, is the defect.

Two shared vocabularies are **already frozen upstream** and MUST NOT be redefined here — spokes compose
against them by name:

- the **Screen inventory** — the canonical screens, routes, archetypes, and auth states — in
  `../../SUBTASK_ia_interaction/outputs/ia-interaction.md`;
- the **Component library** — the named reusable components and their named states — in
  `../../SUBTASK_visual_system/outputs/visual-system.md`.

The authoritative upstream for journeys and requirements is
`../../../SUBTASK_product_requirements/outputs/product-requirements.md` (personas P1–P5, journeys J1–J10,
the `REQ-PROD-001..042` register). Every `REQ-UX-*` this subtree mints MUST reference ≥1 `REQ-PROD-*`.

### Scope

**In scope (this subtree):** the `account_lifecycle` part of the `screens_and_flows` section —
- **Onboarding** — first-run off the empty timeline (J5 / REQ-PROD-032).
- **Edit profile** — change display name and bio after sign-up (J6 / REQ-PROD-016).
- **Settings hub** — the grouped settings surface listing its sub-sections, each addressable and
  returnable (J6 / REQ-PROD-017).
- **Account & contact** — view/update the verified contact; the stated handle-change position (J6 /
  REQ-PROD-017,018).
- **Notification preferences** — choose which activity categories notify (J6 / REQ-PROD-017,029).
- **Sessions & devices** — view active sessions, end a session, sign out (J6 / REQ-PROD-017,014).
- **Data export** — obtain one's own data in a portable form (J8 / REQ-PROD-019).
- **Account deletion** — delete with a confirmation that names the consequence, states what is/is not
  retained, and points to export first (J8 / REQ-PROD-020,021,022).

Each surface is designed with its happy path **and** its empty/error/loading states, and `REQ-UX-065..077`
covers them.

**Out of scope (this subtree):**
- Front-end code or any implementation "how" — design only.
- The IA/screen inventory, the visual system/component library, the product-wide empty/error/loading
  **pattern** section (owned by the sibling `../SUBTASK_considered_states`), responsive behavior, and the
  accessibility standard — compose against each and refer to it; do not redefine it or mint its ids. The
  **notifications activity surface** itself is owned by `../SUBTASK_safety_notifications`; this subtree
  owns only the notification *preferences* settings sub-section and cross-references the activity surface.
- `REQ-UX` ids outside `065..077`, and every other area's ids.
- Assembling the parent `screens-flows.md` (the parent's `SUBTASK_synthesis`).

### Success Criteria (this subtree)
- [ ] `outputs/screens-account-lifecycle.md` carries the `account_lifecycle` part, each surface written by
      exactly one spoke, assembled in order.
- [ ] Onboarding, edit profile, settings hub, account & contact, notification preferences, sessions &
      devices, export, and deletion are each designed with their empty/error/loading states — or recorded
      out-of-scope with a reason.
- [ ] Each screen specifies layout, content, and a primary action — not a bare route name.
- [ ] Every `REQ-UX-065..077` is testable on the live product, `release_gating`-flagged, unique,
      in-range, and traces to ≥1 `REQ-PROD-*` (honouring REQ-PROD-018/029's non-gating staging).
- [ ] Every screen refers to the screen inventory and component library by name; nothing redefined; no new
      screen/component without an additive amendment to this subtree's `contracts/`.
- [ ] Repository-ready hygiene in `screens-account-lifecycle.md`: no host/system/taskflow detail, no
      workspace paths, no agent/DAG/run ids, no attribution trailers.

---

## Constraints and Requirements

- **Design, not code.** State what each screen must show and do and what "done" looks like from the
  user's side; defer the build to later code DAGs.
- **Compose against the frozen vocabularies.** The screen inventory and the component library are inputs,
  not things to redesign. A screen is an arrangement of named components realising a named inventory
  screen; its states are the components' named states (`EmptyState`, `LoadingState`, `InlineError`,
  `SettingRow`/`ListView`/`Dialog` states, etc.), not new inventions.
- **Compose against the contract.** The parent `../contracts/` fixes the `REQ-UX` format, field set,
  surface→owner map, and trace rule; this subtree's `contracts/` only sub-ranges `065..077` among the
  spokes and maps this subtree's surfaces to owners, extending the parent additively, never overriding it.
- **Align with identity & trust.** The auth/account surfaces align with the identity requirements — the
  verified contact (REQ-PROD-012), sign-out that ends the session (REQ-PROD-014), and the defined
  deletion outcome (REQ-PROD-021). Design *what the surface must let the person do and see*, not the
  credential/session mechanism (that is the identity design's `REQ-ID-*`).
- **Methodology posture.** The Phase-B `design` methodology loader is **unavailable in the current
  reconstructed environment** (the loader syscall reports the agent domain unset). Per the ancestor hubs'
  recorded posture, each spoke designs from the named bundle intent — **Experience Design** (primary);
  **Identity & Trust** and **Product Strategy** (support) — and its own product-design competence, and
  records the limitation; it does not block.
- **Plain, checkable human voice.** Narrative output is written plainly; run the `avoid-ai-writing`
  checklist (or the P0/P1 machine-writing catalog by hand when the skill is absent — it is absent in this
  environment) over every narrative deliverable before finalizing, and record the limitation.

---

## Input Specifications

| Source | Identity (from a spoke's view) | Role |
|--------|--------------------------------|------|
| This subtree hub | `../_GLOBAL.md` | Shared context, constraints, the contract pointer, hygiene. |
| This subtree contract | `../contracts/` (read-only) | Surface→owner map, `REQ-UX-065..077` sub-ranges, identities, trace rule. |
| Screen inventory | `../../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The canonical screens/routes/archetypes/auth states every spoke designs into. |
| Component library | `../../../SUBTASK_visual_system/outputs/visual-system.md` | The named components (and their states) every screen is assembled from. |
| Product requirements | `../../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Personas, journeys J5/J6/J8, `REQ-PROD-*` the screens serve and trace to. |
| Screens-&-flows hub + contract | `../../_GLOBAL.md`, `../../contracts/` (read-only) | The `REQ-UX` scheme, field set, surface ownership, trace rule, the `account_lifecycle` id range `065..077`. |

*(Paths are written from a spoke child's own workspace. The screen inventory, component library, and
product requirements are outputs of already-COMPLETED tasks; spokes read them directly as immutable inputs
and MUST NOT poll for or re-verify their existence.)*

---

## Task Structure

### Overview

```
SUBTASK_account_lifecycle/
├── _GLOBAL.md                         (this hub)
├── contracts/                         (READ-ONLY for descendants — the internal seam)
│   ├── _MANIFEST.yaml                 (surface/id-range ownership, identities, derived register)
│   └── account_lifecycle_seam.yaml    (surface→owner, REQ-UX-065..077 sub-ranges, shared-vocab + trace rules)
├── SUBTASK_onboarding_profile/_BRIEF.md
├── SUBTASK_settings_management/_BRIEF.md
├── SUBTASK_leaving/_BRIEF.md
├── SUBTASK_synthesis/_BRIEF.md
└── outputs/
    └── screens-account-lifecycle.md   (the deliverable — assembled by SUBTASK_synthesis)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_onboarding_profile` | none | Design the two first-run / self-presentation surfaces — **Onboarding** (first run off the empty timeline, explaining the empty state and offering at least one route to a non-empty one) and **Edit profile** (change display name and bio after sign-up) — each a designed screen with its layout, content, primary action, and empty/error/loading states, composed against the screen inventory and component library. Bundles: Experience Design (primary); Product Strategy, Identity & Trust (support). Owns `REQ-UX-065..068`. | `outputs/screens-onboarding-profile.md` |
| `SUBTASK_settings_management` | none | Design the **account-settings** surfaces — the **Settings hub** (grouped, each sub-section addressable and returnable), **Account & contact** (view/update the verified contact; the stated handle-change position), **Notification preferences** (choose which activity categories notify; cross-reference, do not redesign, the notifications activity surface owned elsewhere), and **Sessions & devices** (view active sessions, end a session, sign out) — each a designed screen with its layout, content, primary action, and empty/error/loading states, composed against the screen inventory and component library and aligned with the identity requirements (verified contact, session end). Bundles: Experience Design (primary); Identity & Trust, Product Strategy (support). Owns `REQ-UX-069..074`. | `outputs/screens-settings-management.md` |
| `SUBTASK_leaving` | none | Design the two **leaving** surfaces — **Data export** (request and obtain one's own data — chirps, profile, follows — in a portable form) and **Account deletion** (delete with a confirmation that names the consequence, states what is and is not retained per the defined deletion outcome, and points to export first) — each a designed screen with its layout, content, primary action, and empty/error/loading states, composed against the screen inventory and component library and aligned with the identity/privacy requirements. Bundles: Experience Design (primary); Identity & Trust, Product Strategy (support). Owns `REQ-UX-075..077`. | `outputs/screens-leaving.md` |
| `SUBTASK_synthesis` | `SUBTASK_onboarding_profile`, `SUBTASK_settings_management`, `SUBTASK_leaving` | **Verification gate + fold.** Assemble the three spoke outputs into `../outputs/screens-account-lifecycle.md` (the `account_lifecycle` part, surfaces in inventory order); consolidate the `REQ-UX-065..077` register; assert this subtree's identities with recorded evidence (surface coverage & single owner, id uniqueness/range, each screen not-skeletal, every REQ-UX testable + gated + traced, composed against the frozen vocabularies, states consistent with the components' named states, hygiene); remediate a fixable gap by decomposing a remediation subtree, never a silent plug; author `../SYNTHESIS.md` and fold this node to COMPLETED. Bundle: Experience Design. | `../outputs/screens-account-lifecycle.md` + `../SYNTHESIS.md` |

### Dependency Graph (human-readable; the table above is authoritative)

```
onboarding_profile ──┐
settings_management ─┼─> synthesis
leaving ─────────────┘
```

---

## Contract

The two co-designed outputs of this decomposition are the task tree above and the contract in
`contracts/`. The three spokes are parts of ONE account-lifecycle design and share a real seam: one output
part (`account_lifecycle`) split across the spokes, one `REQ-UX-065..077` id space that must stay
collision-free and `REQ-PROD`-traceable, one surface checklist that must be fully covered, two frozen
upstream vocabularies every spoke composes against, and a cross-reference to the product-wide
empty/error/loading **patterns** (owned by the sibling `../SUBTASK_considered_states`) that each screen's
own states must stay consistent with. That seam is frozen before any spoke runs.

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` (surface→owner map + `REQ-UX-065..077` sub-range partition + identities),
extending the parent `../contracts/` and grandparent `../../contracts/` additively — never overriding them.

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| Screens-&-flows seam | `../../contracts/` | The `account_lifecycle` part of `screens_and_flows`; the `REQ-UX-065..077` range assigned to this node; the surface→owner map (this node owns onboarding, edit profile, settings cluster, export, deletion); the shared-vocabulary composition rule; the per-`REQ-UX` trace rule; the STATES_CONSISTENT cross-reference to `considered_states`. |
| Experience-design seam | `../../../contracts/` | The `REQ-UX-NNN` format and field set; the `experience-design.md` section list; the `required_surfaces` checklist. |

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/_MANIFEST.yaml` | `yaml_schema` | kind, per-spoke ownership of surfaces / id sub-ranges, the identities synthesis asserts, the derived register. |
| `contracts/account_lifecycle_seam.yaml` | `yaml_schema` | the surface→owning-spoke map (covering all eight surfaces), the `REQ-UX-065..077` sub-range per spoke, the shared-vocabulary composition rule, and the per-`REQ-UX` trace rule. |

### Ownership (one producer per surface cluster / id range)

| Surfaces / id range | Owning spoke |
|---|---|
| Onboarding, Edit profile + `REQ-UX-065..068` | `SUBTASK_onboarding_profile` |
| Settings hub, Account & contact, Notification preferences, Sessions & devices + `REQ-UX-069..074` | `SUBTASK_settings_management` |
| Data export, Account deletion + `REQ-UX-075..077` | `SUBTASK_leaving` |
| assembled `outputs/screens-account-lifecycle.md`, consolidated `REQ-UX-065..077` register, `../SYNTHESIS.md` | `SUBTASK_synthesis` |

### Identities (asserted by `SUBTASK_synthesis` with recorded evidence; no silent plugs)
1. **SURFACE_COVERAGE** — each of the eight owned surfaces is designed with its empty/error/loading states
   by its owning spoke, OR recorded out-of-scope with a reason.
2. **ID_UNIQUE_IN_RANGE** — every `REQ-UX-065..077` id is unique and within its owning spoke's sub-range;
   no collisions, no out-of-range ids, no gaps claimed as covered.
3. **NOT_SKELETAL** — each designed screen specifies layout, content, and a primary action, and its empty,
   error, and loading states — not a bare route name.
4. **UX_TESTABLE_AND_GATED** — every `REQ-UX-*` has a `statement`, an `acceptance_criteria` a stranger
   could check on the live product, and a `release_gating` flag (with a one-line reason when `false`).
5. **UX_TRACES_TO_PROD** — every `REQ-UX-*` references ≥1 `REQ-PROD-*`.
6. **COMPOSES_AGAINST_VOCAB** — every screen refers to screen-inventory screens by name and is built from
   component-library components by name; nothing redefined; no new screen/component without an additive
   amendment to this subtree's `contracts/`.
7. **STATES_CONSISTENT** — each per-screen empty/error/loading state is consistent with the components'
   own named states and with the product-wide patterns owned by `../SUBTASK_considered_states`.
8. **HYGIENE** — nothing in `screens-account-lifecycle.md` carries host/system/taskflow detail, workspace
   paths, agent/DAG/run ids, or an attribution trailer.

### Derived Artifacts

- Consolidated `REQ-UX-065..077` register — assembled by `SUBTASK_synthesis` from the three spokes' REQ-UX
  entries; consumed by the parent `SUBTASK_synthesis` (screens-&-flows) when it builds the full
  `REQ-UX-040..089` register.

### Thin-Seam Note

The seam is real, not thin: one output part split three ways, a partitioned 13-id space, an eight-surface
checklist, two frozen vocabularies, and a per-screen↔global-pattern cross-reference. Spokes MUST compose
against `contracts/` and MUST NOT redefine the `REQ-UX` scheme, the id ranges, the surface map, or the
shared vocabularies.

---

## Output Specifications

| Deliverable | Format | Location | Description |
|-------------|--------|----------|-------------|
| Onboarding + Edit-profile screens | Markdown | `SUBTASK_onboarding_profile/outputs/screens-onboarding-profile.md` | Designed screens + `REQ-UX-065..068`. |
| Account-settings screens | Markdown | `SUBTASK_settings_management/outputs/screens-settings-management.md` | Designed screens + `REQ-UX-069..074`. |
| Leaving (export + deletion) screens | Markdown | `SUBTASK_leaving/outputs/screens-leaving.md` | Designed screens + `REQ-UX-075..077`. |
| Assembled deliverable | Markdown | `outputs/screens-account-lifecycle.md` | The `account_lifecycle` part + the consolidated `REQ-UX-065..077` register. |
| Fold record | Markdown | `SYNTHESIS.md` | Identity evidence and the fold of this node. |

### Output Quality Criteria

- [ ] Each screen is designed (layout, content, primary action, empty/error/loading states), not skeletal.
- [ ] Every owned surface is covered or recorded out-of-scope with a reason.
- [ ] Every `REQ-UX-065..077` is testable, gated, traced, unique, and in-range.
- [ ] Everything composes against the frozen vocabularies by name.
- [ ] Repository-ready hygiene throughout the deliverable.
