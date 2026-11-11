# Task: Quality, Tests, Idiom, and API Stability Review — PR #193 Ferric Async

## Task Specification

**Slug**: SUBTASK_quality_tests_idiom  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  
**Assigned To**: swe-reviewer

### Objective

Review concerns 2 (code quality and design), 3 (test coverage and depth), 6 (Rust language idiom), and 7 (API and contract stability) for PR #193 (`work/ferric-async-forms-r2`, head `838239e`). Produce a findings report covering what was sound, what warrants a non-blocker note, and whether anything reaches blocker severity.

---

## Context

See `../_GLOBAL.md` for full project context, acceptance criteria, and key reference data.

**Files changed by the three remediation commits:**
- `crates/ferric/src/async_resource.rs` — B1 implementation and new tests
- `crates/ferric/src/vdom.rs` — B2 EventHandler enum
- `crates/ferric/src/dom.rs` — B2 dispatch + WASM test for prevent_default
- `crates/ferric/src/form.rs` — B3 on_input_event_handler + WASM test

Fetch the PR diff and read the relevant source files using `gh pr diff 193 --repo Nousix-LLC/nswe-demo` and read individual source files directly.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Acceptance criteria, scope, constraints |
| PR #193 diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Actual changed lines |
| async_resource.rs | `crates/ferric/src/async_resource.rs` | Implementation + test code |
| vdom.rs | `crates/ferric/src/vdom.rs` | EventHandler enum design |
| dom.rs | `crates/ferric/src/dom.rs` | Dispatch logic + WASM test |
| form.rs | `crates/ferric/src/form.rs` | on_input_event_handler + WASM test |

---

## Review Scope

**Concern 2 — Code quality and design:**
- Responsibilities and coupling: do `async_resource.rs`, `vdom.rs`, `form.rs`, `dom.rs` each own a clean slice of responsibility? Are there unexpected imports or tight coupling introduced by the remediation?
- Is the `EventHandler` enum variant scheme a sound abstraction boundary? Does `vdom.rs` stay free of `web_sys` imports?
- Is the generation counter in `create_resource` straightforward — can a future reader follow the invariant without tracing through multiple layers?
- Does the design invite correct use and discourage misuse?

**Concern 3 — Test coverage and depth:**
- Do the tests in `async_resource.rs` exercise the generation counter scenario (rapid source changes with in-flight futures)? Are the assertions behavioral (checking `Resource` state) or vacuous (checking that something ran)?
- Does the `wasm-bindgen-test` for REQ-ASYNC-042 (`on_input_event_handler_updates_signal_from_dom_value` or similar) attach a real DOM element, dispatch a real input event, and assert the signal state — or does it shortcut the DOM interaction?
- Does the `event_carrying_handler_can_call_prevent_default` test in `dom.rs` actually verify `prevent_default()` took effect (e.g., asserts `event.default_prevented()` returns `true`) — or does it only verify that the handler ran without panicking?
- Are there acceptance criteria scenarios that have no test coverage at all?

**Concern 6 — Rust language idiom:**
- `closure.forget()` in the WASM test (`form.rs` near line 519): is this an acceptable pattern for keeping a closure alive in a WASM test, and is it at least commented so future readers understand why?
- `resource.signal.set(...)` in native tests in `async_resource.rs`: this accesses what appears to be a private field. Does it work because tests are in the same file (Rust allows this within `mod tests { ... }`)? Is a `#[cfg(test)] fn force_ready(...)` helper warranted for legibility?
- Any use of `unsafe` that isn't justified?
- Any Rust anti-patterns (e.g., `unwrap()` in non-test production code paths, unnecessary clones, leaked memory in non-test code)?

**Concern 7 — API and contract stability:**
- `EventHandler` is a public type. The enum redesign must preserve the existing public API surface. Verify that existing callers passing `impl Fn()` to `VElement::on_event()` still compile unchanged (the `NoArg` wrapper in `vdom.rs` should be transparent).
- Does the new `on_input_event_handler()` method on `Bind<T>` extend the public API cleanly? Is it documented?
- Does `create_resource` follow the library's established naming and API conventions?

---

## Output Specification

**Primary Output:** `findings.md` at this task's workspace root (`SUBTASK_quality_tests_idiom/findings.md`)

The findings file MUST contain:

```markdown
## Findings

[For each finding or clean verification, an entry with:
- severity: blocker | non-blocker | clean
- concern: code-quality | tests | idiom | api-stability
- location: crates/ferric/src/file.rs:LINE (where applicable)
- description: what was found]

## What was examined

[Enumeration of files, line ranges, and specific questions examined,
so the synthesis task can confirm coverage without gaps]
```

---

## Suggested Methodology Files

Task type row (Domain Mapping): **Ferric PR review (Rust library)** → Primary: `code-review`, Supporting: `rust`, `framework-design`

Specific files to load:
- `code-review/CodeReview_Checklist_Methodology.md` — quality checklist
- `rust/Rust_Testing_Methodology.md` — Rust test adequacy standards; wasm-bindgen-test patterns
- `rust/Rust_Library_API_And_Stability_Methodology.md` — API surface, semver, backward compat
- `framework-design/FrameworkDesign_Library_API_Design_Methodology.md` — abstraction boundaries, public API writability
- `code-quality/Framework_Clean_Code_Methodology.md` — code quality, naming, responsibility separation

These are SUGGESTIONS. Load fewer if some are clearly inapplicable; load more if the brief reveals additional methodology surface needed.

## Inherited Constraints

- Repository-relative paths only in all findings (no host paths, no taskflow paths)
- Non-blockers previously filed as #196–#201 must NOT be re-raised
- Severity calibration: a finding is a blocker only if it means the requirement is unmet or the API contract is broken for existing callers; style observations are at most non-blocker

## Success Criteria

- All four concern areas (quality, tests, idiom, API stability) examined with evidence from the code
- Each test for REQ-ASYNC-042 and REQ-ASYNC-023 evaluated for behavioral depth (not just "does it run")
- API backward compatibility for `EventHandler` verified
- `findings.md` produced with every concern addressed and severity assigned
