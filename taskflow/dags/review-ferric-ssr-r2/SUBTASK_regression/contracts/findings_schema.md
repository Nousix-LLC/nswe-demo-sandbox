# Findings Schema

Each spoke findings file (criteria_findings.md, sec_quality_findings.md) MUST carry
these sections in this order. The synthesis task reads these sections by heading.

## Criteria Results

(SUBTASK_reg_criteria only)

For each criterion, one entry:

```
### REQ-<ID>: <short name>
**Verdict**: PASS | FAIL
**Evidence**: <file, line, what was checked>
**Finding** (if FAIL): <description>
```

## Security Findings

(SUBTASK_sec_quality only)

For each security concern checked:

```
### <Concern name>
**Result**: Clean | Finding
**Evidence**: <file, line, what was checked>
**Finding** (if applicable): <severity, description, resolution>
```

## Code Quality Findings

(SUBTASK_sec_quality only)

Enumerated findings. For each:

```
- **Severity**: Blocker | Non-blocker | Note
- **Location**: file:line
- **Description**: what the issue is
- **Resolution**: what would satisfy this
```

If none: "No code quality findings."

## What Was Examined and Found Clean

For each concern examined that produced no finding:

```
- <concern> → clean
```
