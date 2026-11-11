# Traceability-matrix skeleton — design-side columns for REQ-UX-*

Design-side slice of the whole-DAG traceability matrix, owned by `SUBTASK_matrix_ux`. One row per
`REQ-UX-*` defined in the experience design, carrying the three design-side columns the sub-contract
assigns to this spoke: `req_id`, `release_gating`, `design_doc_ref`. This slice computes no `bar_ids`,
`epic`, or `issue_numbers`, and asserts no identity; the synthesis child joins it with the other slices
on `req_id`.

## Source and method

- **Source**: `design/experience-design.md` (owner `SUBTASK_experience_design`), the single experience-area
  design file. Read-only; no finding was written back to it.
- **Where the requirements are defined**: the section `## Requirements and acceptance criteria`. Each
  requirement is one `#### REQ-UX-NNN — <title>` heading carrying `- **statement**`,
  `- **acceptance_criteria**`, `- **release_gating**: true|false`, and `- **references**`.
- **`release_gating`**: taken verbatim from each requirement's `- **release_gating**:` field. A `false`
  value in the source carries a stated reason; those reasons are preserved verbatim in the
  "Non-gating requirements" section below (the matrix column itself holds only the boolean).
- **`design_doc_ref`**: the repo-relative design path from `design_artifact_map.yaml`
  (`design/experience-design.md`) plus the requirement's own section — its `#### REQ-UX-NNN — <title>`
  heading under `## Requirements and acceptance criteria`. For brevity the common prefix
  `design/experience-design.md § Requirements and acceptance criteria › ` is stated once here and each
  row's `design_doc_ref` is the heading it points to; the full reference is the prefix joined to the row
  value.
- **`req_id`**: the inherited `REQ-UX-NNN` strings verbatim (zero-padded three digits), per
  `id_and_traceability_schema.yaml`. No renamed scheme; no row for an id the source does not define.

## Count and anomalies

- **Requirements found: 119**, ids contiguous from `REQ-UX-001` to `REQ-UX-119`. The source's own register
  intro states the same ("Ids are unique and contiguous from `REQ-UX-001` to `REQ-UX-119`").
- **Count discrepancy to surface for synthesis**: the subtree hub `_GLOBAL.md` and the inherited counts cite
  ~153 `REQ-UX-*`. The experience design as delivered defines **119**, not 153. This slice reports the
  actual count in the source; the 153 figure is not grounded in `design/experience-design.md` as delivered.
  Flagged here, not reconciled.
- **No `release_gating` defects**: every one of the 119 requirements carries a well-formed
  `- **release_gating**: true|false` field. None is absent, none is malformed; nothing was guessed.
- **Gating split**: 106 `true`, 13 `false`.

## Skeleton rows (design-side columns)

`design_doc_ref` prefix (common to every row): `design/experience-design.md § Requirements and acceptance criteria › `

