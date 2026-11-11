# SUBTASK_mismatch_detect — REQ-SSR-006 Mismatch Detection Review

## Task Specification

**Slug**: SUBTASK_mismatch_detect
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Review the mismatch detection implementation in PR #228 (`work/ferric-ssr-r1`,
`Nousix-LLC/nswe-demo`) against REQ-SSR-006: Does mismatch detection fire on actual structural
mismatches (wrong node type, missing or wrong marker)? Does it log a recoverable warning (not panic)
and fall back to a fresh mount for that subtree? Is there test coverage for the mismatch path?

Produce `mismatch_detect_findings.md` with a named, evidence-backed verdict for REQ-SSR-006 and
a note of the exact hydration-marker format the mismatch detection logic reads from the DOM.

### Context

This task is part of the SUBTASK_axum_mismatch subtree (see `../_GLOBAL.md`). It runs in parallel
with SUBTASK_axum_server. Its output is consumed by SUBTASK_mismatch_synthesis.

**Depends on**: none (independent spoke)
**Dependents**: `SUBTASK_mismatch_synthesis` reads `mismatch_detect_findings.md`

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `../_GLOBAL.md` | PR coordinates, shared constraints, schema |
| Parent context | `../../_GLOBAL.md` | Subtree-wide constraints, CI gate status |
| PR diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | The change under review |
| Branch source | `gh api repos/Nousix-LLC/nswe-demo/contents/<path>?ref=work/ferric-ssr-r1 \| jq -r '.content' \| base64 -d` | Full file content for mismatch detection code and tests |
| Issue #226 | `gh issue view 226 --repo Nousix-LLC/nswe-demo` | Acceptance criteria for REQ-SSR-006 |

---

## Review Scope

Examine the mismatch detection code on the client (WASM) side of the SSR seam:

**REQ-SSR-006**: Does mismatch detection fire on actual structural mismatches (wrong node type,
missing or wrong marker)? Does it log a recoverable warning — not a panic — and fall back to a
fresh mount for that subtree? Is there test coverage for the mismatch path?

Specific things to check:
1. The mismatch detection logic: what conditions trigger it? Does it read DOM markers to identify
   hydration targets? What constitutes a "structural mismatch"?
2. Error handling: does a mismatch cause a `panic!` or an `unwrap()`, or does it log a warning
   (e.g., `warn!`, `console.warn`, or similar) and proceed with a fresh mount?
3. Fallback behavior: does the code actually mount fresh when a mismatch is detected, or does it
   silently continue on the mismatched tree?
4. Test coverage: are there tests that exercise the mismatch detection path? Do they assert
   behavioral outcomes (warning logged, fresh mount performed) or only that the code path was
   reached?

Additionally, **document the exact hydration-marker format** the detection logic reads (e.g.,
attribute name like `data-hydration-id`, attribute format, what values are expected). The synthesis
task cross-checks this against the server-side marker format.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| File | `mismatch_detect_findings.md` |
| Location | this workspace (`SUBTASK_mismatch_detect/`) |

### Output Structure

```markdown
# Mismatch Detection Findings (REQ-SSR-006)

## REQ-SSR-006 — Mismatch detection
**Status**: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
**What was checked**: <what code and tests were examined>
**Evidence**: `<file:line>` (or `<file:start–end>`)
**Finding** (if any): <description of the finding>

## Marker Format Observed
**Client-side marker format**: <exact attribute name and format the detection logic reads>
**Evidence**: `<file:line>`
```

---

## Success Criteria

- [ ] REQ-SSR-006 verdict: named status (CLEAN, FINDING BLOCKER, or FINDING NON-BLOCKER)
- [ ] Evidence cites files and line numbers in `Nousix-LLC/nswe-demo`
- [ ] Marker format documented (attribute name and format, with evidence)
- [ ] `mismatch_detect_findings.md` exists at the declared path before this task reports completed

---

## Suggested Methodology Files

**Task-type row matched**: "Ferric PR review (Rust library)" → Primary: `Code Review`; Supporting: `Rust`,
`Framework Design`

Specific files:
- `code-review/CodeReview_Process_Methodology.md` — systematic review pass; anchoring findings to evidence
- `code-review/CodeReview_Checklist_Methodology.md` — per-criterion checklist discipline
- `rust/Rust_Web_Services_Axum_Methodology.md` — Rust web services context (secondary here, more relevant to sibling)
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — SSR + hydration
  in a Rust UI framework; primary reference for mismatch detection semantics, marker schema, hydration error
  handling discipline

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but
is the final judge — load fewer if some are clearly inapplicable; load more if the brief reveals additional
surface the parent did not anticipate.

---

## Inherited Constraints

- **Non-goal**: REQ-SSR-007 (async resource state) is not in scope for this spoke — do not evaluate it
- **Read-only**: Do not modify source code
- **Line citations**: All findings cite files and line numbers in `Nousix-LLC/nswe-demo`, never host paths
  or taskflow paths
- **Non-blockers**: Flag them but they do not hold the landing
- **Machine gate**: CI passed — treat as a floor; check substance beyond what tests assert
- **Marker format**: Document what you observe; the synthesis task will cross-check with the server side

## Out-of-Scope Methodologies

- `rust/Rust_Async_Tokio_Methodology.md` — async Tokio is server-side; this spoke is client-side WASM
- Any methodology focused on HTML output quality — that is SUBTASK_axum_server's scope
