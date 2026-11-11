# SYNTHESIS — SUBTASK_settings_management

## What this record is

This is the fold record for the account-settings subtree. It is the synthesis task's terminal record
and the seam the fold consumes; there is no separate `COMPLETE.md` for this task. The fold moves the
parent node (`SUBTASK_settings_management`) from `SUSPENDED → COMPLETED`.

---

## Assembled output

`outputs/screens-settings-management.md` contains the four account-settings screens in screen-inventory
order — Settings hub, Account & contact, Notification preferences, Sessions & devices — followed by the
consolidated `REQ-UX-069..074` register. All content was assembled from the four spoke outputs without
re-design.

---

## Identity evidence

Each identity is evaluated with recorded evidence from the assembled output. No identity is silently
plugged; a failing identity would require a remediation subtree before folding.

### SURFACE_COVERAGE — PASS

All four owned surfaces are present, each designed with its empty, error, and loading states, or a state
recorded "does not apply" with a reason matching the composed component's own not-applicable decision:

| Surface | Empty | Error | Loading |
|---|---|---|---|
| Settings hub (`/settings`) | Does not apply — hub lists a fixed set of sub-sections; SettingRow and NavShell record empty as not applying. | Two paths: account-summary degradation (Avatar error treatment; list stays usable); auth-gate / session-expiry routes to Sign in (REQ-UX-007/008). | LoadingState skeleton on Account summary; sub-section list renders immediately. |
| Account & contact (`/settings/account`) | Does not apply at screen level — no-contact case is in-row (caution + PrimaryButton "Add contact"), consistent with SettingRow's and EmptyState's own not-applicable decisions. | Three paths: screen load failure (EmptyState error variant + retry); save failure (InlineError beneath TextField, typed value kept); verification failure (InlineFeedback danger role). Session expiry: to Sign in, draft preserved (REQ-UX-008). | LoadingState skeleton for Contact and Handle rows; NavShell renders immediately. |
| Notification preferences (`/settings/notifications`) | Does not apply — three activity categories are a fixed set; Toggle records empty as not applying; SettingRow row-level empty not applicable. | Screen-level load failure: EmptyState error variant ("try again"). Individual save failure: Toggle reverts + InlineFeedback danger role. Session expiry composes product-wide pattern. | LoadingState skeleton rows at real dimensions; NavShell renders immediately. |
| Sessions & devices (`/settings/sessions`) | "Only this session" case: ListView shows EmptyState ("You're only signed in here..."); This device row and Sign out remain present. | Sessions list load failure: ListView error treatment (EmptyState variant + retry); This device row still renders. Action failures: InlineError inside open Dialog, retryable. Session expiry: product-wide pattern composed. | ListView / LoadingState skeleton rows; NavShell and screen heading render immediately; This device row renders as soon as current session is known. |

### ID_UNIQUE_IN_RANGE — PASS

All six `REQ-UX` ids are present, unique, and within their contracted sub-ranges. No collisions, no
out-of-range ids, no gaps.

| Id | Owning spoke | Sub-range | Present in register |
|---|---|---|---|
| REQ-UX-069 | SUBTASK_settings_hub | 069..069 | ✓ |
| REQ-UX-070 | SUBTASK_account_contact | 070..071 | ✓ |
| REQ-UX-071 | SUBTASK_account_contact | 070..071 | ✓ |
| REQ-UX-072 | SUBTASK_notification_prefs | 072..072 | ✓ |
| REQ-UX-073 | SUBTASK_sessions_devices | 073..074 | ✓ |
| REQ-UX-074 | SUBTASK_sessions_devices | 073..074 | ✓ |

### NOT_SKELETAL — PASS

Each screen specifies layout, content, a primary action, and its empty, error, and loading states.

| Screen | Layout | Content | Primary action |
|---|---|---|---|
| Settings hub | NavShell + 600px reading column; Account summary header; grouped SettingRow list under section labels. | 7 sub-section rows in 5 groups; Delete account styled as destructive; Notification preferences row conditional on release. | Drill-in on a SettingRow (each sub-section). |
| Account & contact | NavShell; Back to settings control; SettingRow list (Contact + Handle). | Contact row with verification-status indicator and Change / Verify now controls; Handle row with stated handle-change position. | PrimaryButton "Save changes" in Contact row edit mode. |
| Notification preferences | NavShell; heading + lead line; three SettingRows with Toggle in control slot. | Replies, Follows, Likes — each with on/off Toggle; defaults all on; fixed set. | Flip a Toggle (immediate-save). |
| Sessions & devices | NavShell; intro line; This device row; Other sessions ListView; Sign out entry. | Per-session rows with device/browser/location/last-active; short session identifier in mono; End session SecondaryButton per other session. | Sign out (server-side session end). |

