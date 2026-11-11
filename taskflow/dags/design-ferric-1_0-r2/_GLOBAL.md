# Design DAG (recovery): Ferric → 1.0 — Subtree Hub

## Project Context

**Status**: Active  
**Recovery of**: frozen/failed `design-ferric-1_0` (overseer I61)  
**Owned by**: overseer iteration I73  
**Observation seam**: `SYNTHESIS.md` at this workspace

### Objective

Validate and complete the Ferric 1.0 framework design that the prior failed run partially produced, fill any
remaining gaps, and produce the root `SYNTHESIS.md` that states the release bar and indexes issues by epic.

The prior run produced:
- All ten design documents on branch `work/design-ferric-1_0` (`design/ferric/`) of `Nousix-LLC/nswe-demo`
- Epics #129–#136 and child issues #137–#164 on the `NSWE Delivery` board (GitHub Project #1)
- PR #128 ("design: Ferric 1.0 framework design") — open, not yet merged

What it did NOT produce: the root `SYNTHESIS.md` at this workspace (the overseer's fold point).

### Scope

**In scope:**
- Validating all ten design documents (`design/ferric/`) against the live Ferric codebase and each other
- Reconciling requirement registers (`REQ-FW-*`, `REQ-SSR-*`, `REQ-API-*`, `REQ-ASYNC-*`, `REQ-RT-*`,
  `REQ-HTTP-*`, `REQ-DX-*`, `REQ-REL-*`, `REQ-PERF-*`) across documents
- Checking the filed issues and epics for completeness and traceability
- Remediating any gaps found (missing requirements, broken traceability, stale references)
- Producing the root `SYNTHESIS.md`

**Out of scope:**
- Framework code changes
- Changes to the chirp product design (`design/` outside `design/ferric/`)
- Any repository other than `Nousix-LLC/nswe-demo`
- Any GitHub Project other than `NSWE Delivery` (Project #1)

### Success Criteria

- [ ] All nine concern areas validated and gap-free
- [ ] All issues/epics on the board traceable to design requirements
- [ ] PR #128 confirmed ready for merge (or updated if needed)
- [ ] Root `SYNTHESIS.md` at this workspace produced with release bar + issue index by epic

---

## Key Inputs

| Input | Location | Status |
|---|---|---|
| Design documents | `design/ferric/` on branch `work/design-ferric-1_0` | Produced by prior run — validate |
| Contract artifacts | `design/ferric/contracts/` on same branch | Produced by prior run — validate |
| Prior-art spoke outputs | `prior-art/` in this workspace | Reference drafts — compare |
| Ferric codebase | `crates/ferric/` on `main` (HEAD `276138f`) | Ground-truth for accuracy checks |
| Filed epics | #129–#136 on `Nousix-LLC/nswe-demo` | Validate against design |
| Filed child issues | #137–#164 on `Nousix-LLC/nswe-demo` | Validate against design |
| PR | #128 on `Nousix-LLC/nswe-demo` | Confirm completeness |

---

## Design Document Register (all ten, as landed on branch)

| File | Concern | REQ register |
|---|---|---|
| `scope-and-requirements.md` | Framework scope & 1.0 requirements | `REQ-FW-*` |
| `ssr-hydration.md` | SSR + hydration (must-have) | `REQ-SSR-*` |
| `authoring-model.md` | `view!` macro, props, children, slots, context | `REQ-API-*` |
| `async-forms-events.md` | Async resources, forms, DOM events | `REQ-ASYNC-*` |
| `router-and-http.md` | Router + HTTP/JSON client | `REQ-RT-*`, `REQ-HTTP-*` |
| `docs-and-dx.md` | Documentation & developer experience | `REQ-DX-*` |
| `release-and-distribution.md` | crates.io publishing, semver, changelog | `REQ-REL-*` |
| `performance-and-benchmark.md` | js-framework-benchmark, peer comparison | `REQ-PERF-*` |
| `release-bar.md` | Consolidated release bar (`BAR-FERRIC-*`) | (consolidation) |
| `release-plan.md` | Ordered epics + traceable backlog | (planning) |

---

## Issue Register (as filed, grouped by epic)

| Epic | # | Title | Stage |
|---|---|---|---|
| Authoring Model (#129) | #138 | Virtual DOM and keyed DOM patching | usable_early |
| Authoring Model (#129) | #139 | `view!` macro surface and compile-time diagnostics | usable_early |
| Authoring Model (#129) | #140 | Component model — props, children, named slots, dynamic dispatch | usable_early |
| Authoring Model (#129) | #141 | Component type-level diagnostics | usable_early |
| Authoring Model (#129) | #142 | Context and dependency injection | usable_early |
| Async/Forms/Events (#130) | #143 | Async resources and suspense | usable_early |
| Async/Forms/Events (#130) | #144 | DOM event handling | usable_early |
| Async/Forms/Events (#130) | #145 | Forms and two-way binding | usable_early |
| Router (#131) | #146 | Core routing — path parameters, nested routes, navigation, links | usable_early |
| Router (#131) | #147 | Active-route awareness | usable_early |
| HTTP Client (#132) | #148 | HTTP methods, JSON bodies, and error handling | usable_early |
| HTTP Client (#132) | #149 | PATCH method, per-request timeout, lean dependency footprint | usable_early |
| SSR + Hydration (#133) | #150 | Server-side HTML rendering and per-request scope isolation | one_oh (must-have) |
| SSR + Hydration (#133) | #151 | Client hydration without re-render (must-have) | one_oh (must-have) |
| SSR + Hydration (#133) | #152 | State carry and async resource resume across the SSR seam | one_oh |
| SSR + Hydration (#133) | #153 | Hydration mismatch detection and Axum integration | one_oh |
| Docs and DX (#134) | #154 | Conceptual guide and start-to-finish tutorial | one_oh |
| Docs and DX (#134) | #155 | API docs and curated examples | one_oh |
| Docs and DX (#134) | #156 | Starter template, reference app, and new-user acceptance path | one_oh |
| Docs and DX (#134) | #157 | README, troubleshooting entry, and CI doc sync | one_oh |
| Performance (#135) | #158 | js-framework-benchmark entry and per-operation results | one_oh |
| Performance (#135) | #159 | Bundle size and dependency footprint | one_oh |
| Performance (#135) | #160 | Peer comparison table and methodology | one_oh |
| Release (#136) | #161 | Publishing readiness — crates.io metadata, licensing, workspace versioning | one_oh |
| Release (#136) | #162 | Semver contract and cargo semver-checks CI enforcement | one_oh |
| Release (#136) | #163 | Changelog — Keep a Changelog 1.1.0 | one_oh |
| Release (#136) | #164 | Versioning and compatibility policy | one_oh |

Also note: Reactive state (#137) is a child issue without a clearly named epic parent in the above — check its
epic assignment during validation.

---

## Task Structure

```
_GLOBAL.md (this document)
├── contracts/_MANIFEST.yaml
├── SUBTASK_review-validate/_BRIEF.md
├── SUBTASK_remediate/_BRIEF.md
└── SUBTASK_synthesize-root/_BRIEF.md
```

### Task Summary

| Task id | Depends on | Description | Output |
|---|---|---|---|
| `SUBTASK_review-validate` | none | Validate all ten design docs, reconcile req registers, check issue traceability | `SUBTASK_review-validate/review-report.md` |
| `SUBTASK_remediate` | `SUBTASK_review-validate` | Apply identified gaps and fixes; confirm PR readiness | `SUBTASK_remediate/remediation-report.md` |
| `SUBTASK_synthesize-root` | `SUBTASK_remediate` | Produce root SYNTHESIS.md; fold parent via engine_resume_suspended | `SYNTHESIS.md` (at this workspace) |

### Dependency Graph

```
SUBTASK_review-validate → SUBTASK_remediate → SUBTASK_synthesize-root
```

---

## Contract

**Contract location**: `contracts/`  
**Contract kind**: `yaml_schema`

Declares the interface between the three spokes so the synthesis task can read the review and remediation
outputs predictably.

---

## Constraints Carried Forward

- **Repository scope**: `Nousix-LLC/nswe-demo` only; GitHub Project #1 (`NSWE Delivery`) only.
- **Work branch**: `work/design-ferric-1_0`; never force-push `main`.
- **GitHub content**: names only repository identities (owner/repo, issue/PR numbers). No host paths, no
  taskflow internals, no attribution trailers.
- **Design, not code**: design documents and backlog items only — no framework code changes.
- **Prior-art**: the `prior-art/` files in this workspace are reference material for comparison; they are
  not what gets committed to the repository.
