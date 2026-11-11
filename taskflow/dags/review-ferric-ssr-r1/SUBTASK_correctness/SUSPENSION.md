# SUBTASK_correctness — Suspension Record

## Status: SUSPENDED (NeedsDecompose)

## Decomposition Summary

This node decomposed PR #228 correctness review into four children:

| Child | Scope | Depends on |
|-------|-------|------------|
| SUBTASK_ssr_render | REQ-SSR-001–005 (render_to_string SSR path) | none |
| SUBTASK_hydration | REQ-HYD-001–004 (hydrate() WASM path) | none |
| SUBTASK_axum_mismatch | REQ-SSR-006, REQ-MIS-001–002, non-goal REQ-SSR-007 | none |
| SUBTASK_correctness_synthesis | Verification gate: cross-check + assemble correctness_findings.md | all three spokes |

## Decomposition Rationale

The brief explicitly enumerates three distinct component areas with separate acceptance criteria:
- **#223 — render_to_string** (server-side Rust code, 5 criteria)
- **#224 — hydrate()** (client-side WASM code, 4 criteria)
- **#226 — Mismatch detection + Axum integration** (framework integration, 3 criteria + non-goal)

The enumerated-concerns rule and the Distinct Concerns Test fire: different specialists can independently
evaluate the SSR render path, the WASM hydration path, and the Axum integration layer. Per trigger precedence,
this scope signal overrides the token and output-size estimates (which were borderline Atomic).

## Resumption Condition

All child tasks reach a terminal lifecycle state.

## Cross-Cutting Concern Noted for Synthesis

The marker format (`data-hydration-id` or equivalent) is the seam between SSR and hydration. SUBTASK_ssr_render
documents it for REQ-SSR-004; SUBTASK_hydration documents it for REQ-HYD-004. SUBTASK_correctness_synthesis
cross-checks these for consistency and MUST NOT silently plug a failure.

## Named-State Authored

- `_GLOBAL.md` — subtree hub document
- `contracts/_MANIFEST.yaml` — findings schema, ownership, and cross-check identities
- `SUBTASK_ssr_render/_BRIEF.md` — spoke brief for #223
- `SUBTASK_hydration/_BRIEF.md` — spoke brief for #224
- `SUBTASK_axum_mismatch/_BRIEF.md` — spoke brief for #226 + non-goal
- `SUBTASK_correctness_synthesis/_BRIEF.md` — synthesis/gate brief
