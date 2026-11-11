# Task: B2 Correctness Analysis — EventHandler enum (vdom.rs + dom.rs)

## Task Specification

**Slug**: SUBTASK_b2_event
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Verify that B2 (REQ-ASYNC-023) is correctly implemented in the `EventHandler` enum
redesign in `crates/ferric/src/vdom.rs` and the event dispatch in `crates/ferric/src/dom.rs`
(PR #193, head `838239e`).

---

## Context

See `../_GLOBAL.md` for subtree context. See `../../_GLOBAL.md` for full project
context and acceptance criteria for REQ-ASYNC-023.

**Files to review**:
- `crates/ferric/src/vdom.rs` — EventHandler enum definition and VElement builder methods
- `crates/ferric/src/dom.rs` — set_events dispatch of both variants

**Key commit**: `9557f0c` — "feat(ferric): redesign EventHandler as enum for event-carrying closures"

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `../_GLOBAL.md` | Scope, constraints, contract |
| Project context | `../../_GLOBAL.md` | REQ-ASYNC-023 acceptance criteria |
| PR diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Changed lines in vdom.rs + dom.rs |
| Inherited contract | `../../contracts/_MANIFEST.yaml` | Findings schema |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Ownership + identities |

---

## Review Scope

**B2 correctness questions (REQ-ASYNC-023):**
- Is `EventHandler` now an enum with `NoArg` and `WithEvent` variants?
- Does `WithEvent` carry `Rc<dyn Fn(&dyn std::any::Any)>` (or equivalent) so callers can receive the event?
- Does a handler receiving `&dyn Any` have a clear downcast path to `&web_sys::Event` for calling `prevent_default()`/`stop_propagation()`?
- Does `vdom.rs` import `web_sys`? (It must NOT — verify no `use web_sys` appears in the vdom.rs diff.)
- Is backward compatibility preserved? Do existing callers passing `impl Fn()` to `VElement::on_event()` still compile via the `on()` builder?
- Does `dom.rs` correctly dispatch both variants (`NoArg` → call with no args; `WithEvent` → pass `&event as &dyn Any`)?
- Does the WASM test in `dom.rs` exercise the `WithEvent` → `prevent_default()` path?

---

## Output Specification

**Primary Output**: `b2_findings.md` at `SUBTASK_b2_event/` workspace root

Must contain:
1. `## Findings` — entries for each question above with:
   - severity: blocker | non-blocker | clean
   - requirement: REQ-ASYNC-023
   - location: crates/ferric/src/vdom.rs:LINE or crates/ferric/src/dom.rs:LINE
   - description
2. `## What was examined` — files, line ranges, specific questions checked

---

## Constraints

- Repository-relative paths only in all locations
- Non-blockers #196–#201 must NOT be re-raised as blockers
- A finding is a blocker only if REQ-ASYNC-023 is unmet

## Success Criteria

- REQ-ASYNC-023 answered with evidence from code
- vdom.rs isolation from web_sys verified
- Backward compatibility verified
- dom.rs dispatch of both variants verified
- b2_findings.md produced with every question answered and severity assigned
