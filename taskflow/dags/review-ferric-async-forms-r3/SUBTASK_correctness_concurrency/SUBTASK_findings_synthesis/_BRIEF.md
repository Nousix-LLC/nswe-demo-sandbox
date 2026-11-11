# Task: Synthesis — Collect Spoke Findings into findings.md

## Task Specification

**Slug**: SUBTASK_findings_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_b1_concurrency, SUBTASK_b2_event, SUBTASK_b3_form
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Collect the three spoke findings (B1+concurrency, B2, B3) and synthesize them into the
required `findings.md` at the SUBTASK_correctness_concurrency workspace root, following
the ancestor findings schema from `review-ferric-async-forms-r3/contracts/_MANIFEST.yaml`.

---

## Context

See `../_GLOBAL.md` for subtree context. See `../../_GLOBAL.md` for full project context.

This synthesis task reads the three spoke outputs and composes a single `findings.md`
that covers all requirements in scope (REQ-ASYNC-001, 003, 005, 016, 023, 042) and
the concurrency assessment. It does NOT re-do the analysis — it merges and verifies
coverage, then writes the final document.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `../_GLOBAL.md` | Scope, constraints, contract |
| Project context | `../../_GLOBAL.md` | Acceptance criteria, findings schema |
| B1+concurrency findings | `../SUBTASK_b1_concurrency/b1_findings.md` | REQ-ASYNC-001,003,005,016 + concurrency |
| B2 findings | `../SUBTASK_b2_event/b2_findings.md` | REQ-ASYNC-023 |
| B3 findings | `../SUBTASK_b3_form/b3_findings.md` | REQ-ASYNC-042 |
| Ancestor contract | `../../contracts/_MANIFEST.yaml` | Required findings.md schema |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Ownership + identities |

---

## Synthesis Scope

1. Verify coverage: every requirement in scope (REQ-ASYNC-001, 003, 005, 016, 023, 042)
   must appear in at least one spoke finding (clean or blocker).
2. Verify no blockers are hidden under approvals — if any spoke finding is severity=blocker,
   escalate it to the top of findings.md.
3. Verify non-blocker constraint: nothing from #196–#201 is re-raised as a blocker.
4. Compose the unified `findings.md` that merges all entries in a single coherent document.

---

## Output Specification

**Primary Output**: `findings.md` at `../` (the SUBTASK_correctness_concurrency workspace root)

Absolute path: `review-ferric-async-forms-r3/SUBTASK_correctness_concurrency/findings.md`

The file MUST follow the ancestor schema from `../../contracts/_MANIFEST.yaml`:

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

## Constraints

- Write findings.md to the PARENT workspace root (one directory up from this workspace)
- Do NOT re-raise non-blockers #196–#201 as blockers
- Repository-relative paths only
- Every requirement in scope must appear in the output

## Success Criteria

- findings.md written at SUBTASK_correctness_concurrency/findings.md
- All 6 requirements (REQ-ASYNC-001, 003, 005, 016, 023, 042) covered
- Concurrency assessment included
- Schema matches ancestor contract
- No coverage gaps
