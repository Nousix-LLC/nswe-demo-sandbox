# Task: app.rs cfg-gate Quality Review

## Task Specification

**Slug**: SUBTASK_app-rs-quality
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Review the code quality of `app.rs` changes introduced by the ferric-ssr-r4 commits, covering
five quality dimensions: cfg-gate idiom, conditional dispatch logic, error handling, docstring
accuracy, and readability. Produce `app-rs-notes.md` with a severity-labeled finding per
dimension.

### Context

This task is part of SUBTASK_code-quality (see `../_GLOBAL.md`). It runs in parallel with
SUBTASK_hydrate-wasm-quality. The synthesis task SUBTASK_quality-synthesis reads this task's
output and SUBTASK_hydrate-wasm-quality's output to produce the final `code-quality.md`.

The ferric-ssr-r4 commits add a `#[cfg(target_arch = "wasm32")]` gate and conditional
`hydrate()` dispatch in `app.rs`. The design intent: when running in a browser (wasm32) and
the root node already has children (server-rendered HTML is present), call `hydrate()` instead
of `mount()`.

This task covers code quality only. Security concerns (HTML injection, escaping) are out of
scope and belong to SUBTASK_security.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Project constraints and subtree-wide context |
| Parent hub | `../../_GLOBAL.md` | Broader review context and inherited constraints |
| PR #228 diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | Full diff to identify what changed in app.rs |
| `app.rs` | branch `work/ferric-ssr-r1`, path `crates/chirp-frontend/src/app.rs` | Primary file for review |

**Reading files via gh API**:
```bash
gh api repos/Nousix-LLC/nswe-demo/contents/crates/chirp-frontend/src/app.rs?ref=work/ferric-ssr-r1 \
  --jq '.content' | base64 -d
```

**Reading the PR diff**:
```bash
gh pr diff 228 --repo Nousix-LLC/nswe-demo
```

---

## Quality Dimensions to Review

Review `app.rs` across these five dimensions:

### 1. cfg-gate idiom
Is `#[cfg(target_arch = "wasm32")]` placed at the right scope? Is the pattern idiomatic Rust
(attribute placement, cfg vs cfg_attr, conditional imports)? Does the gating match what should
only exist in a browser context?

### 2. Conditional dispatch logic
Is the `has_children()` (or equivalent) check correct and semantically meaningful for the
SSR/hydrate vs mount decision? Does the condition accurately distinguish "server-rendered HTML
present" from "empty DOM"? Are there edge cases where the condition could misfire?

### 3. Error handling
What happens when `hydrate()` returns an error? Is the error path complete — does it propagate,
log, or silently discard? Is the error handling consistent with how errors from `mount()` are
handled elsewhere?

### 4. Docstring accuracy
Does the function/module docstring accurately describe the new conditional behavior? Is the
docstring updated to reflect that the function now does one thing in wasm context and another
in native context?

### 5. Readability
Is the new code clear to a reader unfamiliar with the change? Do variable names and inline
comments convey intent? Is the structure easy to follow?

---

## Output Specification

**File**: `app-rs-notes.md`
**Location**: `SUBTASK_app-rs-quality/`

The file MUST follow the finding-note format defined in `../contracts/_MANIFEST.yaml`:

```markdown
# app.rs Quality Notes

## cfg-gate idiom

**Severity**: [Blocker | Warning | Pass]
**Evidence**: [file:line or N/A]

[Finding text — plain voice, concrete, citable]

## Conditional dispatch logic

**Severity**: [Blocker | Warning | Pass]
**Evidence**: [file:line or N/A]

[Finding text]

## Error handling

**Severity**: [Blocker | Warning | Pass]
**Evidence**: [file:line or N/A]

[Finding text]

## Docstring accuracy

**Severity**: [Blocker | Warning | Pass]
**Evidence**: [file:line or N/A]

[Finding text]

## Readability

**Severity**: [Blocker | Warning | Pass]
**Evidence**: [file:line or N/A]

[Finding text]

## Fresh Non-Blockers (if any)

[List with file:line, or "None found"]
```

**Severity semantics**:
- **Blocker**: Must be fixed before the PR can merge; would cause a production defect, incorrect
  behavior, or violated contract.
- **Warning**: Should be fixed; a real quality concern but not an immediate defect risk.
- **Pass**: The dimension checks out; nothing to fix.

---

## Success Criteria

- [ ] All five quality dimensions assessed with severity and evidence
- [ ] Each finding cites the specific file:line from the branch (or "N/A" for structural absences)
- [ ] Fresh non-blockers noted or "None found" stated
- [ ] `app-rs-notes.md` written to this task's workspace

---

## Suggested Methodology Files

**Task type**: "Rust code review" → Primary: `rust`, `code-review`. Supporting: `framework-design`

| File | Rationale |
|---|---|
| `code-review/CodeReview_Process_Methodology.md` | Systematic concern coverage — ensures all five dimensions are examined rather than stopping at the most visible finding |
| `code-review/CodeReview_Checklist_Methodology.md` | Quality checklist for a code review — particularly useful for the error handling and cfg-gate idiom checks |
| `rust/Rust_WebAssembly_Browser_Methodology.md` | WASM/wasm-bindgen discipline — the primary methodology for evaluating whether the cfg-gate is placed and scoped correctly for the wasm32 target |
| `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` | SSR/hydration correctness — necessary context for evaluating whether the `has_children()` condition is semantically correct for the SSR→hydrate vs mount decision |

The above are the parent's flagged methodologies based on the task type. The child agent SHOULD
load these as a starting point but is the final judge of what its work requires — load fewer if
some are clearly inapplicable; load more if the brief reveals additional methodology surface the
parent did not anticipate.

## Inherited Constraints

- **Repository**: Nousix-LLC/nswe-demo, branch `work/ferric-ssr-r1`, PR #228
- **Commits under inspection**: `7fb90c7`, `e625c3f`, `75c1eef`
- **Do not re-raise**: Issues #229–#242
- **Do not reference**: Overseer I267 escalation comments
- **Prose bar**: No AI-tell patterns in output text (no moral adjectives on metrics, no narrated
  candor, no slot-fill templates, no padding filler)
- **Scope**: Code quality only — security is SUBTASK_security; this task does NOT cover HTML
  injection, escaping, or XSS vectors

## Out-of-Scope Methodologies

- `security/Security_Secure_Coding_Methodology.md` — security concerns are SUBTASK_security's
  scope, not this task's
- `rust/Rust_Testing_Methodology.md` — `app.rs` is production code, not a test file; test
  quality belongs to SUBTASK_hydrate-wasm-quality
