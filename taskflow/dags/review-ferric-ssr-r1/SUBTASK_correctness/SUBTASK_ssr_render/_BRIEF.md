# SUBTASK_ssr_render — render_to_string Correctness Review

## Task Specification

**Slug**: SUBTASK_ssr_render
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Review PR #228 (`work/ferric-ssr-r1`, `Nousix-LLC/nswe-demo`) against the five acceptance criteria for issue
#223 (render_to_string). Produce `ssr_render_findings.md` with a named, evidence-backed verdict for each.

---

## Context

This task is part of the PR #228 Correctness Review (see `../_GLOBAL.md`).

**Depends on**: none (independent spoke — runs in parallel with SUBTASK_hydration, SUBTASK_axum_mismatch)
**Dependents**: SUBTASK_correctness_synthesis reads this output

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Shared context | `../_GLOBAL.md` | PR coordinates, shared constraints, contract |
| PR diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | The change under review |
| Branch source | Branch `work/ferric-ssr-r1` | Full file content for SSR code paths |
| Issue #223 | `gh issue view 223 --repo Nousix-LLC/nswe-demo` | render_to_string acceptance criteria |

To browse source files on the branch, use the GitHub CLI or API:
```
gh api repos/Nousix-LLC/nswe-demo/contents/<path>?ref=work/ferric-ssr-r1 | jq -r '.content' | base64 -d
```

---

## Review Scope

Evaluate each criterion. For each: state what you checked, what you found (CLEAN or FINDING), and evidence
(file and line in `Nousix-LLC/nswe-demo`, not host paths).

### Criteria

- **REQ-SSR-001**: Does `render_to_string(component, props)` render a component tree to HTML string
  server-side without a DOM? Does it compile and work in a `#[cfg(not(target_arch = "wasm32"))]` context?

- **REQ-SSR-002**: Do signal-driven components render from their initial signal state at render time (no
  reactivity/subscription during SSR)?

- **REQ-SSR-003**: Do child components and slot-based composition render correctly in the SSR pass? Are
  nested trees exercised?

- **REQ-SSR-004**: Does the rendered HTML include `data-hydration-id` (or equivalent) attribute markers?
  Are they well-formed and stable (same component in same position → same id)?
  **Critical**: Document the exact marker schema (attribute name and value format) you observe. The synthesis
  task cross-checks this against what SUBTASK_hydration finds for REQ-HYD-004.

- **REQ-SSR-005**: Is `render_to_string` callable from an Axum handler (is it in scope, exported, or
  otherwise accessible from server-side Rust)?

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| File | `ssr_render_findings.md` |
| Location | this workspace (`SUBTASK_ssr_render/`) |

### Output Structure

```markdown
# SSR render_to_string Findings (REQ-SSR-001–005)

## Summary
<one paragraph: overall verdict on the render_to_string implementation>

## Findings by Criterion

### REQ-SSR-001 — render_to_string renders without DOM
**Status**: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
**What was checked**: ...
**Evidence**: `<file>:<line>` (or `<file>:<start>–<end>`)
**Finding** (if any): ...

[Repeat for REQ-SSR-002, REQ-SSR-003, REQ-SSR-004, REQ-SSR-005]

## Marker Schema (REQ-SSR-004) — for synthesis cross-check
**Attribute name**: ...
**Value format**: ...
**Stability mechanism**: ...
```

The final section documenting the marker schema is mandatory — the synthesis task depends on it to verify
marker format consistency between this spoke and SUBTASK_hydration.

---

## Success Criteria

- [ ] REQ-SSR-001 through REQ-SSR-005 each have a named, evidence-backed verdict
- [ ] Evidence cites files and line numbers in `Nousix-LLC/nswe-demo` (not host paths)
- [ ] REQ-SSR-004 marker schema is documented in the dedicated section
- [ ] `ssr_render_findings.md` exists at the declared path before this task reports completed

---

## Suggested Methodology Files

**Task-type row matched**: "Ferric PR review (Rust library)" → Primary: `Code Review`; Supporting: `Rust`,
`Framework Design`

Specific files:
- `code-review/CodeReview_Process_Methodology.md` — how to structure a systematic review pass; anchoring
  findings to evidence
- `code-review/CodeReview_Checklist_Methodology.md` — concrete checklist to run against each criterion
- `rust/Rust_WebAssembly_Browser_Methodology.md` — WASM/browser integration, `#[cfg(target_arch = "wasm32")]`
  split, wasm-bindgen conventions; directly applicable to the cfg-gated SSR path
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — SSR + hydration
  in a Rust UI framework; directly applicable to REQ-SSR-001–004 (render semantics, marker design)

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but
is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if
the brief reveals additional methodology surface the parent did not anticipate.

---

## Inherited Constraints

- **Non-goal**: #225/REQ-SSR-007 (async resource state) is not in scope for this spoke — do not evaluate it
- **Read-only**: Do not modify source code
- **Line citations**: All findings cite files and line numbers in `Nousix-LLC/nswe-demo`, never host paths
  or taskflow paths
- **Non-blockers**: Flag them but they do not hold the landing
- **Machine gate**: CI passed — treat as a floor; check substance beyond what tests assert

## Out-of-Scope Methodologies

- `rust/Rust_Web_Services_Axum_Methodology.md` — Axum integration is SUBTASK_axum_mismatch's scope (REQ-MIS-001/002)
  except that REQ-SSR-005 asks whether `render_to_string` is *callable* from Axum: check visibility/exports only,
  not the handler pattern itself
