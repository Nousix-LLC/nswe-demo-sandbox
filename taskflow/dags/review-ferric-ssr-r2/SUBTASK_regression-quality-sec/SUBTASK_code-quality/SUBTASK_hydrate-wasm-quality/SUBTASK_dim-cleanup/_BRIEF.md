# Task: hydrate_wasm.rs — Dimension 2: Setup/Teardown and DOM Cleanup

## Task Specification

**Slug**: SUBTASK_dim-cleanup
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Assess the DOM cleanup discipline in `hydrate_wasm.rs` (commit `75c1eef`): whether
each test that inserts DOM elements reliably removes them before returning, including
in the panic/early-return path. Produce `finding.md` with a severity label and
cited evidence.

### Context

This task is one of five parallel dimension spokes within SUBTASK_hydrate-wasm-quality
(see `../_GLOBAL.md`). It assesses exactly one dimension: setup/teardown and DOM cleanup.

`wasm-bindgen-test` with `run_in_browser` runs all tests in the same browser page within
a test session. A test that appends to `<body>` without removing the element before
returning leaves that element in the DOM for every subsequent test in the session. If
the cleanup call is only at the end of the test body (not guarded against early returns
or panics), a test failure leaves orphaned elements.

The file has a `cleanup(el)` helper that removes an element from the document. The
question is whether it is called on all exit paths from each test.

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

Assess DOM cleanup in `hydrate_wasm.rs`:

- For each `#[wasm_bindgen_test]` function: does it call `cleanup()` (or equivalent)
  on every exit path, including panic/assertion-failure paths?
- In Rust `wasm-bindgen-test`, a test panic unwinds through the test body; cleanup
  code after the final assertion does NOT run on failure. Check whether any test
  relies on cleanup running after a potentially-failing assertion.
- Identify the specific lines where `make_container()` is called and where `cleanup()`
  is called to determine whether the teardown is defensive or only on the happy path.

Do NOT assess: test naming, hardcoded strings, assertion quality, or duplication.

---

## Output Specification

**File**: `finding.md`
**Location**: `SUBTASK_dim-cleanup/`

```markdown
## Setup/teardown and DOM cleanup

**Severity**: [Blocker | Warning | Pass]
**Evidence**: [hydrate_wasm.rs:line or N/A]

[Finding text — plain voice, concrete, citable]
```

Severity semantics:
- **Blocker**: Cleanup failure would cause test-to-test DOM contamination that makes
  test results unreliable (a failing test contaminates subsequent tests).
- **Warning**: Cleanup is present but fragile; contamination is possible in failure
  scenarios but the happy path is clean.
- **Pass**: DOM is reliably cleaned up on all test exit paths.

---

## Success Criteria

- [ ] All three test functions checked for cleanup discipline
- [ ] The panel/early-return risk explicitly addressed (not just happy-path cleanup)
- [ ] Severity assigned with rationale
- [ ] Evidence cites specific line(s) in hydrate_wasm.rs
- [ ] `finding.md` written to this task's workspace

---

## Methodology Guidance

**Primary**: `rust/Rust_WebAssembly_Browser_Methodology.md` — wasm-bindgen-test browser
  isolation and cleanup conventions
**Secondary**: `rust/Rust_Testing_Methodology.md` — test isolation standards

---

## Inherited Constraints

- **Repository**: Nousix-LLC/nswe-demo, commit `75c1eef776953993ddd62dba1436845a0d53a281`
- **Do not re-raise**: Issues #229–#242
- **Do not reference**: Overseer I267 escalation comments
- **Prose bar**: No AI-tell patterns in output text
- **Scope**: Code quality only — security scope belongs to SUBTASK_security
