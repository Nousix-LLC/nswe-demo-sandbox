# COMPLETE — SUBTASK_considered_states

## What was done
Designed the `empty_error_loading_states` section of the screens-&-flows deliverable: the
product-wide empty / loading / error patterns every chirp screen obeys, plus the expired-session /
transient-error recovery that routes the person to sign-in with their place explained and preserves
a drafted chirp. Minted `REQ-UX-086..089`.

## Output produced
- `outputs/empty-error-loading-states.md` — the `empty_error_loading_states` section (the four
  product-wide patterns, how per-screen states compose against them) and the `REQ-UX-086..089`
  register. Repository-ready; no host/system/taskflow detail, no workspace paths, no attribution.

## How it composes with the contract and frozen vocabularies
- **Composed, not invented.** Each pattern is expressed over the component library's named states
  (`EmptyState`, `LoadingState`, `InlineError`, `InlineFeedback`, `Toast`, and the
  `ListView`/`ChirpCard`/`ProfileHeader`/`Avatar` states, plus `ComposeBox` draft-preservation and
  `Dialog` error behaviour). No new component or state is introduced.
- **Session-expiry convention referenced, not redefined.** The recovery pattern composes against the
  IA's `REQ-UX-008` and auth-gated return `REQ-UX-007`; it states how the product's state treatment
  carries a person through, and leaves the IA convention as the owning definition.
- **Id range honoured.** `REQ-UX-086..089` only — four ids, unique, in-range. Each has a
  `statement`, a stranger-checkable `acceptance_criteria`, a `release_gating` flag, and ≥1
  `REQ-PROD-*` trace (086/087/088 → REQ-PROD-033; 089 → REQ-PROD-034).
- **Cross-reference seam set once.** This section is the global treatment the four surface-cluster
  spokes compose their per-screen states against; `SUBTASK_synthesis` asserts `STATES_CONSISTENT`
  across the assembled whole.

## Success criteria (self-checked)
- [x] Composes against `../contracts/` and the component library; patterns expressed over named
      component states, not new inventions.
- [x] Empty, loading, error, and expired-session/transient-error recovery (keep-the-draft) each
      designed as a product-wide pattern a stranger could check on the live product.
- [x] Every `REQ-UX-086..089` is testable, `release_gating`-flagged, unique, in-range, and traces to
      ≥1 `REQ-PROD-*` (033/034).
- [x] Design-only; repository-ready hygiene throughout; plain, checkable human voice; avoid-ai-writing
      checklist run over the narrative by hand against the P0/P1 patterns.

## Limitation recorded
The Phase-B `design` methodology loader was unavailable in this reconstructed environment (the
loader syscall reported the agent domain unset), exactly as the subtree hub's methodology posture
anticipated. Per that posture, the section was designed from the **Experience Design** bundle intent
and product-design competence; the limitation did not block the work. (Recorded here, not in the
repository-ready deliverable.)
