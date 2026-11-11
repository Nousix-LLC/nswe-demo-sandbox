# Task: Assemble & verify the account-settings screens (synthesis gate + fold)

## Task Specification
**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective
Assemble the four account-settings spoke outputs into the `settings_management` deliverable, verify this
subtree's identities with recorded evidence, author the fold record, and fold this subtree's root
(`SUBTASK_settings_management`) to COMPLETED.

### Context
This is the verification gate and fold for the account-settings subtree (see `../_GLOBAL.md`,
`../contracts/`). The four surface spokes have each produced a designed screen with its states and its
`REQ-UX` entries. Your job is mechanical assembly + identity verification, not re-design: you do not
redesign a screen or re-mint a requirement; you integrate what the spokes produced and confirm it holds
together, in screen-inventory order.

**Dependencies**: `SUBTASK_settings_hub`, `SUBTASK_account_contact`, `SUBTASK_notification_prefs`,
`SUBTASK_sessions_devices` (all four must be COMPLETED; read their outputs as immutable inputs — do not
poll). **Dependents**: the parent account-lifecycle `SUBTASK_synthesis` consumes your assembled output.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | The assembled-order, success criteria, and hygiene bar. |
| Internal contract | `../contracts/` (read-only) | The surface→owner map, the `REQ-UX-069..074` partition, the identities to assert, the assembled order, the derived-register spec. |
| Settings hub screen | `../SUBTASK_settings_hub/outputs/screen-settings-hub.md` | The hub screen + `REQ-UX-069`. |
| Account & contact screen | `../SUBTASK_account_contact/outputs/screen-account-contact.md` | The screen + `REQ-UX-070..071`. |
| Notification preferences screen | `../SUBTASK_notification_prefs/outputs/screen-notification-prefs.md` | The screen + `REQ-UX-072`. |
| Sessions & devices screen | `../SUBTASK_sessions_devices/outputs/screen-sessions-devices.md` | The screen + `REQ-UX-073..074`. |

### Output
- `../outputs/screens-settings-management.md` — the `settings_management` section-part: the four designed
  screens assembled in screen-inventory order (Settings hub, Account & contact, Notification preferences,
  Sessions & devices), followed by the consolidated `REQ-UX-069..074` register. Repository-ready; no
  host/system/taskflow detail, no workspace paths, no agent/DAG/run ids, no attribution.
- `../SYNTHESIS.md` — the fold record at the fold location (this subtree root's directory): the identity
  evidence table and the fold. This is both your terminal completion record and the record the fold
  consumes; write no separate `COMPLETE.md`.

### Success criteria — assert each identity with recorded evidence (no silent plugs)
- [ ] **SURFACE_COVERAGE** — all four surfaces present, each with its empty/error/loading states (or a
      "does not apply" matching the composed component's own decision).
- [ ] **ID_UNIQUE_IN_RANGE** — `REQ-UX-069..074` present, each unique, each within its owning spoke's
      sub-range; no collisions, no out-of-range ids, no gaps.
- [ ] **NOT_SKELETAL** — each screen has layout, content, a primary action, and its three states.
- [ ] **UX_TESTABLE_AND_GATED** — every `REQ-UX-*` has a statement, a stranger-checkable
      `acceptance_criteria`, and a `release_gating` flag (false carries a one-line reason; 071 and 072
      are the expected non-gating ones per REQ-PROD-018/029).
- [ ] **UX_TRACES_TO_PROD** — every `REQ-UX-*` references ≥1 `REQ-PROD-*`.
- [ ] **COMPOSES_AGAINST_VOCAB** — every screen refers to inventory screens and library components by
      name; nothing redefined; no out-of-vocabulary screen/component.
- [ ] **STATES_CONSISTENT** — each screen's states are consistent with the components' named states and
      the product-wide patterns owned by `../../../SUBTASK_considered_states`.
- [ ] **HYGIENE** — the assembled deliverable carries no host/system/taskflow detail, workspace paths,
      ids, or attribution.
- [ ] On a fixable gap, remediate by decomposing a remediation subtree (amend the plan), never by a
      silent plug; then fold.
- [ ] Fold: author `../SYNTHESIS.md`, report `status="completed"` with `artifact_path` at
      `../SYNTHESIS.md`, and resume the suspended parent (`SUBTASK_settings_management`) with that seam.

### Constraints
- Design-integration only — no front-end code; no re-design of a spoke's screen or requirement.
- Repository-ready hygiene on all output content.
- Methodology: Experience Design. If the `design` loader is unavailable, work from the bundle intent and
  competence and record the limitation (do not block).
- Write in a plain, checkable human voice; run the avoid-ai-writing checklist (or the P0/P1 catalog by
  hand when the skill is absent — it is absent here) over the assembled narrative before finalizing, and
  record the limitation.
- Evaluate your own scope against the decomposition triggers at dispatch; assembling four short screen
  parts + verifying eight identities is expected to be atomic, but the decision is yours.
