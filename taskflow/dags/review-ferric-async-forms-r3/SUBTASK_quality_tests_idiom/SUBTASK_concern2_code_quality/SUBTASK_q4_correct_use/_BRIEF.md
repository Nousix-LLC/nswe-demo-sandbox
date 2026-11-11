# Task: Q4 — Correct-Use Design Review

## Task Specification

**Slug**: SUBTASK_q4_correct_use
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Examine whether the design across all four changed files invites correct use and discourages misuse — whether callers have clear paths that are hard to get wrong.

### Context

Part of the Concern 2 (code quality) decomposition. See `_GLOBAL.md` for full context, shared inputs, and inherited constraints. Output schema is declared in `../contracts/_MANIFEST.yaml` (sub_finding_format).

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `_GLOBAL.md` | Inherited constraints, scope |
| PR #193 diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Changed lines |
| async_resource.rs | `crates/ferric/src/async_resource.rs` | `create_resource` API |
| vdom.rs | `crates/ferric/src/vdom.rs` | EventHandler API surface |
| dom.rs | `crates/ferric/src/dom.rs` | Dispatch and registration API |
| form.rs | `crates/ferric/src/form.rs` | `on_input_event_handler` API |

---

## Review Scope

Examine the following for Q4 specifically:

1. **`on_input_event_handler` calling convention** (form.rs): Is the function signature unambiguous? Are parameter types precise enough to prevent common mistakes (e.g., passing the wrong closure type, providing arguments in the wrong order)? Does the name communicate what it does and when to use it?
2. **`create_resource` API** (async_resource.rs): Does the public interface make it clear how a caller is expected to use the resource? Are there footguns in the API — ways a caller could misuse the resource lifecycle that the type system does not prevent?
3. **EventHandler registration paths** (vdom.rs, dom.rs): When a caller wants to register an event handler, is the path clear? Is there one obvious way to do it, or multiple paths that might lead to confusion?
4. **Type system encoding**: Does the design encode correctness constraints in types (making incorrect states unrepresentable) or does it rely on caller conventions and runtime checks? Note specific examples where types help or where they leave correctness to convention.

This is NOT a re-examination of module boundaries (that is Q1) or EventHandler variant design (that is Q2). Focus is on the caller's perspective: "If I were using this library for the first time, what could I get wrong?"

---

## Output Specification

**Primary Output:** `sub_findings.md` at this task's workspace root

Must follow `../contracts/_MANIFEST.yaml` sub_finding_format:
- `## Findings` section: one entry per finding or clean verification
- `## What was examined` section: files, line ranges, sub-question coverage

Each `## Findings` entry MUST use:
- `severity`: blocker | non-blocker | clean
- `concern`: code-quality
- `location`: repository-relative path (e.g., `crates/ferric/src/form.rs:12`) or `"structural"`
- `description`: for clean, what was checked and found sound; for findings, the issue, why it matters, and what would satisfy

---

## Success Criteria

- All four files examined for caller-facing API surface
- `on_input_event_handler`, `create_resource`, and event-handler registration paths specifically examined
- Type-encoding of invariants assessed
- `sub_findings.md` produced with `## Findings` and `## What was examined`

---

## Suggested Methodology Files

Task type row (Domain Mapping): **Ferric PR review (Rust library)** → Primary: `code-review`, Supporting: `rust`, `framework-design`

Specific files flagged for Q4:

- `framework-design/FrameworkDesign_Library_API_Design_Methodology.md` — the central methodology for this sub-question. Rationale: Q4 is exactly the library API design question ("does it invite correct use?"); this methodology encodes criteria for API surface clarity, footgun detection, and type-driven correctness.
- `code-review/CodeReview_Checklist_Methodology.md` — caller-centric review criteria. Rationale: the checklist's section on interface design and correct-use invitation is directly applicable.
- `rust/Rust_Type_System_Methodology.md` — Rust-specific type encoding of invariants (newtypes, wrapper types, builder patterns). Rationale: Q4 asks whether types encode correctness; this methodology covers where Rust's type system prevents misuse and where it does not.

These are SUGGESTIONS. Load fewer if some are clearly inapplicable; load more if your reading of the files reveals additional methodology surface needed.

## Inherited Constraints

- Repository-relative paths only
- Issues #196–#201 MUST NOT be re-raised
- Severity `blocker` only if a requirement is unmet or an existing public API contract is broken; style/preference = at most `non-blocker`
- Do not cover Q1 (coupling), Q2 (EventHandler boundary), or Q3 (generation counter) — those have their own spoke tasks
