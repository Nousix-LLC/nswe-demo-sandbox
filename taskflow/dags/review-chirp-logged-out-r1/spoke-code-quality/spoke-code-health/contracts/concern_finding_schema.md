# Concern Finding Schema

Each analysis child (`child-dead-code`, `child-hydrate-scope`) MUST produce a Markdown file
conforming to this schema. The synthesis child reads both files to assemble `FINDINGS.md`.

---

## Required Sections (in order)

### `## Concern N — [Label]`

A single top-level header identifying which concern this file covers. `N` is the concern number
(6 or 7) from the parent spoke concern assignment table.

---

### `## Investigation`

A short account (1–4 paragraphs) of what was read and what was found. Write as a reviewer
noting what they looked at:

- Which files were read
- What the routing structure or code structure showed
- What the data says about the question

No narrated candor ("I found", "it turns out"). Just the facts from the reading.

---

### `## Verdict`

One sentence or short paragraph declaring the finding:

- For concern 6: state whether `sign_up::sign_up_view` is reachable from any live route.
- For concern 7: state whether the EventKind expansion is causally required by the public
  timeline feature, and whether `static_event_kinds()` is manually synced or derived.

---

### `## Finding` (required when the verdict identifies an issue; omit when clean)

One entry per issue, following the parent schema format:

```markdown
### Finding: [Short title]

- **Location**: `crates/<path>/file.rs`, line NN at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle at stake**: [Name the principle]
- **Why it matters**: [Why in this codebase/system]
- **Severity**: blocker | non-blocking
- **Satisfying condition**: [Concrete and verifiable]
```

---

## Prose Bar

Same bar as the parent `findings_schema.md`:
- No moral or character adjectives on technical things
- No narrated candor
- No unnamed contrast pairs or slot-fill templates
- No inflated filler