| req_id | release_gating | design_doc_ref (heading under the prefix above) |
|--------|----------------|--------------------------------------------------|
| REQ-UX-001 | true | REQ-UX-001 — A signed-out shell that explains chirp and never dead-ends |
| REQ-UX-002 | true | REQ-UX-002 — A signed-in shell exposing every primary destination |
| REQ-UX-003 | true | REQ-UX-003 — The current location is always indicated |
| REQ-UX-004 | true | REQ-UX-004 — The product is built from the published screen inventory |
| REQ-UX-005 | true | REQ-UX-005 — Every required surface is reachable without an external link |
| REQ-UX-006 | true | REQ-UX-006 — Profiles and chirps are addressable and shareable |
| REQ-UX-007 | true | REQ-UX-007 — Auth-gated routing returns the person to where they asked to go |
| REQ-UX-008 | true | REQ-UX-008 — An expired session is intercepted, explained, and recovered from |
| REQ-UX-009 | true | REQ-UX-009 — Browser back and forward behave predictably |
| REQ-UX-010 | true | REQ-UX-010 — Lists load in bounded pages with a catch-up affordance |
| REQ-UX-011 | true | REQ-UX-011 — Destructive actions are confirmed before they proceed |
| REQ-UX-012 | true | REQ-UX-012 — The result of every action is shown |
| REQ-UX-013 | true | REQ-UX-013 — Compose is reachable from anywhere, and addressable |
| REQ-UX-014 | true | REQ-UX-014 — Sign-up lands a new account in the product, onboarding first |
| REQ-UX-015 | false | REQ-UX-015 — Sign-in, sign-up, and recovery are interlinked |
| REQ-UX-016 | true | REQ-UX-016 — Sign-out returns to the signed-out shell and does not leak back |
| REQ-UX-017 | true | REQ-UX-017 — Settings groups account-level choices, each addressable |
| REQ-UX-018 | true | REQ-UX-018 — The rules and a help entry are reachable from both shells |
| REQ-UX-019 | false | REQ-UX-019 — A notifications entry with an unseen-activity indicator |
| REQ-UX-020 | true | REQ-UX-020 — The product reads as one product across screens |
| REQ-UX-021 | true | REQ-UX-021 — Text is legible and hierarchy is clear |
| REQ-UX-022 | true | REQ-UX-022 — Colour contrast meets WCAG 2.1 AA |
| REQ-UX-023 | false | REQ-UX-023 — A light theme and a dark theme, at parity |
| REQ-UX-024 | false | REQ-UX-024 — The theme follows the reader's preference and persists |
| REQ-UX-025 | true | REQ-UX-025 — Every interactive element has a visible focus indicator |
| REQ-UX-026 | true | REQ-UX-026 — Consistent spacing, grid, and reading measure |
| REQ-UX-027 | true | REQ-UX-027 — Layers stack in a consistent, legible order |
| REQ-UX-028 | true | REQ-UX-028 — Icons are consistent and never the sole carrier of meaning |
| REQ-UX-029 | true | REQ-UX-029 — Motion is purposeful, bounded, and respects reduced-motion |
| REQ-UX-030 | false | REQ-UX-030 — People are shown consistently, and a missing picture is never broken |
| REQ-UX-031 | true | REQ-UX-031 — Empty, loading, and error states have a designed visual treatment |
| REQ-UX-032 | true | REQ-UX-032 — A consistent voice, with plain and actionable errors |
| REQ-UX-033 | true | REQ-UX-033 — Screens are built from the named component vocabulary, not one-off controls |
| REQ-UX-034 | true | REQ-UX-034 — Every component is built from the published design tokens |
| REQ-UX-035 | true | REQ-UX-035 — The chirp card and compose box behave to the product's core-loop contract |
| REQ-UX-036 | true | REQ-UX-036 — Every list has designed empty, loading, and load-failure states |
| REQ-UX-037 | true | REQ-UX-037 — Forms validate inline at the field level, in plain language |
| REQ-UX-038 | true | REQ-UX-038 — Consequential actions are confirmed through the dialog confirmation variant |
| REQ-UX-039 | true | REQ-UX-039 — The result of every action is shown through the feedback components |
| REQ-UX-040 | true | REQ-UX-040 — A first-visit Landing that explains chirp without an account |
| REQ-UX-041 | true | REQ-UX-041 — Sign-up creates an account from only what it needs |
| REQ-UX-042 | true | REQ-UX-042 — Handle format and uniqueness are reported against the field |
| REQ-UX-043 | true | REQ-UX-043 — Sign-up captures a contact to be verified |
| REQ-UX-044 | true | REQ-UX-044 — Sign-in proves the account is the person's own |
| REQ-UX-045 | true | REQ-UX-045 — Sign-in distinguishes no-such-account from wrong-credential |
| REQ-UX-046 | true | REQ-UX-046 — Recover access starts self-service recovery through the verified contact |
| REQ-UX-047 | true | REQ-UX-047 — Set new credential completes recovery and returns to sign-in |
| REQ-UX-048 | true | REQ-UX-048 — Sign-out confirmation ends the session, optionally on all devices |
| REQ-UX-049 | true | REQ-UX-049 — Each entry/auth screen has designed empty, error, and loading states |
| REQ-UX-050 | true | REQ-UX-050 — The entry/auth screens land the person on the right place and do not leak back |
| REQ-UX-051 | true | REQ-UX-051 — The home timeline reads own and followed chirps, newest first, in bounded pages |
| REQ-UX-052 | true | REQ-UX-052 — A catch-up affordance brings in chirps posted since the last look |
| REQ-UX-053 | true | REQ-UX-053 — The timeline has designed empty, error, and loading states |
| REQ-UX-054 | true | REQ-UX-054 — The 280-character limit is enforced while composing, before submission |
| REQ-UX-055 | true | REQ-UX-055 — Publishing locks against double-posting, confirms on success, and keeps the draft on failure |
| REQ-UX-056 | true | REQ-UX-056 — One compose surface in three placements, with a context-labelled action and an empty state |
| REQ-UX-057 | false | REQ-UX-057 — A chirp is read in the conversation it belongs to |
| REQ-UX-058 | true | REQ-UX-058 — A reply is written from the conversation, and a reply to a gone chirp is reported |
| REQ-UX-059 | true | REQ-UX-059 — Like is an in-place, idempotent toggle with an accurate count |
| REQ-UX-060 | true | REQ-UX-060 — Follow is an in-place, idempotent control that cannot follow yourself |
| REQ-UX-061 | true | REQ-UX-061 — A public profile shows identity and chirps, with or without a session |
| REQ-UX-062 | true | REQ-UX-062 — The owner's profile is their public face with a way to edit it |
| REQ-UX-063 | true | REQ-UX-063 — Followers and following are addressable, paginated lists |
| REQ-UX-064 | false | REQ-UX-064 — A way to find people to follow |
| REQ-UX-065 | true | REQ-UX-065 — Onboarding explains the empty timeline and offers a way off it |
| REQ-UX-066 | true | REQ-UX-066 — Onboarding never blanks or dead-ends across its states |
| REQ-UX-067 | true | REQ-UX-067 — Edit profile changes display name and bio and persists them |
| REQ-UX-068 | true | REQ-UX-068 — Edit profile validates, reports failures in place, and keeps the person's input |
| REQ-UX-069 | true | REQ-UX-069 — The settings hub lists every account sub-section, each addressable and returning to the hub |
| REQ-UX-070 | true | REQ-UX-070 — View, update, and confirm control of the verified contact |
| REQ-UX-071 | false | REQ-UX-071 — The handle-change position is stated on the account screen and the screen matches it |
| REQ-UX-072 | false | REQ-UX-072 — Per-category notification preferences, saved immediately |
| REQ-UX-073 | true | REQ-UX-073 — See active sessions and end another device's session |
| REQ-UX-074 | true | REQ-UX-074 — Sign out ends the session server-side and does not leak back |
| REQ-UX-075 | true | REQ-UX-075 — A person can request and obtain their own data in a portable form |
| REQ-UX-076 | true | REQ-UX-076 — Deletion is confirmed with its consequence, its retained/not-retained outcome, and a pointer to export |
| REQ-UX-077 | true | REQ-UX-077 — Deletion proceeds only on explicit confirmation, and cancelling leaves everything intact |
| REQ-UX-078 | false | REQ-UX-078 — A notifications surface that shows directed activity and clears when seen |
| REQ-UX-079 | true | REQ-UX-079 — Reporting a chirp or account, acknowledged as received |
| REQ-UX-080 | false | REQ-UX-080 — Block and mute, each confirmed with its effect stated |
| REQ-UX-081 | false | REQ-UX-081 — Managing the accounts a person has blocked or muted |
| REQ-UX-082 | true | REQ-UX-082 — A user-facing help & support entry reachable from both shells |
| REQ-UX-083 | true | REQ-UX-083 — Stated rules a report can point to |
| REQ-UX-084 | true | REQ-UX-084 — A not-found screen that explains and routes back |
| REQ-UX-085 | true | REQ-UX-085 — Every safety and notification surface presents considered empty, error, and loading states |
| REQ-UX-086 | true | REQ-UX-086 — Empty surfaces are explained, never blank |
| REQ-UX-087 | true | REQ-UX-087 — Loading shows the shape of what is coming and never runs forever |
| REQ-UX-088 | true | REQ-UX-088 — Failures appear where the action was taken, in plain words, with a way forward |
| REQ-UX-089 | true | REQ-UX-089 — An expired session and a transient error both recover without losing work |
| REQ-UX-090 | true | REQ-UX-090 — The core loop is fully usable on a phone |
| REQ-UX-091 | true | REQ-UX-091 — One reading column, reflowed not rescaled, across viewports |
| REQ-UX-092 | true | REQ-UX-092 — The signed-in navigation shell adapts and keeps every destination reachable |
| REQ-UX-093 | true | REQ-UX-093 — The signed-out shell never dead-ends at any viewport |
| REQ-UX-094 | true | REQ-UX-094 — feed/list screens adapt without losing their controls |
| REQ-UX-095 | true | REQ-UX-095 — form screens are usable with the on-screen keyboard |
| REQ-UX-096 | true | REQ-UX-096 — profile and settings screens stack and keep their way back |
| REQ-UX-097 | true | REQ-UX-097 — overlays present as full-height surfaces on a phone with their actions reachable |
| REQ-UX-098 | true | REQ-UX-098 — touch targets are large enough and reachable |
| REQ-UX-099 | true | REQ-UX-099 — no auto-zoom, no horizontal scroll, portrait and landscape |
| REQ-UX-100 | true | REQ-UX-100 — A named, versioned accessibility standard: WCAG 2.1 AA |
| REQ-UX-101 | true | REQ-UX-101 — Every action is operable by keyboard alone |
| REQ-UX-102 | true | REQ-UX-102 — Focus order is logical and focus is always visible |
| REQ-UX-103 | true | REQ-UX-103 — No keyboard trap; modal focus is held but escapable |
| REQ-UX-104 | true | REQ-UX-104 — A way to bypass the navigation shell to the content |
| REQ-UX-105 | false | REQ-UX-105 — Controls meet a minimum target size |
| REQ-UX-106 | true | REQ-UX-106 — Every control exposes a name, a role, and its state |
| REQ-UX-107 | true | REQ-UX-107 — Each screen exposes landmark regions |
| REQ-UX-108 | true | REQ-UX-108 — One top-level heading per screen, in a nested order |
| REQ-UX-109 | true | REQ-UX-109 — Lists and feeds are exposed as navigable lists |
| REQ-UX-110 | true | REQ-UX-110 — Icon-only controls expose text labels and their active state |
| REQ-UX-111 | true | REQ-UX-111 — Contrast meets WCAG 2.1 AA in every shipped theme |
| REQ-UX-112 | true | REQ-UX-112 — Text resizes and the page reflows without loss |
| REQ-UX-113 | true | REQ-UX-113 — No fact is carried by colour alone, and no content flashes |
| REQ-UX-114 | true | REQ-UX-114 — Reduced motion is honoured with no loss of information |
| REQ-UX-115 | true | REQ-UX-115 — Status changes are announced without stealing focus |
| REQ-UX-116 | true | REQ-UX-116 — Errors are announced and tied to their field |
| REQ-UX-117 | true | REQ-UX-117 — Empty, loading, and expired-session states reach assistive technology |
| REQ-UX-118 | true | REQ-UX-118 — Conformance is verified three ways over the gated set |
| REQ-UX-119 | true | REQ-UX-119 — Accessibility gates the release, and failures are fixes not waivers |

