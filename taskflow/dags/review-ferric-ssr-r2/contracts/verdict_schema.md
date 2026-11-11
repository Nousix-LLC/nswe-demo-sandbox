# Verdict Schema

Each spoke verdict file MUST carry these sections in this order.

## Verdict

One of:
- `RESOLVED` — the blocker or criterion is satisfied, with evidence
- `NOT_RESOLVED` — the blocker or criterion is not satisfied; this becomes a REQUEST-CHANGES blocker
- `PASS` — the criterion is satisfied (used for regression / secondary criteria)
- `FAIL` — the criterion is not satisfied; specify whether it is a blocker or non-blocker

## Requirements Covered

Comma-separated list of requirement IDs examined (e.g. REQ-HYD-003, REQ-SSR-006).

## Evidence

What was read (file paths, commit SHAs, line numbers) and what was found. Specific, citable.

## Findings

Enumerated findings. For each:
- **Severity**: Blocker | Non-blocker | Note
- **Requirement**: which REQ-ID this relates to
- **Location**: file path + line number at the pinned commit
- **Principle**: what rule or bar is at stake
- **Why it matters**: consequence in this system
- **Resolution**: what would satisfy this finding

If no findings: state "No findings" explicitly.

## What Was Examined and Found Clean

For each concern examined that produced no finding, state it explicitly:
- Concern → outcome (clean / no issue found)

This prevents "no findings" from being read as "nothing was checked."
