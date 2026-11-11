# SUBTASK_correctness — PR #228 Correctness Review

## Task Specification

**Slug**: SUBTASK_correctness
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Examine PR #228 (`work/ferric-ssr-r1`, repo `Nousix-LLC/nswe-demo`) against every acceptance
criterion for issues #223, #224, and #226, and produce a named finding (or "clean") for each
criterion. This is a read-only review; do not modify source code.

---

## Context

See `_GLOBAL.md` (parent workspace) for PR details, the full acceptance-criteria list, and
cross-cutting constraints.

**Depends on**: none (independent spoke — runs in parallel with SUBTASK_code_quality,
SUBTASK_security_xss, SUBTASK_security_infra)
**Dependents**: SUBTASK_synthesis reads this output

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Shared context | `../_GLOBAL.md` | PR coordinates, acceptance criteria, non-goal boundary |
| PR diff and source | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | The change under review |
| Branch source | `Nousix-LLC/nswe-demo` branch `work/ferric-ssr-r1` | Full file content for any file touched |
| Issue #223 | `gh issue view 223 --repo Nousix-LLC/nswe-demo` | SSR acceptance criteria |
| Issue #224 | `gh issue view 224 --repo Nousix-LLC/nswe-demo` | Hydration acceptance criteria |
| Issue #226 | `gh issue view 226 --repo Nousix-LLC/nswe-demo` | Mismatch detection + Axum integration criteria |

---

## Review Scope

Evaluate each of the following acceptance criteria individually. For each, state: what you checked,
what you found (clean / finding), evidence (file and line in the repository). A "finding" may be a
blocker or a non-blocker.

### #223 — render_to_string

- **REQ-SSR-001**: Does `render_to_string(component, props)` render a component tree to HTML string
  server-side without a DOM? Does it compile and work in a `#[cfg(not(target_arch = "wasm32"))]`
  context?
- **REQ-SSR-002**: Do signal-driven components render from their initial signal state at render time
  (no reactivity/subscription during SSR)?
- **REQ-SSR-003**: Do child components and slot-based composition render correctly in the SSR pass?
  Are nested trees exercised?
- **REQ-SSR-004**: Does the rendered HTML include `data-hydration-id` (or equivalent) attribute
  markers? Are they well-formed and stable (same component in same position → same id)?
- **REQ-SSR-005**: Is `render_to_string` callable from an Axum handler (is it in scope, exported, or
  otherwise accessible from server-side Rust)?

### #224 — hydrate()

- **REQ-HYD-001**: Does `hydrate(component, props, root)` walk the existing DOM and attach signal
  listeners without re-creating or replacing nodes? Specifically: does it use `querySelector`-style
  matching by `data-hydration-id` rather than `appendChild` / `replaceWith`?
- **REQ-HYD-002**: After hydration, do signal updates propagate to the DOM as in a fresh mount?
  Is there test evidence of reactive updates post-hydration?
- **REQ-HYD-003**: Is `hydrate()` called once from the WASM entry point and does it complete without
  error on a correctly SSR-rendered page? Is there an integration test or demo that exercises this
  path?
- **REQ-HYD-004**: Does the hydration code use the same marker format (`data-hydration-id`) the SSR
  pass emits? Is the format agreed and consistent between server (`render_to_string`) and client
  (`hydrate`)? Are marker values deterministic given the same component tree?

### #226 — Mismatch detection and Axum integration

- **REQ-SSR-006**: Does mismatch detection fire on actual structural mismatches (wrong node type,
  missing or wrong marker)? Does it log a recoverable warning (not panic) and fall back to a fresh
  mount for that subtree? Is there test coverage for the mismatch path?
- **REQ-MIS-001**: Does the Axum integration provide a handler pattern (example or real handler) that
  calls `render_to_string` and returns the HTML response? Is the pattern correct Axum code
  (uses `Html(...)` or equivalent)?
- **REQ-MIS-002**: Is the Axum-rendered HTML well-formed (balanced tags, valid attributes)? Does it
  contain the hydration markers the client needs?

### Non-goal boundary

- **REQ-SSR-007 / #225**: Do NOT evaluate or report on async resource state carry across the SSR seam.
  Confirm explicitly that this is absent or only guarded/stubbed, not that it is deficient.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| File | `correctness_findings.md` |
| Location | this workspace (`SUBTASK_correctness/`) |

### Output Structure

```markdown
# PR #228 Correctness Findings

## Summary
<one-paragraph verdict on correctness: which criteria are met, which have findings>

## Findings by Criterion

### REQ-SSR-001 — render_to_string renders without DOM
**Status**: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
**What was checked**: ...
**Evidence**: ...
**Finding** (if any): ...

[Repeat for each criterion above]

## Non-goal boundary
### REQ-SSR-007 / #225 — async resource state (non-goal)
**Status**: CONFIRMED NON-GOAL
**What was checked**: ...
```

---

## Success Criteria

- Every acceptance criterion has a named, evidence-backed finding or clean verdict
- Each finding names the file and line in the repository (not host paths)
- The non-goal boundary is confirmed explicitly
- Output file exists at the declared path before this task reports completed

---

## Suggested Methodology Files

**Task-type row matched**: "Ferric PR review (Rust library)" → Primary: `Code Review`; Supporting: `Rust`, `Framework Design`

Specific files:
- `code-review/CodeReview_Process_Methodology.md` — governs HOW to structure a systematic review pass; covers what a full review pass looks like, how to anchor findings to evidence
- `code-review/CodeReview_Checklist_Methodology.md` — a concrete checklist of things to look for; run it against each criterion
- `rust/Rust_WebAssembly_Browser_Methodology.md` — covers WASM/browser integration, the `#[cfg(target_arch = "wasm32")]` split, wasm-bindgen conventions; directly applicable to the WASM hydration path
- `rust/Rust_Web_Services_Axum_Methodology.md` — covers correct Axum integration patterns; applicable to REQ-MIS-001/002
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — covers SSR + hydration in a Rust UI framework; directly applicable to hydration correctness and marker consistency

These are the parent's flagged methodologies based on the task type. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.

## Inherited Constraints

- **Non-goal**: #225 / REQ-SSR-007 (async resource state) is not a finding or blocker for this PR
- **Read-only**: Do not modify source code
- **Line citations**: All findings cite files and line numbers in `Nousix-LLC/nswe-demo`, not host paths or taskflow paths
- **Non-blockers**: Flag them but they do not hold the landing (SUBTASK_synthesis will file them as issues)
- **Machine gate**: CI passed all 6 checks — treat as a floor, not a ceiling; it does not substitute for review