### UX_TESTABLE_AND_GATED — PASS

Every `REQ-UX` entry in the consolidated register carries a `statement`, a stranger-checkable
`acceptance_criteria`, and a `release_gating` flag. The two `false` entries carry their one-line reason.

| Id | Has statement | Has acceptance_criteria | release_gating | Non-gating reason present |
|---|---|---|---|---|
| REQ-UX-069 | ✓ | ✓ | true | n/a |
| REQ-UX-070 | ✓ | ✓ | true | n/a |
| REQ-UX-071 | ✓ | ✓ | false | ✓ — rides REQ-PROD-018; a first release may state the handle as fixed. |
| REQ-UX-072 | ✓ | ✓ | false | ✓ — rides REQ-PROD-029; preferences ship when notifications ship. |
| REQ-UX-073 | ✓ | ✓ | true | n/a |
| REQ-UX-074 | ✓ | ✓ | true | n/a |

REQ-UX-071 and REQ-UX-072 are the expected non-gating entries per REQ-PROD-018 and REQ-PROD-029.

### UX_TRACES_TO_PROD — PASS

Every `REQ-UX` entry references at least one `REQ-PROD-*`.

| Id | REQ-PROD references |
|---|---|
| REQ-UX-069 | REQ-PROD-017 |
| REQ-UX-070 | REQ-PROD-012, REQ-PROD-017 |
| REQ-UX-071 | REQ-PROD-018, REQ-PROD-017 |
| REQ-UX-072 | REQ-PROD-029, REQ-PROD-017 |
| REQ-UX-073 | REQ-PROD-017, REQ-PROD-014 |
| REQ-UX-074 | REQ-PROD-014 |

### COMPOSES_AGAINST_VOCAB — PASS

All four screens refer to screens by their inventory names and routes, and are built from named
component-library components. No new screen or component is introduced.

**Screens referenced by inventory name:**
Settings (`/settings`), Account & contact (`/settings/account`), Notification preferences
(`/settings/notifications`), Sessions & devices (`/settings/sessions`), Edit profile
(`/settings/profile`), Blocked & muted (`/settings/blocks`), Export your data (`/settings/export`),
Delete account (`/settings/delete`), Notifications (`/notifications`), Landing (signed-out).

**Components used by name across all four screens:**
NavShell, SettingRow, Toggle, TextField, PrimaryButton, SecondaryButton, IconButton, Dialog (confirmation
variant), InlineFeedback, InlineError, EmptyState, LoadingState, Toast, ListView, Avatar.

No component or screen absent from the library or inventory is introduced; the composition provenance
note in the Notification preferences screen is the most explicit per-screen record.

### STATES_CONSISTENT — PASS

Each screen's empty, error, and loading states are consistent with the components' own named states and
with the product-wide patterns owned by the sibling `SUBTASK_considered_states`.

All four screens:
- Use `LoadingState` (skeleton rows/blocks) for first load, never a blank-panel spinner.
- Use `EmptyState` (or record it as "does not apply" with a reason matching the component's own
  not-applicable decision) — never a blank area, never an apology.
- Compose the product-wide session-expiry recovery (REQ-UX-008: route to Sign in with reason stated,
  preserve draft, return afterward) without redefining it.
- Use `InlineError` / `InlineFeedback` for action-level failures, scoped to the control that failed,
  with the typed value kept for retry.
- No screen invents a per-screen state treatment that conflicts with the product-wide patterns.

The states table in Sessions & devices is the most explicit per-component cross-reference; the Account &
contact states section explicitly notes which component states apply and which do not.

### HYGIENE — PASS

The assembled deliverable (`outputs/screens-settings-management.md`) contains no host or server
addresses, no workspace paths, no agent/DAG/run identifiers, and no attribution trailers. The content
is repository-ready product design.

---

## Avoid-ai-writing review

The `avoid-ai-writing` skill (via `references/patterns.md`) is unavailable in this reconstructed
environment. The assembled deliverable was reviewed against the P0/P1 machine-writing catalog from memory:

- No "honest", "genuine", "faithful", "authentic" applied to abstractions.
- No "to be honest" / "stated plainly" / "let's be clear" candor-narration.
- No "seamless", "robust", "comprehensive", "leverage" filler.
- No slot-fill templates ("whether you're X or Y", "in today's world", "at its core").
- No "Moreover / Furthermore / Additionally" starters.
- No padded triads added for rhythm.

The writing in all four screen sections is direct and checkable throughout. Limitation recorded.

---

## Fold

`SUBTASK_settings_management` is folded from `SUSPENDED → COMPLETED`.

The parent's declared outputs are:
- `outputs/screens-settings-management.md` — assembled and verified.
- `SYNTHESIS.md` — this record.
