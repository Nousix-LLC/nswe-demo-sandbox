# Task: hydrate_wasm.rs — Dimension 1: Test Structure and Naming

## Task Specification

**Slug**: SUBTASK_dim-naming
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Assess the test structure and naming quality of `hydrate_wasm.rs` (commit `75c1eef`),
covering: whether test names describe the behavior being verified, whether each test
focuses on one behavior, whether helpers are well-named, and whether anything should
be split or renamed. Produce `finding.md` with a severity label and cited evidence.

### Context

This task is one of five parallel dimension spokes within SUBTASK_hydrate-wasm-quality
(see `../_GLOBAL.md`). It assesses exactly one dimension: test structure and naming.
It does not cover DOM cleanup, hardcoded strings, duplication, or assertion quality —
those are sibling tasks.

`hydrate_wasm.rs` has three `#[wasm_bindgen_test]` functions and two helpers
(`make_container`, `cleanup`). The file runs in a real browser context via
`wasm-pack test --headless`.

---

## Input Specification

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Subtree constraints and shared context |
| `hydrate_wasm.rs` | commit `75c1eef` | Primary file for this dimension |

**Reading the file:**
```bash
gh api "repos/Nousix-LLC/nswe-demo/contents/crates/ferric/tests/hydrate_wasm.rs?ref=75c1eef776953993ddd62dba1436845a0d53a281" \
  --jq '.content' | base64 -d
```

---

## Dimension Scope

Assess test structure and naming in `hydrate_wasm.rs`:

- Do test names describe the behavior being verified (behavioral naming) rather than
  sequential numbering or vague labels?
- Is each test focused on one behavior, or does any test cover multiple behaviors
  that should be split?
- Are helper functions (`make_container`, `cleanup`) appropriately named for their role?
- Is the overall file structure clear and well-organized?

Do NOT assess: DOM cleanup strategy, hardcoded strings, assertion quality, or duplication.

---

## Output Specification

**File**: `finding.md`
**Location**: `SUBTASK_dim-naming/`

```markdown
## Test structure and naming

**Severity**: [Blocker | Warning | Pass]
**Evidence**: [hydrate_wasm.rs:line or N/A]

[Finding text — plain voice, concrete, citable]
```

Severity semantics:
- **Blocker**: Naming is so misleading it would cause a reviewer to miss a coverage
  gap, or a test covers multiple orthogonal behaviors without structural separation.
- **Warning**: Names or structure have genuine quality issues but do not misrepresent coverage.
- **Pass**: Test names and structure are clear and appropriate.

---

## Success Criteria

- [ ] All three test functions assessed for name quality
- [ ] Helpers assessed for naming
- [ ] Severity assigned with rationale
- [ ] Evidence cites specific line(s) or states N/A for structural absences
- [ ] `finding.md` written to this task's workspace

---

## Methodology Guidance

**Primary**: `rust/Rust_Testing_Methodology.md` — Rust test naming standards
**Secondary**: `code-review/CodeReview_Process_Methodology.md` — systematic coverage

---

## Inherited Constraints

- **Repository**: Nousix-LLC/nswe-demo, commit `75c1eef776953993ddd62dba1436845a0d53a281`
- **Do not re-raise**: Issues #229–#242
- **Do not reference**: Overseer I267 escalation comments
- **Prose bar**: No AI-tell patterns in output text
- **Scope**: Code quality only — security scope belongs to SUBTASK_security
