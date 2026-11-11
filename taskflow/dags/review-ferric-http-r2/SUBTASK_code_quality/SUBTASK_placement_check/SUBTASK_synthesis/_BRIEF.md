# SUBTASK_synthesis: Placement-Check Synthesis Gate

## Task Specification

**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_placement_analysis, SUBTASK_duplication_analysis
**Status**: Pending

### Objective

This is the synthesis and verification gate for the SUBTASK_placement_check decomposition.
It is NOT a prose summary. It:

1. Verifies all four gate checks pass (see Gate Checks below)
2. Combines findings from both sub-spokes into `placement_review_partial.md` following
   `../contracts/spoke_partial_schema.yaml`
3. Authors `SYNTHESIS.md` at the SUBTASK_placement_check workspace root (the fold location)
4. Calls `engine_resume_suspended` to fold the parent (SUBTASK_placement_check)
   SUSPENDED→COMPLETED

If any gate check fails, this task records the failure in `SYNTHESIS.md` and reports
`status="failed"` — it MUST NOT silently plug a gate failure.

### Context

Synthesis gate of SUBTASK_placement_check in SUBTASK_code_quality / review-ferric-http-r2.
See `../_GLOBAL.md` for subtree constraints.

**Parent workspace**: `../` (the SUBTASK_placement_check directory)
**Fold record location**: `../SYNTHESIS.md`

---

## Input Specification

| Input | Source |
|-------|--------|
| Placement findings | `../SUBTASK_placement_analysis/placement_findings.md` |
| Duplication findings | `../SUBTASK_duplication_analysis/duplication_findings.md` |
| Subtree hub | `../_GLOBAL.md` |
| Parent partial schema | `../contracts/spoke_partial_schema.yaml` |
| Ownership manifest | `../contracts/_MANIFEST.yaml` |

---

## Gate Checks (Four-Check Model — MUST all pass)

**Check 1 — Ownership coverage**: Both `placement_findings.md` and `duplication_findings.md`
exist and are non-empty. If either is missing or empty, FAIL.

**Check 2 — Contract wiring**: The `placement_review_partial.md` to be produced will cover
Concern 2 AND Concern 3. Both appear in `## Concerns Covered`. If either is absent, FAIL.

**Check 3 — No duplication or contradiction in combined output**: No finding from the
sub-spokes appears twice in `placement_review_partial.md`. No finding contradicts another.
If violations found, FAIL.

**Check 4 — Conformance to parent schema**: `placement_review_partial.md` has all three
required sections (`## Concerns Covered`, `## Summary`, `## Findings`) per
`../contracts/spoke_partial_schema.yaml`. If any section is missing, FAIL.

On any FAIL: author `../SYNTHESIS.md` recording the failure, report `status="failed"`.
Do NOT silently plug a failure or proceed as if it passed.

---

## Output Specification

**Primary output**: `../placement_review_partial.md`
  Shape (per `../contracts/spoke_partial_schema.yaml`):
  ```
  ## Concerns Covered
  - Concern 2 (placement correctness)
  - Concern 3 (duplication)

  ## Summary
  [One paragraph: what was checked, overall result — clean / N findings raised]

  ## Findings
  [Combined findings from both sub-spokes, using severity: BLOCKER | SHOULD_FIX | ADVISORY | CLEAN]
  ```

**Fold record**: `../SYNTHESIS.md`
  Content: gate check results, what was verified, the combined findings verdict, any
  failures encountered.

After producing outputs, this task MUST:
1. Write `../SYNTHESIS.md` (fold record at parent workspace)
2. Write `../placement_review_partial.md`
3. Report `status="completed"`, `artifact_path="../SYNTHESIS.md"`,
   `outputs=["../placement_review_partial.md", "../SYNTHESIS.md"]`
4. Call `engine_resume_suspended` with:
   - `target_task_id`: the task ID for SUBTASK_placement_check (available in dispatch context)
   - `synthesized_task_id`: this task's own ID (available in dispatch context)
   - `seam_path`: absolute path to `../SYNTHESIS.md`

---

## Success Criteria

- [ ] All four gate checks pass
- [ ] `../placement_review_partial.md` written following `../contracts/spoke_partial_schema.yaml`
- [ ] Every finding from placement_findings.md and duplication_findings.md appears
      in placement_review_partial.md
- [ ] `../SYNTHESIS.md` written at parent workspace (fold location)
- [ ] `engine_resume_suspended` called successfully to fold parent SUSPENDED→COMPLETED

---

## Suggested Methodology Files

**Task-type row (from Domain Mapping):** "Synthesizing / verifying a hub-and-spoke
decomposition" — Primary: Synthesis; Supporting: Code Review, Code Quality

Suggested files:
- `synthesis/Synthesis_Overview_Methodology.md` — the four-check model; ALWAYS load first
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify behavioral contracts
  are satisfied across combined outputs
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — verify all outputs are wired
  and no detached findings
- `synthesis/Synthesis_Duplication_Detection_Methodology.md` — detect duplications in
  combined output
- `synthesis/Synthesis_Code_Review_Methodology.md` — synthesis-level code review gate

The above are the parent's flagged methodologies. The synthesis agent SHOULD load
Synthesis_Overview_Methodology.md first (always), then the sibling check/remediation files
its own reading of the subtree reveals it needs. These are suggestions; the synthesis agent
is the final judge of coverage depth.

## Out-of-Scope Methodologies

- `decomposition/` bundle — synthesis is reassembly, not a split
- Rust-specific methodologies — out of scope for this subtree

---

## Inherited Constraints

- Repo: `Nousix-LLC/nswe-demo`
- Do not expose server addresses, SSH key paths, user names, or internal host paths
  in any artifact
- Rust/signature correctness and security: out of scope
- This task is the gate: a FAIL here means placement_review_partial.md is NOT written
  with best-effort content — the gate fails loudly
