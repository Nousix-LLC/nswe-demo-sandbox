# SYNTHESIS — account-lifecycle screens subtree (fold record)

The verification gate and fold for `SUBTASK_account_lifecycle`. Three spokes each designed one surface
cluster of the `account_lifecycle` part and minted a slice of `REQ-UX-065..077`. This record assembles
them into one part (`outputs/screens-account-lifecycle.md`), consolidates the register, asserts every
contract identity with recorded evidence, and folds this node to COMPLETED.

**Result: clean pass.** All eight owned surfaces are present, each designed with its empty/error/loading
states by its single owner; `REQ-UX-065..077` is complete, unique, in-range, and each entry is testable,
gated, and traced; everything composes against the frozen vocabularies by name; the states are consistent
with the components' own named states and the product-wide patterns; and the deliverable carries no
hygiene leakage. No identity failed, so no remediation subtree was decomposed.

## Inputs folded

| Spoke | Output | Surfaces | REQ-UX |
|---|---|---|---|
| `SUBTASK_onboarding_profile` | `SUBTASK_onboarding_profile/outputs/screens-onboarding-profile.md` | Onboarding, Edit profile | 065–068 |
| `SUBTASK_settings_management` | `SUBTASK_settings_management/outputs/screens-settings-management.md` | Settings hub, Account & contact, Notification preferences, Sessions & devices | 069–074 |
| `SUBTASK_leaving` | `SUBTASK_leaving/outputs/screens-leaving.md` | Data export, Account deletion | 075–077 |

Assembled into `outputs/screens-account-lifecycle.md` in screen-inventory order (Onboarding, Edit profile,
Settings hub, Account & contact, Notification preferences, Sessions & devices, Export your data, Delete
account), followed by the consolidated `REQ-UX-065..077` register.

Verification inputs read: `contracts/_MANIFEST.yaml` and `contracts/account_lifecycle_seam.yaml` (the seam
asserted against); the frozen Screen inventory (`SUBTASK_ia_interaction/outputs/ia-interaction.md`) and
Component library (`SUBTASK_visual_system/outputs/visual-system.md`); and the product requirements
(`SUBTASK_product_requirements/outputs/product-requirements.md`) for the trace and gating checks.

## Identity assertions (with recorded evidence)

### 1. SURFACE_COVERAGE — PASS
All eight owned surfaces are designed, each by exactly one owning spoke, each with its empty, error, and
loading states:

| Surface | Owner | Empty | Error | Loading |
|---|---|---|---|---|
| Onboarding | onboarding_profile | resting EmptyState (the screen itself) | suggestions-preview error variant + retry; core routes stay up | NavShell immediate; preview region skeletons |
| Edit profile | onboarding_profile | optional bio empty valid (TextField empty) | field-level + save-level InlineError, input kept | field skeletons on open; PrimaryButton busy on save |
| Settings hub | settings_management | does not apply — fixed sub-section list (SettingRow/NavShell empty = n/a), reason recorded | account-summary degrade; session-expiry recovery | fixed list immediate; Avatar+lines skeleton for summary |
| Account & contact | settings_management | "no contact set yet" caution inside the Contact row (whole-screen EmptyState n/a, reason recorded) | load-fail EmptyState error; save-fail InlineError; verify-fail InlineFeedback; session-expiry | SettingRow-list skeleton; in-place control loading |
| Notification preferences | settings_management | does not apply — fixed 3 categories (Toggle/SettingRow empty = n/a), reason recorded | load-fail EmptyState error + retry; per-save handled on row | 3 skeleton rows at real size |
| Sessions & devices | settings_management | "only signed in here" ListView EmptyState | list load-fail EmptyState/InlineError + retry; Dialog error; session-expiry | ListView skeleton rows; This device renders early |
| Data export | leaving | default = "nothing yet" EmptyState (correct for a request surface) | prepare-fail InlineError + retry; screen load-fail EmptyState error | first-paint skeletons; "Preparing…" bounded spinner |
| Account deletion | leaving | does not apply — a confirmation always opens with content (Dialog empty = n/a), reason recorded | delete-fail InlineError in panel, account not deleted | confirm busy state, dialog stays open |

"Does not apply" cases are each grounded in the composed component's own named-state decision (the library
explicitly records "does not apply" as a design decision, not an omission). None is a skipped state.

### 2. ID_UNIQUE_IN_RANGE — PASS
Thirteen ids `REQ-UX-065..077`, contiguous, each within its owner's sub-range, no collisions, no gaps, no
out-of-range: onboarding_profile 065/066/067/068 (range 065–068); settings_management 069/070/071/072/073/074
(range 069–074); leaving 075/076/077 (range 075–077).

