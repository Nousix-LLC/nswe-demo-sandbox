# Review-Validate Subtree Hub

## Context

**Status**: Active  
**Part of**: design-ferric-1_0-r2 recovery DAG  
**Purpose**: Validate the Ferric 1.0 design on branch `work/design-ferric-1_0` and produce `review-report.md`
for SUBTASK_remediate to act on.

### Objective

Nine per-concern validators read the design documents on `work/design-ferric-1_0` in parallel and each
produce a structured `concern-findings.md`. A cross-reference validator then reads all nine findings plus
the live GitHub issues (#129–#164) to produce `crossrefs-findings.md`. The synthesis task assembles all
outputs into the final `review-report.md` conforming to the parent contract schema.

### Success Criteria

- [ ] All nine concern areas validated; each produces concern-findings.md
- [ ] REQ-* register cross-references checked; all 36 issues checked for traceability
- [ ] `review-report.md` written at `SUBTASK_review-validate/review-report.md` with all five required sections

---

## Design Document Register (on branch `work/design-ferric-1_0`)

| File (in `design/ferric/`) | Concern | REQ register | Validator task |
|---|---|---|---|
| `scope-and-requirements.md` | Framework scope & 1.0 requirements | `REQ-FW-*` | `SUBTASK_validate-scope` |
| `ssr-hydration.md` | SSR + hydration | `REQ-SSR-*` | `SUBTASK_validate-ssr` |
| `authoring-model.md` | view! macro, props, children, slots, context | `REQ-API-*` | `SUBTASK_validate-authoring` |
| `async-forms-events.md` | Async resources, forms, DOM events | `REQ-ASYNC-*` | `SUBTASK_validate-async` |
| `router-and-http.md` | Router + HTTP/JSON client | `REQ-RT-*`, `REQ-HTTP-*` | `SUBTASK_validate-router` |
| `docs-and-dx.md` | Documentation & developer experience | `REQ-DX-*` | `SUBTASK_validate-docs` |
| `release-and-distribution.md` | crates.io publishing, semver, changelog | `REQ-REL-*` | `SUBTASK_validate-release` |
| `performance-and-benchmark.md` | js-framework-benchmark, peer comparison | `REQ-PERF-*` | `SUBTASK_validate-perf` |
| `release-bar.md` + `release-plan.md` | Consolidated bar + ordered plan | (consolidation) | `SUBTASK_validate-plan` |

---

## Key Inputs Shared Across All Tasks

| Resource | Location | Notes |
|---|---|---|
| Design documents | `design/ferric/` on branch `work/design-ferric-1_0` at `/home/user/nswe-demo` | Use `git show work/design-ferric-1_0:design/ferric/<file>` |
| Design contracts | `design/ferric/contracts/` on same branch | |
| Prior-art | `../prior-art/` (parent workspace) | authoring-model.md, async-forms-events.md, router-and-http.md, release-and-distribution.md, router-and-http.SYNTHESIS.md |
| Ferric codebase | `crates/ferric/` on `main` (HEAD `276138f`) at `/home/user/nswe-demo` | Only needed by SUBTASK_validate-ssr |
| GitHub repo | `Nousix-LLC/nswe-demo` via `gh` | Issues #129–#136 (epics), #137–#164 (child issues) |

---

## Task Structure

```
_GLOBAL.md (this document)
├── contracts/_MANIFEST.yaml
├── SUBTASK_validate-scope/_BRIEF.md       (reads scope-and-requirements.md)
├── SUBTASK_validate-ssr/_BRIEF.md         (reads ssr-hydration.md + codebase)
├── SUBTASK_validate-authoring/_BRIEF.md   (reads authoring-model.md + prior-art)
├── SUBTASK_validate-async/_BRIEF.md       (reads async-forms-events.md + prior-art)
├── SUBTASK_validate-router/_BRIEF.md      (reads router-and-http.md + prior-art)
├── SUBTASK_validate-docs/_BRIEF.md        (reads docs-and-dx.md)
├── SUBTASK_validate-release/_BRIEF.md     (reads release-and-distribution.md + prior-art)
├── SUBTASK_validate-perf/_BRIEF.md        (reads performance-and-benchmark.md)
├── SUBTASK_validate-plan/_BRIEF.md        (reads release-bar.md + release-plan.md)
├── SUBTASK_validate-crossrefs/_BRIEF.md   (reads all 9 findings + GitHub issues)
└── SUBTASK_synthesis/_BRIEF.md            (reads all 10 findings → review-report.md)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---|---|---|---|
| `SUBTASK_validate-scope` | none | Validate scope-and-requirements.md (REQ-FW-*) | `SUBTASK_validate-scope/concern-findings.md` |
| `SUBTASK_validate-ssr` | none | Validate ssr-hydration.md (REQ-SSR-*) | `SUBTASK_validate-ssr/concern-findings.md` |
| `SUBTASK_validate-authoring` | none | Validate authoring-model.md (REQ-API-*) | `SUBTASK_validate-authoring/concern-findings.md` |
| `SUBTASK_validate-async` | none | Validate async-forms-events.md (REQ-ASYNC-*) | `SUBTASK_validate-async/concern-findings.md` |
| `SUBTASK_validate-router` | none | Validate router-and-http.md (REQ-RT-*, REQ-HTTP-*) | `SUBTASK_validate-router/concern-findings.md` |
| `SUBTASK_validate-docs` | none | Validate docs-and-dx.md (REQ-DX-*) | `SUBTASK_validate-docs/concern-findings.md` |
| `SUBTASK_validate-release` | none | Validate release-and-distribution.md (REQ-REL-*) | `SUBTASK_validate-release/concern-findings.md` |
| `SUBTASK_validate-perf` | none | Validate performance-and-benchmark.md (REQ-PERF-*) | `SUBTASK_validate-perf/concern-findings.md` |
| `SUBTASK_validate-plan` | none | Validate release-bar.md + release-plan.md | `SUBTASK_validate-plan/concern-findings.md` |
| `SUBTASK_validate-crossrefs` | `SUBTASK_validate-scope`, `SUBTASK_validate-ssr`, `SUBTASK_validate-authoring`, `SUBTASK_validate-async`, `SUBTASK_validate-router`, `SUBTASK_validate-docs`, `SUBTASK_validate-release`, `SUBTASK_validate-perf`, `SUBTASK_validate-plan` | REQ id cross-reference check + GitHub issue traceability | `SUBTASK_validate-crossrefs/crossrefs-findings.md` |
| `SUBTASK_synthesis` | `SUBTASK_validate-crossrefs` | Assemble review-report.md from all findings | `review-report.md` (at this workspace) |

### Dependency Graph

```
SUBTASK_validate-scope     ──┐
SUBTASK_validate-ssr       ──┤
SUBTASK_validate-authoring ──┤
SUBTASK_validate-async     ──┤
SUBTASK_validate-router    ──┼──> SUBTASK_validate-crossrefs ──> SUBTASK_synthesis
SUBTASK_validate-docs      ──┤
SUBTASK_validate-release   ──┤
SUBTASK_validate-perf      ──┤
SUBTASK_validate-plan      ──┘
```

---

## Contract

**Contract location**: `contracts/`  
**Contract kind**: `yaml_schema`

Declares the concern-findings schema that each validator must produce, so validate-crossrefs and synthesis
can consume them predictably.
