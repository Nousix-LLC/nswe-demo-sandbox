# COMPLETE — SUBTASK_accessibility

## Status
Completed (Atomic). One responsibility, one output section + its REQ-UX register.

## What was done
Designed the `accessibility` section of `experience-design.md` and minted `REQ-UX-100..119`.

- **Named the standard**: chirp conforms to **WCAG 2.1 Level AA**, consistent with the floor the
  visual system already references, and formalized as the concrete form of REQ-PROD-036 (which left the
  exact standard to this design). Scoped the gated conformance set (core loop + get-in screens +
  considered states) versus the whole product, and recorded WCAG 2.2 AA as the near-term direction
  (one 2.2 criterion, minimum target size, adopted early and flagged non-gating).
- **Designed to it** across the five concern areas in the brief:
  - *Operability* — keyboard operability on every archetype and both nav shells, logical focus order +
    visible focus (composing with REQ-UX-025), no keyboard trap with escapable/returning modal focus,
    bypass-to-content, and a minimum target size.
  - *Semantics* — a per-component name/role/state mapping over the whole component library, landmark
    regions, one-h1 nested headings tied to the wayfinding model, list/feed semantics, and icon-label
    exposure (composing with REQ-UX-028).
  - *Perception* — contrast as a condition of the standard (composing with REQ-UX-022), resize/reflow/
    text-spacing, no-colour-alone + no-flash, and reduced motion (composing with REQ-UX-029).
  - *Feedback & errors* — status live-region announcements, errors announced and field-associated,
    and empty/loading/expired-session states reaching assistive technology (the accessible counterpart
    of the considered-states work, tracing to REQ-PROD-033/034).
  - *Verification* — a three-way per-release check (automated scan per theme, keyboard-only pass,
    screen-reader core-loop pass) over the gated set against a stated AT/browser matrix, and the gate.

## Output produced
- `outputs/accessibility.md` — the `accessibility` section content and `REQ-UX-100..119` entries.

## How it composes with the parent subtree
- Owns exactly `section:accessibility` and the id range `REQ-UX-100..REQ-UX-119` assigned in
  `../contracts/ux_section_and_id_map.yaml`; writes no other section and mints no id outside the range.
- Composes against the **screen inventory** (archetypes/screens) from `SUBTASK_ia_interaction` and the
  **component library** + palette + motion from `SUBTASK_visual_system`, referring to both by their
  published names.
- Uses the parent `REQ-UX` field set and section name; does not redefine the scheme, section list, or
  ranges. References the sibling visual-system requirements that carry accessibility weight
  (REQ-UX-022/025/028/029) rather than duplicating them.
- Satisfies the subtree identities for this section: every `REQ-UX-100..119` has a statement, a
  stranger-checkable `acceptance_criteria`, and a `release_gating` flag, and references ≥1 `REQ-PROD-*`
  (ID_UNIQUE_IN_RANGE, UX_TESTABLE_AND_GATED, UX_TRACES_TO_PROD, COMPOSES_AGAINST_PARENT). Ready for
  `SUBTASK_synthesis` to assemble and fold.

## Environment note
The methodology-loader syscall reported the agent domain unset in this reconstructed environment; per
the brief and `../_GLOBAL.md` §Methodology posture, the accessibility design was produced from the
Experience Design bundle intent and product-design competence, citing the actual standard (WCAG 2.1 AA
/ 2.2) over asserting best practice. This did not block the work.
