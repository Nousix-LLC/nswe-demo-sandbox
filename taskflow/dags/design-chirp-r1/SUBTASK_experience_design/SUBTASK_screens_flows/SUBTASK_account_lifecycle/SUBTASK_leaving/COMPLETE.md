# COMPLETE — SUBTASK_leaving

## What was done
Designed the two **leaving** surfaces for chirp to the bar *designed screens, not a skeleton*, each with
its happy path and its empty/error/loading states, and minted `REQ-UX-075..077`:

- **Export your data** (`/settings/export`, settings archetype, signed-in) — request → preparing →
  obtainable result, composed from NavShell / SettingRow / PrimaryButton / SecondaryButton / LoadingState /
  EmptyState / InlineError / Toast; states: default-is-empty (nothing-yet), loading (screen skeleton +
  preparing), error (preparation failure + screen-load error variant). Serves REQ-PROD-019.
- **Delete account** (`/settings/delete`, confirmation archetype, signed-in) — realised as the Dialog
  confirmation variant per the IA destructive-confirmation convention; names the consequence, renders the
  product's defined deletion outcome (what is removed / what may remain / handle), points to export first,
  and requires explicit confirmation; states: default, disabled-until-confirmed, loading (confirm in
  flight), error (failed deletion, nothing removed), empty (N/A with reason). Serves REQ-PROD-020,021,022.

## What was produced
- `outputs/screens-leaving.md` — the two screens at wireframe-level detail + `REQ-UX-075..077`
  (`statement`, testable `acceptance_criteria`, `release_gating`, REQ-PROD references).

## How it composes with the parent
`outputs/screens-leaving.md` is the `leaving` part of the account-lifecycle deliverable
(`surfaces: [data_export, account_deletion]`, `REQ-UX-075..077`), assembled by `SUBTASK_synthesis` in screen
-inventory order after `onboarding_profile` and `settings_management`. It satisfies this subtree's
identities: SURFACE_COVERAGE (both owned surfaces designed with their three states), ID_UNIQUE_IN_RANGE
(075,076,077 — unique, in the `075..077` sub-range, no gaps/collisions), NOT_SKELETAL (layout + content +
primary action + states per screen), UX_TESTABLE_AND_GATED (all three gated true, each with a stranger-
checkable criterion), UX_TRACES_TO_PROD (075→019; 076→021,022; 077→020,022), COMPOSES_AGAINST_VOCAB (only
inventory screens and library components/states, by name), STATES_CONSISTENT (each state is a component's own
named state, deferring the product-wide pattern to the sibling `considered_states`), HYGIENE (clean).

## Design judgments recorded
- **Deletion outcome is rendered, not invented.** Per the brief and REQ-PROD-021, the delete confirmation
  presents the product's *defined* deletion outcome (replied-to/liked chirps; whether the handle frees up);
  the specific policy is the privacy/identity design's. The screen fixes the content shape (removed / may
  remain / handle) and states plainly where the product has not yet set an outcome, rather than implying a
  guarantee. This holds to "what the person is told and must confirm," not the data-removal mechanism.
- **Delete account as the Dialog confirmation variant at an addressable route** — composes the IA
  destructive-confirmation convention and addressability; the sign-out-to-signed-out-shell return is used as
  an IA convention, not redesigned.

## Limitations recorded (did not block)
- **Phase-B `design` methodology loader unavailable** in this reconstructed environment (the methodology
  syscall reports the agent domain unset). Per the ancestor hubs' recorded posture, designed from the named
  bundle intent — Experience Design (primary); Identity & Trust, Product Strategy (support) — and own
  product-design competence.
- **`avoid-ai-writing` skill absent** — ran the P0/P1 machine-writing catalog by hand over the deliverable
  before finalizing (no moral adjectives on abstractions, no narrated candor, no unnamed-half contrasts, no
  slot-fill templates, no padded triads, no hollow intensifiers).
