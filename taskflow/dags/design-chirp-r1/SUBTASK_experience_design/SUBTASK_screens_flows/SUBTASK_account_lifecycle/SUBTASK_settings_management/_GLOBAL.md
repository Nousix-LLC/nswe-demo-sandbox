# _GLOBAL.md — SUBTASK_settings_management (account-settings screens subtree hub)

## Project Context

**Status**: Active

### Objective

Design the **account-settings surfaces** a releasable chirp needs — the settings hub and the three
management sub-sections — each a **designed screen** with its layout, its content, its primary action,
and its **empty, error, and loading states**, to the bar *designed screens, not a skeleton*. This
subtree produces the `settings_management` part of the account-lifecycle deliverable
(`outputs/screens-settings-management.md`) and the `REQ-UX-069..074` register.

This node (`SUBTASK_settings_management`) evaluated its brief against the decomposition triggers and
found the work is **not atomic**: the **Scope-Based** trigger fires by the enumerated-concerns rule (the
brief enumerates four distinct surfaces that span separable concerns — a settings information
architecture / navigation hub, a verified-contact & identity surface, a notification-preferences
surface, and a session-security surface), and the **Output-Size** trigger is at its threshold (four
non-skeletal screens, each with three designed states, plus six traceable `REQ-UX` entries). It
therefore decomposes into four surface spokes and one synthesis gate. The "these are one coherent
settings cluster, one designer should hold it whole" instinct carries no weight at the evaluation point;
the fired scope trigger governs.

**This hub is this decomposing node's own `_GLOBAL.md`. The subtree above is `../_GLOBAL.md`
(account-lifecycle), then `../../_GLOBAL.md` (screens-&-flows), then `../../../_GLOBAL.md`
(experience-design), then `../../../../_GLOBAL.md` (the whole design). Every ancestor governs above this
one, and on any conflict the ancestor wins.**

### What this subtree designs into (grounding, from the dependencies)

chirp is a **hosted, public, account-based consumer web application** — a Twitter-style microblog. At
the current commit the live product offers **no way to change any account setting** — no settings hub,
no contact management, no notification preferences, no session/device management. These are among the
"unglamorous" surfaces a releasable account-based product is expected to have; their absence, not their
styling, is the defect this subtree closes. The settings surface is the home for the account-level
choices the recovery-contact (REQ-PROD-012), sign-out (REQ-PROD-014), and notifications (REQ-PROD-029)
requirements imply (REQ-PROD-017).

Two shared vocabularies are **already frozen upstream** and MUST NOT be redefined here — spokes compose
against them by name:

- the **Screen inventory** — the canonical screens, routes, archetypes, auth states, and the
  settings-as-secondary-nav / destructive-confirmation / sign-out conventions — in
  `SUBTASK_ia_interaction/outputs/ia-interaction.md` (under experience-design);
- the **Component library** — the named reusable components and their named states — in
  `SUBTASK_visual_system/outputs/visual-system.md` (under experience-design).

The authoritative upstream for journeys and requirements is
`SUBTASK_product_requirements/outputs/product-requirements.md` (personas P1–P5, journeys J1–J10, the
`REQ-PROD-001..042` register). Every `REQ-UX-*` this subtree mints MUST reference ≥1 `REQ-PROD-*`.

### Scope

**In scope (this subtree):** the `settings_management` part of the `account_lifecycle` section —
- **Settings hub** — the grouped settings surface (`/settings`, settings archetype) listing every
  sub-section, each addressable and each returning to the hub; links to sub-sections owned by sibling
  spokes/subtrees (edit profile; blocked & muted; export; delete) without designing their contents
  (J6 / REQ-PROD-017).
- **Account & contact** — view/update the verified point of contact with its control-you-own
  verification step, and state the product's handle-change position (`/settings/account`, settings
  archetype; J6 / REQ-PROD-017, 018, 012).
