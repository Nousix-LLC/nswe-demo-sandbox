# COMPLETE — SUBTASK_timeline_reading

## What was done
Designed the **Home timeline** (`/` signed-in, feed/list archetype) as a designed screen — its
layout, content, and primary action, and its empty / error / loading states — and minted the
`REQ-UX-051..053` register. Output: `outputs/screens-timeline-reading.md`.

## How it composes with the parent
This is the `timeline_reading` part of the core-loop screens subtree, assembled first (reading →
writing → reacting → identity/finding) by `SUBTASK_synthesis` into `../outputs/screens-core-loop.md`.
It owns the `home_timeline` surface and the `REQ-UX-051..053` sub-range per `../contracts/`.

## Success criteria (from `_BRIEF.md`)
- [x] Composes against `../contracts/`, the screen inventory, and the component library; nothing
      redefined — references `NavShell`, `ListView`, `ChirpCard`, `EmptyState`, `LoadingState`,
      `InlineError`, `Avatar`, the `space.measure` reading column, and the IA pagination/catch-up/back
      and session-expiry conventions, all by name; no screen or component invented.
- [x] The Home timeline is designed with its empty (brand-new/emptied), error (failed first page /
      load-older / catch-up, shown in place with retry, nothing discarded; expiry routed per IA), and
      loading (first-load skeletons, bounded load-older spinner, frame never blanks, nothing spins
      forever) states.
- [x] Layout, content, and a primary action are specified (bring the timeline current / read newest;
      catch-up is the screen-level primary action, load-older secondary, compose lives in the shell) —
      not a bare route name.
- [x] `REQ-UX-051`, `052`, `053` are each testable by a stranger on the live product, flagged
      `release_gating: true`, unique, within the assigned `051..053` sub-range, and each references
      `REQ-PROD-002`.

## Identities this surface supports (asserted later by `SUBTASK_synthesis`)
- SURFACE_COVERAGE — `home_timeline` designed with its three states; single owner.
- ID_UNIQUE_IN_RANGE — `051..053`, no collisions, in-range.
- NOT_SKELETAL — layout, content, primary action, and three states present.
- UX_TESTABLE_AND_GATED — each REQ-UX has statement + stranger-checkable acceptance_criteria + gating.
- UX_TRACES_TO_PROD — each references REQ-PROD-002.
- COMPOSES_AGAINST_VOCAB — screen and components referenced by name; nothing redefined.
- STATES_CONSISTENT — per-screen empty/error/loading states compose the component library's named
  states and the product-wide patterns (REQ-UX-086..089), including the expired-session / keep-the-
  draft recovery owned by the sibling considered-states surface; no conflicting per-screen treatment.
- HYGIENE — the deliverable carries no host/system/taskflow detail, no workspace paths, no
  agent/DAG/run ids, and no attribution trailer.

## Recorded limitation
The Phase-B `design` methodology loader was unavailable in this reconstructed environment (no
methodology filesets resolvable; agent domain unset). Per the ancestor hubs' recorded posture, the
surface was designed from the named bundle intent — Experience Design (primary), Product Strategy
(support) — and the product-design competence behind them. The limitation did not block the work and
is recorded here rather than in the repository-ready deliverable.

## Output
- `outputs/screens-timeline-reading.md`
