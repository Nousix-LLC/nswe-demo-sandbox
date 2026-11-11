# Task: HTML Injection / Escaping Gap Analysis

## Task Specification

**Slug**: SUBTASK_sec_injection
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Determine whether any new code path introduced by the three remediation commits (9fedad9, 9557f0c, 838239e) writes user-supplied input from `HtmlInputElement::value()` or an event payload to the DOM without passing through the library's established escaping mechanism.

---

## Context

This task is part of the security review subtree for PR #193. See `../_GLOBAL.md` for full scope and constraints.

**Files changed by the remediation commits relevant to this concern:**
- `crates/ferric/src/form.rs` — B3 adds `on_input_event_handler` which reads `HtmlInputElement::value()`
- `crates/ferric/src/vdom.rs` — B2 adds EventHandler enum; this is the rendering path
- `crates/ferric/src/dom.rs` — B2 event dispatch

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Scope and constraints |
| PR diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Changed lines |
| form.rs | `crates/ferric/src/form.rs` | on_input_event_handler source — where input is read |
| vdom.rs | `crates/ferric/src/vdom.rs` | DOM rendering path — where signal values are inserted |
| dom.rs | `crates/ferric/src/dom.rs` | Event dispatch |

---

## Review Questions

1. Does `on_input_event_handler` write the raw `String` from `HtmlInputElement::value()` into a signal — and if so, does the library's existing rendering path escape signal values before inserting them into the DOM?
2. Does any new code path in the diff write user-supplied input (from an event payload or input element) to the DOM without going through the library's established escaping mechanism?

This is about whether a **new** escaping gap was introduced by these commits, not a comprehensive audit of the library's existing escaping.

---

## Output Specification

**Primary Output:** `finding.md` at this task's workspace root (`SUBTASK_sec_injection/finding.md`)

The finding file MUST follow the schema in `../_GLOBAL.md` §Contract:

```markdown
## Finding

- **severity**: blocker | non-blocker | clean
- **concern**: HTML injection / escaping
- **location**: crates/ferric/src/file.rs:LINE (or N/A if no specific line)
- **description**: [what was found or verified clean — be specific]

## What was examined
[Files read, diff sections reviewed, and which sub-questions above were answered]
```

---

## Suggested Methodology Files

Task type row (Domain Mapping): **Security review** → Primary: `security`, Supporting: `code-review`

- `security/Security_Secure_Coding_Methodology.md` — input validation, output encoding, injection vulnerability patterns; use the input validation and XSS/injection sections to frame the data-flow trace
- `code-review/CodeReview_Checklist_Methodology.md` — security section of the checklist; confirms what a reviewer looks for in event-handling and DOM-write paths

These are SUGGESTIONS. The agent is the final judge of what its work requires — load fewer if inapplicable.

## Inherited Constraints

- Repository-relative paths only in all findings (no internal hosts, SSH keys, or infra paths)
- Focused pass on the three remediation commits only; prior library code is background context, not the subject
- Severity `blocker` only if a concrete new injection vulnerability was introduced by this PR

## Success Criteria

- [ ] Both review questions answered with evidence from the diff and the relevant source files
- [ ] `finding.md` produced with `severity` assigned
- [ ] Location provided if a specific line is flagged
