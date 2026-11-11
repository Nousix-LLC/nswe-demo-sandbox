# SUBTASK_hyd001 — REQ-HYD-001: hydrate() DOM Walk Without Re-creating Nodes

## Task Specification

**Slug**: SUBTASK_hyd001
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Determine whether `hydrate(component, props, root)` in PR #228 walks the existing DOM and attaches signal
listeners WITHOUT re-creating or replacing nodes — specifically, whether it uses `querySelector`-style
matching by `data-hydration-id` rather than `appendChild` / `replaceWith`.

---

## Context

This task is part of the SUBTASK_hydration subtree (see `../_GLOBAL.md`).

**Dependents**: SUBTASK_hyd_synthesis reads `criterion_001.md`.

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Shared context | `../_GLOBAL.md` | Constraints, shared inputs, methodology posture |
| PR diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | The change under review |
| Issue #224 | `gh issue view 224 --repo Nousix-LLC/nswe-demo` | REQ-HYD-001 acceptance text |
| Hydration source on branch | `gh api repos/Nousix-LLC/nswe-demo/contents/<hydration-path>?ref=work/ferric-ssr-r1 \| jq -r '.content' \| base64 -d` | Full hydrate() implementation |

Locate the hydration module by searching the diff or PR file tree for files containing `hydrate`,
`data-hydration-id`, or the WASM JS glue.

---

## Review Scope

Evaluate **REQ-HYD-001** only:

> Does `hydrate(component, props, root)` walk the existing DOM and attach signal listeners without
> re-creating or replacing nodes? Specifically: does it use `querySelector`-style matching by
> `data-hydration-id` rather than `appendChild` / `replaceWith`?

What to check:
1. Identify the `hydrate()` function in the diff/branch.
2. Read its body: does it call `querySelector` (or equivalent) to locate existing DOM nodes by
   `data-hydration-id`, or does it call `appendChild` / `replaceWith` / `innerHTML=` / similar
   destructive operations?
3. Verify that signal listeners are attached to already-existing nodes, not to freshly created ones.
4. Note any helper calls that delegate node creation/replacement.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| File | `criterion_001.md` |
| Location | this workspace (`SUBTASK_hyd001/`) |

### Output Structure

```markdown
# REQ-HYD-001 — hydrate() DOM Walk Without Re-creating Nodes

**Status**: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
**What was checked**: <what code paths were examined>
**Evidence**: `<file>:<line>` (or `<file>:<start>–<end>`)
**Finding** (if any): <description of the finding>
```

---

## Success Criteria

- [ ] REQ-HYD-001 has a named, evidence-backed verdict (CLEAN or FINDING with severity)
- [ ] Evidence cites at least one file and line number in `Nousix-LLC/nswe-demo` (not host/taskflow paths)
- [ ] `criterion_001.md` exists at the declared path before task reports completed

---

## Suggested Methodology Files

**Task-type row matched**: "Ferric PR review (Rust library)" → Primary: `code-review`; Supporting: `rust`,
`framework-design`

Specific files:
- `code-review/CodeReview_Checklist_Methodology.md` — criterion-by-criterion review checklist;
  evidence anchoring; CLEAN vs FINDING severity classification. Apply to REQ-HYD-001.
- `code-review/CodeReview_Process_Methodology.md` — systematic review pass structure; reading code
  vs reading tests.
- `rust/Rust_WebAssembly_Browser_Methodology.md` — WASM/browser integration, wasm-bindgen, the
  Rust↔DOM boundary; directly applicable to how hydrate() interacts with the DOM.
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — hydration
  walk strategy in a Rust UI framework; what "attach without replacing" means at the framework level.

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting
point but is the final judge — load fewer if some are clearly inapplicable; load more if the brief
reveals additional surface the parent did not anticipate.

---

## Inherited Constraints

- Scope is REQ-HYD-001 only — do not evaluate other criteria here
- Read-only: do not modify source code
- All findings cite files and line numbers in `Nousix-LLC/nswe-demo`, never host paths
- Non-blockers: flag but do not hold landing
- CI passed — treat as a floor; check substance beyond what tests assert
- Do not evaluate REQ-SSR-007 (async resource state) or Axum integration

## Out-of-Scope Methodologies

- `rust/Rust_Web_Services_Axum_Methodology.md` — Axum is covered by SUBTASK_axum_mismatch
