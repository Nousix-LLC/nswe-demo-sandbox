# Analysis Schema

Each analysis spoke MUST produce `analysis.md` conforming to this schema.
The synthesis spoke reads all three to assemble `../FINDINGS.md`.

---

## Required Sections (in order)

### `## Verdict`

One of exactly two values:

```
CLEAN
```

or

```
FINDING(S)
```

`CLEAN` means the assigned concern was checked and found sound.
`FINDING(S)` means at least one finding was identified.

---

### `## Findings` (required when Verdict = FINDING(S); omit when Verdict = CLEAN)

One subsection per finding:

```markdown
### Finding [letter]: [Short title — what is wrong, not how to fix it]

- **Concern**: [1 | 2 | 5]
- **Location**: `crates/<path>/file.rs`, line NN at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle at stake**: [Name the specific principle or property at stake]
- **Why it matters**: [Why this specific issue matters in this codebase/system]
- **Severity**: blocker | non-blocking
- **Satisfying condition**: [What must be true for this finding to be resolved — concrete and verifiable]
```

Rules:
- Location MUST reference a file path and line number at the pinned commit, not a vague description
- Severity `blocker` = the concern would stop the reviewer from approving; `non-blocking` = the
  concern should be addressed but does not block merge
- Satisfying condition MUST be concrete enough that the author can verify it without asking the reviewer
- Do not add internal host paths, private IPs, server paths, or SSH config to any finding

---

### `## Evidence`

A brief summary of what was read and what was verified: which tests were examined, which code paths
were traced, what assertions were inspected.

---

## Prose Bar

Same as `../contracts/findings_schema.md`:
- No moral or character adjectives attached to technical things
- No narrated candor
- No unnamed contrast pairs
- No slot-fill templates
- No inflated filler
