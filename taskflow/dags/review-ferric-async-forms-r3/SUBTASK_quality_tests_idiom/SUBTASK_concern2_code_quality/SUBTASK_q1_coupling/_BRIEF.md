# Task: Q1 — Responsibility Partitioning and Coupling Review

## Task Specification

**Slug**: SUBTASK_q1_coupling
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Examine whether `async_resource.rs`, `vdom.rs`, `form.rs`, and `dom.rs` each own a clean slice of responsibility, and whether the PR #193 remediation commits introduce unexpected imports or cross-module coupling.

### Context

Part of the Concern 2 (code quality) decomposition. See `_GLOBAL.md` for full context, shared inputs, and inherited constraints. Output schema is declared in `../contracts/_MANIFEST.yaml` (sub_finding_format).

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `_GLOBAL.md` | Inherited constraints, scope |
| PR #193 diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Changed lines |
| async_resource.rs | `crates/ferric/src/async_resource.rs` | Full file read |
| vdom.rs | `crates/ferric/src/vdom.rs` | Full file read |
| dom.rs | `crates/ferric/src/dom.rs` | Full file read |
| form.rs | `crates/ferric/src/form.rs` | Full file read |

---

## Review Scope

Examine the following for Q1 specifically:

1. Does each file own one clear layer of responsibility?
   - `async_resource.rs`: resource lifecycle (signal/subscription management, generation counter) — no DOM concerns expected here
   - `vdom.rs`: virtual DOM representation — expected to be free of concrete DOM / `web_sys` imports
   - `dom.rs`: concrete DOM dispatch and event wiring — the bridge to the browser
   - `form.rs`: form-event handling at the application layer — should not reach into resource lifecycle internals
2. Does the remediation introduce unexpected imports or cross-layer dependencies? Check `use` statements and `extern crate` in each changed file.
3. Are there any module-boundary concerns not covered by Q2 (EventHandler enum design) or Q4 (correct-use)? Those sub-questions have their own spokes; do not overlap.

Evidence-based: for each file, check the import list and the function signatures at the module boundary. State what you found in each file, not just a summary.

---

## Output Specification

**Primary Output:** `sub_findings.md` at this task's workspace root

Must follow `../contracts/_MANIFEST.yaml` sub_finding_format:
- `## Findings` section: one entry per finding or clean verification
- `## What was examined` section: files, line ranges, sub-question coverage

Each `## Findings` entry MUST use:
- `severity`: blocker | non-blocker | clean
- `concern`: code-quality
- `location`: repository-relative path (e.g., `crates/ferric/src/async_resource.rs:14`) or `"structural"`
- `description`: for clean, what was checked and found sound; for findings, the issue, why it matters, and what would satisfy

---

## Success Criteria

- All four files examined for responsibility partitioning
- Import/dependency lists reviewed for unexpected cross-module coupling
- `sub_findings.md` produced with `## Findings` and `## What was examined`
- Each finding references specific file and line range
- Severity assigned accurately per inherited calibration

---

## Suggested Methodology Files

Task type row (Domain Mapping): **Ferric PR review (Rust library)** → Primary: `code-review`, Supporting: `rust`, `framework-design`

Specific files flagged for Q1:

- `code-review/CodeReview_Checklist_Methodology.md` — review-process checklist; covers coupling, responsibility boundaries, and dependency checks. Rationale: provides the structural lens for identifying when a module's responsibilities have drifted or when it imports from an unexpected layer.
- `code-quality/Framework_Clean_Code_Methodology.md` — Single Responsibility Principle, cohesion. Rationale: Q1 is directly asking whether each file has one clear responsibility; Clean Code's SRP criteria are the right rubric.
- `rust/Rust_Library_API_And_Stability_Methodology.md` — module-level API design and boundary discipline in Rust libraries. Rationale: coupling issues often manifest as leaky module-level APIs; this methodology encodes what a clean Rust module boundary looks like.

These are SUGGESTIONS. Load fewer if some are clearly inapplicable; load more if your reading of the files reveals additional methodology surface needed.

## Inherited Constraints

- Repository-relative paths only
- Issues #196–#201 MUST NOT be re-raised
- Severity `blocker` only if a requirement is unmet or an existing public API contract is broken; style/preference = at most `non-blocker`
- Do not cover Q2 (EventHandler boundary), Q3 (generation counter), or Q4 (correct-use) — those have their own spoke tasks
