# SUBTASK_hyd002 — REQ-HYD-002: Signal Updates Propagate Post-Hydration

## Task Specification

**Slug**: SUBTASK_hyd002
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Determine whether, after `hydrate()` completes, signal updates propagate to the DOM in the same way
as a fresh mount — and whether there is test evidence of reactive updates post-hydration.

---

## Context

This task is part of the SUBTASK_hydration subtree (see `../_GLOBAL.md`).

**Dependents**: SUBTASK_hyd_synthesis reads `criterion_002.md`.

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Shared context | `../_GLOBAL.md` | Constraints, shared inputs, methodology posture |
| PR diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | The change under review |
| Issue #224 | `gh issue view 224 --repo Nousix-LLC/nswe-demo` | REQ-HYD-002 acceptance text |
| Hydration source on branch | `gh api repos/Nousix-LLC/nswe-demo/contents/<path>?ref=work/ferric-ssr-r1 \| jq -r '.content' \| base64 -d` | Full signal-subscriber wiring in hydrate() |
| Test files on branch | search the diff for test files that mention `hydrate` or `hydrat` | Evidence of reactive-update tests |

---

## Review Scope

Evaluate **REQ-HYD-002** only:

> After hydration, do signal updates propagate to the DOM as in a fresh mount? Is there test evidence
> of reactive updates post-hydration?

What to check:
1. After `hydrate()` runs, how are signal subscriptions wired? Are the same signal-listener paths
   exercised as in a fresh component mount?
2. Is there a test (unit or integration) that:
   a. Hydrates a component over SSR-rendered HTML, AND
   b. Triggers a signal update, AND
   c. Asserts the DOM changed?
3. If a test exists: does its assertion check observable DOM state (actual behavior), or only that
   something ran (shallow assertion)? Would it fail if signal propagation were broken?
4. If no test exists: note the absence as a finding.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| File | `criterion_002.md` |
| Location | this workspace (`SUBTASK_hyd002/`) |

### Output Structure

```markdown
# REQ-HYD-002 — Signal Updates Propagate Post-Hydration

**Status**: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
**What was checked**: <what code paths and tests were examined>
**Evidence**: `<file>:<line>` (or `<file>:<start>–<end>`)
**Finding** (if any): <description of the finding>
```

---

## Success Criteria

- [ ] REQ-HYD-002 has a named, evidence-backed verdict (CLEAN or FINDING with severity)
- [ ] Evidence cites at least one file and line number in `Nousix-LLC/nswe-demo`
- [ ] `criterion_002.md` exists at the declared path before task reports completed

---

## Suggested Methodology Files

**Task-type row matched**: "Ferric PR review (Rust library)" → Primary: `code-review`; Supporting:
`rust`, `framework-design`

Specific files:
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — signal
  propagation in a Rust UI framework; how reactive subscriptions are wired at mount vs. hydrate;
  what "same as a fresh mount" means in this framework's model.
- `code-review/CodeReview_Checklist_Methodology.md` — reading tests as closely as code; assertion
  quality; "green is a claim, not a proof."
- `code-review/CodeReview_Process_Methodology.md` — systematic review pass; what isn't there (the
  absent test path is a valid finding).
- `rust/Rust_WebAssembly_Browser_Methodology.md` — WASM/browser integration; event-listener
  attachment at the wasm-bindgen boundary.

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting
point but is the final judge.

---

## Inherited Constraints

- Scope is REQ-HYD-002 only — do not evaluate other criteria here
- Read-only: do not modify source code
- All findings cite files and line numbers in `Nousix-LLC/nswe-demo`, never host paths
- Non-blockers: flag but do not hold landing
- CI passed — treat as a floor; check substance beyond what tests assert
- Do not evaluate REQ-SSR-007 (async resource state) or Axum integration

## Out-of-Scope Methodologies

- `rust/Rust_Web_Services_Axum_Methodology.md` — Axum is covered by SUBTASK_axum_mismatch
