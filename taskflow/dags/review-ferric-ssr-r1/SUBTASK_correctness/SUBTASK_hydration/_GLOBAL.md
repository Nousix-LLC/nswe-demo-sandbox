# SUBTASK_hydration — hydrate() Correctness Review Subtree

## Context

This hub governs the decomposition of SUBTASK_hydration: reviewing PR #228 (`work/ferric-ssr-r1`,
`Nousix-LLC/nswe-demo`) against the four hydration acceptance criteria for issue #224.

Each criterion is an independent verification spoke. A synthesis task integrates their findings into
the declared output (`hydration_findings.md`) at this workspace.

---

## Scope

**In Scope:**
- REQ-HYD-001 through REQ-HYD-004 as defined in issue #224
- Hydration code path only (WASM client side): `hydrate()` and related helpers
- Marker schema documentation for the synthesis cross-check

**Out of Scope:**
- #225 / REQ-SSR-007 (async resource state)
- Axum integration (covered by SUBTASK_axum_mismatch)
- SSR render path (covered by SUBTASK_ssr_render, except where REQ-HYD-004 cross-checks markers)

---

## Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_hyd001` | none | REQ-HYD-001: Does hydrate() walk the existing DOM and attach signal listeners without re-creating or replacing nodes? | `criterion_001.md` |
| `SUBTASK_hyd002` | none | REQ-HYD-002: After hydration, do signal updates propagate to the DOM? Test evidence? | `criterion_002.md` |
| `SUBTASK_hyd003` | none | REQ-HYD-003: Is hydrate() called once from the WASM entry point? Integration test/demo? | `criterion_003.md` |
| `SUBTASK_hyd004` | none | REQ-HYD-004: Does hydration use the same marker format as SSR? Document the exact marker schema. | `criterion_004.md` |
| `SUBTASK_hyd_synthesis` | `SUBTASK_hyd001`, `SUBTASK_hyd002`, `SUBTASK_hyd003`, `SUBTASK_hyd004` | Synthesize all four criterion findings into hydration_findings.md at this workspace and fold the parent. | `../hydration_findings.md` |

### Dependency Graph

```
SUBTASK_hyd001 ──┐
SUBTASK_hyd002 ──┤
                 ├── SUBTASK_hyd_synthesis
SUBTASK_hyd003 ──┤
SUBTASK_hyd004 ──┘
```

---

## Subtree Methodology Posture

**Dominant task type**: "Ferric PR review (Rust library)" for all criterion spokes; "Synthesizing / verifying a
hub-and-spoke decomposition" for the synthesis task.

**Primary bundles (all spokes)**: `code-review`, `rust`, `framework-design`

**Cross-cutting files that bind the whole subtree**:
- `rust/Rust_WebAssembly_Browser_Methodology.md` — WASM/browser integration, wasm-bindgen; directly
  applicable to every criterion in this subtree
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — SSR +
  hydration in a Rust UI framework; hydration correctness, signal propagation, marker consistency

**Synthesis posture**: SUBTASK_hyd_synthesis is a verification gate, not a prose summary. It MUST run the
four-check model (contract, wiring, duplication, code review) over the combined criterion outputs and
either assert coverage (PASS) or schedule remediation fix-tasks (FAIL). It produces `hydration_findings.md`
at the parent workspace (this directory) and writes `SYNTHESIS.md` there as the fold record.

---

## Shared Inputs

All criterion spokes use the same upstream sources:

| Input | Source |
|-------|--------|
| PR diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` |
| Issue #224 (acceptance criteria) | `gh issue view 224 --repo Nousix-LLC/nswe-demo` |
| Branch source | `gh api repos/Nousix-LLC/nswe-demo/contents/<path>?ref=work/ferric-ssr-r1 \| jq -r '.content' \| base64 -d` |

---

## Inherited Constraints (from parent brief)

- **Non-goal**: #225/REQ-SSR-007 (async resource state) is not in scope
- **Read-only**: Do not modify source code
- **Line citations**: All findings cite files and line numbers in `Nousix-LLC/nswe-demo`, never host
  or taskflow paths
- **Non-blockers**: Flag them but they do not hold the landing
- **Machine gate**: CI passed — treat as a floor; check substance beyond what tests assert
- **Marker schema (REQ-HYD-004)**: The synthesis cross-check depends on the exact marker schema
  documented by SUBTASK_hyd004; it MUST include attribute name, value format, and determinism
  mechanism

---

## Output

The declared output of this subtree is `hydration_findings.md` at this workspace
(`SUBTASK_hydration/`), produced by SUBTASK_hyd_synthesis.
