# Task: hydrate_wasm.rs — Synthesis: Assemble hydrate-wasm-notes.md

## Task Specification

**Slug**: SUBTASK_dim-synthesis
**Task Kind**: standard
**Depends on**: SUBTASK_dim-naming, SUBTASK_dim-cleanup, SUBTASK_dim-strings, SUBTASK_dim-duplication, SUBTASK_dim-assertions
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Combine the five dimension finding files into a single `hydrate-wasm-notes.md` following
the format required by the parent contract (`../../contracts/_MANIFEST.yaml`). The output
is owned by SUBTASK_hydrate-wasm-quality and consumed by SUBTASK_quality-synthesis.

### Context

This task is the synthesis spoke within SUBTASK_hydrate-wasm-quality (see `../_GLOBAL.md`).
Its five dependency tasks each produced one finding fragment in their respective
`finding.md` files. This task reads those five files and assembles the final output file
at the SUBTASK_hydrate-wasm-quality workspace root.

This is an assembly task. It does NOT re-review the source code or produce new findings.
If a dependency's `finding.md` appears incomplete or inconsistent with the format, note
the gap in the assembly log but do not invent findings — flag it for the parent synthesis
task (SUBTASK_quality-synthesis) to resolve.

---

## Input Specification

| Input | Source | Purpose |
|---|---|---|
| Naming finding | `../SUBTASK_dim-naming/finding.md` | Dimension 1 finding fragment |
| Cleanup finding | `../SUBTASK_dim-cleanup/finding.md` | Dimension 2 finding fragment |
| Strings finding | `../SUBTASK_dim-strings/finding.md` | Dimension 3 finding fragment |
| Duplication finding | `../SUBTASK_dim-duplication/finding.md` | Dimension 4 finding fragment |
| Assertions finding | `../SUBTASK_dim-assertions/finding.md` | Dimension 5 finding fragment |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Required format and ownership |
| Parent contract | `../../contracts/_MANIFEST.yaml` | Finding-note format identity |
| Subtree hub | `../_GLOBAL.md` | Inherited constraints |

---

## Assembly Rules

1. **Order**: Assemble dimensions in this sequence:
   1. Test structure and naming
   2. Setup/teardown and DOM cleanup
   3. Hardcoded strings vs. imported constants
   4. Duplication
   5. Assertion quality

2. **Format**: Each section heading, severity line, evidence line, and finding text
   must be present and follow the format in `../../contracts/_MANIFEST.yaml`.

3. **Fresh Non-Blockers**: If any dimension finding includes a "Fresh Non-Blockers"
   section, include a combined "## Fresh Non-Blockers" section at the end. If none
   do, write "None found."

4. **No new findings**: Do not add findings that do not appear in the five input files.
   Do not modify the substance of any finding.

5. **Prose bar**: The assembled document must be free of AI-tell patterns (no moral
   adjectives on metrics, no narrated candor, no slot-fill templates, no filler).

---

## Output Specification

**File**: `hydrate-wasm-notes.md`
**Location**: `../` (the SUBTASK_hydrate-wasm-quality workspace root — one level up from
this task's directory)

Required structure:

```markdown
# hydrate_wasm.rs Quality Notes

## Test structure and naming

**Severity**: [Blocker | Warning | Pass]
**Evidence**: [hydrate_wasm.rs:line or N/A]

[Finding text]

## Setup/teardown and DOM cleanup

**Severity**: [Blocker | Warning | Pass]
**Evidence**: [hydrate_wasm.rs:line or N/A]

[Finding text]

## Hardcoded strings vs. imported constants

**Severity**: [Blocker | Warning | Pass]
**Evidence**: [hydrate_wasm.rs:line or N/A]

[Finding text]

## Duplication

**Severity**: [Blocker | Warning | Pass]
**Evidence**: [hydrate_wasm.rs:line or N/A]

[Finding text]

## Assertion quality

**Severity**: [Blocker | Warning | Pass]
**Evidence**: [hydrate_wasm.rs:line or N/A]

[Finding text]

## Fresh Non-Blockers (if any)

[List with file:line, or "None found"]
```

---

## Success Criteria

- [ ] All five dimension sections present in the declared order
- [ ] Each section has severity, evidence, and finding text
- [ ] `hydrate-wasm-notes.md` written to `../` (workspace root, not this task's directory)
- [ ] File path and format satisfy `../../contracts/_MANIFEST.yaml`
- [ ] "Fresh Non-Blockers" section present (populated or "None found")
- [ ] No AI-tell patterns in any assembled prose

---

## Inherited Constraints

- **Repository**: Nousix-LLC/nswe-demo, commit `75c1eef776953993ddd62dba1436845a0d53a281`
- **Do not re-raise**: Issues #229–#242
- **Do not reference**: Overseer I267 escalation comments
- **Prose bar**: No AI-tell patterns in output text
- **Scope**: Assembly only — do not introduce new findings or re-review source code
