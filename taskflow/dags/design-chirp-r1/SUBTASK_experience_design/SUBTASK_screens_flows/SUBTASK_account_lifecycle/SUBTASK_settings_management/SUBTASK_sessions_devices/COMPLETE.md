# COMPLETE — SUBTASK_sessions_devices

## What was done

Designed the **Sessions & devices** surface (`/settings/sessions`, settings archetype, signed-in) as a
non-skeletal screen and authored the deliverable `outputs/screen-sessions-devices.md`. It specifies:

- **Layout and content** — a list of `SettingRow`s inside the signed-in `NavShell` against the 600px
  measure: an intro line, a marked **This device** current-session row, an **Other sessions** `ListView`
  of per-session `SettingRow`s (device/browser, approximate location, last-active time, and a
  `type.family.mono` session identifier, with an **End session** `SecondaryButton`/`IconButton`), and the
  **Sign out** entry.
- **Primary action** — Sign out (the screen's decisive, release-gated action); ending another device's
  session is the row-level destructive action.
- **The confirmed end-session flow** — `Dialog` confirmation variant naming the effect, destructive
  `color.danger` confirm + Cancel, server-side end, result shown via `InlineFeedback`/`Toast`, failure via
  `InlineError` in the dialog.
- **The sign-out flow** — `Dialog` confirmation (with the "also sign out of other sessions" option from the
  inventory's Sign out dialog), server-side end, leading **into** the inventory's sign-out transition
  (REQ-UX-016) without redesigning it.
- **Empty / error / loading states** — the empty "only this session" case (`ListView` `EmptyState`), the
  list-load / dialog-action / expired-session (REQ-UX-008) error cases, and the skeleton-row loading case
  with a persistent shell — each a composed component's own named state.
- **REQ-UX-073** (see active sessions + end another device's session; gated; → REQ-PROD-017, REQ-PROD-014)
  and **REQ-UX-074** (sign out, server-side, no back-leak; gated; → REQ-PROD-014), each with a statement
  and a stranger-checkable acceptance_criteria.

## How it composes with the parent

This is the `sessions_and_devices` part of the `settings_management` section-part. `SUBTASK_synthesis`
assembles `outputs/screen-sessions-devices.md` into `../outputs/screens-settings-management.md` in
screen-inventory order (fourth, after settings hub, account & contact, notification preferences) and folds
`REQ-UX-073..074` into the consolidated `REQ-UX-069..074` register.

## Contract / identity conformance (this spoke's part)

- **COMPOSES_AGAINST_VOCAB** — screens named from the inventory (Sessions & devices, Settings, Sign in,
  signed-out Landing); components named from the library (`NavShell`, `SettingRow`, `ListView`, `Dialog`
  confirmation variant, `PrimaryButton`, `SecondaryButton`, `IconButton`, `Toggle`, `InlineFeedback`,
  `InlineError`, `EmptyState`, `LoadingState`, `Toast`, `type.family.mono`, tokens); conventions referenced
  by id (REQ-UX-011, 016, 017, 010, 008). Nothing redefined; no new screen/component; no amendment needed.
- **NOT_SKELETAL** — layout, content, and a primary action, plus empty/error/loading, all specified.
- **SURFACE_COVERAGE** — empty, error, and loading all designed (no "does not apply" claimed).
- **ID_UNIQUE_IN_RANGE** — REQ-UX-073 and REQ-UX-074 only; unique; within the 073..074 sub-range.
- **UX_TESTABLE_AND_GATED** — both carry statement + acceptance_criteria + `release_gating: true`.
- **UX_TRACES_TO_PROD** — 073 → REQ-PROD-017, REQ-PROD-014; 074 → REQ-PROD-014.
- **STATES_CONSISTENT** — each state is a composed component's own named state and composes (does not
  redefine) the product-wide patterns owned by the sibling considered-states work.
- **HYGIENE** — the deliverable carries only user-facing routes, screen/component names, and REQ ids; no
  host/system/taskflow detail, no workspace paths, no agent/DAG/run ids, no attribution.

Scope honoured: designed user-visible behaviour only (not the session/token mechanism, `REQ-ID-*`); designed
sign-out into the inventory's transition without redesigning it; owns only `REQ-UX-073..074`.

## Limitations recorded

- **Methodology loader unavailable.** The Phase-B `design` methodology loader is unreachable in this
  reconstructed environment (the loader syscall reports the agent domain unset). Per the ancestor-hub
  posture, this surface was designed from the named bundle intent — Experience Design (primary), Identity &
  Trust (support) — and product-design competence. No methodology-specific framework file was read.
- **avoid-ai-writing skill absent.** The skill is not present here; the P0/P1 machine-writing catalog was
  run by hand over the deliverable narrative before finalizing, and no P0/P1 tell remained.

## Output

- `outputs/screen-sessions-devices.md`
