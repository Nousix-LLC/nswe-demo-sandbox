# SUBTASK_axum_server — Axum Handler + HTML Output Review (REQ-MIS-001, REQ-MIS-002, REQ-SSR-007)

## Task Specification

**Slug**: SUBTASK_axum_server
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Review the server-side Axum integration in PR #228 (`work/ferric-ssr-r1`, `Nousix-LLC/nswe-demo`)
against two acceptance criteria for issue #226:
- **REQ-MIS-001**: Does the Axum integration provide a handler pattern (example or real handler) that calls
  `render_to_string` and returns the HTML response using `Html(...)` or equivalent?
- **REQ-MIS-002**: Is the Axum-rendered HTML well-formed (balanced tags, valid attributes)? Does it contain
  the hydration markers the client needs?

Also confirm the non-goal boundary:
- **REQ-SSR-007 / #225**: Async resource state carry across the SSR seam — confirm this feature is absent or
  only guarded/stubbed. Do not report its absence as a finding.

Produce `axum_server_findings.md` with a named, evidence-backed verdict for each criterion and an explicit
non-goal confirmation. Document the exact hydration-marker format the server writes into the HTML.

### Context

This task is part of the SUBTASK_axum_mismatch subtree (see `../_GLOBAL.md`). It runs in parallel
with SUBTASK_mismatch_detect. Its output is consumed by SUBTASK_mismatch_synthesis.

**Depends on**: none (independent spoke)
**Dependents**: `SUBTASK_mismatch_synthesis` reads `axum_server_findings.md`

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `../_GLOBAL.md` | PR coordinates, shared constraints, schema |
| Parent context | `../../_GLOBAL.md` | Subtree-wide constraints |
| PR diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | The change under review |
| Branch source | `gh api repos/Nousix-LLC/nswe-demo/contents/<path>?ref=work/ferric-ssr-r1 \| jq -r '.content' \| base64 -d` | Full file content for Axum handler and HTML output |
| Issue #226 | `gh issue view 226 --repo Nousix-LLC/nswe-demo` | Acceptance criteria for REQ-MIS-001, REQ-MIS-002 |

---

## Review Scope

### REQ-MIS-001 — Axum handler pattern

Examine the Axum integration code (example handler or real handler in the PR):
- Does it call `render_to_string`? Is the call correct (right arguments, right context)?
- Does it return the HTML via `Html(...)` (axum's `Html` extractor/response type) or an equivalent
  valid Axum response type?
- Is the handler signature valid Axum code? Does it correctly wire into an Axum router?

### REQ-MIS-002 — HTML well-formedness and markers

Examine the HTML that the Axum handler produces (either via rendered output in tests, example output in
documentation/tests, or by tracing through `render_to_string`):
- Is the HTML well-formed: balanced tags, valid attribute syntax?
- Does it contain the hydration markers the client needs to identify component subtrees? (Exact marker
  format: document the attribute name and value format you observe.)
- Are the markers placed correctly (at the right elements, in the right positions)?

### REQ-SSR-007 / #225 — Non-goal confirmation

Examine the Axum integration code and SSR path to confirm:
- Is there any implementation of async resource state carry across the SSR seam (e.g., serialized
  async state passed from server to client via the HTML, deferred resource hydration)?
- If not: state explicitly what code you examined and that the feature is absent or only
  guarded/stubbed (e.g., behind a feature flag, behind a TODO comment, behind a `todo!()` macro).
- Do NOT report the absence as a deficiency.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| File | `axum_server_findings.md` |
| Location | this workspace (`SUBTASK_axum_server/`) |

### Output Structure

```markdown
# Axum Server-Side Findings (REQ-MIS-001, REQ-MIS-002, REQ-SSR-007)

## REQ-MIS-001 — Axum handler pattern
**Status**: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
**What was checked**: <what handler code was examined>
**Evidence**: `<file:line>`
**Finding** (if any): <description>

## REQ-MIS-002 — HTML well-formedness and markers
**Status**: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
**What was checked**: <what HTML output or render path was examined>
**Evidence**: `<file:line>`
**Finding** (if any): <description>

## Marker Format Observed (Server Side)
**Server-side marker format**: <exact attribute name and format written into HTML>
**Evidence**: `<file:line>`

## Non-goal Boundary
### REQ-SSR-007 / #225 — Async resource state (non-goal)
**Status**: CONFIRMED NON-GOAL
**What was checked**: <what code was examined to confirm absence or stubbing>
**Evidence**: `<file:line>`
```

---

## Success Criteria

- [ ] REQ-MIS-001 verdict: named status (CLEAN, FINDING BLOCKER, or FINDING NON-BLOCKER) with evidence
- [ ] REQ-MIS-002 verdict: named status with evidence
- [ ] REQ-SSR-007 non-goal: explicitly confirmed (what code examined, where absence or stub appears)
- [ ] Server-side marker format documented (attribute name and format, with evidence)
- [ ] Evidence cites files and line numbers in `Nousix-LLC/nswe-demo`
- [ ] `axum_server_findings.md` exists at the declared path before this task reports completed

---

## Suggested Methodology Files

**Task-type row matched**: "Ferric PR review (Rust library)" → Primary: `Code Review`; Supporting: `Rust`,
`Framework Design`

Specific files:
- `code-review/CodeReview_Process_Methodology.md` — systematic review pass; anchoring findings to evidence
- `code-review/CodeReview_Checklist_Methodology.md` — per-criterion checklist discipline
- `rust/Rust_Web_Services_Axum_Methodology.md` — Axum handler patterns, correct use of `Html(...)`, router
  wiring, handler signature requirements; directly applicable to REQ-MIS-001
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — SSR HTML output
  structure, hydration marker placement; relevant background for REQ-MIS-002

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but
is the final judge — load fewer if some are clearly inapplicable; load more if the brief reveals additional
surface the parent did not anticipate.

---

## Inherited Constraints

- **Non-goal**: REQ-SSR-007 MUST be confirmed as absent or stubbed, NOT evaluated as deficient — this is an
  explicit constraint, not an oversight
- **Read-only**: Do not modify source code
- **Line citations**: All findings cite files and line numbers in `Nousix-LLC/nswe-demo`, never host paths
  or taskflow paths
- **Non-blockers**: Flag them but they do not hold the landing
- **Machine gate**: CI passed — treat as a floor; check substance beyond what tests assert
- **Marker format**: Document what you observe; the synthesis task cross-checks with the client side

## Out-of-Scope Methodologies

- Any methodology focused on WASM or `#[cfg(target_arch = "wasm32")]` code — that is SUBTASK_mismatch_detect's scope
- Async Tokio runtime patterns deeper than what is needed to understand the handler (REQ-SSR-007 is a non-goal)
