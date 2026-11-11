# Review DAG: review-ferric-ssr-r2

**Status**: Active — decomposed into spokes

## Project Context

### Objective

Re-review PR #228 (`work/ferric-ssr-r1`, Nousix-LLC/nswe-demo) after ferric-ssr-r4 remediation.
Verify that blockers B1 (REQ-HYD-003: `hydrate()` wiring) and B2 (REQ-SSR-006: `wasm-bindgen-test`
coverage) are genuinely resolved, that all 11 acceptance criteria remain satisfied, and that the
new code meets the standard quality and security bar. Deliver a final APPROVE or REQUEST-CHANGES
verdict in `SYNTHESIS.md` at this workspace root and post the review to PR #228.

### Scope

**In Scope:**
- B1 verification: `hydrate()` called from WASM entry point when root has server-rendered children
  (REQ-HYD-003); cfg-gate pattern correctness in `app.rs`
- B2 verification: `wasm-bindgen-test` coverage exists for mismatch detection, warning, and
  recovery code paths (REQ-SSR-006); tests would catch real regressions
- Regression check: all 9 previously-clean criteria still satisfied after new commits
- Code quality of new code (cfg-gate pattern, `hydrate_wasm.rs` test file)
- Security: HTML injection paths, escaping gaps introduced by new commits
- Fresh non-blockers in new code (do not re-raise #229–#242)

**Out of Scope:**
- REQ-SSR-007 / #225 (confirmed non-goal)
- Previously filed non-blocking issues #229–#242
- Overseer I267 escalation comments (obsoleted by this re-review)

### Success Criteria

- [ ] SYNTHESIS.md at this workspace root with verdict (APPROVE or REQUEST-CHANGES)
- [ ] If APPROVE: B1 and B2 confirmed resolved, all 11 criteria satisfied, CI green, PR ready
- [ ] If REQUEST-CHANGES: remaining blockers named against requirement IDs
- [ ] Review comment posted to PR #228

---

## Cut Rationale

The brief enumerates 5 distinct areas firing the scope-based decomposition trigger. Candidate
cuts evaluated:

1. **By concern** (B1-verify, B2-verify, regression+quality+sec, synthesis): maps to brief
   enumeration; all spokes read-only with disjoint declared outputs; zero cross-sibling write
   conflicts; B1 and B2 can run in parallel.
2. **By requirement group** (SSR, HYD, MIS, synthesis): misaligned with the primary B1/B2
   partition.
3. **By file** (app.rs, hydrate_wasm.rs, others, synthesis): overlaps option 1 but less
   requirement-aligned.

**Chosen**: Option 1 (by concern). Ownership disjointness satisfied (all spokes read-only code;
each writes its own verdict file). Feed-forward sizes: B1=S, B2=S-M, regression+quality+sec=M,
synthesis=S-M. All within acceptable bands.

Verdict placement: Shape B (gate-concentrated) — small subtree, spokes are parallel independent
reads, synthesis gate is the natural verdict point.

---

## Inputs

| Source | Location | Purpose |
|---|---|---|
| PR #228 | github.com/Nousix-LLC/nswe-demo/pull/228 | PR description, commits, CI status |
| Commit `7fb90c7` | PR branch | app.rs hydrate/mount conditional dispatch |
| Commit `e625c3f` | PR branch | hydrate_wasm.rs test file (197 lines) |
| Commit `75c1eef` | PR branch | cfg-gate + rustfmt |
| Issues #223, #224, #226 | GitHub | 11 acceptance criteria |
| Prior review output | review-ferric-ssr-r1 | 9 previously-clean criteria context |

---

## Task Structure

```
_GLOBAL.md (this file)
├── SUBTASK_b1-verify/_BRIEF.md       — verify REQ-HYD-003 (B1 hydrate wiring)
├── SUBTASK_b2-verify/_BRIEF.md       — verify REQ-SSR-006 (B2 wasm-bindgen-test)
├── SUBTASK_regression-quality-sec/_BRIEF.md  — verify 9 regression criteria + quality + security
└── SUBTASK_synthesis/_BRIEF.md       — synthesis: combine verdicts → SYNTHESIS.md → PR comment
```

### Task Summary

| Task id | Depends on | Description | Output |
|---|---|---|---|
| `SUBTASK_b1-verify` | none | Verify B1: REQ-HYD-003 hydrate() wiring in app.rs | `verdict-b1.md` |
| `SUBTASK_b2-verify` | none | Verify B2: REQ-SSR-006 wasm-bindgen-test coverage | `verdict-b2.md` |
| `SUBTASK_regression-quality-sec` | none | Regression check (9 criteria) + code quality + security | `verdict-regression-quality-sec.md` |
| `SUBTASK_synthesis` | `SUBTASK_b1-verify`, `SUBTASK_b2-verify`, `SUBTASK_regression-quality-sec` | Combine verdicts, write SYNTHESIS.md, post PR review | `../SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_b1-verify ──────────────────┐
                                    ├── SUBTASK_synthesis
SUBTASK_b2-verify ──────────────────┤
                                    │
SUBTASK_regression-quality-sec ─────┘
```

---

## Subtree Methodology Posture

**Dominant task type**: Code review (Rust, verification-focused)

**Primary bundles across the subtree**: `code-review`, `rust`, `framework-design`

**Specific files that bind the whole subtree**:
- `code-review/CodeReview_Process_Methodology.md` — review process and standard
- `code-review/CodeReview_Checklist_Methodology.md` — systematic coverage checklist
- `rust/Rust_WebAssembly_Browser_Methodology.md` — WASM/wasm-bindgen discipline
- `rust/Rust_Testing_Methodology.md` — Rust test quality standards
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — SSR/hydration internals

**Note**: These are suggested starting points; each child agent retains judgment over what it
actually loads.

## Subtree-Wide Constraints

- **Repository**: Nousix-LLC/nswe-demo, branch `work/ferric-ssr-r1`, PR #228
- **Review focus**: Remediation re-review; prior review-ferric-ssr-r1 found 9 of 11 criteria clean
- **Do not re-raise**: Issues #229–#242 (previously filed non-blockers)
- **Do not reference**: Overseer I267 escalation comments
- **Verdict bar**: B1 and B2 must both be verified resolved to approve
- **Non-blocking issues**: if new non-blockers found, file GitHub issues and list them in verdict
- **Prose bar**: review output must be free of AI-tell patterns (moral adjectives on metrics,
  narrated candor, slot-fill templates, padding filler)
