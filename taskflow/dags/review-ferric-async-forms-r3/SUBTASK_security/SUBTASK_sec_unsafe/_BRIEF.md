# Task: Unsafe Code Audit

## Task Specification

**Slug**: SUBTASK_sec_unsafe
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Identify any new `unsafe` blocks introduced by the three remediation commits (9fedad9, 9557f0c, 838239e) and, if found, verify that each block's safety invariant is clearly stated and justified.

---

## Context

This task is part of the security review subtree for PR #193. See `../_GLOBAL.md` for full scope and constraints.

**Files changed by the remediation commits:**
- `crates/ferric/src/async_resource.rs` — B1 (create_resource reactive constructor)
- `crates/ferric/src/vdom.rs` — B2 (EventHandler enum)
- `crates/ferric/src/dom.rs` — B2 (event dispatch)
- `crates/ferric/src/form.rs` — B3 (on_input_event_handler + WASM test)

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Scope and constraints |
| PR diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Changed lines to scan for `unsafe` |

The diff is sufficient for this concern — if no `unsafe` appears in the diff, the answer is clean.

---

## Review Questions

1. Does the diff introduce any new `unsafe` blocks?
2. If yes: is each block's invariant (the reason it is memory-safe despite using `unsafe`) clearly stated and justified in a comment adjacent to the block?

---

## Output Specification

**Primary Output:** `finding.md` at this task's workspace root (`SUBTASK_sec_unsafe/finding.md`)

The finding file MUST follow the schema in `../_GLOBAL.md` §Contract:

```markdown
## Finding

- **severity**: blocker | non-blocker | clean
- **concern**: Unsafe code
- **location**: crates/ferric/src/file.rs:LINE (or N/A if no unsafe blocks found)
- **description**: [what was found or verified clean]

## What was examined
[Files, diff sections reviewed, and which sub-questions above were answered]
```

If no `unsafe` blocks are found in the diff, severity is `clean` and location is `N/A`.

---

## Suggested Methodology Files

Task type row (Domain Mapping): **Security review / Rust FFI unsafe code** → Primary: `security`, Supporting: `rust`

- `security/Security_Secure_Coding_Methodology.md` — the memory safety and unsafe code evaluation section applies
- `rust/Rust_Unsafe_FFI_Methodology.md` — Rust unsafe block safety invariant conventions; what a well-documented `unsafe` block looks like, what invariants must be stated

These are SUGGESTIONS. The agent is the final judge. If no `unsafe` appears in the diff, the methodology files may not be needed.

## Inherited Constraints

- Repository-relative paths only in all findings
- Focused pass on the three remediation commits only
- Severity `blocker` only for concrete security vulnerability (undocumented or unjustifiable `unsafe` block) introduced by this PR

## Success Criteria

- [ ] Review questions answered with evidence from the diff
- [ ] `finding.md` produced with `severity` assigned
- [ ] If `unsafe` blocks are found: each one evaluated for stated invariant
