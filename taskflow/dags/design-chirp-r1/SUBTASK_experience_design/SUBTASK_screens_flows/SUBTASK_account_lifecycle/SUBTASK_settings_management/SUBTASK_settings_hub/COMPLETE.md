# COMPLETE — SUBTASK_settings_hub

## What was done
Designed the **Settings hub** (`/settings`, settings archetype, signed-in) as a designed screen — not a
skeleton — and minted **REQ-UX-069**. Output: `outputs/screen-settings-hub.md`.

The hub is the settings secondary-navigation surface: a list of **SettingRow**s inside the signed-in
**NavShell**, grouped (Account / Notifications / Privacy and safety / Security / Your data) and listing
every settings sub-section named in the inventory (REQ-UX-017) — edit profile, account & contact,
notification preferences, sessions & devices, blocked & muted, export your data, delete account. Each row
is an addressable drill-in that returns to the hub; the sibling and externally-owned sub-sections are
referenced by inventory name/route only, their contents designed elsewhere. The Delete account row is
styled destructive (`color.danger`) and routes to a confirmation.

- **Primary action**: opening a sub-section (the SettingRow drill-in). Recorded the deliberate absence of
  a single PrimaryButton (the archetype is a list of peer destinations; sign-out lives in the account menu
  and Sessions & devices), so NOT_SKELETAL is satisfied honestly rather than with a bolted-on CTA.
- **States**: loading designed (narrow — the account-summary header composes Avatar *loading* +
  LoadingState; the fixed menu renders immediately, matching NavShell); empty recorded **does not apply**
  with a reason matching the composed components' own decisions (SettingRow and NavShell both record
  *empty* as not applying); error designed as graceful partial degradation (a failed account summary
  degrades to the Avatar monogram while the navigation list stays usable) plus the composed auth-gating /
  session-expiry routing (REQ-UX-007/008).

## Composition / contract conformance
- Composes against `../contracts/`, the screen inventory, and the component library **by name**; no
  screen, component, token, or value redefined or invented. Owns only the `settings_hub` surface and
  `REQ-UX-069` (in the assigned 069..069 sub-range).
- REQ-UX-069: `statement`, stranger-checkable `acceptance_criteria`, `release_gating: true`, traces to
  `REQ-PROD-017`. Gated because the settings hub rides the gated REQ-PROD-017 (per the seam's trace rule).
- Hygiene: the deliverable carries no host/system/taskflow detail, no workspace paths, no agent/DAG/run
  ids, and no attribution trailer.

## Decompose evaluation
Evaluated against the decomposition triggers at dispatch: one surface, one responsibility (design this
screen), one output, inputs already in context — every trigger cleared and both concern tests passed.
**Atomic**, independently of the ancestor having already split the settings cluster.

## Limitations recorded (do not block; kept out of the repository-ready deliverable)
1. **Methodology loader unavailable.** The Phase-B `design` methodology loader could not be loaded in this
   reconstructed environment (`engine_load_methodology` / `engine_methodology_glob` report the agent
   domain unset). Per the ancestor hubs' recorded posture, the screen was designed from the named bundle
   intent — Experience Design (primary), Product Strategy (support) — and principal-product-designer
   competence. No methodology-specific framework file was consulted.
2. **avoid-ai-writing skill absent.** The skill is not available in this environment; the P0/P1
   machine-writing catalog was run over the narrative by hand before finalizing and the flagged tells
   checked (character adjectives, unnamed contrasts, slot-fill templates, padded triads, hollow filler,
   stacked connectives) — none remained.

## Output
- `outputs/screen-settings-hub.md`
