# Task: Ferric Survey Synthesis

## Task Specification

**Slug**: SUBTASK_ferric-survey-synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_ferric-async-survey, SUBTASK_ferric-router-survey, SUBTASK_ferric-ssr-survey
**Status**: Pending
**Assigned To**: swe-coder

### Objective

Read the three API notes files produced by the spoke tasks, plus the crate structure of `crates/ferric/`, and assemble the complete `ferric-survey.md` document. Verify that all contract identities hold, then write `ferric-survey.md` and `SYNTHESIS.md` at the parent workspace (`../`), and fold the parent task to COMPLETED.

### Context

This task is the synthesis/verification gate for the Ferric Framework Survey subtree. See `../_GLOBAL.md` for subtree context. The parent task `SUBTASK_explore-survey-ferric` is SUSPENDED and will be folded to COMPLETED by this task via `engine_resume_suspended`.

**This is a verification gate, not a prose summary.** Before writing `ferric-survey.md`, this task MUST:
1. Verify that each notes file contains the required sections (per `../contracts/notes-schema.yaml`)
2. Verify that each notes file contains at least one Rust type signature
3. Check that source locations reference actual `crates/ferric/` paths
4. Verify that the assembled ferric-survey.md will cover all 6 sections required by the grandparent brief

If any verification fails, record the failure in `SYNTHESIS.md` and report `status="failed"` rather than producing a deficient survey.

**Dependents**: None (this is the terminal task; it folds the SUSPENDED parent).

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Constraints, contract reference, output location |
| Contract manifest | `../contracts/_MANIFEST.yaml` | Ownership and identities to verify |
| Contract schema | `../contracts/notes-schema.yaml` | Expected sections in each notes file |
| Async notes | `../SUBTASK_ferric-async-survey/ferric-async-notes.md` | PR #193 API documentation |
| Router notes | `../SUBTASK_ferric-router-survey/ferric-router-notes.md` | PR #203 API documentation |
| SSR notes | `../SUBTASK_ferric-ssr-survey/ferric-ssr-notes.md` | PR #228 API documentation |
| Ferric crate structure | `crates/ferric/` in `Nousix-LLC/nswe-demo` | For crate layout (Section 1) and gap identification (Section 6) |

**Accessing the codebase**: Use `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/` for the crate structure, and `gh api repos/Nousix-LLC/nswe-demo/contents/crates/ferric/Cargo.toml` and `crates/ferric/src/lib.rs` for the top-level API surface and feature flags.

---

## Verification Gate (run before assembling the survey)

Apply these checks. If any FAIL, do not produce a deficient survey — report failure.

- [ ] **Identity: signatures_present** — Each notes file contains at least one fenced Rust code block with a type or function signature
- [ ] **Identity: state_model_present** — Each notes file has a "State Model" section (or explicit note that none applies)
- [ ] **Identity: source_locations_valid** — Each notes file references at least one `crates/ferric/` path
- [ ] **Identity: survey_completeness** — The assembled document will cover all 6 sections from the grandparent brief
- [ ] **Ownership coverage** — All artifacts declared in `../contracts/_MANIFEST.yaml` are present before assembly

---

## Output Specification

### Primary Outputs

| Attribute | Value |
|-----------|-------|
| Survey | `ferric-survey.md` at `../` (parent workspace) |
| Fold record | `SYNTHESIS.md` at `../` (parent workspace = fold location) |

### ferric-survey.md Structure

MUST include all 6 sections from the grandparent brief (`../../_BRIEF.md` via SUBTASK_explore-survey-ferric/_BRIEF.md):

1. **Crate Structure** — Top-level file layout of `crates/ferric/`; module organization; re-exported public API surface. (Read `lib.rs` and directory listing from the repo.)

2. **Async Resource Primitives** (from PR #193) — Assembled from `ferric-async-notes.md`. For each primitive: name and type signature, loading/error/data state model, how to create and consume in a component.

3. **Router API** (from PR #203) — Assembled from `ferric-router-notes.md`. Route declaration, navigation API, not-found/redirect handling.

4. **SSR and Hydration** (from PR #228) — Assembled from `ferric-ssr-notes.md`. What `render_to_string` or equivalent provides, how client-side hydration is initiated, Axum integration point.

5. **Component Pattern** — The idiomatic pattern for a component that:
   - Triggers an async fetch on mount
   - Shows a loading indicator while pending
   - Shows an error state with recovery option on failure
   - Shows content when resolved
   - Shows an empty/end-of-list state when the response is empty
   
   This section synthesizes knowledge from the async resource and router notes. It MUST be written as a concrete Rust code example (using whatever Ferric syntax the notes reveal), not just prose.

6. **Gaps or Limitations** — Any capability the frontend task will need that is NOT yet in the framework, requiring a workaround or fallback. Cross-reference the notes files' "Notable Limitations" sections and the grandparent brief's requirements.

### SYNTHESIS.md Structure

The fold record MUST include:
- Verification results (pass/fail for each identity)
- Summary of what was assembled
- Any deviations from the notes (content added from direct codebase reading, e.g. for the crate structure section)

---

## Success Criteria

- [ ] All contract identities verified (pass or documented failure)
- [ ] `ferric-survey.md` written at `../ferric-survey.md` covering all 6 sections
- [ ] `SYNTHESIS.md` written at `../SYNTHESIS.md` with verification results
- [ ] `engine_resume_suspended` called to fold the parent task `SUBTASK_explore-survey-ferric`

---

## Suggested Methodology Files

**Task-type row matched**: "Synthesizing / verifying a hub-and-spoke decomposition" → Synthesis + Code Review + Code Quality

**Primary files to load**:
- `synthesis/Synthesis_Overview_Methodology.md` — rationale: this is a verification gate task; the overview defines the four-check model and the gate pass/fail decision
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — rationale: verifies that each spoke's output satisfies the declared contract (notes schema + ownership manifest)
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — rationale: verifies that all three notes files are wired into the survey document and no spoke output is dead/unused
- `framework-design/FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` — rationale: needed to write the Component Pattern section (Section 5), which synthesizes knowledge from all three PR areas into an idiomatic four-state Ferric component

The above are the parent's flagged methodologies. The child agent SHOULD load these as a starting point but is the final judge of what its work requires.

## Inherited Constraints

- Exploration only — no code changes
- Repository: `Nousix-LLC/nswe-demo`; codebase on `main` at `cb1ced3`
- No host paths, internal addresses, or taskflow references in output documents
- `ferric-survey.md` and `SYNTHESIS.md` MUST be written at `../` (the parent workspace, the fold location)

## Out-of-Scope Methodologies

- Testing methodologies — this task writes no tests
- Decomposition methodologies — this is a synthesis gate, not a decomposition
