# SUBTASK_hyd003 — REQ-HYD-003: hydrate() Called Once From WASM Entry Point

## Task Specification

**Slug**: SUBTASK_hyd003
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Determine whether `hydrate()` is called exactly once from the WASM entry point and completes without
error on a correctly SSR-rendered page — and whether there is an integration test or demo that
exercises this path end-to-end.

---

## Context

This task is part of the SUBTASK_hydration subtree (see `../_GLOBAL.md`).

**Dependents**: SUBTASK_hyd_synthesis reads `criterion_003.md`.

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Shared context | `../_GLOBAL.md` | Constraints, shared inputs, methodology posture |
| PR diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | The change under review |
| Issue #224 | `gh issue view 224 --repo Nousix-LLC/nswe-demo` | REQ-HYD-003 acceptance text |
| WASM entry point source | `gh api repos/Nousix-LLC/nswe-demo/contents/<wasm-entry-path>?ref=work/ferric-ssr-r1 \| jq -r '.content' \| base64 -d` | The `#[wasm_bindgen(start)]` or `main()` function |
| Test/demo files | search diff and branch for integration test or demo files | Evidence of end-to-end exercise |

Locate the WASM entry point by searching for `#[wasm_bindgen(start)]`, `fn main()`, or `hydrate!`
macro in the diff or branch.

---

## Review Scope

Evaluate **REQ-HYD-003** only:

> Is `hydrate()` called once from the WASM entry point and does it complete without error on a
> correctly SSR-rendered page? Is there an integration test or demo that exercises this path?

What to check:
1. Identify the WASM entry point (the function that runs when the WASM module initializes in the
   browser).
2. Verify that `hydrate()` (or the hydration macro/wrapper) is called exactly once from that entry
   point.
3. Check whether there is guard logic to prevent double-hydration.
4. Find any integration test, E2E test, or demo that exercises the full SSR→hydrate path and asserts
   the page renders correctly.
5. If no such test/demo exists: note the absence and assess severity.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| File | `criterion_003.md` |
| Location | this workspace (`SUBTASK_hyd003/`) |

### Output Structure

```markdown
# REQ-HYD-003 — hydrate() Called Once From WASM Entry Point

**Status**: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
**What was checked**: <what code paths and tests were examined>
**Evidence**: `<file>:<line>` (or `<file>:<start>–<end>`)
**Finding** (if any): <description of the finding>
```

---

## Success Criteria

- [ ] REQ-HYD-003 has a named, evidence-backed verdict (CLEAN or FINDING with severity)
- [ ] Evidence cites at least one file and line number in `Nousix-LLC/nswe-demo`
- [ ] `criterion_003.md` exists at the declared path before task reports completed

---

## Suggested Methodology Files

**Task-type row matched**: "Ferric PR review (Rust library)" → Primary: `code-review`; Supporting:
`rust`, `framework-design`. Also applies: "Rust ↔ WebAssembly / browser bindings (wasm-bindgen,
web-sys)" → Rust + Framework Design.

Specific files:
- `rust/Rust_WebAssembly_Browser_Methodology.md` — `#[wasm_bindgen(start)]`, the WASM module
  initialization lifecycle, wasm-bindgen entry points; directly applicable to how hydrate() is
  called from the browser.
- `code-review/CodeReview_Process_Methodology.md` — systematic review; "what isn't there" (the
  absent integration test is a valid finding).
- `code-review/CodeReview_Checklist_Methodology.md` — entry-point coverage; integration test
  evidence.
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — SSR +
  hydration lifecycle in a Rust UI framework; what "called once on a correctly SSR-rendered page"
  means.

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting
point but is the final judge.

---

## Inherited Constraints

- Scope is REQ-HYD-003 only — do not evaluate other criteria here
- Read-only: do not modify source code
- All findings cite files and line numbers in `Nousix-LLC/nswe-demo`, never host paths
- Non-blockers: flag but do not hold landing
- CI passed — treat as a floor; check substance beyond what tests assert
- Do not evaluate REQ-SSR-007 (async resource state) or Axum integration

## Out-of-Scope Methodologies

- `rust/Rust_Web_Services_Axum_Methodology.md` — Axum is covered by SUBTASK_axum_mismatch
