# SUBTASK_quality_check — Code Quality Review Sub-DAG

## Project Context

**Status**: Active
**Goal**: Decompose the code quality review of ferric-ssr-r4 commits into two parallel spoke analyses (one per source file) and one synthesis gate that assembles them into quality_raw_findings.md.

### Objective

Produce `quality_raw_findings.md` conforming to `../contracts/spoke_output_schema.md` §SUBTASK_quality_check covering:
- Code Quality Findings: app.rs new conditional hydrate/mount dispatch; hydrate_wasm.rs test code; fresh non-blockers from #229–#242
- What Was Examined and Found Clean: each concern checked with no finding

### Cut Rationale

The parent brief enumerates 3 distinct quality concerns across 2 source files. The decomposition
splits by source file so each spoke has clear non-overlapping file ownership:
- SUBTASK_app_quality owns app.rs analysis (concern 1 + concern 3 for app.rs)
- SUBTASK_test_quality owns hydrate_wasm.rs analysis (concern 2 + concern 3 for hydrate_wasm.rs)

This minimizes cross-sibling edges (2 edges into synthesis) and distributes the cross-cutting
concern 3 (fresh non-blockers) naturally by file. Candidate: concern-type split (3 spokes)
was rejected because it creates 3 edges into synthesis and splits concern 3 into a third spoke
that depends on reading both files anyway, adding a detached analysis spoke over the same input.

### Repository

- **Repository**: Nousix-LLC/nswe-demo
- **Branch**: `work/ferric-ssr-r1`
- **Pinned commit**: `75c1eef`
- **Commits under review (ferric-ssr-r4)**: `7fb90c7`, `e625c3f`, `75c1eef`

---

## Subtree Methodology Posture

**Dominant task type**: Ferric PR review (Rust library) — code quality sub-task
**Primary bundles**: Code Review, Rust
**Supporting bundles**: Framework Design (UI reactivity & rendering internals)
**Cross-cutting**: All leaf tasks apply the principal-reviewer persona from the swe-reviewer system prompt. Evidence over assertion; every finding cites file and line at pinned commit `75c1eef`. Do not re-raise #229–#242; do not check regression criteria or security concerns.

---

## Task Structure

```
_GLOBAL.md (this document)
├── contracts/
│   ├── _MANIFEST.yaml
│   └── spoke_intermediate_schema.md
├── SUBTASK_app_quality/_BRIEF.md   (app.rs quality analysis)
├── SUBTASK_test_quality/_BRIEF.md  (hydrate_wasm.rs test code analysis)
└── SUBTASK_synthesis/_BRIEF.md     (synthesis gate → quality_raw_findings.md)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_app_quality` | none | Review app.rs new conditional (readability, edge cases, dead code, documentation) + fresh non-blockers in app.rs new code | `SUBTASK_app_quality/app_quality_raw.md` |
| `SUBTASK_test_quality` | none | Review hydrate_wasm.rs new test code (helper quality, assertion specificity, copy-paste patterns) + fresh non-blockers in hydrate_wasm.rs new code | `SUBTASK_test_quality/test_quality_raw.md` |
| `SUBTASK_synthesis` | `SUBTASK_app_quality`, `SUBTASK_test_quality` | Synthesis gate: combine both outputs into quality_raw_findings.md per parent spoke_output_schema.md | `quality_raw_findings.md` |

### Dependency Graph

```
SUBTASK_app_quality  ──┐
                        ├── SUBTASK_synthesis → quality_raw_findings.md
SUBTASK_test_quality ──┘
```

---

## Contract

**Contract location**: `contracts/`
**Contract kind**: `markdown`

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| Findings spoke schema | `../contracts/spoke_output_schema.md` | quality_raw_findings.md MUST follow §SUBTASK_quality_check format |

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/spoke_intermediate_schema.md` | Markdown template | Sections each spoke intermediate file must carry |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `SUBTASK_app_quality/app_quality_raw.md` | `SUBTASK_app_quality` |
| `SUBTASK_test_quality/test_quality_raw.md` | `SUBTASK_test_quality` |
| `quality_raw_findings.md` | `SUBTASK_synthesis` |

### Identities

- [ ] `app_quality_raw.md` carries `## App.rs Code Quality Findings` and `## App.rs Fresh Non-blockers` and `## App.rs What Was Examined and Found Clean`
- [ ] `test_quality_raw.md` carries `## hydrate_wasm.rs Code Quality Findings` and `## hydrate_wasm.rs Fresh Non-blockers` and `## hydrate_wasm.rs What Was Examined and Found Clean`
- [ ] `quality_raw_findings.md` carries `## Code Quality Findings` and `## What Was Examined and Found Clean` per parent spoke_output_schema.md

---

## Subtree-Wide Constraints

- Scope is ferric-ssr-r4 commits only: `7fb90c7`, `e625c3f`, `75c1eef`
- Do NOT re-raise non-blockers #229–#242
- Evidence must cite file + line at pinned commit `75c1eef`
- Security concerns are out of scope (those are SUBTASK_sec_check)
- Architecture review is out of scope
- Do not reference overseer escalation comments from I267

---

## Output Specification

| Deliverable | Location | Description |
|-------------|----------|-------------|
| `quality_raw_findings.md` | `SUBTASK_quality_check/` | Code quality findings following parent spoke_output_schema.md |
