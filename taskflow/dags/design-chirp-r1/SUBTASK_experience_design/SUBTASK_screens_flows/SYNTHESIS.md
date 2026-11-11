# SYNTHESIS — screens-&-flows subtree (verification gate + fold)

This is the fold record for the `SUBTASK_screens_flows` subtree. It assembles the five spoke outputs
into the single deliverable `outputs/screens-flows.md`, consolidates the `REQ-UX-040..089` register,
asserts this subtree's nine contract identities with recorded evidence, and folds this subtree root to
COMPLETED so the parent experience-design subtree can consume `screens-flows.md` as its
`screens_and_flows` and `empty_error_loading_states` sections.

This invocation is a reconstructed resume of the synthesis node. An earlier invocation had assembled the
deliverable and written a fold record but did not reach the terminal fold, so the node was reconstructed
and re-dispatched. Because an agent carries no memory across invocations, this run re-verified the
assembled whole from the five spoke outputs and the contract from scratch, with its own recorded
evidence, rather than trusting the earlier record. The verdict below is this run's own.

## What was assembled

`outputs/screens-flows.md` (2,568 lines) carries, in the order the contract fixes
(`contracts/screens_seam.yaml` `sections`):

1. **Screens and flows** — four cluster parts, in order:
   - *Getting in* (entry and authentication) — from `SUBTASK_get_in`.
   - *The core loop* (reading, posting, reacting, finding people) — from `SUBTASK_core_loop`.
   - *Account lifecycle* (onboarding, management, leaving) — from `SUBTASK_account_lifecycle`.
   - *Safety, notifications, and public-explanatory surfaces* — from `SUBTASK_safety_notifications`.
2. **Empty, error, and loading states** — the product-wide patterns — from `SUBTASK_considered_states`.
3. **Requirements and acceptance criteria — REQ-UX-040..089** — the consolidated register: the five
   spokes' REQ-UX entries gathered by cluster into one register, so the deliverable states each design
   once as narrative and each requirement once in the register.

Each section-part is written by exactly one spoke per `contracts/_MANIFEST.yaml` ownership. This run
assembled and verified only; no screen was re-designed and no `REQ-UX` id was minted or renumbered. The
assembled deliverable already existed as this node's owned output from the earlier invocation; this run
confirmed it is a faithful, complete assembly of the five spoke outputs (see FAITHFUL_ASSEMBLY below) and
adopted it rather than regenerating identical content.

## How the identities were verified

The mechanical identities were checked by two authored scripts in this task's `calculations/`:
`verify_synthesis.py` (section order, id uniqueness and range, faithful assembly, field/gating/trace
coverage, hygiene) and `verify_surfaces.py` (per-screen structure, surface coverage, vocabulary use).
Both read the five spoke outputs and the assembled deliverable and print a per-check verdict; both are
re-runnable and reproducible from the files. They were run with the local Python interpreter rather than
the `engine_compute` coprocessor (see *Environment limitations*). `verify_synthesis.py` reports 7/7
PASS. The design-judgment identities (not-skeletal, composes-against-vocabulary, states-consistency) were
confirmed by reading the assembled prose, using `verify_surfaces.py` to direct the reading to every
designed screen and to any screen a mechanical marker flagged.

## Identity evidence (contracts/_MANIFEST.yaml) — all asserted, none plugged

1. **SECTION_PART_COVERAGE — PASS.** Both sections are present and assembled in contract order. An
   anchored heading scan finds the byte offsets strictly increasing: `## Screens and flows` → `### Getting
   in` → `### The core loop` → `### Account lifecycle` → `### Safety, notifications…` → `## Empty, error,
   and loading states` → `## Requirements and acceptance criteria — REQ-UX-040..089`. Every section-part
   maps to exactly one owning spoke per the ownership map; `empty_error_loading_states` comes from its one
   owner. No section-part is unowned (no hole) and none appears twice (no double-write). (An earlier
   substring check had mis-ordered this by matching a per-screen `##### Empty, error, and loading states`
   sub-heading inside the account-lifecycle part; anchoring the match to the line-start heading level
   resolved it. The ordering was correct; the first check was not.)