- **Notification preferences** — choose which activity categories (replies, follows, likes) send a
  notification; cross-reference, do not redesign, the notifications **activity** surface owned by
  `../../SUBTASK_safety_notifications` (`/settings/notifications`, settings archetype; J6 /
  REQ-PROD-017, 029).
- **Sessions & devices** — view active sessions/devices, end a session on another device (a confirmed,
  destructive action), and sign out (server-side session end) (`/settings/sessions`, settings archetype;
  J6 / REQ-PROD-017, 014).

Each surface is designed with its happy path **and** its empty/error/loading states, and
`REQ-UX-069..074` covers them.

**Out of scope (this subtree):**
- Front-end code or any implementation "how" — design only.
- The IA/screen inventory, the visual system/component library, the product-wide empty/error/loading
  **pattern** section (owned by `../../SUBTASK_considered_states`), responsive behavior, and the
  accessibility standard — compose against each and refer to it; do not redefine it or mint its ids.
- The **notifications activity surface** (Notifications, `/notifications`), **blocked & muted**, **edit
  profile**, **data export**, and **account deletion** — each owned by a sibling spoke or subtree. The
  Settings hub LINKS to the ones it lists; it does not design their contents.
- The credential / session / verification **mechanism** (identity design's `REQ-ID-*`). Design *what the
  person can see and do*, not how the secret or session works.
- `REQ-UX` ids outside `069..074`, and every other area's ids.
- Assembling the parent `screens-account-lifecycle.md` (the parent's `SUBTASK_synthesis`).

### Success Criteria (this subtree)
- [ ] `outputs/screens-settings-management.md` carries the `settings_management` part, each surface
      written by exactly one spoke, assembled in screen-inventory order (settings hub, account & contact,
      notification preferences, sessions & devices).
- [ ] Settings hub, Account & contact, Notification preferences, and Sessions & devices are each designed
      with their empty/error/loading states — or a state recorded "does not apply" with a reason only
      where the composed component itself records that state as not applying.
- [ ] Each screen specifies layout, content, and a primary action — not a bare route name; each
      sub-section is addressable and returns to the hub.
- [ ] Every `REQ-UX-069..074` is testable on the live product, `release_gating`-flagged, unique,
      in-range, and traces to ≥1 `REQ-PROD-*` (honouring REQ-PROD-018/029's non-gating staging).
- [ ] Every screen refers to the screen inventory and component library by name; nothing redefined; no
      new screen/component without an additive amendment to this subtree's `contracts/`.
- [ ] Repository-ready hygiene in the deliverable: no host/system/taskflow detail, no workspace paths, no
      agent/DAG/run ids, no attribution trailers.

---

## Constraints and Requirements

- **Design, not code.** State what each screen must show and do and what "done" looks like from the
  user's side; defer the build to later code DAGs.
- **Compose against the frozen vocabularies.** The screen inventory and the component library are inputs,
  not things to redesign. A screen is an arrangement of named components realising a named inventory
  screen; its states are the components' named states (`EmptyState`, `LoadingState`, `InlineError`,
  `InlineFeedback`, `SettingRow`/`Toggle`/`TextField`/`Dialog` states, etc.), not new inventions.
- **Compose against the contract.** This subtree's `contracts/` fixes the surface→owner map, the
  `REQ-UX-069..074` sub-range per spoke, the shared-vocabulary composition rule, the per-screen↔global-
  pattern cross-reference, and the per-`REQ-UX` trace rule; it extends the parent `../contracts/` and
  grandparents additively, never overriding them.
- **Align with identity & trust.** The settings surfaces align with the identity requirements — the
  verified contact (REQ-PROD-012), sign-out that ends the session server-side (REQ-PROD-014). Design
  *what the surface must let the person do and see*, not the credential/session mechanism (identity's
  `REQ-ID-*`).
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
| This subtree contract | `../contracts/` (read-only) | Surface→owner map, `REQ-UX-069..074` sub-ranges, identities, vocab + trace rules. |
| Screen inventory | `../../../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The settings screens/routes/archetypes, the settings-as-secondary-nav convention, destructive-confirmation convention, the sign-out transition. |
| Component library | `../../../../SUBTASK_visual_system/outputs/visual-system.md` | The named components (and their states) every screen is assembled from. |
| Product requirements | `../../../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Personas, journey J6, `REQ-PROD-012/014/017/018/029` the screens serve and trace to. |
| Account-lifecycle hub + contract | `../../_GLOBAL.md`, `../../contracts/` (read-only) | The `REQ-UX` scheme, field set, surface ownership, the `REQ-UX-069..074` range assigned to this node, the STATES_CONSISTENT cross-reference to `considered_states`. |

*(Paths are written from a spoke child's own workspace. The screen inventory, component library, and
product requirements are outputs of already-COMPLETED tasks; spokes read them directly as immutable
inputs and MUST NOT poll for or re-verify their existence.)*

---

## Task Structure

### Overview

```
SUBTASK_settings_management/
├── _GLOBAL.md                          (this hub)
├── contracts/                          (READ-ONLY for descendants — the internal seam)
│   ├── _MANIFEST.yaml                  (surface/id-range ownership, identities, derived register)
│   └── settings_management_seam.yaml   (surface→owner, REQ-UX-069..074 sub-ranges, vocab + trace rules)
├── SUBTASK_settings_hub/_BRIEF.md
├── SUBTASK_account_contact/_BRIEF.md
├── SUBTASK_notification_prefs/_BRIEF.md
├── SUBTASK_sessions_devices/_BRIEF.md
├── SUBTASK_synthesis/_BRIEF.md
└── outputs/
    └── screens-settings-management.md  (the deliverable — assembled by SUBTASK_synthesis)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_settings_hub` | none | Design the **Settings hub** (`/settings`, settings archetype) — the grouped surface that lists every sub-section (edit profile, account & contact, notification preferences, sessions & devices, blocked & muted, export, delete), each independently addressable and each returning to the hub, linking to sub-sections owned elsewhere without designing their contents — a designed screen with layout, content, primary action, and empty/error/loading states, composed against the screen inventory and component library. Bundles: Experience Design (primary); Product Strategy (support). Owns `REQ-UX-069`. | `outputs/screen-settings-hub.md` |
| `SUBTASK_account_contact` | none | Design **Account & contact** (`/settings/account`, settings archetype) — view/update the verified point of contact with its control-you-own verification step, and state the product's handle-change position — a designed screen with layout, content, primary action, and empty/error/loading states, aligned with the identity requirements (verified contact), designing what the person sees/does and not the verification mechanism. Bundles: Experience Design (primary); Identity & Trust, Product Strategy (support). Owns `REQ-UX-070..071`. | `outputs/screen-account-contact.md` |
| `SUBTASK_notification_prefs` | none | Design **Notification preferences** (`/settings/notifications`, settings archetype) — choose which activity categories (replies, follows, likes) send a notification, cross-referencing but not redesigning the notifications activity surface owned by the sibling safety_notifications — a designed screen with layout, content, primary action, and empty/error/loading states, composed against the screen inventory and component library. Bundles: Experience Design (primary); Product Strategy (support). Owns `REQ-UX-072`. | `outputs/screen-notification-prefs.md` |
| `SUBTASK_sessions_devices` | none | Design **Sessions & devices** (`/settings/sessions`, settings archetype) — view active sessions/devices, end a session on another device (a confirmed, destructive action), and sign out (server-side session end) — a designed screen with layout, content, primary action, and empty/error/loading states, aligned with the identity requirements (sign-out that ends the session), designing what the person sees/does and not the session mechanism. Bundles: Experience Design (primary); Identity & Trust (support). Owns `REQ-UX-073..074`. | `outputs/screen-sessions-devices.md` |
| `SUBTASK_settings_management_synthesis` (workspace `SUBTASK_synthesis/`) | `SUBTASK_settings_hub`, `SUBTASK_account_contact`, `SUBTASK_notification_prefs`, `SUBTASK_sessions_devices` | **Verification gate + fold.** Assemble the four spoke outputs into `../outputs/screens-settings-management.md` (the `settings_management` part, surfaces in inventory order); consolidate the `REQ-UX-069..074` register; assert this subtree's identities with recorded evidence (surface coverage & single owner, id uniqueness/range, each screen not-skeletal, every REQ-UX testable + gated + traced, composed against the frozen vocabularies, states consistent with the components' named states, hygiene); remediate a fixable gap by decomposing a remediation subtree, never a silent plug; author `../SYNTHESIS.md` and fold this node to COMPLETED. Bundle: Experience Design. | `../outputs/screens-settings-management.md` + `../SYNTHESIS.md` |

### Dependency Graph (human-readable; the table above is authoritative)

```
settings_hub ───────┐
account_contact ────┤
notification_prefs ─┼─> synthesis
sessions_devices ───┘
```

---

## Contract

The two co-designed outputs of this decomposition are the task tree above and the contract in
`contracts/`. The four spokes are parts of ONE account-settings design and share a real seam: one output
part (`settings_management`) split across the spokes, one `REQ-UX-069..074` id space that must stay
collision-free and `REQ-PROD`-traceable, one surface checklist that must be fully covered, two frozen
upstream vocabularies every spoke composes against, and a cross-reference to the product-wide
empty/error/loading **patterns** (owned by `../../SUBTASK_considered_states`) that each screen's own
states must stay consistent with. The settings hub additionally references its sub-sections by name
(including ones owned by siblings) without designing them. That seam is frozen before any spoke runs.

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` (surface→owner map + `REQ-UX-069..074` sub-range partition + identities),
extending the parent `../contracts/` and grandparent `../../contracts/` additively — never overriding them.

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| Account-lifecycle seam | `../contracts/` | The `settings_management` surfaces and the `REQ-UX-069..074` range assigned to this node; the surface→owner map; the shared-vocabulary composition rule; the per-`REQ-UX` trace rule; the STATES_CONSISTENT cross-reference to `considered_states`. |
| Screens-&-flows seam | `../../contracts/` | The `account_lifecycle` part of `screens_and_flows`; the surface map; the per-`REQ-UX` trace rule. |
| Experience-design seam | `../../../contracts/` | The `REQ-UX-NNN` format and field set; the `experience-design.md` section list; the `required_surfaces` checklist. |

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/_MANIFEST.yaml` | `yaml_schema` | kind, per-spoke ownership of surfaces / id sub-ranges, the identities synthesis asserts, the derived register. |
| `contracts/settings_management_seam.yaml` | `yaml_schema` | the surface→owning-spoke map (all four surfaces), the `REQ-UX-069..074` sub-range per spoke, the shared-vocabulary composition rule, the per-`REQ-UX` trace rule, and the sub-section link list the hub references. |

### Ownership (one producer per surface / id sub-range)

| Surface / id sub-range | Owning spoke |
|---|---|
| Settings hub + `REQ-UX-069` | `SUBTASK_settings_hub` |
| Account & contact + `REQ-UX-070..071` | `SUBTASK_account_contact` |
| Notification preferences + `REQ-UX-072` | `SUBTASK_notification_prefs` |
| Sessions & devices + `REQ-UX-073..074` | `SUBTASK_sessions_devices` |
| assembled `outputs/screens-settings-management.md`, consolidated `REQ-UX-069..074` register, `../SYNTHESIS.md` | `SUBTASK_synthesis` |

### Identities (asserted by `SUBTASK_synthesis` with recorded evidence; no silent plugs)
1. **SURFACE_COVERAGE** — each of the four owned surfaces (Settings hub, Account & contact, Notification
   preferences, Sessions & devices) is designed with its empty/error/loading states by its owning spoke,
   OR a state is recorded "does not apply" with a reason that matches the composed component's own
   not-applicable decision.
2. **ID_UNIQUE_IN_RANGE** — every `REQ-UX-069..074` id is unique and within its owning spoke's sub-range;
   no collisions, no out-of-range ids, no gaps claimed as covered.
3. **NOT_SKELETAL** — each designed screen specifies layout, content, and a primary action, and its
   empty, error, and loading states — not a bare route name.
4. **UX_TESTABLE_AND_GATED** — every `REQ-UX-*` has a `statement`, an `acceptance_criteria` a stranger
   could check on the live product, and a `release_gating` flag (with a one-line reason when `false`).
5. **UX_TRACES_TO_PROD** — every `REQ-UX-*` references ≥1 `REQ-PROD-*`.
6. **COMPOSES_AGAINST_VOCAB** — every screen refers to screen-inventory screens by name and is built from
   component-library components by name; nothing redefined; no new screen/component without an additive
   amendment to this subtree's `contracts/`.
7. **STATES_CONSISTENT** — each per-screen empty/error/loading state is consistent with the components'
   own named states and with the product-wide patterns owned by `../../SUBTASK_considered_states`.
8. **HYGIENE** — nothing in `screens-settings-management.md` carries host/system/taskflow detail,
   workspace paths, agent/DAG/run ids, or an attribution trailer.

### Derived Artifacts

- Consolidated `REQ-UX-069..074` register — assembled by `SUBTASK_synthesis` from the four spokes'
  REQ-UX entries; consumed by the parent `SUBTASK_synthesis` (account-lifecycle) when it builds the
  consolidated `REQ-UX-065..077` register.
- `outputs/screens-settings-management.md` — assembled by `SUBTASK_synthesis` from the four spoke screen
  parts in screen-inventory order plus the consolidated REQ-UX register; consumed by the parent
  account-lifecycle synthesis as the `settings_management` section-part.

### Thin-Seam Note

The seam is real, not thin: one output part split four ways, a partitioned 6-id space, a four-surface
checklist, two frozen vocabularies, a per-screen↔global-pattern cross-reference, and the hub's reference
to sibling-owned sub-sections. Spokes MUST compose against `contracts/` and MUST NOT redefine the
`REQ-UX` scheme, the id ranges, the surface map, or the shared vocabularies.

---

## Output Specifications

| Deliverable | Format | Location | Description |
|-------------|--------|----------|-------------|
| Settings hub screen | Markdown | `SUBTASK_settings_hub/outputs/screen-settings-hub.md` | Designed screen + `REQ-UX-069`. |
| Account & contact screen | Markdown | `SUBTASK_account_contact/outputs/screen-account-contact.md` | Designed screen + `REQ-UX-070..071`. |
| Notification preferences screen | Markdown | `SUBTASK_notification_prefs/outputs/screen-notification-prefs.md` | Designed screen + `REQ-UX-072`. |
| Sessions & devices screen | Markdown | `SUBTASK_sessions_devices/outputs/screen-sessions-devices.md` | Designed screen + `REQ-UX-073..074`. |
| Assembled deliverable | Markdown | `outputs/screens-settings-management.md` | The `settings_management` part + the consolidated `REQ-UX-069..074` register. |
| Fold record | Markdown | `SYNTHESIS.md` | Identity evidence and the fold of this node. |

### Output Quality Criteria

- [ ] Each screen is designed (layout, content, primary action, empty/error/loading states), not skeletal.
- [ ] Every owned surface is covered; any "does not apply" state carries a reason matching the component.
- [ ] Every `REQ-UX-069..074` is testable, gated, traced, unique, and in-range.
- [ ] Everything composes against the frozen vocabularies by name.
- [ ] Repository-ready hygiene throughout the deliverable.
