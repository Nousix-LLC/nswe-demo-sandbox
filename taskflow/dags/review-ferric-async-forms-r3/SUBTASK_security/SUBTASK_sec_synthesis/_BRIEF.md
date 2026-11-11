# Task: Security Review Synthesis — Compile Findings (Verification Gate)

## Task Specification

**Slug**: SUBTASK_sec_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_sec_injection, SUBTASK_sec_secrets, SUBTASK_sec_unsafe, SUBTASK_sec_event
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Act as the verification gate for the security review subtree: read all four spoke findings, verify the contract identities hold (all concern areas covered, blockers have locations and descriptions), and compile the final `findings.md` at the SUBTASK_security workspace root.

---

## Context

This task is part of the security review subtree for PR #193. See `../_GLOBAL.md` for full scope, constraints, output format, and contract.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Scope, constraints, output format, contract identities |
| Injection finding | `../SUBTASK_sec_injection/finding.md` | HTML injection / escaping result |
| Secrets finding | `../SUBTASK_sec_secrets/finding.md` | Secrets and infra data result |
| Unsafe finding | `../SUBTASK_sec_unsafe/finding.md` | Unsafe code result |
| Event surface finding | `../SUBTASK_sec_event/finding.md` | Event handler / closure result |

---

## Process

This is a **verification gate**, not a prose summary. The gate MUST:

1. Read all four spoke `finding.md` files
2. Verify the three contract identities from `../_GLOBAL.md` §Identities:
   - Every concern area (injection, secrets, unsafe, event surface) has a verdict
   - All 4 spoke findings are represented
   - Any blocker includes a repository-relative location and actionable description
3. If any identity assertion fails (e.g., a spoke file is missing or incomplete), flag it in `findings.md` as a synthesis-gate failure before proceeding
4. Compile the final `findings.md` at `../findings.md` following the format specified in the parent task's `_BRIEF.md`

The synthesis must not add new security analysis. Its role is integration and verification.

---

## Output Specification

**Primary Output:** `findings.md` at the SUBTASK_security workspace root (path: `../findings.md` relative to this task's directory)

The file MUST follow the format from the parent security task's `_BRIEF.md`:

```markdown
## Findings

[For each finding or clean verification, an entry with:
- severity: blocker | non-blocker | clean
- concern: security
- location: crates/ferric/src/file.rs:LINE (where applicable)
- description: what was found or verified clean]

## What was examined

[Enumeration of files, diff sections, and security questions examined]
```

Each of the four concern areas must have at least one entry.

---

## Suggested Methodology Files

Task type row (Domain Mapping): **Synthesizing / verifying a hub-and-spoke decomposition** → Primary: `synthesis`, Supporting: `code-review`

- `synthesis/Synthesis_Overview_Methodology.md` — gate methodology anchor; what a verification gate does and the four-check model (ALWAYS load first)
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify the three identities from `../_GLOBAL.md` §Identities hold
- `synthesis/Synthesis_Code_Review_Methodology.md` — final code review pass over the combined output

These are SUGGESTIONS. The agent is the final judge. The gate posture (this task runs checks and either passes or raises failures) is not a suggestion — it is prescribed.

## Inherited Constraints

- Repository-relative paths only in all findings (no internal hosts, SSH keys, infra paths)
- Focused pass on the three remediation commits only
- Severity `blocker` only for concrete security vulnerability introduced by this PR

## Out-of-Scope Methodologies

- `decomposition/` bundle — this is a synthesis task, not a decomposing task; do not load decomposition-shape guidance
- `synthesis/Synthesis_Remediation_Methodology.md` — only needed if a gate violation requires scheduling fix-tasks; load on demand if a spoke is missing or malformed

## Success Criteria

- [ ] All 4 spoke `finding.md` files read
- [ ] All 3 contract identities from `../_GLOBAL.md` §Identities verified (or flagged as failing)
- [ ] `findings.md` produced at `../findings.md` covering all four concern areas with explicit verdicts
- [ ] Format matches the parent task's `_BRIEF.md` output specification