## Non-gating requirements (release_gating = false) and their stated reasons

Thirteen `REQ-UX-*` are marked `release_gating: false`. Each reason is copied verbatim from the design file
(the source states a reason for every `false` flag). These are design-side facts for the synthesis gate: a
non-gating `REQ-UX-*` is not required to be covered by a `BAR-*`, so `BAR_COVERS_GATING_REQS` applies to the
`true` set only.

- **REQ-UX-015** — the gated behaviors are the flows themselves (REQ-PROD-010/011/013); the cross-links are a convenience a first release can omit, provided recovery remains reachable from help.
- **REQ-UX-019** — notifications ride REQ-PROD-029, which the release bar does not gate; the entry and its indicator ship with notifications when notifications ship.
- **REQ-UX-023** — the gated bar is legibility and contrast (REQ-UX-021, REQ-UX-022) in whatever theme(s) ship; a first release may ship a single theme and add the second as a fast follow, provided the shipped theme meets the bar.
- **REQ-UX-024** — depends on there being more than one theme (REQ-UX-023); ships when the second theme ships.
- **REQ-UX-030** — the designed avatar system (fixed sizes, deterministic placeholder) is polish; the hard minimum, that no state renders a broken image, is carried as part of the considered-states requirement (REQ-UX-031 / REQ-PROD-033).
- **REQ-UX-057** — reading replies as a navigable conversation rides REQ-PROD-004, which the release bar does not gate; the parent reference itself is already recorded by the gating reply requirement (REQ-UX-058 / REQ-PROD-003), so a first release may ship the reply action without the navigable conversation read.
- **REQ-UX-064** — Explore implements REQ-PROD-042, which the product requirements do not gate; a first release may ship with follow-by-profile and follow-from-a-reply and add discovery as a near-term follow-up. The release bar should decide explicitly what minimum discovery v1 includes.
- **REQ-UX-071** — rides REQ-PROD-018, a decision-and-consistency requirement; a first release may state the handle as fixed provided that position is stated on the screen.
- **REQ-UX-072** — notification preferences ride REQ-PROD-029, which the release bar does not gate; a first release may ship without notifications, and these preferences ship when notifications ship.
- **REQ-UX-078** — notifications ride REQ-PROD-029, which the release bar does not gate; the surface and its indicator ship when notifications ship.
- **REQ-UX-080** — block/mute ride REQ-PROD-027, which the release bar does not gate; reporting (REQ-UX-079) is the gated safety floor and these controls ship as the expected near-term addition.
- **REQ-UX-081** — the management screen serves the block/mute controls of REQ-PROD-027, which the release bar does not gate; it ships with those controls.
- **REQ-UX-105** — target size is a WCAG 2.2 criterion (2.5.8) adopted ahead of a full move to 2.2 and beyond the committed 2.1 AA floor; it is an expected mobile-ergonomics improvement a first release can stage.

