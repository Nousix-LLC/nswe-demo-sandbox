# Findings Format Contract

**Purpose**: Declares the structure every concern spoke MUST use in its `partial_findings.md`.
The synthesis task asserts this schema before combining spoke outputs.

---

## Required Sections

Each `partial_findings.md` MUST contain both sections below.

---

### Section: `## Findings`

One entry per finding or clean verification. Each entry MUST follow this structure:

```
- **severity**: <blocker | non-blocker | clean>
  **concern**: <code-quality | tests | idiom | api-stability>
  **location**: <crates/ferric/src/<file>.rs:<LINE> | "structural" for design/process findings>
  **description**: <what was found — for clean, state what was checked and found sound;
                    for findings, state the issue, why it matters, and what would satisfy>
```

**Severity rules (binding):**
- `blocker`: use ONLY when a stated requirement is unmet or an existing public API contract is broken for callers. NOT for style or preference.
- `non-blocker`: for observations that should be addressed but do not block merge (style, naming, missing documentation, minor idiom deviations).
- `clean`: for sub-questions examined and found satisfactory — MUST include what was checked.

**Concern label (binding):**
- Each spoke uses only its own assigned concern label (see the spoke's _BRIEF.md for its label).

**Location format (binding):**
- Repository-relative paths only: `crates/ferric/src/async_resource.rs:42`
- No host paths, no taskflow paths
- Use `"structural"` when the finding is about overall design rather than a specific line

---

### Section: `## What was examined`

A list of files, specific line ranges or function names read, and sub-questions from the parent brief that were covered. This section exists so the synthesis task can confirm coverage without gaps.

Example:
```markdown
## What was examined

- `crates/ferric/src/async_resource.rs` lines 1–420 (full file)
  - Generation counter logic (~lines 80–130)
  - Native tests in `mod tests` (~lines 300–420)
- `crates/ferric/src/vdom.rs` lines 1–250
  - EventHandler enum definition
  - `impl VElement` on_event method
- Sub-questions addressed:
  - [x] Is the generation counter invariant followable without tracing multiple layers?
  - [x] Does the design invite correct use?
  - [ ] (not in scope for this spoke)
```

---

## Disallowed

- Duplicate entries for issues #196, #197, #198, #199, #200, #201 — these are already filed
- Paths that reveal host filesystem structure or taskflow workspace paths
- Severity `blocker` for style observations, naming preferences, or non-breaking design opinions
