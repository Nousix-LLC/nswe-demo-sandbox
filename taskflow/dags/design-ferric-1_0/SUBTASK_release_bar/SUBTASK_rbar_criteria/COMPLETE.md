# COMPLETE — SUBTASK_rbar_criteria

## Task

Produce `bar-criteria.md`: the complete `BAR-FERRIC-*` register for Ferric 1.0, derived from all
eight spoke REQ-* registers and the gap analysis.

## What was produced

**`bar-criteria.md`** — 27 criteria (BAR-FERRIC-001 through BAR-FERRIC-027) in two parts:

- **Part 1 — Criteria**: one criterion per logical surface from the gap analysis, staged
  `usable_early` (001–016) or `one_oh` (017–027), each with a checkable statement, ≥1 REQ-*
  reference, and a verification method drawn from the schema vocabulary.
- **Part 2 — Coverage map**: 57 one_oh-gating REQ-* IDs mapped to their enforcing BAR-FERRIC-*
  criterion.

## Identity verification

- **IA** (every covered surface has ≥1 BAR): 19 surfaces in gap-analysis.md with status=covered;
  all 19 are addressed. Satisfied.
- **IB / I5** (no criterion references an out-of-1.0 surface): no BAR-FERRIC-* references
  REQ-FW-015..018, streaming SSR, server functions, islands, or URL query parameters. Satisfied.
- **I2** (every BAR references ≥1 real REQ-* id): all referenced ids are drawn from the gap
  analysis, which names them as existing in the spoke design outputs. Satisfied.
- **I3** (every one_oh-gating REQ-* covered by ≥1 BAR): the coverage map lists 57 REQ-* ids across
  REQ-FW, REQ-SSR, REQ-API, REQ-ASYNC, REQ-HTTP, REQ-DX, REQ-REL, and REQ-PERF. Satisfied.
- **I4** (SSR+hydration marked must_have): BAR-FERRIC-018 carries `must_have: true`. Satisfied.
- **I5** (the four named out-of-1.0 items appear in gap-analysis with status=out-of-1.0 and no BAR
  enforces them): scoped CSS/styling, browser devtools, hot reload, desktop/mobile — all confirmed
  out-of-1.0 in gap-analysis.md; none referenced here. Satisfied.

## Staging summary

- **usable_early** (16 criteria): reactive state, view tree, view macro, basic props/children,
  context, async resources, forms, DOM events, routing, HTTP core, stable toolchain, frozen surfaces,
  diagnostics.
- **one_oh** (11 criteria): advanced slots/props, SSR resource seam, HTTP PATCH/timeout, SSR,
  hydration (must_have), reference app, publishing, semver/changelog, compat/MSRV policy, docs,
  zero-to-app starter, benchmarks, lean footprint.

## Declared output

`bar-criteria.md` at this workspace.
