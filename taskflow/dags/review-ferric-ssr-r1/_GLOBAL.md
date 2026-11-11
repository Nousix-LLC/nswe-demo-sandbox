# review-ferric-ssr-r1 — Subtree Hub

## Objective

Review PR #228 (`feat(ferric): SSR render_to_string + client-side hydration + Axum integration`) on
branch `work/ferric-ssr-r1` in repo `Nousix-LLC/nswe-demo`. Deliver a verdict (APPROVE or
REQUEST-CHANGES) with concern-by-concern findings, post the review on the PR, file non-blocking
backlog issues, and write the authoritative SYNTHESIS.md.

## Scope

**In scope:**
- Correctness against acceptance criteria for issues #223, #224, #226
- Code quality, API design, test coverage, documentation
- Security: HTML escaping and XSS risk in render_to_string output
- Security: host/infrastructure detail exposure and supply-chain risk in the diff
- Verdict: APPROVE or REQUEST-CHANGES

**Out of scope (DO NOT block on):**
- #225 / REQ-SSR-007 (async resource state carry across SSR seam — blocked on #130)
- Router integration, form submission, or any concern outside ferric-ssr goal scope

## PR Under Review

- **Repository**: `Nousix-LLC/nswe-demo`
- **Branch**: `work/ferric-ssr-r1`
- **PR**: #228
- **Closes issues**: #223, #224, #226
- **CI**: All 6 checks passed (fmt, clippy, test, wasm, doc, image)
- **Machine gate SYNTHESIS**: `taskflow/dags/ferric-ssr-r3/SYNTHESIS.md` — PASS

## Acceptance Criteria the PR is Held To

### #223 — SSR: render_to_string
- REQ-SSR-001: `render_to_string(component, props)` renders a component tree to HTML string server-side (no DOM)
- REQ-SSR-002: Signal-driven components render from initial signal state at render time
- REQ-SSR-003: Child components and slot-based composition render correctly
- REQ-SSR-004: Rendered HTML includes `data-hydration-id` markers for client-side hydration
- REQ-SSR-005: Function accessible from an Axum handler

### #224 — Hydration: `hydrate()`
- REQ-HYD-001: `hydrate(component, props, root)` walks existing DOM, matches nodes to markers, attaches signal listeners without re-creating/replacing nodes
- REQ-HYD-002: After hydration, signal updates propagate to DOM as in a fresh mount
- REQ-HYD-003: `hydrate()` called once from WASM entry point, completes without error on correctly SSR-rendered page
- REQ-HYD-004: Hydration uses same `data-hydration-id` markers the SSR pass emitted; marker format agreed and consistent

### #226 — Mismatch detection and Axum integration
- REQ-SSR-006: If hydration walks a node whose type or marker doesn't match, it logs recoverable mismatch warning (no panic) and falls back to fresh mount for that subtree
- REQ-MIS-001: Axum integration provides handler pattern demonstrating how to call render_to_string and return HTML response
- REQ-MIS-002: Axum-rendered HTML is well-formed and contains hydration markers the client needs

## Task Structure

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_correctness` | none | Review correctness of all acceptance criteria for #223, #224, #226 | `correctness_findings.md` |
| `SUBTASK_code_quality` | none | Review code quality, API design, tests, documentation | `code_quality_findings.md` |
| `SUBTASK_security_xss` | none | Security review: HTML escaping and XSS risk in render_to_string | `security_xss_findings.md` |
| `SUBTASK_security_infra` | none | Security review: infrastructure exposure and supply-chain risk | `security_infra_findings.md` |
| `SUBTASK_synthesis` | `SUBTASK_correctness`, `SUBTASK_code_quality`, `SUBTASK_security_xss`, `SUBTASK_security_infra` | Synthesize findings, post GitHub review, file issues, write SYNTHESIS.md | `SYNTHESIS.md` (at this workspace root) |

## Dependency Graph

```
SUBTASK_correctness   ──┐
SUBTASK_code_quality  ──┤
SUBTASK_security_xss  ──┤─── SUBTASK_synthesis
SUBTASK_security_infra──┘
```

## Subtree Methodology Posture

**Dominant task type:** Ferric PR review (Rust library) — Code Review primary, Rust + Framework Design supporting.

**Primary bundles across the subtree:**
- `code-review` — CodeReview_Process_Methodology.md, CodeReview_Checklist_Methodology.md, CodeReview_Feedback_Guidelines_Methodology.md
- `rust` — Rust_Ownership_Borrowing_Methodology.md, Rust_Error_Handling_Methodology.md, Rust_WebAssembly_Browser_Methodology.md, Rust_Web_Services_Axum_Methodology.md
- `security` — Security_Secure_Coding_Methodology.md
- `framework-design` — FrameworkDesign_Library_API_Design_Methodology.md, FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md

**Cross-cutting bindings for the entire subtree:**
- Every spoke reads the actual PR diff and source code from `Nousix-LLC/nswe-demo` branch `work/ferric-ssr-r1`
- The non-goal boundary (#225/REQ-SSR-007) applies to every node — do not block on async resource state
- All findings must cite files and line numbers in the repository, not host paths or taskflow internals
- Findings without fix-able actions are framed as questions, not verdicts

## Outputs

- `SUBTASK_correctness/correctness_findings.md`
- `SUBTASK_code_quality/code_quality_findings.md`
- `SUBTASK_security_xss/security_xss_findings.md`
- `SUBTASK_security_infra/security_infra_findings.md`
- `SYNTHESIS.md` (at this workspace root, authored by SUBTASK_synthesis)

## Constraints

- Do not modify source code. Read and judge only.
- Do not comment on #225 as a blocker or finding.
- Findings naming lines point at the repository (`Nousix-LLC/nswe-demo`), not host paths.
- Non-blockers become backlog issues filed on the board; they do not hold the landing.
- The SYNTHESIS.md verdict is authoritative for the landing decision.