2. **ID_UNIQUE_IN_RANGE — PASS.** The register carries exactly 50 heading-level entries, 50 distinct,
   contiguous `040..089`, no collision, no out-of-range id, no gap. Each spoke minted its whole sub-range
   and only its sub-range, read from each spoke's own entry headings: get_in `040..050` (11), core_loop
   `051..064` (14), account_lifecycle `065..077` (13), safety_notifications `078..085` (8),
   considered_states `086..089` (4) — 11+14+13+8+4 = 50. The union of the spokes' minted ids equals the
   assembled register exactly, so nothing was dropped, duplicated, or renumbered in assembly. The spokes
   also *reference* a few other-area ids (`REQ-UX-007/008/014/015/016`, owned by `SUBTASK_ia_interaction`
   and `SUBTASK_visual_system`) as cross-references; those are not register entries here and are counted
   as references, not mints — the id check reads mints from headings, not from any occurrence.

3. **SURFACE_COVERAGE — PASS.** Every surface in the parent `required_surfaces` checklist
   (`../contracts/ux_section_and_id_map.yaml`, 21 surfaces), plus the two screen-inventory screens the
   seam adds (`rules_and_terms`, `not_found`), is designed with its empty/error/loading states by its
   owning spoke. The `## Screens and flows` section carries 26 designed screen/group headings covering:
   Landing, Sign up, Sign in, Recover access + Set new credential, Sign out; Home timeline (incl. bounded
   catch-up), Posting and conversation, Social actions (like, follow), Profiles/Followers/Following +
   Explore/discovery; Onboarding, Edit profile, Settings hub + Account & contact + Notification
   preferences + Sessions & devices, Export your data, Delete account; Notifications, Report, Block/mute,
   Blocked & muted, Help & support, Rules & terms, Not found; and the cross-cutting considered-states
   section owns `considered_states_global`. Where a state does not apply to a surface — a toggle control
   (like/follow) has no *empty* state; `Not found` is itself the resolved answer to an absent resource —
   the design records the reason in prose rather than leaving it silent. No required surface is out of
   scope silently.

4. **NOT_SKELETAL — PASS.** Each designed screen specifies its layout, its content, its one primary
   action, and its empty, error, and loading states — not a bare route name. `verify_surfaces.py` flagged
   three headings for a missing marker; each was read and confirmed legitimate, not a hole: *"The
   transitions between these screens"* is connective flow text stitching the auth screens (composing
   against the IA model REQ-UX-007/008/014/015/016), not a screen; *"Social actions"* is a controls part
   whose like and follow controls carry default/active, error, and loading states but no *empty* state,
   because a two-state toggle has none; *"Account & contact"* uses `##### Composition` / `##### Layout`
   sub-headings carrying the full content rather than the literal word "content", and is designed down to
   its SettingRows, verification-status caution, and states. The other 23 headings carry all four parts
   outright.

5. **UX_TESTABLE_AND_GATED — PASS.** Every one of the 50 register entries carries a `statement`, an
   `acceptance_criteria` a stranger could exercise on the live product, and a `release_gating` flag. The
   count is 43 `true` and 7 `false`; each `false` carries a one-line reason on the flag line, and the
   check finds no bare `false`. The seven non-gating entries ride product requirements that are themselves
   non-gating (conversation reading on REQ-PROD-004, discovery/Explore on REQ-PROD-042, notifications on
   REQ-PROD-029, block/mute on REQ-PROD-027, handle-change on REQ-PROD-018, and the stay-signed-in / second
   theme staging).

6. **UX_TRACES_TO_PROD — PASS.** Every one of the 50 register entries references at least one
   `REQ-PROD-*`; the trace check finds no entry without one.

7. **COMPOSES_AGAINST_VOCAB — PASS.** Every screen refers to screen-inventory screens by their inventory
   names and routes (`/`, `/signup`, `/signin`, `/recover`, `/recover/confirm`, `/compose`, `/explore`,
   `/welcome`, `/settings…`, `/notifications`, `/help`, `/rules`, and the rest) and is built from
   component-library components by name. All 18 library components appear by name across the section
   (`NavShell`, `ListView`, `ChirpCard`, `ComposeBox`, `ProfileHeader`, `Avatar`, `SettingRow`, `Toggle`,
   `Dialog`, `Toast`, `InlineError`, `InlineFeedback`, `EmptyState`, `LoadingState`,
   `Primary/Secondary/IconButton`, `TextField`). No screen or component outside the frozen vocabularies is
   introduced, and no additive contract amendment was required.

