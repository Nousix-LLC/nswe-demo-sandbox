# Task: Ferric 1.0 Design — Review and Validation

## Task Specification

**Slug**: SUBTASK_review-validate
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-designer

### Objective

Read and validate the complete Ferric 1.0 design on branch `work/design-ferric-1_0` of
`Nousix-LLC/nswe-demo`. Confirm that all nine concern areas are covered with consistent,
accurate, internally coherent requirements; reconcile the requirement registers; and check
that the filed issues (#129–#164) trace back to those requirements. Produce a structured
review report that SUBTASK_remediate can act on.

### Context

This task is part of the design-ferric-1_0-r2 recovery DAG (see `_GLOBAL.md` in the parent workspace).

The prior run of the design DAG produced all ten design documents, filed all the issues, and opened PR #128.
The root synthesis was never produced, leaving the design unverified and the DAG frozen. This task does
the verification pass the prior run skipped, so the synthesis can proceed on solid ground.

**Dependencies**: none — reads the branch and live repo as given.  
**Dependents**: SUBTASK_remediate (reads this task's review report).

---

## Inputs

| Input | Location | Purpose |
|---|---|---|
| Design documents (all 10) | `design/ferric/` on branch `work/design-ferric-1_0` | Primary subject of validation |
| Design contracts | `design/ferric/contracts/` on same branch | Traceability schema and artifact map |
| Ferric codebase | `crates/ferric/` on `main` (HEAD `276138f`) | Ground truth for accuracy checks |
| Filed epics | GitHub issues #129–#136, `Nousix-LLC/nswe-demo` | Epic completeness check |
| Filed child issues | GitHub issues #137–#164, `Nousix-LLC/nswe-demo` | Traceability check |
| PR | #128, `Nousix-LLC/nswe-demo` | PR description completeness |
| Prior-art spoke outputs | `../prior-art/` (this workspace's parent) | Reference for carried-forward concerns |
| Contract schema | `../contracts/_MANIFEST.yaml` | Governs what this report must contain |

---

## What to Validate

For each of the nine concern areas:

1. **Framework scope & 1.0 requirements** (`scope-and-requirements.md`, `REQ-FW-*`)
   - Requirements are stated as testable conditions a stranger can check
   - The MVP-vs-1.0 line is clear and the out-of-1.0 items are explicitly listed
   - Cross-references to other REQ registers are accurate
   - Compare against `../prior-art/` as needed (no prior art for this concern — it was designed fresh)

2. **SSR + hydration** (`ssr-hydration.md`, `REQ-SSR-*`)
   - Architecture is grounded in the actual `crates/ferric` code at commit `276138f`
   - The "no client-side re-render on hydration" bar is stated as a testable acceptance criterion
   - State carry and async resource resume are addressed
   - No prior art — check freshness and completeness

3. **Authoring model** (`authoring-model.md`, `REQ-API-*`)
   - Check against `../prior-art/authoring-model.md` — confirm the branch version reconciles that draft
   - The `view!` macro, props, children, slots, and context are each given testable requirements

4. **Async, forms, and events** (`async-forms-events.md`, `REQ-ASYNC-*`)
   - Check against `../prior-art/async-forms-events.md` — confirm the branch version reconciles that draft
   - Async resources, suspense-style loading/error, two-way binding, and full DOM events are each addressed

5. **Router + HTTP/JSON client** (`router-and-http.md`, `REQ-RT-*`, `REQ-HTTP-*`)
   - Check against `../prior-art/router-and-http.md` and its SYNTHESIS.md
   - The additive-over-#5/#6 stance: confirm the branch version supersedes the landed surfaces without
     duplicating them
   - Nested routes, route params, active-link, typed JSON, timeouts are addressed

6. **Documentation & developer experience** (`docs-and-dx.md`, `REQ-DX-*`)
   - No prior art — check freshness and completeness
   - Guide, tutorial, API docs, cargo-generate starter template, and DX bar each stated

7. **Release & distribution** (`release-and-distribution.md`, `REQ-REL-*`)
   - Check against `../prior-art/release-and-distribution.md`
   - crates.io metadata, semver policy, changelog, multi-crate versioning

8. **Performance & benchmark** (`performance-and-benchmark.md`, `REQ-PERF-*`)
   - No prior art — check freshness and completeness
   - js-framework-benchmark entry, honest peer comparison, methodology

9. **The plan** (`release-bar.md` + `release-plan.md`)
   - `release-bar.md`: every `BAR-FERRIC-*` criterion cites at least one `REQ-*` id
   - `release-plan.md`: ordered epics + issues, tracing to requirements
   - The `usable_early` / `one_oh` staging is internally consistent across documents

### Requirement register reconciliation

- Confirm no `REQ-*` id appears in more than one register owner
- Confirm every `REQ-*` id cited in a cross-reference actually exists in its owning document
- Confirm `release-bar.md`'s `BAR-FERRIC-*` criteria each cite at least one `REQ-*` that exists

### Issue traceability

- For each epic (#129–#136): read its body and check it references the relevant design document and requirement IDs
- For each child issue (#137–#164): check the body contains at least one `REQ-*` citation
- Flag any issue whose body lacks a clear requirement reference
- Flag any significant `REQ-*` requirement that has no corresponding issue
- Check issue #137 (Reactive state): confirm its epic assignment and whether it's correctly scoped

---

## Output

| Attribute | Value |
|---|---|
| Filename | `review-report.md` |
| Location | `SUBTASK_review-validate/` (this workspace) |
| Format | Markdown, structured per `../contracts/_MANIFEST.yaml` §review_report_schema |

The report must contain these sections (per the contract schema):
- `validation_summary` — one-paragraph verdict
- `per_concern_findings` — nine concerns, each with status and specific issues
- `req_register_reconciliation` — cross-reference check
- `issue_traceability` — per epic, per issue
- `gaps_for_remediation` — prioritized `GAP-NNN` list for SUBTASK_remediate

---

## Success Criteria

- [ ] All ten design documents read and assessed
- [ ] All nine concern areas covered in per-concern findings
- [ ] REQ register reconciliation complete (no orphaned or duplicate IDs found, or all flagged)
- [ ] All 36 issues (8 epics + 28 child) checked for traceability
- [ ] `review-report.md` written with all required sections
- [ ] Every gap identified is assigned a `GAP-NNN` id and a severity
