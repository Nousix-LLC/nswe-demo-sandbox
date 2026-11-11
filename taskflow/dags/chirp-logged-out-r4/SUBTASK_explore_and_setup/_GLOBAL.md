# Chirp Logged-Out — Codebase Exploration Subtree

## Project Context

**Status**: Active

### Objective

Gather all required knowledge about the existing Chirp codebase, design requirements, and
framework APIs to produce `analysis.md` — the reference document the backend and frontend
implementation spokes depend on. Covers git branch setup, design requirements, server API
surface, frontend structure, ferric framework APIs, and API spec comparison.

### Scope

**In Scope:**
- Branch creation/verification for `work/chirp-logged-out`
- Design requirements extraction (product-requirements.md, experience-design.md, release-bar.md)
- chirp-server API surface mapping (routes, auth middleware, router setup)
- chirp-frontend structure (routing, components, API call patterns)
- Ferric framework APIs (Resource, Router, SSR, hydration)
- API spec comparison (existing server vs public_api_spec.md)
- Producing unified analysis.md

**Out of Scope:**
- Writing any code or modifying existing files
- Making final implementation decisions (analysis recommends, spokes decide)

### Success Criteria

- [ ] `work/chirp-logged-out` branch exists and is pushed to origin
- [ ] `analysis.md` exists at `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/analysis.md`
- [ ] All 5 analysis areas (A-E from parent brief) covered with specific file paths

---

## Constraints and Requirements

- Repository: `Nousix-LLC/nswe-demo` at `/home/user/nousix-runtime/nswe-demo`
- Branch base commit: `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`
- Read-only analysis — no code writing, no file modification
- Do NOT put host paths, internal addresses, or taskflow references in git commits
- SSH-tunnel kubectl/helm pattern NOT needed — this is a git/code task only

---

## Subtree Methodology Posture

**Dominant task type**: Codebase reading and analysis
**Primary bundles**: `core`, `rust` (for Axum server analysis), `operations` (for git setup)
**Cross-cutting bindings**: Every reading child is READ-ONLY; only the synthesis task writes output

---

## Task Structure

### Overview

```
_GLOBAL.md (this document)
├── contracts/_MANIFEST.yaml
├── SUBTASK_git_branch/_BRIEF.md       — Create/verify branch
├── SUBTASK_design_analysis/_BRIEF.md  — Read design docs
├── SUBTASK_server_analysis/_BRIEF.md  — Read chirp-server + API spec comparison
├── SUBTASK_frontend_analysis/_BRIEF.md — Read chirp-frontend
├── SUBTASK_ferric_analysis/_BRIEF.md  — Read ferric framework APIs
└── SUBTASK_synthesis/_BRIEF.md        — Integrate → analysis.md + SYNTHESIS.md
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_git_branch` | none | Create/verify work/chirp-logged-out branch; record HEAD SHA | `git_status.md` |
| `SUBTASK_design_analysis` | none | Extract requirements from design docs; identify route names and BAR-011 items | `design_findings.md` |
| `SUBTASK_server_analysis` | none | Map chirp-server routes, auth extractor, router file; compare with API spec | `server_findings.md` |
| `SUBTASK_frontend_analysis` | none | Map chirp-frontend router, existing route paths, API call pattern | `frontend_findings.md` |
| `SUBTASK_ferric_analysis` | none | Document ferric Resource/Router/SSR/hydration APIs | `ferric_findings.md` |
| `SUBTASK_synthesis` | `SUBTASK_git_branch`, `SUBTASK_design_analysis`, `SUBTASK_server_analysis`, `SUBTASK_frontend_analysis`, `SUBTASK_ferric_analysis` | Integrate all findings into analysis.md; write SYNTHESIS.md fold record | `analysis.md`, `SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_git_branch        ──┐
SUBTASK_design_analysis   ──┤
SUBTASK_server_analysis   ──┼── SUBTASK_synthesis
SUBTASK_frontend_analysis ──┤
SUBTASK_ferric_analysis   ──┘
```

---

## Contract

**Contract location**: `contracts/`
**Contract kind**: `markdown_sections`

The seam between reading children and the synthesis task is defined by the required sections
in each findings file. Each reading child MUST produce its declared file with the required
sections; the synthesis task asserts these identities before writing analysis.md.

### Ownership

| Artifact | Owning subtask |
|---|---|
| `SUBTASK_git_branch/git_status.md` | `SUBTASK_git_branch` |
| `SUBTASK_design_analysis/design_findings.md` | `SUBTASK_design_analysis` |
| `SUBTASK_server_analysis/server_findings.md` | `SUBTASK_server_analysis` |
| `SUBTASK_frontend_analysis/frontend_findings.md` | `SUBTASK_frontend_analysis` |
| `SUBTASK_ferric_analysis/ferric_findings.md` | `SUBTASK_ferric_analysis` |
| `analysis.md` (at parent workspace) | `SUBTASK_synthesis` |
| `SYNTHESIS.md` (at parent workspace) | `SUBTASK_synthesis` |

### Identities

- [ ] `git_status.md` MUST contain branch name and HEAD commit SHA
- [ ] `design_findings.md` MUST contain sign-in and sign-up route names, and BAR-011 items for AC-1 through AC-5
- [ ] `server_findings.md` MUST contain the router registration file path, the auth extractor type name, and the API spec verdict (match/conflict/absent for each public endpoint)
- [ ] `frontend_findings.md` MUST contain the router registration file path and the existing sign-in route path
- [ ] `ferric_findings.md` MUST contain the Resource API and Router API usage patterns, and SSR recommendation (yes/no + rationale)
- [ ] `analysis.md` MUST cover all 7 sections from the parent brief's output structure (Branch Status, Design Requirements Summary, chirp-server, chirp-frontend, Ferric Framework, API Spec Verdict, Implementation Guidance)

---

## Output Specifications

| Deliverable | Format | Location | Description |
|-------------|--------|----------|-------------|
| `analysis.md` | Markdown | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/` | Primary output — reference for backend/frontend spokes |
| `SYNTHESIS.md` | Markdown | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/` | Synthesis fold record |
