# _BRIEF.md — SUBTASK_synthesis

## Task Specification

**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_ac4-path, SUBTASK_cta-link, SUBTASK_annotation
**Status**: Pending

### Objective

This task is a **verification gate**. Read the three concern outputs from the spoke tasks,
verify they satisfy the structural contract (all concerns covered, all citing the pinned
commit), assemble them into `FINDINGS.md` at the parent workspace, write `SYNTHESIS.md`
at the parent workspace (fold record), and fold the parent task SUSPENDED→COMPLETED via
`engine_resume_suspended`.

This task MUST run all four verification checks and MUST NOT substitute a prose summary for
a gate assessment.

### Context

This task is part of the SUBTASK_routing-ctas sub-decomposition.
See `../_GLOBAL.md` for route table, scope, and contract.

**Dependencies**: SUBTASK_ac4-path, SUBTASK_cta-link, SUBTASK_annotation (all must be COMPLETED)
**Dependents**: none — this task folds the parent; the ancestor SUBTASK_synthesis reads FINDINGS.md

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Scope, identities to verify, shared context |
| Local contract | `../contracts/_MANIFEST.yaml` | Structural identities to assert over combined outputs |
| Ancestor contract | The ancestor manifest at `../spoke-ui-states/contracts/_MANIFEST.yaml` relative to the dag root | FINDINGS.md schema (findings_schema section) |
| AC-4 concern output | `../SUBTASK_ac4-path/concern-ac4.md` | AC-4 path analysis |
| CTA link concern output | `../SUBTASK_cta-link/concern-cta.md` | CTA link analysis |
| Annotation concern output | `../SUBTASK_annotation/concern-annotation.md` | Annotation analysis |

Ancestor contract absolute path:
`/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-chirp-logged-out-r1/spoke-ui-states/contracts/_MANIFEST.yaml`

---

## Process Specification (four-check verification gate)

This synthesis task runs the four-check gate. If any check fails, record the violation in
SYNTHESIS.md and report `status="failed"`. If all checks pass, assemble FINDINGS.md.

**Check 1 — Behavioral-contract verification**: Do the three concern outputs each address
their assigned concern from `../_GLOBAL.md` Scope? Are all three concerns represented?

**Check 2 — Wiring verification**: Are all three concern output files present and readable?
Does each produce a finding or clean item in the shape declared by `../contracts/_MANIFEST.yaml`?

**Check 3 — Duplication detection**: Does any concern appear in more than one spoke output?
(Each spoke covers exactly one concern; overlap is a violation.)

**Check 4 — Synthesis code review**: Are the concern outputs well-formed? Does each cite
file + line at pinned commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`? Are severity labels
`blocker` or `non-blocking` as required?

If all four checks pass, assemble FINDINGS.md following the ancestor schema:

```markdown
# Findings — routing-ctas review

## Concerns checked
- AC-4 remaining (sign-in-to-sign-up path and usable sign-up): [one-line summary]
- CTA link correctness (compose.rs link("/compose", ...)): [one-line summary]
- Route annotation anomaly (/sign-in alias "for AC-3" comment): [one-line summary]

## Findings
[List of findings with location, principle, rationale, severity, resolution.
If none: "None — all three concerns checked clean."]

## Clean items
[For each concern that passed: what was examined and what was found]
```

After assembling FINDINGS.md, write SYNTHESIS.md at the parent workspace documenting the
gate result (what was checked, what passed, what (if any) was noted).

**Terminal sequence**:
1. Write `FINDINGS.md` to parent workspace (absolute path below).
2. Write `SYNTHESIS.md` to parent workspace (absolute path below).
3. Call `engine_report_status { status: "completed", decompose_evaluation: "Atomic",
   outputs: ["<parent_workspace>/FINDINGS.md"],
   artifact_path: "<parent_workspace>/SYNTHESIS.md" }`.
4. Call `engine_resume_suspended { target_task_id: <parent_task_id>,
   synthesized_task_id: <this_task_id>,
   seam_path: "<parent_workspace>/SYNTHESIS.md" }`.

The `engine_resume_suspended` call folds the parent SUBTASK_routing-ctas SUSPENDED→COMPLETED,
unblocking the ancestor SUBTASK_synthesis which reads `SUBTASK_routing-ctas/FINDINGS.md`.

Parent task id: resolve at dispatch from the DAG (the SUSPENDED task one level up).
Parent workspace (absolute):
`/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-chirp-logged-out-r1/spoke-ui-states/SUBTASK_routing-ctas`

---

## Output Specification

Both output files MUST be written to the **parent workspace** (one level up from this workspace):

| Artifact | Absolute path | Description |
|----------|--------------|-------------|
| `FINDINGS.md` | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-chirp-logged-out-r1/spoke-ui-states/SUBTASK_routing-ctas/FINDINGS.md` | Declared output of the parent task; read by ancestor SUBTASK_synthesis |
| `SYNTHESIS.md` | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-chirp-logged-out-r1/spoke-ui-states/SUBTASK_routing-ctas/SYNTHESIS.md` | Fold record; this task's terminal artifact |

Do NOT write FINDINGS.md or SYNTHESIS.md to this workspace (SUBTASK_synthesis/) — they must
be at the parent workspace for the fold and for the ancestor synthesis to find them.

---

## Success Criteria

- [ ] All three concern outputs read and verified against the contract (four checks run)
- [ ] Gate passes or violation is documented in SYNTHESIS.md (no silent pass)
- [ ] `FINDINGS.md` written to parent workspace following the ancestor schema
- [ ] `SYNTHESIS.md` written to parent workspace (fold record)
- [ ] `engine_resume_suspended` called — parent SUBTASK_routing-ctas folded SUSPENDED→COMPLETED

---

## Suggested Methodology Files

**Task-type row matched**: Synthesizing / verifying a hub-and-spoke decomposition → Primary: `synthesis`

- `synthesis/Synthesis_Overview_Methodology.md` — always load first; defines the four-check
  gate model and the go/no-go decision this task embodies
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — Check 1: verify behavioral
  contracts are covered
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — Check 2: verify all wires complete
- `synthesis/Synthesis_Code_Review_Methodology.md` — Check 4: review combined output quality

The above are the parent's flagged suggestions. The gate posture (run checks, do not summarize)
is prescribed; which specific files to load and how deeply to run each check is this agent's
judgment. Load fewer if a check is clearly inapplicable; load more if the subtree shape reveals
additional needs.

## Inherited Constraints

- Repository: `Nousix-LLC/nswe-demo` only
- Pinned commit: `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Do not post to the PR
- Write FINDINGS.md and SYNTHESIS.md to the PARENT workspace, not this workspace
- FINDINGS.md MUST follow the ancestor schema (findings_schema in spoke-ui-states contracts)
- Do not investigate landing.rs concerns or any concern outside the three assigned here

## Out-of-Scope Methodologies

- `synthesis/Synthesis_Remediation_Methodology.md` — not needed unless the gate fails and
  additional fix tasks must be injected; load it then
- `code-review/CodeReview_PR_Authoring_Methodology.md` — not applicable; this task does not
  author PRs
