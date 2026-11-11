# Task: Verify B1 — REQ-HYD-003 hydrate() wiring

## Task Specification

**Slug**: SUBTASK_b1-verify
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Verify that blocker B1 (REQ-HYD-003) from review-ferric-ssr-r1 is genuinely resolved: confirm
that `hydrate()` is now called from the WASM entry point when the root already has
server-rendered children, and that the cfg-gate pattern and mount/hydrate dispatch are
functionally correct end-to-end.

### Context

**Prior blocker**: review-ferric-ssr-r1 found that `crates/chirp-frontend/src/app.rs::start()`
called `ferric::dom::mount(root, app)` unconditionally; `hydrate()` was never invoked.

**Remediation (ferric-ssr-r4)**:
- Commit `7fb90c7`: `app.rs` — replaced unconditional `mount` with conditional
  `ferric::hydrate(root, app)` / `mount` based on whether root has children
- Commit `75c1eef`: `app.rs` — added `#[cfg(target_arch = "wasm32")]` gate on the hydrate block

**REQ-HYD-003 requirement**: `hydrate()` is called from the WASM entry point when the root
already has server-rendered children (i.e., the SSR+hydration path is wired end-to-end).

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|---|---|---|
| PR #228 diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` or GitHub | See the actual changes |
| `app.rs` current state | `gh api /repos/Nousix-LLC/nswe-demo/contents/crates/chirp-frontend/src/app.rs?ref=work/ferric-ssr-r1` | Verify current code |
| `ferric::hydrate` signature/contract | `crates/ferric/src/lib.rs` or hydrate.rs | Understand what hydrate() does |
| Issue #224 | GitHub issue #224 | REQ-HYD-003 requirement text |
| Parent _GLOBAL.md | `../_GLOBAL.md` | Project context and constraints |

---

## Process Guidance

Read the current `app.rs` file and the diff for commits `7fb90c7` and `75c1eef`. Then verify:

1. **Conditional dispatch**: Does `start()` check whether the root has children, then call
   `ferric::hydrate(root, app)` on the hydration path and `ferric::dom::mount(root, app)` on
   the client-only path?

2. **cfg-gate correctness**: Is `#[cfg(target_arch = "wasm32")]` applied correctly so this
   code only compiles for WASM? Does the native path (SSR render) still work?

3. **Hydrate function wiring**: Does the call pass the correct arguments? Is `root` correctly
   typed and obtained? Is `app` the correct component?

4. **Children check logic**: What condition is used to detect "root already has server-rendered
   children"? Is this condition correct for the SSR case? Could it misfire (false positive for
   empty root, false negative for SSR root)?

5. **End-to-end wiring**: Can you trace the SSR+hydration path from server render → HTML
   delivered to browser → WASM start() → hydrate() called on the SSR-rendered DOM? Is there
   any gap in the chain?

6. **Mount fallback**: Is the mount-only path (client-only, no SSR) also correct?

Report the finding per criterion:
- PASS: state what you verified and found sound
- FAIL (blocker): state precisely what is wrong and what would satisfy you

---

## Output Specification

**File**: `verdict-b1.md`
**Location**: `SUBTASK_b1-verify/`

The file should contain:

```markdown
# B1 Verdict — REQ-HYD-003: hydrate() wiring

## Verdict: [PASS | FAIL]

## Finding

[For each of the 5 checks above: what was examined, what was found — specific file/line
citations at the commit inspected, reasoning in the open]

## If FAIL: Blocker

[Requirement ID, file and line, what is wrong, what would satisfy this finding]

## If PASS: What Was Clean

[What specifically was verified and found sound — this is the record of examination]
```

---

## Success Criteria

- [ ] `app.rs` read at the `work/ferric-ssr-r1` branch HEAD commit
- [ ] All 5 checks covered with specific file:line citations
- [ ] Verdict is PASS or FAIL (not "unclear" — if uncertain, explain the question that would
      settle it and treat it as FAIL until answered)
- [ ] `verdict-b1.md` written to this task's workspace

---

## Suggested Methodology Files

**Task type**: "Ferric PR review (Rust library)" → Primary: `code-review`, Supporting: `rust`,
`framework-design`

Specifically:
- `code-review/CodeReview_Process_Methodology.md` — verification review process; evidence over
  assertion discipline
- `code-review/CodeReview_Checklist_Methodology.md` — systematic concern coverage
- `rust/Rust_WebAssembly_Browser_Methodology.md` — `wasm-bindgen` patterns, cfg-gate
  correctness, WASM entry point conventions
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` —
  SSR+hydration wiring discipline, mount vs hydrate distinction

These are suggested starting points. Load fewer if clearly inapplicable; load more if your
reading of the code reveals additional surface to check.

## Inherited Constraints

- Repository: Nousix-LLC/nswe-demo, branch `work/ferric-ssr-r1`, PR #228
- Commits under inspection: `7fb90c7`, `75c1eef` (the B1-relevant commits)
- Do not re-raise previously filed non-blockers #229–#242
- Do not reference overseer I267 escalation comments
- Prose bar: no AI-tell patterns in output text
