# SUBTASK_code-quality — Subtree Hub

**Status**: Active — decomposed into spoke tasks

## Project Context

### Objective

Review the code quality of all new and changed code introduced by the ferric-ssr-r4 commits
(`7fb90c7`, `e625c3f`, `75c1eef`), producing a `code-quality.md` with an overall PASS/FAIL
verdict. Two files are in scope: `app.rs` (cfg-gate + conditional hydrate dispatch) and
`hydrate_wasm.rs` (new 197-line wasm-bindgen-test file).

### Scope

**In Scope:**
- `app.rs`: cfg-gate idiom, conditional dispatch correctness, error handling, docstring
  accuracy, readability
- `hydrate_wasm.rs`: test structure and naming, setup/teardown and DOM cleanup, hardcoded
  strings vs. imported constants, duplication, assertion quality
- Fresh non-blocking issues found in either file

**Out of Scope:**
- Security concerns (HTML injection, escaping) — SUBTASK_security
- Regression checking of acceptance criteria — SUBTASK_regression-check
- Previously filed issues #229–#242

### Success Criteria

- [ ] `code-quality.md` written at this workspace root
- [ ] app.rs reviewed across all five quality dimensions
- [ ] hydrate_wasm.rs reviewed across all five quality dimensions
- [ ] Fresh non-blockers noted (or "None found")
- [ ] Overall PASS or FAIL verdict stated with rationale

---

## Inputs

| Source | Location | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Parent context and subtree-wide constraints |
| PR #228 diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | Full diff for context |
| `app.rs` | `crates/chirp-frontend/src/app.rs` on branch `work/ferric-ssr-r1` | cfg-gate quality review |
| `hydrate_wasm.rs` | `crates/ferric/tests/hydrate_wasm.rs` on branch | Test quality review |

---

## Task Structure

```
_GLOBAL.md (this file)
├── contracts/
│   └── _MANIFEST.yaml                  — ownership + format identity
├── SUBTASK_app-rs-quality/
│   └── _BRIEF.md                       — review app.rs quality
├── SUBTASK_hydrate-wasm-quality/
│   └── _BRIEF.md                       — review hydrate_wasm.rs quality
└── SUBTASK_quality-synthesis/
    └── _BRIEF.md                       — combine → code-quality.md
```

### Task Summary

| Task id | Depends on | Description | Output |
|---|---|---|---|
| `SUBTASK_app-rs-quality` | none | Review app.rs cfg-gate quality across 5 dimensions | `SUBTASK_app-rs-quality/app-rs-notes.md` |
| `SUBTASK_hydrate-wasm-quality` | none | Review hydrate_wasm.rs test quality across 5 dimensions | `SUBTASK_hydrate-wasm-quality/hydrate-wasm-notes.md` |
| `SUBTASK_quality-synthesis` | `SUBTASK_app-rs-quality`, `SUBTASK_hydrate-wasm-quality` | Combine findings → code-quality.md + overall verdict | `code-quality.md` |

### Dependency Graph

```
SUBTASK_app-rs-quality ───────┐
                              ├── SUBTASK_quality-synthesis
SUBTASK_hydrate-wasm-quality ─┘
```

---

## Contract

**Contract location**: `contracts/`
**Contract kind**: ownership manifest + finding format (`yaml_schema`)

The two spoke tasks read independent source files and each produce a findings markdown file. The
synthesis task reads both note files and assembles the final `code-quality.md`. The contract
freezes the finding-note format so synthesis can assemble mechanically.

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/_MANIFEST.yaml` | ownership manifest | Per-child output ownership and format identities |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `SUBTASK_app-rs-quality/app-rs-notes.md` | `SUBTASK_app-rs-quality` |
| `SUBTASK_hydrate-wasm-quality/hydrate-wasm-notes.md` | `SUBTASK_hydrate-wasm-quality` |
| `code-quality.md` | `SUBTASK_quality-synthesis` |

### Identities

- [ ] `app-rs-notes.md` contains findings for all five app.rs quality dimensions
- [ ] `hydrate-wasm-notes.md` contains findings for all five hydrate_wasm.rs quality dimensions
- [ ] Each finding includes a severity label (Blocker / Warning / Pass) and cited evidence
      (file:line or "N/A") or a "not applicable" note
- [ ] `code-quality.md` incorporates all findings from both note files
- [ ] Overall PASS/FAIL verdict in `code-quality.md` is consistent with finding severities

### Derived Artifacts

None — spokes are read-only analyses; no mocks or stubs generated.

---

## Subtree Methodology Posture

**Dominant task type**: Code review (Rust library — cfg-gate implementation + wasm-bindgen tests)

**Primary bundles**:
- `code-review` — systematic concern coverage and quality checklist
- `rust` — Rust-specific idiom and test quality standards

**Files that bind the whole subtree**:
- `code-review/CodeReview_Process_Methodology.md`
- `code-review/CodeReview_Checklist_Methodology.md`
- `rust/Rust_WebAssembly_Browser_Methodology.md` — WASM/wasm-bindgen discipline (both spokes share this)
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — SSR/hydration correctness context

**Subtask-specific**:
- `rust/Rust_Testing_Methodology.md` — SUBTASK_hydrate-wasm-quality primarily
- `synthesis/Synthesis_Overview_Methodology.md` — SUBTASK_quality-synthesis (verification gate)

**Note**: These are starting points; each child agent retains final judgment.

---

## Subtree-Wide Constraints

- **Repository**: Nousix-LLC/nswe-demo, branch `work/ferric-ssr-r1`, PR #228
- **Commits under inspection**: `7fb90c7`, `e625c3f`, `75c1eef`
- **Do not re-raise**: Issues #229–#242
- **Do not reference**: Overseer I267 escalation comments
- **Non-blockers**: List in notes only; synthesis task decides whether to include in code-quality.md
- **Prose bar**: Output must be free of AI-tell patterns (moral adjectives on metrics, narrated
  candor, slot-fill templates, padding filler)
- **Scope boundary**: Code quality only — security is SUBTASK_security; regression is
  SUBTASK_regression-check
