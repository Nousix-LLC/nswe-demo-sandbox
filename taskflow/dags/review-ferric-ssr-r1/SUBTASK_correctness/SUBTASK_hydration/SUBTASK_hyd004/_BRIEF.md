# SUBTASK_hyd004 — REQ-HYD-004: Marker Schema Consistency (data-hydration-id)

## Task Specification

**Slug**: SUBTASK_hyd004
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Determine whether the hydration code uses the same marker format (`data-hydration-id`) that the SSR
pass emits, whether the format is consistent between client (`hydrate`) and server (`render_to_string`),
and whether marker values are deterministic given the same component tree. Document the EXACT marker
schema (attribute name and value format) observed in the hydration code.

**This output is critical**: SUBTASK_hyd_synthesis cross-checks this against what SUBTASK_ssr_render
finds for REQ-SSR-004. The marker schema section is mandatory.

---

## Context

This task is part of the SUBTASK_hydration subtree (see `../_GLOBAL.md`).

**Dependents**: SUBTASK_hyd_synthesis reads `criterion_004.md` AND cross-checks the marker schema
against the SSR render spoke's finding. The `## Marker Schema` section of this output is a required
input to that cross-check.

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Shared context | `../_GLOBAL.md` | Constraints, shared inputs, methodology posture |
| PR diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | The change under review |
| Issue #224 | `gh issue view 224 --repo Nousix-LLC/nswe-demo` | REQ-HYD-004 acceptance text |
| Hydration source on branch | `gh api repos/Nousix-LLC/nswe-demo/contents/<path>?ref=work/ferric-ssr-r1 \| jq -r '.content' \| base64 -d` | hydrate() marker lookup code |

Search the branch for files containing `data-hydration-id`, `querySelector`, `get_attribute`,
`dataset`, or similar attribute-access patterns that read hydration markers.

---

## Review Scope

Evaluate **REQ-HYD-004** only:

> Does the hydration code use the same marker format (`data-hydration-id`) the SSR pass emits? Is
> the format agreed and consistent between server (`render_to_string`) and client (`hydrate`)? Are
> marker values deterministic given the same component tree?
> **Critical**: Document the exact marker schema (attribute name and value format).

What to check:
1. Identify every place the hydration code reads `data-hydration-id` (or whatever attribute name it
   uses) from the DOM.
2. Determine the exact attribute name used in the hydration code.
3. Determine the value format: is it an integer index, a component-type string, a hash, a path?
   Extract an example from the code.
4. Identify the mechanism that makes values deterministic (counter, deterministic hash, etc.).
5. If the SSR render source is accessible on the same branch, check whether it emits the same
   attribute name and value format. If not accessible, note that the cross-check depends on
   SUBTASK_ssr_render.
6. Flag any mismatch, non-determinism risk, or missing documentation as a finding.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| File | `criterion_004.md` |
| Location | this workspace (`SUBTASK_hyd004/`) |

### Output Structure

```markdown
# REQ-HYD-004 — Marker Schema Consistency

**Status**: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
**What was checked**: <what code paths were examined>
**Evidence**: `<file>:<line>` (or `<file>:<start>–<end>`)
**Finding** (if any): <description of the finding>

## Marker Schema (mandatory — for synthesis cross-check)
**Attribute name**: <exact attribute name string>
**Value format**: <description of the value format with example>
**Determinism mechanism**: <how values are made deterministic>
```

The `## Marker Schema` section is MANDATORY regardless of whether the status is CLEAN or FINDING.
SUBTASK_hyd_synthesis depends on it for the cross-check with SUBTASK_ssr_render.

---

## Success Criteria

- [ ] REQ-HYD-004 has a named, evidence-backed verdict (CLEAN or FINDING with severity)
- [ ] Evidence cites at least one file and line number in `Nousix-LLC/nswe-demo`
- [ ] `## Marker Schema` section is present with attribute name, value format, and determinism mechanism
- [ ] `criterion_004.md` exists at the declared path before task reports completed

---

## Suggested Methodology Files

**Task-type row matched**: "Ferric PR review (Rust library)" → Primary: `code-review`; Supporting:
`rust`, `framework-design`. Also applies: "SSR / hydration in a Rust UI framework" → Framework
Design + Rust.

Specific files:
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — SSR +
  hydration marker conventions in a Rust UI framework; what "agreed between server and client" means;
  determinism requirements for hydration markers.
- `code-review/CodeReview_Checklist_Methodology.md` — evidence anchoring; consistency checks across
  boundaries.
- `code-review/CodeReview_Process_Methodology.md` — reading for what isn't there; cross-boundary
  contracts.
- `rust/Rust_WebAssembly_Browser_Methodology.md` — DOM attribute access from WASM; web-sys
  `get_attribute` patterns; how Rust code on the client reads HTML attributes.

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting
point but is the final judge.

---

## Inherited Constraints

- Scope is REQ-HYD-004 only — do not evaluate other criteria here
- Read-only: do not modify source code
- All findings cite files and line numbers in `Nousix-LLC/nswe-demo`, never host paths
- Non-blockers: flag but do not hold landing
- CI passed — treat as a floor; check substance beyond what tests assert
- Do not evaluate REQ-SSR-007 (async resource state) or Axum integration
- **The marker schema section of the output is mandatory** — the synthesis cross-check depends on it

## Out-of-Scope Methodologies

- `rust/Rust_Web_Services_Axum_Methodology.md` — Axum is covered by SUBTASK_axum_mismatch
