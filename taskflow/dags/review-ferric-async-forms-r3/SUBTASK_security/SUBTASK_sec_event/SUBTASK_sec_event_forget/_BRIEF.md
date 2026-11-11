# Task: Verify closure.forget() Scope in WASM Test

## Task Specification

**Slug**: SUBTASK_sec_event_forget
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Verify that the `closure.forget()` pattern introduced in `form.rs`'s WASM test is strictly confined to test infrastructure and does not appear in any production code path in the diff; and separately, assess whether the `closure.forget()` calls in production code (`dom.rs`'s `set_events()`) represent a correct or problematic pattern.

---

## Context

This task is part of the event handler security surface decomposition. See `../_GLOBAL.md` for full scope and constraints.

**Relevant diff:**
- `crates/ferric/src/form.rs` — B3 adds a `#[wasm_bindgen_test]` block containing `closure.forget()`
- `crates/ferric/src/dom.rs` — B2 `set_events()` production function also calls `closure.forget()`

The brief parent's intent is specifically to verify that the `form.rs` WASM test's `closure.forget()` is test-scoped. However, the reviewer must also note whether any additional production `closure.forget()` patterns in the diff are correct.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `../_GLOBAL.md` | Scope and constraints |
| PR diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Changed lines (search for `closure.forget`) |
| form.rs | `crates/ferric/src/form.rs` | WASM test section |
| dom.rs | `crates/ferric/src/dom.rs` | `set_events()` production function |

---

## Review Questions

This task answers exactly one question:

> Is the `closure.forget()` pattern in the WASM test (form.rs) limited to test scope only, and does it not appear in any production code path in the diff?

Specific sub-checks:
1. Is the `closure.forget()` in `form.rs` gated under `#[cfg(test)]` or a `#[wasm_bindgen_test]` block? Confirm it cannot be compiled into production WASM output.
2. Does `closure.forget()` appear in any non-test code path added by the diff? (The dom.rs `set_events()` function DOES call `closure.forget()` in production — assess whether this is a correct and expected pattern for wasm-bindgen DOM event binding, or a potential memory/safety concern.)
3. If dom.rs `set_events()` calls `closure.forget()` in production: is the closure reference stashed on the DOM element (via `js_sys::Reflect::set`) before `forget()` is called, so the closure is not actually leaked?

---

## Output Specification

**Primary Output:** `finding_forget.md` at this task's workspace root (`SUBTASK_sec_event_forget/finding_forget.md`)

```markdown
## Sub-Finding: closure.forget() Scope

- **severity**: blocker | non-blocker | clean
- **concern**: closure.forget() scope (test vs. production)
- **location**: crates/ferric/src/form.rs:LINE (or N/A)
- **description**: [specific answer: is the test-scope usage confirmed? is the production usage in dom.rs correct? cite evidence]

## What was examined
[Specific lines of form.rs and dom.rs diff, cfg attributes, test gates]
```

---

## Suggested Methodology Files

Task type row (Domain Mapping): **Security review / Rust library** → Primary: `security`, Supporting: `rust`

- `rust/Rust_WebAssembly_Browser_Methodology.md` — `closure.forget()` patterns in wasm-bindgen; why `forget()` is correct when the closure is stashed on a DOM element; memory model for wasm-bindgen closures
- `security/Security_Secure_Coding_Methodology.md` — resource lifecycle and memory management in a security context; what constitutes a production vs. test pattern

These are SUGGESTIONS. The agent is the final judge of what its work requires.

## Inherited Constraints

- Repository-relative paths only in all findings
- Severity `blocker` only for a concrete security vulnerability; a `closure.forget()` in test scope is not a blocker
- Focused pass on the three remediation commits only (9fedad9, 9557f0c, 838239e)

## Success Criteria

- [ ] The form.rs `closure.forget()` confirmed as test-scope-only (or flagged as not test-scoped)
- [ ] The dom.rs production `closure.forget()` assessed for correctness (stashed-then-forgotten pattern)
- [ ] `finding_forget.md` produced with `severity` assigned and evidence cited
