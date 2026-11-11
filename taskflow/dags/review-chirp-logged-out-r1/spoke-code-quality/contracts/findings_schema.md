# FINDINGS.md Schema

Every analysis spoke MUST produce a `FINDINGS.md` conforming to this schema.
The synthesis spoke reads all five FINDINGS.md files and assembles REVIEW.md.

---

## Required Sections (in order)

### `## Verdict`

One of exactly two values:

```
PASS
```

or

```
FINDINGS
```

`PASS` means every assigned sub-concern was checked and found clean.
`FINDINGS` means at least one finding was identified.

---

### `## Findings` (required when Verdict = FINDINGS; omit when Verdict = PASS)

One subsection per finding:

```markdown
### Finding N: [Short title — what is wrong, not how to fix it]

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

### `## Clean Account`

One bullet per assigned sub-concern, whether clean or found with issues.
Each entry states what was checked and what was found (clean or the finding reference).

```markdown
## Clean Account

- **Concern N — [brief label]**: Checked [what specifically]. [What was found sound, or reference to Finding M.]
```

No concern may be silently omitted. If a concern could not be checked (e.g., file is inaccessible),
state the gap explicitly rather than omitting the entry.

---

## Prose Bar

All text in FINDINGS.md must pass the plain-voice bar:

- No moral or character adjectives attached to technical things ("honest", "genuine", "real")
- No narrated candor ("stated plainly", "to be honest", "let's be clear")
- No unnamed contrast pairs ("real X, not the fake kind")
- No slot-fill templates ("a [adjective] step toward [noun]")
- No inflated filler (seamless, robust, comprehensive, leverage, Moreover, Furthermore)

Write findings as a reviewer, not as a commenter narrating their own candor.