8. **STATES_CONSISTENT — PASS.** The `empty_error_loading_states` section sets the four conditions —
   empty, loading, error, and the expired-session / transient-error recovery — over the component
   library's own named states (`EmptyState`, `LoadingState`, `InlineError`, `InlineFeedback`, `Toast`, and
   the `ListView` / `ChirpCard` / `ProfileHeader` / `Avatar` states) and the information architecture's
   session-expiry convention (REQ-UX-007/008). The four surface-cluster spokes set each screen's own
   states by composing those component states with these global patterns: an empty surface is visibly
   distinct from a failed load, a load shows real-dimension skeletons and never spins forever, an error
   is shown at the point of action in plain words with a way forward, and an expired session routes to
   sign-in while the drafted chirp is preserved. Reading the per-screen states (timeline, social controls,
   account & contact, dialogs) found no spoke inventing a pattern that conflicts with the global
   treatment.

9. **HYGIENE — PASS.** A scan of the assembled `outputs/screens-flows.md` for host/system/taskflow tokens
   — `taskflow`, `SUBTASK_`, `_GLOBAL`, `_BRIEF`, `workspace`, filesystem paths, the server address,
   `kubectl`/`k3d`/`argocd`, `Co-Authored-By`, `Claude Code`, the request/process ids, and the account
   name — returns zero occurrences. A separate machine-writing-tell pass (the avoid-ai-writing checklist,
   applied by hand against the P0/P1 tells) found only five uses of "genuinely empty" — a real product
   distinction between an empty surface and a failed-to-load one, not a hollow intensifier — and one "not
   only the happy path" contrast with both halves named; no `honest`-on-an-abstraction, no slot-fill
   template, no padded triad. The deliverable reads as a product document. No tell warranted a change, and
   re-writing spoke prose is outside this gate's scope.

## Remediation

None required. All nine identities passed; no identity failed, so no remediation subtree was decomposed
and no hole was plugged.

## Environment limitations (recorded, not blocking)

1. **Methodology loader unavailable.** The Phase-B `design` methodology loader reported the agent domain
   unset in this reconstructed environment, so the methodology bundle bodies could not be loaded. Per the
   subtree hub's recorded posture, verification and assembly proceeded from the frozen contract and
   product-design competence — Experience Design (primary), with Identity & Trust and Product Strategy as
   support for the auth and account surfaces — and this limitation is recorded rather than blocking the
   fold.
2. **Coprocessor not used; local interpreter instead.** The verification scripts were run with the local
   Python interpreter against the authoritative tree the brief relayed, rather than through the
   `engine_compute` coprocessor (an earlier run recorded the coprocessor resolving to a stale
   reconstruction snapshot). The scripts are saved under this task's `calculations/` and are re-runnable;
   the evidence they produced is reproducible from the files.

## Fold

The five spoke dependencies — `SUBTASK_get_in` (COMPLETE), `SUBTASK_core_loop` (SYNTHESIS, itself
decomposed and folded), `SUBTASK_account_lifecycle` (SYNTHESIS, itself decomposed and folded),
`SUBTASK_safety_notifications` (COMPLETE), `SUBTASK_considered_states` (COMPLETE) — are all terminal with
their outputs observable. This synthesis task has produced `outputs/screens-flows.md` (both sections in
order plus the consolidated `REQ-UX-040..089` register) and this `SYNTHESIS.md`. On the strength of the
identity evidence above, the subtree root `SUBTASK_experience_design/SUBTASK_screens_flows` folds
`SUSPENDED → COMPLETED`; its result is `outputs/screens-flows.md`, consumed by the parent experience-design
synthesis as the `screens_and_flows` and `empty_error_loading_states` sections and as the
`REQ-UX-040..089` slice of the whole `requirements_and_acceptance_criteria` register.
