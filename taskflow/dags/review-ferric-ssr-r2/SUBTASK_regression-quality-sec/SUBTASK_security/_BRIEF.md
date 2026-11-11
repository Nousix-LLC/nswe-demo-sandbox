# Task: Security Review — New Code

## Task Specification

**Slug**: SUBTASK_security
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Check whether the ferric-ssr-r4 commits (`7fb90c7`, `e625c3f`, `75c1eef`) introduce any
HTML injection paths, escaping gaps, or other security issues not present before. Also check
whether the new test code (`hydrate_wasm.rs`) exposes anything security-sensitive.

### Context

This task is part of the SUBTASK_regression-quality-sec spoke of review-ferric-ssr-r2 (see
`../_GLOBAL.md`). It runs in parallel with SUBTASK_regression-check and SUBTASK_code-quality.

The ferric-ssr-r4 commits add:
- A cfg-gate and conditional `hydrate()` dispatch in `app.rs`
- A `hydrate_wasm.rs` test file using `wasm-bindgen-test`

This task does NOT cover code quality (style, structure) — that is SUBTASK_code-quality.
This task does NOT re-check acceptance criteria — that is SUBTASK_regression-check.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Project constraints and context |
| PR #228 diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | See all security-relevant changes |
| `app.rs` | `crates/chirp-frontend/src/app.rs` on branch | New entry-point code |
| `hydrate_wasm.rs` | `crates/ferric/tests/hydrate_wasm.rs` on branch | New test file |
| `ssr.rs` | `crates/ferric/src/ssr.rs` on branch | HTML rendering / escaping path |
| `hydrate.rs` | `crates/ferric/src/hydrate.rs` on branch | DOM manipulation path |

**Note on reading files**: Use `gh` API or SSH per CLAUDE.md. The ferric library performs
server-side HTML rendering in `ssr.rs` — that is the primary escaping concern.

---

## Process Guidance

### HTML injection and escaping gaps

1. **New rendering paths in ssr.rs**: Does any new commit add or modify a path that writes
   HTML? If so, does it escape user-controlled or dynamic content appropriately?
2. **assemble_document path**: Does the new code touch or extend `assemble_document`? If so,
   does the new code introduce any injection path?
3. **hydrate path**: The hydration path sets DOM node content. Does any new code inject
   unescaped strings into DOM positions where scripts could execute?
4. **Attribute values**: Are attribute values set via `setAttribute` or similar in new code
   without escaping?

### Test file security

5. **Logged or exposed data**: Does `hydrate_wasm.rs` log or expose anything that in a CI
   context could leak configuration, tokens, or sensitive structural information?
6. **Hardcoded secrets or tokens**: Any API keys, secrets, or tokens in the test setup?
7. **DOM manipulation test helpers**: Does the test infrastructure write unescaped HTML strings
   to the DOM in ways that set a bad precedent?

### Prior escaping coverage

The prior review did not flag escaping issues in `ssr.rs`. The question here is specifically
whether the NEW commits introduce gaps that were not present before — not a full re-audit of
the existing escaping implementation.

---

## Output Specification

**File**: `security.md`
**Location**: `SUBTASK_security/`

The file must contain:

```markdown
# Security Review — New Code

## HTML Injection and Escaping

### New rendering paths
[Finding or "No new rendering paths introduced"]

### assemble_document
[Finding or "Not touched by new commits"]

### Hydration DOM writes
[Finding or "No new unescaped writes in new code"]

### Attribute values
[Finding or "No new attribute-setting code introduced"]

## Test File Security

### Logged or exposed data
[Finding or "No sensitive data logged in test file"]

### Hardcoded secrets or tokens
[Finding or "None found"]

### DOM manipulation in tests
[Finding or "No concerning DOM manipulation patterns"]

## Overall Security Verdict: [PASS | FAIL]

[If FAIL: state the specific issue and why it is a blocker]
[If PASS: brief statement of what was checked and found clean]
```

---

## Success Criteria

- [ ] HTML injection paths examined for new commits
- [ ] assemble_document checked if touched
- [ ] Hydration DOM writes reviewed for new code
- [ ] Test file checked for security concerns
- [ ] Overall PASS or FAIL verdict stated
- [ ] `security.md` written to this task's workspace

---

## Suggested Methodology Files

**Task type**: "Security review" → Primary: `security`, Supporting: `code-review`

Specifically:
- `security/Security_Secure_Coding_Methodology.md` — HTML injection, escaping, XSS vectors
  (most directly relevant — covers output encoding, context-sensitive escaping)
- `code-review/CodeReview_Process_Methodology.md` — systematic concern coverage
- `code-review/CodeReview_Checklist_Methodology.md` — security checklist items

These are suggested starting points. The child agent retains final judgment.

## Inherited Constraints

- **Repository**: Nousix-LLC/nswe-demo, branch `work/ferric-ssr-r1`, PR #228
- **Commits under inspection**: `7fb90c7`, `e625c3f`, `75c1eef`
- **Do not re-raise**: Issues #229–#242
- **Do not reference**: Overseer I267 escalation comments
- **Prose bar**: No AI-tell patterns in output text
- **Scope**: Security only — code quality is SUBTASK_code-quality; regression check is
  SUBTASK_regression-check
- **Focus**: Whether NEW commits introduce issues not present before; not a full re-audit
