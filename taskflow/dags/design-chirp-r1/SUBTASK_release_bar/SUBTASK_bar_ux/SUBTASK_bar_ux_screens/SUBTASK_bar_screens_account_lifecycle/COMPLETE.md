# COMPLETE — SUBTASK_bar_screens_account_lifecycle

## What this task did
Authored the account-management & lifecycle chapter of the screens release-bar fragment: `BAR-248..255`
holding the 11 release-gating `REQ-UX-*` of the account-lifecycle chapter (`REQ-UX-065, 066, 067, 068, 069,
070, 073, 074, 075, 076, 077`) to concrete, testable release conditions, with a coverage note and a staging
proposal.

Atomic. Evaluated the decomposition triggers against this brief: token and output-size cleared (one fragment,
~150 lines); single-responsibility holds (one kind of change — translate gating requirements into testable
release conditions — one kind of output); the surface enumeration did not fire the Scope/Distinct-Concerns
trigger on honest reading because the seven surfaces are coupled by one shared, deliberately tight id budget
(8 ids for 11 requirements, clustering required) and one coverage note, so they are facets of one authoring
job, not parallel-specialist concerns. The evaluation was independent of the parent's prior cut.

## Output produced
- `outputs/bar-screens-account-lifecycle.md` — one block per `BAR-*` (`id`, `statement`, `references`,
  `verification_method`, `proposed_stage`), the account-lifecycle coverage note, and the staging proposal.
  Repository-ready.

## Clustering (11 gating REQ into 8 ids)
Three same-screen pairs merged; session-list and server-side sign-out kept apart so each `BAR-*` carries one
coherent verification method and one stage with no within-criterion conflict.

| BAR | REQ-UX enforced | Surface | verification_method | proposed_stage |
|---|---|---|---|---|
| BAR-248 | 065, 066 | Onboarding | manual_user_check | usable_early |
| BAR-249 | 067, 068 | Edit profile | manual_user_check | releasable |
| BAR-250 | 069 | Settings hub | manual_user_check | releasable |
| BAR-251 | 070 | Account & contact control | manual_user_check | releasable |
| BAR-252 | 073 | Sessions & devices | operational_check | releasable |
| BAR-253 | 074 | Server-side sign-out, no back-leak | operational_check | usable_early |
| BAR-254 | 075 | Data export | manual_user_check | releasable |
| BAR-255 | 076, 077 | Account deletion | operational_check | releasable |

## How it composes with the parent
Composes against the inherited contracts: this subtree's `../contracts/` (`BAR-248..255` sub-range,
per-chapter gating set, per-BAR field set, sub-fragment layout, proposed_stage convention), the UX partition
(`../../contracts/`, screens owns `BAR-230..264`), the release-bar partition (`../../../contracts/`, UX owns
`BAR-200..299`), and the DAG-root schema (`../../../../contracts/`, `BAR-<NNN>`, closed verification_methods
vocab, stage vocab). `SUBTASK_bar_screens_synthesis` will assemble this fragment with its four siblings into
`SUBTASK_bar_ux_screens/outputs/bar-ux-screens.md`, finalize the within-screens staging, and assert the
sub-identities.

## Success criteria — met
- [x] Composes against the inherited contracts; `BAR-*` only within `BAR-248..255`; no inherited schema redefined.
- [x] Every release-gating `REQ-UX-*` in the chapter referenced by ≥1 `BAR-*` (11 of 11).
- [x] Every `BAR-*` names a verification method from the frozen vocabulary, references ≥1 `REQ-*`, carries a proposed_stage.
- [x] No `BAR-*` justified solely by a non-gating `REQ-UX-*` (071, 072 out of coverage).
- [x] Coverage note lets the synthesis gate assert account-lifecycle gating coverage without re-deriving the set.
- [x] Repository hygiene: no host/system/taskflow detail, no attribution trailer.

## Note for the synthesis gate (taskflow-internal; kept out of the repository deliverable)
The Phase-B `design` methodology loader was unavailable in this environment (`agent_domain_unset`, run-wide, as
the subtree hub records). Per the hub's methodology posture, this chapter was authored by applying the
product-designer persona's release-definition judgment and the relayed bundle guidance (Release Definition
primary; Experience Design, Product Strategy supporting) rather than blocking. This note is internal and is not
present in `outputs/bar-screens-account-lifecycle.md`.
