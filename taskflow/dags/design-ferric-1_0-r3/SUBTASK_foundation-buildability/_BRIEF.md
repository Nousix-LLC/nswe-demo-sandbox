# _BRIEF.md — SUBTASK_foundation-buildability

## Task Specification

**Slug**: SUBTASK_foundation-buildability  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending

### Objective

Evaluate concern 4: **Buildability on the existing foundation**.

Read the key design documents (particularly `ssr-hydration.md`, `authoring-model.md`, `router-and-http.md`, and `scope-and-requirements.md`) alongside the existing codebase (`crates/ferric/`, `crates/ferric-router/`, `crates/ferric-http/`). Determine whether the design's technical assumptions are aligned with what is already in place.

Specifically:

- Does the design correctly characterize what exists today (signals, component model, vdom, router prelude, http prelude) at baseline commit `276138f`?
- Does the SSR + hydration architecture in `ssr-hydration.md` make sound assumptions about the existing reactive runtime and component model? Are there design decisions that would require rewriting or breaking the existing frozen prelude surfaces?
- Does `router-and-http.md` accurately describe the existing frozen `ferric-router` and `ferric-http` prelude surfaces? Does it extend them additively without breaking them?
- Does `authoring-model.md` correctly describe what already exists and what must be built?
- Are there any design decisions that would require rewriting existing landed work (`ferric-foundation`, `ferric-router`, `ferric-http`)?

This is a **design-to-code alignment check**, not a code review. The question is whether the design makes correct and buildable assumptions about the foundation, not whether the code is well-written.

### Context

This task is part of the Ferric 1.0 design gap review (see `_GLOBAL.md` in the parent workspace at `taskflow/dags/design-ferric-1_0-r3/`).

**Depends on**: none (runs in parallel with design-doc-review and ticket-review)  
**Dependents**: SUBTASK_synthesis depends on this task's output

### Inputs

| Input | Source | Purpose |
|---|---|---|
| Parent hub | `taskflow/dags/design-ferric-1_0-r3/_GLOBAL.md` | Shared context |
| Findings schema | `taskflow/dags/design-ferric-1_0-r3/contracts/findings_schema.yaml` | Output format contract |
| Key design docs | `git show origin/work/design-ferric-1_0:design/ferric/<file>` from `taskflow/dags/ferric-foundation/checkout/` | Design assumptions to verify |
| Existing codebase | `taskflow/dags/ferric-foundation/checkout/crates/` | What is already built |
| Contracts file | `taskflow/dags/ferric-foundation/contracts/ferric_api.rs` | Frozen API surface contract |

Design files to read for this concern:
- `scope-and-requirements.md` (sections on what Ferric is today, grounded at `276138f`)
- `ssr-hydration.md` (the must-have — check technical assumptions about existing runtime)
- `authoring-model.md` (check what is claimed as existing vs. new)
- `router-and-http.md` (check alignment with frozen `ferric-router` and `ferric-http` preludes)

Existing code to read:
- `crates/ferric/src/lib.rs` — prelude surface
- `crates/ferric/src/signal.rs` — reactive runtime
- `crates/ferric/src/component.rs` — component model
- `crates/ferric/src/vdom.rs` — virtual DOM
- If `ferric-router` and `ferric-http` exist in the checkout: their `src/lib.rs` and prelude modules
- `taskflow/dags/ferric-foundation/contracts/ferric_api.rs` — the frozen API contract from the foundation DAG

### Methodology

Apply `release-definition/ReleaseDefinition_CompletenessAndGapReview_Methodology.md` for the gap identification process. For foundation alignment specifically: verify each design claim about existing state against the actual source, and for each design extension, verify it would be additive rather than breaking.

### Output

| Attribute | Value |
|---|---|
| Filename | `buildability-findings.md` |
| Format | YAML conforming to `contracts/findings_schema.yaml` |
| Location | `SUBTASK_foundation-buildability/` (this workspace) |

The output is a YAML file with:
- `spoke: foundation-buildability`
- `concern_ids: [4]`
- `findings: [...]` — one entry per finding
- `summary: { blocking_count, non_blocking_count }`

A finding is BLOCKING if the design makes an assumption that is demonstrably wrong about the existing foundation (e.g., assuming a function exists that does not, or designing an SSR extension that would require breaking the frozen prelude). A finding is non-blocking if the design correctly understands the foundation but a clarification or small adjustment would improve alignment.

### Success Criteria

- Design documents listed above are all read.
- Existing codebase files listed above are all read.
- Each design claim about what "already exists" is verified against the actual code.
- Each design claim about what "must be built" is checked to confirm it does not conflict with existing frozen surfaces.
- Output file `buildability-findings.md` written at this workspace, conforming to the findings schema.
- A BLOCKING finding about a foundation conflict names the specific design claim and the specific existing code that contradicts it.