## Join notes for synthesis

- Join key: `req_id`. All 119 ids are verbatim `REQ-UX-NNN`.
- This slice fills `req_id`, `release_gating`, `design_doc_ref` for the `REQ-UX-*` rows only. `bar_ids`
  comes from `SUBTASK_bar_mapping` (inverted `_Enforces REQ-*_`), `epic`/`issue_numbers` from
  `SUBTASK_backlog_pr`, and `live_status` is left for the sibling measurement joined by the fold.
- Gating `REQ-UX-*` the matrix must cover (for `BAR_COVERS_GATING_REQS`, SKELETON_COMPLETE): the 106 rows
  marked `release_gating: true`. The 13 `false` rows MAY appear in the matrix but are not required to carry
  a `bar_ids`.
- Open item for the gate: the hub's ~153 `REQ-UX-*` figure does not match the 119 the experience design
  defines. Resolve against `design/experience-design.md` as delivered (119), or record the hub figure as
  stale.

## Methodology limitation (recorded, per the subtree posture)

The `design` methodology loader was unavailable run-wide (`agent_domain_unset`); the loader call returned
that condition. This spoke proceeded under the principal-product-designer persona and the relayed Release
Definition guidance, as the subtree hub directs. The task is a verbatim extraction against a frozen,
completed input, so the limitation does not affect the extracted values.
