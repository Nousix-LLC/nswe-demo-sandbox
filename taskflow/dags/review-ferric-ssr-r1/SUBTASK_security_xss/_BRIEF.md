# SUBTASK_security_xss — PR #228 HTML Escaping / XSS Security Review

## Task Specification

**Slug**: SUBTASK_security_xss
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Examine PR #228 (`work/ferric-ssr-r1`, repo `Nousix-LLC/nswe-demo`) specifically for HTML injection
and XSS risk in the `render_to_string` output path. Determine whether dynamic/user-supplied content
is correctly escaped before being written into the HTML string, and whether any path exists for
unescaped content to reach the HTML output. This is a read-only review; do not modify source code.

---

## Context

See `_GLOBAL.md` (parent workspace) for PR coordinates and cross-cutting constraints.

**Depends on**: none (independent spoke — runs in parallel with other spokes)
**Dependents**: SUBTASK_synthesis reads this output

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Shared context | `../_GLOBAL.md` | PR coordinates, non-goal boundary |
| PR diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | The change under review |
| Branch source | `Nousix-LLC/nswe-demo` branch `work/ferric-ssr-r1` | Full SSR renderer source |

---

## Review Scope

This review is EXCLUSIVELY about HTML escaping and XSS risk in the SSR output path. It does not
cover correctness, code quality, or infrastructure exposure (those are other spokes).

### A. Text node escaping

- Does `render_to_string` correctly escape the following characters in text node content:
  `<`, `>`, `&`, `"`, `'`?
- Is there any code path where component text output (props, signal values, slot content) is
  inserted into the HTML string without passing through an escape function?
- Is the escaping applied to ALL text inserted as content (not just some paths)?

### B. Attribute value escaping

- Are attribute values written by the SSR renderer properly escaped?
- In particular: does the `data-hydration-id` attribute and any other dynamically-constructed
  attribute get its value escaped before insertion into the HTML string?
- Is there any attribute that could contain user-supplied data without escaping?

### C. Raw HTML insertions

- Does the renderer use any form of raw HTML insertion (e.g., `innerHTML`-equivalent, format string
  that interpolates HTML tags, `format!("<tag>{value}</tag>")` without escaping `value`)?
- If so, is the raw insertion intentional and documented as requiring pre-escaped input?

### D. Format string trust boundaries

- Examine every `format!()`, `write!()`, `push_str()`, and similar string-building call in the
  SSR code path. For each one that interpolates a runtime value into an HTML context, verify that
  the value has been through an escape function before interpolation.
- Are there any `format!()` calls that build HTML tags or attributes directly with user-supplied or
  component-supplied values without escaping?

### E. Test coverage for escaping

- Are there tests that specifically verify that injection characters (`<`, `>`, `&`, `"`, `'`) in
  component props or slot content are escaped in the SSR output?
- Do any tests inject a payload like `<script>` into a prop and verify it appears escaped
  (`&lt;script&gt;`) in the output?

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| File | `security_xss_findings.md` |
| Location | this workspace (`SUBTASK_security_xss/`) |

### Output Structure

```markdown
# PR #228 HTML Escaping / XSS Security Findings

## Summary
<one-paragraph verdict: is the escaping posture correct? Is there any XSS risk?>

## Findings by Area

### A. Text node escaping
**Status**: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
**What was checked**: ...
**Evidence** (file and line in repository): ...
**Finding** (if any): ...

### B. Attribute value escaping
...

### C. Raw HTML insertions
...

### D. Format string trust boundaries
...

### E. Test coverage for escaping
...

## Verdict
PASS (escaping is correct) | FAIL (blocker XSS risk found) | PARTIAL (non-blocker gaps)
```

---

## Success Criteria

- Every escaping area above has an evidence-backed finding or clean verdict
- Any unescaped path is identified with the specific file and line in the repository
- Output file exists at the declared path before this task reports completed

---

## Suggested Methodology Files

**Task-type row matched**: "Security review" → Primary: `Security`; Supporting: `Code Review`

Specific files:
- `security/Security_Secure_Coding_Methodology.md` — covers output encoding, injection prevention, trust boundaries; directly applicable to HTML escaping review
- `code-review/CodeReview_Checklist_Methodology.md` — includes security items on the checklist; run the security section against the diff

Additionally relevant:
- `rust/Rust_WebAssembly_Browser_Methodology.md` — WASM/browser conventions; context for understanding which code paths run server-side vs client-side

These are the parent's flagged methodologies. Load fewer if some are clearly inapplicable; load more if the brief reveals additional surface.

## Inherited Constraints

- **Scope**: This task covers ONLY HTML escaping / XSS. Infrastructure exposure is SUBTASK_security_infra.
- **Read-only**: Do not modify source code
- **Line citations**: All findings cite files and line numbers in `Nousix-LLC/nswe-demo`, not host paths
- **Non-blockers**: Flag them; SUBTASK_synthesis will decide blocking/non-blocking classification
- An unescaped user-supplied value in HTML output IS a blocker — it is an XSS vulnerability
