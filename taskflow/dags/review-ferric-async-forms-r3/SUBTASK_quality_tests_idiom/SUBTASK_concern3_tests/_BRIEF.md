# Task: Concern 3 — Test Coverage and Depth Review, PR #193

## Task Specification

**Slug**: SUBTASK_concern3_tests
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Review test coverage and behavioral depth in the four files changed by PR #193's remediation commits — evaluating whether each test asserts behavior rather than mere execution, whether the DOM tests interact with real DOM objects, and whether any acceptance criteria scenarios lack test coverage. Produce a `partial_findings.md` conforming to the shared findings contract.

### Context

Part of the PR #193 concerns 2/3/6/7 subtree. See `../_GLOBAL.md` for full context, shared inputs, and inherited constraints. The contract for the output format is at `../contracts/findings_format.md`.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `../_GLOBAL.md` | Inherited constraints, shared inputs, scope |
| Findings contract | `../contracts/findings_format.md` | Required output schema |
| PR #193 diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Changed lines |
| async_resource.rs | `crates/ferric/src/async_resource.rs` | Generation counter tests |
| vdom.rs | `crates/ferric/src/vdom.rs` | EventHandler enum |
| dom.rs | `crates/ferric/src/dom.rs` | WASM test for prevent_default |
| form.rs | `crates/ferric/src/form.rs` | WASM test for on_input_event_handler |

---

## Review Scope

Examine the following for Concern 3 (test coverage and depth):

1. **Generation counter scenario in `async_resource.rs`**: Do the native tests exercise the case where the source signal changes while a future is in flight (rapid source changes with in-flight futures)? Are the assertions behavioral — checking `Resource` state after a stale future resolves — or vacuous (checking only that something ran)?

2. **WASM test for REQ-ASYNC-042 in `form.rs`** (`on_input_event_handler_updates_signal_from_dom_value` or similar): Does the test attach a real DOM element to the document, dispatch a genuine input event (not just call a handler function directly), and then assert the expected signal state? Or does it shortcut the DOM interaction?

3. **WASM test for `prevent_default` in `dom.rs`** (`event_carrying_handler_can_call_prevent_default` or similar): Does the test verify that `event.default_prevented()` returns `true` after the handler runs — not merely that the handler completed without panicking?

4. **Acceptance criteria coverage**: Are there scenarios declared in the acceptance criteria for REQ-ASYNC-042 and REQ-ASYNC-023 (or referenced in the PR) that have no test coverage at all in the changed files?

---

## Output Specification

**Primary Output:** `partial_findings.md` at this task's workspace root

Must conform to `../contracts/findings_format.md`: two required sections (`## Findings` and `## What was examined`), using `concern: tests`, severity values from {`blocker`, `non-blocker`, `clean`}, repository-relative locations.

---

## Suggested Methodology Files

Task type row (Domain Mapping): **Ferric PR review (Rust library)** → Primary: `code-review`, Supporting: `rust`, `framework-design`

Specific files flagged for this concern:

- `code-review/CodeReview_Checklist_Methodology.md` — review-process checklist including test coverage questions. Rationale: provides the structural frame for evaluating test adequacy in a code review context.
- `rust/Rust_Testing_Methodology.md` — Rust-specific test adequacy standards; wasm-bindgen-test patterns; behavioral vs. structural assertions; when native tests vs WASM tests are appropriate. Rationale: the key questions (does the WASM test dispatch a real event? does the native test assert Resource state?) are covered by Rust testing methodology.

These are SUGGESTIONS. Load fewer if some are clearly inapplicable; load more if your reading of the files reveals additional methodology surface needed.

## Inherited Constraints

- Repository-relative paths only in all findings
- Issues #196–#201 MUST NOT be re-raised
- Severity `blocker` only if a requirement is unmet (e.g., a test that does not exercise the scenario it claims to test, leaving a stated acceptance criterion uncovered); `non-blocker` for behavioral shallowness that could be improved without blocking merge
- Concerns 1, 2, 4, 5, 6, 7 are out of scope — focus only on Concern 3 (tests)

## Success Criteria

- All four test-depth questions above examined with evidence from the actual test code
- `partial_findings.md` produced with `## Findings` and `## What was examined` sections
- Each test for REQ-ASYNC-042 and REQ-ASYNC-023 evaluated for behavioral depth (not just "does it run")
- Any uncovered acceptance criteria scenarios identified with severity
