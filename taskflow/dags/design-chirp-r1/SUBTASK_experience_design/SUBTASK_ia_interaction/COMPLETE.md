# COMPLETE — SUBTASK_ia_interaction

## What was done
Designed chirp's information architecture and interaction model and published the canonical screen
inventory the experience-design siblings compose against. Produced the `information_architecture_and_interaction`
section content at `outputs/ia-interaction.md`, covering:

- **Screen inventory** (under the exact heading the internal contract requires) — every screen a
  releasable chirp needs, grouped signed-out / signed-in / dialogs, each with a user-facing route, one of
  the seven archetypes (feed/list, form, profile, settings, modal/dialog, confirmation, empty/landing), its
  auth state, and its purpose. This is the shared vocabulary the dependency edges carry to
  `SUBTASK_visual_system`, `SUBTASK_screens_flows`, `SUBTASK_responsive`, `SUBTASK_accessibility`.
- **Navigation & wayfinding** — the signed-out shell vs the signed-in shell, the global navigation set,
  current-location indication, and the designed paths between the no-session / new-session / established-session
  account states.
- **Interaction conventions** — addressable screens & deep-linking, auth-gated routing with return-to,
  mid-use session-expiry interception, browser back/forward behavior, bounded pagination & catch-up,
  destructive-action confirmation, transient feedback, and the sign-up / sign-in / sign-out transitions.
- **REQ-UX-001..019** — nineteen testable requirements, each with a stranger-checkable acceptance
  criterion, a `release_gating` flag, and ≥1 `REQ-PROD-*` reference.

## Decompose evaluation
Atomic. The three concerns the brief named (screen inventory, navigation, interaction conventions) are
mutually-defining facets of one responsibility — one section, one shared vocabulary (the screen inventory
is the spine both the nav shells and the conventions are defined over), one tight 19-id range — not
separable parallel analyses. Output size was the only near-boundary trigger and, per Trigger Precedence,
does not override the single-responsibility finding. Executed in one invocation.

## Composition against contracts
- Used the parent `REQ-UX-NNN` format and field set (`id`, `statement`, `acceptance_criteria`,
  `release_gating`) plus the trace rule (`references` ≥1 `REQ-PROD-*`); redefined nothing.
- Stayed within the assigned id range REQ-UX-001..019 (all 19 ids minted, unique, in range).
- Published the "Screen inventory" in the shape `../contracts/ux_section_and_id_map.yaml` requires
  (screen name, route, archetype, auth state, purpose).
- Two requirements are `release_gating: false` with one-line reasons (REQ-UX-015 flow cross-linking;
  REQ-UX-019 notifications entry), consistent with the non-gating product requirements they ride
  (REQ-PROD-029, REQ-PROD-042).

## Surfaces covered (against the contract's required_surfaces)
first-visit landing, sign-up, sign-in, recovery, sign-out, home timeline, compose, reply/conversation,
view profile (and followers/following), discovery/explore, onboarding, edit profile, account settings,
notification prefs, sessions/devices, data export, account deletion, notifications, report & block/mute,
help/support entry, rules/terms, and the global considered-states conventions (empty/loading/error,
expired-session recovery) as interaction conventions the per-screen flows apply.

## Environment limitation (taskflow-internal note; not in the repository output)
The `design` methodology-loader syscall reported the agent domain unset in this reconstructed environment
(the condition the subtree hub anticipates). Per the hub's instruction this did not block: the section was
designed from the named bundle intent (Experience Design primary; Product Strategy support) and
product-design competence, and this limitation is recorded here rather than in the deliverable, which is
kept repository-ready.

## Output
- `outputs/ia-interaction.md`

## Hygiene
No host/system/taskflow detail, workspace paths, agent/DAG/run ids, or attribution trailers appear in the
deliverable content.
