# SUBTASK_hydration — hydrate() Correctness Review

## Task Specification

**Slug**: SUBTASK_hydration
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Review PR #228 (`work/ferric-ssr-r1`, `Nousix-LLC/nswe-demo`) against the four acceptance criteria for issue
#224 (hydrate()). Produce `hydration_findings.md` with a named, evidence-backed verdict for each.

---

## Context

This task is part of the PR #228 Correctness Review (see `../_GLOBAL.md`).

**Depends on**: none (independent spoke — runs in parallel with SUBTASK_ssr_render, SUBTASK_axum_mismatch)
**Dependents**: SUBTASK_correctness_synthesis reads this output

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Shared context | `../_GLOBAL.md` | PR coordinates, shared constraints, contract |
| PR diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | The change under review |
| Branch source | Branch `work/ferric-ssr-r1` | Full file content for hydration/WASM code paths |
| Issue #224 | `gh issue view 224 --repo Nousix-LLC/nswe-demo` | hydrate() acceptance criteria |

To browse source files on the branch, use the GitHub CLI or API:
```
gh api repos/Nousix-LLC/nswe-demo/contents/<path>?ref=work/ferric-ssr-r1 | jq -r '.content' | base64 -d
```

---

## Review Scope

Evaluate each criterion. For each: state what you checked, what you found (CLEAN or FINDING), and evidence
(file and line in `Nousix-LLC/nswe-demo`, not host paths).

### Criteria

- **REQ-HYD-001**: Does `hydrate(component, props, root)` walk the existing DOM and attach signal listeners
  without re-creating or replacing nodes? Specifically: does it use `querySelector`-style matching by
  `data-hydration-id` rather than `appendChild` / `replaceWith`?

- **REQ-HYD-002**: After hydration, do signal updates propagate to the DOM as in a fresh mount? Is there
  test evidence of reactive updates post-hydration?

- **REQ-HYD-003**: Is `hydrate()` called once from the WASM entry point and does it complete without error
  on a correctly SSR-rendered page? Is there an integration test or demo that exercises this path?

- **REQ-HYD-004**: Does the hydration code use the same marker format (`data-hydration-id`) the SSR pass
  emits? Is the format agreed and consistent between server (`render_to_string`) and client (`hydrate`)? Are
  marker values deterministic given the same component tree?
  **Critical**: Document the exact marker schema (attribute name and value format) you observe in the hydration
  code. The synthesis task cross-checks this against what SUBTASK_ssr_render finds for REQ-SSR-004.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| File | `hydration_findings.md` |
| Location | this workspace (`SUBTASK_hydration/`) |

### Output Structure

```markdown
# hydrate() Findings (REQ-HYD-001–004)

## Summary
<one paragraph: overall verdict on the hydrate() implementation>

## Findings by Criterion

### REQ-HYD-001 — hydrate() attaches without re-creating nodes
**Status**: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
**What was checked**: ...
**Evidence**: `<file>:<line>` (or `<file>:<start>–<end>`)
**Finding** (if any): ...

[Repeat for REQ-HYD-002, REQ-HYD-003, REQ-HYD-004]

## Marker Schema (REQ-HYD-004) — for synthesis cross-check
**Attribute name**: ...
**Value format**: ...
**Determinism mechanism**: ...
```

The final section documenting the marker schema is mandatory — the synthesis task depends on it to verify
marker format consistency between this spoke and SUBTASK_ssr_render.

---

## Success Criteria

- [ ] REQ-HYD-001 through REQ-HYD-004 each have a named, evidence-backed verdict
- [ ] Evidence cites files and line numbers in `Nousix-LLC/nswe-demo` (not host paths)
- [ ] REQ-HYD-004 marker schema is documented in the dedicated section
- [ ] `hydration_findings.md` exists at the declared path before this task reports completed

---

## Suggested Methodology Files

**Task-type row matched**: "Ferric PR review (Rust library)" → Primary: `Code Review`; Supporting: `Rust`,
`Framework Design`

Specific files:
- `code-review/CodeReview_Process_Methodology.md` — how to structure a systematic review pass; anchoring
  findings to evidence
- `code-review/CodeReview_Checklist_Methodology.md` — concrete checklist to run against each criterion
- `rust/Rust_WebAssembly_Browser_Methodology.md` — WASM/browser integration, wasm-bindgen, the boundary between
  Rust compiled to WASM and browser DOM; directly applicable to REQ-HYD-001–004
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — SSR + hydration
  in a Rust UI framework; directly applicable to hydration correctness, signal propagation, marker consistency

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but
is the final judge — load fewer if some are clearly inapplicable; load more if the brief reveals additional
surface the parent did not anticipate.

---

## Inherited Constraints

- **Non-goal**: #225/REQ-SSR-007 (async resource state) is not in scope for this spoke — do not evaluate it
- **Read-only**: Do not modify source code
- **Line citations**: All findings cite files and line numbers in `Nousix-LLC/nswe-demo`, never host paths
  or taskflow paths
- **Non-blockers**: Flag them but they do not hold the landing
- **Machine gate**: CI passed — treat as a floor; check substance beyond what tests assert

## Out-of-Scope Methodologies

- `rust/Rust_Web_Services_Axum_Methodology.md` — Axum integration is covered by SUBTASK_axum_mismatch; this
  spoke focuses solely on the WASM client hydration path
