# Task: B3 Correctness Analysis — Bind::on_input_event_handler (form.rs)

## Task Specification

**Slug**: SUBTASK_b3_form
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Verify that B3 (REQ-ASYNC-042) is correctly implemented in `Bind<T>::on_input_event_handler()`
in `crates/ferric/src/form.rs` (PR #193, head `838239e`), including the WASM test
that exercises this path end-to-end.

---

## Context

See `../_GLOBAL.md` for subtree context. See `../../_GLOBAL.md` for full project
context and acceptance criteria for REQ-ASYNC-042.

**Files to review**:
- `crates/ferric/src/form.rs` — Bind::on_input_event_handler() implementation and WASM test

**Key commit**: `838239e` — "B3 (REQ-ASYNC-042): add Bind::on_input_event_handler() + WASM test"

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `../_GLOBAL.md` | Scope, constraints, contract |
| Project context | `../../_GLOBAL.md` | REQ-ASYNC-042 acceptance criteria |
| PR diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Changed lines in form.rs |
| Inherited contract | `../../contracts/_MANIFEST.yaml` | Findings schema |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Ownership + identities |

---

## Review Scope

**B3 correctness questions (REQ-ASYNC-042):**
- Does `Bind<T>` have `on_input_event_handler(&self) -> EventHandler`?
- Does it return `EventHandler::WithEvent`?
- Does the handler: (a) downcast `&dyn Any` → `&web_sys::Event` → target → `HtmlInputElement` via `dyn_into`, (b) read `HtmlInputElement::value()`, (c) write to the field's raw signal?
- Is signal write ordering correct — write happens on each `input` event, not deferred?
- Is the method gated to `#[cfg(target_arch = "wasm32")]`? If so, is this compatible with REQ-ASYNC-042 (which requires the method to exist)?
- Does the WASM test (`on_input_event_handler_updates_signal_from_dom_value`): (a) use a real DOM element, (b) set element value, (c) dispatch a synthetic input event, (d) assert the field signal equals the typed value? Does this test cover the full DOM→signal path?
- If any step in the downcast chain fails (no target, target not an input), does the handler fail gracefully (no panic)?

---

## Output Specification

**Primary Output**: `b3_findings.md` at `SUBTASK_b3_form/` workspace root

Must contain:
1. `## Findings` — entries for each question above with:
   - severity: blocker | non-blocker | clean
   - requirement: REQ-ASYNC-042
   - location: crates/ferric/src/form.rs:LINE
   - description
2. `## What was examined` — files, line ranges, specific questions checked

---

## Constraints

- Repository-relative paths only in all locations
- Non-blockers #196–#201 must NOT be re-raised as blockers
- A finding is a blocker only if REQ-ASYNC-042 is unmet

## Success Criteria

- REQ-ASYNC-042 answered with evidence from code
- WASM test coverage assessed end-to-end
- on_input_event_handler WASM gating assessed for requirement compatibility
- b3_findings.md produced with every question answered and severity assigned
