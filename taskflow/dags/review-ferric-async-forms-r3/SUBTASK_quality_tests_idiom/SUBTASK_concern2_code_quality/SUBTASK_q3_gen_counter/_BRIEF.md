# Task: Q3 — Generation Counter Clarity Review

## Task Specification

**Slug**: SUBTASK_q3_gen_counter
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Examine whether the generation counter in `create_resource` (in `async_resource.rs`) is followable by a future reader — specifically whether the invariant (what the counter guards and how) is expressed at the right level of abstraction without requiring multi-layer tracing.

### Context

Part of the Concern 2 (code quality) decomposition. See `_GLOBAL.md` for full context, shared inputs, and inherited constraints. Output schema is declared in `../contracts/_MANIFEST.yaml` (sub_finding_format).

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `_GLOBAL.md` | Inherited constraints, scope |
| PR #193 diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Changed lines |
| async_resource.rs | `crates/ferric/src/async_resource.rs` | Full file read |

---

## Review Scope

Examine the following for Q3 specifically:

1. **Counter invariant clarity**: Can a reader encountering the generation counter for the first time understand what it guards — without following references into multiple other functions or modules? Is there a comment, docstring, or naming choice that explains the invariant at the declaration site?
2. **Abstraction level**: Is the counter logic expressed at the right level of abstraction? Could the invariant be misread as something simpler (e.g., a plain length counter) or more complex than it is?
3. **State transition clarity**: At each site where the counter is incremented, decremented, or compared — is it obvious what state transition is being guarded? Would a reader catching a bug in the counter logic understand immediately that the counter is essential and what it protects?
4. **Naming**: Does the counter variable name communicate its purpose? Does it distinguish itself from incidental counters (e.g., loop counters, length tracking)?

This is NOT a correctness review (that is Q1 or the async/reactive concern). This is about whether the counter's design communicates its own purpose clearly.

---

## Output Specification

**Primary Output:** `sub_findings.md` at this task's workspace root

Must follow `../contracts/_MANIFEST.yaml` sub_finding_format:
- `## Findings` section: one entry per finding or clean verification
- `## What was examined` section: files, line ranges, sub-question coverage

Each `## Findings` entry MUST use:
- `severity`: blocker | non-blocker | clean
- `concern`: code-quality
- `location`: repository-relative path (e.g., `crates/ferric/src/async_resource.rs:85`) or `"structural"`
- `description`: for clean, what was checked and found sound; for findings, the issue, why it matters, and what would satisfy

---

## Success Criteria

- Generation counter declaration and all use sites examined in `async_resource.rs`
- Counter naming, surrounding comments/docs, and abstraction level assessed
- `sub_findings.md` produced with `## Findings` and `## What was examined`

---

## Suggested Methodology Files

Task type row (Domain Mapping): **Ferric PR review (Rust library)** → Primary: `code-review`, Supporting: `rust`, `framework-design`

Specific files flagged for Q3:

- `code-quality/Framework_Clean_Code_Methodology.md` — naming, single-level-of-abstraction, explaining intent through code. Rationale: Q3 is specifically about whether the counter communicates its own invariant; Clean Code's criteria for naming and abstraction level are the right rubric.
- `code-review/CodeReview_Checklist_Methodology.md` — review criteria for clarity and self-documentation. Rationale: generation counters that require mental simulation to understand are a known code quality risk; the checklist surfaces this category.
- `operations/BestPractices_Code_Comments_Methodology.md` — when and how comments add value vs. clutter. Rationale: the question is whether a comment is needed at the counter declaration, and this methodology encodes criteria for making that judgment.

These are SUGGESTIONS. Load fewer if some are clearly inapplicable; load more if your reading of the files reveals additional methodology surface needed.

## Inherited Constraints

- Repository-relative paths only
- Issues #196–#201 MUST NOT be re-raised
- Severity `blocker` only if a requirement is unmet or an existing public API contract is broken; style/preference = at most `non-blocker`
- Do not cover Q1 (coupling), Q2 (EventHandler boundary), or Q4 (correct-use) — those have their own spoke tasks
- Correctness of the counter logic itself is out of scope for this spoke (that belongs to Concern 1 or the correctness review)
