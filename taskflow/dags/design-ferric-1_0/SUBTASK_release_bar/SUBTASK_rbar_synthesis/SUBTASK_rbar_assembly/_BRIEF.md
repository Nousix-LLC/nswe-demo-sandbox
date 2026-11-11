# Task: Ferric 1.0 Release Bar — synthesis: criteria, assembly, and fold

## Task Specification

**Slug**: SUBTASK_rbar_assembly
**Task Kind**: synthesis
**Depends on**: none
**Status**: Pending

### Objective

Read the sibling's complete gap analysis and the 8 spoke design documents. Write the complete `BAR-FERRIC-*`
criteria register. Assemble `release-bar.md` (five sections). Verify identities IA, IB, I2, I3, I4, I5. Pass
the avoid-ai-writing check. Write the three declared outputs. Fold SUBTASK_release_bar, then fold
SUBTASK_rbar_synthesis.

This is the synthesis task for SUBTASK_rbar_synthesis. It also carries the fold responsibility for
SUBTASK_release_bar that the original SUBTASK_rbar_synthesis brief assigned (writing SYNTHESIS.md at the
SUBTASK_release_bar workspace root and calling `engine_resume_suspended` for that task).

The sibling `SUBTASK_rbar_gap_review` produced a complete gap analysis at
`../../../SUBTASK_rbar_gap_review/gap-analysis.md`. Use that as the primary surface-coverage input for
writing criteria and the gap review section. SUBTASK_rbar_gap is running concurrently and may produce
`../SUBTASK_rbar_gap/gap-analysis-internal.md`; use it as a cross-check if readable, skip if not yet present.

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Context, identity table, output locations |
| Subtree contract | `../contracts/_MANIFEST.yaml` | Identity assertions, format schemas |
| Parent contract | `../../../contracts/id_and_traceability_schema.yaml` | BAR-FERRIC-* schema, trace rules, verification vocabulary |
| Parent manifest | `../../../contracts/_MANIFEST.yaml` | Identity definitions IA/IB/I2/I3/I4/I5 |
| Sibling gap analysis | `../../../SUBTASK_rbar_gap_review/gap-analysis.md` | **Primary** surface-coverage input |
| Concurrent gap analysis | `../SUBTASK_rbar_gap/gap-analysis-internal.md` | Cross-check if readable; skip if absent |
| Scope + requirements | `../../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | REQ-FW-* register; staging principle (§5); out-of-1.0 list (§6) |
| SSR/hydration design | `../../../SUBTASK_ssr_hydration/ssr-hydration.md` | REQ-SSR-* register |
| Authoring model | `../../../SUBTASK_authoring_model/authoring-model.md` | REQ-API-* register |
| Async/forms/events | `../../../SUBTASK_async_forms_events/async-forms-events.md` | REQ-ASYNC-* register |
| Router + HTTP | `../../../SUBTASK_router_and_http/router-and-http.md` | REQ-RT-*, REQ-HTTP-* registers |
| Docs + DX | `../../../SUBTASK_docs_and_dx/docs-and-dx.md` | REQ-DX-* register |
| Release + distribution | `../../../SUBTASK_release_and_distribution/release-and-distribution.md` | REQ-REL-* register |
| Performance + benchmark | `../../../SUBTASK_performance_and_benchmark/performance-and-benchmark.md` | REQ-PERF-* register |

---

## Staging principle (from scope doc §5)

- **`usable_early`**: requirements whose absence makes building a real app impossible — declarative authoring,
  async/suspense, forms/events, routing/HTTP, stable-Rust build, actionable diagnostics.
- **`one_oh`**: requirements that a credible 1.0 of this framework kind must provide — SSR+hydration (the
  gating must-have, `must_have: true`), crates.io publishing, semver/compat policy, complete docs, named-peer
  performance numbers, lean/documented dependencies, the reference app.

---

## BAR-FERRIC-* id assignment

Assign ids sequentially: BAR-FERRIC-001, BAR-FERRIC-002, ... (zero-padded 3-digit). Each id is unique.
Do NOT write criteria for out-of-1.0 surfaces (identity IB/I5). Every criterion must reference ≥1 REQ-* id
that exists in a spoke register (identity I2). Mark SSR+hydration criteria `must_have: true` (identity I4).

---

## release-bar.md structure (five required sections)

1. **Introduction** — what the bar is, what it is for, how to read it
2. **Staging principle** — the `usable_early` / `one_oh` cut; why SSR+hydration is the gating must-have;
   what separates usable-early from full 1.0
3. **BAR-FERRIC-* criteria** — complete list organized by capability area; must_have criteria marked; each
   criterion: id, statement, references, verification_method, stage
4. **Coverage map** — REQ-* → BAR-FERRIC-* table for all one_oh-gating requirements (identity I3)
5. **Completeness and gap review** — the surface table (surface | status | REQ-refs | notes); out-of-1.0
   items explicitly named with their recorded reason; any gaps noted

---

## Identity verification (assert all; record FAILED if any fails — do not silently adjust)

- **IA**: every covered surface has ≥1 BAR-FERRIC-* with references to its REQ-* ids
- **IB**: every out-of-1.0 surface is enforced by no BAR-FERRIC-*
- **I2**: every BAR-FERRIC-* references ≥1 REQ-* id that exists in a spoke register
- **I3**: every one_oh / release_gating=true REQ-* is referenced by ≥1 BAR-FERRIC-*
- **I4**: ≥1 one_oh BAR-FERRIC-* marks SSR+hydration must_have: true
- **I5**: the four named out-of-1.0 items appear with status=out-of-1.0 and are enforced by no BAR-FERRIC-*

---

## Avoid-ai-writing pass

Before finalizing release-bar.md, review all narrative content for the writing-voice rules:
- No moral character adjective on an abstract noun ("honest product health", "genuine reliability")
- No self-narrating candor ("stated plainly", "to be honest", "the reality is")
- No slot-fill templates ("a robust step toward", "whether you're X or Y")
- No hollow filler ("seamless", "robust", "comprehensive", "leverage", "utilize")
Fix any flagged tells before writing the file.

---

## Declared outputs

- `../../release-bar.md` — the final release bar document at the SUBTASK_release_bar workspace root
  (repo target `design/ferric/release-bar.md`)
- `../../SYNTHESIS.md` — fold record for SUBTASK_release_bar
- `../SYNTHESIS.md` — fold record for SUBTASK_rbar_synthesis; this task's terminal record

### SYNTHESIS.md content

Both SYNTHESIS.md files should carry:
- Identity verification results: IA, IB, I2, I3, I4, I5 — each `passed` or `FAILED: <finding>`
- Summary: total BAR-FERRIC-* count, usable_early / one_oh split, must-have criterion IDs,
  out-of-1.0 surface count, gap count
- Declared output paths confirmed

---

## Fold sequence

After writing all output files:

1. Write `../../release-bar.md`
2. Write `../../SYNTHESIS.md` (fold record for SUBTASK_release_bar)
3. Write `../SYNTHESIS.md` (fold record for SUBTASK_rbar_synthesis; this task's terminal record)
4. Call `engine_report_status { status: "completed", artifact_path: "<abs-path>/SUBTASK_rbar_synthesis/SYNTHESIS.md", outputs: ["<abs-path>/release-bar.md", "<abs-path>/SUBTASK_release_bar/SYNTHESIS.md", "<abs-path>/SUBTASK_rbar_synthesis/SYNTHESIS.md"] }`
5. Call `engine_resume_suspended { target_task_id: "SUBTASK_release_bar", synthesized_task_id: "SUBTASK_rbar_assembly", seam_path: "<abs-path>/SUBTASK_release_bar/SYNTHESIS.md" }`
6. Call `engine_resume_suspended { target_task_id: "SUBTASK_rbar_synthesis", synthesized_task_id: "SUBTASK_rbar_assembly", seam_path: "<abs-path>/SUBTASK_rbar_synthesis/SYNTHESIS.md" }`

Replace `<abs-path>` with the correct absolute paths; use the SUBTASK_release_bar root at:
`/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-ferric-1_0/SUBTASK_release_bar/`

---

## Success criteria

- [ ] All five sections of release-bar.md are present and complete
- [ ] Every covered surface from the gap analysis has a BAR-FERRIC-* criterion (identity IA)
- [ ] No criterion references an out-of-1.0 surface (identity IB)
- [ ] Every criterion references ≥1 real REQ-* id (identity I2)
- [ ] Coverage map covers every one_oh / release_gating=true REQ-* (identity I3)
- [ ] ≥1 one_oh criterion marks SSR+hydration must_have: true (identity I4)
- [ ] All four named out-of-1.0 items appear in the gap section (identity I5)
- [ ] release-bar.md passes the avoid-ai-writing pass
- [ ] release-bar.md is written at `../../release-bar.md`
- [ ] Both SYNTHESIS.md files are written; both engine_resume_suspended calls are made
- [ ] Any failed identity is recorded in SYNTHESIS.md; no silent adjustment

### Constraints

- Own the BAR-FERRIC-* namespace; do not create or modify any REQ-*
- Every statement in release-bar.md must be checkable — not aspirational
- Report any failed identity assertion in SYNTHESIS.md; do not silently adjust outputs to force a pass
- Honor the writing-voice rules for all narrative content
