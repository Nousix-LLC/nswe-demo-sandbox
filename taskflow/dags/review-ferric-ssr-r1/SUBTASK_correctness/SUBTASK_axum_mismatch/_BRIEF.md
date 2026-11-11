# SUBTASK_axum_mismatch — Mismatch Detection + Axum Integration Correctness Review

## Task Specification

**Slug**: SUBTASK_axum_mismatch
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Review PR #228 (`work/ferric-ssr-r1`, `Nousix-LLC/nswe-demo`) against the three acceptance criteria for issue
#226 (mismatch detection + Axum integration) and explicitly confirm the non-goal boundary (REQ-SSR-007/#225).
Produce `axum_mismatch_findings.md` with a named, evidence-backed verdict for each criterion.

---

## Context

This task is part of the PR #228 Correctness Review (see `../_GLOBAL.md`).

**Depends on**: none (independent spoke — runs in parallel with SUBTASK_ssr_render, SUBTASK_hydration)
**Dependents**: SUBTASK_correctness_synthesis reads this output

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Shared context | `../_GLOBAL.md` | PR coordinates, shared constraints, contract |
| PR diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | The change under review |
| Branch source | Branch `work/ferric-ssr-r1` | Full file content for mismatch detection and Axum handler code |
| Issue #226 | `gh issue view 226 --repo Nousix-LLC/nswe-demo` | mismatch detection + Axum criteria |

To browse source files on the branch, use the GitHub CLI or API:
```
gh api repos/Nousix-LLC/nswe-demo/contents/<path>?ref=work/ferric-ssr-r1 | jq -r '.content' | base64 -d
```

---

## Review Scope

Evaluate each criterion and confirm the non-goal. For each criterion: state what you checked, what you found
(CLEAN or FINDING), and evidence (file and line in `Nousix-LLC/nswe-demo`, not host paths).

### Criteria

- **REQ-SSR-006**: Does mismatch detection fire on actual structural mismatches (wrong node type, missing or
  wrong marker)? Does it log a recoverable warning (not panic) and fall back to a fresh mount for that
  subtree? Is there test coverage for the mismatch path?

- **REQ-MIS-001**: Does the Axum integration provide a handler pattern (example or real handler) that calls
  `render_to_string` and returns the HTML response? Is the pattern correct Axum code (uses `Html(...)` or
  equivalent)?

- **REQ-MIS-002**: Is the Axum-rendered HTML well-formed (balanced tags, valid attributes)? Does it contain
  the hydration markers the client needs?

### Non-goal boundary

- **REQ-SSR-007 / #225**: Do NOT evaluate async resource state carry across the SSR seam. Examine the code
  to confirm this feature is absent or only guarded/stubbed, then state that explicitly. Do not report its
  absence as a finding or deficiency.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| File | `axum_mismatch_findings.md` |
| Location | this workspace (`SUBTASK_axum_mismatch/`) |

### Output Structure

```markdown
# Mismatch Detection + Axum Integration Findings (REQ-SSR-006, REQ-MIS-001–002)

## Summary
<one paragraph: overall verdict on mismatch detection and Axum integration>

## Findings by Criterion

### REQ-SSR-006 — Mismatch detection
**Status**: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
**What was checked**: ...
**Evidence**: `<file>:<line>` (or `<file>:<start>–<end>`)
**Finding** (if any): ...

### REQ-MIS-001 — Axum handler pattern
**Status**: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
**What was checked**: ...
**Evidence**: `<file>:<line>`
**Finding** (if any): ...

### REQ-MIS-002 — HTML well-formedness and markers
**Status**: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
**What was checked**: ...
**Evidence**: `<file>:<line>`
**Finding** (if any): ...

## Non-goal Boundary
### REQ-SSR-007 / #225 — Async resource state (non-goal)
**Status**: CONFIRMED NON-GOAL
**What was checked**: <what code was examined to confirm absence or stubbing>
**Evidence**: `<file>:<line>`
```

---

## Success Criteria

- [ ] REQ-SSR-006, REQ-MIS-001, REQ-MIS-002 each have a named, evidence-backed verdict
- [ ] REQ-SSR-007/non-goal is explicitly confirmed (what code was examined, where it shows absence or stubbing)
- [ ] Evidence cites files and line numbers in `Nousix-LLC/nswe-demo` (not host paths)
- [ ] `axum_mismatch_findings.md` exists at the declared path before this task reports completed

---

## Suggested Methodology Files

**Task-type row matched**: "Ferric PR review (Rust library)" → Primary: `Code Review`; Supporting: `Rust`,
`Framework Design`

Specific files:
- `code-review/CodeReview_Process_Methodology.md` — how to structure a systematic review pass; anchoring
  findings to evidence
- `code-review/CodeReview_Checklist_Methodology.md` — concrete checklist to run against each criterion
- `rust/Rust_Web_Services_Axum_Methodology.md` — Axum integration patterns, correct use of `Html(...)`,
  handler signatures; directly applicable to REQ-MIS-001
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — SSR + hydration
  in a Rust UI framework; relevant background for mismatch detection semantics (REQ-SSR-006)

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but
is the final judge — load fewer if some are clearly inapplicable; load more if the brief reveals additional
surface the parent did not anticipate.

---

## Inherited Constraints

- **Non-goal**: #225/REQ-SSR-007 (async resource state) MUST be confirmed as absent or stubbed, not evaluated
  as deficient — this is an explicit instruction, not an oversight
- **Read-only**: Do not modify source code
- **Line citations**: All findings cite files and line numbers in `Nousix-LLC/nswe-demo`, never host paths
  or taskflow paths
- **Non-blockers**: Flag them but they do not hold the landing
- **Machine gate**: CI passed — treat as a floor; check substance beyond what tests assert
