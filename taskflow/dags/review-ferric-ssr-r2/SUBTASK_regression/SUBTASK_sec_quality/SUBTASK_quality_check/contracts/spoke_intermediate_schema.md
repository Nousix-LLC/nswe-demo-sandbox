# Spoke Intermediate Output Schema

Each analysis spoke in the SUBTASK_quality_check sub-decomposition MUST produce a file
conforming to its assigned section(s) of this schema so SUBTASK_synthesis can assemble them
into quality_raw_findings.md.

---

## SUBTASK_app_quality → app_quality_raw.md

Must carry exactly these sections in this order:

```markdown
## App.rs Code Quality Findings

- **Severity**: Blocker | Non-blocker | Note
- **Location**: file:line (at pinned commit 75c1eef)
- **Description**: what the issue is
- **Resolution**: what would satisfy this

(or "No app.rs code quality findings.")

## App.rs Fresh Non-blockers

(New instances of patterns from #229-#242 found in genuinely new app.rs code introduced by
commits 7fb90c7, e625c3f, 75c1eef. Or: "No fresh non-blockers found in app.rs new code.")

## App.rs What Was Examined and Found Clean

- <concern> → clean
...
```

Required concerns covered:
- New conditional hydrate/mount dispatch in app.rs (readability, edge cases, dead code, documentation accuracy)
- Fresh instances of #229-#242 patterns in new app.rs code

---

## SUBTASK_test_quality → test_quality_raw.md

Must carry exactly these sections in this order:

```markdown
## hydrate_wasm.rs Code Quality Findings

- **Severity**: Blocker | Non-blocker | Note
- **Location**: file:line (at pinned commit 75c1eef)
- **Description**: what the issue is
- **Resolution**: what would satisfy this

(or "No hydrate_wasm.rs code quality findings.")

## hydrate_wasm.rs Fresh Non-blockers

(New instances of patterns from #229-#242 found in genuinely new hydrate_wasm.rs code introduced
by commits 7fb90c7, e625c3f, 75c1eef. Or: "No fresh non-blockers found in hydrate_wasm.rs new code.")

## hydrate_wasm.rs What Was Examined and Found Clean

- <concern> → clean
...
```

Required concerns covered:
- New test helpers quality (naming, clarity, non-redundancy)
- Assertion specificity (do they check behavior or just that code ran?)
- Copy-paste patterns suggesting missed abstraction
- Fresh instances of #229-#242 patterns in new hydrate_wasm.rs code

---

## Synthesis assembly rule

SUBTASK_synthesis combines both spoke files into quality_raw_findings.md following the parent
contract at `../contracts/spoke_output_schema.md`. The assembly is mechanical:

1. Write `## Code Quality Findings` by merging both spokes' findings sections
2. Write `## What Was Examined and Found Clean` by merging both spokes' clean sections
3. Verify: every concern from SUBTASK_quality_check _BRIEF.md appears in one section
