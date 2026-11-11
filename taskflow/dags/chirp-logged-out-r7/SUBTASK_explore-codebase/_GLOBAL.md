# Codebase Exploration Subtree — Chirp Logged-Out r7

## Context

**Status**: Active  
**Parent**: `chirp-logged-out-r7` taskflow  
**Parent Hub**: `../_GLOBAL.md`  
**Declared output at parent level**: `analysis.md` (owned by this task per parent `contracts/_MANIFEST.yaml`)

### Objective

Explore the Chirp codebase and design documents to understand the current state of each relevant system component, then synthesize that reading into `analysis.md` — the gap analysis document the downstream backend and frontend tasks consume.

The exploration splits by source: each survey spoke reads one codebase or document set independently; the synthesis hub combines their findings into the declared output.

### Scope

**In scope:**
- Reading `design/product-requirements.md`, `design/experience-design.md`, `design/release-bar.md` for AC requirements
- Reading `crates/chirp-server/` for existing API routes and auth middleware
- Reading `crates/chirp-frontend/` for router setup and existing route behavior
- Reading `crates/ferric/` for async resource primitives and component patterns (PRs #193, #203, #228)
- Reading parent `contracts/public_api_contract.md` for inherited API surface declaration
- Creating the work branch `work/chirp-logged-out` from `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`
- Writing `analysis.md` and `SYNTHESIS.md` at this workspace root

**Out of scope:**
- Any code changes in any crate
- Writing tests
- Authoring PRs or commits (other than branch creation)

---

## Inherited Contracts (READ-ONLY for all descendants)

Ancestor contracts at `../contracts/` bind this subtree:

| Ancestor artifact | Path | Binding |
|---|---|---|
| Ownership manifest | `../contracts/_MANIFEST.yaml` | `analysis.md` is owned by this task (SUBTASK_explore-codebase); descendants must produce it at this workspace root |
| Public API contract | `../contracts/public_api_contract.md` | Declares the API surface SUBTASK_backend-api must implement; survey children read this for context |

Descendants MUST NOT write to `../contracts/`.

---

## Task Structure

```
_GLOBAL.md (this document)
├── contracts/
│   └── _MANIFEST.yaml               (survey output ownership + synthesis identity)
├── SUBTASK_explore-survey-design/
│   └── _BRIEF.md                    → design-survey.md
├── SUBTASK_explore-survey-backend/
│   └── _BRIEF.md                    → backend-survey.md
├── SUBTASK_explore-survey-frontend/
│   └── _BRIEF.md                    → frontend-survey.md
├── SUBTASK_explore-survey-ferric/
│   └── _BRIEF.md                    → ferric-survey.md
└── SUBTASK_explore-synthesis/
    └── _BRIEF.md                    → analysis.md + SYNTHESIS.md (at this workspace root)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_explore-survey-design` | none | Read design docs, extract AC requirements | `SUBTASK_explore-survey-design/design-survey.md` |
| `SUBTASK_explore-survey-backend` | none | Read chirp-server/, document API routes and auth | `SUBTASK_explore-survey-backend/backend-survey.md` |
| `SUBTASK_explore-survey-frontend` | none | Read chirp-frontend/, document routes and logged-out behavior | `SUBTASK_explore-survey-frontend/frontend-survey.md` |
| `SUBTASK_explore-survey-ferric` | none | Read ferric/, document async resource primitives from PRs #193, #203, #228 | `SUBTASK_explore-survey-ferric/ferric-survey.md` |
| `SUBTASK_explore-synthesis` | `SUBTASK_explore-survey-design`, `SUBTASK_explore-survey-backend`, `SUBTASK_explore-survey-frontend`, `SUBTASK_explore-survey-ferric` | Synthesize surveys into analysis.md; create branch; write SYNTHESIS.md | `analysis.md`, `SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_explore-survey-design    ──┐
                                   │
SUBTASK_explore-survey-backend   ──┤──► SUBTASK_explore-synthesis
                                   │
SUBTASK_explore-survey-frontend  ──┤
                                   │
SUBTASK_explore-survey-ferric    ──┘
```

---

## Cut Rationale

Each survey child reads one distinct codebase or document set with no overlap in what they write. The synthesis child aggregates their outputs. This maximizes parallelism (all 4 surveys can run concurrently), maintains disjoint file ownership, and keeps each survey child in the S-band (~50-100 lines of focused notes).

---

## Contract

**Contract location**: `contracts/`  
**Contract kind**: `yaml_schema` (document assembly)

The contract declares ownership of each survey file and the identity assertions the synthesis task must verify.

| Artifact | Declares |
|---|---|
| `contracts/_MANIFEST.yaml` | Survey output ownership, path of each intermediate file, identity: analysis.md must cover all required sections from parent brief |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `SUBTASK_explore-survey-design/design-survey.md` | `SUBTASK_explore-survey-design` |
| `SUBTASK_explore-survey-backend/backend-survey.md` | `SUBTASK_explore-survey-backend` |
| `SUBTASK_explore-survey-frontend/frontend-survey.md` | `SUBTASK_explore-survey-frontend` |
| `SUBTASK_explore-survey-ferric/ferric-survey.md` | `SUBTASK_explore-survey-ferric` |
| `analysis.md` (at this workspace root) | `SUBTASK_explore-synthesis` |
| `SYNTHESIS.md` (at this workspace root) | `SUBTASK_explore-synthesis` |

### Identities

- [ ] `analysis.md` MUST contain: branch status, API endpoint survey, frontend route survey, Ferric primitives survey, per-AC gap analysis (AC-1 through AC-5), implementation plan summary
- [ ] Branch `work/chirp-logged-out` MUST exist at commit `cb1ced3` before `analysis.md` is written
- [ ] No code changes in any crate; `analysis.md` is the only new file in the codebase

---

## Subtree Methodology Posture

**Dominant task type**: Codebase exploration / analysis (reading Rust code, design docs)

**Primary bundles** applicable to survey spokes:
- `rust` → understanding Axum handler patterns, Ferric framework internals
- `architecture` → API design evaluation lens

**Primary bundles** applicable to synthesis:
- `architecture/Architecture_API_Design_Methodology.md` → gap analysis framing
- `core/BestPractices_Coding_Standards_Methodology.md` → code quality baseline

**Cross-cutting constraints** for all descendants:
- No code changes — exploration only
- Repository: Nousix-LLC/nswe-demo, branch `work/chirp-logged-out` from `cb1ced3`
- No host paths, internal addresses, or taskflow references in any output or committed content
- Rust 2021 edition; Cargo workspace conventions

---

## Output Specifications

| Deliverable | Format | Location | Description |
|-------------|--------|----------|-------------|
| design-survey.md | Markdown | `SUBTASK_explore-survey-design/` | Extracted ACs, requirements, screen specs |
| backend-survey.md | Markdown | `SUBTASK_explore-survey-backend/` | Existing API endpoints, auth requirements, handler patterns |
| frontend-survey.md | Markdown | `SUBTASK_explore-survey-frontend/` | Router config, routes, current logged-out behavior |
| ferric-survey.md | Markdown | `SUBTASK_explore-survey-ferric/` | Async resource primitives, SSR, component patterns |
| analysis.md | Markdown | `./` (this workspace root) | Final gap analysis — all required sections |
| SYNTHESIS.md | Markdown | `./` (this workspace root) | Subtree synthesis record |
