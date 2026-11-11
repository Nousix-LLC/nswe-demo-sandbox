# Task: Ferric 1.0 — the release bar (concern 9a)

## Task Specification
**Slug**: SUBTASK_release_bar
**Task Kind**: standard
**Status**: Pending

### Objective
Consolidate the eight concern designs into the single, testable **Ferric 1.0 release bar**: a concrete
statement of what "a real 1.0 framework" means for Ferric, held against what frameworks of its kind provide —
not "it compiles" or "the examples run". Own the `BAR-FERRIC-*` register.

### Context
Part of the Ferric 1.0 framework design (see `../_GLOBAL.md`). This mirrors the repo's existing
`design/release-bar.md` shape, adapted to a framework: `BAR-FERRIC-*` criteria, each with a statement, the
`REQ-*` it enforces, a `verification_method` from the contract vocabulary, and a `stage` (`usable_early` |
`one_oh`). SSR+hydration is the gating **must-have** (identity I4).

**Dependencies**: `SUBTASK_scope_and_requirements` and all seven capability spokes (SSR, authoring, async,
router/http, docs/DX, release, performance) — it reads every `REQ-*` register and consolidates.

### Distinct concerns to cover (name them; let your own evaluation decide how to split)
- **MVP-vs-1.0 staging**: the two-stage cut (usable-early vs. one_oh) applied across the design, with the
  principle that separates them. No hidden cuts.
- **The bar**: the `BAR-FERRIC-*` criteria, each checkable by a stranger via a named verification method, each
  referencing the `REQ-*` it enforces.
- **Completeness & gap review**: a deliberate sweep over the surfaces a **framework/library** of Ferric's kind
  is expected to have (reactivity, rendering, SSR/hydration, authoring ergonomics, async/data, routing, HTTP,
  docs/DX, release/semver, performance, accessibility-of-output, testing story, MSRV), recording covered /
  out-of-1.0 / gap with a reason for each — so the out-of-1.0 items (styling, devtools, hot reload,
  desktop/mobile) are recorded decisions, not oversights.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context + constraints. |
| Contract | `../contracts/` | `BAR-FERRIC-*` schema, verification + stage vocabularies, trace rules (I2–I5). |
| All REQ registers | `../SUBTASK_scope_and_requirements/scope-and-requirements.md` and each `../SUBTASK_*/<area>.md` | The `REQ-*` each bar criterion enforces; read every one. |
| Repo precedent | `design/release-bar.md` (chirp) | The release-bar document shape to match. |

### Declared output
- `release-bar.md` (this task's workspace) — MVP-vs-1.0 staging, the `BAR-FERRIC-*` criteria, and the
  completeness & gap review. Repo target `design/ferric/release-bar.md`.

### Success criteria
- [ ] Every `BAR-FERRIC-*` has a statement, `references` to real `REQ-*` ids (identity I2), a
      `verification_method` from the contract vocabulary, and a `stage`.
- [ ] Every `one_oh`-gating `REQ-*` across all registers is enforced by ≥1 criterion (identity I3); a coverage
      map (REQ → BAR) is included.
- [ ] ≥1 `one_oh` criterion marks SSR+hydration as the must-have (identity I4).
- [ ] The out-of-1.0 items are recorded in the gap review and enforced by no criterion (identity I5).
- [ ] The bar is testable, not aspirational: every criterion is checkable against the framework by someone who
      was not in the room.

### Constraints
- Own `BAR-FERRIC-*`; do not redefine any `REQ-*` (identity I1). Design, not implementation.
- Honor the writing-voice rules; run the avoid-ai-writing pass before finalizing.
