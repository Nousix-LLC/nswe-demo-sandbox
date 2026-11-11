# Task: Synthesize Sub-Findings into finding.md

## Task Specification

**Slug**: SUBTASK_sec_event_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_sec_event_downcast, SUBTASK_sec_event_forget
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Compile the two sub-findings from the downcast and closure.forget() spokes into the single `finding.md` required by the parent security review contract (`../_GLOBAL.md` §Contract and `../contracts/_MANIFEST.yaml`). Assert that both sub-questions are answered and that the combined severity verdict is consistent with the evidence.

This task is a **verification gate**: it does not simply prose-summarize; it verifies that both sub-findings are present, internally consistent, and that the combined verdict is defensible. If either sub-finding is missing, contradictory, or its severity assessment is inconsistent with the stated evidence, this task MUST flag the gap rather than silently plug it.

---

## Context

This task depends on:
- `SUBTASK_sec_event_downcast/finding_downcast.md` — severity verdict and evidence for the downcast reachability question
- `SUBTASK_sec_event_forget/finding_forget.md` — severity verdict and evidence for the closure.forget() scope question

See `../_GLOBAL.md` for full scope and constraints.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `../_GLOBAL.md` | Scope, constraints, and output schema |
| Downcast sub-finding | `../SUBTASK_sec_event_downcast/finding_downcast.md` | Downcast reachability verdict |
| Forget sub-finding | `../SUBTASK_sec_event_forget/finding_forget.md` | closure.forget() scope verdict |
| Parent contract schema | `../../contracts/_MANIFEST.yaml` | Required finding.md structure |

---

## Verification Gate: Four Checks

1. **Coverage check**: Both sub-questions from the parent `_BRIEF.md` are answered (downcast reachability + closure.forget() scope). If either is missing, inject a remediation task; do not proceed.
2. **Severity consistency**: The combined `severity` in `finding.md` is the MAXIMUM severity across the two sub-findings. If sub-finding A is `blocker` and sub-finding B is `clean`, the combined verdict is `blocker`. If both are `clean`, the combined verdict is `clean`. Record reasoning.
3. **Schema compliance**: `finding.md` conforms to the schema in `../../_GLOBAL.md` §Contract (required fields: `severity`, `concern`, `location`, `description`; `## What was examined` section present).
4. **Evidence quality**: Each verdict in the combined finding cites specific file/line evidence. A verdict unsupported by specific evidence from the diff is flagged as insufficient.

---

## Output Specification

**Primary Output:** `finding.md` at the SUBTASK_sec_event workspace root (`../finding.md`)

The file MUST follow the schema in `../../_GLOBAL.md` §Contract:

```markdown
## Finding

- **severity**: blocker | non-blocker | clean
- **concern**: Event handler security surface / closure.forget() scope
- **location**: crates/ferric/src/file.rs:LINE (or N/A)
- **description**: [combined description covering both the downcast mechanism and closure scope, with specific evidence]

## What was examined
[Files read, diff sections reviewed, and which sub-questions above were answered]
```

---

## Suggested Methodology Files

Task type row (Domain Mapping): **Synthesizing / verifying a hub-and-spoke decomposition** → Primary: `synthesis`, Supporting: `code-review`

- `synthesis/Synthesis_Overview_Methodology.md` — the four-check gate model; combined severity computation
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify that sub-findings conform to the declared schema

These are SUGGESTIONS. The agent is the final judge of what its work requires.

## Inherited Constraints

- `finding.md` MUST be written at the SUBTASK_sec_event workspace root (i.e., `../finding.md` relative to this task's workspace)
- Repository-relative paths only
- Severity `blocker` only for a concrete security vulnerability

## Success Criteria

- [ ] Both sub-findings read and coverage verified
- [ ] Combined severity computed (maximum of sub-finding severities)
- [ ] `finding.md` produced at `../finding.md` conforming to the parent contract schema
- [ ] `## What was examined` section present and complete
- [ ] No sub-question silently dropped or unanswered
