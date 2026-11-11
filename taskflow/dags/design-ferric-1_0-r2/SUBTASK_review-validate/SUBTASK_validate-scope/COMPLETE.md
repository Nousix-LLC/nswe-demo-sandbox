# Task Complete: SUBTASK_validate-scope

## What was done

Read `design/ferric/scope-and-requirements.md` from branch `work/design-ferric-1_0` at
`/home/user/nswe-demo` and validated it against all five criteria in the brief.

## Output produced

`SUBTASK_validate-scope/concern-findings.md`

## Validation summary

**Status: needs-fix** — 3 specific issues, 4 gaps (GAP-001 through GAP-004).

The document is structurally sound: all six required sections are present (framework
definition & kind, users & what they build, author journeys, requirements & acceptance
criteria, MVP-vs-1.0 line, out-of-1.0 list), 18 REQ-FW-* ids are registered, staging and
`release_gating` fields are present on every requirement and internally consistent, the
journey-to-requirement coverage table is complete, and the document maintains the
"what, not how" discipline throughout.

**Issues found:**

1. Accessibility requirements are silently absent from both the REQ-FW-* register and
   the out-of-1.0 list — a major gap for a production web-framework 1.0. (GAP-001)

2. Component-level error handling is not addressed or deferred. WASM-thread panics
   currently abort the whole app; a 1.0 targeting production use should state its position
   on error boundaries. (GAP-002)

3. REQ-FW-013's acceptance criterion for "lean dependency footprint" uses "narrowly-scoped
   additions justified per crate" — a qualitative phrase that cannot be checked
   reproducibly. (GAP-004, minor)

4. Testing utilities are not mentioned or explicitly deferred. (GAP-003, minor)

Cross-references to sibling registers (REQ-SSR-*, REQ-API-*, REQ-ASYNC-*, REQ-RT-*,
REQ-HTTP-*, REQ-DX-*, REQ-REL-*, REQ-PERF-*, BAR-FERRIC-*) are consistent with the
document's stated role as sole owner of REQ-FW-* reading sibling registers as read-only.
Formal cross-reference validation deferred to SUBTASK_validate-crossrefs.

## Success criteria check

- [x] `scope-and-requirements.md` read from branch
- [x] All REQ-FW-* ids listed (REQ-FW-001 through REQ-FW-018)
- [x] Each validation criterion assessed (testability, MVP/1.0 line, cross-references,
      completeness, Ferric framing consistency)
- [x] `concern-findings.md` written with all required sections per contract schema
- [x] Every gap assigned a GAP-NNN id with severity (GAP-001 major, GAP-002 major,
      GAP-003 minor, GAP-004 minor)
