# Task: Assess ferric-macros/context scope from PR #192

## Task Specification

**Slug**: SUBTASK_macros-assessment  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

Analyze the 12 ferric-macros and ferric context API commits that were bundled into PR #192 (`work/ferric-router-r1`) without a review brief. Produce a structured scope assessment document that:
1. Maps each commit to the GitHub issue(s) it closes (#137–#142)
2. Estimates the size and complexity of each concern
3. Identifies the design documents / acceptance criteria that should anchor a proper review brief
4. Recommends how to structure the follow-on PR(s) for these changes

### Context

This task is part of the ferric-router-r2 remediation DAG (see `../_GLOBAL.md`).

The review-ferric-router-r1 verdict (REQUEST CHANGES, blocker B1) found that ~3,290 lines of proc-macro code and ferric context API changes were bundled into the router PR without being described in the PR body or presented with acceptance criteria. This assessment is the first step toward commissioning a proper review for those changes.

**Git repository**: `/home/user/nswe-demo` on server `mattm@100.90.75.93`  
**SSH command pattern** (per `../../../CLAUDE.md`):
```bash
ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 \
  'bash -lc "cd /home/user/nswe-demo && <git command>"'
```

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Understand scope and the 12 commits to assess |
| Contract manifest | `../contracts/_MANIFEST.yaml` | Confirm owned output path |
| Review synthesis | `../../review-ferric-router-r1/SYNTHESIS.md` | See what the reviewer found (not reviewed, security gap noted for proc-macros) |

### The 12 commits to assess (from `work/ferric-router-r1`, NOT going to `work/ferric-router-r2`)

| Commit | Description | Likely issue(s) |
|--------|-------------|-----------------|
| `1ccdce0` | `test(ferric): baseline audit — #137 and #138 ACs satisfied` | #137, #138 |
| `3be2f51` | `feat(ferric-macros): scaffold proc-macro crate with stub view! macro` | #139 |
| `912ed57` | `ferric: wire ferric-macros dependency and re-export view! in prelude` | #139 |
| `d25a7f7` | `feat(ferric-macros): implement full view! proc-macro (sec 2.12 + 2.9)` | #139 |
| `3c3d4aa` | `feat(ferric-macros): implement view! macro (#139)` | #139 |
| `4c77b9a` | `test(ferric-macros): conformance tests for view! lowering table (§2.12)` | #139 |
| `c28b0e1` | `fix(ferric): re-export VElement, VNode, EventKind at crate root` | (support) |
| `d027534` | `fix(conformance): resolve VElement::into() type ambiguity in test_nested_element` | (support) |
| `0088a5c` | `feat(ferric): implement #[component] macro, Children/Slot/SlotFn types (#140)` | #140 |
| `82d267f` | `feat(ferric): implement context API — provide_context, use_context, expect_context (#142)` | #142 |
| `763f4d6` | `feat(ferric-macros): add compile-fail diagnostic suite for component authoring mistakes (#141)` | #141 |
| `e29e2f4` | `fix(ci): resolve fmt, clippy, and rustdoc failures on ferric-macros` | (CI) |

---

## Process Specification

The task involves:
1. Examining the commit diffs on `work/ferric-router-r1` for each of the 12 commits
2. Reviewing the `crates/ferric-macros/` directory structure and key source files
3. Looking at issues #137–#142 on GitHub to understand the design context
4. Assessing the proc-macro security surface (proc-macros execute at compile time — a trust-surface addition noted by the reviewer)
5. Identifying what design documents exist (the Ferric 1.0 design commit `9a24c28` appears in the branch history)
6. Producing the structured assessment

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `macros-assessment.md` |
| Location | `outputs/` |

### Output Structure

```markdown
# Ferric-Macros/Context Scope Assessment

## Executive Summary
<2-3 sentence summary of what these commits add and the recommended path forward>

## Scope Overview

### crates/ferric-macros/ — New crate
<size, purpose, key source files and their line counts>

### crates/ferric/ context API changes
<what changed in signal.rs, component.rs, lib.rs>

## Issue-to-Commit Mapping

### #137: <issue title>
<commits, ACs, what was done>

### #138: <issue title>
...etc through #142

## Complexity Assessment

| Area | Lines | Complexity | Notes |
|------|-------|------------|-------|
| `crates/ferric-macros/` proc-macro crate | ~N | High/Med/Low | <note> |
| ferric context API (signal.rs) | +163 | ... | ... |
| ferric #[component] types (component.rs) | +34 | ... | ... |
| ferric re-exports (lib.rs) | +13 | ... | ... |

## Security Surface Note
<Proc-macros execute at compile time — this is a build-time trust-surface addition.
What the code does, whether it reads env vars / filesystem, what the security posture is>

## Design Documents Available
<List any design documents referenced in commit messages or found in the repo>

## Recommended PR Structure
<Should this be one PR or multiple? What would the PR title/brief/acceptance-criteria look like?>

## Suggested Review Brief Template
<Outline of the _BRIEF.md that should be authored for the follow-on review task>
```

---

## Success Criteria

- [ ] All 12 commits assessed (not just the ferric-macros commits — the ferric context API commits too)
- [ ] Issue-to-commit mapping complete (#137–#142)
- [ ] `crates/ferric-macros/` structure described with file-level line counts
- [ ] Security surface note present (proc-macro compile-time execution)
- [ ] A recommended PR structure provided (one PR or multiple, with reasoning)
- [ ] `outputs/macros-assessment.md` exists

---

## Suggested Methodology Files

**Task-type row matched**: "Ferric PR review (Rust library)" → Primary: `code-review`, Supporting: `rust`, `framework-design`

**Specific files to load**:
- `code-review/CodeReview_Checklist_Methodology.md` — the review checklist framework; use it to structure the assessment of each concern area.
- `rust/Rust_Macros_And_Codegen_Methodology.md` — proc-macro (proc-macro vs macro_rules vs build.rs) design considerations; especially relevant for assessing the `crates/ferric-macros/` proc-macro crate and its security surface.

*Rationale*: The core work is analyzing a Rust proc-macro crate and understanding its security/complexity profile. The code review checklist methodology provides the right frame for a structured assessment. The Rust macros methodology provides specific criteria for assessing proc-macro design quality and compile-time trust surface.

**These are the parent's suggestions; the child agent loads what its own work requires — load fewer if inapplicable, load more if the work reveals additional needs.**

---

## Inherited Constraints

- Use SSH for all server operations per `CLAUDE.md`
- Server address MUST NOT appear in GitHub issues, PRs, or committed files
- Read-only analysis only — do NOT modify any code or create branches in this task
- Do NOT open a PR for the macros scope — only produce the assessment document
- The macros changes are on `work/ferric-router-r1`; examine them there, do not create any new branch

---

## Out-of-Scope Methodologies

- `operations/GitWorkflow_PR_Lifecycle_Methodology.md` — not creating a PR here, only assessing scope
- `synthesis/` bundle — this is a standard (not synthesis) task
