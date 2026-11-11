# COMPLETE — SUBTASK_responsive

## What was done
Designed chirp's responsive behaviour and authored the `responsive_layout` section plus the
`REQ-UX-090..099` register at `outputs/responsive.md`. The section specifies, as design intent (what,
not how):

- A phone-first strategy and three breakpoints (`breakpoint.compact` < 640px, `breakpoint.medium`
  640–1023px, `breakpoint.wide` ≥ 1024px), anchored to the 600px reading measure.
- How the signed-in and signed-out `NavShell` reflow across the three ranges (bottom tab bar + top bar
  on compact → side navigation on medium/wide), keeping every destination reachable and the active one
  marked.
- How each of the seven screen archetypes (feed/list, form, profile, settings, modal/dialog,
  confirmation, empty/landing) adapts — what stacks, collapses, goes full-screen, and stays reachable.
- Touch-target minimums (44×44 CSS px, ≥8px between targets), thumb reachability of the core-loop
  actions, and input ergonomics (no auto-zoom on field focus, no horizontal scroll, portrait and
  landscape).
- The release floor: the core loop fully usable on a phone (REQ-UX-090 → REQ-PROD-035).

## Output
- `outputs/responsive.md` — the `responsive_layout` section content and `REQ-UX-090..099` entries.

## How it composes with the subtree
- Owns exactly the `responsive_layout` section and the `REQ-UX-090..099` id range per
  `../contracts/ux_section_and_id_map.yaml`; introduces no section or id outside that range.
- Composes against the screen inventory (`SUBTASK_ia_interaction`) and the component library + design
  tokens (`SUBTASK_visual_system`); refers to screens, archetypes, components, and tokens by their
  published names and redefines none of them.
- Each `REQ-UX-09x` carries the parent field set (`id`, `statement`, `acceptance_criteria`,
  `release_gating`) plus the `references` trace, and names ≥1 `REQ-PROD-*` per the trace rule.
- `SUBTASK_synthesis` assembles this section into `experience-design.md` and folds the subtree.

## Verification against success criteria
- [x] Composes against `../contracts/`, the screen inventory, and the component library.
- [x] Breakpoints and per-archetype + nav-shell adaptation are specified concretely.
- [x] The phone-usable core loop is stated as a testable requirement (REQ-UX-090).
- [x] Every `REQ-UX-090..099` is testable by a stranger, release-gating-flagged, and traces to ≥1
      `REQ-PROD-*`. Ids: 090–099, ten entries, unique and in range.
- [x] Repository-ready hygiene: no host/system/taskflow detail, workspace paths, agent/DAG/run ids, or
      attribution trailer in the output content.

## Recorded limitation
The `design`-domain methodology-loader syscall reports the agent domain unset in this reconstructed
environment, so the Experience Design bundle body could not be loaded on demand. Per the brief and the
subtree hub, the responsive design was produced from the named bundle intent and product-design
competence; the limitation is recorded here and did not block the work. (This note is taskflow-internal
and is deliberately kept out of the repository-ready output.)
