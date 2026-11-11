# Task: Security Review — PR #193 Ferric Async

## Task Specification

**Slug**: SUBTASK_security  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  
**Assigned To**: swe-reviewer

### Objective

Perform the security review pass (concern 5) for PR #193 (`work/ferric-async-forms-r2`, head `838239e`). Verify no new HTML injection or escaping gap, no host path, internal address, or infrastructure detail committed into the repository, and no other security-relevant issue introduced by the three remediation commits.

---

## Context

See `../_GLOBAL.md` for full project context, acceptance criteria, and key reference data.

**Files changed by the three remediation commits:**
- `crates/ferric/src/async_resource.rs` — B1 (create_resource)
- `crates/ferric/src/vdom.rs` — B2 (EventHandler enum)
- `crates/ferric/src/dom.rs` — B2 (event dispatch)
- `crates/ferric/src/form.rs` — B3 (on_input_event_handler + WASM test)

Fetch the PR diff using `gh pr diff 193 --repo Nousix-LLC/nswe-demo`, then read individual source files for any flagged areas.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Scope and constraints |
| PR #193 diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Actual changed lines |
| Changed source files | `crates/ferric/src/{async_resource,vdom,dom,form}.rs` | Direct inspection where needed |

---

## Review Scope

**HTML injection / escaping:**
- The PR adds event handling and form binding. Does any new code path write user-supplied input (from `HtmlInputElement::value()` or an event payload) to the DOM without going through the library's established escaping mechanism?
- Does `on_input_event_handler` write the raw `String` from `HtmlInputElement::value()` into a signal — and if so, does the library's existing rendering path escape signal values before inserting them into the DOM? (This is about whether a NEW escaping gap was introduced, not a comprehensive audit of the library's existing escaping.)

**Secrets and infrastructure data:**
- Does the diff contain any hardcoded IP addresses, hostnames, credentials, auth tokens, SSH keys, or similar infrastructure details?
- Do the new test files contain any real server addresses, real credentials, or other sensitive data?

**Unsafe code:**
- Does the diff introduce any new `unsafe` blocks? If so, is the invariant clearly stated and justified?

**Other security-relevant concerns:**
- Does the new event-carrying handler path have any surface for a crafted event to cause unexpected behavior (e.g., panics on downcast that could be triggered remotely)?
- Is the `closure.forget()` pattern in the WASM test limited to test scope only (not leaking into production code paths)?

---

## Output Specification

**Primary Output:** `findings.md` at this task's workspace root (`SUBTASK_security/findings.md`)

The findings file MUST contain:

```markdown
## Findings

[For each finding or clean verification, an entry with:
- severity: blocker | non-blocker | clean
- concern: security
- location: crates/ferric/src/file.rs:LINE (where applicable)
- description: what was found or verified clean]

## What was examined

[Enumeration of files, diff sections, and security questions examined]
```

---

## Suggested Methodology Files

Task type row (Domain Mapping): **Ferric PR review (Rust library)** → Primary: `code-review`, Supporting: `rust`, `framework-design`

Specific files to load:
- `security/Security_Secure_Coding_Methodology.md` — secure coding checklist for the concerns above
- `code-review/CodeReview_Checklist_Methodology.md` — security section of the review checklist

These are SUGGESTIONS. Load fewer if some are clearly inapplicable.

## Inherited Constraints

- Repository-relative paths only in all findings
- This is a focused pass on the three remediation commits; a full library security audit is out of scope
- Severity calibration: a finding is a blocker only if it represents a concrete security vulnerability introduced by this PR

## Success Criteria

- All four security questions above answered with evidence from the diff and source files
- `findings.md` produced with severity assigned to each finding
- No unexamined security concern within scope