### 3. NOT_SKELETAL — PASS
Each of the eight screens specifies layout, content, and a primary action, plus its empty/error/loading
states — never a bare route name. Primary actions on record: Write your first chirp → Compose (Onboarding);
Save changes (Edit profile); open a sub-section (Settings hub); Save the updated contact (Account &
contact); flip a category Toggle (Notification preferences); Sign out (Sessions & devices); Prepare my data
(Export); Delete my account (Delete account).

### 4. UX_TESTABLE_AND_GATED — PASS
Every entry carries a statement, a stranger-checkable acceptance criterion exercisable on the live product,
and a `release_gating` flag. Gated `true`: 065, 066, 067, 068, 069, 070, 073, 074, 075, 076, 077. Gated
`false` with a one-line reason: 071 (rides the non-gating REQ-PROD-018 handle-change decision), 072 (rides
the non-gating REQ-PROD-029 notifications).

### 5. UX_TRACES_TO_PROD — PASS
Every entry references ≥1 `REQ-PROD-*`, and every referenced id exists in the product requirements register:
065→032; 066→032,033; 067→016; 068→016,033,034; 069→017; 070→012,017; 071→018,017; 072→029,017; 073→017,014;
074→014; 075→019; 076→021,022; 077→020,022. Set verified present: 012, 014, 016, 017, 018, 019, 020, 021,
022, 029, 032, 033, 034.

### 6. COMPOSES_AGAINST_VOCAB — PASS
Every screen refers to a Screen-inventory screen by name and route (Onboarding `/welcome`, Edit profile
`/settings/profile`, Settings `/settings`, Account & contact `/settings/account`, Notification preferences
`/settings/notifications`, Sessions & devices `/settings/sessions`, Export your data `/settings/export`,
Delete account `/settings/delete` — all present in the inventory with matching archetype and auth state) and
is built only from named Component-library components (Avatar, ProfileHeader, TextField, Toggle,
PrimaryButton, SecondaryButton, IconButton, NavShell, ListView, SettingRow, Dialog, Toast, InlineFeedback,
InlineError, EmptyState, LoadingState — each present in the library). No screen or component is redefined
and none is introduced outside the frozen vocabularies.

### 7. STATES_CONSISTENT — PASS
Each per-screen empty/error/loading state is one of the composed components' own named states (ListView
empty/loading/error; EmptyState default/error; LoadingState skeletons and bounded spinner; Toggle
immediate-save with revert-on-failure; Dialog loading/error/disabled-confirm; SettingRow pending/error;
TextField empty/error/loading; Avatar error monogram), and the product-wide treatments the spokes lean on —
expired-session recovery and keep-the-draft on a transient error (REQ-UX-008), the empty/loading/error
patterns — are referred to as owned by the sibling `SUBTASK_considered_states`, not redefined. No screen
invents a conflicting per-screen pattern.

### 8. HYGIENE — PASS
`outputs/screens-account-lifecycle.md` carries only user-facing design content — routes, component and
screen names, token names, journeys, and REQ ids. No host/system/taskflow detail, no workspace paths, no
agent/DAG/run ids, and no attribution trailer. This fold record is the internal verification artifact and
is not part of the repository-ready deliverable.

## Methodology posture (recorded limitation)
The Phase-B `design` methodology loader was unavailable in this reconstructed environment (the loader
reports the agent domain unset). Per the ancestor hubs' recorded posture, verification was performed from
the Experience Design bundle intent and product-design competence; this did not block the gate. The
narrative deliverable and this record were checked by hand against the P0/P1 machine-writing catalog (the
`avoid-ai-writing` skill is absent in this environment) and written in a plain, checkable voice.

## Fold
All contract identities hold with recorded evidence; the assembled deliverable and the consolidated
`REQ-UX-065..077` register are produced. This record resolves the synthesis fold: the account-lifecycle
node (`SUBTASK_account_lifecycle`) folds `SUSPENDED → COMPLETED`, and its parent (`SUBTASK_screens_flows`)
may consume `outputs/screens-account-lifecycle.md` and the register when it builds the full screens-&-flows
deliverable.

## Outputs
- `outputs/screens-account-lifecycle.md` — the assembled `account_lifecycle` part (eight surfaces in
  inventory order) plus the consolidated `REQ-UX-065..077` register.
- `SYNTHESIS.md` — this fold record.
