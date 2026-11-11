# PR #228 Correctness Review — SUBTASK_correctness Subtree Hub

## Project Context

**Status**: Active

### Objective

Review PR #228 (`work/ferric-ssr-r1`, `Nousix-LLC/nswe-demo`) for correctness against every acceptance
criterion in issues #223, #224, and #226. Produce `correctness_findings.md` with a named verdict (CLEAN or
FINDING) and evidence for each criterion.

### Scope

**In scope:**
- #223 (render_to_string): REQ-SSR-001 through REQ-SSR-005
- #224 (hydrate()): REQ-HYD-001 through REQ-HYD-004
- #226 (mismatch detection + Axum integration): REQ-SSR-006, REQ-MIS-001, REQ-MIS-002
- REQ-SSR-007 / #225: Confirm explicitly as non-goal (absent or stubbed, not deficient)

**Out of scope:**
- Modifying source code
- Code quality, style, or security concerns (covered by sibling spokes in the parent DAG)
- Async resource state carry (#225/REQ-SSR-007) — confirm it is absent, do not evaluate as deficient

### Success Criteria

- [ ] Every criterion listed above has a CLEAN or FINDING verdict with cited evidence
- [ ] REQ-SSR-004 (SSR marker format) and REQ-HYD-004 (hydration marker format) are cross-checked for consistency
- [ ] Non-goal REQ-SSR-007 is explicitly confirmed
- [ ] `correctness_findings.md` exists at `../correctness_findings.md` before the synthesis task reports completed

---

## Input Specifications

All spoke tasks share these primary inputs:

| Source | Access | Purpose |
|--------|--------|---------|
| PR diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | The change under review |
| Branch source | Branch `work/ferric-ssr-r1` via `gh api` or `gh pr files` | Full file content for files touched |
| Issue #223 | `gh issue view 223 --repo Nousix-LLC/nswe-demo` | render_to_string acceptance criteria |
| Issue #224 | `gh issue view 224 --repo Nousix-LLC/nswe-demo` | hydrate() acceptance criteria |
| Issue #226 | `gh issue view 226 --repo Nousix-LLC/nswe-demo` | mismatch detection + Axum criteria |

**CI gate**: All 6 CI checks passed on PR #228. Treat as a floor, not a ceiling; it does not substitute for review.

---

## Subtree Methodology Posture

**Dominant task type**: Ferric PR review (Rust library)

**Primary bundles** every child draws from:
- `code-review` — review process, checklist, feedback guidelines
- `rust` — especially `Rust_WebAssembly_Browser_Methodology.md` (WASM/cfg split), `Rust_Web_Services_Axum_Methodology.md` (Axum patterns)
- `framework-design` — especially `FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` (SSR + hydration in a Rust UI framework)

**Synthesis child** additionally draws from:
- `synthesis` — Synthesis_Overview, Synthesis_Code_Review, Synthesis_Contract_Verification

**Cross-cutting binding for the entire subtree**: The marker format (`data-hydration-id` or equivalent) is the
seam between the SSR and hydration paths. Every child that touches markers (SUBTASK_ssr_render on REQ-SSR-004,
SUBTASK_hydration on REQ-HYD-004) MUST document the exact marker schema observed. The synthesis cross-checks
these for agreement.

**Suggestion-not-prescription**: Child agents retain final judgment over what they load and how deeply they go.

---

## Subtree-Wide Constraints

- **Read-only**: No source code modification
- **Non-goal**: Async resource state (#225/REQ-SSR-007) is not a finding or blocker
- **Evidence standard**: All findings cite files and line numbers in `Nousix-LLC/nswe-demo`, never host paths or taskflow paths
- **Non-blockers**: Flag them but they do not hold the landing (SUBTASK_synthesis in the parent DAG files them as issues)
- **Machine gate**: CI passed — it is a floor; reviewers check substance beyond what tests assert

---

## Task Structure

```
_GLOBAL.md (this document)
├── contracts/
│   └── _MANIFEST.yaml              (findings schema + cross-check identities)
├── SUBTASK_ssr_render/
│   └── _BRIEF.md                   → ssr_render_findings.md
├── SUBTASK_hydration/
│   └── _BRIEF.md                   → hydration_findings.md
├── SUBTASK_axum_mismatch/
│   └── _BRIEF.md                   → axum_mismatch_findings.md
└── SUBTASK_correctness_synthesis/
    └── _BRIEF.md                   → ../correctness_findings.md (parent output)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_ssr_render` | none | Review #223 criteria (REQ-SSR-001–005): render_to_string SSR path | `ssr_render_findings.md` |
| `SUBTASK_hydration` | none | Review #224 criteria (REQ-HYD-001–004): hydrate() WASM path | `hydration_findings.md` |
| `SUBTASK_axum_mismatch` | none | Review #226 criteria (REQ-SSR-006, REQ-MIS-001–002) + confirm non-goal REQ-SSR-007 | `axum_mismatch_findings.md` |
| `SUBTASK_correctness_synthesis` | `SUBTASK_ssr_render`, `SUBTASK_hydration`, `SUBTASK_axum_mismatch` | Verification gate: cross-check marker consistency and produce correctness_findings.md | `../correctness_findings.md` |

### Dependency Graph

```
SUBTASK_ssr_render     ──┐
                         │
SUBTASK_hydration      ──├── SUBTASK_correctness_synthesis
                         │
SUBTASK_axum_mismatch  ──┘
```

---

## Contract

**Contract location**: `contracts/`
**Contract kind**: `yaml_schema`

### Structural Declarations

Each spoke MUST produce its findings file conforming to this schema:

```yaml
# findings file schema (YAML block per criterion)
criteria:
  - id: <REQ-XXX-NNN>                      # criterion identifier as in the brief
    status: CLEAN | FINDING_BLOCKER | FINDING_NON_BLOCKER
    what_checked: <text>                    # what code/behavior was examined
    evidence: <"file:line" or "file:line–line">   # location in Nousix-LLC/nswe-demo
    finding: <text | null>                 # null when status is CLEAN

non_goal: <null | text>                    # for REQ-SSR-007 confirmation (axum_mismatch spoke only)
```

Spokes MAY produce markdown-formatted files following this structure as long as the information is present and
unambiguous. The synthesis task reads the information structurally; prose framing around it is acceptable.

**Cross-check identity**: The marker format documented in `ssr_render_findings.md` for REQ-SSR-004 MUST
agree with the marker format documented in `hydration_findings.md` for REQ-HYD-004. The synthesis task
verifies this identity and MUST NOT silently plug a failure.

### Ownership

| Artifact | Owning subtask |
|----------|---------------|
| `ssr_render_findings.md` | `SUBTASK_ssr_render` |
| `hydration_findings.md` | `SUBTASK_hydration` |
| `axum_mismatch_findings.md` | `SUBTASK_axum_mismatch` |
| `../correctness_findings.md` | `SUBTASK_correctness_synthesis` |

### Identities

- [ ] Every criterion in scope has a verdict (no criterion silently omitted)
- [ ] REQ-SSR-004 marker schema (from ssr_render) agrees with REQ-HYD-004 marker schema (from hydration)
- [ ] REQ-SSR-007/non-goal is explicitly confirmed as absent/stubbed (not evaluated as deficient)
- [ ] No finding cites a host path, taskflow path, or test assertion as evidence of behavior — evidence is code at a named file:line

### Derived Artifacts

None. Spokes work directly from PR diff and branch source.
