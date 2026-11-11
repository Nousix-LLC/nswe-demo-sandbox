# Task: Q2 — EventHandler Abstraction Boundary Review

## Task Specification

**Slug**: SUBTASK_q2_eventhandler
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Examine whether the `EventHandler` enum variant scheme (`NoArg` / event-carrying variant) introduced in `vdom.rs` and dispatched in `dom.rs` is a sound abstraction boundary — specifically whether `vdom.rs` stays free of `web_sys` imports that would bleed the DOM dependency into the virtual DOM layer.

### Context

Part of the Concern 2 (code quality) decomposition. See `_GLOBAL.md` for full context, shared inputs, and inherited constraints. Output schema is declared in `../contracts/_MANIFEST.yaml` (sub_finding_format).

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `_GLOBAL.md` | Inherited constraints, scope |
| PR #193 diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Changed lines |
| vdom.rs | `crates/ferric/src/vdom.rs` | EventHandler enum definition |
| dom.rs | `crates/ferric/src/dom.rs` | EventHandler dispatch logic |

---

## Review Scope

Examine the following for Q2 specifically:

1. **EventHandler enum soundness**: Is the `NoArg` / event-carrying variant scheme a good model for the two event-handler cases? Does it model the distinction cleanly (i.e., is `NoArg` the right name, are the variants ergonomic to match, does the enum cover the actual use cases without being over-general or under-general)?
2. **vdom.rs / web_sys boundary**: Does `vdom.rs` import any `web_sys` types directly? If it does, does that bleed the concrete DOM layer into the virtual DOM abstraction — and is that a problem? Check `use web_sys::*` and any `web_sys::` qualification in vdom.rs specifically.
3. **Dispatch in dom.rs**: Does `dom.rs` correctly consume the `EventHandler` variants? Is the dispatch logic clear and complete (does every variant get handled, no unreachable arms)?
4. **Abstraction boundary completeness**: Does the boundary between `vdom.rs` (virtual DOM) and `dom.rs` (concrete DOM) make sense at the EventHandler level? Could a future contributor understand where to add a new event-handler variant without touching the wrong layer?

---

## Output Specification

**Primary Output:** `sub_findings.md` at this task's workspace root

Must follow `../contracts/_MANIFEST.yaml` sub_finding_format:
- `## Findings` section: one entry per finding or clean verification
- `## What was examined` section: files, line ranges, sub-question coverage

Each `## Findings` entry MUST use:
- `severity`: blocker | non-blocker | clean
- `concern`: code-quality
- `location`: repository-relative path (e.g., `crates/ferric/src/vdom.rs:38`) or `"structural"`
- `description`: for clean, what was checked and found sound; for findings, the issue, why it matters, and what would satisfy

---

## Success Criteria

- `vdom.rs` and `dom.rs` examined at the `EventHandler` definition and dispatch sites
- `vdom.rs` import list checked for `web_sys` leakage
- Dispatch completeness in `dom.rs` checked (match arms)
- `sub_findings.md` produced with `## Findings` and `## What was examined`

---

## Suggested Methodology Files

Task type row (Domain Mapping): **Ferric PR review (Rust library)** → Primary: `code-review`, Supporting: `rust`, `framework-design`

Specific files flagged for Q2:

- `framework-design/FrameworkDesign_Library_API_Design_Methodology.md` — abstraction boundary discipline, invitability of correct use. Rationale: the `EventHandler` enum redesign is a library abstraction; this methodology covers whether it is well-bounded, models the right cases, and maintains clean layer separation.
- `code-review/CodeReview_Checklist_Methodology.md` — coupling and boundary evaluation during review. Rationale: `web_sys` leakage into `vdom.rs` is a classic coupling red flag that the review checklist surfaces.
- `rust/Rust_Trait_Design_Methodology.md` — Rust abstraction patterns; enum design. Rationale: enum variant ergonomics and exhaustive pattern matching are Rust-specific concerns; this methodology covers when enum variants are the right abstraction and how to judge them.

These are SUGGESTIONS. Load fewer if some are clearly inapplicable; load more if your reading of the files reveals additional methodology surface needed.

## Inherited Constraints

- Repository-relative paths only
- Issues #196–#201 MUST NOT be re-raised
- Severity `blocker` only if a requirement is unmet or an existing public API contract is broken; style/preference = at most `non-blocker`
- Do not cover Q1 (coupling), Q3 (generation counter), or Q4 (correct-use) — those have their own spoke tasks
