# Task: Correctness and Concurrency Review — PR #193 Ferric Async

## Task Specification

**Slug**: SUBTASK_correctness_concurrency  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  
**Assigned To**: swe-reviewer

### Objective

Verify that B1 (REQ-ASYNC-001, 003, 005, 016), B2 (REQ-ASYNC-023), and B3 (REQ-ASYNC-042) are correctly implemented in PR #193 (`work/ferric-async-forms-r2`, head `838239e`). Additionally verify there are no concurrency or async hazards in the `spawn_local` / reactive-effect composition (concern 4 from review scope).

---

## Context

See `../_GLOBAL.md` for full project context, acceptance criteria, and key reference data.

**Files changed by the three remediation commits:**
- `crates/ferric/src/async_resource.rs` — B1 (`create_resource` reactive constructor + generation counter)
- `crates/ferric/src/vdom.rs` — B2 (`EventHandler` enum redesign)
- `crates/ferric/src/dom.rs` — B2 (dispatch of both `EventHandler` variants)
- `crates/ferric/src/form.rs` — B3 (`on_input_event_handler()` + WASM test)

Fetch the PR diff and read the relevant source files using `gh pr diff 193 --repo Nousix-LLC/nswe-demo` and `gh pr view 193 --repo Nousix-LLC/nswe-demo`, then read individual source files directly.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Acceptance criteria, scope, key data |
| PR #193 diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Actual changed lines |
| async_resource.rs | `crates/ferric/src/async_resource.rs` | B1 implementation |
| vdom.rs | `crates/ferric/src/vdom.rs` | B2 EventHandler enum |
| dom.rs | `crates/ferric/src/dom.rs` | B2 event dispatch |
| form.rs | `crates/ferric/src/form.rs` | B3 on_input_event_handler |

---

## Review Scope

Examine the following correctness questions against the actual code:

**B1 — REQ-ASYNC-001, 003, 005, 016:**
- Does `create_resource(source, fetcher)` exist as a two-argument function? Does it fire immediately on construction (REQ-ASYNC-001)?
- When a signal read by `source()` changes, does the resource reset to `Loading` and re-trigger the fetcher with the new source value (REQ-ASYNC-003)?
- Are in-flight futures from stale source values discarded — specifically, is there a generation counter, and does the future compare its generation before writing its result (REQ-ASYNC-005, REQ-ASYNC-016)?
- Is the generation counter implementation sound in a single-threaded WASM executor? Can a stale future's result race to overwrite a newer result?

**B2 — REQ-ASYNC-023:**
- Is `EventHandler` an enum with `NoArg` and `WithEvent` variants?
- Does `WithEvent` carry a `Rc<dyn Fn(&dyn std::any::Any)>` (or equivalent) so callers can receive the event?
- Does a handler receiving `&dyn Any` have a clear downcast path to `&web_sys::Event` for calling `prevent_default()`/`stop_propagation()`?
- Does `vdom.rs` import `web_sys`? (It must NOT.)
- Is backward compatibility preserved? Do existing callers passing `impl Fn()` to `VElement::on_event()` still compile?
- Does `dom.rs` correctly dispatch both variants?

**B3 — REQ-ASYNC-042:**
- Does `Bind<T>` have `on_input_event_handler(&self) -> EventHandler`?
- Does it return `EventHandler::WithEvent`?
- Does the handler: (a) downcast `&dyn Any` → `&web_sys::Event` → `HtmlInputElement` via `target()`, (b) read `HtmlInputElement::value()`, (c) write to the field signal?
- Is signal write ordering correct (write happens on each `input` event, not deferred)?

**Concurrency and async hazards (concern 4):**
- Does `create_resource` use `spawn_local` inside a reactive effect (`create_effect`)? If so, verify there are no double-borrow or use-after-free issues in closure captures (Rust's borrow checker should catch most of these, but check `clone`/`Rc` patterns).
- Does the generation counter use types with `'static` bounds as required by the async closure?
- Is there any scenario where the effect and the future's completion race to access the same mutable state without protection? (In a single-threaded WASM executor this is safe, but verify the reasoning is sound.)

---

## Output Specification

**Primary Output:** `findings.md` at this task's workspace root (`SUBTASK_correctness_concurrency/findings.md`)

The findings file MUST contain:

```markdown
## Findings

[For each finding or clean verification, an entry with:
- severity: blocker | non-blocker | clean
- requirement: REQ-ASYNC-NNN (where applicable)
- location: crates/ferric/src/file.rs:LINE
- description: what was found]

## What was examined

[Enumeration of files, line ranges, and specific questions examined,
so the synthesis task can confirm coverage without gaps]
```

---

## Suggested Methodology Files

Task type row (Domain Mapping): **Ferric PR review (Rust library)** → Primary: `code-review`, Supporting: `rust`, `framework-design`

Specific files to load:
- `code-review/CodeReview_Checklist_Methodology.md` — correctness review checklist; apply to each REQ-ASYNC-NNN
- `code-review/CodeReview_Process_Methodology.md` — review process and severity calibration
- `rust/Rust_Async_Tokio_Methodology.md` — `spawn_local`, async closure captures, `'static` bounds
- `rust/Rust_Ownership_Borrowing_Methodology.md` — closure capture patterns, `Rc` sharing

These are SUGGESTIONS. Load fewer if some are clearly inapplicable; load more if the brief reveals additional methodology surface needed.

## Inherited Constraints

- Verdict and findings must be independent of the code DAG's own synthesis (`taskflow/dags/ferric-async-forms-r3/SYNTHESIS.md`) — that document is a code-DAG self-report; this review's findings must be derived from reading the actual source code
- Repository-relative paths only in all findings (no host paths, no taskflow paths)
- Non-blockers previously filed as #196–#201 must NOT be re-raised as blockers
- Severity calibration: a finding is a blocker only if it means the requirement is unmet; a preference or style difference is at most non-blocker

## Success Criteria

- All B1, B2, B3 correctness questions above answered with evidence from the code
- Concurrency hazard assessment complete for `spawn_local` / reactive effect composition
- `findings.md` produced with every question answered and severity assigned
- No unexamined acceptance criterion
