# Task: Concern 6 — Rust Language Idiom Review, PR #193

## Task Specification

**Slug**: SUBTASK_concern6_idiom
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Review Rust language idiom across the four files changed by PR #193's remediation commits — evaluating specific idiomatic patterns, `unsafe` usage, and common Rust anti-patterns in the changed code. Produce a `partial_findings.md` conforming to the shared findings contract.

### Context

Part of the PR #193 concerns 2/3/6/7 subtree. See `../_GLOBAL.md` for full context, shared inputs, and inherited constraints. The contract for the output format is at `../contracts/findings_format.md`.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `../_GLOBAL.md` | Inherited constraints, shared inputs, scope |
| Findings contract | `../contracts/findings_format.md` | Required output schema |
| PR #193 diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Changed lines |
| async_resource.rs | `crates/ferric/src/async_resource.rs` | Implementation + native tests |
| vdom.rs | `crates/ferric/src/vdom.rs` | EventHandler enum |
| dom.rs | `crates/ferric/src/dom.rs` | Dispatch logic + WASM test |
| form.rs | `crates/ferric/src/form.rs` | on_input_event_handler + WASM test |

---

## Review Scope

Examine the following for Concern 6 (Rust language idiom):

1. **`closure.forget()` in `form.rs` WASM test** (near line 519): Is `Closure::forget()` an acceptable pattern for keeping a closure alive in a WASM test context? Is it commented to explain why (the closure must outlive the test without being dropped)? If this pattern is used without explanation, future readers may assume it is a leak.

2. **`resource.signal.set(...)` in native tests in `async_resource.rs`**: This accesses what appears to be a private field. Does it work because tests are in the same module (Rust allows access to private fields within `mod tests` in the same file)? Is a `#[cfg(test)]` helper method (e.g., `fn force_ready(...)`) warranted for legibility, or is direct field access the established pattern in this codebase?

3. **`unsafe` usage**: Does any added code use `unsafe` blocks? If so, are they justified with a comment explaining the invariant that makes them sound?

4. **Common Rust anti-patterns in production code paths**: Are there uses of `unwrap()` in non-test, non-prototype production code paths that should use `?` or structured error handling? Unnecessary `.clone()` calls that could be avoided? Memory that leaks in non-test code (closures registered but never freed outside test contexts)?

Note: test-only code is held to a lower standard for some of these (e.g., `unwrap()` in tests is acceptable); the question is whether any anti-patterns appear in production code paths.

---

## Output Specification

**Primary Output:** `partial_findings.md` at this task's workspace root

Must conform to `../contracts/findings_format.md`: two required sections (`## Findings` and `## What was examined`), using `concern: idiom`, severity values from {`blocker`, `non-blocker`, `clean`}, repository-relative locations.

---

## Suggested Methodology Files

Task type row (Domain Mapping): **Ferric PR review (Rust library)** → Primary: `code-review`, Supporting: `rust`, `framework-design`

Specific files flagged for this concern:

- `code-review/CodeReview_Checklist_Methodology.md` — code review discipline; idiom checks are part of the code review checklist. Rationale: provides the frame for evaluating language idiom in a review context.
- `rust/Rust_Testing_Methodology.md` — Rust-specific test idiom: when `Closure::forget()` is appropriate, `#[cfg(test)]` helper patterns, test-vs-production code distinctions. Rationale: two of the four idiom questions (closure forget, private field access in tests) are specifically about test idiom, which this methodology covers.

These are SUGGESTIONS. Load fewer if some are clearly inapplicable; load more if your reading of the files reveals additional methodology surface needed.

## Out-of-Scope Methodologies

- `rust/Rust_Unsafe_FFI_Methodology.md` — out of scope unless the review reveals non-trivial unsafe usage; a quick scan for unsafe blocks is part of this task's scope, but deep FFI analysis belongs to a separate review if needed.

## Inherited Constraints

- Repository-relative paths only in all findings
- Issues #196–#201 MUST NOT be re-raised
- Severity `blocker` only if a requirement is unmet or an API contract is broken; idiom deviations are `non-blocker` unless they cause correctness issues in production paths
- Concerns 1, 2, 3, 4, 5, 7 are out of scope — focus only on Concern 6 (Rust idiom)

## Success Criteria

- All four idiom questions above examined with evidence from the actual code
- `closure.forget()` specifically evaluated for appropriateness and documentation
- Private field access in tests specifically evaluated
- Any `unsafe` blocks identified and their justification assessed
- `partial_findings.md` produced with `## Findings` and `## What was examined` sections
