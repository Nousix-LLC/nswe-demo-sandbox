# COMPLETE — SUBTASK_notification_prefs

## What was done
Designed the **Notification preferences** surface (`/settings/notifications`, settings archetype,
signed-in) as a designed screen — layout, content, and primary action, plus its empty, error, and
loading states — and authored `REQ-UX-072`. Output: `outputs/screen-notification-prefs.md`.

## How it composes (for SUBTASK_synthesis)
- **Surface owned:** `notification_preferences` (the only surface this spoke owns, per
  `../contracts/settings_management_seam.yaml`). Id owned: `REQ-UX-072` (sole id in this spoke's
  sub-range 072..072).
- **Assembled position:** third, in screen-inventory order (settings hub → account & contact →
  notification preferences → sessions & devices).
- **Composed against the frozen vocabularies by name:** screen inventory (Notification preferences,
  `/settings/notifications`, settings archetype) and component library (NavShell, SettingRow, Toggle
  [immediate-save, revert-on-failure], InlineFeedback, EmptyState, LoadingState). Nothing redefined; no
  screen or component invented; no additive amendment to `../contracts/` was needed.

## Identity evidence (this spoke's part of the subtree identities)
- **SURFACE_COVERAGE** — empty/error/loading all addressed: **loading** = LoadingState skeleton rows on
  first load; **error** = EmptyState error variant with retry for a failed screen load (row-level save
  failure handled by the Toggle revert + danger InlineFeedback); **empty** = recorded "does not apply"
  with a component-matching reason (Toggle and SettingRow both record *empty* as not applying; the three
  categories are a fixed set).
- **NOT_SKELETAL** — layout, content (three category rows), and a named primary action (flip a
  category's Toggle, immediate + confirmed) are specified; addressable at `/settings/notifications` and
  returns to the Settings hub.
- **ID_UNIQUE_IN_RANGE** — one id, `REQ-UX-072`, within range, no collision.
- **UX_TESTABLE_AND_GATED** — `REQ-UX-072` has a statement, a stranger-checkable acceptance_criteria
  exercisable on the live product, and `release_gating: false` with a one-line reason.
- **UX_TRACES_TO_PROD** — references REQ-PROD-029 and REQ-PROD-017 (journey J6).
- **COMPOSES_AGAINST_VOCAB** — screen and components referenced by name only.
- **STATES_CONSISTENT** — each state is a composed component's own named state; the session-expiry
  recovery and the Notifications activity surface are cross-referenced to their owners, not redesigned.
- **HYGIENE** — the deliverable carries no host/system/taskflow detail, no workspace paths, no
  agent/DAG/run ids, and no attribution trailer.

## Scope honoured
Designed the notification **preferences** settings sub-section only. The **Notifications** activity
surface (`/notifications`) is cross-referenced, not redesigned (owned by the sibling safety &
notifications area). The product-wide empty/error/loading patterns and session-expiry recovery are
composed, not redefined (owned by the sibling considered-states area).

## Limitations recorded (per the brief and subtree hub)
- **Methodology loader unavailable.** The Phase-B `design` methodology loader could not be reached in
  this reconstructed environment (the loader syscall reported the agent domain unset). Per the recorded
  posture, the screen was designed from the named bundle intent — Experience Design (primary); Product
  Strategy (support) — and product-design competence; this did not block the work.
- **avoid-ai-writing skill absent.** The skill is not available in this environment; the P0/P1
  machine-writing catalog was applied by hand to the deliverable before finalizing.

## Evaluation
Decompose-evaluation: **Atomic** (one surface, one screen, one owned id; every decomposition trigger
cleared and both concern tests passed).
