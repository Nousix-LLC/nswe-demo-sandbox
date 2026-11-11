# Spoke Output Schema

Each spoke in the SUBTASK_sec_quality sub-decomposition MUST produce a file
conforming to its assigned section(s) of this schema so SUBTASK_synthesis can
assemble them mechanically.

---

## SUBTASK_sec_check → security_raw_findings.md

Must carry exactly this section in this order:

```markdown
## Security Findings

### <Concern name>
**Result**: Clean | Finding
**Evidence**: <file, line, what was checked>
**Finding** (if applicable): <severity, description, resolution>

### <Concern name>
...
```

Required concerns (one subsection each):
- HTML Injection in ssr.rs
- DOM Spoofing in app.rs
- Test Injection Safety in hydrate_wasm.rs

---

## SUBTASK_quality_check → quality_raw_findings.md

Must carry these sections in this order:

```markdown
## Code Quality Findings

- **Severity**: Blocker | Non-blocker | Note
- **Location**: file:line
- **Description**: what the issue is
- **Resolution**: what would satisfy this

(or "No code quality findings.")

## What Was Examined and Found Clean

- <concern> → clean
...
```

Required concerns covered:
- app.rs new conditional hydrate/mount dispatch (readability, edge cases, dead code)
- hydrate_wasm.rs new test code (helper quality, assertion clarity, copy-paste patterns)
- Fresh non-blockers from new code (patterns from #229–#242 reappearing)

---

## Synthesis assembly rule

SUBTASK_synthesis combines both spoke files into sec_quality_findings.md following
the full `../contracts/findings_schema.md`. The assembly is mechanical:

1. Write a `## Security Findings` section by copying SUBTASK_sec_check/security_raw_findings.md's Security Findings section verbatim
2. Write a `## Code Quality Findings` section by copying SUBTASK_quality_check/quality_raw_findings.md's Code Quality Findings section verbatim
3. Write a `## What Was Examined and Found Clean` section that merges:
   - Security concerns found clean from security_raw_findings.md
   - Quality concerns found clean from quality_raw_findings.md
4. Verify: every concern listed in the SUBTASK_sec_quality _BRIEF.md appears in one of the first three sections
